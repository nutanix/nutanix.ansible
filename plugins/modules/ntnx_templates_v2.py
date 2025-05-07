#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_templates_v2
short_description: Manage Nutanix AHV template resources
description:
    - This module allows you to create, update, and delete Nutanix AHV templates.
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
options:
    state:
        description:
            - The desired state of the template.
        choices: ['present', 'absent']
        default: 'present'
    ext_id:
        description:
            - A globally unique identifier of an instance that is suitable for external consumption.
        type: str
    template_name:
        description:
            - The user defined name of a Template.
        type: str
    template_description:
        description:
            - The description of the template.
        type: str
    template_version_spec:
        description:
            - Used for creating new versions of templates, allowing specification of version details such as name,
              description, `extId`, and the source of the new version.
            - Each instance includes an `extId` field, which holds a globally unique identifier for the instance.
        type: dict
        suboptions:
            version_name:
                description:
                    - The user defined name of a Template Version.
                type: str
            version_description:
                description:
                    - The user defined description of a Template Version.
                type: str
            version_source:
                description:
                    - Source of the created Template Version.
                      The source can either be a VM when creating a new Template Version or
                      an existing Version within a Template when creating a new Version.
                type: dict
                suboptions:
                    template_vm_reference:
                        description:
                            - The reference to a template VM.
                        type: dict
                        suboptions:
                            ext_id:
                                description:
                                    - The identifier of a VM.
                                type: str
                            guest_customization:
                                            description:
                                                - Stage a Sysprep or cloud-init configuration file to be used by the guest for the next boot.
                                                  Note that the Sysprep command must be used to generalize the Windows VMs before triggering this API call.
                                            type: dict
                                            suboptions:
                                                config:
                                                    type: dict
                                                    description: The Nutanix Guest Tools customization settings.
                                                    suboptions:
                                                        sysprep:
                                                            description: Sysprep configuration for Windows guests
                                                            type: dict
                                                            suboptions:
                                                                    install_type:
                                                                        description:
                                                                            - Indicates whether the guest will be freshly
                                                                              installed using this unattend configuration,
                                                                              or this unattend configuration will be applied to a pre-prepared image.
                                                                              Default is 'PREPARED'.
                                                                        type: str
                                                                        choices: ["FRESH", "PREPARED"]
                                                                    sysprep_script:
                                                                        description: Parameters for the sysprep script
                                                                        type: dict
                                                                        suboptions:
                                                                                unattendxml:
                                                                                    description: unattend.xml settings
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        value:
                                                                                            description: XML content for unattend.xml
                                                                                            type: str
                                                                                custom_key_values:
                                                                                    description: Custom key-value pairs
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        key_value_pairs:
                                                                                            description: The list of the individual KeyValuePair elements.
                                                                                            type: list
                                                                                            elements: dict
                                                                                            suboptions:
                                                                                                name:
                                                                                                    description: The key of this key-value pair
                                                                                                    type: str
                                                                                                value:
                                                                                                    description:
                                                                                                        - The value associated with the key
                                                                                                          for this key-value pair
                                                                                                    type: raw

                                                        cloudinit:
                                                            description: Cloud-init configuration for Linux guests
                                                            type: dict
                                                            suboptions:
                                                                    datasource_type:
                                                                        description:
                                                                            - Type of cloud-init datasource
                                                                            - Required when using user_data
                                                                        type: str
                                                                        choices: ["CONFIG_DRIVE_V2"]
                                                                    metadata:
                                                                        description:
                                                                            - The contents of the meta_data configuration for cloud-init.
                                                                              This can be formatted as YAML or JSON. The value must be base64 encoded.
                                                                        type: str
                                                                    cloud_init_script:
                                                                        description: The script to use for cloud-init.
                                                                        type: dict
                                                                        suboptions:
                                                                                user_data:
                                                                                    description: User data script
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        value:
                                                                                            description:
                                                                                                - base64 encoded cloud init script.
                                                                                            type: str
                                                                                            required: True
                                                                                custom_key_values:
                                                                                    description: Custom key-value pairs
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        key_value_pairs:
                                                                                            description: The list of the individual KeyValuePair elements.
                                                                                            type: list
                                                                                            elements: dict
                                                                                            suboptions:
                                                                                                name:
                                                                                                    description: The key of this key-value pair
                                                                                                    type: str
                                                                                                value:
                                                                                                    description:
                                                                                                        - The value associated with the key
                                                                                                          for this key-value pair
                                                                                                    type: raw

                    template_version_reference:
                        description:
                            - The reference to a template version.
                        type: dict
                        suboptions:
                            version_id:
                                description:
                                    - The identifier of a Template Version.
                                type: str
                            override_vm_config:
                                description:
                                    - Overrides specification for VM create from a Template.
                                type: dict
                                suboptions:
                                        name:
                                            description: VM name.
                                            type: str
                                        num_sockets:
                                            description: Number of vCPU sockets.
                                            type: int
                                        num_cores_per_socket:
                                            description: Number of cores per socket.
                                            type: int
                                        num_threads_per_core:
                                            description: Number of threads per core.
                                            type: int
                                        memory_size_bytes:
                                            description: Memory size in bytes.
                                            type: int
                                        nics:
                                            description: NICs attached to the VM.
                                            type: list
                                            elements: dict
                                            suboptions:
                                                    backing_info:
                                                        description: Defines a NIC emulated by the hypervisor
                                                        type: dict
                                                        suboptions:
                                                            model:
                                                                description: Model of the NIC
                                                                type: str
                                                                choices: ["VIRTIO", "E1000"]
                                                            mac_address:
                                                                description: MAC address of the emulated NIC.
                                                                type: str
                                                            is_connected:
                                                                description: Indicates whether the NIC is connected or not. Default is True.
                                                                type: bool
                                                            num_queues:
                                                                description: The number of Tx/Rx queue pairs for this NIC.
                                                                type: int
                                                    network_info:
                                                        description: Network information for a NIC.
                                                        type: dict
                                                        suboptions:
                                                            nic_type:
                                                                description: Type of the NIC
                                                                type: str
                                                                choices: ["NORMAL_NIC", "DIRECT_NIC", "NETWORK_FUNCTION_NIC", "SPAN_DESTINATION_NIC"]
                                                            network_function_chain:
                                                                description:
                                                                    - The network function chain associates with the NIC.
                                                                      Only valid if nic_type is NORMAL_NIC.
                                                                type: dict
                                                                suboptions:
                                                                    ext_id:
                                                                        description:
                                                                            - The globally unique identifier of a network function chain.
                                                                              It should be of type UUID.
                                                                        required: true
                                                                        type: str
                                                            network_function_nic_type:
                                                                description: The type of this Network function NIC. Defaults to INGRESS.
                                                                type: str
                                                                choices: ["INGRESS", "EGRESS", "TAP"]
                                                            subnet:
                                                                description:
                                                                    - Network identifier for this adapter.
                                                                      Only valid if nic_type is NORMAL_NIC or DIRECT_NIC.
                                                                type: dict
                                                                suboptions:
                                                                    ext_id:
                                                                        description: The globally unique identifier of a subnet. It should be of type UUID.
                                                                        required: true
                                                                        type: str
                                                            vlan_mode:
                                                                description:
                                                                    - By default, all the virtual NICs are created in ACCESS mode,
                                                                      which permits only one VLAN per virtual network.
                                                                      TRUNKED mode allows multiple VLANs on a single VM NIC for network-aware user VMs.
                                                                type: str
                                                                choices: ["ACCESS", "TRUNK"]
                                                            trunked_vlans:
                                                                description:
                                                                    - List of networks to trunk if VLAN mode is marked as TRUNKED.
                                                                      If empty and VLAN mode is set to TRUNKED, all the VLANs are trunked.
                                                                type: list
                                                                elements: int
                                                            should_allow_unknown_macs:
                                                                description:
                                                                    - Indicates whether an unknown unicast traffic is forwarded to this NIC or not.
                                                                      This is applicable only for the NICs on the overlay subnets.
                                                                type: bool
                                                            ipv4_config:
                                                                description: The IP address configurations.
                                                                type: dict
                                                                suboptions:
                                                                    should_assign_ip:
                                                                        description:
                                                                            - If set to true (default value), an IP address must be assigned to the VM NIC
                                                                              either the one explicitly specified by the user or allocated automatically
                                                                              by the IPAM service by not specifying the IP address.
                                                                              If false, then no IP assignment is required for this VM NIC.
                                                                        type: bool
                                                                    ip_address:
                                                                        description: Primary IP address configuration
                                                                        type: dict
                                                                        suboptions:
                                                                            value:
                                                                                description: IP address
                                                                                type: str
                                                                                required: True
                                                                            prefix_length:
                                                                                description: Prefix length of the IP address
                                                                                type: int
                                                                    secondary_ip_address_list:
                                                                        description: List of secondary IP addresses
                                                                        type: list
                                                                        elements: dict
                                                                        suboptions:
                                                                            value:
                                                                                description: IP address
                                                                                type: str
                                                                                required: True
                                                                            prefix_length:
                                                                                description: Prefix length of the IP address
                                                                                type: int

                                        guest_customization:
                                            description:
                                                - Stage a Sysprep or cloud-init configuration file to be used by the guest for the next boot.
                                                  Note that the Sysprep command must be used to generalize the Windows VMs before triggering this API call.
                                            type: dict
                                            suboptions:
                                                config:
                                                    type: dict
                                                    description: The Nutanix Guest Tools customization settings.
                                                    suboptions:
                                                        sysprep:
                                                            description: Sysprep configuration for Windows guests
                                                            type: dict
                                                            suboptions:
                                                                    install_type:
                                                                        description:
                                                                            - Indicates whether the guest will be freshly installed
                                                                              using this unattend configuration,
                                                                              or this unattend configuration will be applied to a pre-prepared image.
                                                                              Default is 'PREPARED'.
                                                                        type: str
                                                                        choices: ["FRESH", "PREPARED"]
                                                                    sysprep_script:
                                                                        description: Parameters for the sysprep script
                                                                        type: dict
                                                                        suboptions:
                                                                                unattendxml:
                                                                                    description: unattend.xml settings
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        value:
                                                                                            description: XML content for unattend.xml
                                                                                            type: str
                                                                                custom_key_values:
                                                                                    description: Custom key-value pairs
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        key_value_pairs:
                                                                                            description: The list of the individual KeyValuePair elements.
                                                                                            type: list
                                                                                            elements: dict
                                                                                            suboptions:
                                                                                                name:
                                                                                                    description: The key of this key-value pair
                                                                                                    type: str
                                                                                                value:
                                                                                                    description:
                                                                                                        - The value associated with the key
                                                                                                          for this key-value pair
                                                                                                    type: raw

                                                        cloudinit:
                                                            description: Cloud-init configuration for Linux guests
                                                            type: dict
                                                            suboptions:
                                                                    datasource_type:
                                                                        description:
                                                                            - Type of cloud-init datasource
                                                                            - Required when using user_data
                                                                        type: str
                                                                        choices: ["CONFIG_DRIVE_V2"]
                                                                    metadata:
                                                                        description:
                                                                            - The contents of the meta_data configuration for cloud-init.
                                                                              This can be formatted as YAML or JSON. The value must be base64 encoded.
                                                                        type: str
                                                                    cloud_init_script:
                                                                        description: The script to use for cloud-init.
                                                                        type: dict
                                                                        suboptions:
                                                                                user_data:
                                                                                    description: User data script
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        value:
                                                                                            description:
                                                                                                - base64 encoded cloud init script.
                                                                                            type: str
                                                                                            required: True
                                                                                custom_key_values:
                                                                                    description: Custom key-value pairs
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        key_value_pairs:
                                                                                            description: The list of the individual KeyValuePair elements.
                                                                                            type: list
                                                                                            elements: dict
                                                                                            suboptions:
                                                                                                name:
                                                                                                    description: The key of this key-value pair
                                                                                                    type: str
                                                                                                value:
                                                                                                    description:
                                                                                                        - The value associated with the key
                                                                                                          for this key-value pair
                                                                                                    type: raw
            vm_spec:
                description:
                    - VM configuration.
                type: dict
                suboptions:
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

                    ext_id:
                        description: A globally unique identifier of an instance that is suitable for external consumption.
                        type: str
                    name:
                        description: VM name.
                        type: str
                    description:
                        description: VM description.
                        type: str
                    num_sockets:
                        description: Number of VCPU sockets
                        type: int
                    num_cores_per_socket:
                        description: Number of CPU cores per socket
                        type: int
                    num_threads_per_core:
                        description: Number of threads per core
                        type: int
                    num_numa_nodes:
                        description: Number of NUMA nodes. 0 means NUMA is disabled.
                        type: int
                    memory_size_bytes:
                        description: Size of memory in bytes
                        type: int
                    is_vcpu_hard_pinning_enabled:
                        description: Indicates whether the vCPUs should be hard pinned to specific pCPUs or not.
                        type: bool
                    is_cpu_passthrough_enabled:
                        description:
                            - Indicates whether to passthrough the host CPU features to the guest or not.
                              Enabling this will make VM incapable of live migration.
                        type: bool
                    enabled_cpu_features:
                        description:
                            - The list of additional CPU features to be enabled.
                              HardwareVirtualization Indicates whether hardware assisted virtualization
                              should be enabled for the Guest OS or not. Once enabled, the Guest OS can deploy a nested hypervisor.
                        type: list
                        elements: str
                        choices: ["HARDWARE_VIRTUALIZATION"]
                    is_memory_overcommit_enabled:
                        description:
                            - Indicates whether the memory overcommit feature should be enabled for the VM or not.
                              If enabled, parts of the VM memory may reside outside of the hypervisor physical memory.
                              Once enabled, it should be expected that the VM may suffer performance degradation.
                        type: bool
                    is_gpu_console_enabled:
                        description: Indicates whether the vGPU console is enabled or not.
                        type: bool
                    categories:
                        description: Categories for the VM.
                        type: list
                        elements: dict
                        suboptions:
                            ext_id:
                                description: The globally unique identifier of a VM category. It should be of type UUID.
                                type: str
                                required: True
                    cluster:
                        description: Reference to a cluster.
                        type: dict
                        suboptions:
                            ext_id:
                                description: The globally unique identifier of a cluster. It should be of type UUID.
                                type: str
                                required: True
                    availability_zone:
                        description: Reference to an availability zone.
                        type: dict
                        suboptions:
                            ext_id:
                                description: External identifier of the availability zone reference
                                type: str
                                required: True
                    guest_customization:
                                            description:
                                                - Stage a Sysprep or cloud-init configuration file to be used by the guest for the next boot.
                                                  Note that the Sysprep command must be used to generalize the Windows VMs before triggering this API call.
                                            type: dict
                                            suboptions:
                                                config:
                                                    type: dict
                                                    description: The Nutanix Guest Tools customization settings.
                                                    suboptions:
                                                        sysprep:
                                                            description: Sysprep configuration for Windows guests
                                                            type: dict
                                                            suboptions:
                                                                    install_type:
                                                                        description:
                                                                            - Indicates whether the guest will be freshly installed
                                                                              using this unattend configuration, or this unattend
                                                                              configuration will be applied to a pre-prepared image.
                                                                              Default is 'PREPARED'.
                                                                        type: str
                                                                        choices: ["FRESH", "PREPARED"]
                                                                    sysprep_script:
                                                                        description: Parameters for the sysprep script
                                                                        type: dict
                                                                        suboptions:
                                                                                unattendxml:
                                                                                    description: unattend.xml settings
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        value:
                                                                                            description: XML content for unattend.xml
                                                                                            type: str
                                                                                custom_key_values:
                                                                                    description: Custom key-value pairs
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        key_value_pairs:
                                                                                            description: The list of the individual KeyValuePair elements.
                                                                                            type: list
                                                                                            elements: dict
                                                                                            suboptions:
                                                                                                name:
                                                                                                    description: The key of this key-value pair
                                                                                                    type: str
                                                                                                value:
                                                                                                    description:
                                                                                                        - The value associated with the key
                                                                                                          for this key-value pair
                                                                                                    type: raw

                                                        cloudinit:
                                                            description: Cloud-init configuration for Linux guests
                                                            type: dict
                                                            suboptions:
                                                                    datasource_type:
                                                                        description:
                                                                            - Type of cloud-init datasource
                                                                            - Required when using user_data
                                                                        type: str
                                                                        choices: ["CONFIG_DRIVE_V2"]
                                                                    metadata:
                                                                        description:
                                                                            - The contents of the meta_data configuration for cloud-init.
                                                                              This can be formatted as YAML or JSON. The value must be base64 encoded.
                                                                        type: str
                                                                    cloud_init_script:
                                                                        description: The script to use for cloud-init.
                                                                        type: dict
                                                                        suboptions:
                                                                                user_data:
                                                                                    description: User data script
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        value:
                                                                                            description:
                                                                                                - base64 encoded cloud init script.
                                                                                            type: str
                                                                                            required: True
                                                                                custom_key_values:
                                                                                    description: Custom key-value pairs
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        key_value_pairs:
                                                                                            description: The list of the individual KeyValuePair elements.
                                                                                            type: list
                                                                                            elements: dict
                                                                                            suboptions:
                                                                                                name:
                                                                                                    description: The key of this key-value pair
                                                                                                    type: str
                                                                                                value:
                                                                                                    description:
                                                                                                        - The value associated with the key
                                                                                                          for this key-value pair
                                                                                                    type: raw
                    hardware_clock_timezone:
                        description: VM hardware clock timezone in IANA TZDB format (America/Los_Angeles).
                        type: str
                    is_branding_enabled:
                        description: Indicates whether to remove AHV branding from VM firmware tables or not.
                        type: bool
                    boot_config:
                        description:
                            - Indicates the order of device types in which the VM should try to boot from.
                              If the boot device order is not provided the system will decide an appropriate boot device order.
                        type: dict
                        suboptions:
                            legacy_boot:
                                description: Legacy boot configuration
                                type: dict
                                suboptions:
                                                    boot_device:
                                                        description: Boot device settings for legacy boot
                                                        type: dict
                                                        suboptions:
                                                            boot_device_disk:
                                                                description: Boot device from disk
                                                                type: dict
                                                                suboptions:
                                                                    disk_address:
                                                                        description: Disk address for boot device
                                                                        type: dict
                                                                        suboptions:
                                                                            bus_type:
                                                                                description:
                                                                                    - Bus type for the device.
                                                                                      The acceptable values are SCSI, IDE, PCI, SATA, SPAPR (only PPC).
                                                                                type: str
                                                                                choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                                                required: True
                                                                            index:
                                                                                description:
                                                                                    - Device index on the bus.
                                                                                      This field is ignored unless the bus details are specified.
                                                                                type: int
                                                            boot_device_nic:
                                                                description: Boot device from NIC
                                                                type: dict
                                                                suboptions:
                                                                    mac_address:
                                                                        description: MAC address of the NIC
                                                                        type: str
                                                    boot_order:
                                                            description:
                                                                - Indicates the order of device types in which the VM should try to boot from.
                                                                  If the boot device order is not provided the system will
                                                                  decide an appropriate boot device order.
                                                            type: list
                                                            elements: str
                                                            choices: ["CDROM", "NETWORK", "DISK"]
                            uefi_boot:
                                description: UEFI boot configuration
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
                                                            description: The globally unique identifier of a VM disk container. It should be of type UUID.
                                                            type: str
                                                            required: True
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
                                                            description: Reference to the data source
                                                            type: dict
                                                            suboptions:
                                                                image_reference:
                                                                    description: Image reference for the data source
                                                                    type: dict
                                                                    suboptions:
                                                                        image_ext_id:
                                                                            description: The globally unique identifier of an image. It should be of type UUID.
                                                                            type: str
                                                                vm_disk_reference:
                                                                    description: VM disk reference for the data source
                                                                    type: dict
                                                                    suboptions:
                                                                        disk_ext_id:
                                                                            description: The globally unique identifier of a VM disk. It should be of type UUID.
                                                                            type: str
                                                                        disk_address:
                                                                            description: Disk address.
                                                                            type: dict
                                                                            suboptions:
                                                                                bus_type:
                                                                                    description:
                                                                                        - Bus type for the device.
                                                                                          The acceptable values are SCSI, IDE, PCI, SATA, SPAPR (only PPC).
                                                                                    type: str
                                                                                    choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                                                    required: True
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
                                                                                    type: str
                                                                                    required: True

                    is_vga_console_enabled:
                        description: Indicates whether the VGA console should be disabled or not.
                        type: bool
                    machine_type:
                        description: Machine type for the VM. Machine type Q35 is required for secure boot and does not support IDE disks
                        type: str
                        choices: ["PC", "PSERIES", "Q35"]
                    vtpm_config:
                        description: Indicates how the vTPM for the VM should be configured.
                        type: dict
                        suboptions:
                            is_vtpm_enabled:
                                description: Indicates whether the virtual trusted platform module is enabled for the Guest OS or not.
                                type: bool
                            version:
                                description: Version of the vTPM
                                type: str
                    is_agent_vm:
                        description:
                            - Indicates whether the VM is an agent VM or not.
                              When their host enters maintenance mode, once the normal VMs are evacuated,
                              the agent VMs are powered off.
                              When the host is restored, agent VMs are powered on before the normal VMs are restored.
                              In other words, agent VMs cannot be HA-protected or live migrated.
                        type: bool
                    apc_config:
                        description:
                            - Advanced Processor Compatibility configuration for the VM.
                              Enabling this retains the CPU model for the VM across power cycles and migrations.
                        type: dict
                        suboptions:
                            is_apc_enabled:
                                description: If enabled, the selected CPU model will be retained across live and cold migrations of the VM.
                                type: bool
                            cpu_model:
                                description:
                                    - CPU model associated with the VM if Advanced Processor Compatibility(APC) is enabled.
                                      If APC is enabled and no CPU model is explicitly set, a default baseline CPU model is picked by the system.
                                      See the APC documentation for more information
                                type: dict
                                suboptions:
                                    ext_id:
                                        description: The globally unique identifier of the CPU model associated with the VM.
                                        type: str
                                    name:
                                        description: Name of the CPU model associated with the VM.
                                        type: str
                    storage_config:
                        description: Storage configuration for VM.
                        type: dict
                        suboptions:
                            is_flash_mode_enabled:
                                description: Indicates whether the virtual disk is pinned to the hot tier or not.
                                type: bool
                            qos_config:
                                description: QoS parameters to be enforced.
                                type: dict
                                suboptions:
                                    throttled_iops:
                                        description: Throttled IOPS for the governed entities. The block size for the I/O is 32 kB.
                                        type: int
                    disks:
                        description: Disks attached to the VM.
                        type: list
                        elements: dict
                        suboptions:
                            backing_info:
                                description: Supporting storage to create virtual disk on.
                                type: dict
                                suboptions:
                                    vm_disk:
                                        description: VM disk information
                                        type: dict
                                        suboptions:
                                            disk_size_bytes:
                                                description: Size of the disk in bytes
                                                type: int
                                            storage_container:
                                                description:
                                                    - This reference is for disk level storage container preference.
                                                      This preference specifies the storage container to which this disk belongs.
                                                type: dict
                                                suboptions:
                                                    ext_id:
                                                        description: The globally unique identifier of a VM disk container. It should be of type UUID.
                                                        type: str
                                                        required: True
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
                                                        description: Reference to the data source
                                                        type: dict
                                                        suboptions:
                                                            image_reference:
                                                                description: Image reference for the data source
                                                                type: dict
                                                                suboptions:
                                                                    image_ext_id:
                                                                        description: The globally unique identifier of an image. It should be of type UUID.
                                                                        type: str
                                                            vm_disk_reference:
                                                                description: VM disk reference for the data source
                                                                type: dict
                                                                suboptions:
                                                                    disk_ext_id:
                                                                        description: The globally unique identifier of a VM disk. It should be of type UUID.
                                                                        type: str
                                                                    disk_address:
                                                                        description: Disk address.
                                                                        type: dict
                                                                        suboptions:
                                                                            bus_type:
                                                                                description:
                                                                                    - Bus type for the device.
                                                                                      The acceptable values are SCSI, IDE, PCI, SATA, SPAPR (only PPC).
                                                                                type: str
                                                                                choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                                                required: True
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
                                                                                description: The globally unique identifier of a VM. It should be of type UUID.
                                                                                type: str
                                                                                required: True
                                    adsf_volume_group:
                                            description: write
                                            type: dict
                                            suboptions:
                                                volume_group_ext_id:
                                                    description:
                                                       - The globally unique identifier of an ADSF volume group. It should be of type UUID.
                                                    type: str
                            disk_address:
                                        description: Address information for the disk
                                        type: dict
                                        suboptions:
                                            bus_type:
                                                description:
                                                    - Bus type for the device.
                                                      The acceptable values are SCSI, IDE, PCI, SATA, SPAPR (only PPC).
                                                type: str
                                                choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                required: True
                                            index:
                                                description:
                                                    - Device index on the bus.
                                                      This field is ignored unless the bus details are specified.
                                                type: int

                    cd_roms:
                        description: CD-ROMs attached to the VM.
                        type: list
                        elements: dict
                        suboptions:
                            backing_info:
                                description: Storage provided by Nutanix ADSF
                                type: dict
                                suboptions:
                                    disk_size_bytes:
                                        description: Size of the disk in bytes
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
                                                type: str
                                                required: True
                                    storage_config:
                                        description: Storage configuration for the disk
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
                                                description: Reference to the data source
                                                type: dict
                                                suboptions:
                                                    image_reference:
                                                        description: Image reference for the data source
                                                        type: dict
                                                        suboptions:
                                                            image_ext_id:
                                                                description: The globally unique identifier of an image. It should be of type UUID.
                                                                type: str
                                                    vm_disk_reference:
                                                        description: VM disk reference for the data source
                                                        type: dict
                                                        suboptions:
                                                            disk_ext_id:
                                                                description: The globally unique identifier of a VM disk. It should be of type UUID.
                                                                type: str
                                                            disk_address:
                                                                description: Disk address.
                                                                type: dict
                                                                suboptions:
                                                                    bus_type:
                                                                        description:
                                                                            - Bus type for the device.
                                                                              The acceptable values are SCSI, IDE, PCI, SATA, SPAPR (only PPC).
                                                                        type: str
                                                                        choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                                        required: True
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
                                                                        description: The globally unique identifier of a VM. It should be of type UUID.
                                                                        type: str
                                                                        required: True
                            disk_address:
                                description: Virtual Machine disk (VM disk).
                                type: dict
                                suboptions:
                                    bus_type:
                                        description: Bus type for the device. The acceptable values are IDE, SATA.
                                        type: str
                                        choices: ["IDE", "SATA"]
                                    index:
                                        description: Device index on the bus. This field is ignored unless the bus details are specified.
                                        type: int
                    nics:
                        description: NICs attached to the VM.
                        type: list
                        elements: dict
                        suboptions:
                                backing_info:
                                    description: Defines a NIC emulated by the hypervisor
                                    type: dict
                                    suboptions:
                                        model:
                                            description: Model of the NIC
                                            type: str
                                            choices: ["VIRTIO", "E1000"]
                                        mac_address:
                                            description: MAC address of the emulated NIC.
                                            type: str
                                        is_connected:
                                            description: Indicates whether the NIC is connected or not. Default is True.
                                            type: bool
                                        num_queues:
                                            description: The number of Tx/Rx queue pairs for this NIC.
                                            type: int
                                network_info:
                                    description: Network information for a NIC.
                                    type: dict
                                    suboptions:
                                        nic_type:
                                            description: Type of the NIC
                                            type: str
                                            choices: ["NORMAL_NIC", "DIRECT_NIC", "NETWORK_FUNCTION_NIC", "SPAN_DESTINATION_NIC"]
                                        network_function_chain:
                                            description: The network function chain associates with the NIC. Only valid if nic_type is NORMAL_NIC.
                                            type: dict
                                            suboptions:
                                                ext_id:
                                                    description: The globally unique identifier of a network function chain. It should be of type UUID.
                                                    required: true
                                                    type: str
                                        network_function_nic_type:
                                            description: The type of this Network function NIC. Defaults to INGRESS.
                                            type: str
                                            choices: ["INGRESS", "EGRESS", "TAP"]
                                        subnet:
                                            description: Network identifier for this adapter. Only valid if nic_type is NORMAL_NIC or DIRECT_NIC.
                                            type: dict
                                            suboptions:
                                                ext_id:
                                                    description: The globally unique identifier of a subnet. It should be of type UUID.
                                                    required: true
                                                    type: str
                                        vlan_mode:
                                            description:
                                                - By default, all the virtual NICs are created in ACCESS mode,
                                                  which permits only one VLAN per virtual network.
                                                  TRUNKED mode allows multiple VLANs on a single
                                                  VM NIC for network-aware user VMs.
                                            type: str
                                            choices: ["ACCESS", "TRUNK"]
                                        trunked_vlans:
                                            description:
                                                - List of networks to trunk if VLAN mode is marked as TRUNKED.
                                                  If empty and VLAN mode is set to TRUNKED, all the VLANs are trunked.
                                            type: list
                                            elements: int
                                        should_allow_unknown_macs:
                                            description:
                                                - Indicates whether an unknown unicast traffic is forwarded to this NIC or not.
                                                  This is applicable only for the NICs on the overlay subnets.
                                            type: bool
                                        ipv4_config:
                                            description: The IP address configurations.
                                            type: dict
                                            suboptions:
                                                should_assign_ip:
                                                    description:
                                                        - If set to true (default value), an IP address must be assigned to the VM NIC
                                                          either the one explicitly specified by the user
                                                          or allocated automatically by the IPAM service by not specifying the IP address.
                                                          If false, then no IP assignment is required for this VM NIC.
                                                    type: bool
                                                ip_address:
                                                    description: Primary IP address configuration
                                                    type: dict
                                                    suboptions:
                                                        value:
                                                            description: IP address
                                                            type: str
                                                            required: True
                                                        prefix_length:
                                                            description: Prefix length of the IP address
                                                            type: int
                                                secondary_ip_address_list:
                                                    description: List of secondary IP addresses
                                                    type: list
                                                    elements: dict
                                                    suboptions:
                                                        value:
                                                            description: IP address
                                                            type: str
                                                            required: True
                                                        prefix_length:
                                                            description: Prefix length of the IP address
                                                            type: int
                    gpus:
                        description: GPUs attached to the VM.
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description: Name of the GPU
                                type: str
                            mode:
                                description: Mode of the GPU
                                type: str
                                choices: ["PASSTHROUGH_GRAPHICS", "PASSTHROUGH_COMPUTE", "VIRTUAL"]
                            device_id:
                                description: Device ID of the GPU
                                type: int
                            vendor:
                                description: Vendor of the GPU
                                type: str
                                choices: ["NVIDIA", "INTEL", "AMD"]
                            pci_address:
                                description: PCI address of the GPU
                                type: dict
                                suboptions:
                                    segment:
                                        description: Segment number of the PCI address
                                        type: int
                                    bus:
                                        description: Bus number of the PCI address
                                        type: int
                                    device:
                                        description: Device number of the PCI address
                                        type: int
                                    func:
                                        description: Function number of the PCI address
                                        type: int
                    serial_ports:
                        description: Serial ports configured on the VM.
                        type: list
                        elements: dict
                        suboptions:
                            is_connected:
                                description: Indicates whether the serial port is connected or not.
                                type: bool
                            ext_id:
                                description: A globally unique identifier of an instance that is suitable for external consumption.
                                type: str
                            index:
                                description: Index of the serial port.
                                type: int
            is_active_version:
                description:
                    - Specify whether to mark the Template Version as active or not.
                      The newly created Version during Template Creation,
                      updating or Guest OS updating is set to Active by default unless specified otherwise.
                type: bool
            is_gc_override_enabled:
                description:
                    - Allow or disallow override of the Guest Customization during Template deployment.
                type: bool
    guest_update_status:
        description:
            - The status of the guest update.
        type: dict
        suboptions:
            deployed_vm_reference:
                description:
                    - The identifier of the temporary VM created on initiating Guest OS Update.
                type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Create new template  from a vm
  nutanix.ncp.ntnx_templates_v2:
    ext_id: "{{ template1_ext_id }}"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    template_name: "{{ template_name }}"
    template_description: "ansible test"
    template_version_spec:
      version_source:
        template_vm_reference:
          ext_id: "{{ vm_uuid }}"

- name: Update template description & name
  nutanix.ncp.ntnx_templates_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ template1_ext_id }}"
    template_version_spec:
      version_name: "{{ version_2_name }}"
      version_description: "ansible_template_version_description New"
      version_source:
        template_version_reference:
          version_id: "{{version1_ext_id}}"
          override_vm_config:
          num_sockets: 4
          num_cores_per_socket: 4
          num_threads_per_core: 4
          name: "new_vm_name"

- name: Delete Template
  nutanix.ncp.ntnx_templates_v2:
    ext_id: "{{ template1_ext_id }}"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
"""

RETURN = r"""
response:
    description: The response from the Nutanix API.
    type: dict
    returned: always
    sample:
        {
                    "create_time": "2024-05-20T08:02:06.806063+00:00",
                    "created_by": {
                        "additional_attributes": null,
                        "buckets_access_keys": null,
                        "created_by": null,
                        "created_time": null,
                        "display_name": null,
                        "email_id": null,
                        "ext_id": "00000000-0000-0000-0000-000000000000",
                        "first_name": null,
                        "idp_id": null,
                        "is_force_reset_password_enabled": null,
                        "last_login_time": null,
                        "last_name": null,
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
                    "ext_id": "5448bd78-5343-4e1c-8f30-9246d88c1147",
                    "guest_update_status": null,
                    "links": null,
                    "template_description": "ansible test",
                    "template_name": "rDkjscJgMJBoansible-agtemplate",
                    "template_version_spec": {
                        "create_time": "2024-05-20T08:02:06.776259+00:00",
                        "created_by": {
                            "additional_attributes": null,
                            "buckets_access_keys": null,
                            "created_by": null,
                            "created_time": null,
                            "display_name": null,
                            "email_id": null,
                            "ext_id": "00000000-0000-0000-0000-000000000000",
                            "first_name": null,
                            "idp_id": null,
                            "is_force_reset_password_enabled": null,
                            "last_login_time": null,
                            "last_name": null,
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
                        "ext_id": "148038b3-6e68-48d9-ba29-4c8f36798be5",
                        "is_active_version": true,
                        "is_gc_override_enabled": true,
                        "links": null,
                        "tenant_id": null,
                        "version_description": "Created from VM: MinReqVMalaa2",
                        "version_name": "Initial Version",
                        "version_source": null,
                        "version_source_discriminator": null,
                        "vm_spec": {
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
                            "categories": [
                                {
                                    "ext_id": "eb8b4155-b3d1-5772-8d2f-d566d43d8e46"
                                }
                            ],
                            "cd_roms": null,
                            "cluster": {
                                "ext_id": "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
                            },
                            "create_time": null,
                            "description": null,
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
                            "is_branding_enabled": true,
                            "is_cpu_passthrough_enabled": false,
                            "is_cross_cluster_migration_in_progress": null,
                            "is_gpu_console_enabled": false,
                            "is_live_migrate_capable": null,
                            "is_memory_overcommit_enabled": false,
                            "is_vcpu_hard_pinning_enabled": false,
                            "is_vga_console_enabled": true,
                            "links": null,
                            "machine_type": "PC",
                            "memory_size_bytes": 4294967296,
                            "name": "MinReqVMalaa2",
                            "nics": null,
                            "num_cores_per_socket": 1,
                            "num_numa_nodes": 0,
                            "num_sockets": 1,
                            "num_threads_per_core": 1,
                            "ownership_info": null,
                            "power_state": "ON",
                            "protection_policy_state": null,
                            "protection_type": null,
                            "serial_ports": null,
                            "source": null,
                            "storage_config": null,
                            "tenant_id": null,
                            "update_time": null,
                            "vtpm_config": {
                                "is_vtpm_enabled": false,
                                "version": null
                            }
                        }
                    },
                    "tenant_id": null,
                    "update_time": "2024-05-20T08:02:06.806063+00:00",
                    "updated_by": {
                        "additional_attributes": null,
                        "buckets_access_keys": null,
                        "created_by": null,
                        "created_time": null,
                        "display_name": null,
                        "email_id": null,
                        "ext_id": "00000000-0000-0000-0000-000000000000",
                        "first_name": null,
                        "idp_id": null,
                        "is_force_reset_password_enabled": null,
                        "last_login_time": null,
                        "last_name": null,
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
                    }
                }
task_ext_id:
    description: The unique identifier of the task.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
changed:
    description: Indicates whether the state of the template has changed.
    type: bool
    returned: always
    sample: true
ext_id:
    description: Template external ID
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
error:
    description: The error message if any.
    type: str
    returned: when error occurs
    sample: "Failed to create templates"
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
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_etag,
    get_templates_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_template  # noqa: E402
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
    version_source_map = {
        "template_vm_reference": vmm_sdk.TemplateVmReference,
        "template_version_reference": vmm_sdk.TemplateVersionReference,
    }

    template_vm_reference_spec = dict(
        ext_id=dict(type="str"),
        guest_customization=dict(
            type="dict",
            options=vm_specs.get_gc_spec(),
            obj=vmm_sdk.GuestCustomizationParams,
        ),
    )

    override_config_spec = dict(
        name=dict(type="str"),
        num_sockets=dict(type="int"),
        num_cores_per_socket=dict(type="int"),
        num_threads_per_core=dict(type="int"),
        memory_size_bytes=dict(type="int"),
        nics=dict(
            type="list",
            elements="dict",
            options=vm_specs.get_nic_spec(),
            obj=vmm_sdk.AhvConfigNic,
        ),
        guest_customization=dict(
            type="dict",
            options=vm_specs.get_gc_spec(),
            obj=vmm_sdk.GuestCustomizationParams,
        ),
    )

    template_version_reference_spec = dict(
        version_id=dict(type="str"),
        override_vm_config=dict(
            type="dict", options=override_config_spec, obj=vmm_sdk.VmConfigOverride
        ),
    )

    version_source_spec = dict(
        template_vm_reference=dict(
            type="dict",
            options=template_vm_reference_spec,
            obj=vmm_sdk.TemplateVmReference,
        ),
        template_version_reference=dict(
            type="dict",
            options=template_version_reference_spec,
            obj=vmm_sdk.TemplateVersionReference,
        ),
    )

    version_spec = dict(
        version_name=dict(type="str"),
        version_description=dict(type="str"),
        version_source=dict(
            type="dict", options=version_source_spec, obj=version_source_map
        ),
        vm_spec=dict(
            type="dict", options=vm_specs.get_vm_spec(), obj=vmm_sdk.AhvConfigVm
        ),
        is_active_version=dict(type="bool"),
        is_gc_override_enabled=dict(type="bool"),
    )

    guest_update_status_spec = dict(
        deployed_vm_reference=dict(type="str"),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        template_name=dict(type="str"),
        template_description=dict(type="str"),
        template_version_spec=dict(
            type="dict", options=version_spec, obj=vmm_sdk.TemplateVersionSpec
        ),
        guest_update_status=dict(
            type="dict", options=guest_update_status_spec, obj=vmm_sdk.GuestUpdateStatus
        ),
    )

    return module_args


def create_template(module, result):
    templates = get_templates_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.Template()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create templates Spec", **result)

    if module.check_mode:
        result["response"] = spec.to_dict()
        return

    resp = None
    try:
        resp = templates.create_template(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating template",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.TEMPLATES
        )
        if ext_id:
            resp = get_template(module, templates, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def update_template(module, result):
    templates = get_templates_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_template(module, templates, ext_id)
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if not update_spec.created_by.user_type:
        update_spec.created_by.user_type = "LOCAL"
    if not update_spec.template_version_spec.created_by.user_type:
        update_spec.template_version_spec.created_by.user_type = "LOCAL"
    if update_spec.template_version_spec.ext_id:
        update_spec.template_version_spec.ext_id = None
    if not update_spec.updated_by.user_type:
        update_spec.updated_by.user_type = "LOCAL"

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating templates update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = templates.update_template_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating template",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_template(module, templates, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_template(module, result):
    templates = get_templates_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Template with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_template(module, templates, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for deleting template", **result)

    kwargs = {"if_match": etag}

    try:
        resp = templates.delete_template_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting template",
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
            ("state", "present", ("template_name", "ext_id"), True),
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
    }
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_template(module, result)
        else:
            create_template(module, result)
    else:
        delete_template(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
