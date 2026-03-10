#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_projects_v2
short_description: Create, update, and delete projects in Nutanix Prism Central using v4 APIs.
version_added: "2.6.0"
description:
    - Create, update, and delete projects in Nutanix Prism Central.
    - Projects are logical grouping constructs that organize resources across the Nutanix platform.
    - This module uses the v4 multidomain API.
options:
    ext_id:
        description:
            - The external ID of the project.
            - Required for update and delete operations.
        type: str
    name:
        description:
            - Name of the project.
            - Required for create operations.
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
- name: Create a project
  nutanix.ncp.ntnx_projects_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    wait: true
    name: "my-project"
    project_id: "my-project-id"
    description: "A test project"
  register: result

- name: Update a project
  nutanix.ncp.ntnx_projects_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    wait: true
    ext_id: "{{ project_ext_id }}"
    name: "my-project-updated"
    description: "Updated description"
  register: result

- name: Delete a project
  nutanix.ncp.ntnx_projects_v2:
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
        - The project response object.
        - Will contain the project details after create or update when C(wait) is true.
        - Will contain task details when C(wait) is false.
    returned: always
    type: dict
    sample: {
        "name": "my-project",
        "description": "A test project",
        "id": "my-project-id",
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "state": "ACTIVE",
        "is_system_defined": false,
        "is_default": false
    }
changed:
    description: Whether the state of the project was changed.
    returned: always
    type: bool
    sample: true
ext_id:
    description: The external ID of the project.
    returned: when available
    type: str
    sample: "00000000-0000-0000-0000-000000000000"
task_ext_id:
    description: The external ID of the task created for the operation.
    returned: when a task is created
    type: str
    sample: "00000000-0000-0000-0000-000000000000"
skipped:
    description: Whether the operation was skipped due to no changes.
    returned: when idempotency check determines no update needed
    type: bool
    sample: true
msg:
    description: Additional message about the operation.
    returned: when applicable
    type: str
    sample: "Project with ext_id:xxx will be deleted."
"""

import traceback  # noqa: E402
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
)

SDK_IMP_ERROR = None
try:
    import ntnx_multidomain_py_client as multidomain_sdk  # noqa: E402
except ImportError:
    multidomain_sdk = None
    SDK_IMP_ERROR = traceback.format_exc()


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        project_id=dict(type="str"),
    )
    return module_args


def create_project(module, result):
    projects = get_projects_api_instance(module)
    sg = SpecGenerator(module)
    default_spec = multidomain_sdk.Project()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create project spec", **result
        )

    project_id = module.params.get("project_id")
    if project_id:
        spec.id = project_id

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


def update_project(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    projects = get_projects_api_instance(module)

    current_spec = get_project(module, projects, ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update project spec", **result
        )

    project_id = module.params.get("project_id")
    if project_id:
        update_spec.id = project_id

    if check_project_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = projects.update_project_by_id(extId=ext_id, body=update_spec)
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
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_project(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    projects = get_projects_api_instance(module)

    if module.check_mode:
        result["msg"] = "Project with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    current_spec = get_project(module, projects, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting project", **result
        )

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


def check_project_idempotency(old_spec, update_spec):
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    return old_spec == update_spec


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
    result = {"changed": False, "response": None, "ext_id": None}
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_project(module, result)
        else:
            create_project(module, result)
    else:
        delete_project(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
