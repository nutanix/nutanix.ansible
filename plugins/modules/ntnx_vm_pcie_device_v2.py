#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_pcie_device_v2
short_description: Create or Delete a PCIe device on a Nutanix AHV VM
version_added: 2.5.0
description:
  - This module allows you to create (attach) and delete (detach) a PCIe passthrough device on an existing AHV VM in Nutanix Prism Central.
  - The PCIe device is referenced through the cluster-level PCIe device C(ext_id) discovered via the clustermgmt v4 API.
  - The Nutanix VMM v4 API does not expose an update endpoint for PCIe devices.
  - Providing C(ext_id) with C(state=present) is therefore a no-op and returns C(skipped=true).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a PCIe device for a VM) -
      Required Roles: Account Owner, Administrator, Consumer, Developer, Operator, Prism Admin, Project Admin, Project Manager, Super Admin, User,
      Virtual Machine Admin, Self-Service Admin (deprecated)
    - >-
      B(Remove a PCIe device from a VM) -
      Required Roles: Account Owner, Administrator, Consumer, Developer, Operator, Prism Admin, Project Admin, Project Manager, Super Admin, User,
      Virtual Machine Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - If C(state) is set to C(present) and no C(ext_id) is supplied, a new PCIe device is attached to the VM.
      - If C(state) is set to C(present) and C(ext_id) is supplied, the module is a no-op
        (PCIe devices cannot be updated in-place); the module returns C(skipped=true).
      - If C(state) is set to C(absent), the PCIe device with the given C(ext_id) is detached from the VM.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the PCIe device attached to the VM.
      - Required for delete operation.
    type: str
    required: false
  vm_ext_id:
    description:
      - The external ID (UUID) of the parent VM.
    type: str
    required: true
  backing_info:
    description:
      - Indicates the way a PCIe device is associated to the VM.
      - This corresponds to the C(PcieDeviceReference) discriminator of the C(backing_info) one-of field.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      device_ext_id:
        description:
          - Globally unique identifier denoting a physical PCIe device on the host / cluster.
          - Discover valid values via the Prism Central clustermgmt v4 C(pcie-devices) API.
          - Required for create operation.
        type: str
        required: false
  assigned_device_info:
    description:
      - Information about the currently attached PCIe device on the VM.
      - This field is populated by the server on read; providing it on create is optional and typically not required.
    type: dict
    required: false
    suboptions:
      device:
        description:
          - Reference to the PCIe device.
        type: dict
        required: false
        suboptions:
          device_ext_id:
            description:
              - Globally unique identifier denoting the PCIe device label (UUID).
            type: str
            required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Attach a PCIe device to a VM
  nutanix.ncp.ntnx_vm_pcie_device_v2:
    state: present
    vm_ext_id: "c4d28fba-7adb-46b4-5495-01d795d8260b"
    backing_info:
      device_ext_id: "348d4ecb-9ec9-55e6-ad06-5ec88eee87c0"
  register: result
  ignore_errors: true

- name: Detach a PCIe device from a VM
  nutanix.ncp.ntnx_vm_pcie_device_v2:
    state: absent
    vm_ext_id: "c4d28fba-7adb-46b4-5495-01d795d8260b"
    ext_id: "0e6d0dcc-a7e4-47a5-54eb-d58396649a49"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating or deleting a PCIe device on a VM.
    - If the operation is create and C(wait) is true, it will return the PCIe device details.
    - If the operation is create and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "assigned_device_info": null,
      "backing_info": {
        "device_ext_id": "348d4ecb-9ec9-55e6-ad06-5ec88eee87c0"
      },
      "ext_id": "0e6d0dcc-a7e4-47a5-54eb-d58396649a49",
      "links": null,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:05b0b0c4-c1a2-5630-9db5-460e5239eef5"

ext_id:
  description:
    - The external ID of the PCIe device attached to the VM.
  returned: always
  type: str
  sample: "0e6d0dcc-a7e4-47a5-54eb-d58396649a49"

vm_ext_id:
  description:
    - The external ID of the parent VM.
  returned: always
  type: str
  sample: "c4d28fba-7adb-46b4-5495-01d795d8260b"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the operation was skipped (e.g. PCIe device update is not supported by the SDK).
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message from the module.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "PCIe device update is not supported by the SDK. Nothing to change."
"""

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
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_pcie_device, get_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as virtual_machine_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as virtual_machine_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    pcie_device_reference_spec = dict(
        device_ext_id=dict(type="str", required=False),
    )

    pcie_device_info_spec = dict(
        device=dict(
            type="dict",
            options=pcie_device_reference_spec,
            required=False,
            obj=virtual_machine_management_sdk.PcieDeviceReference,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        vm_ext_id=dict(type="str", required=True),
        backing_info=dict(
            type="dict",
            options=pcie_device_reference_spec,
            required=False,
            obj=virtual_machine_management_sdk.PcieDeviceReference,
        ),
        assigned_device_info=dict(
            type="dict",
            options=pcie_device_info_spec,
            required=False,
            obj=virtual_machine_management_sdk.PcieDeviceInfo,
        ),
    )
    return module_args


def _find_new_pcie_device(module, api_instance, vm_ext_id, device_ext_id):
    """List PCIe devices on the VM and return the ext_id of the newly created
    device whose ``backing_info.device_ext_id`` matches ``device_ext_id``.

    The ``CreatePcieDevice`` task's ``entities_affected`` only references the
    parent VM, so we cannot rely on ``get_entity_ext_id_from_task`` to return
    the PCIe device ext_id. Falling back to a targeted list lets us return the
    real resource details to the user.
    """
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


def create_PcieDevice(module, result, api_instance):
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id

    validate_required_params(module, ["backing_info"])
    backing_info = module.params.get("backing_info") or {}
    if not backing_info.get("device_ext_id"):
        module.fail_json(
            msg=(
                "Missing required parameter(s): backing_info.device_ext_id "
                "(needed to attach a physical PCIe device to the VM)."
            ),
            **result,
        )

    sg = SpecGenerator(module)
    default_spec = virtual_machine_management_sdk.PcieDevice()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create VM PCIe device spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vm = get_vm(module, api_instance, vm_ext_id)
    etag = get_etag(vm)
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.create_pcie_device(vmExtId=vm_ext_id, body=spec, **kwargs)
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
            ext_id = _find_new_pcie_device(
                module,
                api_instance,
                vm_ext_id,
                backing_info.get("device_ext_id"),
            )
        if ext_id:
            result["ext_id"] = ext_id
            pcie = get_pcie_device(module, api_instance, ext_id, vm_ext_id)
            result["response"] = strip_internal_attributes(pcie.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to determine ext_id of the newly created PCIe device on VM {0}".format(
                        vm_ext_id
                    )
                ),
                msg="Failed to get entity ext_id from task for VM PCIe device",
            )

    result["changed"] = True


def update_PcieDevice(module, result, api_instance):
    """PCIe device update is not supported by the VMM v4 SDK.

    Providing ``ext_id`` alongside ``state=present`` is treated as an
    idempotent no-op and the module exits with ``skipped=True`` after
    verifying the existing device.
    """
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id

    pcie = get_pcie_device(module, api_instance, ext_id, vm_ext_id)
    result["response"] = strip_internal_attributes(pcie.to_dict())
    result["skipped"] = True
    module.exit_json(
        msg=(
            "PCIe device update is not supported by the VMM v4 SDK. "
            "Existing device with ext_id '{0}' left unchanged.".format(ext_id)
        ),
        **result,
    )


def delete_PcieDevice(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id

    if module.check_mode:
        result["msg"] = "PCIe device with ext_id:{0} on VM {1} will be deleted.".format(
            ext_id, vm_ext_id
        )
        return

    vm = get_vm(module, api_instance, vm_ext_id)
    etag = get_etag(vm)
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.delete_pcie_device_by_id(
            vmExtId=vm_ext_id, extId=ext_id, **kwargs
        )
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
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
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
        "response": None,
        "failed": False,
        "ext_id": None,
        "vm_ext_id": None,
        "skipped": False,
    }
    api_instance = get_vm_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_PcieDevice(module, result, api_instance)
        else:
            create_PcieDevice(module, result, api_instance)
    else:
        delete_PcieDevice(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
