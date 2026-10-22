#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpn_connections_info_v2
short_description: Fetch VPN connections info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about VPN connections in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VPN connection.
  - If C(ext_id) is not provided, list multiple VPN connections optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get VPN connection by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, VPC Admin
    - >-
      B(Get list of VPN connections) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the VPN connection.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get VPN connection using ext_id
  nutanix.ncp.ntnx_vpn_connections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6b0d70b5-6ce8-4116-b46a-4b1c9e8f83fd"
  register: result
  ignore_errors: true

- name: List all VPN connections
  nutanix.ncp.ntnx_vpn_connections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List VPN connections with filter
  nutanix.ncp.ntnx_vpn_connections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'vpn_connection_ansible'"
  register: result
  ignore_errors: true

- name: List VPN connections with limit
  nutanix.ncp.ntnx_vpn_connections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VpnConnection info v4 API.
    - It can be a single VpnConnection if external ID is provided.
    - List of multiple VpnConnection if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
        "advertised_prefixes": null,
        "description": "VPN connection created by Ansible",
        "dpd_config": {
            "interval_secs": 30,
            "operation": "RESTART",
            "timeout_secs": 120
        },
        "dynamic_route_priority": 100,
        "ebgp_status": null,
        "ext_id": "6b0d70b5-6ce8-4116-b46a-4b1c9e8f83fd",
        "ipsec_config": {
            "esp_pfs_dh_group_number": 14,
            "ike_authentication_algorithm": "SHA256",
            "ike_encryption_algorithm": "AES256",
            "ike_lifetime_secs": 86400,
            "ipsec_authentication_algorithm": "SHA256",
            "ipsec_encryption_algorithm": "AES256",
            "ipsec_lifetime_secs": 43200,
            "local_authentication_id": "10.0.0.1",
            "local_vti_ip": {
                "ipv4": {
                    "prefix_length": 30,
                    "value": "169.254.1.1"
                },
                "ipv6": null
            },
            "pre_shared_key": null,
            "remote_authentication_id": "10.0.0.2",
            "remote_vti_ip": {
                "ipv4": {
                    "prefix_length": 30,
                    "value": "169.254.1.2"
                },
                "ipv6": null
            }
        },
        "ipsec_tunnel_status": null,
        "learned_prefixes": null,
        "links": null,
        "local_gateway_reference": "2e40ff57-20aa-4d2b-b179-298db969c20d",
        "local_gateway_role": "INITIATOR",
        "metadata": null,
        "name": "vpn_connection_ansible",
        "qos_config": {
            "egress_limit_mbps": 100,
            "ingress_limit_mbps": 100
        },
        "remote_gateway_reference": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
        "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VPN connections info"

error:
  description: This field typically holds information about any errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the VPN connection.
  type: str
  returned: When external ID is provided
  sample: "6b0d70b5-6ce8-4116-b46a-4b1c9e8f83fd"

total_available_results:
  description: The total number of available VPN connections in PC.
  type: int
  returned: When all VPN connections are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_vpn_connections_api_instance,
)
from ..module_utils.v4.network.helpers import get_vpn_connection  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_vpn_connection_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_vpn_connection(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_vpn_connections(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VPN connections info spec", **result)

    try:
        resp = api_instance.list_vpn_connections(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VPN connections info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vpn_connections_api_instance(module)
    if module.params.get("ext_id"):
        get_vpn_connection_using_ext_id(module, api_instance, result)
    else:
        get_vpn_connections(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
