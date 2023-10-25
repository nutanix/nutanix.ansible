# -*- coding: utf-8 -*-

# Copyright: (c) 2017,  Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for ntnx_vms_base
    DOCUMENTATION = r"""
options:
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
  force_power_off:
      description:
        - when set the vm will restart if it's necessary
      type: bool
      default: false
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
  networks:
    description:
      - list of subnets to which the VM needs to connect to
    type: list
    elements: dict
    required: false
    suboptions:
      uuid:
        description:
          - Subnet's uuid
        type: str
      state:
        description:
          - Subnets's state to delete it
        type: str
        choices:
          - absent
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
          cluster:
            description:
              - Name or UUID of the cluster from which subnet will be queried for subnet name given
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
      private_ip:
        description:
          - Optionally assign static IP to the VM
        type: str
        required: false
      mac_address:
        description:
          - Optionally assign a MAC Address to the VM
        type: str
        required: false
      is_connected:
        description:
          - Connect or disconnect the VM to the subnet
        type: bool
        required: false
        default: true
  vcpus:
    description:
      - Number of sockets
    required: false
    type: int
  cores_per_vcpu:
    description:
      - This is the number of vcpus per socket
    required: false
    type: int
  memory_gb:
    description:
      - Memory size in GB
    required: false
    type: int
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
  name:
    description: VM Name
    required: false
    type: str
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
  owner:
    description: Name or UUID of the owner
    required: false
    type: dict
    suboptions:
      name:
        description:
          - Owner Name
          - Mutually exclusive with C(uuid)
        type: str
      uuid:
        description:
          - Owner UUID
          - Mutually exclusive with C(name)
        type: str
"""
