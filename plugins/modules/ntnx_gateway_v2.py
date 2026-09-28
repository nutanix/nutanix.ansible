#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_gateway_v2
short_description: Create, Update, Delete, Upgrade network gateways in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, delete and upgrade network gateways in Nutanix Prism Central.
  - A Network Gateway is a VyOS-based VM that connects VPC networks to external or remote networks using VPN, VTEP, or BGP.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Network Gateway) -
      Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin, Project Admin, Super Admin,
      Tenant Admin, VPC Admin
    - >-
      B(Update a Network Gateway) -
      Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin, Project Admin, Super Admin,
      Tenant Admin, VPC Admin
    - >-
      B(Delete a Network Gateway) -
      Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin, Project Admin, Super Admin,
      Tenant Admin, VPC Admin
    - >-
      B(Upgrade a Network Gateway) -
      Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin, Project Admin, Super Admin,
      Tenant Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create gateway.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update gateway.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete gateway.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the gateway.
    type: str
    required: false
  upgrade:
    description:
      - When true and ext_id is provided, upgrades the gateway to the latest supported version.
    type: bool
    required: false
    default: false
  name:
    description:
      - Name of the gateway.
    type: str
    required: false
  description:
    description:
      - Description of the gateway.
    type: str
    required: false
  vpc_reference:
    description:
      - VPC.
    type: str
    required: false
  cloud_network_reference:
    description:
      - Cloud network on which network gateway is deployed.
    type: str
    required: false
  project_ext_id:
    description:
      - UUID of the project that owns this entity.
    type: str
    required: false
  gateway_device_vendor:
    description:
      - Third-party gateway vendor.
    type: str
    required: false
  metadata:
    description:
      - Metadata associated with this resource.
    type: dict
    required: false
    suboptions:
      owner_reference_id:
        description:
          - A globally unique identifier that represents the owner of this resource.
        type: str
        required: false
      owner_user_name:
        description:
          - The userName of the owner of this resource.
        type: str
        required: false
      project_reference_id:
        description:
          - A globally unique identifier that represents the project this resource belongs to.
        type: str
        required: false
      project_name:
        description:
          - The name of the project this resource belongs to.
        type: str
        required: false
      category_ids:
        description:
          - A list of globally unique identifiers that represent all the categories the resource is associated with.
        type: list
        elements: str
        required: false
  deployment:
    description:
      - Network gateway deployment configuration.
    type: dict
    required: false
    suboptions:
      cluster_reference:
        description:
          - Cluster reference used to identify which on-prem cluster to deploy the gateway VM on.
        type: str
        required: false
      vcenter_datastore_name:
        description:
          - vCenter datastore to which the gateway disks and images will be uploaded during deployment.
        type: str
        required: false
      should_synchronize_system_ntp_servers:
        description:
          - Boolean flag indicating which NTP servers are configured on the gateway.
        type: bool
        required: false
      should_synchronize_system_dns_servers:
        description:
          - Boolean flag indicating which DNS servers are configured on the gateway.
        type: bool
        required: false
      ntp_servers:
        description:
          - List of NTP servers configured on the gateway.
        type: list
        elements: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address.
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
              - IPv6 address.
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
              - Fully qualified domain name.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - The fully qualified domain name of the host.
                type: str
                required: false
      dns_servers:
        description:
          - List of DNS servers configured on the gateway.
        type: list
        elements: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address.
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
              - IPv6 address.
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
      management_interface:
        description:
          - Network interface used to deliver network services and for managing the gateway.
        type: dict
        required: false
        suboptions:
          subnet_reference:
            description:
              - Management Subnet extId reference used for deploying Network Gateway.
            type: str
            required: false
          vlan_id:
            description:
              - The on-prem VLAN to deploy the gateway on.
            type: int
            required: false
          mtu:
            description:
              - MTU of management interface.
            type: int
            required: false
          address:
            description:
              - IP address.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address.
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
                  - IPv6 address.
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
          default_gateway:
            description:
              - Default gateway.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address.
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
                  - IPv6 address.
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
      interfaces:
        description:
          - List of network interfaces for this gateway.
        type: list
        elements: dict
        required: false
        suboptions:
          subnet_reference:
            description:
              - The VLAN subnet to deploy this network gateway VM on.
            type: str
            required: false
          mac_address:
            description:
              - MAC address of this gateway interface.
            type: str
            required: false
          mtu:
            description:
              - MTU of this gateway interface.
            type: int
            required: false
          ip_address:
            description:
              - IP address.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address.
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
                  - IPv6 address.
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
          default_gateway_address:
            description:
              - Default gateway address.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address.
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
                  - IPv6 address.
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
  services:
    description:
      - Local or remote gateway service type.
    type: dict
    required: false
    suboptions:
      local_services:
        description:
          - Service configuration for a local gateway.
        type: dict
        required: false
        suboptions:
          service_address:
            description:
              - Service address.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address.
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
                  - IPv6 address.
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
          service_addresses:
            description:
              - List of service addresses.
            type: list
            elements: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address.
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
                  - IPv6 address.
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
          local_vpn_service:
            description:
              - VPN service hosted on this local gateway.
            type: dict
            required: false
            suboptions:
              ebgp_config:
                description:
                  - BGP configuration.
                type: dict
                required: false
                suboptions:
                  asn:
                    description:
                      - Autonomous system number.
                    type: int
                    required: false
                  password:
                    description:
                      - BGP password.
                    type: str
                    required: false
                  should_redistribute_routes:
                    description:
                      - Redistribute routes over eBGP.
                    type: bool
                    required: false
              peer_igp_config:
                description:
                  - Internal routing configuration (Static, OSPF, or iBGP).
                  - Supported only for VLAN-attached gateways; not supported for VPC-attached gateways
                    (use external Static or eBGP instead).
                  - Exactly one of C(ospf_config), C(ibgp_config_list), or C(local_prefix_list) must be specified.
                type: dict
                required: false
                suboptions:
                  ospf_config:
                    description:
                      - OSPF configuration.
                      - Mutually exclusive with C(ibgp_config_list) and C(local_prefix_list).
                    type: dict
                    required: false
                    suboptions:
                      area_id:
                        description:
                          - OSPF area id of this gateway.
                        type: str
                        required: false
                      authentication_type:
                        description:
                          - OSPF authentication type.
                        type: str
                        required: false
                        choices:
                          - PLAIN_TEXT
                          - MD5
                      password:
                        description:
                          - Password for authentication.
                        type: str
                        required: false
                  ibgp_config_list:
                    description:
                      - iBGP configuration.
                      - Mutually exclusive with C(ospf_config) and C(local_prefix_list).
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      peer_ip:
                        description:
                          - IP address of the iBGP peer.
                        type: dict
                        required: false
                      asn:
                        description:
                          - Autonomous system number.
                        type: int
                        required: false
                      password:
                        description:
                          - BGP password.
                        type: str
                        required: false
                      should_redistribute_routes:
                        description:
                          - Redistribute routes over eBGP.
                        type: bool
                        required: false
                  local_prefix_list:
                    description:
                      - Static local prefixes (static internal routing).
                      - Mutually exclusive with C(ospf_config) and C(ibgp_config_list).
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      ipv4:
                        description:
                          - IPv4 subnet.
                        type: dict
                        required: false
                        suboptions:
                          ip:
                            description:
                              - IP address of the subnet.
                            type: dict
                            required: true
                            suboptions:
                              value:
                                description:
                                  - The IPv4 address of the host.
                                type: str
                                required: true
                              prefix_length:
                                description:
                                  - Prefix length of the IPv4 subnet.
                                type: int
                                required: false
                                default: 32
                          prefix_length:
                            description:
                              - The prefix length of the network to which this host IPv4 address belongs.
                            type: int
                            required: true
                      ipv6:
                        description:
                          - IPv6 subnet.
                        type: dict
                        required: false
                        suboptions:
                          ip:
                            description:
                              - IP address of the subnet.
                            type: dict
                            required: true
                            suboptions:
                              value:
                                description:
                                  - The IPv6 address of the host.
                                type: str
                                required: true
                              prefix_length:
                                description:
                                  - Prefix length of the IPv6 subnet.
                                type: int
                                required: false
                                default: 128
                          prefix_length:
                            description:
                              - The prefix length of the network to which this host IPv6 address belongs.
                            type: int
                            required: true
          local_vtep_service:
            description:
              - VTEP service hosted on this local gateway.
            type: dict
            required: false
            suboptions:
              vxlan_port:
                description:
                  - VXLAN port.
                type: int
                required: false
          local_bgp_service:
            description:
              - BGP service hosted on this local gateway.
            type: dict
            required: false
            suboptions:
              vpc_reference:
                description:
                  - Reference to the VPC that this network gateway serves as its BGP speaker.
                type: str
                required: false
              asn:
                description:
                  - Autonomous system number.
                type: int
                required: false
              is_bgp_add_path_enabled:
                description:
                  - If the BGP additional paths capability is enabled on this local gateway.
                type: bool
                required: false
      remote_services:
        description:
          - Service configuration for a remote gateway.
        type: dict
        required: false
        suboptions:
          remote_vpn_service:
            description:
              - VPN service hosted on this remote gateway.
            type: dict
            required: false
            suboptions:
              service_address:
                description:
                  - Service address.
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - IPv4 address.
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
                      - IPv6 address.
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
              should_install_xi_route:
                description:
                  - Boolean flag indicating user opt-in for installing Xi LB route in on-prem Prism Central and Prism Element CVMs.
                type: bool
                required: false
              ebgp_config:
                description:
                  - BGP configuration.
                type: dict
                required: false
                suboptions:
                  asn:
                    description:
                      - Autonomous system number.
                    type: int
                    required: false
                  password:
                    description:
                      - BGP password.
                    type: str
                    required: false
                  should_redistribute_routes:
                    description:
                      - Redistribute routes over eBGP.
                    type: bool
                    required: false
              peer_igp_config:
                description:
                  - Internal routing configuration (Static, OSPF, or iBGP).
                  - Supported only for VLAN-attached gateways; not supported for VPC-attached gateways
                    (use external Static or eBGP instead).
                  - Exactly one of C(ospf_config), C(ibgp_config_list), or C(local_prefix_list) must be specified.
                type: dict
                required: false
                suboptions:
                  ospf_config:
                    description:
                      - OSPF configuration.
                      - Mutually exclusive with C(ibgp_config_list) and C(local_prefix_list).
                    type: dict
                    required: false
                    suboptions:
                      area_id:
                        description:
                          - OSPF area id of this gateway.
                        type: str
                        required: false
                      authentication_type:
                        description:
                          - OSPF authentication type.
                        type: str
                        required: false
                        choices:
                          - PLAIN_TEXT
                          - MD5
                      password:
                        description:
                          - Password for authentication.
                        type: str
                        required: false
                  ibgp_config_list:
                    description:
                      - iBGP configuration.
                      - Mutually exclusive with C(ospf_config) and C(local_prefix_list).
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      peer_ip:
                        description:
                          - IP address of the iBGP peer.
                        type: dict
                        required: false
                      asn:
                        description:
                          - Autonomous system number.
                        type: int
                        required: false
                      password:
                        description:
                          - BGP password.
                        type: str
                        required: false
                      should_redistribute_routes:
                        description:
                          - Redistribute routes over eBGP.
                        type: bool
                        required: false
                  local_prefix_list:
                    description:
                      - Static local prefixes (static internal routing).
                      - Mutually exclusive with C(ospf_config) and C(ibgp_config_list).
                    type: list
                    elements: dict
                    required: false
          remote_vtep_service:
            description:
              - VTEP service hosted on this remote gateway.
            type: dict
            required: false
            suboptions:
              vxlan_port:
                description:
                  - VXLAN port.
                type: int
                required: false
              vteps:
                description:
                  - Remote VXLAN Tunnel Endpoints configuration.
                type: list
                elements: dict
                required: false
                suboptions:
                  address:
                    description:
                      - IP address of the remote VTEP endpoint.
                    type: dict
                    required: false
                    suboptions:
                      ipv4:
                        description:
                          - IPv4 address.
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
                          - IPv6 address.
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
          remote_bgp_service:
            description:
              - BGP service hosted on this remote gateway.
            type: dict
            required: false
            suboptions:
              asn:
                description:
                  - Autonomous system number.
                type: int
                required: false
              address:
                description:
                  - IP address of the remote BGP gateway.
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - IPv4 address.
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
                      - IPv6 address.
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
  high_availability_group:
    description:
      - High availability group configuration.
    type: dict
    required: false
    suboptions:
      is_ha_enabled:
        description:
          - Indicates whether high availability is enabled.
        type: bool
        required: false
      algorithm:
        description:
          - High availability algorithm.
        type: str
        required: false
        choices:
          - ACTIVE_BACKUP
      peered_gateways:
        description:
          - Information about peered gateways in a high availability group.
        type: list
        elements: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External ID of the peered gateway.
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
- name: Create a local VTEP gateway
  nutanix.ncp.ntnx_gateway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "gw_local_vtep_ansible"
    description: "Local VTEP gateway created by Ansible"
    gateway_device_vendor: "GENERIC"
    vpc_reference: "d1111111-1111-1111-1111-111111111111"
    project_ext_id: "00000000-0000-0000-0000-000000000000"
    metadata:
      owner_reference_id: "a7777777-7777-7777-7777-777777777777"
      owner_user_name: "admin"
      project_reference_id: "00000000-0000-0000-0000-000000000000"
      project_name: "default"
    deployment:
      cluster_reference: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
      should_synchronize_system_ntp_servers: false
      should_synchronize_system_dns_servers: false
      ntp_servers:
        - fqdn:
            value: "pool.ntp.org"
        - ipv4:
            value: "10.40.64.16"
            prefix_length: 32
      dns_servers:
        - ipv4:
            value: "8.8.8.8"
            prefix_length: 32
      management_interface:
        subnet_reference: "c3333333-3333-3333-3333-333333333333"
        default_gateway:
          ipv4:
            value: "192.168.50.1"
            prefix_length: 32
      interfaces:
        - subnet_reference: "c3333333-3333-3333-3333-333333333333"
          default_gateway_address:
            ipv4:
              value: "192.168.50.1"
              prefix_length: 32
    services:
      local_services:
        service_address:
          ipv4:
            value: "10.44.3.231"
            prefix_length: 32
        service_addresses:
          - ipv4:
              value: "10.44.3.231"
              prefix_length: 32
        local_vtep_service:
          vxlan_port: 4789
  register: result

- name: Update gateway name and description
  nutanix.ncp.ntnx_gateway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "gw_local_vtep_ansible_updated"
    description: "Updated description for gateway with all attributes"
  register: result

- name: Upgrade an existing gateway to the latest supported version
  nutanix.ncp.ntnx_gateway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    upgrade: true
  register: result

- name: Delete a gateway
  nutanix.ncp.ntnx_gateway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, upgrading or deleting a network gateway.
    - If the operation is create or update and C(wait) is true, it will return the gateway details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete or upgrade, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "cloud_network_reference": null,
      "deployment": {
          "cluster_reference": "00065c06-b7be-0e44-784a-7cc25505d491",
          "dns_servers": [
              {
                  "ipv4": {
                      "prefix_length": 32,
                      "value": "8.8.8.8"
                  },
                  "ipv6": null
              }
          ],
          "interfaces": [
              {
                  "default_gateway_address": {
                      "ipv4": {
                          "prefix_length": 32,
                          "value": "192.168.50.1"
                      },
                      "ipv6": null
                  },
                  "ip_address": {
                      "ipv4": {
                          "prefix_length": 32,
                          "value": "192.168.50.52"
                      },
                      "ipv6": null
                  },
                  "mac_address": "50:6b:8d:37:00:6e",
                  "mtu": null,
                  "subnet_reference": "5a5c6abd-b6c5-4e53-b856-fd1da8b39178"
              }
          ],
          "management_interface": {
              "address": {
                  "ipv4": {
                      "prefix_length": 32,
                      "value": "192.168.50.52"
                  },
                  "ipv6": null
              },
              "default_gateway": {
                  "ipv4": {
                      "prefix_length": 32,
                      "value": "192.168.50.1"
                  },
                  "ipv6": null
              },
              "mtu": null,
              "subnet_reference": "5a5c6abd-b6c5-4e53-b856-fd1da8b39178",
              "vlan_id": null
          },
          "ntp_servers": [
              {
                  "fqdn": {
                      "value": "pool.ntp.org"
                  },
                  "ipv4": null,
                  "ipv6": null
              },
              {
                  "fqdn": null,
                  "ipv4": {
                      "prefix_length": 32,
                      "value": "10.40.64.16"
                  },
                  "ipv6": null
              }
          ],
          "should_synchronize_system_dns_servers": false,
          "should_synchronize_system_ntp_servers": false,
          "vcenter_datastore_name": null
      },
      "description": "Gateway created by Ansible integration tests with all attributes",
      "ext_id": "452f36ad-1850-4a12-a7aa-dd41d0b8abd5",
      "gateway_device_vendor": "GENERIC",
      "high_availability_group": null,
      "installed_software_version": null,
      "is_active": true,
      "links": null,
      "metadata": {
          "category_ids": null,
          "owner_reference_id": "cddbe7e2-a8e2-539d-a763-a61380e4bc61",
          "owner_user_name": "admin",
          "project_name": "_internal",
          "project_reference_id": "00000000-0000-0000-0000-000000000000"
      },
      "name": "gw_ansible_lPRuVhwcmNRE_all",
      "project_ext_id": "00000000-0000-0000-0000-000000000000",
      "services": {
          "local_bgp_service": null,
          "local_vpn_service": null,
          "local_vtep_service": {
              "vxlan_port": 4789
          },
          "service_address": {
              "ipv4": {
                  "prefix_length": 32,
                  "value": "10.44.3.237"
              },
              "ipv6": null
          },
          "service_addresses": [
              {
                  "ipv4": {
                      "prefix_length": 32,
                      "value": "10.44.3.237"
                  },
                  "ipv6": null
              }
          ]
      },
      "status": null,
      "supported_software_version": null,
      "tenant_id": null,
      "vm": null,
      "vm_reference": "af438984-bbcf-4e25-b0a6-c43023cdd9bf",
      "vpc": null,
      "vpc_reference": "797ecc5a-e2c5-41f2-a6e9-310bc05d71b1"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:3c42282a-3dbe-4026-8469-fe8c145ad1e4"

ext_id:
  description:
    - The external ID of the gateway.
  returned: always
  type: str
  sample: "c13bf194-4017-4efb-abbf-d44c837818a9"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: always
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating gateway"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_gateways_api_instance,
)
from ..module_utils.v4.network.helpers import get_gateway  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


READ_ONLY_FIELDS = (
    "installed_software_version",
    "supported_software_version",
    "status",
    "vpc",
    "vm",
    "links",
    "ext_id",
    "tenant_id",
)


def _get_ipv4_address_spec():
    return dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )


def _get_ipv6_address_spec():
    return dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )


def _get_ip_address_spec():
    return dict(
        ipv4=dict(
            type="dict",
            options=_get_ipv4_address_spec(),
            required=False,
            obj=networking_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=_get_ipv6_address_spec(),
            required=False,
            obj=networking_sdk.IPv6Address,
        ),
    )


def _get_ip_address_or_fqdn_spec():
    spec = _get_ip_address_spec()
    spec["fqdn"] = dict(
        type="dict",
        options=dict(value=dict(type="str", required=False)),
        required=False,
        obj=networking_sdk.FQDN,
    )
    return spec


def _get_management_interface_spec():
    return dict(
        subnet_reference=dict(type="str", required=False),
        vlan_id=dict(type="int", required=False),
        mtu=dict(type="int", required=False),
        address=dict(
            type="dict",
            options=_get_ip_address_spec(),
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        default_gateway=dict(
            type="dict",
            options=_get_ip_address_spec(),
            required=False,
            obj=networking_sdk.IPAddress,
        ),
    )


def _get_gateway_interface_spec():
    return dict(
        subnet_reference=dict(type="str", required=False),
        mac_address=dict(type="str", required=False),
        mtu=dict(type="int", required=False),
        ip_address=dict(
            type="dict",
            options=_get_ip_address_spec(),
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        default_gateway_address=dict(
            type="dict",
            options=_get_ip_address_spec(),
            required=False,
            obj=networking_sdk.IPAddress,
        ),
    )


def _get_deployment_spec():
    return dict(
        cluster_reference=dict(type="str", required=False),
        vcenter_datastore_name=dict(type="str", required=False),
        should_synchronize_system_ntp_servers=dict(type="bool", required=False),
        should_synchronize_system_dns_servers=dict(type="bool", required=False),
        ntp_servers=dict(
            type="list",
            elements="dict",
            required=False,
            options=_get_ip_address_or_fqdn_spec(),
            obj=networking_sdk.IPAddressOrFQDN,
        ),
        dns_servers=dict(
            type="list",
            elements="dict",
            required=False,
            options=_get_ip_address_spec(),
            obj=networking_sdk.IPAddress,
        ),
        management_interface=dict(
            type="dict",
            options=_get_management_interface_spec(),
            required=False,
            obj=networking_sdk.GatewayManagementInterface,
        ),
        interfaces=dict(
            type="list",
            elements="dict",
            required=False,
            options=_get_gateway_interface_spec(),
            obj=networking_sdk.GatewayInterface,
        ),
    )


def _get_bgp_config_spec():
    return dict(
        asn=dict(type="int", required=False),
        password=dict(type="str", required=False, no_log=True),
        should_redistribute_routes=dict(type="bool", required=False),
    )


def _get_ip_subnet_spec():
    return dict(
        ipv4=dict(
            type="dict",
            required=False,
            obj=networking_sdk.IPv4Subnet,
            options=dict(
                ip=dict(
                    type="dict",
                    required=True,
                    options=_get_ipv4_address_spec(),
                    obj=networking_sdk.IPv4Address,
                ),
                prefix_length=dict(type="int", required=True),
            ),
        ),
        ipv6=dict(
            type="dict",
            required=False,
            obj=networking_sdk.IPv6Subnet,
            options=dict(
                ip=dict(
                    type="dict",
                    required=True,
                    options=_get_ipv6_address_spec(),
                    obj=networking_sdk.IPv6Address,
                ),
                prefix_length=dict(type="int", required=True),
            ),
        ),
    )


def _get_ospf_config_spec():
    return dict(
        area_id=dict(type="str", required=False),
        authentication_type=dict(
            type="str",
            required=False,
            choices=["PLAIN_TEXT", "MD5"],
            obj=networking_sdk.AuthenticationType,
        ),
        password=dict(type="str", required=False, no_log=True),
    )


def _get_ibgp_config_spec():
    spec = _get_bgp_config_spec()
    spec["peer_ip"] = dict(
        type="dict",
        required=False,
        options=_get_ip_address_spec(),
        obj=networking_sdk.IPAddress,
    )
    return spec


def _get_peer_igp_config_spec():
    return dict(
        ospf_config=dict(
            type="dict",
            required=False,
            options=_get_ospf_config_spec(),
            obj=networking_sdk.OspfConfig,
        ),
        ibgp_config_list=dict(
            type="list",
            elements="dict",
            required=False,
            options=_get_ibgp_config_spec(),
            obj=networking_sdk.IbgpConfig,
        ),
        local_prefix_list=dict(
            type="list",
            elements="dict",
            required=False,
            options=_get_ip_subnet_spec(),
            obj=networking_sdk.IPSubnet,
        ),
    )


def _get_local_services_spec():
    return dict(
        service_address=dict(
            type="dict",
            options=_get_ip_address_spec(),
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        service_addresses=dict(
            type="list",
            elements="dict",
            required=False,
            options=_get_ip_address_spec(),
            obj=networking_sdk.IPAddress,
        ),
        local_vpn_service=dict(
            type="dict",
            required=False,
            options=dict(
                ebgp_config=dict(
                    type="dict",
                    options=_get_bgp_config_spec(),
                    required=False,
                    obj=networking_sdk.BgpConfig,
                ),
                peer_igp_config=dict(
                    type="dict",
                    options=_get_peer_igp_config_spec(),
                    required=False,
                    mutually_exclusive=[
                        ("ospf_config", "ibgp_config_list", "local_prefix_list"),
                    ],
                    obj=networking_sdk.InternalRoutingConfig,
                ),
            ),
            obj=networking_sdk.LocalVpnService,
        ),
        local_vtep_service=dict(
            type="dict",
            required=False,
            options=dict(
                vxlan_port=dict(type="int", required=False),
            ),
            obj=networking_sdk.LocalVtepService,
        ),
        local_bgp_service=dict(
            type="dict",
            required=False,
            options=dict(
                vpc_reference=dict(type="str", required=False),
                asn=dict(type="int", required=False),
                is_bgp_add_path_enabled=dict(type="bool", required=False),
            ),
            obj=networking_sdk.LocalBgpService,
        ),
    )


def _get_remote_services_spec():
    return dict(
        remote_vpn_service=dict(
            type="dict",
            required=False,
            options=dict(
                service_address=dict(
                    type="dict",
                    options=_get_ip_address_spec(),
                    required=False,
                    obj=networking_sdk.IPAddress,
                ),
                should_install_xi_route=dict(type="bool", required=False),
                ebgp_config=dict(
                    type="dict",
                    options=_get_bgp_config_spec(),
                    required=False,
                    obj=networking_sdk.BgpConfig,
                ),
                peer_igp_config=dict(
                    type="dict",
                    options=_get_peer_igp_config_spec(),
                    required=False,
                    mutually_exclusive=[
                        ("ospf_config", "ibgp_config_list", "local_prefix_list"),
                    ],
                    obj=networking_sdk.InternalRoutingConfig,
                ),
            ),
            obj=networking_sdk.RemoteVpnService,
        ),
        remote_vtep_service=dict(
            type="dict",
            required=False,
            options=dict(
                vxlan_port=dict(type="int", required=False),
                vteps=dict(
                    type="list",
                    elements="dict",
                    required=False,
                    options=dict(
                        address=dict(
                            type="dict",
                            options=_get_ip_address_spec(),
                            required=False,
                            obj=networking_sdk.IPAddress,
                        ),
                    ),
                    obj=networking_sdk.Vtep,
                ),
            ),
            obj=networking_sdk.RemoteVtepService,
        ),
        remote_bgp_service=dict(
            type="dict",
            required=False,
            options=dict(
                asn=dict(type="int", required=False),
                address=dict(
                    type="dict",
                    options=_get_ip_address_spec(),
                    required=False,
                    obj=networking_sdk.IPAddress,
                ),
            ),
            obj=networking_sdk.RemoteBgpService,
        ),
    )


def _get_services_spec():
    # SpecGenerator resolves the Gatewayservices OneOf via dynamic ``obj`` on
    # the parent ``services`` argument (local_services / remote_services).
    return dict(
        local_services=dict(
            type="dict",
            options=_get_local_services_spec(),
            required=False,
        ),
        remote_services=dict(
            type="dict",
            options=_get_remote_services_spec(),
            required=False,
        ),
    )


def _get_ha_group_spec():
    return dict(
        is_ha_enabled=dict(type="bool", required=False),
        algorithm=dict(
            type="str",
            required=False,
            choices=["ACTIVE_BACKUP"],
            obj=networking_sdk.HighAvailabilityAlgorithm,
        ),
        peered_gateways=dict(
            type="list",
            elements="dict",
            required=False,
            options=dict(
                ext_id=dict(type="str", required=False),
            ),
            obj=networking_sdk.PeeredGateway,
        ),
    )


def get_module_spec():
    # maps of spec classes for attributes having more than one type of objects allowed as it value
    services_allowed_objs = {
        "local_services": networking_sdk.LocalNetworkServices,
        "remote_services": networking_sdk.RemoteNetworkServices,
    }

    module_args = dict(
        ext_id=dict(type="str"),
        upgrade=dict(type="bool", default=False),
        name=dict(type="str"),
        description=dict(type="str"),
        vpc_reference=dict(type="str"),
        cloud_network_reference=dict(type="str"),
        project_ext_id=dict(type="str"),
        gateway_device_vendor=dict(type="str"),
        metadata=dict(
            type="dict",
            options=dict(
                owner_reference_id=dict(type="str"),
                owner_user_name=dict(type="str"),
                project_reference_id=dict(type="str"),
                project_name=dict(type="str"),
                category_ids=dict(type="list", elements="str"),
            ),
            obj=networking_sdk.Metadata,
        ),
        deployment=dict(
            type="dict",
            options=_get_deployment_spec(),
            obj=networking_sdk.GatewayDeployment,
        ),
        services=dict(
            type="dict",
            options=_get_services_spec(),
            obj=services_allowed_objs,
            mutually_exclusive=[("local_services", "remote_services")],
        ),
        high_availability_group=dict(
            type="dict",
            options=_get_ha_group_spec(),
            obj=networking_sdk.HighAvailabilityGroup,
        ),
    )
    return module_args


def create_Gateway(module, api_instance, result):
    validate_required_params(module, ["name"])
    sg = SpecGenerator(module)
    default_spec = networking_sdk.Gateway()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create gateway spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_gateway(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating gateway",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_resp, rel=TASK_CONSTANTS.RelEntityType.GATEWAY
        )
        if ext_id:
            result["ext_id"] = ext_id
            gw_resp = get_gateway(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(gw_resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Gateway"
                ),
                msg="Failed to get entity ext_id from task for Gateway",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old = deepcopy(old_spec_dict)
    new = deepcopy(update_spec_dict)
    strip_internal_attributes(old)
    strip_internal_attributes(new)
    for field in READ_ONLY_FIELDS:
        old.pop(field, None)
        new.pop(field, None)
    return old == new


def update_Gateway(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_gateway(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for updating gateway", **result)
    kwargs = {"if_match": etag}

    # Clear existing OneOf services so SpecGenerator instantiates the correct
    # LocalNetworkServices / RemoteNetworkServices type from module params.
    update_base = deepcopy(old_spec)
    if module.params.get("services"):
        update_base.services = None

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=update_base)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update gateway spec", **result)

    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = None
    try:
        resp = api_instance.update_gateway_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating gateway",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        gw_resp = get_gateway(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(gw_resp.to_dict())
    result["changed"] = True


def upgrade_Gateway(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Gateway with ext_id:{0} will be upgraded.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.upgrade_gateway_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while upgrading gateway",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_resp = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_resp.to_dict())
    result["changed"] = True


def delete_Gateway(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Gateway with ext_id:{0} will be deleted.".format(ext_id)
        return

    old_spec = get_gateway(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.delete_gateway_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting gateway",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
        ],
        mutually_exclusive=[
            ("vpc_reference", "cloud_network_reference"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_gateways_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("upgrade"):
            if not module.params.get("ext_id"):
                module.fail_json(msg="ext_id is required when upgrade=true", **result)
            upgrade_Gateway(module, api_instance, result)
        elif module.params.get("ext_id"):
            update_Gateway(module, api_instance, result)
        else:
            create_Gateway(module, api_instance, result)
    else:
        delete_Gateway(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
