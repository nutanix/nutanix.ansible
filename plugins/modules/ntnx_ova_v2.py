#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ova_v2
short_description: "Create, Update and Delete Ova from VM, url or object lite"
version_added: 2.3.0
description:
    - Create, Update and Delete Ova from VM, url or object lite
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - State of the Ova to be created, updated or deleted
            - if C(state) is present, it will create or update the ova.
            - If C(state) is set to C(present) and ext_id is not provided then the operation will be create the ova
            - If C(state) is set to C(present) and ext_id is provided then the operation will be update the ova
            - If C(state) is set to C(absent) and ext_id is provided , then operation will be delete the ova
        type: str
        choices: ["present", "absent"]
        default: "present"
    wait:
        description:
            - Wait for the task to complete
        type: bool
        default: true
    name:
        description:
            - Name of the Ova to be created or updated
        type: str
    ext_id:
        description:
            - External ID of the Ova to be updated or deleted
        type: str
    checksum:
        description:
            - Checksum of the Ova
        type: dict
        suboptions:
            ova_sha1_checksum:
                description:
                    - SHA1 checksum of the Ova
                type: dict
                suboptions:
                    hex_digest:
                        description:
                            - The SHA1 digest of an OVA file in hexadecimal format.
                        type: str
                        required: true
            ova_sha256_checksum:
                description:
                    - SHA256 checksum of the Ova
                type: dict
                suboptions:
                    hex_digest:
                        description:
                            - The SHA256 digest of an OVA file in hexadecimal format.
                        type: str
                        required: true
    source:
        description:
            - Source of the created OVA file.
            - The source can either be a VM, URL, or a Object lite.
        type: dict
        suboptions:
            ova_url_source:
                description:
                    - Source of the Ova file from a URL.
                type: dict
                suboptions:
                    url:
                        description:
                            - The URL that can be used to download an OVA.
                        type: str
                        required: true
                    should_allow_insecure_url:
                        description:
                            Ignore the certificate errors if the value is true.
                        type: bool
                        default: false
                    basic_auth:
                        description:
                            - Basic authentication credentials for image source HTTP/S URL.
                        type: dict
                        suboptions:
                            username:
                                description:
                                    - Username for basic authentication.
                                type: str
                                required: true
                            password:
                                description:
                                    - Password for basic authentication.
                                type: str
                                no_log: true
                                required: true
            ova_vm_source:
                description:
                    - Source of the Ova file from a VM.
                type: dict
                suboptions:
                    vm_ext_id:
                        description:
                            - The identifier of a VM to be exported to an OVA.
                        type: str
                        required: true
                    disk_file_format:
                        description:
                            - Disk format of an OVA.
                        type: str
                        choices: ["VMDK", "QCOW2"]
                        required: true
            objects_lite_source:
                description:
                    - Key that identifies the source object in the bucket.
                    - The resource implies the bucket, 'vmm-ovas' for OVA.
                type: dict
                suboptions:
                    key:
                        description:
                            - Key that identifies the source object in the bucket.
                        type: str
                        required: true
    cluster_location_ext_ids:
        description:
            - List of cluster identifiers where the OVA is located.
            - This field is required when creating an OVA from URL or Objects lite upload.
        type: list
        elements: str
    vm_config:
        description:
            - Configuration of the VM stored in the OVA.
        type: dict
        suboptions:
            name:
                description:
                    - Name of the VM stored in the OVA.
                type: str
            description:
                description:
                    - Description of the VM stored in the OVA.
                type: str
            num_sockets:
                description:
                    - Number of CPU sockets for the VM.
                type: int
            num_cores_per_socket:
                description:
                    - Number of cores per CPU socket.
                type: int
            num_threads_per_core:
                description:
                    - Number of threads per core.
                type: int
            num_numa_nodes:
                description:
                    - Number of NUMA nodes for the VM.
                type: int
            memory_size_bytes:
                description:
                    - Memory size of the VM in bytes.
                type: int
            is_vcpu_hard_pinning_enabled:
                description:
                    - Indicates whether the vCPUs should be hard pinned to specific pCPUs or not.
                type: bool
            is_cpu_passthrough_enabled:
                description:
                    - Indicates whether to passthrough the host CPU features to the guest or not.
                    - Enabling this will make VM incapable of live migration.
                type: bool
            enabled_cpu_features:
                description:
                    - List of CPU features to be enabled for the VM.
                type: list
                choices: ["HARDWARE_VIRTUALIZATION"]
                elements: str
            is_memory_overcommit_enabled:
                description:
                    - Indicates whether the memory overcommit feature should be enabled for the VM or not.
                    - If enabled, parts of the VM memory may reside outside of the hypervisor physical memory.
                    - Once enabled, it should be expected that the VM may suffer performance degradation.
                type: bool
            is_gpu_console_enabled:
                description:
                    - Indicates whether the vGPU console is enabled or not.
                type: bool
            categories:
                description:
                    - List of categories associated with the VM.
                type: list
                elements: dict
                suboptions:
                    ext_id:
                        description:
                            - External ID of the category.
                        type: str
            project:
                description:
                    - Project associated with the VM.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - External ID of the project.
                        type: str
            cluster:
                description:
                    - Cluster where the VM is located.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - External ID of the cluster.
                        type: str
            availability_zone:
                description:
                    - Reference to an availability zone.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - External ID of the availability zone.
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
                                    - cloudinit
                                required: false
                                type: dict
                                suboptions:
                                    datasource_type:
                                        description:
                                            - The type of the data source.
                                            - Required when using user_data.
                                        type: str
                                        choices: ["CONFIG_DRIVE_V2"]
                                    metadata:
                                        description: Metadata configuration.
                                        type: str
                                    cloud_init_script:
                                        description: Cloud init script configuration.
                                        type: dict
                                        suboptions:
                                            user_data:
                                                description: User data for cloud-init.
                                                type: dict
                                                required: false
                                                suboptions:
                                                    value:
                                                        description:
                                                            - base64 encoded cloud init script.
                                                        type: str
                                                        required: true
                                            custom_key_values:
                                                description: Custom key-value pairs for cloud-init.
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
                                                                required: false
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
                                                        description:
                                                            - Bus type for the device.
                                                            - The acceptable values are SCSI, IDE, PCI, SATA, SPAPR (only PPC).
                                                        type: str
                                                        choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                        required: true
                                                    index:
                                                        description:
                                                            - Device index on the bus.
                                                            - This field is ignored unless the bus details are specified.
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
    disk_format:
        description:
            - Disk format of the OVA.
        type: str
        choices: ["VMDK", "QCOW2"]

extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create Ova from the VM
  nutanix.ncp.ntnx_ova_v2:
    name: "name"
    source:
      ova_vm_source:
        vm_ext_id: "12345678-1234-1234-1234-123456789012"
        disk_file_format: "QCOW2"
  register: result

- name: Create Ova from a valid url
  nutanix.ncp.ntnx_ova_v2:
    name: "{{ ova_name }}_url"
    source:
      ova_url_source:
        url: "https://example.com/path/to/ova/file.ova"
        should_allow_insecure_url: true
    cluster_location_ext_ids:
      - "000636a4-e7ce-389e-185b-ac1f6b6f97e2"
  register: result

- name: Create ova using object store source
  nutanix.ncp.ntnx_ova_v2:
    name: "object-ova"
    source:
      objects_lite_source:
        key: "object_name"
    cluster_location_ext_ids:
      - "000636a4-e7ce-389e-185b-ac1f6b6f97e2"
  register: result

- name: Update Ova
  nutanix.ncp.ntnx_ova_v2:
    ext_id: "12345678-1234-1234-1234-123456789012"
    name: "name_updated"
  register: result

- name: Delete Ova
  nutanix.ncp.ntnx_ova_v2:
    ext_id: "12345678-1234-1234-1234-123456789012"
    state: absent
  register: result
"""

RETURN = r"""
response:
    description: Response when we create, update or delete an Ova
    returned: always
    type: dict
    sample:
        {
            "checksum": {
                "hex_digest": "8b6b28a02d0630a7140adac3466bc5dabd4b3de2a02d1051b9815e82f5957390"
            },
            "cluster_location_ext_ids": [
                "000636a4-e7ce-389e-185b-ac1f6b6f97e2"
            ],
            "create_time": "2025-06-09T10:32:38.810439+00:00",
            "created_by": {
                "additional_attributes": null,
                "buckets_access_keys": null,
                "created_by": null,
                "created_time": null,
                "creation_type": null,
                "description": null,
                "display_name": null,
                "email_id": null,
                "ext_id": "30303030-3030-3030-2d30-3030302d3030",
                "first_name": null,
                "idp_id": null,
                "is_force_reset_password_enabled": null,
                "last_login_time": null,
                "last_name": null,
                "last_updated_by": null,
                "last_updated_time": null,
                "links": null,
                "locale": null,
                "middle_initial": null,
                "password": null,
                "region": null,
                "status": null,
                "tenant_id": null,
                "user_type": null,
                "username": "admin"
            },
            "disk_format": "QCOW2",
            "ext_id": "aab776d5-d83f-4e32-a9de-63e91f9f5e47",
            "last_update_time": "2025-06-09T10:32:38.810439+00:00",
            "links": null,
            "name": "JSVJIbifvyVgansible-agova",
            "parent_vm": "JSVJIbifvyVgansible-agvm",
            "size_bytes": 10240,
            "source": null,
            "tenant_id": null,
            "vm_config": {
                "apc_config": null,
                "availability_zone": null,
                "bios_uuid": null,
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
                "cluster": null,
                "create_time": null,
                "custom_attributes": null,
                "description": "ansible test ova",
                "disks": null,
                "enabled_cpu_features": null,
                "ext_id": null,
                "generation_uuid": null,
                "gpus": null,
                "guest_customization": null,
                "guest_tools": null,
                "hardware_clock_timezone": "UTC",
                "host": null,
                "is_agent_vm": false,
                "is_branding_enabled": null,
                "is_cpu_hotplug_enabled": true,
                "is_cpu_passthrough_enabled": false,
                "is_cross_cluster_migration_in_progress": null,
                "is_gpu_console_enabled": null,
                "is_live_migrate_capable": null,
                "is_memory_overcommit_enabled": null,
                "is_scsi_controller_enabled": true,
                "is_vcpu_hard_pinning_enabled": null,
                "is_vga_console_enabled": null,
                "links": null,
                "machine_type": "PC",
                "memory_size_bytes": 1073741824,
                "name": "JSVJIbifvyVgansible-agvm",
                "nics": null,
                "num_cores_per_socket": 1,
                "num_numa_nodes": null,
                "num_sockets": 2,
                "num_threads_per_core": 1,
                "ownership_info": null,
                "pcie_devices": null,
                "power_state": null,
                "project": null,
                "protection_policy_state": null,
                "protection_type": null,
                "serial_ports": null,
                "source": null,
                "storage_config": null,
                "tenant_id": null,
                "update_time": null,
                "vtpm_config": null
            }
        }
task_ext_id:
    description: Task ext_id if the operation is async
    returned: always
    type: str
    sample: "ZXJnb24=:350f0fd5-097d-4ece-8f44-6e5bfbe2dc08"
ext_id:
    description: External id of the Ova
    returned: always
    type: str
    sample: "aab776d5-d83f-4e32-a9de-63e91f9f5e47"
error:
    description: Error message if any
    returned: always
    type: str
changed:
    description: Indicates if the module made any changes
    returned: always
    type: bool
    sample: true
failed:
    description: Indicates if the module failed
    returned: when failed
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

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
from ..module_utils.v4.vmm.api_client import get_etag, get_ova_api_instance # noqa: E402
from ..module_utils.v4.vmm.helpers import get_ova  # noqa: E402
from ..module_utils.v4.vmm.spec.vms import VmSpecs as vm_specs  # noqa: E402
from ..module_utils.v4.iam.spec.iam import UserSpecs as user_specs  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    checksum_allowed_types = {
        "ova_sha1_checksum": vmm_sdk.OvaSha1Checksum,
        "ova_sha256_checksum": vmm_sdk.OvaSha256Checksum,
    }
    source_allowed_types = {
        "ova_url_source": vmm_sdk.OvaUrlSource,
        "ova_vm_source": vmm_sdk.OvaVmSource,
        "objects_lite_source": vmm_sdk.ObjectsLiteSource,
    }
    ova_sha_checksum_spec = dict(
        hex_digest= dict(type="str", required=True),
    )
    checksum_spec = dict(
        ova_sha1_checksum=dict(
            type="dict", options=ova_sha_checksum_spec),
        ova_sha256_checksum=dict(
            type="dict", options=ova_sha_checksum_spec),
        )
    ova_url_source_spec = dict(
        url=dict(type="str", required=True),
        should_allow_insecure_url=dict(
            type="bool",
            default=False,
        ),
        basic_auth=dict(
            type="dict",
            options=dict(
                username=dict(type="str", required=True),
                password=dict(type="str", no_log=True, required=True),
            ),
        ),
    )
    ova_vm_source_spec = dict(
        vm_ext_id=dict(type="str", required=True),
        disk_file_format= dict(
            type="str",
            choices=["VMDK", "QCOW2"],
            required=True,
        ),
    )
    objects_lite_source_spec = dict(
        key=dict(type="str", required=True),
    )
    source_spec = dict(
        ova_url_source=dict(
            type="dict",
            options=ova_url_source_spec,
        ),
        ova_vm_source=dict(
            type="dict",
            options=ova_vm_source_spec,
        ),
        objects_lite_source=dict(
            type="dict",
            options=objects_lite_source_spec,
        ),
    )
    vm_config_spec = vm_specs.get_vm_spec()
    vm_config_spec.pop("ext_id", None)

    module_args = dict(
        name= dict(type="str"),
        ext_id= dict(type="str"),
        checksum=dict(
            type="dict",
            options=checksum_spec,
            obj=checksum_allowed_types,
            mutually_exclusive=[("ova_sha1_checksum", "ova_sha256_checksum")],
        ),
        source=dict(
            type="dict",
            options=source_spec,
            obj=source_allowed_types,
            mutually_exclusive=[
                ("ova_url_source", "ova_vm_source", "objects_lite_source")
            ],
        ),
        cluster_location_ext_ids= dict(
            type="list",
            elements="str",
        ),
        vm_config=dict(
            type="dict",
            options=vm_config_spec,
            obj=vmm_sdk.AhvConfigVm,
        ),
        disk_format= dict(
            type="str",
            choices=["VMDK", "QCOW2"],
        )
    )

    return module_args


def create_ova(module, ova, result):
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.Ova()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create ova spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = ova.create_ova(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating ova",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.OVA
        )
        if ext_id:
            resp = get_ova(module, ova, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    if current_spec.get("name") != update_spec.get("name"):
        return False
    return True


def update_ova(module, ova, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_ova(module, ova, ext_id=ext_id)

    etag_value = get_etag(current_spec)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.Ova()
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating ova update spec", **result)

    # check for idempotency
    if check_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = ova.update_ova_by_id(extId=ext_id, body=update_spec, if_match=etag_value)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating ova",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_ova(module, ova, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_ova(module, ova, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Ova with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = ova.delete_ova_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting ova",
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
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name",)),
            ("state", "present", ("source",), True),
        ],
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
    ova = get_ova_api_instance(module)
    if state == "present":
        if module.params.get("ext_id"):
            update_ova(module, ova, result)
        else:
            create_ova(module, ova, result)
    else:
        delete_ova(module, ova, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
