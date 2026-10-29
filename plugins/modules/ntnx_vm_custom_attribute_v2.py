#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_custom_attribute_v2
short_description: Add or remove custom attributes on a VM
version_added: "2.7.0"
description:
    - Add or remove custom attributes on a VM.
    - Adds to the custom attributes of the VM.
    - Removes from the custom attributes of the VM.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Add to the VM's custom attributes) -
      Required Roles: Account Owner, Administrator, Backup Admin, Consumer, Developer, Operator,
      Prism Admin, Project Admin, Project Manager, Self-Service Admin (deprecated), Super Admin,
      Tenant Admin, Tenant Consumer, User, Virtual Machine Admin
    - >-
      B(Remove from the VM's custom attributes) -
      Required Roles: Account Owner, Administrator, Backup Admin, Consumer, Developer, Operator,
      Prism Admin, Project Admin, Project Manager, Self-Service Admin (deprecated), Super Admin,
      Tenant Admin, Tenant Consumer, User, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - Specify state.
            - If C(state) is C(present), add custom attributes to the VM.
            - If C(state) is C(absent), remove custom attributes from the VM.
        type: str
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - A globally unique identifier of a VM of type UUID.
        type: str
        required: true
    custom_attributes:
        description:
            - List of custom attributes to be added/removed.
            - A collection of user-defined key/value pairs as strings in the format C(key:value)
              representing custom attributes of the VM.
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
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    custom_attributes:
      - "environment:production"
      - "owner:engineering"
  register: result

- name: Remove custom attributes from a VM
  nutanix.ncp.ntnx_vm_custom_attribute_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    custom_attributes:
      - "environment:production"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for adding or removing custom attributes on a VM.
        - If C(wait) is true, it will contain the current list of custom attributes on the VM.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: raw
    sample:
        - "environment:production"
        - "owner:engineering"
task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
ext_id:
    description: The external ID of the VM.
    returned: always
    type: str
    sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
skipped:
    description: This indicates whether the task was skipped
    returned: when the module is idempotent
    type: bool
    sample: true
failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent
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
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402

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
            choices=["present", "absent"],
            default="present",
        ),
        ext_id=dict(type="str", required=True),
        custom_attributes=dict(
            type="list",
            elements="str",
            required=True,
        ),
    )
    return module_args


def _get_current_custom_attributes(module, api_instance, ext_id):
    vm = get_vm(module, api_instance, ext_id)
    return list(getattr(vm, "custom_attributes", None) or [])


def add_vm_custom_attributes(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    requested = module.params.get("custom_attributes") or []
    result["ext_id"] = ext_id

    if module.check_mode:
        spec = vmm_sdk.UpdateCustomAttributesParams(custom_attributes=requested)
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current = _get_current_custom_attributes(module, api_instance, ext_id)
    to_add = [attr for attr in requested if attr not in set(current)]
    spec = vmm_sdk.UpdateCustomAttributesParams(custom_attributes=to_add)

    if not to_add:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.add_vm_custom_attributes(extId=ext_id, body=spec)
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
        wait_for_completion(module, task_ext_id)
        result["response"] = _get_current_custom_attributes(
            module, api_instance, ext_id
        )
    result["changed"] = True


def remove_vm_custom_attributes(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    requested = module.params.get("custom_attributes") or []
    result["ext_id"] = ext_id

    if module.check_mode:
        spec = vmm_sdk.UpdateCustomAttributesParams(custom_attributes=requested)
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current = _get_current_custom_attributes(module, api_instance, ext_id)
    to_remove = [attr for attr in requested if attr in set(current)]
    spec = vmm_sdk.UpdateCustomAttributesParams(custom_attributes=to_remove)

    if not to_remove:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.remove_vm_custom_attributes(extId=ext_id, body=spec)
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
        wait_for_completion(module, task_ext_id)
        result["response"] = _get_current_custom_attributes(
            module, api_instance, ext_id
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
        "ext_id": None,
    }

    api_instance = get_vm_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        add_vm_custom_attributes(module, result, api_instance)
    else:
        remove_vm_custom_attributes(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
