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
  - A network gateway is a managed VyOS-based appliance VM used by Flow Virtual Networking to
    provide VPN, VTEP or BGP connectivity between VPCs / overlay subnets and external or remote networks.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Network Gateway) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin, VPC Admin
    - >-
      B(Update a Network Gateway) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin, VPC Admin
    - >-
      B(Delete a Network Gateway) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin, VPC Admin
    - >-
      B(Upgrade a Network Gateway) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
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
      - Required for update, delete and upgrade operations.
    type: str
    required: false
  upgrade:
    description:
      - When true and C(ext_id) is provided the module upgrades the gateway to the latest supported version
        using the C(/gateways/{extId}/$actions/upgrade) endpoint.
      - Mutually exclusive with regular update fields; C(state) must be C(present).
    type: bool
    required: false
    default: false
  name:
    description:
      - Name of the gateway.
      - Required for create operation.
      - Maximum 128 characters.
    type: str
    required: false
  description:
    description:
      - Description of the gateway.
      - Maximum 1000 characters.
    type: str
    required: false
  vpc_reference:
    description:
      - External ID of the VPC where this gateway will be deployed.
      - Mutually exclusive with C(cloud_network_reference).
    type: str
    required: false
  cloud_network_reference:
    description:
      - External ID of the cloud network on which the gateway is deployed (NC2 deployments).
      - Mutually exclusive with C(vpc_reference).
    type: str
    required: false
  vm_reference:
    description:
      - Reference to a dedicated VM on which a local gateway is deployed.
    type: str
    required: false
  gateway_device_vendor:
    description:
      - Third-party gateway vendor identifier for remote gateways.
    type: str
    required: false
  is_active:
    description:
      - Indicates whether the gateway can be used to service a subnet extension's datapath.
      - This field is server populated for local gateways and is typically read-only.
    type: bool
    required: false
  deployment:
    description:
      - Deployment configuration describing where the network gateway VM is deployed and how its NICs are configured.
      - Required when deploying a local (on-prem) network gateway.
    type: dict
    required: false
    suboptions:
      cluster_reference:
        description:
          - PE cluster external ID on which to deploy the gateway VM.
        type: str
        required: true
      vcenter_datastore_name:
        description:
          - Datastore name to use when the hypervisor is ESXi.
        type: str
        required: false
      should_synchronize_system_ntp_servers:
        description:
          - Whether to synchronize NTP servers from the system configuration.
        type: bool
        required: false
      should_synchronize_system_dns_servers:
        description:
          - Whether to synchronize DNS servers from the system configuration.
        type: bool
        required: false
      ntp_servers:
        description:
          - List of NTP servers (IPv4/IPv6/FQDN) configured on the gateway VM.
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
                default: 32
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
                default: 128
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
      dns_servers:
        description:
          - List of DNS server IP addresses (IPv4/IPv6) configured on the gateway VM.
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
                default: 32
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
                default: 128
      management_interface:
        description:
          - Management network interface for the gateway VM.
          - When C(vpc_reference) is provided, the gateway auto-provisions its subnet inside the VPC;
            otherwise a VLAN subnet or a VLAN id must be supplied along with C(address) and C(default_gateway).
        type: dict
        required: false
        suboptions:
          subnet_reference:
            description:
              - External ID of the on-prem VLAN subnet used to reach the gateway VM.
            type: str
            required: false
          vlan_id:
            description:
              - VLAN id to use when a subnet reference is not supplied (VLAN without IPAM).
            type: int
            required: false
          mtu:
            description:
              - MTU for the management interface.
            type: int
            required: false
          address:
            description:
              - Static IP address assigned to the management interface.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address of the management interface.
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
                    default: 32
              ipv6:
                description:
                  - IPv6 address of the management interface.
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
                    default: 128
          default_gateway:
            description:
              - Default gateway of the management network.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address of the default gateway.
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
                    default: 32
              ipv6:
                description:
                  - IPv6 address of the default gateway.
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
                    default: 128
      interfaces:
        description:
          - Additional data-plane interfaces attached to the gateway VM.
        type: list
        elements: dict
        required: false
        suboptions:
          subnet_reference:
            description:
              - External ID of the VLAN or VPC subnet to attach the interface to.
            type: str
            required: false
          mac_address:
            description:
              - MAC address of the interface (optional, usually auto-assigned).
            type: str
            required: false
          mtu:
            description:
              - MTU for this interface.
            type: int
            required: false
          ip_address:
            description:
              - Static IP address of the interface.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address of the interface.
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
                    default: 32
              ipv6:
                description:
                  - IPv6 address of the interface.
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
                    default: 128
          default_gateway_address:
            description:
              - Default gateway address to use for traffic on this interface.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address of the default gateway for this interface.
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
                    default: 32
              ipv6:
                description:
                  - IPv6 address of the default gateway for this interface.
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
                    default: 128
  services:
    description:
      - Local or remote gateway service.
      - Set exactly one of C(local_services) OR C(remote_services); each of them must
        additionally include exactly one of C(vpn), C(vtep) or C(bgp).
    type: dict
    required: false
    suboptions:
      local_services:
        description:
          - Service configuration for a local (on-prem / this-PC) gateway.
        type: dict
        required: false
        suboptions:
          service_address:
            description:
              - Primary floating IP address associated with the local gateway.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address of the service address.
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
                    default: 32
              ipv6:
                description:
                  - IPv6 address of the service address.
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
                    default: 128
          service_addresses:
            description:
              - List of floating IP addresses associated with the local gateway.
            type: list
            elements: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address entry.
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
                    default: 32
              ipv6:
                description:
                  - IPv6 address entry.
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
                    default: 128
          vpn:
            description:
              - Local VPN service configuration.
            type: dict
            required: false
            suboptions:
              ebgp_config:
                description:
                  - Peer eBGP configuration for the VPN tunnel.
                type: dict
                required: false
                suboptions:
                  asn:
                    description:
                      - Autonomous System Number.
                    type: int
                    required: false
                  password:
                    description:
                      - Optional BGP MD5 authentication password.
                    type: str
                    required: false
                  should_redistribute_routes:
                    description:
                      - Whether to redistribute learned routes back to the peer.
                    type: bool
                    required: false
          vtep:
            description:
              - Local VTEP (VXLAN Tunnel End Point) service configuration.
            type: dict
            required: false
            suboptions:
              vxlan_port:
                description:
                  - UDP port used for VXLAN encapsulation.
                type: int
                required: false
          bgp:
            description:
              - Local BGP service configuration.
            type: dict
            required: false
            suboptions:
              vpc_reference:
                description:
                  - VPC external ID whose routes should be exchanged over BGP.
                type: str
                required: false
              asn:
                description:
                  - Autonomous System Number of this local BGP gateway.
                type: int
                required: false
              is_bgp_add_path_enabled:
                description:
                  - Enable BGP Add-Path capability on the local BGP service.
                type: bool
                required: false
      remote_services:
        description:
          - Service configuration for a remote gateway (reference to a peer in another PC / cloud).
        type: dict
        required: false
        suboptions:
          vpn:
            description:
              - Remote VPN service configuration.
            type: dict
            required: false
            suboptions:
              service_address:
                description:
                  - Public IP address of the remote VPN endpoint.
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - IPv4 address of the remote endpoint.
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
                        default: 32
                  ipv6:
                    description:
                      - IPv6 address of the remote endpoint.
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
                        default: 128
              should_install_xi_route:
                description:
                  - Whether to install Xi routes learned from the remote VPN peer.
                type: bool
                required: false
              ebgp_config:
                description:
                  - eBGP configuration used with the remote VPN peer.
                type: dict
                required: false
                suboptions:
                  asn:
                    description:
                      - Autonomous System Number of the remote peer.
                    type: int
                    required: false
                  password:
                    description:
                      - Optional BGP MD5 authentication password.
                    type: str
                    required: false
                  should_redistribute_routes:
                    description:
                      - Whether to redistribute learned routes back to the peer.
                    type: bool
                    required: false
          vtep:
            description:
              - Remote VTEP service configuration.
            type: dict
            required: false
            suboptions:
              vxlan_port:
                description:
                  - UDP port used for VXLAN encapsulation.
                type: int
                required: false
              vteps:
                description:
                  - List of remote VTEP endpoints.
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
                          - IPv4 address of the remote VTEP.
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
                            default: 32
                      ipv6:
                        description:
                          - IPv6 address of the remote VTEP.
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
                            default: 128
          bgp:
            description:
              - Remote BGP service configuration.
            type: dict
            required: false
            suboptions:
              asn:
                description:
                  - Autonomous System Number of the remote BGP gateway.
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
                      - IPv4 address of the remote BGP peer.
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
                        default: 32
                  ipv6:
                    description:
                      - IPv6 address of the remote BGP peer.
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
                        default: 128
  high_availability_group:
    description:
      - High availability configuration binding this gateway with one or more peered gateways.
    type: dict
    required: false
    suboptions:
      is_ha_enabled:
        description:
          - Whether HA is enabled for the gateway.
        type: bool
        required: false
      algorithm:
        description:
          - Algorithm used to select the active peer.
        type: str
        required: false
        choices:
          - ACTIVE_BACKUP
      peered_gateways:
        description:
          - List of peered gateway references participating in the HA group.
        type: list
        elements: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External ID of the peered gateway.
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
- name: Create a local VPN network gateway on an on-prem VLAN subnet
  nutanix.ncp.ntnx_gateway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "gw_local_vpn_ansible"
    description: "Local VPN gateway created by Ansible"
    deployment:
      cluster_reference: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
      should_synchronize_system_ntp_servers: true
      should_synchronize_system_dns_servers: true
      management_interface:
        subnet_reference: "9be0a3f9-8fe5-4a83-b3a0-8d1c7c8e2b21"
        mtu: 1500
        address:
          ipv4:
            value: "10.44.76.230"
            prefix_length: 24
        default_gateway:
          ipv4:
            value: "10.44.76.1"
            prefix_length: 24
    services:
      local_services:
        vpn: {}
  register: result

- name: Create a remote BGP gateway referencing an external ASN
  nutanix.ncp.ntnx_gateway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "gw_remote_bgp_ansible"
    description: "Remote BGP gateway peer"
    gateway_device_vendor: "GENERIC"
    services:
      remote_services:
        bgp:
          asn: 65001
          address:
            ipv4:
              value: "192.0.2.10"
              prefix_length: 32
  register: result

- name: Update gateway description
  nutanix.ncp.ntnx_gateway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "gw_local_vpn_ansible"
    description: "Updated gateway description"
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
      "deployment": null,
      "description": "Remote BGP gateway created by Ansible example playbook",
      "ext_id": "c13bf194-4017-4efb-abbf-d44c837818a9",
      "gateway_device_vendor": "GENERIC",
      "high_availability_group": null,
      "installed_software_version": null,
      "is_active": null,
      "links": null,
      "metadata": {
          "category_ids": null,
          "owner_reference_id": "00000000-0000-0000-0000-000000000000",
          "owner_user_name": "admin",
          "project_name": "_internal",
          "project_reference_id": "00000000-0000-0000-0000-000000000000"
      },
      "name": "gateway_ansible_example",
      "projectExtId": "00000000-0000-0000-0000-000000000000",
      "services": {
          "remote_services": {
              "remote_bgp_service": {
                  "address": {"ipv4": {"prefix_length": 32, "value": "192.0.2.10"}, "ipv6": null},
                  "asn": 65001
              },
              "remote_vpn_service": null,
              "remote_vtep_service": null
          }
      },
      "status": null,
      "supported_software_version": null,
      "tenant_id": null,
      "vm": null,
      "vm_reference": null,
      "vpc": null,
      "vpc_reference": null
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
  sample: "Gateway with name 'gateway_ansible_example' already exists. Skipping creation."

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
    "vm_reference",
    "is_active",
    "status",
    "vpc",
    "vm",
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
        options=dict(value=dict(type="str", required=True)),
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
        cluster_reference=dict(type="str", required=True),
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
        vpn=dict(
            type="dict",
            required=False,
            options=dict(
                ebgp_config=dict(
                    type="dict",
                    options=_get_bgp_config_spec(),
                    required=False,
                    obj=networking_sdk.BgpConfig,
                ),
            ),
            obj=networking_sdk.LocalVpnService,
        ),
        vtep=dict(
            type="dict",
            required=False,
            options=dict(
                vxlan_port=dict(type="int", required=False),
            ),
            obj=networking_sdk.LocalVtepService,
        ),
        bgp=dict(
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
        vpn=dict(
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
            ),
            obj=networking_sdk.RemoteVpnService,
        ),
        vtep=dict(
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
        bgp=dict(
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
    # NOTE: no ``obj=`` for this dict. ``Gatewayservices`` is a discriminated
    # union whose sub-classes (``LocalNetworkServices`` / ``RemoteNetworkServices``)
    # don't hang off attribute names, so SpecGenerator cannot recurse into it.
    # We instead build the final object manually in ``_build_services_object``.
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
                ext_id=dict(type="str", required=True),
            ),
            obj=networking_sdk.PeeredGateway,
        ),
    )


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        upgrade=dict(type="bool", default=False),
        name=dict(type="str"),
        description=dict(type="str"),
        vpc_reference=dict(type="str"),
        cloud_network_reference=dict(type="str"),
        vm_reference=dict(type="str"),
        gateway_device_vendor=dict(type="str"),
        is_active=dict(type="bool"),
        deployment=dict(
            type="dict",
            options=_get_deployment_spec(),
            obj=networking_sdk.GatewayDeployment,
        ),
        services=dict(
            type="dict",
            options=_get_services_spec(),
        ),
        high_availability_group=dict(
            type="dict",
            options=_get_ha_group_spec(),
            obj=networking_sdk.HighAvailabilityGroup,
        ),
    )
    return module_args


def _build_ip_address(value):
    if not value:
        return None
    obj = networking_sdk.IPAddress()
    if value.get("ipv4"):
        obj.ipv4 = networking_sdk.IPv4Address(
            value=value["ipv4"].get("value"),
            prefix_length=value["ipv4"].get("prefix_length", 32),
        )
    if value.get("ipv6"):
        obj.ipv6 = networking_sdk.IPv6Address(
            value=value["ipv6"].get("value"),
            prefix_length=value["ipv6"].get("prefix_length", 128),
        )
    return obj


def _build_bgp_config(value):
    if not value:
        return None
    return networking_sdk.BgpConfig(
        asn=value.get("asn"),
        password=value.get("password"),
        should_redistribute_routes=value.get("should_redistribute_routes"),
    )


def _build_local_services(local):
    if not local:
        return None
    lns = networking_sdk.LocalNetworkServices()
    lns.service_address = _build_ip_address(local.get("service_address"))
    if local.get("service_addresses"):
        lns.service_addresses = [
            _build_ip_address(ip) for ip in local["service_addresses"]
        ]
    if local.get("vpn") is not None:
        vpn = networking_sdk.LocalVpnService()
        if local["vpn"].get("ebgp_config"):
            vpn.ebgp_config = _build_bgp_config(local["vpn"]["ebgp_config"])
        lns.local_vpn_service = vpn
    if local.get("vtep") is not None:
        vtep = networking_sdk.LocalVtepService()
        if local["vtep"].get("vxlan_port") is not None:
            vtep.vxlan_port = local["vtep"]["vxlan_port"]
        lns.local_vtep_service = vtep
    if local.get("bgp") is not None:
        bgp = networking_sdk.LocalBgpService()
        if local["bgp"].get("vpc_reference") is not None:
            bgp.vpc_reference = local["bgp"]["vpc_reference"]
        if local["bgp"].get("asn") is not None:
            bgp.asn = local["bgp"]["asn"]
        if local["bgp"].get("is_bgp_add_path_enabled") is not None:
            bgp.is_bgp_add_path_enabled = local["bgp"]["is_bgp_add_path_enabled"]
        lns.local_bgp_service = bgp
    return lns


def _build_remote_services(remote):
    if not remote:
        return None
    rns = networking_sdk.RemoteNetworkServices()
    if remote.get("vpn") is not None:
        vpn = networking_sdk.RemoteVpnService()
        vpn.service_address = _build_ip_address(remote["vpn"].get("service_address"))
        if remote["vpn"].get("should_install_xi_route") is not None:
            vpn.should_install_xi_route = remote["vpn"]["should_install_xi_route"]
        vpn.ebgp_config = _build_bgp_config(remote["vpn"].get("ebgp_config"))
        rns.remote_vpn_service = vpn
    if remote.get("vtep") is not None:
        vtep = networking_sdk.RemoteVtepService()
        if remote["vtep"].get("vxlan_port") is not None:
            vtep.vxlan_port = remote["vtep"]["vxlan_port"]
        if remote["vtep"].get("vteps"):
            vteps = []
            for v in remote["vtep"]["vteps"]:
                vtep_obj = networking_sdk.Vtep()
                vtep_obj.address = _build_ip_address(v.get("address"))
                vteps.append(vtep_obj)
            vtep.vteps = vteps
        rns.remote_vtep_service = vtep
    if remote.get("bgp") is not None:
        bgp = networking_sdk.RemoteBgpService()
        if remote["bgp"].get("asn") is not None:
            bgp.asn = remote["bgp"]["asn"]
        bgp.address = _build_ip_address(remote["bgp"].get("address"))
        rns.remote_bgp_service = bgp
    return rns


def _apply_services_payload(spec, params_services):
    """Populate ``spec.services`` from module params.

    The SDK expresses ``services`` as a discriminated union
    (``Gatewayservices``) — SpecGenerator cannot recurse into it so we build
    the ``LocalNetworkServices`` / ``RemoteNetworkServices`` object manually
    here.
    """
    if not params_services:
        return
    local = params_services.get("local_services")
    remote = params_services.get("remote_services")
    if local:
        spec.services = _build_local_services(local)
    elif remote:
        spec.services = _build_remote_services(remote)


def _restore_services_wrapper(response_dict):
    """Wrap raw SDK services back into the local/remote_services envelope.

    The SDK stores services as either LocalNetworkServices or
    RemoteNetworkServices, both flattened onto `services`. To make the
    returned payload symmetric with the request layout, we introspect the
    known top-level keys and put them back under either
    `local_services` or `remote_services`.
    """
    if not isinstance(response_dict, dict):
        return response_dict
    services = response_dict.get("services")
    if not isinstance(services, dict):
        return response_dict
    if "local_services" in services or "remote_services" in services:
        return response_dict
    local_keys = {
        "service_address",
        "service_addresses",
        "local_vpn_service",
        "local_vtep_service",
        "local_bgp_service",
    }
    remote_keys = {
        "remote_vpn_service",
        "remote_vtep_service",
        "remote_bgp_service",
    }
    has_local = any(k in services for k in local_keys)
    has_remote = any(k in services for k in remote_keys)
    if has_local:
        response_dict["services"] = {"local_services": services}
    elif has_remote:
        response_dict["services"] = {"remote_services": services}
    return response_dict


def create_Gateway(module, api_instance, result):
    validate_required_params(module, ["name"])
    sg = SpecGenerator(module)
    default_spec = networking_sdk.Gateway()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create gateway spec", **result)

    _apply_services_payload(spec, module.params.get("services"))
    strip_read_only_fields(spec, fields=READ_ONLY_FIELDS)

    if module.check_mode:
        response_dict = _restore_services_wrapper(
            strip_internal_attributes(spec.to_dict())
        )
        result["response"] = response_dict
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
            result["response"] = _restore_services_wrapper(
                strip_internal_attributes(gw_resp.to_dict())
            )
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
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update gateway spec", **result)

    if module.params.get("services"):
        _apply_services_payload(update_spec, module.params.get("services"))
    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

    if module.check_mode:
        response_dict = _restore_services_wrapper(
            strip_internal_attributes(update_spec.to_dict())
        )
        result["response"] = response_dict
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
        result["response"] = _restore_services_wrapper(
            strip_internal_attributes(gw_resp.to_dict())
        )
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
