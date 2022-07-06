#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_rules_info
short_description: security_rule info module
version_added: 1.3.0
description: 'Get security_rule info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: network_security_rule
    security_rule_uuid:
      description:
        - security_rule UUID
      type: str
    sort_order:
        description:
        - The sort order in which results are returned
        type: str
        choices:
            - ASCENDING
            - DESCENDING
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
  - name: List security_rule using name filter criteria
    ntnx_security_rules_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
         name: "{{ security_rule.name }}"
      kind: security_rule
    register: result

  - name: List security_rule using length, offset, sort order and name sort attribute
    ntnx_security_rules_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      length: 1
      offset: 1
      sort_order: "ASCENDING"
      sort_attribute: "name"
    register: result
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: Metadata for security_rule_info list output
  returned: always
  type: dict
  sample: {
    "metadata": {
            "kind": "security_rule",
            "length": 1,
            "offset": 2,
            "sort_attribute": "name",
            "sort_order": "DESCENDING",
            "total_matches": 3
        } }
entities:
  description: security_rule intent response
  returned: always
  type: list
  sample: {
    "entities": [
                {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "creation_time": "2022-07-02T07:31:20Z",
                        "kind": "network_security_rule",
                        "last_update_time": "2022-07-02T07:31:22Z",
                        "owner_reference": {
                            "kind": "user",
                            "name": "admin",
                            "uuid": "00000000-0000-0000-0000-000000000000"
                        },
                        "spec_hash": "00000000000000000000000000000000000000000000000000",
                        "spec_version": 0,
                        "uuid": "734a569e-f43b-4b33-b71b-e3b5f1970a37"
                    },
                    "spec": {
                        "name": "isolation_test_rule",
                        "resources": {
                            "is_policy_hitlog_enabled": false,
                            "isolation_rule": {
                                "action": "MONITOR",
                                "first_entity_filter": {
                                    "kind_list": [
                                        "vm"
                                    ],
                                    "params": {
                                        "Environment": [
                                            "Dev"
                                        ]
                                    },
                                    "type": "CATEGORIES_MATCH_ALL"
                                },
                                "second_entity_filter": {
                                    "kind_list": [
                                        "vm"
                                    ],
                                    "params": {
                                        "Environment": [
                                            "Production"
                                        ]
                                    },
                                    "type": "CATEGORIES_MATCH_ALL"
                                }
                            }
                        }
                    },
                    "status": {
                        "description": null,
                        "execution_context": {
                            "task_uuid": [
                                "2b88bf1d-ed24-4bc0-a0eb-baecc4cae71f"
                            ]
                        },
                        "name": "isolation_test_rule",
                        "resources": {
                            "isolation_rule": {
                                "action": "MONITOR",
                                "first_entity_filter": {
                                    "kind_list": [
                                        "vm"
                                    ],
                                    "params": {
                                        "Environment": [
                                            "Dev"
                                        ]
                                    },
                                    "type": "CATEGORIES_MATCH_ALL"
                                },
                                "second_entity_filter": {
                                    "kind_list": [
                                        "vm"
                                    ],
                                    "params": {
                                        "Environment": [
                                            "Production"
                                        ]
                                    },
                                    "type": "CATEGORIES_MATCH_ALL"
                                }
                            }
                        },
                        "state": "COMPLETE"
                    }
                }
            ]
            }
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.security_rules import SecurityRule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        security_rule_uuid=dict(type="str"),
        kind=dict(type="str", default="network_security_rule"),
        sort_order=dict(type="str", choices=["ASCENDING", "DESCENDING"]),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_security_rule(module, result):
    security_rule = SecurityRule(module)
    security_rule_uuid = module.params.get("security_rule_uuid")
    resp = security_rule.read(security_rule_uuid)

    result["response"] = resp


def list_security_rule(module, result):
    security_rule = SecurityRule(module)
    spec, error = security_rule.get_info_spec()

    resp = security_rule.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("security_rule_uuid"):
        get_security_rule(module, result)
    else:
        list_security_rule(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
