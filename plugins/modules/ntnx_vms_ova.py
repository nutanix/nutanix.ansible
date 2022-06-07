#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vms_ova
short_description: VM module which supports ova creation
version_added: 1.2.0
description: "Creates an ova entity"
options:
  src_vm_uuid:
    description: VM UUID
    required: true
    type: str
  name:
      description:
        - Name of the OVA
      required: true
      type: str
  file_format:
      description:
        - File format of disk in OVA
      required: true
      type: str
      choices:
        - QCOW2
        - VMDK
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: create_ova_image  with check mode
  ntnx_vms_ova:
      src_vm_uuid: "{{ vm.vm_uuid }}"
      name: integration_test_VMDK_ova
      file_format: VMDK
  register: result
  ignore_errors: true
  check_mode: yes

- name: create QCOW2 ova_image
  ntnx_vms_ova:
      src_vm_uuid: "{{ vm.vm_uuid }}"
      name: integration_test_QCOW2_ova
      file_format: QCOW2
  register: result
  ignore_errors: true

- name: create VMDK ova_image
  ntnx_vms_ova:
      src_vm_uuid: "{{ vm.vm_uuid }}"
      name: integration_test_VMDK_ova
      file_format: VMDK
  register: result
  ignore_errors: true
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The ova metadata
  returned: always
  type: dict
  sample: {
    "categories": {},
    "categories_mapping": {},
    "creation_time": "2022-04-10T09:43:32Z",
    "entity_version": "2",
    "kind": "vm",
    "last_update_time": "2022-04-10T09:43:32Z",
    "owner_reference": {
        "kind": "user",
        "name": "admin",
        "uuid": "00000000-0000-0000-0000-000000000000"
    },
    "project_reference": {
        "kind": "project",
        "name": "default",
        "uuid": "37e22e5c-a914-4213-83e5-105123b8b5cf"
    },
    "spec_version": 0,
    "uuid": "dded1b87-e566-419a-aac0-fb282792fb83"
}
spec:
  description: An intentful representation of an ova spec
  returned: always
  type: dict
  sample: {
    "cluster_reference": {
    "kind": "cluster",
    "name": "auto_cluster_prod_4f4433c72b64",
    "uuid": "0005dc0f-13a7-62e0-185b-ac1f6b6f97e2"
},
"name": "integration_test_ova_vm",
"resources": {
    "boot_config": {
        "boot_device_order_list": [
            "CDROM",
            "DISK",
            "NETWORK"
        ],
        "boot_type": "LEGACY"
    },
    "disk_list": [],
    "gpu_list": [],
    "hardware_clock_timezone": "UTC",
    "is_agent_vm": false,
    "machine_type": "PC",
    "memory_size_mib": 4096,
    "nic_list": [],
    "num_sockets": 1,
    "num_threads_per_core": 1,
    "num_vcpus_per_socket": 1,
    "power_state": "ON",
    "power_state_mechanism": {
        "guest_transition_config": {
            "enable_script_exec": false,
            "should_fail_on_script_failure": false
        },
        "mechanism": "HARD"
    },
    "serial_port_list": [],
    "vga_console_enabled": true,
    "vnuma_config": {
        "num_vnuma_nodes": 0
    }
}
}
status:
  description: An intentful representation of an ova status
  returned: always
  type: dict
  sample: {
                "cluster_reference": {
                    "kind": "cluster",
                    "name": "auto_cluster_prod_4f4433c72b64",
                    "uuid": "0005dc0f-13a7-62e0-185b-ac1f6b6f97e2"
                },
                "execution_context": {
                    "task_uuid": [
                        "56471800-3702-4894-ab5d-b272f52f6352"
                    ]
                },
                "name": "integration_test_ova_vm",
                "resources": {
                    "boot_config": {
                        "boot_device_order_list": [
                            "CDROM",
                            "DISK",
                            "NETWORK"
                        ],
                        "boot_type": "LEGACY"
                    },
                    "disk_list": [],
                    "gpu_list": [],
                    "hardware_clock_timezone": "UTC",
                    "host_reference": {
                        "kind": "host",
                        "name": "10.46.136.28",
                        "uuid": "c91be067-9885-4cbb-92cc-876242c0c396"
                    },
                    "hypervisor_type": "AHV",
                    "is_agent_vm": false,
                    "machine_type": "PC",
                    "memory_size_mib": 4096,
                    "nic_list": [],
                    "num_sockets": 1,
                    "num_threads_per_core": 1,
                    "num_vcpus_per_socket": 1,
                    "power_state": "ON",
                    "power_state_mechanism": {
                        "guest_transition_config": {
                            "enable_script_exec": false,
                            "should_fail_on_script_failure": false
                        },
                        "mechanism": "HARD"
                    },
                    "protection_type": "UNPROTECTED",
                    "serial_port_list": [],
                    "vga_console_enabled": true,
                    "vnuma_config": {
                        "num_vnuma_nodes": 0
                    }
                },
                "state": "COMPLETE"
            }
src_vm_uuid:
  description: The vm uuid
  returned: always
  type: str
  sample: "64c5a93d-7cd4-45f9-81e9-e0b08d35077a"
task_uuid:
  description: The task uuid for the ova creation
  returned: always
  type: str
  sample: "f83bbb29-3ca8-42c2-b29b-4fca4a7a25c3"
"""


from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.vms import VM  # noqa: E402


def get_module_spec():
    module_args = dict(
        src_vm_uuid=dict(type="str", required=True),
        name=dict(type="str", required=True),
        file_format=dict(type="str", choices=["QCOW2", "VMDK"], required=True),
    )

    return module_args


def create(module, result):
    src_vm_uuid = module.params["src_vm_uuid"]

    vm = VM(module)
    spec = vm.get_ova_image_spec()
    result["src_vm_uuid"] = src_vm_uuid

    if module.check_mode:
        result["response"] = spec
        return

    resp = vm.create_ova_image(spec)

    result["changed"] = True
    result["response"] = resp
    result["task_uuid"] = resp["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = vm.read(src_vm_uuid)
        result["response"] = resp


def wait_for_task_completion(module, result, raise_error=True):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid, raise_error=raise_error)
    result["response"] = resp
    if not result.get("vm_uuid") and resp.get("entity_reference_list"):
        result["vm_uuid"] = resp["entity_reference_list"][0]["uuid"]


def run_module():
    module = BaseModule(argument_spec=get_module_spec(), supports_check_mode=True)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_uuid": None,
        "src_vm_uuid": None,
        "task_uuid": None,
    }
    create(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
