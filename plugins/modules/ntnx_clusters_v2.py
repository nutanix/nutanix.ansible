#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_v2
short_description: Manage Nutanix clusters in Prism Central
description:
  - This module allows you to create, update, and destroy Nutanix clusters using Prism Central.
  - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
options:
  state:
    description:
      - Specify state
      - If C(state) is set to C(present) then the operation will be create the cluster.
      - if C(state) is set to C(present) and C(ext_id) is given then it will update that cluster.
      - If C(state) is set to C(absent) and if the cluster exists, then cluster is destroyed.
      - After cluster create, register the cluster to PC for update or destroy.
    choices:
      - present
      - absent
    type: str
    default: present
  ext_id:
    description:
      - The external ID of the cluster.
      - Mandatory to trigger update or destroy operation.
    type: str
  name:
    description:
      - The name of the cluster.
    type: str
  nodes:
    description:
      - The list of nodes in the cluster.
    type: dict
    suboptions:
      node_list:
        description:
          - The list of nodes in the cluster.
        type: list
        elements: dict
        required: true
        suboptions:
          controller_vm_ip:
            description:
              - The IP address of the controller VM.
            type: dict
            required: true
            suboptions:
              ipv4:
                description:
                  - The IPv4 address of the controller VM.
                type: dict
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the IPv4 address.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description:
                  - The IPv6 address of the controller VM.
                type: dict
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the IPv6 address.
                    type: int
                    required: false
                    default: 128
          host_ip:
            description:
              - The IP address of the host.
              - Not required for cluster creation.
            type: dict
            suboptions:
              ipv4:
                description:
                  - The IPv4 address of the host.
                type: dict
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the IPv4 address.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description:
                  - The IPv6 address of the host.
                type: dict
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the IPv6 address.
                    type: int
                    required: false
                    default: 128
  config:
    description:
      - The configuration of the cluster.
    type: dict
    suboptions:
      cluster_function:
        description:
          - The function of the cluster.
        type: list
        elements: str
        choices:
          - AOS
          - ONE_NODE
          - TWO_NODE
      authorized_public_key_list:
        description:
          - The list of authorized public keys.
          - Cannot be set during cluster create.
          - Use cluster update to update the list.
          - Given public keys will override the existing public keys.
        type: list
        elements: dict
        suboptions:
          name:
            description:
              - The name of the public key.
            type: str
            required: true
          key:
            description:
              - The key of the public key.
            type: str
            required: true
      redundancy_factor:
        description:
          - The redundancy factor of the cluster.
        type: int
      cluster_arch:
        description:
          - The architecture of the cluster.
        type: str
        choices:
          - X86_64
          - PPC64LE
      fault_tolerance_state:
        description:
          - The fault tolerance state of the cluster.
        type: dict
        suboptions:
          domain_awareness_level:
            description:
              - The domain awareness level of the fault tolerance state.
            type: str
            required: true
            choices:
              - NODE
              - BLOCK
              - RACK
              - DISK
          desired_cluster_fault_tolerance:
            description:
              - The desired cluster fault tolerance of the fault tolerance state.
            type: str
            choices:
              - CFT_1N_OR_1D
              - CFT_2N_OR_2D
              - CFT_1N_AND_1D
              - CFT_0N_AND_0D
      operation_mode:
        description:
          - The operation mode of the cluster.
        type: str
        choices:
          - NORMAL
          - READ_ONLY
          - STAND_ALONE
          - SWITCH_TO_TWO_NODE
          - OVERRIDE
      encryption_in_transit_status:
        description:
          - The encryption in transit status of the cluster.
        type: str
        choices:
          - ENABLED
          - DISABLED
      pulse_status:
        description:
          - Flag to enable/disable pulse in cluster.
          - Supported only in update cluster operation.
        type: dict
        suboptions:
          is_enabled:
            description:
              - Whether to enable or disable pulse.
            type: bool
          pii_scrubbing_level:
            description:
              - The PII scrubbing level of the pulse.
            type: str
            choices:
              - ALL
              - DEFAULT
  network:
    description:
      - The network configuration of the cluster.
    type: dict
    suboptions:
      external_address:
        description:
          - The external address of the cluster.
        type: dict
        suboptions:
          ipv4:
            description:
              - The IPv4 address of the external address.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv4 address.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - The IPv6 address of the external address.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv6 address.
                type: int
                required: false
                default: 128
      external_data_service_ip:
        description:
          - The external data service IP of the cluster.
          - Cannot be set during cluster create.
          - Use cluster update to add/update.
        type: dict
        suboptions:
          ipv4:
            description:
              - The IPv4 address of the external data service IP.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv4 address.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - The IPv6 address of the external data service IP.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv6 address.
                type: int
                required: false
                default: 128
      nfs_subnet_whitelist:
        description:
          - The list of NFS subnet whitelist.
        type: list
        elements: str
      ntp_server_ip_list:
        description:
          - The list of NTP servers.
        type: list
        elements: dict
        suboptions:
          ipv4:
            description:
              - The IPv4 address of the NTP server.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv4 address.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - The IPv6 address of the NTP server.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv6 address.
                type: int
                required: false
                default: 128
          fqdn:
            description:
              - The FQDN of the NTP server.
            type: dict
            suboptions:
              value:
                description:
                  - The FQDN value.
                type: str
                required: true
      ntp_server_config_list:
        description:
          - NTP server configuration list.
          - Supported only in update cluster operation.
        type: list
        elements: dict
        required: false
        suboptions:
          ntp_server_address:
            description:
              - NTP server address.
            type: dict
            required: true
            suboptions:
              ipv4:
                description:
                  - The IPv4 address of the NTP server.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The value of the NTP server IP address.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix for the NTP server IP address.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description:
                  - The IPv6 address of the NTP server.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The value of the NTP server IPv6 address.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix for the NTP server IPv6 address.
                    type: int
                    required: false
                    default: 128
              fqdn:
                description:
                  - The Fully Qualified Domain Name (FQDN) of the NTP server.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The value of the NTP server FQDN.
                    type: str
                    required: true
          encryption_algorithm:
            description:
              - Encryption algorithm used for NTP server authentication.
            type: str
            required: false
            choices:
              - "SHA256"
              - "SHA384"
              - "SHA512"
          encryption_key:
            description:
              - Encryption key in hexadecimal format used for NTP server authentication.
            type: str
            required: false
          encryption_key_id:
            description:
              - Encryption key Id used for NTP server authentication.
            type: int
            required: false
      name_server_ip_list:
        description:
          - The list of name servers.
        type: list
        elements: dict
        suboptions:
          ipv4:
            description:
              - The IPv4 address of the name server.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv4 address.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - The IPv6 address of the name server.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv6 address.
                type: int
                required: false
                default: 128
          fqdn:
            description:
              - The FQDN of the name server.
            type: dict
            suboptions:
              value:
                description:
                  - The FQDN value.
                type: str
                required: true
      smtp_server:
        description:
          - The SMTP server configuration.
          - Cannot be set during cluster create.
          - Add/Update smtp server during cluster update.
        type: dict
        suboptions:
          email_address:
            description:
              - The email address of the SMTP server.
            type: str
          server:
            description:
              - The server configuration of the SMTP server.
            type: dict
            suboptions:
              ip_address:
                description:
                  - The IP address of the SMTP server.
                type: dict
                suboptions:
                  ipv4:
                    description:
                      - The IPv4 address of the SMTP server.
                    type: dict
                    suboptions:
                      value:
                        description:
                          - The IPv4 address value.
                        type: str
                        required: true
                      prefix_length:
                        description:
                          - The prefix length of the IPv4 address.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - The IPv6 address of the SMTP server.
                    type: dict
                    suboptions:
                      value:
                        description:
                          - The IPv6 address value.
                        type: str
                        required: true
                      prefix_length:
                        description:
                          - The prefix length of the IPv6 address.
                        type: int
                        required: false
                        default: 128
                  fqdn:
                    description:
                      - The FQDN of the SMTP server.
                    type: dict
                    suboptions:
                      value:
                        description:
                          - The FQDN value.
                        type: str
                        required: true
              port:
                description:
                  - The port of the SMTP server.
                type: int
              username:
                description:
                  - The username of the SMTP server.
                type: str
              password:
                description:
                  - The password of the SMTP server.
                  - If password is set, then idempotency checks will be skipped.
                type: str
          type:
            description:
              - The type of the SMTP server.
            type: str
            choices:
              - PLAIN
              - STARTTLS
              - SSL
      masquerading_ip:
        description:
          - The masquerading IP of the cluster.
        type: dict
        suboptions:
          ipv4:
            description:
              - The IPv4 address of the masquerading IP.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv4 address.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - The IPv6 address of the masquerading IP.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv6 address.
                type: int
                required: false
                default: 128
      management_server:
        description:
          - The management server configuration.
        type: dict
        suboptions:
          ip:
            description:
              - The IP address of the management server.
            type: dict
            suboptions:
              ipv4:
                description:
                  - The IPv4 address of the management server.
                type: dict
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the IPv4 address.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description:
                  - The IPv6 address of the management server.
                type: dict
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the IPv6 address.
                    type: int
                    required: false
                    default: 128
          type:
            description:
              - The type of the management server.
            type: str
            choices:
              - VCENTER
          is_registered:
            description:
              - Whether the management server is registered.
            type: bool
          in_use:
            description:
              - Whether the management server is in use.
            type: bool
          is_drs_enabled:
            description:
              - Whether DRS is enabled for the management server.
            type: bool
      fqdn:
        description:
          - The FQDN of the cluster.
        type: str
      key_management_server_type:
        description:
          - The key management server type of the cluster.
        type: str
        choices:
          - LOCAL
          - PRISM_CENTRAL
          - EXTERNAL
      backplane:
        description:
          - The backplane network configuration.
        type: dict
        suboptions:
          is_segmentation_enabled:
            description:
              - Whether segmentation is enabled for the backplane network.
            type: bool
          vlan_tag:
            description:
              - The VLAN tag of the backplane network.
            type: int
          subnet:
            description:
              - The subnet of the backplane network.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv4 address.
                type: int
                required: false
                default: 32
          netmask:
            description:
              - The netmask of the backplane network.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv4 address.
                type: int
                required: false
                default: 32
      http_proxy_list:
        description:
          - The list of HTTP proxies.
        type: list
        elements: dict
        suboptions:
          ip_address:
            description:
              - The IP address of the HTTP proxy.
            type: dict
            suboptions:
              ipv4:
                description:
                  - The IPv4 address of the HTTP proxy.
                type: dict
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the IPv4 address.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description:
                  - The IPv6 address of the HTTP proxy.
                type: dict
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the IPv6 address.
                    type: int
                    required: false
                    default: 128
          port:
            description:
              - The port of the HTTP proxy.
            type: int
          username:
            description:
              - The username of the HTTP proxy.
            type: str
          password:
            description:
              - The password of the HTTP proxy.
            type: str
          name:
            description:
              - The name of the HTTP proxy.
            type: str
            required: true
          proxy_types:
            description:
              - The types of the HTTP proxy.
            type: list
            elements: str
            choices:
              - HTTP
              - HTTPS
              - SOCKS
      http_proxy_white_list:
        description:
          - The list of HTTP proxy white list.
        type: list
        elements: dict
        suboptions:
          target_type:
            description:
              - The target type of the HTTP proxy white list.
            type: str
            required: true
            choices:
              - IPV6_ADDRESS
              - HOST_NAME
              - DOMAIN_NAME_SUFFIX
              - IPV4_NETWORK_MASK
              - IPV4_ADDRESS
          target:
            description:
              - The target of the HTTP proxy white list.
            type: str
            required: true
  categories:
    description:
      - The extIDs of categories of the cluster.
    type: list
    elements: str
  container_name:
    description:
      - The name of the container.
    type: str
  dryrun:
    description:
      - Whether to run prechecks only.
    type: bool
  timeout:
    description:
      - The timeout for the operation.
      - The timeout in seconds.
      - By default there is no timeout
    type: int
  wait:
    description:
      - Whether to wait for the operation to complete.
    type: bool
    default: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: Create cluster
  nutanix.ncp.ntnx_clusters_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    name: "cluster1"
    nodes:
      node_list:
        - controller_vm_ip:
            ipv4:
              value: "10.0.0.1"
    config:
      cluster_function: ["AOS"]
      redundancy_factor: 1
      cluster_arch: "X86_64"
      fault_tolerance_state:
        domain_awareness_level: "DISK"

- name: Create cluster with network configuration
  nutanix.ncp.ntnx_clusters_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    name: "cluster1"
    nodes:
      node_list:
        - controller_vm_ip:
            ipv4:
              value: "10.0.0.1"
    config:
      cluster_function: ["AOS"]
      authorized_public_key_list:
        - name: "key1"
          key: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDQ6"
      redundancy_factor: 1
      cluster_arch: X86_64
      fault_tolerance_state:
        domain_awareness_level: "DISK"
    network:
      external_address:
        ipv4:
          value: "10.0.0.2"
      ntp_server_ip_list:
        - fqdn:
            value: "test.ntp.org"
      name_server_ip_list:
        - ipv4:
            value: "10.0.0.9"
    timeout: 1800

- name: Update cluster
  nutanix.ncp.ntnx_clusters_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "<ext_id>"
    name: "cluster1"
    nodes:
    node_list:
      - controller_vm_ip:
          ipv4:
            value: "10.1.0.1"
    config:
      cluster_function: ["AOS"]
      redundancy_factor: 1
      cluster_arch: "X86_64"
      fault_tolerance_state:
        domain_awareness_level: "DISK"

- name: Destroy cluster
  nutanix.ncp.ntnx_clusters_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    state: absent
"""

RETURN = r"""
response:
    description:
        - Response for the cluster operation.
        - For update, it will be cluster details if C(wait) is True.
        - For update, it will be task details if C(wait) is False.
        - For create and delete, it will be always task details.
    type: dict
    returned: always
    sample:
        {
  "config":
    {
      "authorized_public_key_list":
        [
          {
            "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDQ6",
            "name": "key1",
          },
        ],
      "build_info":
        {
          "build_type": "release",
          "commit_id": "9b27c8bcb5fcaac58016f3bed74009655a157049",
          "full_version": "el8.5-release-fraser-6.8-stable-9b27c8bcb5fcaac58016f3bed74009655a157049",
          "short_commit_id": "9b27c8",
          "version": "fraser-6.8-stable",
        },
      "cluster_arch": "X86_64",
      "cluster_function": ["AOS", "ONE_NODE"],
      "cluster_software_map":
        [
          { "software_type": "NCC", "version": "ncc-5.0.0" },
          {
            "software_type": "NOS",
            "version": "el8.5-release-fraser-6.8-stable-9b27c8bcb5fcaac58016f3bed74009655a157049",
          },
        ],
      "encryption_in_transit_status": null,
      "encryption_option": null,
      "encryption_scope": null,
      "fault_tolerance_state":
        {
          "current_max_fault_tolerance": 0,
          "desired_max_fault_tolerance": 0,
          "domain_awareness_level": "DISK",
        },
      "hypervisor_types": ["AHV"],
      "incarnation_id": 1283123882137,
      "is_lts": false,
      "operation_mode": "NORMAL",
      "password_remote_login_enabled": true,
      "redundancy_factor": 1,
      "remote_support": false,
      "timezone": "UTC",
    },
  "container_name": null,
  "ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
  "inefficient_vm_count": null,
  "links": null,
  "name": "ansible_ag",
  "network":
    {
      "backplane":
        {
          "is_segmentation_enabled": false,
          "netmask": null,
          "subnet": null,
          "vlan_tag": null,
        },
      "external_address":
        {
          "ipv4": { "prefix_length": 32, "value": "10.0.0.1" },
          "ipv6": null,
        },
      "external_data_service_ip":
        {
          "ipv4": { "prefix_length": 32, "value": "10.0.0.2" },
          "ipv6": null,
        },
      "fqdn": null,
      "key_management_server_type": null,
      "management_server": null,
      "masquerading_ip": null,
      "masquerading_port": null,
      "name_server_ip_list":
        [
          {
            "fqdn": null,
            "ipv4": { "prefix_length": 32, "value": "10.0.0.6" },
            "ipv6": null,
          },
        ],
      "nfs_subnet_whitelist": null,
      "ntp_server_ip_list":
        [
          {
            "fqdn": { "value": "0.ntp.org" },
            "ipv4": null,
            "ipv6": null,
          },
        ],
      "smtp_server":
        {
          "email_address": "test@test.com",
          "server":
            {
              "ip_address":
                {
                  "ipv4": { "prefix_length": 32, "value": "10.0.0.8" },
                  "ipv6": null,
                },
              "password": null,
              "port": 25,
              "username": "username",
            },
          "type": "STARTTLS",
        },
    },
  "nodes":
    {
      "node_list":
        [
          {
            "controller_vm_ip":
              {
                "ipv4": { "prefix_length": 32, "value": "10.0.0.6" },
                "ipv6": null,
              },
            "host_ip":
              {
                "ipv4": { "prefix_length": 32, "value": "10.0.0.10" },
                "ipv6": null,
              },
            "node_uuid": "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9",
          },
        ],
      "number_of_nodes": 1,
    },
  "run_prechecks_only": null,
  "tenant_id": null,
  "upgrade_status": "SUCCEEDED",
  "vm_count": 1,
}
ext_id:
    description:
        - The external ID of the cluster.
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
task_ext_id:
    description:
        - The task external ID.
    type: str
    returned: always
    sample: "ZXJnb24=:100a5778-9824-49c7-9444-222aa97f5874"
changed:
    description:
        - Indicates if any changes were made during the operation.
    type: bool
    returned: always
    sample: true
msg:
    description:
        - The message from module operation if any.
    type: str
    returned: always
    sample: "Cluster with external ID '00061de6-4a87-6b06-185b-ac1f6b6f97e2' will be deleted."
error:
    description:
        - The error message if an error occurs.
    type: str
    returned: when an error occurs
skipped:
    description:
        - Indicates if the operation was skipped.
    type: bool
    returned: when the operation was skipped
    sample: true
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
    get_etag,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cluster  # noqa: E402
from ..module_utils.v4.clusters_mgmt.spec.clusters import ClusterSpecs  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clusters_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clusters_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = ClusterSpecs.get_cluster_spec()
    module_args["timeout"] = dict(type="int")
    module_args["dryrun"] = dict(type="bool")
    return module_args


def create_cluster(module, result):
    clusters = get_clusters_api_instance(module)
    sg = SpecGenerator(module)
    default_spec = clusters_sdk.Cluster()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating cluster create spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    dry_run = module.params.get("dryrun", False)
    try:
        resp = clusters.create_cluster(body=spec, _dryrun=dry_run)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating cluster",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id, polling_gap=15)

        # Post cluster create, cluster is still not registered to PC
        # So there will be no cluster info in PC, hence respond with task status
        result["response"] = strip_internal_attributes(resp.to_dict())

    if module.params.get("dryrun", False):
        result["changed"] = False
    else:
        result["changed"] = True


def check_cluster_idempotency(current_spec, update_spec):
    current_spec = strip_internal_attributes(current_spec.to_dict())
    update_spec = strip_internal_attributes(update_spec.to_dict())
    current_network = current_spec.get("network") or {}
    update_network = update_spec.get("network") or {}
    current_ntp_server_config = current_network.get("ntp_server_config_list") or []
    update_ntp_server_config = update_network.get("ntp_server_config_list") or []
    if len(current_ntp_server_config) != len(update_ntp_server_config):
        return False
    # trigger update if smtp server password is set
    smtp_server = update_network.get("smtp_server") or {}
    server = smtp_server.get("server") or {}
    if server.get("password"):
        return False
    for current_ntp, update_ntp in zip(
        current_ntp_server_config, update_ntp_server_config
    ):
        if isinstance(current_ntp, dict):
            current_ntp["encryption_key"] = None
        if isinstance(update_ntp, dict):
            update_ntp["encryption_key"] = None
    if current_spec != update_spec:
        return False
    return True


def update_cluster(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    sg = SpecGenerator(module)
    default_spec = clusters_sdk.Cluster()
    spec, err = sg.generate_spec(obj=default_spec)
    clusters = get_clusters_api_instance(module)
    current_spec = get_cluster(module, clusters, ext_id=ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for updating cluster", **result)

    kwargs = {"if_match": etag}
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating clusters update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_cluster_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)
    resp = None
    try:
        resp = clusters.update_cluster_by_id(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating cluster",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_cluster(module, clusters, ext_id=ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def destroy_cluster(module, result):
    ext_id = module.params.get("ext_id")

    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Cluster with external ID '{0}' will be deleted.".format(ext_id)
        return

    clusters = get_clusters_api_instance(module)
    current_spec = get_cluster(module, clusters, ext_id=ext_id)

    etag = get_etag(current_spec)
    if not etag:
        return module.fail_json("unable to fetch etag for destroying cluster", **result)

    kwargs = {"if_match": etag}
    dry_run = module.params.get("dryrun", False)
    resp = None
    try:
        resp = clusters.delete_cluster_by_id(extId=ext_id, _dryrun=dry_run, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting cluster",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        support_proxy=True,
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_cluster(module, result)
        else:
            create_cluster(module, result)
    else:
        destroy_cluster(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
