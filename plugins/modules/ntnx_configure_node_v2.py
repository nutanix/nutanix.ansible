#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_configure_node_v2
short_description: Configures the node in the hardware provider with the given settings
version_added: "2.7.0"
description:
  - Configures the node in the hardware provider with the given settings.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Configure Node) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module will configure the node.
      - If C(state) is C(absent), the module will fail.
    type: str
    choices:
      - present
    default: present
  configuration:
    description:
      - Configuration for configuring a node.
      - Exactly one of the mutually exclusive suboptions must be provided.
    type: dict
    required: true
    suboptions:
      configure_server_details:
        description:
          - Configuration details for setting up a server node in the hardware provider.
          - Mutually exclusive with C(pre_cluster_config_details), C(post_cluster_config_details)
            and C(un_configure_server_details).
        type: dict
        required: false
        suboptions:
          node_ext_id:
            description:
              - External ID of the node.
            type: str
            required: true
          group_id:
            description:
              - Identifier of the group (e.g., organization or tenant) to which the node belongs.
              - This field is required for Cisco nodes.
            type: str
            required: false
          server_settings_config:
            description:
              - Configuration settings for the server hardware.
            type: dict
            required: false
            suboptions:
              network_adaptor_fec_mode:
                description:
                  - Forward Error Correction (FEC) mode for the network adaptor.
                type: str
                required: false
                choices:
                  - CL91
                  - CL74
                  - "OFF"
              server_identity_pool_ext_id:
                description:
                  - UUID of the server identity pool to be used for server configuration.
                type: str
                required: false
          physical_network_adapter_config:
            description:
              - Configuration for physical network adapters with network groups and port mappings.
            type: dict
            required: false
            suboptions:
              network_groups:
                description:
                  - List of network groups defining network segments with their associated VLANs and port mappings.
                type: list
                elements: dict
                required: false
                suboptions:
                  name:
                    description:
                      - Name of the network group.
                    type: str
                    required: true
                  type:
                    description:
                      - Type of the network group defining its purpose.
                    type: str
                    required: true
                    choices:
                      - INFRA
                  mtu_bytes:
                    description:
                      - Maximum Transmission Unit (MTU) size for the network group.
                    type: int
                    required: false
                  vlans:
                    description:
                      - VLAN IDs or VLAN ranges assigned to the network group (e.g., '100' or '100-200').
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - Value of the VLAN configuration that can be either a single VLAN ID or a VLAN range.
                          - Provide exactly one of C(vlan_id) or C(vlan_range).
                        type: dict
                        required: true
                        suboptions:
                          vlan_id:
                            description:
                              - Configuration for a single VLAN identifier.
                              - Mutually exclusive with C(vlan_range).
                            type: dict
                            required: false
                            suboptions:
                              id:
                                description:
                                  - Configuration for a single VLAN identifier.
                                type: int
                                required: true
                          vlan_range:
                            description:
                              - Configuration for a range of VLAN identifiers.
                              - Mutually exclusive with C(vlan_id).
                            type: dict
                            required: false
                            suboptions:
                              start_id:
                                description:
                                  - Starting VLAN ID for the range (inclusive).
                                type: int
                                required: true
                              end_id:
                                description:
                                  - Ending VLAN ID for the range (inclusive).
                                type: int
                                required: true
                  port_mappings:
                    description:
                      - List of physical port mappings by MAC address.
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      mac_address:
                        description:
                          - MAC address of the physical network interface to be mapped to this network group.
                        type: str
                        required: false
          bmc_ip_addressing_config:
            description:
              - BMC IP addressing configuration for the node.
              - Provide exactly one of C(in_out_band_bmc_ip_config) or C(unified_bmc_ip_config).
            type: dict
            required: false
            suboptions:
              in_out_band_bmc_ip_config:
                description:
                  - BMC IP addressing configuration with separate in-band and out-of-band options.
                  - Mutually exclusive with C(unified_bmc_ip_config).
                type: dict
                required: false
                suboptions:
                  in_band:
                    description:
                      - BMC IP configuration containing IPv4 and IPv6 addressing options for in-band.
                    type: dict
                    required: false
                    suboptions:
                      ipv4:
                        description:
                          - IPv4 configuration for the BMC.
                          - Provide exactly one of C(ip_pool_config) or C(static_ip_config).
                        type: dict
                        required: false
                        suboptions:
                          ip_pool_config:
                            description:
                              - IP configuration using a pool of IP addresses from the hardware provider.
                              - Mutually exclusive with C(static_ip_config).
                            type: dict
                            required: false
                            suboptions:
                              ip_pool_ext_id:
                                description:
                                  - Unique identifier (UUID) of the IP pool.
                                type: str
                                required: false
                              vlan_id:
                                description:
                                  - Configuration for a single VLAN identifier.
                                type: int
                                required: false
                          static_ip_config:
                            description:
                              - IP configuration using a static IP address.
                              - Mutually exclusive with C(ip_pool_config).
                            type: dict
                            required: false
                            suboptions:
                              ip_address:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  ipv4:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv4 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv4 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                                  ipv6:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv6 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv6 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                              gateway:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  ipv4:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv4 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv4 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                                  ipv6:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv6 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv6 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                              vlan_id:
                                description:
                                  - Configuration for a single VLAN identifier.
                                type: int
                                required: false
                      ipv6:
                        description:
                          - IPv6 configuration for the BMC.
                          - Provide exactly one of C(ip_pool_config) or C(static_ip_config).
                        type: dict
                        required: false
                        suboptions:
                          ip_pool_config:
                            description:
                              - IP configuration using a pool of IP addresses from the hardware provider.
                              - Mutually exclusive with C(static_ip_config).
                            type: dict
                            required: false
                            suboptions:
                              ip_pool_ext_id:
                                description:
                                  - Unique identifier (UUID) of the IP pool.
                                type: str
                                required: false
                              vlan_id:
                                description:
                                  - Configuration for a single VLAN identifier.
                                type: int
                                required: false
                          static_ip_config:
                            description:
                              - IP configuration using a static IP address.
                              - Mutually exclusive with C(ip_pool_config).
                            type: dict
                            required: false
                            suboptions:
                              ip_address:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  ipv4:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv4 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv4 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                                  ipv6:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv6 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv6 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                              gateway:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  ipv4:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv4 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv4 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                                  ipv6:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv6 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv6 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                              vlan_id:
                                description:
                                  - Configuration for a single VLAN identifier.
                                type: int
                                required: false
                  out_of_band:
                    description:
                      - BMC IP configuration containing IPv4 and IPv6 addressing options for out-of-band.
                    type: dict
                    required: false
                    suboptions:
                      ipv4:
                        description:
                          - IPv4 configuration for the BMC.
                          - Provide exactly one of C(ip_pool_config) or C(static_ip_config).
                        type: dict
                        required: false
                        suboptions:
                          ip_pool_config:
                            description:
                              - IP configuration using a pool of IP addresses from the hardware provider.
                              - Mutually exclusive with C(static_ip_config).
                            type: dict
                            required: false
                            suboptions:
                              ip_pool_ext_id:
                                description:
                                  - Unique identifier (UUID) of the IP pool.
                                type: str
                                required: false
                              vlan_id:
                                description:
                                  - Configuration for a single VLAN identifier.
                                type: int
                                required: false
                          static_ip_config:
                            description:
                              - IP configuration using a static IP address.
                              - Mutually exclusive with C(ip_pool_config).
                            type: dict
                            required: false
                            suboptions:
                              ip_address:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  ipv4:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv4 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv4 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                                  ipv6:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv6 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv6 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                              gateway:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  ipv4:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv4 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv4 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                                  ipv6:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv6 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv6 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                              vlan_id:
                                description:
                                  - Configuration for a single VLAN identifier.
                                type: int
                                required: false
                      ipv6:
                        description:
                          - IPv6 configuration for the BMC.
                          - Provide exactly one of C(ip_pool_config) or C(static_ip_config).
                        type: dict
                        required: false
                        suboptions:
                          ip_pool_config:
                            description:
                              - IP configuration using a pool of IP addresses from the hardware provider.
                              - Mutually exclusive with C(static_ip_config).
                            type: dict
                            required: false
                            suboptions:
                              ip_pool_ext_id:
                                description:
                                  - Unique identifier (UUID) of the IP pool.
                                type: str
                                required: false
                              vlan_id:
                                description:
                                  - Configuration for a single VLAN identifier.
                                type: int
                                required: false
                          static_ip_config:
                            description:
                              - IP configuration using a static IP address.
                              - Mutually exclusive with C(ip_pool_config).
                            type: dict
                            required: false
                            suboptions:
                              ip_address:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  ipv4:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv4 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv4 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                                  ipv6:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv6 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv6 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                              gateway:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 or IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  ipv4:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv4 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv4 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                                  ipv6:
                                    description:
                                      - An unique address that identifies a device on the internet or a local network
                                        in IPv6 format.
                                    type: dict
                                    required: false
                                    suboptions:
                                      value:
                                        description:
                                          - The IPv6 address of the host.
                                        type: str
                                        required: true
                                      prefix_length:
                                        description:
                                          - The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                              vlan_id:
                                description:
                                  - Configuration for a single VLAN identifier.
                                type: int
                                required: false
              unified_bmc_ip_config:
                description:
                  - Unified BMC IP addressing configuration with direct IPv4 and IPv6 settings.
                  - Mutually exclusive with C(in_out_band_bmc_ip_config).
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - IPv4 configuration for the BMC.
                      - Provide exactly one of C(ip_pool_config) or C(static_ip_config).
                    type: dict
                    required: false
                    suboptions:
                      ip_pool_config:
                        description:
                          - IP configuration using a pool of IP addresses from the hardware provider.
                          - Mutually exclusive with C(static_ip_config).
                        type: dict
                        required: false
                        suboptions:
                          ip_pool_ext_id:
                            description:
                              - Unique identifier (UUID) of the IP pool.
                            type: str
                            required: false
                          vlan_id:
                            description:
                              - Configuration for a single VLAN identifier.
                            type: int
                            required: false
                      static_ip_config:
                        description:
                          - IP configuration using a static IP address.
                          - Mutually exclusive with C(ip_pool_config).
                        type: dict
                        required: false
                        suboptions:
                          ip_address:
                            description:
                              - An unique address that identifies a device on the internet or a local network
                                in IPv4 or IPv6 format.
                            type: dict
                            required: false
                            suboptions:
                              ipv4:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 format.
                                type: dict
                                required: false
                                suboptions:
                                  value:
                                    description:
                                      - The IPv4 address of the host.
                                    type: str
                                    required: true
                                  prefix_length:
                                    description:
                                      - The prefix length of the network to which this host IPv4 address belongs.
                                    type: int
                                    required: false
                                    default: 32
                              ipv6:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  value:
                                    description:
                                      - The IPv6 address of the host.
                                    type: str
                                    required: true
                                  prefix_length:
                                    description:
                                      - The prefix length of the network to which this host IPv6 address belongs.
                                    type: int
                                    required: false
                                    default: 128
                          gateway:
                            description:
                              - An unique address that identifies a device on the internet or a local network
                                in IPv4 or IPv6 format.
                            type: dict
                            required: false
                            suboptions:
                              ipv4:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 format.
                                type: dict
                                required: false
                                suboptions:
                                  value:
                                    description:
                                      - The IPv4 address of the host.
                                    type: str
                                    required: true
                                  prefix_length:
                                    description:
                                      - The prefix length of the network to which this host IPv4 address belongs.
                                    type: int
                                    required: false
                                    default: 32
                              ipv6:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  value:
                                    description:
                                      - The IPv6 address of the host.
                                    type: str
                                    required: true
                                  prefix_length:
                                    description:
                                      - The prefix length of the network to which this host IPv6 address belongs.
                                    type: int
                                    required: false
                                    default: 128
                          vlan_id:
                            description:
                              - Configuration for a single VLAN identifier.
                            type: int
                            required: false
                  ipv6:
                    description:
                      - IPv6 configuration for the BMC.
                      - Provide exactly one of C(ip_pool_config) or C(static_ip_config).
                    type: dict
                    required: false
                    suboptions:
                      ip_pool_config:
                        description:
                          - IP configuration using a pool of IP addresses from the hardware provider.
                          - Mutually exclusive with C(static_ip_config).
                        type: dict
                        required: false
                        suboptions:
                          ip_pool_ext_id:
                            description:
                              - Unique identifier (UUID) of the IP pool.
                            type: str
                            required: false
                          vlan_id:
                            description:
                              - Configuration for a single VLAN identifier.
                            type: int
                            required: false
                      static_ip_config:
                        description:
                          - IP configuration using a static IP address.
                          - Mutually exclusive with C(ip_pool_config).
                        type: dict
                        required: false
                        suboptions:
                          ip_address:
                            description:
                              - An unique address that identifies a device on the internet or a local network
                                in IPv4 or IPv6 format.
                            type: dict
                            required: false
                            suboptions:
                              ipv4:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 format.
                                type: dict
                                required: false
                                suboptions:
                                  value:
                                    description:
                                      - The IPv4 address of the host.
                                    type: str
                                    required: true
                                  prefix_length:
                                    description:
                                      - The prefix length of the network to which this host IPv4 address belongs.
                                    type: int
                                    required: false
                                    default: 32
                              ipv6:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  value:
                                    description:
                                      - The IPv6 address of the host.
                                    type: str
                                    required: true
                                  prefix_length:
                                    description:
                                      - The prefix length of the network to which this host IPv6 address belongs.
                                    type: int
                                    required: false
                                    default: 128
                          gateway:
                            description:
                              - An unique address that identifies a device on the internet or a local network
                                in IPv4 or IPv6 format.
                            type: dict
                            required: false
                            suboptions:
                              ipv4:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv4 format.
                                type: dict
                                required: false
                                suboptions:
                                  value:
                                    description:
                                      - The IPv4 address of the host.
                                    type: str
                                    required: true
                                  prefix_length:
                                    description:
                                      - The prefix length of the network to which this host IPv4 address belongs.
                                    type: int
                                    required: false
                                    default: 32
                              ipv6:
                                description:
                                  - An unique address that identifies a device on the internet or a local network
                                    in IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                  value:
                                    description:
                                      - The IPv6 address of the host.
                                    type: str
                                    required: true
                                  prefix_length:
                                    description:
                                      - The prefix length of the network to which this host IPv6 address belongs.
                                    type: int
                                    required: false
                                    default: 128
                          vlan_id:
                            description:
                              - Configuration for a single VLAN identifier.
                            type: int
                            required: false
      pre_cluster_config_details:
        description:
          - Configuration details for pre-cluster operations on nodes before cluster creation or expansion.
          - Mutually exclusive with C(configure_server_details), C(post_cluster_config_details)
            and C(un_configure_server_details).
        type: dict
        required: false
        suboptions:
          nodes:
            description:
              - List of nodes to perform pre-cluster operations on.
            type: list
            elements: dict
            required: true
            suboptions:
              ext_id:
                description:
                  - External ID of the node.
                type: str
                required: true
      post_cluster_config_details:
        description:
          - Configuration details for post-cluster operations on nodes after cluster creation.
          - Mutually exclusive with C(configure_server_details), C(pre_cluster_config_details)
            and C(un_configure_server_details).
        type: dict
        required: false
        suboptions:
          cluster_ext_id:
            description:
              - External ID of the cluster.
            type: str
            required: true
          nodes:
            description:
              - List of nodes to perform post-cluster operations on.
            type: list
            elements: dict
            required: true
            suboptions:
              ext_id:
                description:
                  - External ID of the node.
                type: str
                required: true
      un_configure_server_details:
        description:
          - Configuration to unconfigure a node and optionally clean up policies.
          - Mutually exclusive with C(configure_server_details), C(pre_cluster_config_details)
            and C(post_cluster_config_details).
        type: dict
        required: false
        suboptions:
          node_ext_id:
            description:
              - External ID of the node.
            type: str
            required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Configure a server node
  nutanix.ncp.ntnx_configure_node_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    configuration:
      configure_server_details:
        node_ext_id: "7eee1613-ac19-4a32-8d6a-c8ed93c5cf06"
        group_id: "group-1"
        server_settings_config:
          network_adaptor_fec_mode: CL91
          server_identity_pool_ext_id: "c30eea15-2ea6-47b4-9cb9-0b63aa215e1f"
        physical_network_adapter_config:
          network_groups:
            - name: infra
              type: INFRA
              mtu_bytes: 1500
              vlans:
                - value:
                    vlan_id:
                      id: 64
              port_mappings:
                - mac_address: "4e:ae:b6:ec:9e:aa"
        bmc_ip_addressing_config:
          in_out_band_bmc_ip_config:
            in_band:
              ipv4:
                ip_pool_config:
                  ip_pool_ext_id: "ec149395-ae87-42ec-9c26-d0266bf60550"
                  vlan_id: 6
  register: result
  ignore_errors: true

- name: Apply pre-cluster configuration to nodes
  nutanix.ncp.ntnx_configure_node_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    configuration:
      pre_cluster_config_details:
        nodes:
          - ext_id: "7eee1613-ac19-4a32-8d6a-c8ed93c5cf06"
  register: result
  ignore_errors: true

- name: Apply post-cluster configuration to nodes
  nutanix.ncp.ntnx_configure_node_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    configuration:
      post_cluster_config_details:
        cluster_ext_id: "fb464f35-4c44-41e5-b401-38cbffe2d7e6"
        nodes:
          - ext_id: "7eee1613-ac19-4a32-8d6a-c8ed93c5cf06"
  register: result
  ignore_errors: true

- name: Unconfigure a server node
  nutanix.ncp.ntnx_configure_node_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    configuration:
      un_configure_server_details:
        node_ext_id: "7eee1613-ac19-4a32-8d6a-c8ed93c5cf06"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for configuring a node.
    - Task details when C(wait) is true.
  returned: always
  type: dict
  sample:
    {
      "completed_time": "2026-09-09T06:26:51.524581+00:00",
      "created_time": "2026-09-09T06:26:47.167906+00:00",
      "entities_affected": [
        {"ext_id": "d1a1a1a1-1111-2222-3333-444455556666", "rel": "lifecycle:config:node"}
      ],
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "operation": "ConfigureNode",
      "operation_description": "Configure node",
      "status": "SUCCEEDED"
    }

changed:
  description: This indicates whether the action was executed.
  returned: always
  type: bool
  sample: true

task_ext_id:
  description: The external ID of the task.
  returned: when applicable
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the related entity if returned.
  returned: when applicable
  type: str
  sample: "d1a1a1a1-1111-2222-3333-444455556666"

msg:
  description: This indicates the status or error message.
  returned: contextual
  type: str
  sample: "Node configuration will be triggered."

error:
  description: This field holds the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_nodes_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )
    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )
    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            obj=lifecycle_sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            obj=lifecycle_sdk.IPv6Address,
            required=False,
        ),
    )

    ip_pool_config_spec = dict(
        ip_pool_ext_id=dict(type="str", required=False),
        vlan_id=dict(type="int", required=False),
    )
    static_ip_config_spec = dict(
        ip_address=dict(
            type="dict",
            options=ip_address_spec,
            obj=lifecycle_sdk.IPAddress,
            required=False,
        ),
        gateway=dict(
            type="dict",
            options=ip_address_spec,
            obj=lifecycle_sdk.IPAddress,
            required=False,
        ),
        vlan_id=dict(type="int", required=False),
    )

    bmc_ip_version_spec = dict(
        ip_pool_config=dict(
            type="dict",
            options=ip_pool_config_spec,
            required=False,
        ),
        static_ip_config=dict(
            type="dict",
            options=static_ip_config_spec,
            required=False,
        ),
    )
    bmc_ip_version_obj = {
        "ip_pool_config": lifecycle_sdk.IPPoolConfig,
        "static_ip_config": lifecycle_sdk.StaticIPConfig,
    }
    bmc_ip_config_spec = dict(
        ipv4=dict(
            type="dict",
            options=bmc_ip_version_spec,
            obj=bmc_ip_version_obj,
            required=False,
            mutually_exclusive=[("ip_pool_config", "static_ip_config")],
        ),
        ipv6=dict(
            type="dict",
            options=bmc_ip_version_spec,
            obj=bmc_ip_version_obj,
            required=False,
            mutually_exclusive=[("ip_pool_config", "static_ip_config")],
        ),
    )

    in_out_band_bmc_ip_config_spec = dict(
        in_band=dict(
            type="dict",
            options=bmc_ip_config_spec,
            obj=lifecycle_sdk.BmcIPConfig,
            required=False,
        ),
        out_of_band=dict(
            type="dict",
            options=bmc_ip_config_spec,
            obj=lifecycle_sdk.BmcIPConfig,
            required=False,
        ),
    )
    unified_bmc_ip_config_spec = dict(
        ipv4=dict(
            type="dict",
            options=bmc_ip_version_spec,
            obj=bmc_ip_version_obj,
            required=False,
            mutually_exclusive=[("ip_pool_config", "static_ip_config")],
        ),
        ipv6=dict(
            type="dict",
            options=bmc_ip_version_spec,
            obj=bmc_ip_version_obj,
            required=False,
            mutually_exclusive=[("ip_pool_config", "static_ip_config")],
        ),
    )

    bmc_ip_addressing_config_spec = dict(
        in_out_band_bmc_ip_config=dict(
            type="dict",
            options=in_out_band_bmc_ip_config_spec,
            required=False,
        ),
        unified_bmc_ip_config=dict(
            type="dict",
            options=unified_bmc_ip_config_spec,
            required=False,
        ),
    )

    vlan_id_spec = dict(
        id=dict(type="int", required=True),
    )
    vlan_range_spec = dict(
        start_id=dict(type="int", required=True),
        end_id=dict(type="int", required=True),
    )
    vlan_info_spec = dict(
        value=dict(
            type="dict",
            required=True,
            options=dict(
                vlan_id=dict(
                    type="dict",
                    options=vlan_id_spec,
                    required=False,
                ),
                vlan_range=dict(
                    type="dict",
                    options=vlan_range_spec,
                    required=False,
                ),
            ),
            obj={
                "vlan_id": lifecycle_sdk.VlanId,
                "vlan_range": lifecycle_sdk.VlanRange,
            },
            mutually_exclusive=[("vlan_id", "vlan_range")],
            required_one_of=[("vlan_id", "vlan_range")],
        ),
    )
    port_mapping_spec = dict(
        mac_address=dict(type="str", required=False),
    )
    network_group_spec = dict(
        name=dict(type="str", required=True),
        type=dict(type="str", required=True, choices=["INFRA"]),
        mtu_bytes=dict(type="int", required=False),
        vlans=dict(
            type="list",
            elements="dict",
            options=vlan_info_spec,
            obj=lifecycle_sdk.VlanInfo,
            required=False,
        ),
        port_mappings=dict(
            type="list",
            elements="dict",
            options=port_mapping_spec,
            obj=lifecycle_sdk.PortMapping,
            required=False,
        ),
    )
    physical_network_adapter_config_spec = dict(
        network_groups=dict(
            type="list",
            elements="dict",
            options=network_group_spec,
            obj=lifecycle_sdk.NetworkGroup,
            required=False,
        ),
    )

    server_settings_config_spec = dict(
        network_adaptor_fec_mode=dict(
            type="str",
            required=False,
            choices=["CL91", "CL74", "OFF"],
        ),
        server_identity_pool_ext_id=dict(type="str", required=False),
    )

    configure_server_details_spec = dict(
        node_ext_id=dict(type="str", required=True),
        group_id=dict(type="str", required=False),
        server_settings_config=dict(
            type="dict",
            options=server_settings_config_spec,
            obj=lifecycle_sdk.ServerSettingsConfig,
            required=False,
        ),
        physical_network_adapter_config=dict(
            type="dict",
            options=physical_network_adapter_config_spec,
            obj=lifecycle_sdk.PhysicalNetworkAdapterConfig,
            required=False,
        ),
        bmc_ip_addressing_config=dict(
            type="dict",
            options=bmc_ip_addressing_config_spec,
            obj={
                "in_out_band_bmc_ip_config": lifecycle_sdk.InOutBandBmcIPConfig,
                "unified_bmc_ip_config": lifecycle_sdk.UnifiedBmcIPConfig,
            },
            required=False,
            mutually_exclusive=[("in_out_band_bmc_ip_config", "unified_bmc_ip_config")],
        ),
    )

    node_info_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    pre_cluster_config_details_spec = dict(
        nodes=dict(
            type="list",
            elements="dict",
            options=node_info_spec,
            obj=lifecycle_sdk.NodeInfo,
            required=True,
        ),
    )

    post_cluster_config_details_spec = dict(
        cluster_ext_id=dict(type="str", required=True),
        nodes=dict(
            type="list",
            elements="dict",
            options=node_info_spec,
            obj=lifecycle_sdk.NodeInfo,
            required=True,
        ),
    )

    un_configure_server_details_spec = dict(
        node_ext_id=dict(type="str", required=True),
    )

    configuration_spec = dict(
        configure_server_details=dict(
            type="dict",
            options=configure_server_details_spec,
            required=False,
        ),
        pre_cluster_config_details=dict(
            type="dict",
            options=pre_cluster_config_details_spec,
            required=False,
        ),
        post_cluster_config_details=dict(
            type="dict",
            options=post_cluster_config_details_spec,
            required=False,
        ),
        un_configure_server_details=dict(
            type="dict",
            options=un_configure_server_details_spec,
            required=False,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        configuration=dict(
            type="dict",
            required=True,
            options=configuration_spec,
            obj={
                "configure_server_details": lifecycle_sdk.ConfigureServerDetails,
                "pre_cluster_config_details": lifecycle_sdk.PreClusterConfigDetails,
                "post_cluster_config_details": lifecycle_sdk.PostClusterConfigDetails,
                "un_configure_server_details": lifecycle_sdk.UnConfigureServerDetails,
            },
            mutually_exclusive=[
                (
                    "configure_server_details",
                    "pre_cluster_config_details",
                    "post_cluster_config_details",
                    "un_configure_server_details",
                )
            ],
            required_one_of=[
                (
                    "configure_server_details",
                    "pre_cluster_config_details",
                    "post_cluster_config_details",
                    "un_configure_server_details",
                )
            ],
        ),
    )
    return module_args


def run_action(module, result, api_instance):
    validate_required_params(module, ["configuration"])

    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.ConfigureNodeSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for configuring node", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Node configuration will be triggered."
        return

    resp = None
    try:
        resp = api_instance.configure_node(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while configuring node",
        )
    if resp is not None and getattr(resp, "data", None) is not None:
        task_ext_id = getattr(resp.data, "ext_id", None)
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
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_nodes_api_instance(module)
    run_action(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
