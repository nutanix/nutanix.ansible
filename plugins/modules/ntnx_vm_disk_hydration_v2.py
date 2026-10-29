#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_disk_hydration_v2
short_description: Enable or disable hydration for a VM disk
version_added: "2.7.0"
description:
    - Enable or disable hydration for a VM disk.
    - Enable a VM disk to be hydrated to the local storage container in the background.
    - If the VM disk hydration has been disabled, this will resume the hydration process.
    - Disable hydration for a VM disk.
    - The hydration process will be stopped and the disk will not be migrated to the local storage container.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Enable hydration for a VM disk) -
      Required Roles: Account Owner, Administrator, Backup Admin, Cluster Admin, Consumer, Developer,
      Disaster Recovery Admin, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin,
      Project Manager, Self-Service Admin (deprecated), Storage Admin, Super Admin, User, VPC Admin,
      Virtual Machine Admin
    - >-
      B(Disable hydration for a VM disk) -
      Required Roles: Account Owner, Administrator, Backup Admin, Cluster Admin, Consumer, Developer,
      Disaster Recovery Admin, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin,
      Project Manager, Self-Service Admin (deprecated), Storage Admin, Super Admin, User, VPC Admin,
      Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - Specify state.
            - If C(state) is C(present), enable hydration for the VM disk.
            - If C(state) is C(absent), disable hydration for the VM disk.
        type: str
        choices:
            - present
            - absent
        default: present
    vm_ext_id:
        description:
            - A globally unique identifier of a VM of type UUID.
        type: str
        required: true
    ext_id:
        description:
            - A globally unique identifier of a VM disk of type UUID.
        type: str
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
- name: Enable hydration for a VM disk
  nutanix.ncp.ntnx_vm_disk_hydration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    ext_id: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"
  register: result

- name: Disable hydration for a VM disk
  nutanix.ncp.ntnx_vm_disk_hydration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    ext_id: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for enabling or disabling hydration for a VM disk.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: dict
    sample:
        {
            "completed_time": "2027-01-12T05:31:44.875612+00:00",
            "created_time": "2027-01-12T05:31:44.382175+00:00",
            "entities_affected": [
                {
                    "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
                    "rel": "vmm:ahv:config:vm"
                },
                {
                    "ext_id": "0f34a2a7-6068-48ba-859d-1ced14d7f5da",
                    "rel": "vmm:ahv:config:vm:disk"
                }
            ],
            "ext_id": "ZXJnb24=:d0eba95b-5ac1-5564-9be7-7137a82214ab",
            "operation": "EnableVmDiskHydration",
            "progress_percentage": 100,
            "status": "SUCCEEDED"
        }
task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:d0eba95b-5ac1-5564-9be7-7137a82214ab"
ext_id:
    description: The external ID of the VM disk.
    returned: always
    type: str
    sample: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"
vm_ext_id:
    description: The external ID of the VM.
    returned: always
    type: str
    sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "Hydration will be enabled for VM disk with ext_id:0f34a2a7-6068-48ba-859d-1ced14d7f5da."
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

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client  # noqa: E402, F401  # pylint: disable=unused-import
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(
            type="str",
            choices=["present", "absent"],
            default="present",
        ),
        vm_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def enable_vm_disk_hydration(module, result, api_instance):
    vm_ext_id = module.params.get("vm_ext_id")
    ext_id = module.params.get("ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Hydration will be enabled for VM disk with ext_id:{0}.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.enable_vm_disk_hydration(vmExtId=vm_ext_id, extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while enabling hydration for VM disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def disable_vm_disk_hydration(module, result, api_instance):
    vm_ext_id = module.params.get("vm_ext_id")
    ext_id = module.params.get("ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Hydration will be disabled for VM disk with ext_id:{0}.".format(ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.disable_vm_disk_hydration(vmExtId=vm_ext_id, extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disabling hydration for VM disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
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
        enable_vm_disk_hydration(module, result, api_instance)
    else:
        disable_vm_disk_hydration(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
