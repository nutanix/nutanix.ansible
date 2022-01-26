#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = r'''
---
module: nutanix_vm

short_description: VM module which suports VM CRUD operations

version_added: "1.0.0"

description: Create, Update, Delete, Power-on, Power-off Nutanix VM's

options:
    nutanix_host:
        description:
        - PC hostname or IP address
        type: str
        required: True
    nutanix_port:
        description:
        - PC port
        type: str
        default: 9440
        required: False
    nutanix_username:
        description:
        - PC username
        type: str
        required: True
    nutanix_password:
        description:
        - PC password;
        required: True
        type: str
    validate_certs:
        description:
        - Set value to C(False) to skip validation for self signed certificates
        - This is not recommended for production setup
        type: bool
        default: True
    wait_timeout:
        description: This is the wait_timeout description.
        required: false
        type: int
        default: 300
    wait:
        description: This is the wait description.
        required: false
        type: bool
        default: true
    name:
        description: VM Name
        required: true
        type: str
    desc:
        description: A description for VM.
        required: false
        type: str
    project:
        description: Name or UUID of the project.
        required: false
        suboptions:
            name:
                description:
                    - Project Name
                    - Mutually exclusive with C(uuid)
                type: str
                required: true
            uuid:
                description:
                    - Project UUID
                    - Mutually exclusive with C(name)
                type: str
                required: true
    cluster:
        description: Name or UUID of the cluster on which the VM will be placed.
        required: true
        suboptions:
            name:
                description:
                    - Cluster Name
                    - Mutually exclusive with C(uuid)
                type: str
                required: true
            uuid:
                description:
                    - Cluster UUID
                    - Mutually exclusive with C(name)
                type: str
                required: true
    vcpus:
        description: Number of vCPUs
        required: false
        type: int
        default: 1
    cores_per_vcpu:
        description: This is the num_vcpus_per_socket.
        type: int
        default: 1
    memory_gb:
        description: Memory size in GB
        type: int
        default: 1
    memory_overcommit_enabled:
        description: This is the memory_overcommit_enabled description
        type: bool
        default: false
    networks:
        type: list
        elements: dict
        required: False
        suboptions:
            subnet:
                description: Name or UUID of the subnet to which the VM should be connnected.
                suboptions:
                    name:
                        description:
                            - Cluster Name
                            - Mutually exclusive with C(uuid)
                        type: str
                        required: true
                    uuid:
                        description:
                            - Cluster UUID
                            - Mutually exclusive with C(name)
                        type: str
                        required: true
            private_ip:
                description: Optionally assign static IP to the VM.
                type: str
                required: False
            connected:
                type: bool
                required: False
                default: True
    disks:
        description: Disks attached to the VM
        type: list
        elements: dict
        default: []
        suboptions:
            type:
                description: 'CDROM or DISK'
                choices: [ 'CDROM', 'DISK' ]
                default: disk
                type: str
            size_gb:
                description:
                    - The Disk Size in GB.
                    - This option is applicable for only disk type above.
                type: int
            bus:
                description: 'Bus type of the device'
                choices: [ 'SCSI', 'PCI', 'SATA', 'IDE' ] for disk type.
                choices: [ 'SATA', 'IDE' ] for cdrom type.
                type: str
            storage_container:
                description:
                    - Mutually exclusive with C(clone_image) and C(empty_cdrom)
                suboptions:
                    name:
                        description:
                            - Storage containter Name
                            - Mutually exclusive with C(uuid)
                        type: str
                        required: true
                    uuid:
                        description:
                            - Storage container UUID
                            - Mutually exclusive with C(name)
                        type: str
                        required: true
            clone_image:
                description:
                    - Mutually exclusive with C(storage_container) and C(empty_cdrom)
                suboptions:
                    name:
                        description:
                            - Image Name
                            - Mutually exclusive with C(uuid)
                        type: str
                        required: true
                    uuid:
                        description:
                            - Image UUID
                            - Mutually exclusive with C(name)
                        type: str
                        required: true
            empty_cdrom:
                type: bool
                description: Mutually exclusive with C(clone_image) and C(storage_container)
    boot_config:
        description:
            - Indicates whether the VM should use Secure boot, UEFI boot or Legacy boot.
        required: False
        suboptions:
            boot_type:
                description: Boot type of VM.
                choices: [ "LEGACY", "UEFI", "SECURE_BOOT" ]
                default: "LEGACY"
                type: str
            boot_order:
                description:
                    - Applicable only for LEGACY boot_type
                    - Boot device order list
                type: list
                default:
                    - "CDROM",
                    - "DISK",
                    - "NETWORK"
    guest_customization:
        description:
        type: dict
        suboptions:
            type:
                type: str
                choices: [ sysprep, cloud_init ]
                default: sysprep
                description: The Customization type
            script_path:
                type: str
                required: True
                description: The Absolute Script Path
            is_overridable:
                type: bool
                default: False
                description: Flag to allow override of customization during deployment.
    timezone:
        description: VM's hardware clock timezone in IANA TZDB format (America/Los_Angeles).
        type: str
        default: UTC

    categories:
        type: list
        elements: str
        required: False
'''


from ..base_module import BaseModule
from ....plugins.module_utils.prism.vms import VM


def run_module():
    module_args = {}
    module  = BaseModule(argument_spec=module_args)
    result = {}
    vm = VM(module)
    spec = vm.get_spec()
    response = vm.create(spec)
    result = response
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
