#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vms_info
short_description: VM  info module
version_added: 1.0.0
description: 'Get vm info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: vm
    vm_uuid:
        description:
            - vm UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
"""
EXAMPLES = r"""
  - name: List VMS using name filter criteria
    ntnx_vms_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
         vm_name: "{{ vm.name }}"
      kind: vm
    register: result

  - name: List VMS using length, offset, sort order and vm_name sort attribute
    ntnx_vms_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      length: 1
      offset: 1
      sort_order: "ASCENDING"
      sort_attribute: "vm_name"
    register: result

"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: Metadata for vm list output
  returned: always
  type: dict
  sample: {
    "metadata": {
            "kind": "vm",
            "length": 11,
            "offset": 0,
            "sort_attribute": "vm_name",
            "sort_order": "ASCENDING",
            "total_matches": 11
        }
        }
entities:
  description: VM intent response
  returned: always
  type: list
  sample: {
    "entities": [
            {
                "metadata": {
                    "categories": {},
                    "categories_mapping": {},
                    "creation_time": "2022-03-09T08:37:32Z",
                    "entity_version": "2",
                    "kind": "vm",
                    "last_update_time": "2022-03-09T08:37:32Z",
                    "owner_reference": {
                        "kind": "user",
                        "name": "admin",
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "project_reference": {
                        "kind": "project",
                        "name": "default",
                        "uuid": "3972d1c5-e015-40e4-b9d2-5ae296e654e3"
                    },
                    "spec_version": 0,
                    "uuid": "d9ead770-467d-4cfb-af65-83b7d0f857ad"
                },
                "spec": {
                    "cluster_reference": {
                        "kind": "cluster",
                        "name": "auto_cluster_prod_1a642ea0a5c3",
                        "uuid": "0005d734-09d4-0462-185b-ac1f6b6f97e2"
                    },
                    "name": "integration_test_vm",
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
                        "hardware_virtualization_enabled": false,
                        "is_agent_vm": false,
                        "machine_type": "PC",
                        "memory_size_mib": 4096,
                        "nic_list": [
                            {
                                "ip_endpoint_list": [
                                    {
                                        "ip": "192.168.1.13",
                                        "type": "ASSIGNED"
                                    }
                                ],
                                "is_connected": true,
                                "mac_address": "50:6b:8d:39:d3:41",
                                "nic_type": "NORMAL_NIC",
                                "secondary_ip_address_list": [],
                                "subnet_reference": {
                                    "kind": "subnet",
                                    "name": "integration_test_overlay_subnet",
                                    "uuid": "b4f341e5-d2b5-4bc2-8652-2b547acaf21a"
                                },
                                "trunked_vlan_list": [],
                                "uuid": "020e0ac4-1e5e-483b-879a-f0266f3d93a3",
                                "vlan_mode": "ACCESS"
                            }
                        ],
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
                },
                "status": {
                    "cluster_reference": {
                        "kind": "cluster",
                        "name": "auto_cluster_prod_1a642ea0a5c3",
                        "uuid": "0005d734-09d4-0462-185b-ac1f6b6f97e2"
                    },
                    "execution_context": {
                        "task_uuids": [
                            "e66a0754-3cb4-4028-9a2d-b9122b29f6fc"
                        ]
                    },
                    "name": "integration_test_vm",
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
                        "hardware_virtualization_enabled": false,
                        "host_reference": {
                            "kind": "host",
                            "name": "10.46.136.28",
                            "uuid": "e16b6989-a149-4f93-989f-bc3e96f88a40"
                        },
                        "hypervisor_type": "AHV",
                        "is_agent_vm": false,
                        "machine_type": "PC",
                        "memory_size_mib": 4096,
                        "nic_list": [
                            {
                                "ip_endpoint_list": [
                                    {
                                        "ip": "192.168.1.13",
                                        "type": "ASSIGNED"
                                    }
                                ],
                                "is_connected": true,
                                "mac_address": "50:6b:8d:39:d3:41",
                                "nic_type": "NORMAL_NIC",
                                "secondary_ip_address_list": [],
                                "subnet_reference": {
                                    "kind": "subnet",
                                    "name": "integration_test_overlay_subnet",
                                    "uuid": "b4f341e5-d2b5-4bc2-8652-2b547acaf21a"
                                },
                                "trunked_vlan_list": [],
                                "uuid": "020e0ac4-1e5e-483b-879a-f0266f3d93a3",
                                "vlan_mode": "ACCESS"
                            }
                        ],
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
                        "storage_config": {},
                        "vga_console_enabled": true,
                        "vnuma_config": {
                            "num_vnuma_nodes": 0
                        }
                    },
                    "state": "COMPLETE"
                }
            }
        ],
        }
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.vms import VM  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    """Extend base argument spec"""

    module_args = dict(
        vm_uuid=dict(type="str"),
        kind=dict(type="str", default="vm"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )
    return module_args


def get_vm(module, result):
    vm = VM(module)
    vm_uuid = module.params.get("vm_uuid")
    resp = vm.read(vm_uuid)

    result["response"] = resp


def get_vms(module, result):
    vm = VM(module)
    spec, error = vm.get_info_spec()

    resp = vm.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("vm_uuid"):
        get_vm(module, result)
    else:
        get_vms(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
