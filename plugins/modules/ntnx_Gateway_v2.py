#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_Gateway_v2
short_description: Create, Update, Delete network gateways in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to create, update, and delete network gateways in Nutanix Prism Central.
  - A network gateway is a virtual appliance that provides north-south connectivity
    services (VPN, VTEP, BGP, Layer 2 stretch) between on-prem and remote sites for
    Nutanix VPC networking.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a network gateway) -
      Required Roles: Prism Admin, Super Admin, VPC Admin
    - >-
      B(Update a network gateway) -
      Required Roles: Prism Admin, Super Admin, VPC Admin
    - >-
      B(Delete a network gateway) -
      Required Roles: Prism Admin, Super Admin, VPC Admin
    - >-
      Prerequisite - When deploying a local gateway on-prem, the referenced management
      subnet, VPC (optional), and cluster must already exist. Remote gateways only
      require identifying network service parameters.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create network gateway.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update network gateway.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete network gateway.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the network gateway.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the network gateway.
      - Required for create operation.
    type: str
    required: false
  description:
    description:
      - Description of the network gateway.
    type: str
    required: false
  vpc_reference:
    description:
      - Reference to the VPC associated with the network gateway (only for local
        gateway deployments that must be attached to a specific VPC).
    type: str
    required: false
  cloud_network_reference:
    description:
      - Reference to the cloud network associated with the network gateway (used for
        cloud-hosted gateways).
    type: str
    required: false
  gateway_device_vendor:
    description:
      - The vendor of the gateway device.
    type: str
    required: false
  project_ext_id:
    description:
      - External ID of the project to which this network gateway belongs.
    type: str
    required: false
  deployment:
    description:
      - Network gateway deployment configuration used when deploying a local network
        gateway VM on-premise.
    type: dict
    required: false
    suboptions:
      cluster_reference:
        description:
          - Cluster reference required to identify which on-prem cluster to deploy the gateway VM on.
        type: str
        required: false
      management_interface:
        description:
          - Management interface used to deliver network services and manage the gateway.
        type: dict
        required: false
        suboptions:
          subnet_reference:
            description:
              - The on-prem VLAN subnet to deploy the network gateway VM on.
            type: str
            required: false
          vlan_id:
            description:
              - VLAN identifier for the management interface (when a VLAN network
                without IPAM is used).
            type: int
            required: false
          address:
            description:
              - Address of the management interface.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
              ipv6:
                description:
                  - IPv6 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
          default_gateway:
            description:
              - Default gateway of the management interface's subnet.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
              ipv6:
                description:
                  - IPv6 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
          mtu:
            description:
              - MTU value for the management interface.
            type: int
            required: false
      interfaces:
        description:
          - List of network interfaces used to deliver network services.
        type: list
        elements: dict
        required: false
        suboptions:
          subnet_reference:
            description:
              - The VLAN subnet to deploy this network gateway VM on.
            type: str
            required: false
          ip_address:
            description:
              - IP address to assign to this interface.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
              ipv6:
                description:
                  - IPv6 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
          default_gateway_address:
            description:
              - Default gateway address for the interface subnet.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
              ipv6:
                description:
                  - IPv6 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
          mac_address:
            description:
              - MAC address of the interface.
            type: str
            required: false
          mtu:
            description:
              - MTU value for the interface.
            type: int
            required: false
      vcenter_datastore_name:
        description:
          - Name of the vCenter datastore where the gateway VM will be deployed
            (only for ESXi-based deployments).
        type: str
        required: false
      should_synchronize_system_ntp_servers:
        description:
          - Whether the gateway VM should synchronize its NTP configuration with
            the parent Nutanix cluster's NTP settings.
        type: bool
        required: false
      ntp_servers:
        description:
          - List of NTP servers to configure on the gateway VM (used when
            C(should_synchronize_system_ntp_servers) is false).
        type: list
        elements: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address of the NTP server.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the network.
                type: int
                required: false
          ipv6:
            description:
              - IPv6 address of the NTP server.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - The IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the network.
                type: int
                required: false
          fqdn:
            description:
              - Fully qualified domain name of the NTP server.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - The FQDN value.
                type: str
                required: true
      should_synchronize_system_dns_servers:
        description:
          - Whether the gateway VM should synchronize its DNS configuration with
            the parent Nutanix cluster's DNS settings.
        type: bool
        required: false
      dns_servers:
        description:
          - List of DNS servers to configure on the gateway VM (used when
            C(should_synchronize_system_dns_servers) is false).
        type: list
        elements: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address of the DNS server.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the network.
                type: int
                required: false
          ipv6:
            description:
              - IPv6 address of the DNS server.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - The IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the network.
                type: int
                required: false
  services:
    description:
      - Services provided by the gateway.
      - Exactly one of C(local_network_services) or C(remote_network_services) must be
        provided per gateway (mutually exclusive).
    type: dict
    required: false
    suboptions:
      local_network_services:
        description:
          - Services of this local gateway.
        type: dict
        required: false
        suboptions:
          service_address:
            description:
              - Primary service address of the local gateway.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
              ipv6:
                description:
                  - IPv6 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
          service_addresses:
            description:
              - Additional service addresses of the local gateway.
            type: list
            elements: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
              ipv6:
                description:
                  - IPv6 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the network.
                    type: int
                    required: false
          local_vpn_service:
            description:
              - VPN service hosted on this local gateway.
            type: dict
            required: false
            suboptions:
              ebgp_config:
                description:
                  - eBGP configuration for the VPN.
                type: dict
                required: false
                suboptions:
                  asn:
                    description:
                      - ASN of the eBGP session.
                    type: int
                    required: false
                  password:
                    description:
                      - eBGP session password.
                    type: str
                    required: false
                  should_redistribute_routes:
                    description:
                      - Whether to redistribute routes learned by this peer.
                    type: bool
                    required: false
              peer_igp_config:
                description:
                  - Internal routing configuration used for peering.
                type: dict
                required: false
                suboptions:
                  ospf_config:
                    description:
                      - OSPF configuration.
                    type: dict
                    required: false
                    suboptions:
                      area_id:
                        description:
                          - OSPF area identifier.
                        type: str
                        required: false
                      authentication_type:
                        description:
                          - Authentication mechanism for OSPF.
                        type: str
                        required: false
                        choices:
                          - MD5
                          - PLAIN_TEXT
                      password:
                        description:
                          - OSPF authentication password.
                        type: str
                        required: false
                  ibgp_config_list:
                    description:
                      - List of iBGP peers for internal routing.
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      peer_ip:
                        description:
                          - IP address of the iBGP peer.
                        type: dict
                        required: false
                        suboptions:
                          ipv4:
                            description:
                              - IPv4 address specification.
                            type: dict
                            required: false
                            suboptions:
                              value:
                                description:
                                  - The IPv4 address value.
                                type: str
                                required: true
                              prefix_length:
                                description:
                                  - Prefix length of the network.
                                type: int
                                required: false
                          ipv6:
                            description:
                              - IPv6 address specification.
                            type: dict
                            required: false
                            suboptions:
                              value:
                                description:
                                  - The IPv6 address value.
                                type: str
                                required: true
                              prefix_length:
                                description:
                                  - Prefix length of the network.
                                type: int
                                required: false
                      asn:
                        description:
                          - ASN of the iBGP peer.
                        type: int
                        required: false
                      password:
                        description:
                          - iBGP session password.
                        type: str
                        required: false
                      should_redistribute_routes:
                        description:
                          - Whether to redistribute routes learned by this peer.
                        type: bool
                        required: false
                  local_prefix_list:
                    description:
                      - Local prefixes to advertise (IPv4/IPv6).
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      ipv4:
                        description:
                          - IPv4 subnet specification.
                        type: dict
                        required: false
                        suboptions:
                          ip:
                            description:
                              - IPv4 address value.
                            type: dict
                            required: true
                            suboptions:
                              value:
                                description:
                                  - IPv4 value.
                                type: str
                                required: true
                              prefix_length:
                                description:
                                  - Prefix length of the network.
                                type: int
                                required: false
                          prefix_length:
                            description:
                              - Prefix length of the IPv4 subnet.
                            type: int
                            required: true
                      ipv6:
                        description:
                          - IPv6 subnet specification.
                        type: dict
                        required: false
                        suboptions:
                          ip:
                            description:
                              - IPv6 address value.
                            type: dict
                            required: true
                            suboptions:
                              value:
                                description:
                                  - IPv6 value.
                                type: str
                                required: true
                              prefix_length:
                                description:
                                  - Prefix length of the network.
                                type: int
                                required: false
                          prefix_length:
                            description:
                              - Prefix length of the IPv6 subnet.
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
                  - VXLAN port to use for the VTEP tunnel.
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
                  - ASN of the local BGP service.
                type: int
                required: false
              is_bgp_add_path_enabled:
                description:
                  - Whether BGP ADD-PATH is enabled.
                type: bool
                required: false
      remote_network_services:
        description:
          - Services of this remote gateway.
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
                  - Primary service address of the remote gateway.
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - IPv4 address specification.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - The IPv4 address value.
                        type: str
                        required: true
                      prefix_length:
                        description:
                          - Prefix length of the network.
                        type: int
                        required: false
                  ipv6:
                    description:
                      - IPv6 address specification.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - The IPv6 address value.
                        type: str
                        required: true
                      prefix_length:
                        description:
                          - Prefix length of the network.
                        type: int
                        required: false
              ebgp_config:
                description:
                  - eBGP configuration for the remote VPN.
                type: dict
                required: false
                suboptions:
                  asn:
                    description:
                      - ASN of the eBGP session.
                    type: int
                    required: false
                  password:
                    description:
                      - eBGP session password.
                    type: str
                    required: false
                  should_redistribute_routes:
                    description:
                      - Whether to redistribute routes learned by this peer.
                    type: bool
                    required: false
              peer_igp_config:
                description:
                  - Internal routing configuration used for peering.
                type: dict
                required: false
                suboptions:
                  ospf_config:
                    description:
                      - OSPF configuration.
                    type: dict
                    required: false
                    suboptions:
                      area_id:
                        description:
                          - OSPF area identifier.
                        type: str
                        required: false
                      authentication_type:
                        description:
                          - Authentication mechanism for OSPF.
                        type: str
                        required: false
                        choices:
                          - MD5
                          - PLAIN_TEXT
                      password:
                        description:
                          - OSPF authentication password.
                        type: str
                        required: false
                  ibgp_config_list:
                    description:
                      - List of iBGP peers for internal routing.
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      peer_ip:
                        description:
                          - IP address of the iBGP peer.
                        type: dict
                        required: false
                        suboptions:
                          ipv4:
                            description:
                              - IPv4 address specification.
                            type: dict
                            required: false
                            suboptions:
                              value:
                                description:
                                  - The IPv4 address value.
                                type: str
                                required: true
                              prefix_length:
                                description:
                                  - Prefix length of the network.
                                type: int
                                required: false
                          ipv6:
                            description:
                              - IPv6 address specification.
                            type: dict
                            required: false
                            suboptions:
                              value:
                                description:
                                  - The IPv6 address value.
                                type: str
                                required: true
                              prefix_length:
                                description:
                                  - Prefix length of the network.
                                type: int
                                required: false
                      asn:
                        description:
                          - ASN of the iBGP peer.
                        type: int
                        required: false
                      password:
                        description:
                          - iBGP session password.
                        type: str
                        required: false
                      should_redistribute_routes:
                        description:
                          - Whether to redistribute routes learned by this peer.
                        type: bool
                        required: false
                  local_prefix_list:
                    description:
                      - Local prefixes to advertise (IPv4/IPv6).
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      ipv4:
                        description:
                          - IPv4 subnet specification.
                        type: dict
                        required: false
                        suboptions:
                          ip:
                            description:
                              - IPv4 address value.
                            type: dict
                            required: true
                            suboptions:
                              value:
                                description:
                                  - IPv4 value.
                                type: str
                                required: true
                              prefix_length:
                                description:
                                  - Prefix length of the network.
                                type: int
                                required: false
                          prefix_length:
                            description:
                              - Prefix length of the IPv4 subnet.
                            type: int
                            required: true
                      ipv6:
                        description:
                          - IPv6 subnet specification.
                        type: dict
                        required: false
                        suboptions:
                          ip:
                            description:
                              - IPv6 address value.
                            type: dict
                            required: true
                            suboptions:
                              value:
                                description:
                                  - IPv6 value.
                                type: str
                                required: true
                              prefix_length:
                                description:
                                  - Prefix length of the network.
                                type: int
                                required: false
                          prefix_length:
                            description:
                              - Prefix length of the IPv6 subnet.
                            type: int
                            required: true
              should_install_xi_route:
                description:
                  - Whether to install the Xi route.
                type: bool
                required: false
          remote_vtep_service:
            description:
              - VTEP service hosted on this remote gateway.
            type: dict
            required: false
            suboptions:
              vxlan_port:
                description:
                  - VXLAN port to use for the VTEP tunnel.
                type: int
                required: false
              vteps:
                description:
                  - VTEP endpoint addresses.
                type: list
                elements: dict
                required: false
                suboptions:
                  address:
                    description:
                      - IP address of the VTEP endpoint.
                    type: dict
                    required: false
                    suboptions:
                      ipv4:
                        description:
                          - IPv4 address specification.
                        type: dict
                        required: false
                        suboptions:
                          value:
                            description:
                              - The IPv4 address value.
                            type: str
                            required: true
                          prefix_length:
                            description:
                              - Prefix length of the network.
                            type: int
                            required: false
                      ipv6:
                        description:
                          - IPv6 address specification.
                        type: dict
                        required: false
                        suboptions:
                          value:
                            description:
                              - The IPv6 address value.
                            type: str
                            required: true
                          prefix_length:
                            description:
                              - Prefix length of the network.
                            type: int
                            required: false
          remote_bgp_service:
            description:
              - BGP service hosted on this remote gateway.
            type: dict
            required: false
            suboptions:
              address:
                description:
                  - Address of the remote BGP service.
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - IPv4 address specification.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - The IPv4 address value.
                        type: str
                        required: true
                      prefix_length:
                        description:
                          - Prefix length of the network.
                        type: int
                        required: false
                  ipv6:
                    description:
                      - IPv6 address specification.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - The IPv6 address value.
                        type: str
                        required: true
                      prefix_length:
                        description:
                          - Prefix length of the network.
                        type: int
                        required: false
              asn:
                description:
                  - ASN of the remote BGP service.
                type: int
                required: false
  high_availability_group:
    description:
      - High availability configuration for the network gateway.
    type: dict
    required: false
    suboptions:
      is_ha_enabled:
        description:
          - Whether high availability is enabled.
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
          - List of peered gateways participating in the HA group.
        type: list
        elements: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External ID of the peered gateway.
            type: str
            required: true
  metadata:
    description:
      - Metadata associated with the resource.
    type: dict
    required: false
    suboptions:
      owner_reference_id:
        description:
          - Globally unique identifier of the owner of this resource.
        type: str
        required: false
      owner_user_name:
        description:
          - User name of the owner.
        type: str
        required: false
      project_reference_id:
        description:
          - Reference to the project.
        type: str
        required: false
      project_name:
        description:
          - Name of the project.
        type: str
        required: false
      category_ids:
        description:
          - List of category IDs.
        type: list
        elements: str
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create a local network gateway (BGP)
  nutanix.ncp.ntnx_Gateway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "local_gateway_ansible"
    description: "Local BGP gateway created by Ansible"
    vpc_reference: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    deployment:
      cluster_reference: "9a5a3f5a-1234-4d2b-b179-298db969c20d"
      management_interface:
        subnet_reference: "1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p"
        address:
          ipv4:
            value: "10.0.0.10"
            prefix_length: 24
        default_gateway:
          ipv4:
            value: "10.0.0.1"
            prefix_length: 24
        mtu: 1500
    services:
      local_network_services:
        local_bgp_service:
          vpc_reference: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
          asn: 65001
          is_bgp_add_path_enabled: false
  register: result
  ignore_errors: true

- name: Create a remote network gateway (VPN)
  nutanix.ncp.ntnx_Gateway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "remote_gateway_ansible"
    description: "Remote VPN gateway created by Ansible"
    services:
      remote_network_services:
        remote_vpn_service:
          service_address:
            ipv4:
              value: "203.0.113.10"
              prefix_length: 32
          ebgp_config:
            asn: 65100
            should_redistribute_routes: true
          should_install_xi_route: false
  register: result
  ignore_errors: true

- name: Update network gateway
  nutanix.ncp.ntnx_Gateway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "local_gateway_ansible_updated"
    description: "Updated network gateway description"
    services:
      local_network_services:
        local_bgp_service:
          vpc_reference: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
          asn: 65002
          is_bgp_add_path_enabled: true
  register: result
  ignore_errors: true

- name: Delete network gateway
  nutanix.ncp.ntnx_Gateway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting network gateway
    - If the operation is create or update and C(wait) is true, it will return the network gateway details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "cloud_network_reference": null,
      "deployment": {
          "cluster_reference": "9a5a3f5a-1234-4d2b-b179-298db969c20d",
          "dns_servers": null,
          "interfaces": null,
          "management_interface": {
              "address": {"ipv4": {"prefix_length": 32, "value": "10.0.0.10"}, "ipv6": null},
              "default_gateway": {"ipv4": {"prefix_length": 32, "value": "10.0.0.1"}, "ipv6": null},
              "mtu": 1500,
              "subnet_reference": "1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p",
              "vlan_id": null
          },
          "ntp_servers": null,
          "should_synchronize_system_dns_servers": null,
          "should_synchronize_system_ntp_servers": null,
          "vcenter_datastore_name": null
      },
      "description": "Local BGP gateway created by Ansible",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "gateway_device_vendor": null,
      "high_availability_group": null,
      "installed_software_version": null,
      "is_active": true,
      "links": null,
      "metadata": null,
      "name": "local_gateway_ansible",
      "project_ext_id": null,
      "services": {
          "local_bgp_service": {
              "asn": 65001,
              "is_bgp_add_path_enabled": false,
              "vpc_reference": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
          },
          "local_vpn_service": null,
          "local_vtep_service": null,
          "service_address": null,
          "service_addresses": null
      },
      "status": {"message": "Gateway is up", "state": "UP"},
      "supported_software_version": null,
      "tenant_id": null,
      "vm": null,
      "vm_reference": null,
      "vpc": null,
      "vpc_reference": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    }

task_ext_id:
  description:
    - The external ID of the task associated with the operation.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the network gateway.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (idempotent no-op)
  returned: when applicable
  type: str
  sample: "Gateway with name 'local_gateway_ansible' already exists. Skipping creation."

error:
  description: This indicates the error message if any error occurred
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the status message
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating network gateway"
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
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def _ip_address_value_spec():
    return dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )


def _ip_address_spec():
    return dict(
        ipv4=dict(
            type="dict",
            options=_ip_address_value_spec(),
            obj=networking_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=_ip_address_value_spec(),
            obj=networking_sdk.IPv6Address,
        ),
    )


def _ip_address_or_fqdn_spec():
    fqdn_spec = dict(value=dict(type="str", required=True))
    spec = _ip_address_spec()
    spec["fqdn"] = dict(type="dict", options=fqdn_spec, obj=networking_sdk.FQDN)
    return spec


def _ipv4_subnet_spec():
    return dict(
        ip=dict(
            type="dict",
            options=_ip_address_value_spec(),
            required=True,
            obj=networking_sdk.IPv4Address,
        ),
        prefix_length=dict(type="int", required=True),
    )


def _ipv6_subnet_spec():
    return dict(
        ip=dict(
            type="dict",
            options=_ip_address_value_spec(),
            required=True,
            obj=networking_sdk.IPv6Address,
        ),
        prefix_length=dict(type="int", required=True),
    )


def _ip_subnet_spec():
    return dict(
        ipv4=dict(
            type="dict", options=_ipv4_subnet_spec(), obj=networking_sdk.IPv4Subnet
        ),
        ipv6=dict(
            type="dict", options=_ipv6_subnet_spec(), obj=networking_sdk.IPv6Subnet
        ),
    )


def _bgp_config_spec():
    return dict(
        asn=dict(type="int", required=False),
        password=dict(type="str", required=False, no_log=True),
        should_redistribute_routes=dict(type="bool", required=False),
    )


def _ospf_config_spec():
    return dict(
        area_id=dict(type="str", required=False),
        authentication_type=dict(
            type="str", required=False, choices=["MD5", "PLAIN_TEXT"]
        ),
        password=dict(type="str", required=False, no_log=True),
    )


def _ibgp_config_spec():
    return dict(
        peer_ip=dict(
            type="dict", options=_ip_address_spec(), obj=networking_sdk.IPAddress
        ),
        asn=dict(type="int", required=False),
        password=dict(type="str", required=False, no_log=True),
        should_redistribute_routes=dict(type="bool", required=False),
    )


def _internal_routing_config_spec():
    return dict(
        ospf_config=dict(
            type="dict", options=_ospf_config_spec(), obj=networking_sdk.OspfConfig
        ),
        ibgp_config_list=dict(
            type="list",
            elements="dict",
            options=_ibgp_config_spec(),
            obj=networking_sdk.IbgpConfig,
        ),
        local_prefix_list=dict(
            type="list",
            elements="dict",
            options=_ip_subnet_spec(),
            obj=networking_sdk.IPSubnet,
        ),
    )


def _local_vpn_service_spec():
    return dict(
        ebgp_config=dict(
            type="dict", options=_bgp_config_spec(), obj=networking_sdk.BgpConfig
        ),
        peer_igp_config=dict(
            type="dict",
            options=_internal_routing_config_spec(),
            obj=networking_sdk.InternalRoutingConfig,
        ),
    )


def _local_vtep_service_spec():
    return dict(vxlan_port=dict(type="int", required=False))


def _local_bgp_service_spec():
    return dict(
        vpc_reference=dict(type="str", required=False),
        asn=dict(type="int", required=False),
        is_bgp_add_path_enabled=dict(type="bool", required=False),
    )


def _local_network_services_spec():
    return dict(
        service_address=dict(
            type="dict", options=_ip_address_spec(), obj=networking_sdk.IPAddress
        ),
        service_addresses=dict(
            type="list",
            elements="dict",
            options=_ip_address_spec(),
            obj=networking_sdk.IPAddress,
        ),
        local_vpn_service=dict(
            type="dict",
            options=_local_vpn_service_spec(),
            obj=networking_sdk.LocalVpnService,
        ),
        local_vtep_service=dict(
            type="dict",
            options=_local_vtep_service_spec(),
            obj=networking_sdk.LocalVtepService,
        ),
        local_bgp_service=dict(
            type="dict",
            options=_local_bgp_service_spec(),
            obj=networking_sdk.LocalBgpService,
        ),
    )


def _remote_vpn_service_spec():
    return dict(
        service_address=dict(
            type="dict", options=_ip_address_spec(), obj=networking_sdk.IPAddress
        ),
        ebgp_config=dict(
            type="dict", options=_bgp_config_spec(), obj=networking_sdk.BgpConfig
        ),
        peer_igp_config=dict(
            type="dict",
            options=_internal_routing_config_spec(),
            obj=networking_sdk.InternalRoutingConfig,
        ),
        should_install_xi_route=dict(type="bool", required=False),
    )


def _vtep_spec():
    return dict(
        address=dict(
            type="dict", options=_ip_address_spec(), obj=networking_sdk.IPAddress
        )
    )


def _remote_vtep_service_spec():
    return dict(
        vxlan_port=dict(type="int", required=False),
        vteps=dict(
            type="list", elements="dict", options=_vtep_spec(), obj=networking_sdk.Vtep
        ),
    )


def _remote_bgp_service_spec():
    return dict(
        address=dict(
            type="dict", options=_ip_address_spec(), obj=networking_sdk.IPAddress
        ),
        asn=dict(type="int", required=False),
    )


def _remote_network_services_spec():
    return dict(
        remote_vpn_service=dict(
            type="dict",
            options=_remote_vpn_service_spec(),
            obj=networking_sdk.RemoteVpnService,
        ),
        remote_vtep_service=dict(
            type="dict",
            options=_remote_vtep_service_spec(),
            obj=networking_sdk.RemoteVtepService,
        ),
        remote_bgp_service=dict(
            type="dict",
            options=_remote_bgp_service_spec(),
            obj=networking_sdk.RemoteBgpService,
        ),
    )


def _management_interface_spec():
    return dict(
        subnet_reference=dict(type="str", required=False),
        vlan_id=dict(type="int", required=False),
        address=dict(
            type="dict", options=_ip_address_spec(), obj=networking_sdk.IPAddress
        ),
        default_gateway=dict(
            type="dict", options=_ip_address_spec(), obj=networking_sdk.IPAddress
        ),
        mtu=dict(type="int", required=False),
    )


def _gateway_interface_spec():
    return dict(
        subnet_reference=dict(type="str", required=False),
        ip_address=dict(
            type="dict", options=_ip_address_spec(), obj=networking_sdk.IPAddress
        ),
        default_gateway_address=dict(
            type="dict", options=_ip_address_spec(), obj=networking_sdk.IPAddress
        ),
        mac_address=dict(type="str", required=False),
        mtu=dict(type="int", required=False),
    )


def _deployment_spec():
    return dict(
        cluster_reference=dict(type="str", required=False),
        management_interface=dict(
            type="dict",
            options=_management_interface_spec(),
            obj=networking_sdk.GatewayManagementInterface,
        ),
        interfaces=dict(
            type="list",
            elements="dict",
            options=_gateway_interface_spec(),
            obj=networking_sdk.GatewayInterface,
        ),
        vcenter_datastore_name=dict(type="str", required=False),
        should_synchronize_system_ntp_servers=dict(type="bool", required=False),
        ntp_servers=dict(
            type="list",
            elements="dict",
            options=_ip_address_or_fqdn_spec(),
            obj=networking_sdk.IPAddressOrFQDN,
        ),
        should_synchronize_system_dns_servers=dict(type="bool", required=False),
        dns_servers=dict(
            type="list",
            elements="dict",
            options=_ip_address_spec(),
            obj=networking_sdk.IPAddress,
        ),
    )


def _services_spec():
    return dict(
        local_network_services=dict(
            type="dict",
            options=_local_network_services_spec(),
            obj=networking_sdk.LocalNetworkServices,
        ),
        remote_network_services=dict(
            type="dict",
            options=_remote_network_services_spec(),
            obj=networking_sdk.RemoteNetworkServices,
        ),
    )


def _peered_gateway_spec():
    return dict(ext_id=dict(type="str", required=True))


def _high_availability_group_spec():
    return dict(
        is_ha_enabled=dict(type="bool", required=False),
        algorithm=dict(type="str", required=False, choices=["ACTIVE_BACKUP"]),
        peered_gateways=dict(
            type="list",
            elements="dict",
            options=_peered_gateway_spec(),
            obj=networking_sdk.PeeredGateway,
        ),
    )


def _metadata_spec():
    return dict(
        owner_reference_id=dict(type="str", required=False),
        owner_user_name=dict(type="str", required=False),
        project_reference_id=dict(type="str", required=False),
        project_name=dict(type="str", required=False),
        category_ids=dict(type="list", elements="str", required=False),
    )


def get_module_spec():
    services_obj_map = {
        "local_network_services": networking_sdk.LocalNetworkServices,
        "remote_network_services": networking_sdk.RemoteNetworkServices,
    }

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        vpc_reference=dict(type="str"),
        cloud_network_reference=dict(type="str"),
        gateway_device_vendor=dict(type="str"),
        project_ext_id=dict(type="str"),
        deployment=dict(
            type="dict",
            options=_deployment_spec(),
            obj=networking_sdk.GatewayDeployment,
        ),
        services=dict(
            type="dict",
            options=_services_spec(),
            obj=services_obj_map,
            mutually_exclusive=[("local_network_services", "remote_network_services")],
        ),
        high_availability_group=dict(
            type="dict",
            options=_high_availability_group_spec(),
            obj=networking_sdk.HighAvailabilityGroup,
        ),
        metadata=dict(
            type="dict", options=_metadata_spec(), obj=networking_sdk.Metadata
        ),
    )
    return module_args


def _strip_read_only_gateway_fields(spec):
    """Remove server-populated read-only fields from a Gateway spec before update."""
    for field in (
        "installed_software_version",
        "supported_software_version",
        "vm_reference",
        "is_active",
        "status",
        "vpc",
        "vm",
        "links",
        "tenant_id",
    ):
        if hasattr(spec, field):
            setattr(spec, field, None)
    return spec


def _find_gateway_by_name(module, gateways_api, name):
    """Return the first gateway matching the provided name, or None."""
    try:
        resp = gateways_api.list_gateways(_filter="name eq '{0}'".format(name))
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while checking for existing gateway by name",
        )
    if resp is None or resp.data is None:
        return None
    data = resp.data
    if isinstance(data, list) and len(data) > 0:
        return data[0]
    return None


def create_Gateway(module, result, gateways_api):
    validate_required_params(module, ["name"])

    sg = SpecGenerator(module)
    default_spec = networking_sdk.Gateway()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create network gateway spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    existing = _find_gateway_by_name(module, gateways_api, module.params.get("name"))
    if existing is not None:
        result["ext_id"] = getattr(existing, "ext_id", None)
        result["response"] = strip_internal_attributes(existing.to_dict())
        result["skipped"] = (
            "Gateway with name '{0}' already exists. Skipping creation.".format(
                module.params.get("name")
            )
        )
        result["msg"] = result["skipped"]
        return

    resp = None
    try:
        resp = gateways_api.create_gateway(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating network gateway",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.GATEWAY
        )
        if ext_id:
            result["ext_id"] = ext_id
            gateway_resp = get_gateway(module, gateways_api, ext_id)
            result["response"] = strip_internal_attributes(gateway_resp.to_dict())
    result["changed"] = True


def _check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    for read_only in (
        "installed_software_version",
        "supported_software_version",
        "vm_reference",
        "is_active",
        "status",
        "vpc",
        "vm",
        "links",
        "tenant_id",
    ):
        old_spec_dict.pop(read_only, None)
        update_spec_dict.pop(read_only, None)
    return old_spec_dict == update_spec_dict


def update_Gateway(module, result, gateways_api):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_gateway(module, gateways_api, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating network gateway", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update network gateway spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if _check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = "Nothing to change."
        module.exit_json(msg="Nothing to change.", **result)

    _strip_read_only_gateway_fields(update_spec)

    resp = None
    try:
        resp = gateways_api.update_gateway_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating network gateway",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        gateway_resp = get_gateway(module, gateways_api, ext_id)
        result["response"] = strip_internal_attributes(gateway_resp.to_dict())
    result["changed"] = True


def delete_Gateway(module, result, gateways_api):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Network gateway with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    old_spec = get_gateway(module, gateways_api, ext_id)
    etag = get_etag(data=old_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = gateways_api.delete_gateway_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting network gateway",
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
        "task_ext_id": None,
        "error": None,
    }
    api_instance = get_gateways_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_Gateway(module, result, api_instance)
        else:
            create_Gateway(module, result, api_instance)
    else:
        delete_Gateway(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
