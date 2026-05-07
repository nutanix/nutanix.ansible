#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_resource_group_v2
short_description: Manage resource groups in Nutanix Prism Central using v4 APIs
version_added: "2.6.0"
description:
    - Create, update, and delete resource groups in Nutanix Prism Central.
    - Resource groups define placement targets (clusters and storage containers)
      where resources within a project can be deployed.
    - This module uses PC v4 APIs based SDKs.
options:
    state:
        description:
            - Specify state.
            - If C(state) is set to C(present) then the module will create a resource group.
            - If C(state) is set to C(present) and C(ext_id) is given, then the module will update the resource group.
            - If C(state) is set to C(absent) with C(ext_id), then the module will delete the resource group.
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
            - The external ID of the resource group.
            - Required for C(state)=absent for delete.
            - Required for C(state)=present to trigger update of resource group.
        type: str
    name:
        description:
            - Name of the resource group.
            - Required for create operations.
            - Maximum 64 characters.
        type: str
    project_ext_id:
        description:
            - UUID of the project that owns this resource group.
        type: str
    placement_targets:
        description:
            - List of placement targets defining where resources can be deployed.
        type: list
        elements: dict
        suboptions:
            cluster_ext_id:
                description:
                    - UUID of the AOS cluster.
                type: str
            storage_containers:
                description:
                    - List of storage containers available for this cluster target.
                type: list
                elements: dict
                suboptions:
                    ext_id:
                        description:
                            - UUID of the storage container.
                        type: str
    capabilities:
        description:
            - Capabilities and features for this resource group.
            - Each item is a key-value pair.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The key of the key-value pair.
                type: str
            value:
                description:
                    - The value associated with the key.
                type: raw
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create a resource group with placement targets
  nutanix.ncp.ntnx_resource_group_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "my-resource-group"
    project_ext_id: "78945612-3579-11e9-8647-d663bd873d93"
    placement_targets:
      - cluster_ext_id: "00064c46-8fef-6895-185b-ac1f6b6f97e2"
  register: result

- name: Update a resource group name
  nutanix.ncp.ntnx_resource_group_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "93673459-0234-4789-a123-456789012345"
    name: "my-resource-group-updated"
  register: result

- name: Delete a resource group
  nutanix.ncp.ntnx_resource_group_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "93673459-0234-4789-a123-456789012345"
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC Resource Groups v4 API.
        - It will contain the resource group details after create or update when C(wait) is true.
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
    description: The external ID of the resource group.
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
    get_resource_groups_api_instance,
)
from ..module_utils.v4.multidomain.helpers import get_resource_group  # noqa: E402
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    kv_pair_spec = dict(
        name=dict(type="str"),
        value=dict(type="raw"),
    )

    storage_container_spec = dict(
        ext_id=dict(type="str"),
    )

    placement_target_spec = dict(
        cluster_ext_id=dict(type="str"),
        storage_containers=dict(
            type="list",
            elements="dict",
            options=storage_container_spec,
            obj=multidomain_sdk.StorageContainerDetails,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        project_ext_id=dict(type="str"),
        placement_targets=dict(
            type="list",
            elements="dict",
            options=placement_target_spec,
            obj=multidomain_sdk.TargetDetails,
        ),
        capabilities=dict(
            type="list",
            elements="dict",
            options=kv_pair_spec,
            obj=multidomain_sdk.KVPair,
        ),
    )
    return module_args


def create_resource_group(module, resource_groups, result):
    validate_required_params(module, ["name"])

    sg = SpecGenerator(module)
    default_spec = multidomain_sdk.ResourceGroup()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create resource group spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = resource_groups.create_resource_group(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating resource group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.RESOURCE_GROUP
        )
        if ext_id:
            resp = get_resource_group(module, resource_groups, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_resource_group_idempotency(old_spec, update_spec):
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    if old_spec != update_spec:
        return False
    return True


def update_resource_group(module, resource_groups, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_resource_group(module, resource_groups, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating resource group", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update resource group spec", **result)

    if check_resource_group_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    kwargs = {"if_match": etag}
    try:
        resp = resource_groups.update_resource_group_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating resource group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_resource_group(module, resource_groups, ext_id)
        result["ext_id"] = ext_id
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_resource_group(module, resource_groups, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Resource group with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_resource_group(module, resource_groups, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting resource group", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = resource_groups.delete_resource_group_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting resource group",
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

    resource_groups = get_resource_groups_api_instance(module)

    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_resource_group(module, resource_groups, result)
        else:
            create_resource_group(module, resource_groups, result)
    else:
        delete_resource_group(module, resource_groups, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
