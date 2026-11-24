#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_device_bundle_v2
short_description: Create or delete a device bundle for a VM
version_added: "2.7.0"
description:
    - Create or delete a device bundle for a VM.
    - Attach a device bundle to a VM.
    - Remove a device bundle from a VM.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Attach a Device Bundle to a VM) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Remove a Device Bundle from a VM) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=virtual_machine_management)"
options:
    state:
        description:
            - Specify state.
            - If C(state) is C(present), create and attach a device bundle to the VM.
            - If C(state) is C(absent), remove the device bundle from the VM.
        type: str
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - The external ID of the device bundle of type UUID.
            - Required for delete operation.
        type: str
    vm_ext_id:
        description:
            - A globally unique identifier of a VM of type UUID.
        type: str
        required: true
    backing_info:
        description:
            - Backing information for the device bundle.
            - Required for create operation.
        type: dict
        suboptions:
            device_bundle_profile:
                description:
                    - Reference to a device bundle profile.
                    - Required for create operation.
                type: dict
                required: true
                suboptions:
                    ext_id:
                        description:
                            - A globally unique identifier of a device bundle profile of type UUID.
                        type: str
                        required: true
            assigned_instance_info:
                description:
                    - Reference to a device bundle instance.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - A globally unique identifier of a device bundle instance of type UUID.
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
- name: Create a device bundle for a VM
  nutanix.ncp.ntnx_vm_device_bundle_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vm_ext_id: "00000000-0000-0000-0000-000000000001"
    backing_info:
      device_bundle_profile:
        ext_id: "00000000-0000-0000-0000-000000000002"
  register: result

- name: Delete a device bundle from a VM
  nutanix.ncp.ntnx_vm_device_bundle_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    vm_ext_id: "00000000-0000-0000-0000-000000000001"
    ext_id: "00000000-0000-0000-0000-000000000003"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for creating or deleting a device bundle for a VM.
        - If the operation is create and C(wait) is true, it will return the task details after completion.
        - If the operation is create and C(wait) is false, it will return the task details.
        - If the operation is delete, it will return the task details.
    returned: always
    type: dict
    sample:
        {
            "backing_info": {
                "assigned_instance_info": null,
                "device_bundle_profile": {
                    "ext_id": "b2c3d4e5-6789-0abc-def1-234567890bcd"
                }
            },
            "ext_id": "c3d4e5f6-7890-abcd-ef12-34567890cdef",
            "links": null,
            "tenant_id": null
        }
task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:05b0b0c4-c1a2-5630-9db5-460e5239eef5"
ext_id:
    description: The external ID of the device bundle.
    returned: always
    type: str
    sample: "c3d4e5f6-7890-abcd-ef12-34567890cdef"
vm_ext_id:
    description: The external ID of the VM.
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000001"
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
    sample: "Device bundle with ext_id:c3d4e5f6-7890-abcd-ef12-34567890cdef will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    device_bundle_profile_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    assigned_instance_spec = dict(
        ext_id=dict(type="str"),
    )

    backing_info_spec = dict(
        device_bundle_profile=dict(
            type="dict",
            options=device_bundle_profile_spec,
            required=True,
            obj=vmm_sdk.DeviceBundleProfileReference,
        ),
        assigned_instance_info=dict(
            type="dict",
            options=assigned_instance_spec,
            required=False,
            obj=vmm_sdk.DeviceBundleInstanceReference,
        ),
    )

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
            options=backing_info_spec,
            required=False,
            obj=vmm_sdk.DeviceBundleBackingInfo,
        ),
    )
    return module_args


def create_device_bundle(module, result, api_instance):
    validate_required_params(module, ["backing_info"])

    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.DeviceBundle()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create device bundle spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_device_bundle(vmExtId=vm_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating device bundle",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def delete_device_bundle(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id

    if module.check_mode:
        result["msg"] = "Device bundle with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_device_bundle_by_id(vmExtId=vm_ext_id, extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting device bundle",
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
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_vm_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        create_device_bundle(module, result, api_instance)
    else:
        delete_device_bundle(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
