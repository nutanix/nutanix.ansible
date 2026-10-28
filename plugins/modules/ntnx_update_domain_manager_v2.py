#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_update_domain_manager_v2
short_description: Update a Domain Manager (Prism Central) entity
version_added: "2.7.0"
description:
    - Update a domain manager (Prism Central) resource.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Update Domain Manager) -
      Required Roles: Cluster Admin, Domain Manager Admin, Internal Super Admin,
      Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported (update the domain manager entity).
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external identifier of the domain manager (Prism Central) resource.
      - Required for update entity.
    type: str
    required: true
  config:
    description: Domain manager (Prism Central) cluster configuration details.
    type: dict
    required: true
    suboptions:
      should_enable_lockdown_mode:
        description: A boolean value indicating whether to enable lockdown mode for a cluster.
        type: bool
        required: false
      build_info:
        description: Currently representing the build information to be used for the cluster creation.
        type: dict
        required: false
        suboptions:
          version:
            description: Software version.
            type: str
            required: false
      name:
        description: Name of the domain manager (Prism Central).
        type: str
        required: false
      size:
        description: Domain manager (Prism Central) size is an enumeration of starter, small, large, or extra large starter values.
        type: str
        required: false
        choices:
          - SMALL
          - LARGE
          - EXTRALARGE
          - STARTER
      resource_config:
        description:
          - This configuration is used to provide the resource-related details
            like container external identifiers of the domain manager (Prism
            Central).
        type: dict
        required: false
        suboptions:
          container_ext_ids:
            description: The external identifier of the container that will be used to create the domain manager (Prism Central) cluster.
            type: list
            required: false
            elements: str
      credentials:
        description: The credentials consist of a username and password for a particular user of a domain manager (Prism Central).
        type: list
        elements: dict
        required: false
        suboptions:
          username:
            description: Username expected to be used to gain access into a system.
            type: str
            required: true
          password:
            description: Password expected to be used to gain access into a system.
            type: str
            required: true
  network:
    description: Domain manager (Prism Central) network configuration details.
    type: dict
    required: true
    suboptions:
      external_address:
        description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
        type: dict
        required: false
        suboptions:
          ipv4:
            description: An unique address that identifies a device on the internet or a local network in IPv4 format.
            type: dict
            required: false
            suboptions:
              value:
                description: The IPv4 address of the host.
                type: str
                required: true
              prefix_length:
                description: The prefix length of the network to which this host IPv4 address belongs.
                type: int
                required: false
                default: 32
          ipv6:
            description: An unique address that identifies a device on the internet or a local network in IPv6 format.
            type: dict
            required: false
            suboptions:
              value:
                description: The IPv6 address of the host.
                type: str
                required: true
              prefix_length:
                description: The prefix length of the network to which this host IPv6 address belongs.
                type: int
                required: false
                default: 128
      name_servers:
        description:
          - List of name servers on a cluster.
          - For create operation, only ipv4 address / fqdn values are supported currently.
        type: list
        required: false
        elements: dict
        suboptions:
          ipv4:
            description: An unique address that identifies a device on the internet or a local network in IPv4 format.
            type: dict
            required: false
            suboptions:
              value:
                description: The IPv4 address of the host.
                type: str
                required: true
              prefix_length:
                description: The prefix length of the network to which this host IPv4 address belongs.
                type: int
                required: false
                default: 32
          ipv6:
            description: An unique address that identifies a device on the internet or a local network in IPv6 format.
            type: dict
            required: false
            suboptions:
              value:
                description: The IPv6 address of the host.
                type: str
                required: true
              prefix_length:
                description: The prefix length of the network to which this host IPv6 address belongs.
                type: int
                required: false
                default: 128
          fqdn:
            description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
            type: dict
            required: false
            suboptions:
              value:
                description: Fully Qualified Domain Name of the Host.
                type: str
                required: false
      ntp_servers:
        description:
          - List of NTP servers on a cluster
          - For create operation, only ipv4 address / fqdn values are supported currently.
        type: list
        required: false
        elements: dict
        suboptions:
          ipv4:
            description: An unique address that identifies a device on the internet or a local network in IPv4 format.
            type: dict
            required: false
            suboptions:
              value:
                description: The IPv4 address of the host.
                type: str
                required: true
              prefix_length:
                description: The prefix length of the network to which this host IPv4 address belongs.
                type: int
                required: false
                default: 32
          ipv6:
            description: An unique address that identifies a device on the internet or a local network in IPv6 format.
            type: dict
            required: false
            suboptions:
              value:
                description: The IPv6 address of the host.
                type: str
                required: true
              prefix_length:
                description: The prefix length of the network to which this host IPv6 address belongs.
                type: int
                required: false
                default: 128
          fqdn:
            description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
            type: dict
            required: false
            suboptions:
              value:
                description: Fully Qualified Domain Name of the Host.
                type: str
                required: false
      internal_networks:
        description: This configuration is used to internally manage Prism Central network.
        type: list
        elements: dict
        required: false
        suboptions:
          default_gateway:
            description:
              - The default gateway of the network.
              - An unique address that identifies a device on the internet or a local network in
                IPv4/IPv6 format or a Fully Qualified Domain Name.
            type: dict
            required: true
            suboptions:
              ipv4:
                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv4 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description: The prefix length of the network to which this host IPv4 address belongs.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv6 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description: The prefix length of the network to which this host IPv6 address belongs.
                    type: int
                    required: false
                    default: 128
              fqdn:
                description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                type: dict
                required: false
                suboptions:
                  value:
                    description: Fully Qualified Domain Name of the Host.
                    type: str
                    required: false
          subnet_mask:
            description:
              - The subnet mask of the network.
              - An unique address that identifies a device on the internet or a local network in
                IPv4/IPv6 format or a Fully Qualified Domain Name.
            type: dict
            required: true
            suboptions:
              ipv4:
                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv4 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description: The prefix length of the network to which this host IPv4 address belongs.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv6 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description: The prefix length of the network to which this host IPv6 address belongs.
                    type: int
                    required: false
                    default: 128
              fqdn:
                description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                type: dict
                required: false
                suboptions:
                  value:
                    description: Fully Qualified Domain Name of the Host.
                    type: str
                    required: false
          ip_ranges:
            description: Range of IPs used for Prism Central network setup.
            type: list
            elements: dict
            required: false
            suboptions:
              begin:
                description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description: The IPv4 address of the host.
                        type: str
                        required: true
                      prefix_length:
                        description: The prefix length of the network to which this host IPv4 address belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description: The IPv6 address of the host.
                        type: str
                        required: true
                      prefix_length:
                        description: The prefix length of the network to which this host IPv6 address belongs.
                        type: int
                        required: false
                        default: 128
              end:
                description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description: The IPv4 address of the host.
                        type: str
                        required: true
                      prefix_length:
                        description: The prefix length of the network to which this host IPv4 address belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description: The IPv6 address of the host.
                        type: str
                        required: true
                      prefix_length:
                        description: The prefix length of the network to which this host IPv6 address belongs.
                        type: int
                        required: false
                        default: 128
      external_networks:
        description: This configuration is used to manage Prism Central.
        type: list
        elements: dict
        required: false
        suboptions:
          default_gateway:
            description:
              - The default gateway of the network.
              - An unique address that identifies a device on the internet or a local network in
                IPv4/IPv6 format or a Fully Qualified Domain Name.
            type: dict
            required: true
            suboptions:
              ipv4:
                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv4 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description: The prefix length of the network to which this host IPv4 address belongs.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv6 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description: The prefix length of the network to which this host IPv6 address belongs.
                    type: int
                    required: false
                    default: 128
              fqdn:
                description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                type: dict
                required: false
                suboptions:
                  value:
                    description: Fully Qualified Domain Name of the Host.
                    type: str
                    required: false
          subnet_mask:
            description:
              - The subnet mask of the network.
              - An unique address that identifies a device on the internet or a local network in
                IPv4/IPv6 format or a Fully Qualified Domain Name.
            type: dict
            required: true
            suboptions:
              ipv4:
                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv4 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description: The prefix length of the network to which this host IPv4 address belongs.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv6 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description: The prefix length of the network to which this host IPv6 address belongs.
                    type: int
                    required: false
                    default: 128
              fqdn:
                description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                type: dict
                required: false
                suboptions:
                  value:
                    description: Fully Qualified Domain Name of the Host.
                    type: str
                    required: false
          ip_ranges:
            description: Range of IPs used for Prism Central network setup.
            type: list
            elements: dict
            required: true
            suboptions:
              begin:
                description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description: The IPv4 address of the host.
                        type: str
                        required: true
                      prefix_length:
                        description: The prefix length of the network to which this host IPv4 address belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description: The IPv6 address of the host.
                        type: str
                        required: true
                      prefix_length:
                        description: The prefix length of the network to which this host IPv6 address belongs.
                        type: int
                        required: false
                        default: 128
              end:
                description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description: The IPv4 address of the host.
                        type: str
                        required: true
                      prefix_length:
                        description: The prefix length of the network to which this host IPv4 address belongs.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description: The IPv6 address of the host.
                        type: str
                        required: true
                      prefix_length:
                        description: The prefix length of the network to which this host IPv6 address belongs.
                        type: int
                        required: false
                        default: 128
          network_ext_id:
            description: The network external identifier to which Domain Manager (Prism Central) is to be deployed or is already configured.
            type: str
            required: true
      http_proxy_config:
        description:
          - List of HTTP Proxy server configuration needed to access a cluster
            which is hosted behind a HTTP Proxy to not reveal its identity.
        type: list
        elements: dict
        required: false
        suboptions:
          ip_address:
            description:
              - HTTP Proxy server IP configuration needed to access a cluster
                which is hosted behind a HTTP Proxy to not reveal its identity.
            type: dict
            required: false
            suboptions:
              ipv4:
                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv4 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description: The prefix length of the network to which this host IPv4 address belongs.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                type: dict
                required: false
                suboptions:
                  value:
                    description: The IPv6 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description: The prefix length of the network to which this host IPv6 address belongs.
                    type: int
                    required: false
                    default: 128
          port:
            description:
              - HTTP Proxy server port configuration needed to access a cluster
                which is hosted behind a HTTP Proxy to not reveal its identity.
            type: int
            required: false
          username:
            description:
              - HTTP Proxy server username needed to access a cluster which is
                hosted behind a HTTP Proxy to not reveal its identity.
            type: str
            required: false
          password:
            description:
              - HTTP Proxy server password needed to access a cluster which is
                hosted behind a HTTP Proxy to not reveal its identity.
            type: str
            required: false
          name:
            description:
              - HTTP Proxy server name configuration needed to access a cluster
                which is hosted behind a HTTP Proxy to not reveal its identity.
            type: str
            required: true
          proxy_types:
            description: List of HTTP proxy types.
            type: list
            elements: str
            required: false
            choices:
              - HTTP
              - HTTPS
              - SOCKS
      http_proxy_white_list_config:
        description:
          - Targets HTTP traffic to which is exempted from going through the
            configured HTTP Proxy.
        type: list
        elements: dict
        required: false
        suboptions:
          target_type:
            description:
              - Type of the target which is exempted from going through the
                configured HTTP Proxy.
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
              - Target's identifier which is exempted from going through the
                configured HTTP Proxy.
            type: str
            required: true
  should_enable_high_availability:
    description: This configuration enables Prism Central to be deployed in scale-out mode.
    type: bool
    required: false
    default: false
  hosting_cluster_ext_id:
    description:
      - The external identifier of the cluster hosting the domain manager
        (Prism Central) instance.
    type: str
    required: false
  dryrun:
    description:
      - When C(true), the API executes in dry-run mode — it validates the
        request without performing the actual update.
    type: bool
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
- name: Update Prism Central name
  nutanix.ncp.ntnx_update_domain_manager_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
    config:
      name: "PC_updated_name"
    network: {}
  register: result

- name: Update Prism Central VIP (IPv4)
  nutanix.ncp.ntnx_update_domain_manager_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
    config: {}
    network:
      external_address:
        ipv4:
          value: "10.44.76.25"
          prefix_length: 32
  register: result

- name: Dry-run domain manager update
  nutanix.ncp.ntnx_update_domain_manager_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
    config:
      name: "PC_dryrun_name"
    network: {}
    dryrun: true
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for the domain manager update operation.
    - Domain manager details if C(wait) is true.
    - Task details if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "config": {
        "name": "PC_updated_name",
        "size": "SMALL"
      },
      "ext_id": "cfddac63-ffdb-4d9c-9a8c-54abf89ce234",
      "network": {
        "external_address": {
          "ipv4": {"prefix_length": 32, "value": "10.44.76.25"}
        }
      }
    }
task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:7f8d3f3c-91b1-4b5b-8117-91c54b7bdd92"
ext_id:
  description:
    - The external ID of the domain manager.
  returned: always
  type: str
  sample: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
skipped:
  description: This indicates whether the task was skipped
  returned: always
  type: bool
  sample: false
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
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while updating domain manager"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.helpers import get_pc_config  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
    get_etag,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Server-populated attributes that must NOT be sent back in the update body.
_DOMAIN_MANAGER_READ_ONLY_FIELDS = (
    "created_time",
    "is_registered_with_hosting_cluster",
    "node_ext_ids",
    "links",
    "tenant_id",
)


def get_module_spec():
    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", default=32),
    )
    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", default=128),
    )
    ip_address_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=prism_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=prism_sdk.IPv6Address),
    )
    fqdn_spec = dict(
        value=dict(type="str"),
    )
    ipaddress_or_fqdn_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=prism_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=prism_sdk.IPv6Address),
        fqdn=dict(type="dict", options=fqdn_spec, obj=prism_sdk.FQDN),
    )
    ip_ranges_spec = dict(
        begin=dict(type="dict", options=ip_address_spec, obj=prism_sdk.IPAddress),
        end=dict(type="dict", options=ip_address_spec, obj=prism_sdk.IPAddress),
    )
    build_info_spec = dict(
        version=dict(type="str"),
    )
    resource_config_spec = dict(
        container_ext_ids=dict(type="list", elements="str"),
    )
    credentials_spec = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )
    config_spec = dict(
        should_enable_lockdown_mode=dict(type="bool"),
        build_info=dict(type="dict", options=build_info_spec, obj=prism_sdk.BuildInfo),
        name=dict(type="str"),
        size=dict(
            type="str",
            choices=["SMALL", "LARGE", "EXTRALARGE", "STARTER"],
        ),
        resource_config=dict(
            type="dict",
            options=resource_config_spec,
            obj=prism_sdk.DomainManagerResourceConfig,
        ),
        credentials=dict(
            type="list",
            elements="dict",
            options=credentials_spec,
            obj=prism_sdk.BasicAuth,
        ),
    )
    internal_networks_spec = dict(
        default_gateway=dict(
            type="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
            required=True,
        ),
        subnet_mask=dict(
            type="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
            required=True,
        ),
        ip_ranges=dict(
            type="list",
            elements="dict",
            options=ip_ranges_spec,
            obj=prism_sdk.IpRange,
        ),
    )
    external_networks_spec = dict(
        default_gateway=dict(
            type="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
            required=True,
        ),
        subnet_mask=dict(
            type="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
            required=True,
        ),
        ip_ranges=dict(
            type="list",
            elements="dict",
            options=ip_ranges_spec,
            obj=prism_sdk.IpRange,
            required=True,
        ),
        network_ext_id=dict(type="str", required=True),
    )
    http_proxy_spec = dict(
        ip_address=dict(type="dict", options=ip_address_spec, obj=prism_sdk.IPAddress),
        port=dict(type="int"),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
        name=dict(type="str", required=True),
        proxy_types=dict(
            type="list",
            elements="str",
            choices=["HTTP", "HTTPS", "SOCKS"],
        ),
    )
    http_proxy_white_list_spec = dict(
        target_type=dict(
            type="str",
            required=True,
            choices=[
                "IPV6_ADDRESS",
                "HOST_NAME",
                "DOMAIN_NAME_SUFFIX",
                "IPV4_NETWORK_MASK",
                "IPV4_ADDRESS",
            ],
        ),
        target=dict(type="str", required=True),
    )
    network_spec = dict(
        external_address=dict(
            type="dict", options=ip_address_spec, obj=prism_sdk.IPAddress
        ),
        name_servers=dict(
            type="list",
            elements="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
        ),
        ntp_servers=dict(
            type="list",
            elements="dict",
            options=ipaddress_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
        ),
        http_proxy_config=dict(
            type="list",
            elements="dict",
            options=http_proxy_spec,
            obj=prism_sdk.HttpProxyConfig,
        ),
        http_proxy_white_list_config=dict(
            type="list",
            elements="dict",
            options=http_proxy_white_list_spec,
            obj=prism_sdk.HttpProxyWhiteListConfig,
        ),
        internal_networks=dict(
            type="list",
            elements="dict",
            options=internal_networks_spec,
            obj=prism_sdk.BaseNetwork,
        ),
        external_networks=dict(
            type="list",
            elements="dict",
            options=external_networks_spec,
            obj=prism_sdk.ExternalNetwork,
        ),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        config=dict(
            type="dict",
            options=config_spec,
            obj=prism_sdk.DomainManagerClusterConfig,
            required=True,
        ),
        network=dict(
            type="dict",
            options=network_spec,
            obj=prism_sdk.DomainManagerNetwork,
            required=True,
        ),
        hosting_cluster_ext_id=dict(type="str"),
        should_enable_high_availability=dict(type="bool", default=False),
        dryrun=dict(type="bool"),
    )
    return module_args


def check_domain_manager_idempotency(old_spec, update_spec):
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    return old_spec == update_spec


def update_domain_manager(module, result, api_instance):
    """Update a domain manager (Prism Central) by ext_id."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_pc_config(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating domain manager with ext_id: {0}".format(
                ext_id
            ),
            **result,
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update domain manager spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_domain_manager_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    strip_read_only_fields(update_spec, fields=_DOMAIN_MANAGER_READ_ONLY_FIELDS)

    kwargs = {"if_match": etag}
    if module.params.get("dryrun") is not None:
        kwargs["_dryrun"] = module.params.get("dryrun")

    try:
        resp = api_instance.update_domain_manager_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating domain manager with ext_id: {0}".format(
                ext_id
            ),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        refreshed = get_pc_config(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(refreshed.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_domain_manager_api_instance(module)
    update_domain_manager(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
