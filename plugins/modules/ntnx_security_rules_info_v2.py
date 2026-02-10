#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_rules_info_v2
short_description: Fetch network security policies info from Nutanix PC.
version_added: 2.0.0
description:
    - Fetch list of multiple network security policies info.
    - Fetch specific network security policy info by ext_id.
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - External id to fetch specific network security policy info.
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: Get all policies
  nutanix.ncp.ntnx_security_rules_info_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
  register: result

- name: Get particular policy
  nutanix.ncp.ntnx_security_rules_info_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    ext_id: "569a018e-18ac-4813-b00f-2aa0d0005042"
  register: result

- name: Fetch certain policy using filters
  nutanix.ncp.ntnx_security_rules_info_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    filter: "name eq 'rule1'"
  register: result

- name: Fetch only 5 policies using limit
  nutanix.ncp.ntnx_security_rules_info_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    limit: 5
  register: result
"""
RETURN = r"""
response:
  description:
    - Network security policy info if ext_id is provided
    - List of network security policies if ext_id is not provided
  returned: always
  type: dict
  sample: {
            "created_by": "00000000-0000-0000-0000-000000000000",
            "creation_time": "2024-07-19T12:55:54.945000+00:00",
            "description": "Ansible created rule updated",
            "ext_id": "e8347a03-28a0-4eaa-9f43-64fd74cdee9e",
            "is_hitlog_enabled": false,
            "is_ipv6_traffic_allowed": false,
            "is_system_defined": false,
            "last_update_time": "2024-07-19T12:56:21.167000+00:00",
            "links": null,
            "name": "ansible-nsr-HqsWGHjQBsok2-updated",
            "rules": [
                {
                    "description": "inbound1",
                    "ext_id": "81ae70d1-d010-4c70-999f-bbeba03ce64e",
                    "links": null,
                    "spec": {
                        "secured_group_action": "ALLOW",
                        "secured_group_category_references": [
                            "569a018e-18ac-4813-b00f-2aa0d0005042"
                        ]
                    },
                    "tenant_id": null,
                    "type": "INTRA_GROUP"
                },
                {
                    "description": "inbound4_updated",
                    "ext_id": "fb6860d5-bb3e-45ba-871f-4870474b5430",
                    "links": null,
                    "spec": {
                        "dest_address_group_references": null,
                        "dest_allow_spec": null,
                        "dest_category_references": null,
                        "dest_subnet": null,
                        "icmp_services": null,
                        "is_all_protocol_allowed": null,
                        "network_function_chain_reference": null,
                        "secured_group_category_references": [
                            "569a018e-18ac-4813-b00f-2aa0d0005042"
                        ],
                        "service_group_references": [
                            "f77c1342-95e4-411e-9281-42ef2123d5b1"
                        ],
                        "src_address_group_references": null,
                        "src_allow_spec": null,
                        "src_category_references": null,
                        "src_subnet": {
                            "prefix_length": 24,
                            "value": "10.0.1.0"
                        },
                        "tcp_services": null,
                        "udp_services": null
                    },
                    "tenant_id": null,
                    "type": "APPLICATION"
                },
                {
                    "description": "outbound1",
                    "ext_id": "fc9ad075-24a0-42a7-9977-2d9df462227d",
                    "links": null,
                    "spec": {
                        "dest_address_group_references": null,
                        "dest_allow_spec": null,
                        "dest_category_references": null,
                        "dest_subnet": {
                            "prefix_length": 24,
                            "value": "10.0.1.0"
                        },
                        "icmp_services": null,
                        "is_all_protocol_allowed": true,
                        "network_function_chain_reference": null,
                        "secured_group_category_references": [
                            "569a018e-18ac-4813-b00f-2aa0d0005042"
                        ],
                        "service_group_references": null,
                        "src_address_group_references": null,
                        "src_allow_spec": null,
                        "src_category_references": null,
                        "src_subnet": null,
                        "tcp_services": null,
                        "udp_services": null
                    },
                    "tenant_id": null,
                    "type": "APPLICATION"
                }
            ],
            "scope": "ALL_VLAN",
            "secured_groups": null,
            "state": "MONITOR",
            "tenant_id": null,
            "type": "APPLICATION",
            "vpc_references": null
        }
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching network security policy info"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false
ext_id:
    description: External id of the network security policy if fetched by ext_id
    returned: always
    type: str
    sample: "e8347a03-28a0-4eaa-9f43-64fd74cdee9e"
total_available_results:
    description:
        - The total number of available network security policies in PC.
    type: int
    returned: when all network security policies are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_network_security_policy_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_network_security_policy(module, result):
    network_security_policies = get_network_security_policy_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = network_security_policies.get_network_security_policy_by_id(ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network security policy info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_network_security_policies(module, result):
    network_security_policies = get_network_security_policy_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating network security policies info Spec", **result
        )

    try:
        resp = network_security_policies.list_network_security_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network security policies info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        support_proxy=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_network_security_policy(module, result)
    else:
        get_network_security_policies(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
