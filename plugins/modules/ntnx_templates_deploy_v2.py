#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_templates_deploy_v2
short_description: Deploy Nutanix templates
description:
    - This module allows you to deploy Nutanix templates.
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Deploy VMs from a template) -
      Operation Name: Deploy VM Templates -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will deploy a template.
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external ID of the template to deploy.
        required: true
        type: str
    version_id:
        description:
            - The identifier of a Template Version.
        type: str
    number_of_vms:
        description:
            - Number of VMs to be deployed.
        type: int
    override_vms_config:
        description:
            - A list specifying the VM configuration overrides for each of the VMs to be created.
              Each element in the list corresponds to a VM and includes the override configurations
              such as VM Name, Configuration, and Guest Customization. The position of the element
              in the list defines the index of the VM to which the override configuration will be applied.
        type: list
        elements: dict
        suboptions:
                name:
                    description: Name of the virtual machine
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
                        nic_backing_info:
                            description:
                                - Backing Information about how NIC is associated with a VM.
                                - Will work with pc.7.5 and later.
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
                        nic_network_info:
                            description:
                                - Network configuration for the NIC.
                                - Will work with pc.7.5 and later.
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
                            required: false
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
                                                    - Indicates whether the guest will be freshly installed using this unattend configuration,
                                                      or this unattend configuration will be applied to a pre-prepared image. Default is 'PREPARED'.
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
                                                                    description:
                                                                        - XML content for unattend.xml.
                                                                        - The API requires this value to be base64 encoded.
                                                                        - You can either pass an already-encoded string, or pass the raw
                                                                          unattend.xml content and let Ansible encode it using the
                                                                          C(b64encode) filter, e.g.
                                                                          C("{{ unattend_xml_content | b64encode }}").
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
                                                                            description: The value associated with the key for this key-value pair
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
                                                                        - The cloud-init user-data script.
                                                                        - The API requires this value to be base64 encoded.
                                                                        - You can either pass an already-encoded string, or pass the raw
                                                                          cloud-init script and let Ansible encode it using the
                                                                          C(b64encode) filter, e.g.
                                                                          C("{{ cloud_init_content | b64encode }}").
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
                                                                            description: The value associated with the key for this key-value pair
                                                                            type: raw
                guest_customization_profile_config:
                    description:
                        - Reference to an existing VM Guest Customization Profile to apply when deploying this VM,
                          with optional per-VM overrides.
                        - Mutually exclusive with C(guest_customization) at the API level
                          (use either an inline customization or a profile reference, not both).
                        - Nutanix Guest Tools (NGT) must be installed on the source VM
                          that backs the template; otherwise, the API rejects the
                          template-deploy request with VMM-24120 ("Guest customization
                          profile config is provided during Template deployment but
                          NGT was not installed on the source VM.").
                    required: false
                    type: dict
                    suboptions:
                        profile:
                            description:
                                - Reference to a VM Guest Customization profile.
                            type: dict
                            suboptions:
                                ext_id:
                                    description: External ID of the VM Guest Customization Profile.
                                    type: str
                                    required: true
                        config_override_spec:
                            description:
                                - Sysprep configuration override specification for Windows operating system customization.
                            type: dict
                            suboptions:
                                customization:
                                    description:
                                        - Sysprep customization override.
                                        - Either C(sysprep_params) or C(answer_file) is allowed, not both.
                                    type: dict
                                    suboptions:
                                        answer_file:
                                            description: Override the answer file (unattend.xml).
                                            type: dict
                                            suboptions:
                                                unattend_xml:
                                                    description:
                                                        - The custom unattend.xml file content as a string.
                                                        - This replaces the unattend.xml from the referenced VM Guest Customization Profile.
                                                        - Note that double quotes in the XML file must be escaped to maintain correctness.
                                                        - Should be base64 encoded.
                                                        - You can either pass an already-encoded string, or pass the raw
                                                          unattend.xml content and let Ansible encode it using the
                                                          C(b64encode) filter, e.g.
                                                          C("{{ unattend_xml_content | b64encode }}").
                                                    type: str
                                        sysprep_params:
                                            description: Override individual Sysprep parameters.
                                            type: dict
                                            suboptions:
                                                general_settings:
                                                    description:
                                                    - Override specification for general Windows unattended installation settings.
                                                    - These settings override the corresponding general settings from the referenced profile.
                                                    - To completely discard the setting from the referenced profile, specify an empty object as the value.
                                                    type: dict
                                                    suboptions:
                                                        computer_name:
                                                            description:
                                                                - Override mechanism for computer name generation.
                                                                - You can either use the VM name, provide a computer name,
                                                                  or discard the setting from the referenced profile.
                                                                - If using a VM name or computer name, meet the sysprep's computer name requirements;
                                                                  otherwise, the request would fail.
                                                            type: dict
                                                            suboptions:
                                                                name:
                                                                    description: Set computer name to a specific value.
                                                                    type: dict
                                                                    suboptions:
                                                                        value:
                                                                            description: The computer name.
                                                                            type: str
                                                                use_vm_name:
                                                                    description: Use the deployed VM's name as the computer name.
                                                                    type: dict
                                                                discard:
                                                                    description: Discard the profile's computer-name value.
                                                                    type: dict
                                                        timezone:
                                                            description:
                                                                - Override for timezone setting. You can either provide a new timezone value or
                                                                  discard the setting from the referenced profile.
                                                                - For valid timezone values, refer to Windows sysprep documentation.
                                                            type: dict
                                                            suboptions:
                                                                value:
                                                                    description: Set timezone to a specific value.
                                                                    type: dict
                                                                    suboptions:
                                                                        value:
                                                                            description: Timezone value.
                                                                            type: str
                                                                discard:
                                                                    description: Discard the profile's timezone.
                                                                    type: dict
                                                        administrator_password:
                                                            description:
                                                                - Override for administrator password.
                                                                - You can either provide a new password or discard the setting from the referenced profile.
                                                            type: dict
                                                            suboptions:
                                                                value:
                                                                    description: Set administrator password to a specific value
                                                                    type: dict
                                                                    suboptions:
                                                                        value:
                                                                            description: The administrator password.
                                                                            type: str
                                                                discard:
                                                                    description: Discard the profile's administrator password.
                                                                    type: dict
                                                        auto_logon_settings:
                                                            description:
                                                                - Override specification for autologon settings.
                                                                - These settings override the corresponding autologon settings
                                                                  from the referenced profile.
                                                                - To completely discard the setting from the referenced profile,
                                                                  specify an empty object as the value.
                                                            type: dict
                                                            suboptions:
                                                                logon_count:
                                                                    description:
                                                                        - Override value for the number of automatic logons allowed.
                                                                        - This overrides the logon count from the referenced profile.
                                                                    type: int
                                                        windows_product_key:
                                                            description:
                                                                - Override for Windows product key.
                                                                - You can either provide a new product key or discard the setting from the referenced profile.
                                                                - Note that entering an invalid product key causes Windows Setup to fail.
                                                            type: dict
                                                            suboptions:
                                                                value:
                                                                    description: Set Windows product key to a specific value.
                                                                    type: dict
                                                                    suboptions:
                                                                        value:
                                                                            description: The Windows product key.
                                                                            type: str
                                                                discard:
                                                                    description: Discard the profile's Windows product key.
                                                                    type: dict
                                                        registered_owner:
                                                            description:
                                                                - Override for registered owner information.
                                                                - You can either provide new owner details or discard the setting from the referenced profile.
                                                            type: dict
                                                            suboptions:
                                                                value:
                                                                    description: Set registered owner to a specific value.
                                                                    type: dict
                                                                    suboptions:
                                                                        value:
                                                                            description: The registered owner name.
                                                                            type: str
                                                                discard:
                                                                    description: Discard the profile's registered owner.
                                                                    type: dict
                                                        registered_organization:
                                                            description:
                                                                - Override for registered organization information.
                                                                - You can either provide new organization details or discard
                                                                  the setting from the referenced profile.
                                                            type: dict
                                                            suboptions:
                                                                value:
                                                                    description: Set registered organization to a specific value.
                                                                    type: dict
                                                                    suboptions:
                                                                        value:
                                                                            description: The registered organization name.
                                                                            type: str
                                                                discard:
                                                                    description: Discard the profile's registered organization.
                                                                    type: dict
                                                first_logon_commands:
                                                    description:
                                                        - Override for first logon commands.
                                                        - This overrides the first logon commands from the referenced profile.
                                                        - Commands are executed in the order specified.
                                                        - To completely discard the setting from the referenced profile, specify an empty array as the value.
                                                    type: list
                                                    elements: str
                                                locale_settings:
                                                    description:
                                                        - Override specification for language and input locale settings.
                                                        - These settings override the corresponding locale settings from the referenced profile.
                                                        - To completely discard the setting from the referenced profile, specify an empty object as the value.
                                                    type: dict
                                                    suboptions:
                                                        user_locale:
                                                            description:
                                                                - Override for per-user locale settings used for formatting dates, times, currency, and numbers.
                                                                - You can either provide a new locale value or discard the setting from the referenced profile.
                                                                - Value must follow RFC 3066 language-tagging conventions, for example, en-US, fr-FR, es-ES.
                                                            type: dict
                                                            suboptions:
                                                                value:
                                                                    description: Set user locale to a specific value.
                                                                    type: dict
                                                                    suboptions:
                                                                        value:
                                                                            description: The new locale value.
                                                                            type: str
                                                                discard:
                                                                    description: Discard the profile's user locale.
                                                                    type: dict
                                                        system_locale:
                                                            description:
                                                                - Override for the default language used for non-Unicode programs.
                                                                - You can either provide a new locale value or discard the setting from the referenced profile.
                                                                - Value must follow RFC 3066 language-tagging conventions, for example, en-US, fr-FR, es-ES.
                                                            type: dict
                                                            suboptions:
                                                                value:
                                                                    description: Set system locale to a specific value.
                                                                    type: dict
                                                                    suboptions:
                                                                        value:
                                                                            description: The new locale value.
                                                                            type: str
                                                                discard:
                                                                    description: Discard the profile's system locale.
                                                                    type: dict
                                                        ui_language:
                                                            description:
                                                                - Override for the default system language used to display user interface items.
                                                                - You can either provide a new language value or discard
                                                                  the setting from the referenced profile.
                                                                - Value must follow RFC 3066 language-tagging conventions,
                                                                  for example, en-US, fr-FR, es-ES.
                                                            type: dict
                                                            suboptions:
                                                                value:
                                                                    description: Set UI language to a specific value.
                                                                    type: dict
                                                                    suboptions:
                                                                        value:
                                                                            description: The new language value.
                                                                            type: str
                                                                discard:
                                                                    description: Discard the profile's UI language.
                                                                    type: dict
                                                workgroup_or_domain_info:
                                                    description:
                                                        - Override specification for workgroup or domain information.
                                                        - You can either provide a new workgroup or domain settings or discard
                                                          the settings from the referenced profile.
                                                    type: dict
                                                    suboptions:
                                                        workgroup:
                                                            description: Override workgroup settings.
                                                            type: dict
                                                            suboptions:
                                                                name:
                                                                    description:
                                                                        - Override value for workgroup name.
                                                                        - This overrides the workgroup name from the referenced profile.
                                                                        - It must be a valid NetBIOS name.
                                                                    type: str
                                                        domain_settings:
                                                            description: Override domain join settings.
                                                            type: dict
                                                            suboptions:
                                                                credentials:
                                                                    description:
                                                                        - Override specification for domain credentials.
                                                                        - This overrides the domain credentials from the referenced profile.
                                                                    type: dict
                                                                    suboptions:
                                                                        domain_name:
                                                                            description:
                                                                                - Override value for domain name.
                                                                                - This overrides the domain name from the referenced profile.
                                                                                - Can be either the fully qualified DNS name or NetBIOS name of the domain.
                                                                            type: str
                                                                        username:
                                                                            description:
                                                                                - Override value for domain username.
                                                                                - This overrides the domain username from the referenced profile.
                                                                            type: str
                                                                        password:
                                                                            description:
                                                                                - Override value for domain password.
                                                                                - This overrides the domain password from the referenced profile.
                                                                            type: str
                                                        discard:
                                                            description: Discard the profile's workgroup or domain settings.
                                                            type: dict
                                                network_settings:
                                                    description:
                                                       - Override specification for network settings.
                                                       - These settings override the corresponding network settings from the referenced profile.
                                                       - To completely discard the setting from the referenced profile, specify an empty object as the value.
                                                    type: dict
                                                    suboptions:
                                                        nic_config_list:
                                                            description:
                                                               - Override specification for NIC configuration list.
                                                               - This overrides the NIC configurations from the referenced profile.
                                                               - Configurations are applied to NICs in serial order.
                                                            type: list
                                                            elements: dict
                                                            suboptions:
                                                                dns_config:
                                                                    description:
                                                                        - Override specification for DNS configuration.
                                                                        - This overrides the DNS settings from the referenced profile.
                                                                    type: dict
                                                                    suboptions:
                                                                        preferred_dns_server_address:
                                                                            description:
                                                                                - Override value for preferred DNS server address.
                                                                                - This overrides the preferred DNS server from the referenced profile.
                                                                            type: str
                                                                        alternate_dns_server_addresses:
                                                                            description:
                                                                                - Override value for alternate DNS server addresses.
                                                                                - This overrides the alternate DNS servers from the referenced profile.
                                                                            type: list
                                                                            elements: str
                                                                ipv4_config:
                                                                    description:
                                                                        - Override mechanism for IPv4 configuration.
                                                                        - You can either use DHCP, provide a custom IPv4 configuration,
                                                                          or discard the setting from the referenced profile.
                                                                        - If DHCP is specified, DhcpEnabled is set to True in the unattend.xml.
                                                                    type: dict
                                                                    suboptions:
                                                                        use_dhcp:
                                                                            description: Use DHCP for IPv4.
                                                                            type: dict
                                                                        static_config:
                                                                            description: Static IPv4 configuration.
                                                                            type: dict
                                                                            suboptions:
                                                                                ip_address:
                                                                                    description:
                                                                                        - An unique address that identifies a device on the internet
                                                                                          or a local network in IPv4 format.
                                                                                    type: dict
                                                                                    suboptions:
                                                                                        value:
                                                                                            description: IPv4 address value.
                                                                                            type: str
                                                                                            required: true
                                                                                        prefix_length:
                                                                                            description:
                                                                                                - Prefix length for the address.
                                                                                                - Defaults to 32 if not provided.
                                                                                            type: int
                                                                                default_gateways:
                                                                                    description:
                                                                                        - Override value for default gateways.
                                                                                        - This overrides the default gateway configuration
                                                                                          from the referenced profile.
                                                                                    type: list
                                                                                    elements: str
    cluster_reference:
        description:
            - The identifier of the Cluster where the VM(s) will be created using a Template.
        type: str
    wait:
        description:
            - Whether to wait for the template deployment to complete.
        type: bool
        default: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Deploy VM
  nutanix.ncp.ntnx_templates_deploy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ template_ext_id }}"
    version_id: "{{version_ext_id}}"
    cluster_reference: "{{cluster.uuid}}"

- name: Deploy vm and override config
  nutanix.ncp.ntnx_templates_deploy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ template_ext_id }}"
    version_id: "{{version_ext_id}}"
    cluster_reference: "{{cluster.uuid}}"
    override_vms_config:
      - name: vm_template_override
        num_sockets: 4
        num_cores_per_socket: 4
        num_threads_per_core: 2
        memory_size_bytes: 4294967296

- name: Deploy VM from template with a Guest Customization Profile and per-VM overrides
  nutanix.ncp.ntnx_templates_deploy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ template_ext_id }}"
    version_id: "{{ version_ext_id }}"
    cluster_reference: "{{ cluster.uuid }}"
    number_of_vms: 1
    override_vms_config:
      - name: vm_template_with_profile
        guest_customization_profile_config:
          profile:
            ext_id: "b1c2d3e4-5f67-4890-a123-456789abcdef"
          config_override_spec:
            customization:
              sysprep_params:
                general_settings:
                  computer_name:
                    name:
                      value: "PC-DEPLOY-1"
                  timezone:
                    value:
                      value: "UTC"
                  administrator_password:
                    value:
                      value: "Password123"
                network_settings:
                  nic_config_list:
                    - dns_config:
                        preferred_dns_server_address: "10.0.0.10"
                        alternate_dns_server_addresses:
                          - "10.0.0.11"
                      ipv4_config:
                        static_config:
                          ip_address:
                            value: "10.0.0.50"
                            prefix_length: 24
                          default_gateways:
                            - "10.0.0.1"
"""

RETURN = r"""
ext_id:
    description: The external ID of the deployed template.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
task_ext_id:
    description: The external ID of the deployment task.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
response:
    description: The response from the template deployment API which always includes the task details.
    type: dict
    returned: always
    sample:
        {
                "cluster_ext_ids": null,
                "completed_time": "2024-05-20T08:13:07.945618+00:00",
                "completion_details": null,
                "created_time": "2024-05-20T08:12:59.209878+00:00",
                "entities_affected": [
                    {
                        "ext_id": "fa236286-b965-4125-8367-672e6597a2f8",
                        "rel": "vmm:content:templates"
                    }
                ],
                "error_messages": null,
                "ext_id": "ZXJnb24=:f27e2a60-a171-48e5-a7ab-8872c8560984",
                "is_cancelable": false,
                "last_updated_time": "2024-05-20T08:13:07.945617+00:00",
                "legacy_error_message": null,
                "operation": "kVmTemplateDeploy",
                "operation_description": null,
                "owned_by": {
                    "ext_id": "00000000-0000-0000-0000-000000000000",
                    "name": "admin"
                },
                "parent_task": null,
                "progress_percentage": 100,
                "started_time": "2024-05-20T08:12:59.226669+00:00",
                "status": "SUCCEEDED",
                "sub_steps": null,
                "sub_tasks": [
                    {
                        "ext_id": "ZXJnb24=:1089a445-8d35-47ce-b059-2fad04432017",
                        "href": "https://000.000.000.000:9440/api/prism/v4.0.b1/config/tasks/ZXJnb24=:1089a445-8d35-47ce-b059-2fad04432017",
                        "rel": "subtask"
                    },
                    {
                        "ext_id": "ZXJnb24=:e5f36bac-751d-4e69-b72c-aebb32b6cfea",
                        "href": "https://000.000.000.000:9440/api/prism/v4.0.b1/config/tasks/ZXJnb24=:e5f36bac-751d-4e69-b72c-aebb32b6cfea",
                        "rel": "subtask"
                    },
                    {
                        "ext_id": "ZXJnb24=:a2bca528-3455-4115-9da0-79ed7c0ace96",
                        "href": "https://000.000.000.000:9440/api/prism/v4.0.b1/config/tasks/ZXJnb24=:a2bca528-3455-4115-9da0-79ed7c0ace96",
                        "rel": "subtask"
                    }
                ],
                "warnings": null
            }
changed:
    description: Indicates whether the template deployment changed the system.
    type: bool
    returned: always
    sample: true
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "Api Exception raised while deploying template"
error:
    description: The error message if the template deployment failed.
    type: str
    returned: when error occurs
    sample: "Failed to deploy template"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
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
from ..module_utils.v4.vmm.spec.vm_guest_customization_profiles import (  # noqa: E402
    VmGcProfileOverrideSpecs,
)
from ..module_utils.v4.vmm.spec.vms import VmSpecs as vm_specs  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_override_vm_config_schema():
    override_config_schema = dict(
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
        guest_customization_profile_config=dict(
            type="dict",
            options=VmGcProfileOverrideSpecs.get_guest_customization_profile_config_spec(),
            obj=vmm_sdk.VmGcProfileConfig,
            no_log=False,
        ),
    )
    return override_config_schema


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        version_id=dict(type="str"),
        number_of_vms=dict(type="int"),
        override_vms_config=dict(
            type="list",
            elements="dict",
            options=get_override_vm_config_schema(),
            mutually_exclusive=[
                ("guest_customization", "guest_customization_profile_config"),
            ],
        ),
        cluster_reference=dict(type="str"),
    )

    return module_args


def deploy_template(module, result):
    templates = get_templates_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_template(module, templates, ext_id=ext_id)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.TemplateDeployment()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create templates deploy spec", **result)

    # Generate override vm config map for each VM
    override_vms_config = module.params.get("override_vms_config", [])
    if override_vms_config:
        override_vm_config_map = {}
        vm_index = 0
        override_vms_config_schema = get_override_vm_config_schema()
        kwargs = {"module_args": override_vms_config_schema}
        for vm_config in override_vms_config:
            s = vmm_sdk.VmConfigOverride()
            s, err = sg.generate_spec(obj=s, attr=vm_config, **kwargs)
            if err:
                result["error"] = err
                module.fail_json(
                    msg="Failed generating vm config override spec", **result
                )
            override_vm_config_map[str(vm_index)] = s
            vm_index += 1

        spec.override_vm_config_map = override_vm_config_map

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create deploy template spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        version_ext_id = module.params.get("version_id")
        result["msg"] = (
            "Template ({0}) with given version ({1}) will be deployed.".format(
                ext_id,
                version_ext_id  # fmt: skip
            )
        )
        return

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for deploying template", **result)

    kwargs = {"if_match": etag}

    try:
        resp = templates.deploy_template(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deploying template",
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
    }
    deploy_template(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
