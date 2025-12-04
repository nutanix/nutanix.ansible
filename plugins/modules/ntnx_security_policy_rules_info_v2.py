#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_policy_rules_info_v2
short_description: Fetch network security policy rulesinfo from Nutanix PC.
version_added: 2.5.0
description:
    - Fetch specific network security policy rules info by policy_ext_id.
options:
    policy_ext_id:
        description:
            - External id to fetch specific network security policy rules info.
        type: str
        required: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all security policy rules
  nutanix.ncp.ntnx_security_policy_rules_info_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    validate_certs: false
    policy_ext_id: "e8347a03-28a0-4eaa-9f43-64fd74cdee9e"
  register: result
  ignore_errors: true

- name: List security policy rules using filter
  nutanix.ncp.ntnx_security_policy_rules_info_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    validate_certs: false
    policy_ext_id: "e8347a03-28a0-4eaa-9f43-64fd74cdee9e"
    filter: "type eq Microseg.Config.RuleType'INTRA_GROUP'"
  register: result
  ignore_errors: true

- name: List security policy rules using limit
  nutanix.ncp.ntnx_security_policy_rules_info_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    validate_certs: false
    policy_ext_id: "e8347a03-28a0-4eaa-9f43-64fd74cdee9e"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - List of network security policy rules
  returned: always
  type: dict
  sample:
    [
        {
            "description": "outbound1",
            "ext_id": "1e77e030-ba4b-424b-8c58-b6ec7261287a",
            "links": null,
            "spec": {
                "dest_address_group_references": null,
                "dest_allow_spec": "ALL",
                "dest_category_associated_entity_type": null,
                "dest_category_references": null,
                "dest_entity_group_reference": null,
                "dest_subnet": null,
                "icmp_services": null,
                "is_all_protocol_allowed": true,
                "network_function_chain_reference": null,
                "network_function_reference": null,
                "secured_group_category_associated_entity_type": "VM",
                "secured_group_category_references": [
                    "1d082287-b1b3-4ea1-591a-628b2a601591",
                    "658fbe2f-0026-41a1-6863-2122fef794c6"
                ],
                "secured_group_entity_group_reference": null,
                "service_group_references": null,
                "src_address_group_references": null,
                "src_allow_spec": null,
                "src_category_associated_entity_type": null,
                "src_category_references": null,
                "src_entity_group_reference": null,
                "src_subnet": null,
                "tcp_services": null,
                "udp_services": null
            },
            "tenant_id": null,
            "type": "APPLICATION"
        }
    ]

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

policy_ext_id:
    description: External id of the network security policy rule
    returned: always
    type: str
    sample: "e8347a03-28a0-4eaa-9f43-64fd74cdee9e"

total_available_results:
    description:
        - The total number of available network security policy rules in PC.
    type: int
    returned: when all network security policy rules are fetched
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
        policy_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_network_security_policy_rules(module, result):
    policy_ext_id = module.params.get("policy_ext_id")
    result["policy_ext_id"] = policy_ext_id
    network_security_policies = get_network_security_policy_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating network security policy rules info Spec", **result
        )

    try:
        resp = network_security_policies.list_network_security_policy_rules(
            policyExtId=policy_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network security policy rules info",
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
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    get_network_security_policy_rules(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
