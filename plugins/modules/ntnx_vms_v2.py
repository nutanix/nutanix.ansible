#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_vms_v2
short_description: "Create, Update and delete VMs in Nutanix AHV based PC"
version_added: 2.0.0
description: "Create, Update and delete VMs in Nutanix AHV based PC"
notes:
    - During vm update, Update or create of subresources like disks, nics, cd_roms, gpus, serial_ports, etc. is not supported.
    - Use subresources specific modules to update or create subresources.
    - Power state management is not supported in this module. use ntnx_vms_power_actions_v2 module to manage power state.
    - Avoid providing subresources spec during update operation.
options:
    ext_id:
        description:
            - external ID of the VM.
            - Required for updating or deleting the VM.
        required: false
        type: str
    name:
        description:
            - The name of the VM.
        type: str
    description:
        description:
            - The description of the VM.
        required: false
        type: str
    num_sockets:
        description:
            - The number of sockets for the VM.
        required: false
        type: int
    num_cores_per_socket:
        description:
            - The number of cores per socket for the VM.
        required: false
        type: int
    num_threads_per_core:
        description:
            - The number of threads per core for the VM.
        required: false
        type: int
    num_numa_nodes:
        description:
            - The number of NUMA nodes for the VM.
        required: false
        type: int
    memory_size_bytes:
        description:
            - The memory size in bytes for the VM.
        required: false
        type: int
    is_vcpu_hard_pinning_enabled:
        description:
            - Whether vCPU hard pinning is enabled for the VM.
        required: false
        type: bool
    is_cpu_passthrough_enabled:
        description:
            - Whether CPU passthrough is enabled for the VM.
        required: false
        type: bool
    enabled_cpu_features:
        description:
            - The list of enabled CPU features for the VM.
        required: false
        type: list
        elements: str
        choices: ["HARDWARE_VIRTUALIZATION"]
    is_memory_overcommit_enabled:
        description:
            - Whether memory overcommit is enabled for the VM.
        required: false
        type: bool
    is_gpu_console_enabled:
        description:
            - Whether GPU console is enabled for the VM.
        required: false
        type: bool
    categories:
        description:
            - The list of categories for the VM.
        required: false
        type: list
        elements: dict
        suboptions:
            ext_id:
                description:
                    - The external ID of the category.
                required: true
                type: str
    cluster:
        description:
            - The cluster reference for the VM.
        type: dict
        suboptions:
            ext_id:
                description:
                    - The external ID of the cluster.
                required: true
                type: str
    availability_zone:
        description:
            - The availability zone reference for the VM.
        required: false
        type: dict
        suboptions:
            ext_id:
                description:
                    - The external ID of the availability zone.
                required: true
                type: str
    guest_customization:
        description:
            - Stage a Sysprep or cloud-init configuration file to be used by the guest for the next boot.
              Note that the Sysprep command must be used to generalize the Windows VMs before triggering this API call.
        required: false
        type: dict
        suboptions:
            config:
                description:
                    - The Nutanix Guest Tools customization settings.
                required: false
                type: dict
                suboptions:
                    sysprep:
                        description:
                            - sysprep config
                        required: false
                        type: dict
                        suboptions:
                            install_type:
                                description:
                                    - Indicates whether the guest will be freshly installed using this unattend configuration,
                                      or this unattend configuration will be applied to a pre-prepared image.
                                type: str
                                choices: ["FRESH", "PREPARED"]
                            sysprep_script:
                                description: Sysprep script configuration.
                                type: dict
                                suboptions:
                                    unattendxml:
                                        description: Configuration for Unattend XML.
                                        type: dict
                                        suboptions:
                                            value:
                                                description: The Vales of the field
                                                type: str
                                    custom_key_values:
                                        description: Custom key-value pairs for system preparation.
                                        type: dict
                                        suboptions:
                                            key_value_pairs:
                                                description: The list of the individual KeyValuePair elements.
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    name:
                                                        description: Key Name
                                                        type: str
                                                    value:
                                                        description: Key Value
                                                        type: raw
                    cloudinit:
                        description:
                            - cloudinit config
                        required: false
                        type: dict
                        suboptions:
                            datasource_type:
                                description:
                                    - The type of the data source.
                                type: str
                                choices: ["CONFIG_DRIVE_V2"]
                            metadata:
                                description:
                                    - The metadata.
                                type: str
                            cloud_init_script:
                                description:
                                    - The cloud-init script.
                                type: dict
                                suboptions:
                                    user_data:
                                        description:
                                            - The user data.
                                        type: dict
                                        suboptions:
                                            value:
                                                description:
                                                    - The value of the user data.
                                                type: str
                                                required: true
                                    custom_key_values:
                                        description:
                                            - The custom key values.
                                        type: dict
                                        suboptions:
                                            key_value_pairs:
                                                description:
                                                    - The list of the individual KeyValuePair elements.
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    name:
                                                        description:
                                                            - The name of the key.
                                                        type: str
                                                    value:
                                                        description:
                                                            - The value of the key.
                                                        type: raw
    guest_tools:
        description:
            - The guest tools for the VM.
        required: false
        type: dict
        suboptions:
            is_enabled:
                description:
                    - Whether the guest tools are enabled for the VM.
                type: bool
            capabilities:
                description:
                    - The list of capabilities for the guest tools.
                type: list
                elements: str
                choices: ["SELF_SERVICE_RESTORE", "VSS_SNAPSHOT"]
    hardware_clock_timezone:
        description:
            - The hardware clock timezone for the VM.
        required: false
        type: str
    is_branding_enabled:
        description:
            - Whether branding is enabled for the VM.
        required: false
        type: bool
    boot_config:
        description:
            - The boot configuration for the VM.
        required: false
        type: dict
        suboptions:
            legacy_boot:
                description:
                    - The legacy boot configuration.
                required: false
                type: dict
                suboptions:
                    boot_device:
                        description:
                            - The boot device for legacy boot.
                        type: dict
                        suboptions:
                            boot_device_disk:
                                description: Specification for booting from disk.
                                type: dict
                                suboptions:
                                    disk_address:
                                        description: Address specification for the disk.
                                        type: dict
                                        suboptions:
                                            bus_type:
                                                description: Bus type for the device. The acceptable values are SCSI, IDE, PCI, SATA, SPAPR (only PPC).
                                                type: str
                                                choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                required: true
                                            index:
                                                description: Device index on the bus. This field is ignored unless the bus details are specified.
                                                type: int
                            boot_device_nic:
                                description: Specification for booting from network interface controller (NIC).
                                type: dict
                                suboptions:
                                        mac_address:
                                                description: Mac address
                                                type: str
                    boot_order:
                        description:
                            - Indicates the order of device types in which the VM should try to boot from.
                              If the boot device order is not provided the system will decide an appropriate boot device order.
                        type: list
                        elements: str
                        choices: ["CDROM", "NETWORK", "DISK"]
            uefi_boot:
                description:
                    - The UEFI boot configuration.
                required: false
                type: dict
                suboptions:
                    is_secure_boot_enabled:
                        description: Indicate whether to enable secure boot or not.
                        type: bool
                    nvram_device:
                        description: Configuration for NVRAM to be presented to the VM.
                        type: dict
                        suboptions:
                            backing_storage_info:
                                description: Storage provided by Nutanix ADSF
                                type: dict
                                suboptions:
                                    disk_size_bytes:
                                        description: Size of the disk in Bytes
                                        type: int
                                    storage_container:
                                        description:
                                            - This reference is for disk level storage container preference.
                                              This preference specifies the storage container to which this disk belongs.
                                        type: dict
                                        suboptions:
                                            ext_id:
                                                description:
                                                    - The globally unique identifier of a VM disk container. It should be of type UUID.
                                                required: true
                                                type: str
                                    storage_config:
                                        description: Storage configuration for VM disks.
                                        type: dict
                                        suboptions:
                                            is_flash_mode_enabled:
                                                description: Indicates whether the virtual disk is pinned to the hot tier or not.
                                                type: bool
                                    data_source:
                                        description: A reference to a disk or image that contains the contents of a disk.
                                        type: dict
                                        suboptions:
                                            reference:
                                                description: Reference to the data source, mutually exclusive with either image_reference or vm_disk_reference.
                                                type: dict
                                                suboptions:
                                                        image_reference:
                                                            description: Reference to an image.
                                                            type: dict
                                                            suboptions:
                                                                image_ext_id:
                                                                    description: The globally unique identifier of an image. It should be of type UUID.
                                                                    type: str
                                                        vm_disk_reference:
                                                            description: Reference to a virtual machine disk.
                                                            type: dict
                                                            suboptions:
                                                                disk_ext_id:
                                                                    description: The globally unique identifier of a VM disk. It should be of type UUID.
                                                                    type: str
                                                                disk_address:
                                                                    description: The address of the disk.
                                                                    type: dict
                                                                    suboptions:
                                                                        bus_type:
                                                                            description:
                                                                                - Bus type for the device. The acceptable values
                                                                                  are SCSI, IDE, PCI, SATA, SPAPR (only PPC).
                                                                            type: str
                                                                            choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                                            required: true
                                                                        index:
                                                                            description:
                                                                                - Device index on the bus.
                                                                                  This field is ignored unless the bus details are specified.
                                                                            type: int
                                                                vm_reference:
                                                                    description: This is a reference to a VM.
                                                                    type: dict
                                                                    suboptions:
                                                                        ext_id:
                                                                            description:
                                                                                - The globally unique identifier of a VM. It should be of type UUID.
                                                                            required: true
                                                                            type: str

    is_vga_console_enabled:
        description:
            - Whether VGA console is enabled for the VM.
        required: false
        type: bool
    machine_type:
        description:
            - The machine type for the VM.
        required: false
        type: str
        choices: ["PC", "PSERIES", "Q35"]
    vtpm_config:
        description:
            - The vTPM configuration for the VM.
        required: false
        type: dict
        suboptions:
            is_vtpm_enabled:
                description:
                    - Indicates whether the virtual trusted platform module is enabled for the Guest OS or not.
                type: bool
            version:
                description:
                    - The version of the vTPM.
                type: str
    is_agent_vm:
        description:
            - Whether the VM is an agent VM.
        required: false
        type: bool
    apc_config:
        description:
            - The APC configuration for the VM.
        required: false
        type: dict
        suboptions:
            is_apc_enabled:
                description:
                    - Indicates whether the APC is enabled or not.
                type: bool
            cpu_model:
                description:
                    - The CPU model reference.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - The external ID of the CPU model.
                        type: str
                    name:
                        description:
                            - The name of the CPU model.
                        type: str
    storage_config:
        description:
            - The storage configuration for the VM.
        required: false
        type: dict
        suboptions:
            is_flash_mode_enabled:
                description:
                    - Indicates whether the virtual disk is pinned to the hot tier or not.
                type: bool
            qos_config:
                description:
                    - The QoS configuration for the VM.
                type: dict
                suboptions:
                    throttled_iops:
                        description:
                            - The throttled IOPS.
                        type: int

    disks:
        description:
            - The list of disks for the VM.
        required: false
        type: list
        elements: dict
        suboptions:
            backing_info:
                description:
                    - Supporting storage to create virtual disk on.
                type: dict
                suboptions:
                    vm_disk:
                        description:
                            - The VM disk information.
                        type: dict
                        suboptions:
                            disk_size_bytes:
                                description:
                                    - The size of the disk in bytes.
                                    - Mutually exclusive with C(data_source) during update.
                                type: int
                            storage_container:
                                description:
                                    - The storage container reference.
                                type: dict
                                suboptions:
                                    ext_id:
                                        description:
                                            - The external ID of the storage container.
                                        type: str
                                        required: true
                            storage_config:
                                description:
                                    - The storage configuration for the disk.
                                type: dict
                                suboptions:
                                    is_flash_mode_enabled:
                                        description:
                                            - Indicates whether the virtual disk is pinned to the hot tier or not.
                                        type: bool
                            data_source:
                                description:
                                    - The data source for the disk.
                                    - Mutually exclusive with C(disk_size_bytes) during update.
                                type: dict
                                suboptions:
                                    reference:
                                        description:
                                            - The reference to the data source.
                                        type: dict
                                        suboptions:
                                            image_reference:
                                                description:
                                                    - The reference to an image.
                                                    - Mutually exclusive with C(vm_disk_reference).
                                                type: dict
                                                suboptions:
                                                    image_ext_id:
                                                        description:
                                                            - The external ID of the image.
                                                        type: str
                                            vm_disk_reference:
                                                description:
                                                    - The reference to a VM disk.
                                                    - Mutually exclusive with C(image_reference).
                                                type: dict
                                                suboptions:
                                                    disk_ext_id:
                                                        description:
                                                            - The external ID of the VM disk.
                                                        type: str
                                                    disk_address:
                                                        description:
                                                            - The address of the disk.
                                                        type: dict
                                                        suboptions:
                                                            bus_type:
                                                                description:
                                                                    - The bus type of the disk.
                                                                type: str
                                                                choices:
                                                                    - 'SCSI'
                                                                    - 'IDE'
                                                                    - 'PCI'
                                                                    - 'SATA'
                                                                    - 'SPAPR'
                                                                required: true
                                                            index:
                                                                description:
                                                                    - The index of the disk.
                                                                type: int
                                                    vm_reference:
                                                        description:
                                                            - The reference to the VM.
                                                        type: dict
                                                        suboptions:
                                                            ext_id:
                                                                description:
                                                                    - The external ID of the VM.
                                                                type: str
                                                                required: true
                    adsf_volume_group:
                        description:
                            - The ADSF volume group reference.
                        type: dict
                        suboptions:
                            volume_group_ext_id:
                                description:
                                    - The external ID of the volume group.
                                type: str
            disk_address:
                description:
                    - The address of the disk.
                type: dict
                suboptions:
                    bus_type:
                        description:
                            - The bus type of the disk.
                        type: str
                        choices:
                            - 'SCSI'
                            - 'IDE'
                            - 'PCI'
                            - 'SATA'
                            - 'SPAPR'
                        required: true
                    index:
                        description:
                            - The index of the disk.
                        type: int
    cd_roms:
        description:
            - The list of CD-ROMs for the VM.
        required: false
        type: list
        elements: dict
        suboptions:
            backing_info:
                description:
                    - Storage provided by Nutanix ADSF
                type: dict
                suboptions:
                    disk_size_bytes:
                        description:
                            - The size of the CDROM in bytes.
                        type: int
                    storage_container:
                        description:
                            - The storage container reference.
                        type: dict
                        suboptions:
                            ext_id:
                                description:
                                    - The external ID of the storage container.
                                type: str
                                required: true
                    storage_config:
                        description:
                            - The storage configuration.
                        type: dict
                        suboptions:
                            is_flash_mode_enabled:
                                description:
                                    - Indicates whether the virtual disk is pinned to the hot tier or not.
                                type: bool
                    data_source:
                        description:
                            - The data source for the disk.
                        type: dict
                        suboptions:
                            reference:
                                description:
                                    - The reference to the data source.
                                type: dict
                                suboptions:
                                    image_reference:
                                        description:
                                            - The reference to an image.
                                            - Mutually exclusive with C(vm_disk_reference).
                                        type: dict
                                        suboptions:
                                            image_ext_id:
                                                description:
                                                    - The external ID of the image.
                                                type: str
                                    vm_disk_reference:
                                        description:
                                            - The reference to a VM disk.
                                            - Mutually exclusive with C(image_reference).
                                        type: dict
                                        suboptions:
                                            disk_ext_id:
                                                description:
                                                    - The external ID of the VM disk.
                                                type: str
                                            disk_address:
                                                description:
                                                    - The address of the disk.
                                                type: dict
                                                suboptions:
                                                    bus_type:
                                                        description:
                                                            - The bus type of the disk.
                                                        type: str
                                                        required: true
                                                        choices:
                                                            - 'SCSI'
                                                            - 'IDE'
                                                            - 'PCI'
                                                            - 'SATA'
                                                            - 'SPAPR'
                                                    index:
                                                        description:
                                                            - The index of the disk.
                                                        type: int
                                            vm_reference:
                                                description:
                                                    - The reference to the VM.
                                                type: dict
                                                suboptions:
                                                    ext_id:
                                                        description:
                                                            - The external ID of the VM.
                                                        type: str
                                                        required: true
            disk_address:
                description:
                    - The address of the CDROM.
                type: dict
                suboptions:
                    bus_type:
                        description:
                            - Bus type for the device
                        type: str
                        choices:
                            - 'IDE'
                            - 'SATA'
                    index:
                        description:
                            - Device index on the bus.
                            - This field is ignored unless the bus details are specified.
                        type: int
    nics:
        description:
            - The list of NICs for the VM.
        required: false
        type: list
        elements: dict
        suboptions:
            backing_info:
                description:
                    - The backing information for the NIC.
                type: dict
                suboptions:
                    model:
                        description:
                            - The model of the NIC.
                        type: str
                        choices:
                            - VIRTIO
                            - E1000
                        required: false
                    mac_address:
                        description:
                            - The MAC address of the NIC.
                        type: str
                        required: false
                    is_connected:
                        description:
                            - Whether the NIC needs to be connected or not.
                        type: bool
                        required: false
                    num_queues:
                        description:
                            - The number of queues for the NIC.
                        type: int
                        required: false
            network_info:
                description:
                    - The network configuration for the NIC.
                type: dict
                suboptions:
                    nic_type:
                        description:
                            - The type of the NIC.
                        type: str
                        choices:
                            - NORMAL_NIC
                            - DIRECT_NIC
                            - NETWORK_FUNCTION_NIC
                            - SPAN_DESTINATION_NIC
                        required: false
                    network_function_chain:
                        description:
                            - The network function chain for the NIC.
                        type: dict
                        suboptions:
                            ext_id:
                                description:
                                    - The external ID of the network function chain.
                                type: str
                                required: true
                        required: false
                    network_function_nic_type:
                        description:
                            - The type of the network function NIC.
                        type: str
                        choices:
                            - INGRESS
                            - EGRESS
                            - TAP
                        required: false
                    subnet:
                        description:
                            - The subnet for the NIC.
                        type: dict
                        suboptions:
                            ext_id:
                                description:
                                    - The external ID of the subnet.
                                type: str
                                required: true
                        required: false
                    vlan_mode:
                        description:
                            - The VLAN mode for the NIC.
                        type: str
                        choices:
                            - ACCESS
                            - TRUNK
                        required: false
                    trunked_vlans:
                        description:
                            - The trunked VLANs for the NIC.
                        type: list
                        elements: int
                        required: false
                    should_allow_unknown_macs:
                        description:
                            - Whether to allow unknown MAC addresses or not.
                        type: bool
                        required: false
                    ipv4_config:
                        description:
                            - The IPv4 configuration for the NIC.
                        type: dict
                        suboptions:
                            should_assign_ip:
                                description:
                                    - Whether to assign an IP address or not.
                                type: bool
                                required: false
                            ip_address:
                                description:
                                    - The IP address for the NIC.
                                type: dict
                                suboptions:
                                    value:
                                        description:
                                            - The IP address value.
                                        type: str
                                        required: True
                                    prefix_length:
                                        description:
                                            - The prefix length for the IP address.
                                            - Can be skipped, default it will be 32.
                                        type: int
                                        required: false
                            secondary_ip_address_list:
                                description:
                                    - The list of secondary IP addresses for the NIC.
                                type: list
                                elements: dict
                                suboptions:
                                    value:
                                        description:
                                            - The IP address value.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description:
                                            - The prefix length for the IP address.
                                            - Can be skipped, default it will be 32.
                                        type: int
                                        required: false
                        required: false
    gpus:
        description:
            - The list of GPUs for the VM.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The name of the GPU.
                required: false
                type: str
            mode:
                description:
                    - The mode of the GPU.
                choices: ['PASSTHROUGH_GRAPHICS', 'PASSTHROUGH_COMPUTE', 'VIRTUAL']
                type: str
            device_id:
                description:
                    - The ID of the GPU device.
                type: int
            vendor:
                description:
                    - The vendor of the GPU.
                choices: ['NVIDIA', 'AMD', 'INTEL']
                type: str
            pci_address:
                description:
                    - The PCI address of the GPU.
                type: dict
                suboptions:
                    segment:
                        description:
                            - The segment of the PCI address.
                        type: int
                    func:
                        description:
                            - The function of the PCI address.
                        type: int
                    device:
                        description:
                            - The device of the PCI address.
                        type: int
                    bus:
                        description:
                            - The bus of the PCI address.
                        type: int
    serial_ports:
        description:
            - The list of serial ports for the VM.
        required: false
        type: list
        elements: dict
        suboptions:
            index:
                description:
                    - Index of the serial port.
                type: int
            is_connected:
                description:
                    - Indicates whether the serial port is connected or not.
                type: bool
            ext_id:
                description:
                    - its not supported for serial ports using VM
                type: str
    state:
        description:
            - The desired state of the VM.
            - if C(state) is present, it will create or update the vm.
            - If C(state) is set to C(present) and ext_id is not provided then the operation will be create the vm
            - If C(state) is set to C(present) and ext_id is provided then the operation will be update the vm
            - If C(state) is set to C(absent) and ext_id is provided , then operation will be delete the vm
        choices: ['present', 'absent']
        type: str
    wait:
        description:
            - Whether to wait for the task to complete.
        required: false
        type: bool
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
- name: Create VM with minimum requirements
  nutanix.ncp.ntnx_vms_v2:
    name: "test_name"
    description: "ansible test"
    cluster:
      ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
  register: result
  ignore_errors: true

- name: Create VM with full requirements
  nutanix.ncp.ntnx_vms_v2:
    name: "test_name"
    description: "ansible test"
    cluster:
      ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
    num_sockets: 1
    num_cores_per_socket: 1
    num_threads_per_core: 1
    num_numa_nodes: 1
    memory_size_bytes: 4294967296
    is_vcpu_hard_pinning_enabled: false
    is_cpu_passthrough_enabled: false
    is_memory_overcommit_enabled: false
    is_gpu_console_enabled: false
    is_vga_console_enabled: false
    machine_type: "PC"
    hardware_clock_timezone: "UTC"
    enabled_cpu_features:
      - HARDWARE_VIRTUALIZATION
    is_branding_enabled: false
    is_agent_vm: false
    apc_config:
      is_apc_enabled: false
    vtpm_config:
      is_vtpm_enabled: false
  register: result
  ignore_errors: true
- name: Update VM
  nutanix.ncp.ntnx_vms_v2:
    state: present
    ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
    name: "new_name_updated"
    description: "Test VM updated"
    num_sockets: 2
    num_threads_per_core: 2
    num_cores_per_socket: 2
    num_numa_nodes: 2
    memory_size_bytes: 4294967296
    machine_type: "Q35"
    is_vcpu_hard_pinning_enabled: true
    is_cpu_passthrough_enabled: false
    is_memory_overcommit_enabled: false
    is_gpu_console_enabled: false
    is_branding_enabled: true
    is_vga_console_enabled: false
    is_agent_vm: true
    enabled_cpu_features: HARDWARE_VIRTUALIZATION
  register: result
  ignore_errors: true
- name: Delete VM
  nutanix.ncp.ntnx_vms_v2:
    state: absent
    ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
  register: result
"""
RETURN = r"""
response:
  description:
        - Response for the vm operations.
        - vm details if C(wait) is true.
        - Task details if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
            "apc_config": {
                "cpu_model": null,
                "is_apc_enabled": false
            },
            "availability_zone": null,
            "bios_uuid": "9d199d16-1c8e-4ddf-40f5-20a2d78aa918",
            "boot_config": {
                "boot_device": null,
                "boot_order": [
                    "CDROM",
                    "DISK",
                    "NETWORK"
                ]
            },
            "categories": null,
            "cd_roms": null,
            "cluster": {
                "ext_id": "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
            },
            "create_time": "2024-06-24T08:01:46.269181+00:00",
            "description": "ansible test",
            "disks": null,
            "enabled_cpu_features": null,
            "ext_id": "9d199d16-1c8e-4ddf-40f5-20a2d78aa918",
            "generation_uuid": "8bd335e2-f616-4806-87b3-53120c1f2acb",
            "gpus": null,
            "guest_customization": null,
            "guest_tools": null,
            "hardware_clock_timezone": "UTC",
            "host": null,
            "is_agent_vm": false,
            "is_branding_enabled": true,
            "is_cpu_passthrough_enabled": false,
            "is_cross_cluster_migration_in_progress": false,
            "is_gpu_console_enabled": false,
            "is_live_migrate_capable": null,
            "is_memory_overcommit_enabled": false,
            "is_vcpu_hard_pinning_enabled": false,
            "is_vga_console_enabled": true,
            "links": null,
            "machine_type": "PC",
            "memory_size_bytes": 1073741824,
            "name": "GFGLBElSNEGBansible-agvm",
            "nics": null,
            "num_cores_per_socket": 1,
            "num_numa_nodes": 0,
            "num_sockets": 1,
            "num_threads_per_core": 1,
            "ownership_info": {
                "owner": {
                    "ext_id": "00000000-0000-0000-0000-000000000000"
                }
            },
            "power_state": "OFF",
            "protection_policy_state": null,
            "protection_type": "UNPROTECTED",
            "serial_ports": null,
            "source": null,
            "storage_config": null,
            "tenant_id": null,
            "update_time": "2024-06-24T08:01:46.806598+00:00",
            "vtpm_config": {
                "is_vtpm_enabled": false,
                "version": null
            }
        }


changed:
  description:
    - Whether the vm is changed or not.
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false


ext_id:
  description:
          - External ID of the vm.
  returned: always
  type: str
  sample: "33dba56c-f123-4ec6-8b38-901e1cf716c2"

skipped:
    description:
        - Whether the operation is skipped or not.
        - Will be returned if operation is skipped.
    type: bool
    returned: always
"""


import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402
from ..module_utils.v4.vmm.spec.vms import VmSpecs as vm_specs  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = vm_specs.get_vm_spec()

    return module_args


def create_vm(module, result):
    vms = get_vm_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.AhvConfigVm()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create vms spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = vms.create_vm(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating vm",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.VM
        )
        if ext_id:
            resp = get_vm(module, vms, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    if current_spec != update_spec:
        return False
    return True


def update_vm(module, result):
    vms = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_vm(module, vms, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vm update spec", **result)

    # check for idempotency
    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = vms.update_vm_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating vm",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_vm(module, vms, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_vm(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    vms = get_vm_api_instance(module)
    vm = get_vm(module, vms, ext_id)
    etag = get_etag(vm)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.delete_vm_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting vm",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
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
        "task_ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_vm(module, result)
        else:
            create_vm(module, result)
    else:
        delete_vm(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
