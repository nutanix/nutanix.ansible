#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_v2
short_description: Create, Update and Delete VMs in Nutanix PC
version_added: "2.6.0"
description:
    - Create, Update and Delete VMs in Nutanix PC.
    - This module uses PC v4 APIs based SDKs.
notes:
    - During VM update, subresource changes (disks, nics, cd_roms, gpus, serial_ports) are not supported.
    - Use subresource-specific modules to manage subresources.
    - Power state management is not supported. Use ntnx_vms_power_actions_v2 instead.
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create VM) -
      Operation Name: Create New Virtual Machine -
      Required Roles: Account Owner, Administrator, Consumer, Developer, Operator, Prism Admin, User,
      Project Admin, Project Manager, Self-Service Admin (deprecated), Super Admin, Virtual Machine Admin,
      Backup Admin, Disaster Recovery Admin, NCM Connector
    - >-
      B(Update VM using ext_id) -
      Operation Name: Update Virtual Machine Basic Config -
      Required Roles: Account Owner, Administrator, Consumer, Developer, Operator, Prism Admin, User,
      Project Admin, Project Manager, Self-Service Admin (deprecated), Super Admin, Virtual Machine Admin,
      Backup Admin, NCM Connector
    - >-
      B(Delete VM using ext_id) -
      Operation Name: Delete Existing Virtual Machine -
      Required Roles: Account Owner, Administrator, Consumer, Developer, Operator, Prism Admin, User,
      Project Admin, Project Manager, Self-Service Admin (deprecated), Super Admin, Virtual Machine Admin,
      Backup Admin, NCM Connector
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - External ID of the VM.
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
    project:
        description: Reference to a project.
        type: dict
        suboptions:
            ext_id:
                description: The globally unique identifier of a project. It should be of type UUID.
                type: str
    host:
        description: Reference to a host.
        type: dict
        suboptions:
            ext_id:
                description: The globally unique identifier of a host. It should be of type UUID.
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
                            - Sysprep config.
                        required: false
                        type: dict
                        suboptions:
                            install_type:
                                description:
                                    - Indicates whether the guest will be freshly installed or applied to a pre-prepared image.
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
                                                description: The value of the field.
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
                                                        description: Key Name.
                                                        type: str
                                                    value:
                                                        description: Key Value.
                                                        type: raw
                    cloudinit:
                        description:
                            - Cloud-init config.
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
                                                    - Base64 encoded cloud init script.
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
                                                description: Bus type for the device.
                                                type: str
                                                choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                required: true
                                            index:
                                                description: Device index on the bus.
                                                type: int
                            boot_device_nic:
                                description: Specification for booting from NIC.
                                type: dict
                                suboptions:
                                    mac_address:
                                        description: Mac address.
                                        type: str
                    boot_order:
                        description:
                            - Indicates the order of device types in which the VM should try to boot from.
                        type: list
                        elements: str
                        choices: ["CDROM", "NETWORK", "DISK"]
            uefi_boot:
                description:
                    - The UEFI boot configuration.
                required: false
                type: dict
                suboptions:
                    boot_device:
                        description:
                            - The boot device settings for UEFI boot.
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
                                                description: Bus type for the device.
                                                type: str
                                                choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                required: true
                                            index:
                                                description: Device index on the bus.
                                                type: int
                            boot_device_nic:
                                description: Specification for booting from NIC.
                                type: dict
                                suboptions:
                                    mac_address:
                                        description: Mac address.
                                        type: str
                    boot_order:
                        description:
                            - Indicates the order of device types in which the VM should try to boot from.
                        type: list
                        elements: str
                        choices: ["CDROM", "NETWORK", "DISK"]
                    is_secure_boot_enabled:
                        description: Indicate whether to enable secure boot or not.
                        type: bool
                    nvram_device:
                        description: Configuration for NVRAM to be presented to the VM.
                        type: dict
                        suboptions:
                            backing_storage_info:
                                description: Storage provided by Nutanix ADSF.
                                type: dict
                                suboptions:
                                    disk_size_bytes:
                                        description: Size of the disk in Bytes.
                                        type: int
                                    storage_container:
                                        description: Storage container reference for this disk.
                                        type: dict
                                        suboptions:
                                            ext_id:
                                                description: The globally unique identifier of a VM disk container.
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
                                                description: Reference to the data source.
                                                type: dict
                                                suboptions:
                                                    image_reference:
                                                        description: Reference to an image.
                                                        type: dict
                                                        suboptions:
                                                            image_ext_id:
                                                                description: The globally unique identifier of an image.
                                                                type: str
                                                    vm_disk_reference:
                                                        description: Reference to a virtual machine disk.
                                                        type: dict
                                                        suboptions:
                                                            disk_ext_id:
                                                                description: The globally unique identifier of a VM disk.
                                                                type: str
                                                            disk_address:
                                                                description: The address of the disk.
                                                                type: dict
                                                                suboptions:
                                                                    bus_type:
                                                                        description: Bus type for the device.
                                                                        type: str
                                                                        choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                                        required: true
                                                                    index:
                                                                        description: Device index on the bus.
                                                                        type: int
                                                            vm_reference:
                                                                description: Reference to a VM.
                                                                type: dict
                                                                suboptions:
                                                                    ext_id:
                                                                        description: The globally unique identifier of a VM.
                                                                        required: true
                                                                        type: str
    is_vga_console_enabled:
        description:
            - Whether VGA console is enabled for the VM.
        required: false
        type: bool
    machine_type:
        description:
            - Machine type for the VM.
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
                    - Indicates whether the virtual trusted platform module is enabled.
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
                                            - Indicates whether the virtual disk is pinned to the hot tier.
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
                                                type: dict
                                                suboptions:
                                                    image_ext_id:
                                                        description:
                                                            - The external ID of the image.
                                                        type: str
                                            vm_disk_reference:
                                                description:
                                                    - The reference to a VM disk.
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
                                                                choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
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
                        choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
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
                    - Storage provided by Nutanix ADSF.
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
                                    - Indicates whether the virtual disk is pinned to the hot tier.
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
                                        type: dict
                                        suboptions:
                                            image_ext_id:
                                                description:
                                                    - The external ID of the image.
                                                type: str
                                    vm_disk_reference:
                                        description:
                                            - The reference to a VM disk.
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
                                                        choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
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
                            - Bus type for the device.
                        type: str
                        choices: ["IDE", "SATA"]
                    index:
                        description:
                            - Device index on the bus.
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
                    - The backing information for the NIC (deprecated, use nic_backing_info).
                type: dict
                suboptions:
                    model:
                        description:
                            - The model of the NIC.
                        type: str
                        choices: ["VIRTIO", "E1000"]
                    mac_address:
                        description:
                            - The MAC address of the NIC.
                        type: str
                    is_connected:
                        description:
                            - Whether the NIC needs to be connected.
                        type: bool
                    num_queues:
                        description:
                            - The number of queues for the NIC.
                        type: int
            nic_backing_info:
                description:
                    - Backing Information about how NIC is associated with a VM.
                type: dict
                suboptions:
                    virtual_ethernet_nic:
                        description:
                            - The virtual ethernet NIC information.
                        type: dict
                        suboptions:
                            model:
                                description:
                                    - The model of the NIC.
                                type: str
                                choices: ["VIRTIO", "E1000"]
                            mac_address:
                                description:
                                    - The MAC address of the NIC.
                                type: str
                            is_connected:
                                description:
                                    - Whether the NIC needs to be connected.
                                type: bool
                            num_queues:
                                description:
                                    - The number of queues for the NIC.
                                type: int
            network_info:
                description:
                    - The network configuration for the NIC (deprecated, use nic_network_info).
                type: dict
                suboptions:
                    nic_type:
                        description:
                            - The type of the NIC.
                        type: str
                        choices: ["NORMAL_NIC", "DIRECT_NIC", "NETWORK_FUNCTION_NIC", "SPAN_DESTINATION_NIC"]
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
                    network_function_nic_type:
                        description:
                            - The type of the network function NIC.
                        type: str
                        choices: ["INGRESS", "EGRESS", "TAP"]
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
                    vlan_mode:
                        description:
                            - The VLAN mode for the NIC.
                        type: str
                        choices: ["ACCESS", "TRUNK"]
                    trunked_vlans:
                        description:
                            - The trunked VLANs for the NIC.
                        type: list
                        elements: int
                    should_allow_unknown_macs:
                        description:
                            - Whether to allow unknown MAC addresses or not.
                        type: bool
                    ipv4_config:
                        description:
                            - The IPv4 configuration for the NIC.
                        type: dict
                        suboptions:
                            should_assign_ip:
                                description:
                                    - Whether to assign an IP address or not.
                                type: bool
                            ip_address:
                                description:
                                    - The IP address for the NIC.
                                type: dict
                                suboptions:
                                    value:
                                        description:
                                            - The IP address value.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description:
                                            - The prefix length for the IP address.
                                        type: int
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
                                        type: int
            nic_network_info:
                description:
                    - Network configuration for the NIC.
                type: dict
                suboptions:
                    virtual_ethernet_nic_network_info:
                        description:
                            - The network configuration for the virtual ethernet NIC.
                        type: dict
                        suboptions:
                            nic_type:
                                description:
                                    - The type of the NIC.
                                type: str
                                choices: ["NORMAL_NIC", "DIRECT_NIC", "NETWORK_FUNCTION_NIC", "SPAN_DESTINATION_NIC"]
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
                            network_function_nic_type:
                                description:
                                    - The type of the network function NIC.
                                type: str
                                choices: ["INGRESS", "EGRESS", "TAP"]
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
                            vlan_mode:
                                description:
                                    - The VLAN mode for the NIC.
                                type: str
                                choices: ["ACCESS", "TRUNK"]
                            trunked_vlans:
                                description:
                                    - The trunked VLANs for the NIC.
                                type: list
                                elements: int
                            should_allow_unknown_macs:
                                description:
                                    - Whether to allow unknown MAC addresses or not.
                                type: bool
                            ipv4_config:
                                description:
                                    - The IPv4 configuration for the NIC.
                                type: dict
                                suboptions:
                                    should_assign_ip:
                                        description:
                                            - Whether to assign an IP address or not.
                                        type: bool
                                    ip_address:
                                        description:
                                            - The IP address for the NIC.
                                        type: dict
                                        suboptions:
                                            value:
                                                description:
                                                    - The IP address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - The prefix length for the IP address.
                                                type: int
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
                                                type: int
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
                type: str
            mode:
                description:
                    - The mode of the GPU.
                choices: ["PASSTHROUGH_GRAPHICS", "PASSTHROUGH_COMPUTE", "VIRTUAL"]
                type: str
            device_id:
                description:
                    - The ID of the GPU device.
                type: int
            vendor:
                description:
                    - The vendor of the GPU.
                choices: ["NVIDIA", "AMD", "INTEL"]
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
                    - External ID of the serial port (not supported for serial ports during VM creation).
                type: str
    state:
        description:
            - The desired state of the VM.
            - If C(state) is C(present) and ext_id is not provided, the VM will be created.
            - If C(state) is C(present) and ext_id is provided, the VM will be updated.
            - If C(state) is C(absent) and ext_id is provided, the VM will be deleted.
        choices: ["present", "absent"]
        type: str
    wait:
        description:
            - Whether to wait for the task to complete.
        required: false
        type: bool
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create VM with minimum requirements
  nutanix.ncp.ntnx_vm_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: "test-vm"
    description: "ansible test vm"
    cluster:
      ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
  register: result

- name: Create VM with full configuration
  nutanix.ncp.ntnx_vm_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: "test-vm-full"
    description: "ansible full config test vm"
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
    is_branding_enabled: false
    is_agent_vm: false
    apc_config:
      is_apc_enabled: false
    vtpm_config:
      is_vtpm_enabled: false
  register: result

- name: Update VM
  nutanix.ncp.ntnx_vm_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
    name: "updated-vm-name"
    description: "updated description"
    num_sockets: 2
    memory_size_bytes: 4294967296
  register: result

- name: Delete VM
  nutanix.ncp.ntnx_vm_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for the VM operations.
    - VM details if C(wait) is true.
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
            "boot_order": ["CDROM", "DISK", "NETWORK"]
        },
        "cluster": {
            "ext_id": "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
        },
        "description": "ansible test vm",
        "ext_id": "9d199d16-1c8e-4ddf-40f5-20a2d78aa918",
        "hardware_clock_timezone": "UTC",
        "is_agent_vm": false,
        "is_branding_enabled": true,
        "is_cpu_passthrough_enabled": false,
        "is_gpu_console_enabled": false,
        "is_memory_overcommit_enabled": false,
        "is_vcpu_hard_pinning_enabled": false,
        "is_vga_console_enabled": true,
        "machine_type": "PC",
        "memory_size_bytes": 1073741824,
        "name": "test-vm",
        "num_cores_per_socket": 1,
        "num_numa_nodes": 0,
        "num_sockets": 1,
        "num_threads_per_core": 1,
        "power_state": "OFF",
        "protection_type": "UNPROTECTED",
        "vtpm_config": {
            "is_vtpm_enabled": false,
            "version": null
        }
    }
changed:
  description: Whether the VM is changed or not.
  returned: always
  type: bool
  sample: true
error:
  description: This field holds information about if the task has errors.
  returned: always
  type: bool
  sample: false
ext_id:
  description: External ID of the VM.
  returned: always
  type: str
  sample: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
task_ext_id:
  description: External ID of the task.
  returned: when a task is created
  type: str
  sample: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
skipped:
  description: Whether the operation is skipped due to idempotency.
  type: bool
  returned: when operation is skipped
msg:
  description: Message indicating the result of the operation.
  returned: when there is an error, operation is idempotent or in check mode
  type: str
  sample: "VM with ext_id:33dba56c-f123-4ec6-8b38-901e1cf716c2 will be deleted."
failed:
  description: Whether the operation failed.
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """Return the module argument spec using the shared VmSpecs definition."""
    return vm_specs.get_vm_spec()


def create_vm(module, api_instance, result):
    """Create a new VM using the provided module parameters.

    Args:
        module: Ansible module instance.
        api_instance: VmApi SDK instance.
        result: Dict to store operation results.
    """
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.AhvConfigVm()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create VM spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_vm(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating VM",
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
            resp = get_vm(module, api_instance, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    """Check if the current spec and update spec are identical.

    Args:
        current_spec: Current VM spec object.
        update_spec: Updated VM spec object.

    Returns:
        bool: True if specs are identical (no changes needed).
    """
    return current_spec == update_spec


def update_vm(module, api_instance, result):
    """Update an existing VM using the provided module parameters.

    Args:
        module: Ansible module instance.
        api_instance: VmApi SDK instance.
        result: Dict to store operation results.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_vm(module, api_instance, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VM update spec", **result)

    apc_config_params = module.params.get("apc_config")
    if (
        apc_config_params is not None
        and isinstance(apc_config_params, dict)
        and apc_config_params.get("is_apc_enabled") is False
        and hasattr(update_spec, "apc_config")
        and update_spec.apc_config is not None
        and hasattr(update_spec.apc_config, "cpu_model")
    ):
        update_spec.apc_config.cpu_model = None

    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    etag = get_etag(current_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.update_vm_by_id(extId=ext_id, body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating VM",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_vm(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_vm(module, api_instance, result):
    """Delete an existing VM by ext_id.

    Args:
        module: Ansible module instance.
        api_instance: VmApi SDK instance.
        result: Dict to store operation results.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "VM with ext_id:{0} will be deleted.".format(ext_id)
        return

    vm = get_vm(module, api_instance, ext_id)
    etag = get_etag(vm)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.delete_vm_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting VM",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
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

    api_instance = get_vm_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_vm(module, api_instance, result)
        else:
            create_vm(module, api_instance, result)
    else:
        delete_vm(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
