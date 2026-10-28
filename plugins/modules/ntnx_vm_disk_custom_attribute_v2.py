#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_disk_custom_attribute_v2
short_description: Add or remove custom attributes on an AHV VM disk in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to add or remove custom attributes (user-defined C(key:value)
    metadata strings) on an individual AHV VM disk in Nutanix Prism Central.
  - When C(state=present), the provided C(custom_attributes) are added to the VM disk.
  - When C(state=absent), the provided C(custom_attributes) are removed from the VM disk.
  - VM disks backed by Volume Groups and CD-ROMs are not eligible for disk-level custom attributes.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Update Virtual Machine Disk Custom Attributes) -
    Required Roles: Account Owner, Administrator, User, Consumer, Developer,
    Operator, Prism Admin, Project Admin, Project Manager,
    Self-Service Admin (deprecated), Super Admin, Virtual Machine Admin,
    Backup Admin, Tenant Admin, Tenant Consumer
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - Specify the desired action.
      - If C(state) is set to C(present), the provided C(custom_attributes) are added to the VM disk.
      - If C(state) is set to C(absent), the provided C(custom_attributes) are removed from the VM disk.
    type: str
    choices:
      - present
      - absent
    default: present
  vm_ext_id:
    description:
      - The external ID of the VM whose disk is being updated.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the VM disk on which custom attributes are added or removed.
    type: str
    required: true
  custom_attributes:
    description:
      - List of custom attributes to be added or removed on the VM disk.
      - Each item is a string in C(key:value) format
        (for example C(environment:production), C(tier:gold)).
      - Keys must match the API pattern for custom attributes (lowercase key, optional value).
      - Maximum of 64 attributes per request.
      - For C(state=present), the module adds only those attributes which are not already present.
      - For C(state=absent), the module removes only those attributes which are currently present.
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
- name: Add custom attributes to a VM disk
  nutanix.ncp.ntnx_vm_disk_custom_attribute_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    ext_id: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"
    custom_attributes:
      - "environment:production"
      - "tier:gold"
      - "owner:ansible"
  register: result
  ignore_errors: true

- name: Remove custom attributes from a VM disk
  nutanix.ncp.ntnx_vm_disk_custom_attribute_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    ext_id: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"
    custom_attributes:
      - "tier:gold"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for adding or removing custom attributes on a VM disk.
    - VM disk details (including the resulting C(custom_attributes) list) if C(wait) is true.
    - Task details if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "backing_info": {
        "data_source": null,
        "disk_ext_id": "0f34a2a7-6068-48ba-859d-1ced14d7f5da",
        "disk_size_bytes": 26843545600,
        "is_migration_in_progress": false,
        "storage_config": null,
        "storage_container": {
          "ext_id": "78ec68c5-d9b0-4ba4-a3e9-96f90d580a0b"
        }
      },
      "custom_attributes": [
        "environment:production",
        "tier:gold",
        "owner:ansible"
      ],
      "disk_address": {
        "bus_type": "SCSI",
        "index": 1
      },
      "ext_id": "0f34a2a7-6068-48ba-859d-1ced14d7f5da",
      "links": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent
  type: str
  sample: "Nothing to change."

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

skipped:
  description: This indicates whether the task was skipped
  returned: when the module is idempotent
  type: bool
  sample: true

task_ext_id:
  description: The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

vm_ext_id:
  description: The external ID of the VM.
  returned: always
  type: str
  sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"

ext_id:
  description: The external ID of the VM disk.
  returned: always
  type: str
  sample: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"
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
from ..module_utils.v4.vmm.helpers import get_disk  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        custom_attributes=dict(
            type="list",
            elements="str",
            required=True,
        ),
    )
    return module_args


def _get_disk_custom_attributes(module, api_instance, vm_ext_id, ext_id):
    """Return the current custom_attributes list on a VM disk (empty list if none)."""
    disk = get_disk(module, api_instance, ext_id=ext_id, vm_ext_id=vm_ext_id)
    current = getattr(disk, "custom_attributes", None) or []
    return list(current), disk


def _build_spec(attributes):
    return vmm_sdk.UpdateCustomAttributesParams(custom_attributes=attributes)


def add_vm_disk_custom_attributes(module, result, api_instance):
    vm_ext_id = module.params.get("vm_ext_id")
    ext_id = module.params.get("ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    requested = list(module.params.get("custom_attributes") or [])
    current, disk = _get_disk_custom_attributes(module, api_instance, vm_ext_id, ext_id)

    to_add = [attr for attr in requested if attr not in current]
    spec = _build_spec(to_add)

    if not to_add:
        result["skipped"] = True
        result["response"] = strip_internal_attributes(disk.to_dict())
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.add_vm_disk_custom_attributes(
            vmExtId=vm_ext_id, extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while adding custom attributes to VM disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        updated_disk = get_disk(
            module, api_instance, ext_id=ext_id, vm_ext_id=vm_ext_id
        )
        result["response"] = strip_internal_attributes(updated_disk.to_dict())
    result["changed"] = True


def remove_vm_disk_custom_attributes(module, result, api_instance):
    vm_ext_id = module.params.get("vm_ext_id")
    ext_id = module.params.get("ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    requested = list(module.params.get("custom_attributes") or [])
    current, disk = _get_disk_custom_attributes(module, api_instance, vm_ext_id, ext_id)

    to_remove = [attr for attr in requested if attr in current]
    spec = _build_spec(to_remove)

    if not to_remove:
        result["skipped"] = True
        result["response"] = strip_internal_attributes(disk.to_dict())
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.remove_vm_disk_custom_attributes(
            vmExtId=vm_ext_id, extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while removing custom attributes from VM disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        updated_disk = get_disk(
            module, api_instance, ext_id=ext_id, vm_ext_id=vm_ext_id
        )
        result["response"] = strip_internal_attributes(updated_disk.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "vm_ext_id": None,
        "ext_id": None,
    }
    api_instance = get_vm_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        add_vm_disk_custom_attributes(module, result, api_instance)
    else:
        remove_vm_disk_custom_attributes(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
