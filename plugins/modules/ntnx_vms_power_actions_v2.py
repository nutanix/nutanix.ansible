#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vms_power_actions_v2
short_description: Perform power actions on Nutanix VMs
description:
    - This module allows you to perform power actions on Nutanix VMs, such as powering on, powering off, resetting, and more.
options:
    ext_id:
        description:
            - The external ID of the VM.
        type: str
        required: true
    state:
        description:
            - The desired power state of the VM.
            - power_on -> Turn on the VM.
            - power_off -> Turn off the VM.
            - force_power_cycle -> Forcefully power cycle the VM.
            - reset -> Reset the VM.
            - shutdown -> Shutdown the VM using ACPI.
            - guest_shutdown -> Shutdown the VM using NGT.
            - reboot -> Reboot the VM using ACPI.
            - guest_reboot -> Reboot the VM using NGT.
        type: str
        choices:
            - power_on
            - power_off
            - force_power_cycle
            - reset
            - shutdown
            - guest_shutdown
            - reboot
            - guest_reboot
        default: power_on
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        default: true
    guest_power_state_transition_config:
        description:
            - Configuration options for guest power state transition.
        type: dict
        suboptions:
            should_enable_script_exec:
                description:
                    - Indicates whether to run the set script before the VM shutdowns/restarts.
                type: bool
            should_fail_on_script_failure:
                description:
                    - Indicates whether to abort VM shutdown/restart if the script fails.
                type: bool
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Prem Karat (@premkarat)
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""

- name: Power on a VM
  ntnx_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: power_on
      wait: true
  register: result

- name: Power off a VM
  ntnx_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: power_off
      wait: true
  register: result

- name: Reset a VM
  ntnx_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: reset
      wait: true
  register: result

- name: Shutdown a VM using ACPI
  ntnx_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: shutdown
      wait: true
  register: result

- name: Shutdown a VM using NGT
  ntnx_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: guest_shutdown
      wait: true
  register: result

- name: Reboot a VM using ACPI
  ntnx_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: reboot
      wait: true
  register: result

- name: Reboot a VM using NGT
  ntnx_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: guest_reboot
      wait: true
      guest_power_state_transition_config:
          should_enable_script_exec: true
          should_fail_on_script_failure: true
  register: result

- name: Power on a VM with guest power state transition configuration
  ntnx_vms_power_actions_v2:
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
      state: power_on
      wait: true
      guest_power_state_transition_config:
          should_enable_script_exec: true
          should_fail_on_script_failure: true
  register: result
"""

RETURN = r"""
ext_id:
    description: The external ID of the VM.
    type: str
    returned: always
    sample: "0005a7b8-0b0b-4b3b-0000-000000000000"
task_ext_id:
    description: The external ID of the power action task.
    type: str
    returned: when a power action task is triggered
response:
    description: The response from the power action task.
    type: dict
    returned: always
    sample: {"status": "success"}
changed:
    description: Indicates whether the power state of the VM has changed.
    type: bool
    returned: always
    sample: true
skipped:
    description: Indicates whether the power action was skipped because the VM is already in the desired state.
    type: bool
    returned: when the power action is skipped
msg:
    description: A human-readable message about the result of the power action.
    type: str
    returned: always
    sample: "Power on action completed successfully."
"""

import traceback  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


def get_module_spec():
    guest_power_state_transition_config = dict(
        should_enable_script_exec=dict(type="bool"),
        should_fail_on_script_failure=dict(type="bool"),
    )
    module_args = dict(
        ext_id=dict(type="str", required=True),
        state=dict(
            type="str",
            choices=[
                "power_on",
                "power_off",
                "force_power_cycle",
                "reset",
                "shutdown",
                "guest_shutdown",
                "reboot",
                "guest_reboot",
            ],
            default="power_on",
        ),
        guest_power_state_transition_config=dict(
            type="dict",
            options=guest_power_state_transition_config,
            obj=vmm_sdk.GuestPowerStateTransitionConfig,
        ),
    )
    return module_args


def power_actions(module, state, result):
    vmm = get_vm_api_instance(module)
    vm_ext_id = module.params["ext_id"]
    result["ext_id"] = vm_ext_id
    if module.check_mode or state == "guest_shutdown" or state == "guest_reboot":
        sg = SpecGenerator(module)
        default_spec = vmm_sdk.GuestPowerOptions()
        spec, err = sg.generate_spec(obj=default_spec)
        if err:
            result["error"] = err
            module.fail_json(msg="Failed generating spec for guest reboot vm", **result)
        if module.check_mode:
            result["response"] = strip_internal_attributes(spec.to_dict())
            return

    vm = get_vm(module, vmm, vm_ext_id)
    if (vm.power_state == "ON" and state == "power_on") or (
        vm.power_state == "OFF" and state != "power_on"
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)
        return
    etag = get_etag(vm)
    kwargs = {"if_match": etag}
    resp = None
    try:
        if state == "power_on":
            resp = vmm.power_on_vm(extId=vm_ext_id, **kwargs)

        elif state == "power_off":
            resp = vmm.power_off_vm(extId=vm_ext_id, **kwargs)

        elif state == "force_power_cycle":
            resp = vmm.power_cycle_vm(extId=vm_ext_id, **kwargs)

        elif state == "reset":
            resp = vmm.reset_vm(extId=vm_ext_id, **kwargs)

        elif state == "shutdown":
            resp = vmm.shutdown_vm(extId=vm_ext_id, **kwargs)

        elif state == "guest_shutdown":
            resp = vmm.shutdown_guest_vm(extId=vm_ext_id, body=spec, **kwargs)

        elif state == "reboot":
            resp = vmm.reboot_vm(extId=vm_ext_id, **kwargs)

        elif state == "guest_reboot":
            resp = vmm.reboot_guest_vm(extId=vm_ext_id, body=spec, **kwargs)

        else:
            result["error"] = "Action is not supported"
            module.fail_json(msg="Action is not supported", **result)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Failed to ${state} VM",
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
    module = BaseModule(
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
        "error": None,
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
