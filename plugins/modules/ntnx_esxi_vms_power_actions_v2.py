#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_esxi_vms_power_actions_v2
short_description: Perform power actions on ESXi VMs in Nutanix Prism Central
description:
    - This module allows you to perform power actions on ESXi VMs, such as powering on, powering off, resetting, suspending and more.
    - This module uses PC v4 APIs based SDKs
version_added: "2.7.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Power On ESXi Virtual Machine) -
      Required Roles: Prism Admin, Project Manager, Self-Service Admin (deprecated), Super Admin,
      Backup Admin
    - >-
      B(Power Off ESXi Virtual Machine) -
      Required Roles: Prism Admin, Project Manager, Self-Service Admin (deprecated), Super Admin,
      Backup Admin
    - >-
      B(Reset ESXi Virtual Machine) -
      Required Roles: Prism Admin, Project Manager, Self-Service Admin (deprecated), Super Admin
    - >-
      B(Suspend ESXi Virtual Machine) -
      Required Roles: Prism Admin, Project Manager, Self-Service Admin (deprecated), Super Admin
    - >-
      B(Guest Shutdown ESXi Virtual Machine) -
      Required Roles: Prism Admin, Project Manager, Self-Service Admin (deprecated), Super Admin
    - >-
      B(Guest Reboot ESXi Virtual Machine) -
      Required Roles: Prism Admin, Project Manager, Self-Service Admin (deprecated), Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - The external ID of the ESXi VM.
        type: str
        required: true
    state:
        description:
            - The desired power state of the ESXi VM.
            - power_on -> Turn on the VM.
            - power_off -> Turn off the VM.
            - reset -> Reset the VM.
            - suspend -> Suspend the VM.
            - guest_shutdown -> Shutdown the VM using NGT.
            - guest_reboot -> Reboot the VM using NGT.
        type: str
        choices:
            - power_on
            - power_off
            - reset
            - suspend
            - guest_shutdown
            - guest_reboot
        default: power_on
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        default: true
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
- name: Power on an ESXi VM
  nutanix.ncp.ntnx_esxi_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: power_on
      wait: true
  register: result

- name: Power off an ESXi VM
  nutanix.ncp.ntnx_esxi_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: power_off
      wait: true
  register: result

- name: Reset an ESXi VM
  nutanix.ncp.ntnx_esxi_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: reset
      wait: true
  register: result

- name: Suspend an ESXi VM
  nutanix.ncp.ntnx_esxi_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: suspend
      wait: true
  register: result

- name: Shutdown an ESXi VM using NGT
  nutanix.ncp.ntnx_esxi_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: guest_shutdown
      wait: true
  register: result

- name: Reboot an ESXi VM using NGT
  nutanix.ncp.ntnx_esxi_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: guest_reboot
      wait: true
  register: result
"""

RETURN = r"""
ext_id:
    description: The external ID of the ESXi VM.
    type: str
    returned: always
    sample: "0005a7b8-0b0b-4b3b-0000-000000000000"
task_ext_id:
    description: The external ID of the power action task.
    type: str
    returned: when a power action task is triggered
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"
response:
    description:
        - The task response of the power action.
        - In check mode, the response is not set.
    type: dict
    returned: always
    sample: {
        "completed_time": "2024-09-04T06:26:51.524581+00:00",
        "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
        "operation": "PowerOnVm",
        "progress_percentage": 100,
        "status": "SUCCEEDED"
    }
changed:
    description: Indicates whether the power state of the ESXi VM has changed.
    type: bool
    returned: always
    sample: true
failed:
    description: Indicates whether the power action failed.
    type: bool
    returned: always
    sample: false
skipped:
    description: Indicates whether the power action was skipped because the VM is already in the desired state.
    type: bool
    returned: when the power action is skipped
    sample: true
msg:
    description: A human-readable message about the result of the power action.
    type: str
    returned: when there is an error, the module is idempotent or in check mode
    sample: "Nothing to change."
error:
    description: The error message if an error occurred.
    type: str
    returned: when an error occurs
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
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_esxi_vm_api_instance,
    get_etag,
)
from ..module_utils.v4.vmm.helpers import get_esxi_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402,F401
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402,F401

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

POWER_ACTION_METHODS = {
    "power_on": "power_on_vm",
    "power_off": "power_off_vm",
    "reset": "reset_vm",
    "suspend": "suspend_vm",
    "guest_shutdown": "shutdown_guest_vm",
    "guest_reboot": "reboot_guest_vm",
}


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        state=dict(
            type="str",
            choices=list(POWER_ACTION_METHODS),
            default="power_on",
        ),
    )
    return module_args


def is_action_needed(power_state, state):
    """
    Check whether the requested power action changes the current power state.
    """
    if state == "power_on":
        return power_state != "ON"
    if state == "suspend":
        return power_state not in ("OFF", "SUSPENDED")
    return power_state != "OFF"


def power_actions(module, state, result):
    vmm = get_esxi_vm_api_instance(module)
    vm_ext_id = module.params["ext_id"]
    result["ext_id"] = vm_ext_id

    if module.check_mode:
        result["msg"] = (
            "ESXi VM with ext_id:{0} will have {1} action performed.".format(
                vm_ext_id, state
            )
        )
        return

    vm = get_esxi_vm(module, vmm, vm_ext_id)
    if not is_action_needed(vm.power_state, state):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag = get_etag(vm)
    kwargs = {"if_match": etag}
    resp = None
    try:
        action = getattr(vmm, POWER_ACTION_METHODS[state])
        resp = action(extId=vm_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing {0} on ESXi VM".format(state),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    # poll for the last unfinished task
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
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "ext_id": None,
    }
    state = module.params.get("state")
    power_actions(module, state, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
