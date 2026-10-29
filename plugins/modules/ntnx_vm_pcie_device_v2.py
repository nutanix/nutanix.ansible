#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_pcie_device_v2
short_description: Create or delete a PCIe device for a VM
version_added: "2.7.0"
description:
    - Create or delete a PCIe device for a VM.
    - Creates and attaches a PCIe device to a virtual machine.
    - Removes the specified PCIe device from a virtual machine.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Create a PCIe device for a VM) -
      Required Roles: Account Owner, Administrator, Consumer, Developer, Operator, Prism Admin,
      Project Admin, Project Manager, Self-Service Admin (deprecated), Super Admin, Tenant Admin,
      Tenant Consumer, User, Virtual Machine Admin
    - >-
      B(Remove a PCIe device from a VM) -
      Required Roles: Account Owner, Administrator, Consumer, Developer, Operator, Prism Admin,
      Project Admin, Project Manager, Self-Service Admin (deprecated), Super Admin, Tenant Admin,
      Tenant Consumer, User, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - Specify state.
            - If C(state) is C(present), create and attach a PCIe device to the VM.
            - If C(state) is C(absent), remove the PCIe device from the VM.
        type: str
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - Globally unique identifier of a PCIe device of type UUID.
            - Required for delete.
        type: str
    vm_ext_id:
        description:
            - A globally unique identifier of a VM of type UUID.
        type: str
        required: true
    backing_info:
        description:
            - Indicates the way a PCIe device is associated to the VM.
            - Required for create.
        type: dict
        suboptions:
            device_ext_id:
                description:
                    - Globally unique identifier denoting PCIe device label. It should be of type UUID.
                type: str
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
- name: Create a PCIe device for a VM
  nutanix.ncp.ntnx_vm_pcie_device_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vm_ext_id: "c4d28fba-7adb-46b4-5495-01d795d8260b"
    backing_info:
      device_ext_id: "348d4ecb-9ec9-55e6-ad06-5ec88eee87c0"
  register: result

- name: Delete a PCIe device from a VM
  nutanix.ncp.ntnx_vm_pcie_device_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    vm_ext_id: "c4d28fba-7adb-46b4-5495-01d795d8260b"
    ext_id: "0e6d0dcc-a7e4-47a5-54eb-d58396649a49"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for creating or deleting a PCIe device for a VM.
        - If the operation is create and C(wait) is true, it will return the PCIe device details.
        - If the operation is create and C(wait) is false, it will return the task details.
        - If the operation is delete, it will return the task details.
    returned: always
    type: dict
    sample:
        {
            "backing_info": {
                "device_ext_id": "348d4ecb-9ec9-55e6-ad06-5ec88eee87c0"
            },
            "ext_id": "0e6d0dcc-a7e4-47a5-54eb-d58396649a49"
        }
task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:05b0b0c4-c1a2-5630-9db5-460e5239eef5"
ext_id:
    description: The external ID of the PCIe device.
    returned: always
    type: str
    sample: "0e6d0dcc-a7e4-47a5-54eb-d58396649a49"
vm_ext_id:
    description: The external ID of the VM.
    returned: always
    type: str
    sample: "c4d28fba-7adb-46b4-5495-01d795d8260b"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
error:
    description: This indicates the error message if any error occurred
    returned: when an error occurs
    type: str
failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "PCIe device with ext_id:0e6d0dcc-a7e4-47a5-54eb-d58396649a49 will be deleted."
"""

import copy  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_pcie_device  # noqa: E402

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
        ext_id=dict(type="str"),
        vm_ext_id=dict(type="str", required=True),
        backing_info=dict(
            type="dict",
            options=dict(
                device_ext_id=dict(type="str"),
            ),
            obj=vmm_sdk.PcieDeviceReference,
        ),
    )
    return module_args


def _find_pcie_device_ext_id(module, api_instance, vm_ext_id, device_ext_id):
    try:
        resp = api_instance.list_pcie_devices_by_vm_id(vmExtId=vm_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing VM PCIe devices",
        )
    for pcie in resp.data or []:
        backing = getattr(pcie, "backing_info", None)
        if (
            backing is not None
            and getattr(backing, "device_ext_id", None) == device_ext_id
        ):
            return pcie.ext_id
    return None


def create_pcie_device(module, result, api_instance):
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id

    if not module.params.get("backing_info"):
        module.fail_json(msg="Missing required parameter: backing_info", **result)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.PcieDevice()
    create_params = copy.deepcopy(module.params)
    create_params.pop("ext_id", None)
    create_params.pop("vm_ext_id", None)
    create_params.pop("state", None)
    spec, err = sg.generate_spec(obj=default_spec, attr=create_params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create VM PCIe device spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_pcie_device(vmExtId=vm_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating VM PCIe device",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.PCIE_DEVICE
        )
        if not ext_id:
            backing_info = module.params.get("backing_info") or {}
            ext_id = _find_pcie_device_ext_id(
                module,
                api_instance,
                vm_ext_id,
                backing_info.get("device_ext_id"),
            )
        if ext_id:
            result["ext_id"] = ext_id
            pcie = get_pcie_device(module, api_instance, ext_id, vm_ext_id)
            result["response"] = strip_internal_attributes(pcie.to_dict())
    result["changed"] = True


def delete_pcie_device(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id

    if module.check_mode:
        result["msg"] = "PCIe device with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_pcie_device_by_id(vmExtId=vm_ext_id, extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting VM PCIe device",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("backing_info",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_vm_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        create_pcie_device(module, result, api_instance)
    else:
        delete_pcie_device(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
