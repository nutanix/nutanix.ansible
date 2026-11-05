#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_image_node_v2
short_description: Image a node
version_added: "2.7.0"
description:
  - Installs AOS or hypervisor or host OS on the node.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Image a Node) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module will image the node.
      - If C(state) is C(absent), the module will fail.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - External ID of the node
    type: str
    required: true
  configuration:
    description:
      - Configuration for imaging a node
      - Provide exactly one of C(host_installation_details), C(aos_installation_details),
        C(hci_imaging_details), or C(reconfiguration_details).
    type: dict
    required: true
    suboptions:
      host_installation_details:
        description:
          - Hypervisor or host OS installation details of the node
          - Mutually exclusive with C(aos_installation_details), C(hci_imaging_details),
            and C(reconfiguration_details).
        type: dict
        required: false
        suboptions:
          patched_image_ext_id:
            description:
              - External ID of a patched hypervisor or host OS image
            type: str
            required: true
          patched_image_url:
            description:
              - URL of the patched image to be installed on the node.
              - If the URL is provided, nodes download the image from the given URL instead of
                downloading it from Foundation Central
            type: str
            required: false
      aos_installation_details:
        description:
          - AOS installation details for the node
          - Mutually exclusive with C(host_installation_details), C(hci_imaging_details),
            and C(reconfiguration_details).
        type: dict
        required: false
        suboptions:
          network_details:
            description:
              - Networking configuration for AOS including management interface
            type: dict
            required: true
            suboptions:
              management:
                description:
                  - Details of the network
                type: dict
                required: true
                suboptions:
                  ip:
                    description:
                      - IP address of the network
                    type: dict
                    required: false
                    suboptions:
                      ipv4:
                        description:
                          - An unique address that identifies a device on the internet or a local
                            network in IPv4 format.
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
                              - The prefix length of the network to which this host IPv4 address
                                belongs.
                            type: int
                            required: false
                            default: 32
                      ipv6:
                        description:
                          - An unique address that identifies a device on the internet or a local
                            network in IPv6 format.
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
                              - The prefix length of the network to which this host IPv6 address
                                belongs.
                            type: int
                            required: false
                            default: 128
                  gateway:
                    description:
                      - Gateway IP of the network
                    type: dict
                    required: false
                    suboptions:
                      ipv4:
                        description:
                          - An unique address that identifies a device on the internet or a local
                            network in IPv4 format.
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
                              - The prefix length of the network to which this host IPv4 address
                                belongs.
                            type: int
                            required: false
                            default: 32
                      ipv6:
                        description:
                          - An unique address that identifies a device on the internet or a local
                            network in IPv6 format.
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
                              - The prefix length of the network to which this host IPv6 address
                                belongs.
                            type: int
                            required: false
                            default: 128
                  vlan_id:
                    description:
                      - VLAN ID of the network
                    type: int
                    required: false
          name_servers:
            description:
              - List of DNS servers for the CVM
            type: list
            elements: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - An unique address that identifies a device on the internet or a local
                    network in IPv4 format.
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
                  - An unique address that identifies a device on the internet or a local
                    network in IPv6 format.
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
          ntp_servers:
            description:
              - List of NTP servers for the CVM
            type: list
            elements: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - An unique address that identifies a device on the internet or a local
                    network in IPv4 format.
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
                  - An unique address that identifies a device on the internet or a local
                    network in IPv6 format.
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
              fqdn:
                description:
                  - A fully qualified domain name that specifies its exact location in the tree
                    hierarchy of the Domain Name System.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The fully qualified domain name of the host.
                    type: str
                    required: false
          aos_image_details:
            description:
              - Details of the AOS image
              - Provide C(local_aos_image_details).
            type: dict
            required: true
            suboptions:
              local_aos_image_details:
                description:
                  - Details of the AOS image managed by Foundation Central
                type: dict
                required: true
                suboptions:
                  ext_id:
                    description:
                      - External ID of the AOS image managed by Foundation Central
                    type: str
                    required: true
          cvm_memory_gb:
            description:
              - Memory allocation for the CVM in GB.
              - This value will be overridden by FC if it does not fall within the range expected
                by Foundation Central for the given node
            type: int
            required: false
      hci_imaging_details:
        description:
          - Hyper Converged Infrastructure imaging configuration including hypervisor and AOS
            details
          - Mutually exclusive with C(host_installation_details), C(aos_installation_details),
            and C(reconfiguration_details).
        type: dict
        required: false
        suboptions:
          hypervisor_details:
            description:
              - Hypervisor installation details for HCI configuration
            type: dict
            required: true
            suboptions:
              hostname:
                description:
                  - Hostname of the hypervisor or host OS
                type: str
                required: true
              image_details:
                description:
                  - Details of the hypervisor image to be installed on the node
                  - Provide C(local_host_image_details).
                type: dict
                required: true
                suboptions:
                  local_host_image_details:
                    description:
                      - Details of the uploaded host image
                    type: dict
                    required: true
                    suboptions:
                      ext_id:
                        description:
                          - External ID of the uploaded host image
                        type: str
                        required: true
              network_details:
                description:
                  - Networking configuration for HCI hypervisor including management interface
                type: dict
                required: true
                suboptions:
                  management:
                    description:
                      - Details of the management network
                    type: dict
                    required: true
                    suboptions:
                      mtu_bytes:
                        description:
                          - Maximum transmission unit of the management network
                        type: int
                        required: false
                      vlan_id:
                        description:
                          - VLAN ID of the network
                        type: int
                        required: false
                      ip:
                        description:
                          - IP address of the network
                        type: dict
                        required: false
                        suboptions:
                          ipv4:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv4 format.
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
                                  - The prefix length of the network to which this host IPv4
                                    address belongs.
                                type: int
                                required: false
                                default: 32
                          ipv6:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv6 format.
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
                                  - The prefix length of the network to which this host IPv6
                                    address belongs.
                                type: int
                                required: false
                                default: 128
                      gateway:
                        description:
                          - Gateway IP of the network
                        type: dict
                        required: false
                        suboptions:
                          ipv4:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv4 format.
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
                                  - The prefix length of the network to which this host IPv4
                                    address belongs.
                                type: int
                                required: false
                                default: 32
                          ipv6:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv6 format.
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
                                  - The prefix length of the network to which this host IPv6
                                    address belongs.
                                type: int
                                required: false
                                default: 128
                      bond_settings:
                        description:
                          - Network bonding configuration.
                          - Choose either Active-Backup bonding for simple failover or LACP bonding
                            for dynamic link aggregation
                        type: dict
                        required: false
                        suboptions:
                          bond_config:
                            description:
                              - Bond configuration type
                              - Provide exactly one of C(active_backup_bond) or C(lacp_bond).
                            type: dict
                            required: false
                            suboptions:
                              active_backup_bond:
                                description:
                                  - Active-Backup bonding configuration where one NIC is active and
                                    others provide failover redundancy
                                  - Mutually exclusive with C(lacp_bond).
                                type: dict
                                required: false
                                suboptions:
                                  nics:
                                    description:
                                      - Details of the NICs
                                    type: dict
                                    required: true
                                    suboptions:
                                      mac_address:
                                        description:
                                          - MAC address of the NIC
                                        type: list
                                        elements: str
                                        required: false
                              lacp_bond:
                                description:
                                  - LACP (Link Aggregation Control Protocol) bonding configuration
                                    for dynamic link aggregation
                                  - Mutually exclusive with C(active_backup_bond).
                                type: dict
                                required: false
                                suboptions:
                                  lacp_settings:
                                    description:
                                      - Details of the LACP settings
                                    type: dict
                                    required: true
                                    suboptions:
                                      rate:
                                        description:
                                          - Rate of the LACP
                                        type: str
                                        required: false
                                        choices:
                                          - SLOW
                                          - FAST
                                  nics:
                                    description:
                                      - Details of the NICs
                                    type: dict
                                    required: true
                                    suboptions:
                                      mac_address:
                                        description:
                                          - MAC address of the NIC
                                        type: list
                                        elements: str
                                        required: false
              name_servers:
                description:
                  - List of nameserver IP addresses to be used by the host
                type: list
                elements: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv4 format.
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
                          - The prefix length of the network to which this host IPv4 address
                            belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv6 format.
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
                          - The prefix length of the network to which this host IPv6 address
                            belongs.
                        type: int
                        required: false
                        default: 128
              ntp_servers:
                description:
                  - List of NTP server IP addresses to be used by the host
                type: list
                elements: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv4 format.
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
                          - The prefix length of the network to which this host IPv4 address
                            belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv6 format.
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
                          - The prefix length of the network to which this host IPv6 address
                            belongs.
                        type: int
                        required: false
                        default: 128
                  fqdn:
                    description:
                      - A fully qualified domain name that specifies its exact location in the
                        tree hierarchy of the Domain Name System.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - The fully qualified domain name of the host.
                        type: str
                        required: false
          aos_details:
            description:
              - AOS installation details for the node
            type: dict
            required: true
            suboptions:
              network_details:
                description:
                  - Networking configuration for AOS including management interface
                type: dict
                required: true
                suboptions:
                  management:
                    description:
                      - Details of the network
                    type: dict
                    required: true
                    suboptions:
                      ip:
                        description:
                          - IP address of the network
                        type: dict
                        required: false
                        suboptions:
                          ipv4:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv4 format.
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
                                  - The prefix length of the network to which this host IPv4
                                    address belongs.
                                type: int
                                required: false
                                default: 32
                          ipv6:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv6 format.
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
                                  - The prefix length of the network to which this host IPv6
                                    address belongs.
                                type: int
                                required: false
                                default: 128
                      gateway:
                        description:
                          - Gateway IP of the network
                        type: dict
                        required: false
                        suboptions:
                          ipv4:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv4 format.
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
                                  - The prefix length of the network to which this host IPv4
                                    address belongs.
                                type: int
                                required: false
                                default: 32
                          ipv6:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv6 format.
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
                                  - The prefix length of the network to which this host IPv6
                                    address belongs.
                                type: int
                                required: false
                                default: 128
                      vlan_id:
                        description:
                          - VLAN ID of the network
                        type: int
                        required: false
              name_servers:
                description:
                  - List of DNS servers for the CVM
                type: list
                elements: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv4 format.
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
                          - The prefix length of the network to which this host IPv4 address
                            belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv6 format.
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
                          - The prefix length of the network to which this host IPv6 address
                            belongs.
                        type: int
                        required: false
                        default: 128
              ntp_servers:
                description:
                  - List of NTP servers for the CVM
                type: list
                elements: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv4 format.
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
                          - The prefix length of the network to which this host IPv4 address
                            belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv6 format.
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
                          - The prefix length of the network to which this host IPv6 address
                            belongs.
                        type: int
                        required: false
                        default: 128
                  fqdn:
                    description:
                      - A fully qualified domain name that specifies its exact location in the
                        tree hierarchy of the Domain Name System.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - The fully qualified domain name of the host.
                        type: str
                        required: false
              aos_image_details:
                description:
                  - Details of the AOS image
                  - Provide C(local_aos_image_details).
                type: dict
                required: true
                suboptions:
                  local_aos_image_details:
                    description:
                      - Details of the AOS image managed by Foundation Central
                    type: dict
                    required: true
                    suboptions:
                      ext_id:
                        description:
                          - External ID of the AOS image managed by Foundation Central
                        type: str
                        required: true
              cvm_memory_gb:
                description:
                  - Memory allocation for the CVM in GB.
                  - This value will be overridden by FC if it does not fall within the range
                    expected by Foundation Central for the given node
                type: int
                required: false
      reconfiguration_details:
        description:
          - Configuration for updating network settings, hostname, DNS, and NTP on nodes with
            existing installations without reimaging
          - Mutually exclusive with C(host_installation_details), C(aos_installation_details),
            and C(hci_imaging_details).
        type: dict
        required: false
        suboptions:
          host_details:
            description:
              - Configuration details for the host layer (hypervisor)
            type: dict
            required: false
            suboptions:
              network_details:
                description:
                  - Network configuration for the host (IP, gateway, VLAN, bond)
                type: dict
                required: false
                suboptions:
                  management:
                    description:
                      - Details of the management network
                    type: dict
                    required: false
                    suboptions:
                      mtu_bytes:
                        description:
                          - Maximum transmission unit of the management network
                        type: int
                        required: false
                      vlan_id:
                        description:
                          - VLAN ID of the network
                        type: int
                        required: false
                      ip:
                        description:
                          - IP address of the network
                        type: dict
                        required: false
                        suboptions:
                          ipv4:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv4 format.
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
                                  - The prefix length of the network to which this host IPv4
                                    address belongs.
                                type: int
                                required: false
                                default: 32
                          ipv6:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv6 format.
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
                                  - The prefix length of the network to which this host IPv6
                                    address belongs.
                                type: int
                                required: false
                                default: 128
                      gateway:
                        description:
                          - Gateway IP of the network
                        type: dict
                        required: false
                        suboptions:
                          ipv4:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv4 format.
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
                                  - The prefix length of the network to which this host IPv4
                                    address belongs.
                                type: int
                                required: false
                                default: 32
                          ipv6:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv6 format.
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
                                  - The prefix length of the network to which this host IPv6
                                    address belongs.
                                type: int
                                required: false
                                default: 128
                      bond_settings:
                        description:
                          - Network bonding configuration.
                          - Choose either Active-Backup bonding for simple failover or LACP bonding
                            for dynamic link aggregation
                        type: dict
                        required: false
                        suboptions:
                          bond_config:
                            description:
                              - Bond configuration type
                              - Provide exactly one of C(active_backup_bond) or C(lacp_bond).
                            type: dict
                            required: false
                            suboptions:
                              active_backup_bond:
                                description:
                                  - Active-Backup bonding configuration where one NIC is active and
                                    others provide failover redundancy
                                  - Mutually exclusive with C(lacp_bond).
                                type: dict
                                required: false
                                suboptions:
                                  nics:
                                    description:
                                      - Details of the NICs
                                    type: dict
                                    required: true
                                    suboptions:
                                      mac_address:
                                        description:
                                          - MAC address of the NIC
                                        type: list
                                        elements: str
                                        required: false
                              lacp_bond:
                                description:
                                  - LACP (Link Aggregation Control Protocol) bonding configuration
                                    for dynamic link aggregation
                                  - Mutually exclusive with C(active_backup_bond).
                                type: dict
                                required: false
                                suboptions:
                                  lacp_settings:
                                    description:
                                      - Details of the LACP settings
                                    type: dict
                                    required: true
                                    suboptions:
                                      rate:
                                        description:
                                          - Rate of the LACP
                                        type: str
                                        required: false
                                        choices:
                                          - SLOW
                                          - FAST
                                  nics:
                                    description:
                                      - Details of the NICs
                                    type: dict
                                    required: true
                                    suboptions:
                                      mac_address:
                                        description:
                                          - MAC address of the NIC
                                        type: list
                                        elements: str
                                        required: false
              name_servers:
                description:
                  - List of nameserver IP addresses to be used by the host
                type: list
                elements: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv4 format.
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
                          - The prefix length of the network to which this host IPv4 address
                            belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv6 format.
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
                          - The prefix length of the network to which this host IPv6 address
                            belongs.
                        type: int
                        required: false
                        default: 128
              ntp_servers:
                description:
                  - List of NTP server IP addresses to be used by the host
                type: list
                elements: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv4 format.
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
                          - The prefix length of the network to which this host IPv4 address
                            belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv6 format.
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
                          - The prefix length of the network to which this host IPv6 address
                            belongs.
                        type: int
                        required: false
                        default: 128
                  fqdn:
                    description:
                      - A fully qualified domain name that specifies its exact location in the
                        tree hierarchy of the Domain Name System.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - The fully qualified domain name of the host.
                        type: str
                        required: false
              hostname:
                description:
                  - Hostname of the hypervisor or host OS
                type: str
                required: false
          cvm_details:
            description:
              - Configuration details for the CVM layer
            type: dict
            required: false
            suboptions:
              network_details:
                description:
                  - Network configuration for the CVM (IP, gateway, VLAN)
                type: dict
                required: false
                suboptions:
                  management:
                    description:
                      - Details of the network
                    type: dict
                    required: true
                    suboptions:
                      ip:
                        description:
                          - IP address of the network
                        type: dict
                        required: false
                        suboptions:
                          ipv4:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv4 format.
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
                                  - The prefix length of the network to which this host IPv4
                                    address belongs.
                                type: int
                                required: false
                                default: 32
                          ipv6:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv6 format.
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
                                  - The prefix length of the network to which this host IPv6
                                    address belongs.
                                type: int
                                required: false
                                default: 128
                      gateway:
                        description:
                          - Gateway IP of the network
                        type: dict
                        required: false
                        suboptions:
                          ipv4:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv4 format.
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
                                  - The prefix length of the network to which this host IPv4
                                    address belongs.
                                type: int
                                required: false
                                default: 32
                          ipv6:
                            description:
                              - An unique address that identifies a device on the internet or a
                                local network in IPv6 format.
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
                                  - The prefix length of the network to which this host IPv6
                                    address belongs.
                                type: int
                                required: false
                                default: 128
                      vlan_id:
                        description:
                          - VLAN ID of the network
                        type: int
                        required: false
              name_servers:
                description:
                  - List of DNS servers for the CVM
                type: list
                elements: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv4 format.
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
                          - The prefix length of the network to which this host IPv4 address
                            belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv6 format.
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
                          - The prefix length of the network to which this host IPv6 address
                            belongs.
                        type: int
                        required: false
                        default: 128
              ntp_servers:
                description:
                  - List of NTP servers for the CVM
                type: list
                elements: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv4 format.
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
                          - The prefix length of the network to which this host IPv4 address
                            belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - An unique address that identifies a device on the internet or a local
                        network in IPv6 format.
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
                          - The prefix length of the network to which this host IPv6 address
                            belongs.
                        type: int
                        required: false
                        default: 128
                  fqdn:
                    description:
                      - A fully qualified domain name that specifies its exact location in the
                        tree hierarchy of the Domain Name System.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - The fully qualified domain name of the host.
                        type: str
                        required: false
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
- name: Image a node using a patched host image
  nutanix.ncp.ntnx_image_node_v2:
    nutanix_host: "10.0.0.1"
    nutanix_username: "admin"
    nutanix_password: "Nutanix.123"
    validate_certs: false
    ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
    configuration:
      host_installation_details:
        patched_image_ext_id: "b2b2b2b2-1111-2222-3333-444455556666"
        patched_image_url: "https://example.com/images/patched.iso"
  register: result

- name: Image a node by installing AOS
  nutanix.ncp.ntnx_image_node_v2:
    nutanix_host: "10.0.0.1"
    nutanix_username: "admin"
    nutanix_password: "Nutanix.123"
    validate_certs: false
    ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
    configuration:
      aos_installation_details:
        network_details:
          management:
            vlan_id: 1
            ip:
              ipv4:
                value: "10.0.0.21"
                prefix_length: 24
            gateway:
              ipv4:
                value: "10.0.0.1"
                prefix_length: 24
        name_servers:
          - ipv4:
              value: "8.8.8.8"
        ntp_servers:
          - fqdn:
              value: "pool.ntp.org"
        aos_image_details:
          local_aos_image_details:
            ext_id: "a3a3a3a3-1111-2222-3333-444455556666"
        cvm_memory_gb: 32
  register: result

- name: Image a node with HCI imaging details
  nutanix.ncp.ntnx_image_node_v2:
    nutanix_host: "10.0.0.1"
    nutanix_username: "admin"
    nutanix_password: "Nutanix.123"
    validate_certs: false
    ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
    configuration:
      hci_imaging_details:
        hypervisor_details:
          hostname: "ahv-host-01"
          image_details:
            local_host_image_details:
              ext_id: "c4c4c4c4-1111-2222-3333-444455556666"
          network_details:
            management:
              mtu_bytes: 1500
              vlan_id: 1
              ip:
                ipv4:
                  value: "10.0.0.11"
                  prefix_length: 24
              gateway:
                ipv4:
                  value: "10.0.0.1"
                  prefix_length: 24
              bond_settings:
                bond_config:
                  active_backup_bond:
                    nics:
                      mac_address:
                        - "aa:bb:cc:dd:ee:01"
          name_servers:
            - ipv4:
                value: "8.8.8.8"
          ntp_servers:
            - fqdn:
                value: "pool.ntp.org"
        aos_details:
          network_details:
            management:
              vlan_id: 1
              ip:
                ipv4:
                  value: "10.0.0.21"
                  prefix_length: 24
              gateway:
                ipv4:
                  value: "10.0.0.1"
                  prefix_length: 24
          aos_image_details:
            local_aos_image_details:
              ext_id: "a3a3a3a3-1111-2222-3333-444455556666"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for imaging a node.
    - If C(wait) is true, it will contain the final task payload after completion.
    - If C(wait) is false, it will contain the initial task details.
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
      "operation": "ImageNode",
      "operation_description": "Image node",
      "status": "SUCCEEDED"
    }

task_ext_id:
  description: The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the node.
  returned: always
  type: str
  sample: "d1a1a1a1-1111-2222-3333-444455556666"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error or in check mode operation
  type: str
  sample: "Node with ext_id:d1a1a1a1-1111-2222-3333-444455556666 will be imaged."

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
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

    fqdn_spec = dict(
        value=dict(type="str", required=False),
    )

    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=lifecycle_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=lifecycle_sdk.IPv6Address,
        ),
    )

    ip_address_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=lifecycle_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=lifecycle_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            required=False,
            obj=lifecycle_sdk.FQDN,
        ),
    )

    network_details_spec = dict(
        ip=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=lifecycle_sdk.IPAddress,
        ),
        gateway=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=lifecycle_sdk.IPAddress,
        ),
        vlan_id=dict(type="int", required=False),
    )

    nics_spec = dict(
        mac_address=dict(type="list", elements="str", required=False),
    )

    lacp_settings_spec = dict(
        rate=dict(type="str", required=False, choices=["SLOW", "FAST"]),
    )

    active_backup_bond_spec = dict(
        nics=dict(
            type="dict",
            options=nics_spec,
            required=True,
            obj=lifecycle_sdk.Nics,
        ),
    )

    lacp_bond_spec = dict(
        lacp_settings=dict(
            type="dict",
            options=lacp_settings_spec,
            required=True,
            obj=lifecycle_sdk.LacpSettings,
        ),
        nics=dict(
            type="dict",
            options=nics_spec,
            required=True,
            obj=lifecycle_sdk.Nics,
        ),
    )

    bond_config_spec = dict(
        active_backup_bond=dict(
            type="dict",
            options=active_backup_bond_spec,
            required=False,
        ),
        lacp_bond=dict(
            type="dict",
            options=lacp_bond_spec,
            required=False,
        ),
    )

    bond_settings_spec = dict(
        bond_config=dict(
            type="dict",
            options=bond_config_spec,
            required=False,
            obj=dict(
                active_backup_bond=lifecycle_sdk.ActiveBackupBond,
                lacp_bond=lifecycle_sdk.LacpBond,
            ),
        ),
    )

    management_network_spec = dict(
        mtu_bytes=dict(type="int", required=False),
        vlan_id=dict(type="int", required=False),
        ip=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=lifecycle_sdk.IPAddress,
        ),
        gateway=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=lifecycle_sdk.IPAddress,
        ),
        bond_settings=dict(
            type="dict",
            options=bond_settings_spec,
            required=False,
            obj=lifecycle_sdk.BondSettings,
        ),
    )

    aos_networking_spec = dict(
        management=dict(
            type="dict",
            options=network_details_spec,
            required=True,
            obj=lifecycle_sdk.NetworkDetails,
        ),
    )

    local_aos_image_details_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    aos_image_details_spec = dict(
        local_aos_image_details=dict(
            type="dict",
            options=local_aos_image_details_spec,
            required=True,
        ),
    )

    aos_installation_details_spec = dict(
        network_details=dict(
            type="dict",
            options=aos_networking_spec,
            required=True,
            obj=lifecycle_sdk.AosNetworking,
        ),
        name_servers=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            required=False,
            obj=lifecycle_sdk.IPAddress,
        ),
        ntp_servers=dict(
            type="list",
            elements="dict",
            options=ip_address_or_fqdn_spec,
            required=False,
            obj=lifecycle_sdk.IPAddressOrFQDN,
        ),
        aos_image_details=dict(
            type="dict",
            options=aos_image_details_spec,
            required=True,
            obj={
                "local_aos_image_details": lifecycle_sdk.LocalAOSImageDetails,
            },
        ),
        cvm_memory_gb=dict(type="int", required=False),
    )

    local_host_image_details_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    hypervisor_image_details_spec = dict(
        local_host_image_details=dict(
            type="dict",
            options=local_host_image_details_spec,
            required=True,
        ),
    )

    hci_hypervisor_networking_spec = dict(
        management=dict(
            type="dict",
            options=management_network_spec,
            required=True,
            obj=lifecycle_sdk.ManagementNetwork,
        ),
    )

    hci_hypervisor_details_spec = dict(
        hostname=dict(type="str", required=True),
        image_details=dict(
            type="dict",
            options=hypervisor_image_details_spec,
            required=True,
            obj={
                "local_host_image_details": lifecycle_sdk.LocalHostImageDetails,
            },
        ),
        network_details=dict(
            type="dict",
            options=hci_hypervisor_networking_spec,
            required=True,
            obj=lifecycle_sdk.HciHypervisorNetworking,
        ),
        name_servers=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            required=False,
            obj=lifecycle_sdk.IPAddress,
        ),
        ntp_servers=dict(
            type="list",
            elements="dict",
            options=ip_address_or_fqdn_spec,
            required=False,
            obj=lifecycle_sdk.IPAddressOrFQDN,
        ),
    )

    hci_imaging_details_spec = dict(
        hypervisor_details=dict(
            type="dict",
            options=hci_hypervisor_details_spec,
            required=True,
            obj=lifecycle_sdk.HciHypervisorDetails,
        ),
        aos_details=dict(
            type="dict",
            options=aos_installation_details_spec,
            required=True,
            obj=lifecycle_sdk.AosInstallationDetails,
        ),
    )

    host_network_details_spec = dict(
        management=dict(
            type="dict",
            options=management_network_spec,
            required=False,
            obj=lifecycle_sdk.ManagementNetwork,
        ),
    )

    host_reconfiguration_details_spec = dict(
        network_details=dict(
            type="dict",
            options=host_network_details_spec,
            required=False,
            obj=lifecycle_sdk.HostNetworkDetails,
        ),
        name_servers=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            required=False,
            obj=lifecycle_sdk.IPAddress,
        ),
        ntp_servers=dict(
            type="list",
            elements="dict",
            options=ip_address_or_fqdn_spec,
            required=False,
            obj=lifecycle_sdk.IPAddressOrFQDN,
        ),
        hostname=dict(type="str", required=False),
    )

    cvm_reconfiguration_details_spec = dict(
        network_details=dict(
            type="dict",
            options=aos_networking_spec,
            required=False,
            obj=lifecycle_sdk.AosNetworking,
        ),
        name_servers=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            required=False,
            obj=lifecycle_sdk.IPAddress,
        ),
        ntp_servers=dict(
            type="list",
            elements="dict",
            options=ip_address_or_fqdn_spec,
            required=False,
            obj=lifecycle_sdk.IPAddressOrFQDN,
        ),
    )

    host_installation_details_spec = dict(
        patched_image_ext_id=dict(type="str", required=True),
        patched_image_url=dict(type="str", required=False),
    )

    reconfiguration_details_spec = dict(
        host_details=dict(
            type="dict",
            options=host_reconfiguration_details_spec,
            required=False,
            obj=lifecycle_sdk.HostReconfigurationDetails,
        ),
        cvm_details=dict(
            type="dict",
            options=cvm_reconfiguration_details_spec,
            required=False,
            obj=lifecycle_sdk.CvmReconfigurationDetails,
        ),
    )

    configuration_spec = dict(
        host_installation_details=dict(
            type="dict",
            options=host_installation_details_spec,
            required=False,
        ),
        aos_installation_details=dict(
            type="dict",
            options=aos_installation_details_spec,
            required=False,
        ),
        hci_imaging_details=dict(
            type="dict",
            options=hci_imaging_details_spec,
            required=False,
        ),
        reconfiguration_details=dict(
            type="dict",
            options=reconfiguration_details_spec,
            required=False,
        ),
    )

    configuration_one_of = (
        "host_installation_details",
        "aos_installation_details",
        "hci_imaging_details",
        "reconfiguration_details",
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        configuration=dict(
            type="dict",
            required=True,
            options=configuration_spec,
            obj={
                "host_installation_details": lifecycle_sdk.HostInstallationDetails,
                "aos_installation_details": lifecycle_sdk.AosInstallationDetails,
                "hci_imaging_details": lifecycle_sdk.HciImagingDetails,
                "reconfiguration_details": lifecycle_sdk.ReconfigurationDetails,
            },
            mutually_exclusive=[configuration_one_of],
            required_one_of=[configuration_one_of],
        ),
    )
    return module_args


def run_action(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["ext_id", "configuration"])

    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.ImageNodeSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for imaging node", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Node with ext_id:{0} will be imaged.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.image_node(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while imaging node with ext_id: {0}".format(
                ext_id
            ),
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
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    api_instance = get_nodes_api_instance(module)
    run_action(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
