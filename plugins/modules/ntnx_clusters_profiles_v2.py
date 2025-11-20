#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_profiles_v2
short_description: Manage Nutanix cluster profiles in Prism Central
description:
  - This module allows you to create, update, and delete Nutanix cluster profiles using Prism Central.
  - A cluster profile is a collection of configuration settings that can be applied to a cluster.
  - This module uses PC v4 APIs based SDKs
version_added: "2.4.0"
options:
  state:
    description:
      - Specify state
      - If C(state) is set to C(present) then the operation will be create the cluster profile
      - if C(state) is set to C(present) and C(ext_id) is given then it will update that cluster profile.
      - If C(state) is set to C(absent) and if the cluster profile exists, then cluster profile is deleted.
    choices:
      - present
      - absent
    type: str
    default: present
  ext_id:
    description:
      - The external ID of the cluster profile
      - Required to trigger update or delete operation.
    type: str
  name:
    description:
      - The name of the cluster profile.
    type: str
    required: false
  description:
    description:
      - The description of the cluster profile.
    type: str
    required: false
  allowed_overrides:
    description:
      - Indicates if a configuration of attached clusters can be skipped from monitoring.
    type: list
    elements: str
    required: false
    choices:
      - "NFS_SUBNET_WHITELIST_CONFIG"
      - "NTP_SERVER_CONFIG"
      - "SNMP_SERVER_CONFIG"
      - "SMTP_SERVER_CONFIG"
      - "PULSE_CONFIG"
      - "NAME_SERVER_CONFIG"
      - "RSYSLOG_SERVER_CONFIG"
  name_server_ip_list:
    description:
      - List of name servers on a cluster.
      - This is a part of payload for both clusters create and update operations.
      - Currently, only IPv4 address and FQDN (fully qualified domain name) values are supported for the create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      ipv4:
        description:
          - The IPv4 address of the name server.
        type: dict
        suboptions:
          value:
            description:
              - The value of the name server IP address.
            type: str
            required: true
          prefix_length:
            description:
              - The prefix for the name server IP address.
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
              - The value of the name server IPv6 address.
            type: str
            required: true
          prefix_length:
            description:
              - The prefix for the name server IPv6 address.
            type: int
            required: false
            default: 128
  ntp_server_ip_list:
    description:
      - List of NTP servers on a cluster.
      - This is a part of payload for both cluster create and update operations.
      - Currently, only IPv4 address and FQDN (fully qualified domain name) values are supported for the create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      ipv4:
        description:
          - The IPv4 address of the NTP server.
        type: dict
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
  smtp_server:
    description:
      - SMTP servers on a cluster. This is part of payload for cluster update operation only.
    type: dict
    required: false
    suboptions:
      email_address:
        description:
          - The email address of the SMTP server.
        type: str
        required: true
      server:
        description:
          - SMTP network details.
        type: dict
        required: true
        suboptions:
          ip_address:
            description:
              - An unique address that identifies a device on the internet or a local network in IPv4/IPv6 format or a Fully Qualified Domain Name.
            type: dict
            required: true
            suboptions:
              ipv4:
                description:
                  - The IPv4 address of the SMTP server.
                type: dict
                suboptions:
                  value:
                    description:
                      - The value of the SMTP server IP address.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix for the SMTP server IP address.
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
                      - The value of the SMTP server IPv6 address.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix for the SMTP server IPv6 address.
                    type: int
                    required: false
                    default: 128
              fqdn:
                description:
                  - The Fully Qualified Domain Name (FQDN) of the SMTP server.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The value of the SMTP server FQDN.
                    type: str
          port:
            description:
              - The port number of the SMTP server.
            type: int
            required: false
          username:
            description:
              - The username for the SMTP server.
            type: str
            required: false
          password:
            description:
              - The password for the SMTP server.
            type: str
            required: false
      type:
        description:
          - The type of the SMTP server.
        type: str
        required: false
        choices:
          - "PLAIN"
          - "STARTTLS"
          - "SSL"
  nfs_subnet_whitelist:
    description:
      - NFS subnet allowlist addresses. This is part of the payload for cluster update operation only.
    type: list
    elements: str
    required: false
  snmp_config:
    description:
      - SNMP configuration for the cluster.
    type: dict
    required: false
    suboptions:
      is_enabled:
        description:
          - SNMP status
        type: bool
        required: false
      users:
        description:
          - SNMP user information.
        type: list
        elements: dict
        required: false
        suboptions:
          username:
            description:
              - SNMP username. For SNMP trap v3 version, SNMP username is required parameter.
            type: str
            required: true
          auth_type:
            description:
              - SNMP user authentication type.
            type: str
            required: true
            choices:
              - "MD5"
              - "SHA"
          auth_key:
            description:
              - SNMP user authentication key.
            type: str
            required: true
          priv_type:
            description:
              - SNMP user encryption type.
            type: str
            required: false
            choices:
              - "AES"
              - "DES"
          priv_key:
            description:
              - SNMP user encryption key.
            type: str
            required: false
      transports:
        description:
          - SNMP transport details.
        type: list
        elements: dict
        required: false
        suboptions:
          protocol:
            description:
              - SNMP protocol type
            type: str
            required: true
            choices:
              - "UDP"
              - "TCP"
              - "UDP6"
              - "TCP6"
          port:
            description:
              - SNMP transport port
            type: int
            required: true
      traps:
        description:
          - SNMP trap details.
        type: list
        elements: dict
        required: false
        suboptions:
          address:
            description:
              - An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
            type: dict
            required: true
            suboptions:
              ipv4:
                description:
                  - The IPv4 address of the SNMP trap server.
                type: dict
                suboptions:
                  value:
                    description:
                      - The value of the SNMP trap server IP address.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix for the SNMP trap server IP address.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description:
                  - The IPv6 address of the SNMP trap server.
                type: dict
                suboptions:
                  value:
                    description:
                      - The value of the SNMP trap server IPv6 address.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix for the SNMP trap server IPv6 address.
                    type: int
                    required: false
                    default: 128
          username:
            description:
              - SNMP username. For SNMP trap v3 version, SNMP username is required parameter.
            type: str
            required: false
          protocol:
            description:
              - SNMP protocol type
            type: str
            required: true
            choices:
              - "UDP"
              - "TCP"
              - "UDP6"
              - "TCP6"
          port:
            description:
              - SNMP transport port
            type: int
            required: false
          should_inform:
            description:
              - SNMP information status.
            type: bool
            required: false
          engine_id:
            description:
              - SNMP engine ID.
            type: str
            required: false
          version:
            description:
              - SNMP version.
            type: str
            required: true
            choices:
              - "V2"
              - "V3"
          reciever_name:
            description:
              - SNMP receiver name.
            type: str
            required: false
          community_string:
            description:
              - SNMP community string.
            type: str
            required: false
  rsyslog_server_list:
    description:
      - List of rsyslog servers.
    type: list
    elements: dict
    required: false
    suboptions:
      server_name:
        description:
          - RSYSLOG server name.
        type: str
        required: true
      ip_address:
        description:
          - An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
        type: dict
        required: true
        suboptions:
          ipv4:
            description:
              - The IPv4 address of the RSYSLOG server.
            type: dict
            suboptions:
              value:
                description:
                  - The value of the RSYSLOG server IP address.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix for the RSYSLOG server IP address.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - The IPv6 address of the RSYSLOG server.
            type: dict
            suboptions:
              value:
                description:
                  - The value of the RSYSLOG server IPv6 address.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix for the RSYSLOG server IPv6 address.
                type: int
                required: false
                default: 128
      port:
        description:
          - RSYSLOG server port.
        type: int
        required: true
      network_protocol:
        description:
          - RSYSLOG server protocol type.
        type: str
        required: true
        choices:
          - "UDP"
          - "TCP"
          - "RELP"
      modules:
        description:
          - List of modules registered to RSYSLOG server.
        type: list
        elements: dict
        required: false
        suboptions:
          name:
            description:
              - RSYSLOG module name.
            type: str
            required: true
            choices:
              - "AUDIT"
              - "CALM"
              - "MINERVA_CVM"
              - "STARGATE"
              - "FLOW_SERVICE_LOGS"
              - "SYSLOG_MODULE"
              - "CEREBRO"
              - "API_AUDIT"
              - "GENESIS"
              - "PRISM"
              - "ZOOKEEPER"
              - "FLOW"
              - "EPSILON"
              - "ACROPOLIS"
              - "UHARA"
              - "LCM"
              - "APLOS"
              - "NCM_AIOPS"
              - "CURATOR"
              - "CASSANDRA"
              - "LAZAN"
          log_severity_level:
            description:
              - RSYSLOG module log severity level.
            type: str
            required: true
            choices:
              - "EMERGENCY"
              - "NOTICE"
              - "ERROR"
              - "ALERT"
              - "INFO"
              - "WARNING"
              - "DEBUG"
              - "CRITICAL"
          should_log_monitor_files:
            description:
              - Whether to log monitor files.
            type: bool
            required: false
  pulse_status:
    description:
      - Pulse status for a cluster.
    type: dict
    required: false
    suboptions:
      is_enabled:
        description:
          - Whether the pulse is enabled.
        type: bool
        required: false
      pii_scrubbing_level:
        description:
          - PII Scrubbing Level for pulse.
        type: str
        required: false
        choices:
          - "ALL"
          - "DEFAULT"
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create cluster profile
  nutanix.ncp.ntnx_clusters_profiles_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    name: "cluster_profile_1"
    description: "Cluster profile description"
    allowed_overrides:
      - "NTP_SERVER_CONFIG"
    name_server_ip_list:
      - ipv4:
          value: "240.29.254.180"
          prefix_length: 32
      - ipv6:
          value: "1a7d:9a64:df8d:dfd8:39c6:c4ea:e35c:0ba4"
          prefix_length: 128
    ntp_server_ip_list:
      - ipv4:
          value: "240.29.254.180"
          prefix_length: 32
      - ipv6:
          value: "1a7d:9a64:df8d:dfd8:39c6:c4ea:e35c:0ba4"
          prefix_length: 128
      - fqdn:
          value: "ntp.example.com"
    smtp_server:
      email_address: "email@example.com"
      server:
        ip_address:
          ipv4:
            value: "240.29.254.180"
            prefix_length: 32
          ipv6:
            value: "1a7d:9a64:df8d:dfd8:39c6:c4ea:e35c:0ba4"
            prefix_length: 128
          fqdn:
            value: "smtp.example.com"
        port: 465
        username: "smtp-user"
        password: "smtp-password"
      type: "SSL"
    nfs_subnet_whitelist:
      - "10.110.106.45/255.255.255.255"
    snmp_config:
      is_enabled: false
      users:
        - username: "snmpuser1"
          auth_type: "MD5"
          auth_key: "Test_SNMP_user_authentication_key"
          priv_type: "DES"
          priv_key: "Test_SNMP_user_encryption_key"
      transports:
        - protocol: "UDP"
          port: 21
      traps:
        - address:
            ipv4:
              value: "240.29.254.180"
              prefix_length: 32
            ipv6:
              value: "1a7d:9a64:df8d:dfd8:39c6:c4ea:e35c:0ba4"
              prefix_length: 128
          username: "trapuser"
          protocol: "UDP"
          port: 59
          should_inform: false
          engine_id: "abcd1234"
          version: "V3"
          reciever_name: "trap-receiver"
          community_string: "snmp-server community public RO 192.168.1.0 255.255.255.0"
    rsyslog_server_list:
      - server_name: "testServer1"
        ip_address:
          ipv4:
            value: "240.29.254.180"
            prefix_length: 32
          ipv6:
            value: "1a7d:9a64:df8d:dfd8:39c6:c4ea:e35c:0ba4"
            prefix_length: 128
        port: 29
        network_protocol: "UDP"
        modules:
          - name: "CASSANDRA"
            log_severity_level: "EMERGENCY"
            should_log_monitor_files: true
          - name: "CURATOR"
            log_severity_level: "ERROR"
            should_log_monitor_files: false
    pulse_status:
      is_enabled: false
      pii_scrubbing_level: "DEFAULT"
  register: result

- name: Update cluster profile
  nutanix.ncp.ntnx_clusters_profiles_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    name: "cluster_profile_1_updated"
    ext_id: "1146f181-188b-49e2-5995-356bf1b74aeb"
    description: "Cluster profile description"
    allowed_overrides:
      - "NTP_SERVER_CONFIG"
    name_server_ip_list:
      - ipv4:
          value: "240.29.254.180"
          prefix_length: 32
      - ipv6:
          value: "1a7d:9a64:df8d:dfd8:39c6:c4ea:e35c:0ba4"
          prefix_length: 128
    ntp_server_ip_list:
      - ipv4:
          value: "240.29.254.180"
          prefix_length: 32
      - ipv6:
          value: "1a7d:9a64:df8d:dfd8:39c6:c4ea:e35c:0ba4"
          prefix_length: 128
      - fqdn:
          value: "ntp.example.com"
    smtp_server:
      email_address: "email@example.com"
      server:
        ip_address:
          ipv4:
            value: "240.29.254.180"
            prefix_length: 32
          ipv6:
            value: "1a7d:9a64:df8d:dfd8:39c6:c4ea:e35c:0ba4"
            prefix_length: 128
          fqdn:
            value: "smtp.example.com"
        port: 465
        username: "smtp-user"
        password: "smtp-password"
      type: "SSL"
    nfs_subnet_whitelist:
      - "10.110.106.45/255.255.255.255"
    snmp_config:
      is_enabled: false
      users:
        - username: "snmpuser1"
          auth_type: "MD5"
          auth_key: "Test_SNMP_user_authentication_key"
          priv_type: "DES"
          priv_key: "Test_SNMP_user_encryption_key"
      transports:
        - protocol: "UDP"
          port: 21
      traps:
        - address:
            ipv4:
              value: "240.29.254.180"
              prefix_length: 32
            ipv6:
              value: "1a7d:9a64:df8d:dfd8:39c6:c4ea:e35c:0ba4"
              prefix_length: 128
          username: "trapuser"
          protocol: "UDP"
          port: 59
          should_inform: false
          engine_id: "abcd1234"
          version: "V3"
          reciever_name: "trap-receiver"
          community_string: "snmp-server community public RO 192.168.1.0 255.255.255.0"
    rsyslog_server_list:
      - server_name: "testServer1"
        ip_address:
          ipv4:
            value: "240.29.254.180"
            prefix_length: 32
          ipv6:
            value: "1a7d:9a64:df8d:dfd8:39c6:c4ea:e35c:0ba4"
            prefix_length: 128
        port: 29
        network_protocol: "UDP"
        modules:
          - name: "CASSANDRA"
            log_severity_level: "EMERGENCY"
            should_log_monitor_files: true
          - name: "CURATOR"
            log_severity_level: "ERROR"
            should_log_monitor_files: false
    pulse_status:
      is_enabled: false
      pii_scrubbing_level: "DEFAULT"
  register: result

- name: Delete cluster profile
  nutanix.ncp.ntnx_clusters_profiles_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "1146f181-188b-49e2-5995-356bf1b74aeb"
    state: "absent"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for the cluster profile operation.
        - For create and update, it will be cluster profile details if C(wait) is True and task details if C(wait) is False.
        - For delete, it will be always task details.
    type: dict
    returned: always
    sample:
      {
        "allowed_overrides": [
            "NTP_SERVER_CONFIG"
        ],
        "cluster_count": 0,
        "clusters": null,
        "create_time": "2025-11-05T13:20:58.452203+00:00",
        "created_by": "00000000-0000-0000-0000-000000000000",
        "description": "Cluster profile description",
        "drifted_cluster_count": 0,
        "ext_id": "4664f67d-539b-4ada-5d38-4d6d9c19b32b",
        "last_update_time": "2025-11-05T13:20:58.452203+00:00",
        "last_updated_by": "00000000-0000-0000-0000-000000000000",
        "links": null,
        "name": "cluster_profile_1",
        "name_server_ip_list": [
            {
                "ipv4": {
                    "prefix_length": 32,
                    "value": "240.29.254.180"
                },
                "ipv6": null
            }
        ],
        "nfs_subnet_whitelist": null,
        "ntp_server_ip_list": [
            {
                "fqdn": null,
                "ipv4": {
                    "prefix_length": 32,
                    "value": "240.29.254.180"
                },
                "ipv6": null
            }
        ],
        "pulse_status": {
            "is_enabled": false,
            "pii_scrubbing_level": "DEFAULT"
        },
        "rsyslog_server_list": [
            {
                "ext_id": null,
                "ip_address": {
                    "ipv4": {
                        "prefix_length": 32,
                        "value": "240.29.254.180"
                    },
                    "ipv6": null
                },
                "links": null,
                "modules": [
                    {
                        "log_severity_level": "EMERGENCY",
                        "name": "CASSANDRA",
                        "should_log_monitor_files": true
                    },
                    {
                        "log_severity_level": "ERROR",
                        "name": "CURATOR",
                        "should_log_monitor_files": false
                    }
                ],
                "network_protocol": "UDP",
                "port": 29,
                "server_name": "testServer1",
                "tenant_id": null
            }
        ],
        "smtp_server": {
            "email_address": "email@example.com",
            "server": {
                "ip_address": {
                    "fqdn": null,
                    "ipv4": {
                        "prefix_length": 32,
                        "value": "240.29.254.180"
                    },
                    "ipv6": null
                },
                "password": null,
                "port": 465,
                "username": "smtp-user"
            },
            "type": "SSL"
        },
        "snmp_config": {
            "ext_id": null,
            "is_enabled": false,
            "links": null,
            "tenant_id": null,
            "transports": [
                {
                    "port": 21,
                    "protocol": "UDP"
                }
            ],
            "traps": [
                {
                    "address": {
                        "ipv4": {
                            "prefix_length": 32,
                            "value": "240.29.254.180"
                        },
                        "ipv6": null
                    },
                    "community_string": "snmp-server community public RO 192.168.1.0 255.255.255.0",
                    "engine_id": "0x1234567890abcdef12",
                    "ext_id": null,
                    "links": null,
                    "port": 59,
                    "protocol": "UDP",
                    "reciever_name": "trap-receiver",
                    "should_inform": false,
                    "tenant_id": null,
                    "username": "trapuser",
                    "version": "V2"
                }
            ],
            "users": [
                {
                    "auth_key": null,
                    "auth_type": "MD5",
                    "ext_id": null,
                    "links": null,
                    "priv_key": null,
                    "priv_type": "DES",
                    "tenant_id": null,
                    "username": "snmpuser1"
                }
            ]
        },
        "tenant_id": null
      }
ext_id:
    description:
        - The external ID of the cluster profile.
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
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent or check mode (in delete operation)
    type: str
    sample: "Failed generating cluster profile create spec"
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
    get_cluster_profiles_api_instance,
    get_etag,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cluster_profile  # noqa: E402
from ..module_utils.v4.clusters_mgmt.spec.cluster_profiles import (  # noqa: E402
    ClusterProfileSpecs,
)
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

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clusters_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clusters_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = ClusterProfileSpecs.get_cluster_profile_spec()
    return module_args


def create_cluster_profile(module, cluster_profiles, result):

    sg = SpecGenerator(module)
    default_spec = clusters_sdk.ClusterProfile()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating cluster profile create spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = cluster_profiles.create_cluster_profile(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating cluster profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.CLUSTER_PROFILE
        )
        if ext_id:
            result["ext_id"] = ext_id
            cluster_profile = get_cluster_profile(module, cluster_profiles, ext_id)
            result["response"] = strip_internal_attributes(cluster_profile.to_dict())
    result["changed"] = True


def check_cluster_idempotency(current_spec, update_spec):

    users_current = current_spec.get("snmp_config", {}).get("users", [])
    users_update = update_spec.get("snmp_config", {}).get("users", [])

    if len(users_current) != len(users_update):
        return False

    if current_spec.get("smtp_server", {}).get("server") is not None:
        current_spec["smtp_server"]["server"]["password"] = None
    if update_spec.get("smtp_server", {}).get("server") is not None:
        update_spec["smtp_server"]["server"]["password"] = None

    for user_current, user_update in zip(users_current, users_update):
        if isinstance(user_current, dict):
            user_current["auth_key"] = None
            user_current["priv_key"] = None
        if isinstance(user_update, dict):
            user_update["auth_key"] = None
            user_update["priv_key"] = None

    if current_spec != update_spec:
        return False
    return True


def update_cluster_profile(module, cluster_profiles, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    sg = SpecGenerator(module)
    current_spec = get_cluster_profile(module, cluster_profiles, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating cluster profile", **result
        )

    kwargs = {"if_match": etag}
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating cluster profile update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_cluster_idempotency(
        strip_internal_attributes(current_spec.to_dict()),
        strip_internal_attributes(update_spec.to_dict()),
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)
    resp = None
    try:
        resp = cluster_profiles.update_cluster_profile_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating cluster profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_cluster_profile(module, cluster_profiles, ext_id=ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_cluster_profile(module, cluster_profiles, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    if module.check_mode:
        result["msg"] = (
            "Cluster Profile with ext_id:'{0}' will be deleted.".format(ext_id)
        )
        return

    current_spec = get_cluster_profile(module, cluster_profiles, ext_id=ext_id)

    etag = get_etag(current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting cluster profile", **result
        )

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = cluster_profiles.delete_cluster_profile_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting cluster profile",
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
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name",)),
            ("state", "absent", ("ext_id",)),
        ],
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
    cluster_profiles = get_cluster_profiles_api_instance(module)
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_cluster_profile(module, cluster_profiles, result)
        else:
            create_cluster_profile(module, cluster_profiles, result)
    else:
        delete_cluster_profile(module, cluster_profiles, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
