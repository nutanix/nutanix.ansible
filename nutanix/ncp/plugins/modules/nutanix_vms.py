#!/usr/bin/python

# Copyright: (c) 2021
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""

---
module: nutanix_vms
short_description: This module allows to communicate with the resource /vms
version_added: 1.0.0
description: This module allows to perform the following tasks on /vms
options:
  state:
    description: This is the action used to indicate the type of request
    aliases:
      - action
    required: true
    type: str
  auth:
    description: >-
      we need to define username, password, ip address and port in the following format :
      -----
      credentials:
        username: User Name
        password: Password
      config:
        ip_address: IPv4 Address
        port: port number
      -----
      to be used in the auth as follow:
      -----
      auth:
        credentials: '{{credentials}}'
        url: '{{config.ip_address}}:{{config.port}}'
      -----
    required: true
    type: dict
  wait_timeout:
    description: This is the wait_timeout description
    required: false
    type: int
    default: 300
  wait:
    description: This is the wait description
    required: false
    type: bool
    default: true
  validate_certs:
    description: This is the validate_certs description
    required: false
    type: bool
    default: false
  vcpus:
    description: Number of vCPU sockets.
    aliases:
      - spec__resources__num_sockets
    required: false
    type: int
    default: 1
  name:
    description: vm Name
    aliases:
      - spec__name
    required: False
    type: str
  desc:
    description: A description for vm.
    aliases:
      - description
      - spec__description
    required: false
    type: str
  cores_per_vcpu:
    description: This is the num_vcpus_per_socket description
    aliases:
      - spec__resources__num_vcpus_per_socket
    type: int
    default: 1
  timezone:
    description: VM's hardware clock timezone in IANA TZDB format (America/Los_Angeles).
    aliases:
      - spec__resources__hardware_clock_timezone
    type: str
    default: UTC
  boot_type:
    description: >-
      Indicates whether the VM should use Secure boot, UEFI boot or Legacy
      boot.If UEFI or Secure boot is enabled then other legacy boot options
      (like boot_device and boot_device_order_list) are ignored. Secure boot
      depends on UEFI    boot, i.e. enabling Secure boot means that UEFI boot is
      also enabled.
    aliases:
      - spec__resources__boot_config__boot_type
    type: str
    default: LEGACY
  memory_overcommit_enabled:
    description: This is the memory_overcommit_enabled description
    aliases:
      - spec__resources__memory_overcommit_enabled
    type: bool
    default: false
  memory_size_mib:
    description: Memory size in MiB
    aliases:
      - memory_gb
      - spec__resources__memory_size_mib
    type: int
    default: 1
  cluster:
    description: The reference to a cluster
    type: dict
    default: {}
    suboptions:
      cluster_name:
        description: Cluster Name
        aliases:
          - name
          - spec__cluster_reference__name
        type: str
        required: false
      cluster_uuid:
        description: Cluster UUID
        aliases:
          - uuid
          - spec__cluster_reference__uuid
        type: str
        required: false
      cluster_kind:
        description: The Kind Name
        aliases:
          - spec__cluster_reference__kind
        type: str
        required: false
        default: cluster
  categories:
    description: >-
      Categories for the vm. This allows assigning one value of a key to any
      entity. Changes done in this will be reflected   in the categories_mapping
      field.
    aliases:
      - metadata__categories_mapping
    type: dict
  use_categories_mapping:
    description: >-
      Client need to specify this field as true if user want to use the newer
      way of assigning the categories. Without this things should work as it was
      earlier.
    aliases:
      - metadata__use_categories_mapping
    type: bool
    default: false
  uuid:
    description: VM UUID
    aliases:
      - metadata__uuid
    type: str
    required: false
  networks:
    description: NICs attached to the VM.
    aliases:
      - spec__resources__nic_list
    type: list
    elements: dict
    default: []
    suboptions:
      nic_uuid:
        description: >-
          The NIC's UUID, which is used to uniquely identify this particular
          NIC. This UUID may be used to refer to the   NIC outside the context
          of the particular VM it is attached to.
        aliases:
          - uuid
        type: str
      subnet_name:
        description: Network subnet name and it's mutual execlusive with subnet_uuid
        type: str
      subnet_uuid:
        description: Network subnet uuid and it's mutual execlusive with subnet_name
        type: str
      subnet_kind:
        description: The Subnet kind
        type: str
        default: subnet
      is_connected:
        description: Whether or not the NIC is connected. True by default.
        default: False
        aliases:
          - connected
        type: bool
      private_ip:
        description: 'IP endpoints for the adapter. Currently, IPv4 addresses are supported.'
        aliases:
          - ip_endpoint_list
        elements: str
        default: []
        type: list
      nic_type:
        description: The type of this Network function NIC.
        default: NORMAL_NIC
        type: str
  disks:
    description: Disks attached to the VM
    aliases:
      - spec__resources__disk_list
    type: list
    elements: dict
    default: []
    suboptions:
      type:
        description: 'Disk Type , CDROM or Disk'
        type: str
      size_gb:
        description: The Disk Size in Giga
        type: int
      bus:
        description: 'The Disk bus , like sata or pcie'
        type: str
      storage_container:
        description: >-
          This preference specifies the storage configuration parameters for VM
          disks.
        aliases:
          - storage_config
        type: dict
        suboptions:
          storage_container_name:
            description: storage container name
            type: str
          storage_container_uuid:
            description: storage container uuid
            aliases:
              - uuid
            type: str
  boot_device_order_list:
    description: >-
      Indicates the order of device types in which VM should try to boot from.
      If boot device  order is not provided the system will decide appropriate
      boot device order.
    aliases:
      - spec__resources__boot_config__boot_device_order_list
    type: list
    elements: str
    default:
      - CDROM
      - DISK
      - NETWORK
  guest_customization:
    description: >-
        VM guests may be customized at boot time using one of several different
        methods. Currently, cloud-init w/ ConfigDriveV2 (for Linux VMs) and Sysprep
        (for Windows VMs) are supported. Only ONE OF sysprep or cloud_init should be
        provided. Note that guest customization can currently only be set during VM
        creation. Attempting to change it after creation will result in an error.
        Additional properties can be specified. For example - in the context of VM
        template creation if "override_script" is set to "True" then the deployer
        can upload their own custom script
    aliases:
      - spec__resources__guest_customization
    type: dict
    suboptions:
        type:
            type: str
            choices: [ sysprep, cloud_init ]
            default: sysprep
            description: The customization type
        script_path:
            type: str
            required: True
            description: The Absolute Script Path
        is_overridable:
            type: bool
            default: False
            description: Flag to allow override of customization by deployer.
author:
 - Gevorg Khachatryan (@gevorg_khachatryan)
"""
EXAMPLES = r"""
---
  - hosts: localhost
    become: true
    collections:
      - nutanix.ncp
    vars:
      credentials:
        username: UserName
        password: Password
      config:
        ip_address: xxx.xxx.xxx.xxx
        port: 9440
      cluster:
        uuid: "0005d632-6a07-32eb-0a75-50a487bc911e"
      networks:
        mannaged:
          name: "test"
          uuid: "ca7fab15-83be-4cca-bc28-88b0b8db293d"
          ip: "10.50.0.11"
      storage_config:
        uuid: "6e78251f-9cf9-45d7-ad16-59274e6f2ea2"
    tasks:
    - name: VM with Cluster , Network, UTC time zone, one Disk
      nutanix_vms:
        state: present
        name: "Cluster Network and Disk"
        timezone: "UTC"
        auth:
          credentials: "{{credentials}}"
          url: "{{config.ip_address}}:{{config.port}}"
        cluster:
          cluster_uuid: "{{cluster.uuid}}"
        networks:
          - connected: True
            subnet_name: "{{networks.mannaged.name}}"
        disks:
          - type: "DISK"
            size_gb: 5
            bus: "PCI"
      register: result
      ignore_errors: True
    - name: VM with Cluster, different Disks, memory size
      nutanix_vms:
        state: present
        name: "Different disks"
        auth:
          credentials: "{{credentials}}"
          url: "{{config.ip_address}}:{{config.port}}"
        cluster:
          cluster_uuid: "{{cluster.uuid}}"
        disks:
          - type: "DISK"
            size_gb: 4
            bus: "SATA"
          - type: "DISK"
            size_gb: 3
            bus: "SCSI"
        memory_gb: 20
      register: result
      ignore_errors: True
    - name: VM with Cluster, different CDROMS
      nutanix_vms:
        state: present
        name: "CDROM"
        auth:
          credentials: "{{credentials}}"
          url: "{{config.ip_address}}:{{config.port}}"
        cluster:
          cluster_uuid: "{{cluster.uuid}}"
        disks:
          - type: "CDROM"
            bus: "SATA"
          - type: "CDROM"
            bus: "IDE"
        cores_per_vcpu: 1
      register: result
      ignore_errors: True
    - name: delete recently created vm
      nutanix_vms:
        uuid: '{{ result["response"]["metadata"]["uuid"] }}'
        state: absent
        auth:
          credentials: "{{credentials}}"
          url: "{{config.ip_address}}:{{config.port}}"
      register: result
    - name: VM with all specification
      nutanix_vms:
        state: present
        name: "All specification"
        timezone: "GMT"
        auth:
          credentials: "{{credentials}}"
          url: "{{config.ip_address}}:{{config.port}}"
        cluster:
          cluster_uuid: "{{cluster.uuid}}"
        disks:
          - type: "DISK"
            size_gb: 1
            bus: "SCSI"
          - type: "DISK"
            size_gb: 4
            bus: "PCI"
          - type: "DISK"
            size_gb: 16
            bus: "SATA"
          - type: "DISK"
            size_gb: 16
            bus: "SCSI"
          - type: "CDROM"
            size_gb: 4
            bus: "IDE"
        boot_device_order_list:
          - "DISK"
          - "CDROM"
          - "NETWORK"
        vcpus: 20
        cores_per_vcpu: 4
        memory_gb: 6
      register: result
      ignore_errors: True
"""


RETURN = r"""
"""
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.vms import VM  # noqa: E402


def run_module():
    BaseModule.argument_spec.update(
        dict(
            spec__name=dict(type="str", required=False, aliases=["name"]),
            spec__description=dict(
                type="str", required=False, aliases=["desc", "description"]
            ),
            metadata__uuid=dict(type="str", aliases=["uuid"], required=False),
            spec__resources__num_sockets=dict(type="int", default=1, aliases=["vcpus"]),
            spec__resources__num_vcpus_per_socket=dict(
                type="int",
                default=1,
                aliases=["cores_per_vcpu"],
            ),
            cluster=dict(
                type="dict",
                default={},
                options=dict(
                    spec__cluster_reference__uuid=dict(
                        type="str", aliases=["cluster_uuid", "uuid"], required=False
                    ),
                    spec__cluster_reference__name=dict(
                        type="str", aliases=["cluster_name", "name"], required=False
                    ),
                    spec__cluster_reference__kind=dict(
                        type="str",
                        aliases=["cluster_kind"],
                        required=False,
                        default="cluster",
                    ),
                ),
            ),
            spec__resources__nic_list=dict(
                type="list",
                elements="dict",
                aliases=["networks"],
                options=dict(
                    uuid=dict(type="str", aliases=["nic_uuid"]),
                    subnet_uuid=dict(type="str"),
                    subnet_name=dict(type="str"),
                    subnet_kind=dict(type="str", default="subnet"),
                    is_connected=dict(
                        type="bool", aliases=["connected"], default=False
                    ),
                    ip_endpoint_list=dict(
                        type="list", aliases=["private_ip"], default=[], elements="str"
                    ),
                    nic_type=dict(type="str", default="NORMAL_NIC"),
                ),
                default=[],
            ),
            spec__resources__disk_list=dict(
                type="list",
                elements="dict",
                aliases=["disks"],
                options=dict(
                    type=dict(type="str"),
                    size_gb=dict(type="int"),
                    bus=dict(type="str"),
                    storage_config=dict(
                        type="dict",
                        aliases=["storage_container"],
                        options=dict(
                            storage_container_name=dict(type="str"),
                            storage_container_uuid=dict(type="str", aliases=["uuid"]),
                        ),
                    ),
                ),
                default=[],
            ),
            spec__resources__hardware_clock_timezone=dict(
                type="str", default="UTC", aliases=["timezone"]
            ),
            spec__resources__boot_config__boot_type=dict(
                type="str", default="LEGACY", aliases=["boot_type"]
            ),
            spec__resources__boot_config__boot_device_order_list=dict(
                elements="str",
                type="list",
                default=["CDROM", "DISK", "NETWORK"],
                aliases=["boot_device_order_list"],
            ),
            spec__resources__memory_overcommit_enabled=dict(
                type="bool", default=False, aliases=["memory_overcommit_enabled"]
            ),
            spec__resources__memory_size_mib=dict(
                type="int", default=1, aliases=["memory_size_mib", "memory_gb"]
            ),
            metadata__categories_mapping=dict(type="dict", aliases=["categories"]),
            metadata__use_categories_mapping=dict(
                type="bool", aliases=["use_categories_mapping"], default=False
            ),
            spec__resources__guest_customization=dict(
                type="dict",
                aliases=["guest_customization"],
                options=dict(
                    type=dict(
                        type="str", choices=["sysprep", "cloud_init"], default="sysprep"
                    ),
                    script_path=dict(type="str", required=True),
                    is_overridable=dict(type="bool", default=False),
                ),
            ),
        )
    )

    module = BaseModule()
    if module.params.get("spec__resources__memory_size_mib"):
        module.params["spec__resources__memory_size_mib"] = (
            module.params["spec__resources__memory_size_mib"] * 1024
        )
    if module.params.get("metadata__categories_mapping"):
        module.params["metadata__use_categories_mapping"] = True
    VM(module)


def main():
    run_module()


if __name__ == "__main__":
    main()
