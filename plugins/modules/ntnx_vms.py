#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vms
short_description: VM module which suports VM CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete, Power-on, Power-off Nutanix VM''s'
options:
  name:
    description: VM Name
    required: false
    type: str
  vm_uuid:
    description: VM UUID
    type: str
  desc:
    description: A description for VM.
    required: false
    type: str
  project:
    description: Name or UUID of the project
    required: false
    type: dict
    suboptions:
      name:
        description:
          - Project Name
          - Mutually exclusive with C(uuid)
        type: str
      uuid:
        description:
          - Project UUID
          - Mutually exclusive with C(name)
        type: str
  cluster:
    description:
      - Name or UUID of the cluster on which the VM will be placed
    type: dict
    required: false
    suboptions:
      name:
        description:
          - Cluster Name
          - Mutually exclusive with C(uuid)
        type: str
      uuid:
        description:
          - Cluster UUID
          - Mutually exclusive with C(name)
        type: str
  vcpus:
    description:
      - Number of sockets
    required: false
    type: int
    default: 1
  cores_per_vcpu:
    description:
      - This is the number of vcpus per socket
    required: false
    type: int
    default: 1
  memory_gb:
    description:
      - Memory size in GB
    required: false
    type: int
    default: 1
  networks:
    description:
      - list of subnets to which the VM needs to connect to
    type: list
    elements: dict
    required: false
    suboptions:
      subnet:
        description:
          - Name or UUID of the subnet to which the VM should be connnected
        type: dict
        suboptions:
          name:
            description:
              - Subnet Name
              - Mutually exclusive with C(uuid)
            type: str
          uuid:
            description:
              - Subnet UUID
              - Mutually exclusive with C(name)
            type: str
      private_ip:
        description:
          - Optionally assign static IP to the VM
        type: str
        required: false
      is_connected:
        description:
          - Connect or disconnect the VM to the subnet
        type: bool
        required: false
        default: true
  disks:
    description:
      - List of disks attached to the VM
    type: list
    elements: dict
    suboptions:
      type:
        description:
          - CDROM or DISK
        choices:
          - CDROM
          - DISK
        default: DISK
        type: str
      size_gb:
        description:
          - The Disk Size in GB.
          - This option is applicable for only DISK type above.
        type: int
      bus:
        description: Bus type of the device
        default: SCSI
        choices:
          - SCSI
          - PCI
          - SATA
          - IDE
        type: str
      storage_container:
        description:
          - Mutually exclusive with C(clone_image) and C(empty_cdrom)
        type: dict
        suboptions:
          name:
            description:
              - Storage containter Name
              - Mutually exclusive with C(uuid)
            type: str
          uuid:
            description:
              - Storage container UUID
              - Mutually exclusive with C(name)
            type: str
      clone_image:
        description:
          - Mutually exclusive with C(storage_container) and C(empty_cdrom)
        type: dict
        suboptions:
          name:
            description:
              - Image Name
              - Mutually exclusive with C(uuid)
            type: str
          uuid:
            description:
              - Image UUID
              - Mutually exclusive with C(name)
            type: str
      empty_cdrom:
        type: bool
        description:
          - Mutually exclusive with C(clone_image) and C(storage_container)
  boot_config:
    description:
      - >-
        Indicates whether the VM should use Secure boot, UEFI boot or Legacy
        boot.
    type: dict
    required: false
    suboptions:
      boot_type:
        description:
          - Boot type of VM.
        choices:
          - LEGACY
          - UEFI
          - SECURE_BOOT
        default: LEGACY
        type: str
      boot_order:
        description:
          - Applicable only for LEGACY boot_type
          - Boot device order list
        type: list
        elements: str
        default:
          - CDROM
          - DISK
          - NETWORK
  guest_customization:
    description:
      - cloud_init or sysprep guest customization
    type: dict
    suboptions:
      type:
        description:
          - cloud_init or sysprep type
        type: str
        required: True
        choices:
          - cloud_init
          - sysprep
      script_path:
        description:
          - Absolute file path to the script.
        type: path
        required: true
      is_overridable:
        description:
          - Flag to allow override of customization during deployment.
        type: bool
        default: false
        required: false
  timezone:
    description:
      - VM's hardware clock timezone in IANA TZDB format (America/Los_Angeles).
    type: str
    default: UTC
    required: false
  categories:
    description:
      - categories to be attached to the VM.
    type: dict
    required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_opperations
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
"""

EXAMPLES = r"""
  - name: VM with CentOS-7-cloud-init image
    ntnx_vms:
      state: present
      name: VM with CentOS-7-cloud-init image
      timezone: "UTC"
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      cluster:
        name: "{{ cluster_name }}"
      disks:
        - type: "DISK"
          size_gb: 10
          clone_image:
            name:  "{{ centos }}"
          bus: "SCSI"
      guest_customization:
        type: "cloud_init"
        script_path: "./cloud_init.yml"
        is_overridable: True

  - name: VM with Cluster, Network, Universal time zone, one Disk
    ntnx_vms:
      state: present
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      name: "VM with Cluster Network and Disk"
      timezone: "Universal"
      cluster:
        name: "{{ cluster_name }}"
      networks:
        - is_connected: True
          subnet:
            name: "{{ network_name }}"
      disks:
        - type: "DISK"
          size_gb: 10
          bus: "PCI"

  - name: VM with Cluster, different CDROMs
    ntnx_vms:
      state: present
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      name: "VM with multiple CDROMs"
      cluster:
        name: "{{ cluster_name }}"
      disks:
        - type: "CDROM"
          bus: "SATA"
          empty_cdrom: True
        - type: "CDROM"
          bus: "IDE"
          empty_cdrom: True
      cores_per_vcpu: 1

  - name: VM with diffrent disk types and diffrent sizes with UEFI boot type
    ntnx_vms:
      state: present
      name: VM with UEFI boot type
      timezone: GMT
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      cluster:
        name: "{{ cluster_name }}"
      categories:
        AppType:
          - Apache_Spark
      disks:
        - type: "DISK"
          clone_image:
            name: "{{ ubuntu }}"
          bus: "SCSI"
          size_gb: 20
        - type: DISK
          size_gb: 1
          bus: SCSI
        - type: DISK
          size_gb: 2
          bus: PCI
          storage_container:
            name: "{{ storage_container_name }}"
        - type: DISK
          size_gb: 3
          bus: SATA
      boot_config:
        boot_type: UEFI
        boot_order:
          - DISK
          - CDROM
          - NETWORK
      vcpus: 2
      cores_per_vcpu: 1
      memory_gb: 1

  - name: VM with managed and unmanaged network
    ntnx_vms:
      state: present
      name: VM_NIC
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      timezone: UTC
      cluster:
        name: "{{ cluster.name }}"
      networks:
        - is_connected: true
          subnet:
            uuid: "{{ network.dhcp.uuid }}"
        - is_connected: true
          subnet:
            uuid: "{{ network.static.uuid }}"
      disks:
        - type: DISK
          size_gb: 1
          bus: SCSI
        - type: DISK
          size_gb: 3
          bus: PCI
        - type: CDROM
          bus: SATA
          empty_cdrom: True
        - type: CDROM
          bus: IDE
          empty_cdrom: True
      boot_config:
        boot_type: UEFI
        boot_order:
          - DISK
          - CDROM
          - NETWORK
      vcpus: 2
      cores_per_vcpu: 2
      memory_gb: 2

  - name: Delete VM
    ntnx_vms:
      state: absent
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      vm_uuid: '{{ vm_uuid }}'
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
                "categories": {
                    "AppType": "Apache_Spark"
                },
                "categories_mapping": {
                    "AppType": [
                        "Apache_Spark"
                    ]
                },
                "creation_time": "2022-02-13T14:13:38Z",
                "entity_version": "2",
                "kind": "vm",
                "last_update_time": "2022-02-13T14:13:38Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "project_reference": {
                    "kind": "project",
                    "name": "_internal",
                    "uuid": "d32032b3-8384-459e-9de7-e0e3d54e13c1"
                },
                "spec_version": 0,
                "uuid": "2b011db0-4d44-43e3-828a-d0a32dab340c"
            }
spec:
  description: An intentful representation of a vm spec
  returned: always
  type: dict
  sample: {
                "cluster_reference": {
                    "kind": "cluster",
                    "name": "auto_cluster_prod_1aa888141361",
                    "uuid": "0005d578-2faf-9fb6-3c07-ac1f6b6f9780"
                },
                "description": "VM with cluster, network, category, disk with Ubuntu image, guest customization ",
                "name": "VM with Ubuntu image",
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
                                "uuid": "64ccb355-fd73-4b68-a44b-24bc03ef3c66"
                            },
                            "device_properties": {
                                "device_type": "DISK",
                                "disk_address": {
                                    "adapter_type": "SATA",
                                    "device_index": 0
                                }
                            },
                            "disk_size_bytes": 32212254720,
                            "disk_size_mib": 30720,
                            "storage_config": {
                                "storage_container_reference": {
                                    "kind": "storage_container",
                                    "name": "SelfServiceContainer",
                                    "uuid": "47ca25c3-9d27-4b94-b6b1-dfa5b25660b4"
                                }
                            },
                            "uuid": "e7d5d42f-c14b-4f9b-aa64-56661a9ec822"
                        },
                        {
                            "device_properties": {
                                "device_type": "CDROM",
                                "disk_address": {
                                    "adapter_type": "IDE",
                                    "device_index": 0
                                }
                            },
                            "disk_size_bytes": 382976,
                            "disk_size_mib": 1,
                            "storage_config": {
                                "storage_container_reference": {
                                    "kind": "storage_container",
                                    "name": "SelfServiceContainer",
                                    "uuid": "47ca25c3-9d27-4b94-b6b1-dfa5b25660b4"
                                }
                            },
                            "uuid": "1ce566d3-1c8c-4492-96d1-c39ed7c47513"
                        }
                    ],
                    "gpu_list": [],
                    "guest_customization": {
                        "cloud_init": {
                            "user_data": "I2Nsb3VkLWNvbmZpZwpjaHBhc3N3ZDoKICBsaXN0OiB8CiAgICByb290Ok51
                                          dGFuaXguMTIzCiAgICBleHBpcmU6IEZhbHNlCmZxZG46IG15TnV0YW5peFZNIAo="
                        },
                        "is_overridable": true
                    },
                    "hardware_clock_timezone": "UTC",
                    "is_agent_vm": false,
                    "machine_type": "PC",
                    "memory_size_mib": 1024,
                    "nic_list": [
                        {
                            "ip_endpoint_list": [],
                            "is_connected": true,
                            "mac_address": "50:6b:8d:f9:06:68",
                            "nic_type": "NORMAL_NIC",
                            "subnet_reference": {
                                "kind": "subnet",
                                "name": "vlan.800",
                                "uuid": "671c0590-8496-4068-8480-702837fa2e42"
                            },
                            "trunked_vlan_list": [],
                            "uuid": "4e15796b-67eb-4f93-8e01-3b60ecf80894",
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
            }
status:
  description: An intentful representation of a vm status
  returned: always
  type: dict
  sample: {
                "cluster_reference": {
                    "kind": "cluster",
                    "name": "auto_cluster_prod_1aa888141361",
                    "uuid": "0005d578-2faf-9fb6-3c07-ac1f6b6f9780"
                },
                "description": "VM with cluster, network, category, disk with Ubuntu image, guest customization ",
                "execution_context": {
                    "task_uuid": [
                        "82c5c1d3-eb6a-406a-8f58-306028099d21"
                    ]
                },
                "name": "VM with Ubuntu image",
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
                                "uuid": "64ccb355-fd73-4b68-a44b-24bc03ef3c66"
                            },
                            "device_properties": {
                                "device_type": "DISK",
                                "disk_address": {
                                    "adapter_type": "SATA",
                                    "device_index": 0
                                }
                            },
                            "disk_size_bytes": 32212254720,
                            "disk_size_mib": 30720,
                            "is_migration_in_progress": false,
                            "storage_config": {
                                "storage_container_reference": {
                                    "kind": "storage_container",
                                    "name": "SelfServiceContainer",
                                    "uuid": "47ca25c3-9d27-4b94-b6b1-dfa5b25660b4"
                                }
                            },
                            "uuid": "e7d5d42f-c14b-4f9b-aa64-56661a9ec822"
                        },
                        {
                            "device_properties": {
                                "device_type": "CDROM",
                                "disk_address": {
                                    "adapter_type": "IDE",
                                    "device_index": 0
                                }
                            },
                            "disk_size_bytes": 382976,
                            "disk_size_mib": 1,
                            "is_migration_in_progress": false,
                            "storage_config": {
                                "storage_container_reference": {
                                    "kind": "storage_container",
                                    "name": "SelfServiceContainer",
                                    "uuid": "47ca25c3-9d27-4b94-b6b1-dfa5b25660b4"
                                }
                            },
                            "uuid": "1ce566d3-1c8c-4492-96d1-c39ed7c47513"
                        }
                    ],
                    "gpu_list": [],
                    "guest_customization": {
                        "cloud_init": {
                            "user_data": "I2Nsb3VkLWNvbmZpZwpjaHBhc3N3ZDoKICBsaXN0OiB8CiAgICByb290Ok51dGFuaXguMTIz
                                          CiAgICBleHBpcmU6IEZhbHNlCmZxZG46IG15TnV0YW5peFZNIAo="
                        },
                        "is_overridable": true
                    },
                    "hardware_clock_timezone": "UTC",
                    "host_reference": {
                        "kind": "host",
                        "name": "10.46.136.134",
                        "uuid": "7da77782-5e38-4ef8-a098-d6f63a001aae"
                    },
                    "hypervisor_type": "AHV",
                    "is_agent_vm": false,
                    "machine_type": "PC",
                    "memory_size_mib": 1024,
                    "nic_list": [
                        {
                            "ip_endpoint_list": [],
                            "is_connected": true,
                            "mac_address": "50:6b:8d:f9:06:68",
                            "nic_type": "NORMAL_NIC",
                            "subnet_reference": {
                                "kind": "subnet",
                                "name": "vlan.800",
                                "uuid": "671c0590-8496-4068-8480-702837fa2e42"
                            },
                            "trunked_vlan_list": [],
                            "uuid": "4e15796b-67eb-4f93-8e01-3b60ecf80894",
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
                    "vga_console_enabled": true,
                    "vnuma_config": {
                        "num_vnuma_nodes": 0
                    }
                },
                "state": "COMPLETE"
}
vm_uuid:
  description: The created vm uuid
  returned: always
  type: str
  sample: "2b011db0-4d44-43e3-828a-d0a32dab340c"
task_uuid:
  description: The task uuid for the creation
  returned: always
  type: str
  sample: "82c5c1d3-eb6a-406a-8f58-306028099d21"
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.vms import VM  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    network_spec = dict(
        subnet=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        private_ip=dict(type="str", required=False),
        is_connected=dict(type="bool", default=True),
    )

    disk_spec = dict(
        type=dict(type="str", choices=["CDROM", "DISK"], default="DISK"),
        size_gb=dict(type="int"),
        bus=dict(type="str", choices=["SCSI", "PCI", "SATA", "IDE"], default="SCSI"),
        storage_container=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        clone_image=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        empty_cdrom=dict(type="bool"),
    )

    boot_config_spec = dict(
        boot_type=dict(
            type="str", choices=["LEGACY", "UEFI", "SECURE_BOOT"], default="LEGACY"
        ),
        boot_order=dict(
            type="list", elements="str", default=["CDROM", "DISK", "NETWORK"]
        ),
    )

    gc_spec = dict(
        type=dict(type="str", choices=["cloud_init", "sysprep"], required=True),
        script_path=dict(type="path", required=True),
        is_overridable=dict(type="bool", default=False),
    )

    module_args = dict(
        name=dict(type="str", required=False),
        vm_uuid=dict(type="str"),
        desc=dict(type="str"),
        project=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        cluster=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        vcpus=dict(type="int", default=1),
        cores_per_vcpu=dict(type="int", default=1),
        memory_gb=dict(type="int", default=1),
        networks=dict(type="list", elements="dict", options=network_spec),
        disks=dict(
            type="list",
            elements="dict",
            options=disk_spec,
            mutually_exclusive=[
                ("storage_container", "clone_image", "empty_cdrom"),
                ("size_gb", "empty_cdrom"),
            ],
        ),
        boot_config=dict(type="dict", options=boot_config_spec),
        guest_customization=dict(type="dict", options=gc_spec),
        timezone=dict(type="str", default="UTC"),
        categories=dict(type="dict"),
    )

    return module_args


def create_vm(module, result):
    vm = VM(module)
    spec, error = vm.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating VM Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = vm.create(spec)
    vm_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["vm_uuid"] = vm_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = vm.read(vm_uuid)
        result["response"] = resp


def delete_vm(module, result):
    vm_uuid = module.params["vm_uuid"]
    if not vm_uuid:
        result["error"] = "Missing parameter vm_uuid in playbook"
        module.fail_json(msg="Failed deleting VM", **result)

    vm = VM(module)
    resp = vm.delete(vm_uuid)
    result["changed"] = True
    result["response"] = resp
    result["vm_uuid"] = vm_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid)
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name",)),
            ("state", "absent", ("vm_uuid",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_vm(module, result)
    elif state == "absent":
        delete_vm(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
