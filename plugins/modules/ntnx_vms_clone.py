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
version_added: 1.2.0
description: "This creates a new vm by cloning the current vm "

extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
      - nutanix.ncp.ntnx_vms_base
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: clone vm  with check mode
  ntnx_vms_clone:
      src_vm_uuid: "{{ vm.vm_uuid }}"
      networks:
        - is_connected: false
          subnet:
            name: "{{ network.dhcp.name }}"
  check_mode: yes

- name: clone vm  and change vcpus,memory_gb,cores_per_vcpu,timezone,desc,name with force_power_off
  ntnx_vms_clone:
      src_vm_uuid: "{{ vm.vm_uuid }}"
      vcpus: 2
      cores_per_vcpu: 2
      memory_gb: 2
      name: cloned vm
      desc: cloned vm
      timezone: GMT
      force_power_off: true

- name: clone vm and add network
  ntnx_vms_clone:
      src_vm_uuid: "{{ vm.vm_uuid }}"
      networks:
        - is_connected: true
          subnet:
            uuid: "{{ network.dhcp.uuid }}"
        - is_connected: true
          subnet:
            uuid: "{{ static.uuid }}"

- name: clone vm  with script
  ntnx_vms_clone:
      src_vm_uuid: "{{ vm.vm_uuid }}"
      guest_customization:
        type: "cloud_init"
        script_path: "./cloud_init.yml"
        is_overridable: True
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The vm kind metadata
  returned: always
  type: dict
  sample: {
"categories": {},
"categories_mapping": {},
"creation_time": "2022-04-13T08:14:05Z",
"entity_version": "2",
"kind": "vm",
"last_update_time": "2022-04-13T08:14:05Z",
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
"uuid": "47ff23df-5a63-4800-810c-7f4e18efc14b"
}
spec:
  description: An intentful representation of a vm spec
  returned: always
  type: dict
  sample: {

                "cluster_reference": {
                    "kind": "cluster",
                    "name": "auto_cluster_prod_4f4433c72b64",
                    "uuid": "0005dc0f-13a7-62e0-185b-ac1f6b6f97e2"
                },
                "name": "integration_test_clone_vm",
                "resources": {
                    "boot_config": {
                        "boot_device_order_list": [
                            "CDROM",
                            "DISK",
                            "NETWORK"
                        ],
                        "boot_type": "LEGACY"
                    },
                    "disk_list": [
                        {
                            "data_source_reference": {
                                "kind": "image",
                                "uuid": "7cb304dd-9ccf-4295-a516-3b922964df08"
                            },
                            "device_properties": {
                                "device_type": "DISK",
                                "disk_address": {
                                    "adapter_type": "SCSI",
                                    "device_index": 0
                                }
                            },
                            "disk_size_bytes": 21474836480,
                            "disk_size_mib": 20480,
                            "storage_config": {
                                "storage_container_reference": {
                                    "kind": "storage_container",
                                    "name": "SelfServiceContainer",
                                    "uuid": "d53867d9-81ef-43a4-b157-15cf7602426e"
                                }
                            },
                            "uuid": "ea16feb9-4a40-48fc-a929-4b362767d2d8"
                        }
                    ],
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
  description: An intentful representation of a vm status
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
                        "053f487c-ebc9-4e96-84e4-ec40b3dd043d"
                    ]
                },
                "name": "integration_test_clone_vm",
                "resources": {
                    "boot_config": {
                        "boot_device_order_list": [
                            "CDROM",
                            "DISK",
                            "NETWORK"
                        ],
                        "boot_type": "LEGACY"
                    },
                    "disk_list": [
                        {
                            "data_source_reference": {
                                "kind": "image",
                                "uuid": "7cb304dd-9ccf-4295-a516-3b922964df08"
                            },
                            "device_properties": {
                                "device_type": "DISK",
                                "disk_address": {
                                    "adapter_type": "SCSI",
                                    "device_index": 0
                                }
                            },
                            "disk_size_bytes": 21474836480,
                            "disk_size_mib": 20480,
                            "is_migration_in_progress": false,
                            "storage_config": {
                                "storage_container_reference": {
                                    "kind": "storage_container",
                                    "name": "SelfServiceContainer",
                                    "uuid": "d53867d9-81ef-43a4-b157-15cf7602426e"
                                }
                            },
                            "uuid": "ea16feb9-4a40-48fc-a929-4b362767d2d8"
                        }
                    ],
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
  description: The cloned vm uuid
  returned: always
  type: str
  sample: "2b011db0-4d44-43e3-828a-d0a32dab340c"
task_uuid:
  description: The task uuid for the clone
  returned: always
  type: str
  sample: "82c5c1d3-eb6a-406a-8f58-306028099d21"
"""

from copy import deepcopy

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.default_vm_spec import DefaultVMSpec  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.vms import VM  # noqa: E402


def get_module_spec():
    default_vm_spec = deepcopy(DefaultVMSpec.vm_argument_spec)
    default_vm_spec.pop("vm_uuid")
    default_vm_spec.update(src_vm_uuid=dict(type="str", required=True))

    return default_vm_spec


def clone_vm(module, result):
    src_vm_uuid = module.params["src_vm_uuid"]

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
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True
    )
    utils.remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_uuid": None,
        "src_vm_uuid": None,
        "task_uuid": None,
    }
    clone_vm(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
