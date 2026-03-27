#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_project_v2
short_description: Manage projects in Nutanix Prism Central using v4 APIs
version_added: "2.6.0"
description:
    - Create, update, and delete projects in Nutanix Prism Central.
    - Projects are logical grouping constructs that organize resources across the Nutanix platform.
    - This module uses PC v4 APIs based SDKs.
options:
    state:
        description:
            - Specify state.
            - If C(state) is set to C(present) then the module will create a project.
            - If C(state) is set to C(present) and C(ext_id) is given, then the module will update the project.
            - If C(state) is set to C(absent) with C(ext_id), then the module will delete the project.
        choices:
            - present
            - absent
        type: str
        default: present
    wait:
        description: Wait for the operation to complete.
        type: bool
        required: false
        default: True
    ext_id:
        description:
            - The external ID of the project.
            - Required for C(state)=absent for delete.
            - Required for C(state)=present to trigger update of project.
        type: str
    name:
        description:
            - Name of the project.
            - Required for create operations.
            - This field is immutable and cannot be updated after creation.
            - Must be between 1 and 64 characters.
        type: str
    description:
        description:
            - Description of the project.
            - Maximum 1024 characters.
        type: str
    project_id:
        description:
            - Unique human-readable ID for the project.
            - Required for create operations.
            - Must be between 1 and 64 characters.
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create a project with all fields
  nutanix.ncp.ntnx_project_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    wait: true
    name: "my-project"
    project_id: "my-project-id"
    description: "A test project created via Ansible"
  register: result

- name: Update a project description
  nutanix.ncp.ntnx_project_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    wait: true
    ext_id: "{{ project_ext_id }}"
    description: "Updated description"
  register: result

- name: Delete a project
  nutanix.ncp.ntnx_project_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    wait: true
    ext_id: "{{ project_ext_id }}"
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC Projects v4 API.
        - It will contain the project details after create or update when C(wait) is true.
        - It will contain task details when C(wait) is false.
    returned: always
    type: dict
    sample: "<Need to add sample>"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

ext_id:
    description: The external ID of the project.
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000000"

task_ext_id:
    description: The external ID of the task created for the operation.
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000000"

skipped:
    description: Whether the operation was skipped due to no changes (idempotency).
    returned: When module is idempotent
    type: bool
    sample: true

msg:
    description: Additional message about the operation.
    returned: When there is an error, module is idempotent or check mode (in delete operation)
    type: str
    sample: "Nothing to change."

error:
    description: This field holds information about errors that occurred during the task execution.
    returned: When an error occurs
    type: str

failed:
    description: This indicates whether the task failed.
    returned: When something fails
    type: bool
    sample: true
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.multidomain.api_client import (  # noqa: E402
    get_etag,
    get_projects_api_instance,
)
from ..module_utils.v4.multidomain.helpers import get_project  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_multidomain_py_client as multidomain_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as multidomain_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        project_id=dict(type="str"),
    )
    return module_args


def create_project(module, projects, result):
    validate_required_params(module, ["name", "project_id"])

    sg = SpecGenerator(module)
    default_spec = multidomain_sdk.Project()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create project spec", **result)

    project_id = module.params.get("project_id")
    if project_id:
        spec.id = project_id

    # SpecGenerator picks up Ansible's 'state' param ("present"/"absent")
    # and sets it on the SDK object; reset to None so the API does not
    # receive an invalid enum value.
    spec.state = None

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = projects.create_project(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating project",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.PROJECT
        )
        if ext_id:
            resp = get_project(module, projects, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_project_idempotency(old_spec, update_spec):
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    if old_spec != update_spec:
        return False
    return True


def _clear_read_only_fields(spec):
    """
    Clear server-managed read-only fields on an SDK Project spec so they
    are omitted from the serialized PUT body (the SDK excludes None attrs).
    """
    spec.created_timestamp = None
    spec.modified_timestamp = None
    spec.created_by = None
    spec.updated_by = None
    spec.is_system_defined = None
    spec.is_default = None
    spec.ext_id = None
    spec.links = None
    spec.tenant_id = None


def update_project(module, projects, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_project(module, projects, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for updating project", **result)

    # Preserve original state before SpecGenerator overwrites it
    original_state = current_spec.state

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update project spec", **result)

    project_id = module.params.get("project_id")
    if project_id:
        update_spec.id = project_id

    # Restore original state so that Ansible's "present"/"absent"
    # does not leak into the API payload.
    update_spec.state = original_state

    if check_project_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    # Clear server-managed read-only fields before sending to API
    _clear_read_only_fields(update_spec)

    resp = None
    kwargs = {"if_match": etag}
    try:
        resp = projects.update_project_by_id(extId=ext_id, body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating project",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_project(module, projects, ext_id)
        result["ext_id"] = ext_id
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_project(module, projects, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Project with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_project(module, projects, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for deleting project", **result)

    kwargs = {"if_match": etag}

    try:
        resp = projects.delete_project_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting project",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_multidomain_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }

    projects = get_projects_api_instance(module)

    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_project(module, projects, result)
        else:
            create_project(module, projects, result)
    else:
        delete_project(module, projects, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
