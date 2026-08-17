#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_custom_attribute_v2
short_description: Add or remove custom attributes on a VM or a VM disk in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to add or remove user-defined custom attributes
    (key/value string tags) on an AHV VM, or on a specific VM disk, in
    Nutanix Prism Central.
  - Each custom attribute is a string in the strict format C(key:value)
    (e.g. C(environment:production)).
  - If C(disk_ext_id) is provided, the operation is performed on the specified
    VM disk. Otherwise it is performed on the VM.
  - If C(state) is set to C(present), the supplied custom attributes are added.
  - If C(state) is set to C(absent), the supplied custom attributes are removed.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Add / Remove VM custom attributes) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin (with C(Update_Virtual_Machine_Custom_Attributes) permission).
    - >-
      B(Add / Remove VM disk custom attributes) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin (with C(Update_Virtual_Machine_Disk_Custom_Attributes) permission).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - If C(state) is set to C(present), the supplied custom attributes are added to the VM (or VM disk).
      - If C(state) is set to C(absent), the supplied custom attributes are removed from the VM (or VM disk).
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  vm_ext_id:
    description:
      - The external ID of the VM on which custom attributes should be added or removed.
    type: str
    required: true
  disk_ext_id:
    description:
      - The external ID of the VM disk on which custom attributes should be added or removed.
      - When provided, custom attributes are added / removed on the disk rather than on the VM itself.
      - Volume Group backed disks and CD-ROMs are not eligible for disk custom attributes.
    type: str
    required: false
  custom_attributes:
    description:
      - A list of user-defined custom attributes as strings in the C(key:value) format
        (for example C(environment:production), C(owner:engineering)).
      - For C(state=present), the module will add only those attributes which are not already present.
      - For C(state=absent), the module will remove only those attributes which are currently present.
    type: list
    elements: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Add custom attributes to a VM
  nutanix.ncp.ntnx_vm_custom_attribute_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    custom_attributes:
      - "environment:production"
      - "owner:engineering"
  register: result
  ignore_errors: true

- name: Add custom attributes to a specific VM disk
  nutanix.ncp.ntnx_vm_custom_attribute_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    disk_ext_id: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"
    custom_attributes:
      - "storageclass:premium"
      - "backup:daily"
  register: result
  ignore_errors: true

- name: Remove custom attributes from a VM
  nutanix.ncp.ntnx_vm_custom_attribute_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    custom_attributes:
      - "environment:production"
  register: result
  ignore_errors: true

- name: Remove custom attributes from a specific VM disk
  nutanix.ncp.ntnx_vm_custom_attribute_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    disk_ext_id: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"
    custom_attributes:
      - "backup:daily"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for adding or removing custom attributes on the VM or the VM disk.
    - If C(wait) is true, contains the final task details after the action completes.
    - If C(wait) is false, contains the initial task response returned when the action is triggered.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T06:26:51.524581+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T06:26:47.167906+00:00",
      "entities_affected": [
        {
          "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
          "rel": "vmm:ahv:config:vm"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T06:26:51.524581+00:00",
      "legacy_error_message": null,
      "operation": "AddVmCustomAttributes",
      "operation_description": "Add VM Custom Attributes",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-21T06:26:47.185754+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task associated with the add/remove custom attributes action.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

vm_ext_id:
  description:
    - The external ID of the VM on which custom attributes were added or removed.
  returned: always
  type: str
  sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"

disk_ext_id:
  description:
    - The external ID of the VM disk on which custom attributes were added or removed.
  returned: when C(disk_ext_id) is provided
  type: str
  sample: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"

ext_id:
  description:
    - The external ID of the entity on which the action was performed.
    - Matches C(vm_ext_id) when acting on a VM, otherwise matches C(disk_ext_id) when acting on a VM disk.
  returned: always
  type: str
  sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"

custom_attributes:
  description:
    - The current list of custom attributes on the target VM (or VM disk) after the action, when C(wait) is true.
  returned: when C(wait) is true and the action succeeds
  type: list
  elements: str
  sample:
    - "environment:production"
    - "owner:engineering"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped because there was nothing to change.
  returned: when the operation is a no-op
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Status / informational message returned by the module.
  returned: When there is an error, module is idempotent, or in check mode
  type: str
  sample: "Nothing to change."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_disk, get_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(
            type="str",
            required=False,
            default="present",
            choices=["present", "absent"],
        ),
        vm_ext_id=dict(type="str", required=True),
        disk_ext_id=dict(type="str", required=False),
        custom_attributes=dict(
            type="list",
            elements="str",
            required=True,
        ),
    )
    return module_args


def _get_current_vm_custom_attributes(module, api_instance, vm_ext_id):
    """Return the current list of custom attributes on the VM (or [] if none)."""
    vm = get_vm(module, api_instance, vm_ext_id)
    return list(getattr(vm, "custom_attributes", None) or [])


def _get_current_disk_custom_attributes(module, api_instance, vm_ext_id, disk_ext_id):
    """Return the current list of custom attributes on the VM disk (or [] if none)."""
    disk = get_disk(module, api_instance, disk_ext_id, vm_ext_id)
    return list(getattr(disk, "custom_attributes", None) or [])


def _diff_add(requested, current):
    """Return the subset of requested attributes not already present in current."""
    current_set = set(current)
    return [attr for attr in requested if attr not in current_set]


def _diff_remove(requested, current):
    """Return the subset of requested attributes actually present in current."""
    current_set = set(current)
    return [attr for attr in requested if attr in current_set]


def _build_spec(attributes):
    return vmm_sdk.UpdateCustomAttributesParams(custom_attributes=attributes)


def add_VmCustomAttribute(module, result, api_instance):
    vm_ext_id = module.params.get("vm_ext_id")
    disk_ext_id = module.params.get("disk_ext_id")
    requested = module.params.get("custom_attributes") or []

    result["vm_ext_id"] = vm_ext_id
    if disk_ext_id:
        result["disk_ext_id"] = disk_ext_id
        result["ext_id"] = disk_ext_id
        current = _get_current_disk_custom_attributes(
            module, api_instance, vm_ext_id, disk_ext_id
        )
    else:
        result["ext_id"] = vm_ext_id
        current = _get_current_vm_custom_attributes(module, api_instance, vm_ext_id)

    to_add = _diff_add(requested, current)
    spec = _build_spec(to_add)

    if not to_add:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        if disk_ext_id:
            resp = api_instance.add_vm_disk_custom_attributes(
                vmExtId=vm_ext_id, extId=disk_ext_id, body=spec
            )
        else:
            resp = api_instance.add_vm_custom_attributes(extId=vm_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while adding VM custom attributes",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        if disk_ext_id:
            result["custom_attributes"] = _get_current_disk_custom_attributes(
                module, api_instance, vm_ext_id, disk_ext_id
            )
        else:
            result["custom_attributes"] = _get_current_vm_custom_attributes(
                module, api_instance, vm_ext_id
            )

    result["changed"] = True


def remove_VmCustomAttribute(module, result, api_instance):
    vm_ext_id = module.params.get("vm_ext_id")
    disk_ext_id = module.params.get("disk_ext_id")
    requested = module.params.get("custom_attributes") or []

    result["vm_ext_id"] = vm_ext_id
    if disk_ext_id:
        result["disk_ext_id"] = disk_ext_id
        result["ext_id"] = disk_ext_id
        current = _get_current_disk_custom_attributes(
            module, api_instance, vm_ext_id, disk_ext_id
        )
    else:
        result["ext_id"] = vm_ext_id
        current = _get_current_vm_custom_attributes(module, api_instance, vm_ext_id)

    to_remove = _diff_remove(requested, current)
    spec = _build_spec(to_remove)

    if not to_remove:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        if disk_ext_id:
            resp = api_instance.remove_vm_disk_custom_attributes(
                vmExtId=vm_ext_id, extId=disk_ext_id, body=spec
            )
        else:
            resp = api_instance.remove_vm_custom_attributes(extId=vm_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while removing VM custom attributes",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        if disk_ext_id:
            result["custom_attributes"] = _get_current_disk_custom_attributes(
                module, api_instance, vm_ext_id, disk_ext_id
            )
        else:
            result["custom_attributes"] = _get_current_vm_custom_attributes(
                module, api_instance, vm_ext_id
            )

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)

    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "vm_ext_id": None,
        "disk_ext_id": None,
        "ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_vm_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        add_VmCustomAttribute(module, result, api_instance)
    else:
        remove_VmCustomAttribute(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
