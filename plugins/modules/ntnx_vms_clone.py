#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vms_clone
short_description: VM module which supports VM clone operations
version_added: 1.0.2
description: "This creates a new vm by cloning the current vm "

extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_opperations
      - nutanix.ncp.ntnx_vms_base
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: clone vm  with check mode
  ntnx_vms_clone:
      vm_uuid: "{{ vm.vm_uuid }}"
      networks:
        - is_connected: false
          subnet:
            name: "{{ network.dhcp.name }}"
  register: result
  ignore_errors: true
  check_mode: yes

- name: clone vm  and change vcpus,memory_gb,cores_per_vcpu,timezone,desc,name with force_power_off
  ntnx_vms_clone:
      vm_uuid: "{{ vm.vm_uuid }}"
      vcpus: 2
      cores_per_vcpu: 2
      memory_gb: 2
      name: cloned vm
      desc: cloned vm
      timezone: GMT
      force_power_off: true

- name: clone vm and add network
  ntnx_vms_clone:
      vm_uuid: "{{ vm.vm_uuid }}"
      networks:
        - is_connected: true
          subnet:
            uuid: "{{ network.dhcp.uuid }}"
        - is_connected: true
          subnet:
            uuid: "{{ static.uuid }}"

- name: clone vm  with script 
  ntnx_vms_clone:
      vm_uuid: "{{ vm.vm_uuid }}"
      guest_customization:
        type: "cloud_init"
        script_path: "./cloud_init.yml"
        is_overridable: True
  register: result
"""

RETURN = r"""
"""


from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.vms import VM  # noqa: E402
from ..module_utils import utils


def clone_vm(module, result):
    vm_uuid = module.params["vm_uuid"]

    vm = VM(module)

    spec, error = vm.get_clone_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating VM Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = vm.clone(spec)

    result["changed"] = True
    result["response"] = resp
    result["task_uuid"] = resp["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = vm.read(vm_uuid)
        result["response"] = resp


def wait_for_task_completion(module, result, raise_error=True):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid, raise_error=raise_error)
    result["response"] = resp
    if not result.get("vm_uuid") and resp.get("entity_reference_list"):
        result["vm_uuid"] = resp["entity_reference_list"][0]["uuid"]


def run_module():
    module = BaseModule(supports_check_mode=True)
    utils.remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_uuid": None,
        "task_uuid": None,
    }
    clone_vm(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
