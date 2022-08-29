#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: ntnx_protection_rules_info
short_description: protection rule info module
version_added: 1.5.0
description: 'Get protection rule  info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: protection_rule
    rule_uuid:
        description:
            - protection rule UUID
        type: str
    sort_order:
        description:
            - The sort order in which results are returned
        type: str
        choices: ["ASCENDING", "DESCENDING"]
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""

- name: List all Protection rules
  ntnx_protection_rules_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
  register: result
  ignore_errors: True

- name: List protection rule using uuid criteria
  ntnx_protection_rules_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
    rule_uuid: "{{ test_rule_uuid }}"
  register: result

"""
RETURN = r"""
rule_affected_entities:
  description:
    - affected entities to protection policy
    - only obtained when uuid is used for getting info of protection policy
  returned: always
  type: dict
  sample: {
                "entity_list": [
                    {
                        "vm_reference": {
                            "kind": "vm",
                            "name": "test-check",
                            "uuid": "asdasds-490b-498a-a51c-2a13c38582cc"
                        }
                    }
                ]
            }
rule_info:
  description:
    - intent response of protection policy
    - only obtained when uuid is used for getting info of protection policy
  returned: always
  type: dict
  sample: {
                "api_version": "3.1",
                "metadata": {
                    "categories": {},
                    "categories_mapping": {},
                    "creation_time": "2022-08-26T10:56:08Z",
                    "kind": "protection_rule",
                    "last_update_time": "2022-08-26T12:02:42Z",
                    "owner_reference": {
                        "kind": "user",
                        "name": "admin",
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec_hash": "00000000000000000000000000000000000000000000000000",
                    "spec_version": 1,
                    "uuid": "asdasasdda-7a99-43ea-b49e-9120f955a518"
                },
                "spec": {
                    "name": "test-check",
                    "resources": {
                        "availability_zone_connectivity_list": [
                            {
                                "destination_availability_zone_index": 1,
                                "snapshot_schedule_list": [
                                    {
                                        "local_snapshot_retention_policy": {
                                            "num_snapshots": 1
                                        },
                                        "recovery_point_objective_secs": 3600,
                                        "remote_snapshot_retention_policy": {
                                            "num_snapshots": 1
                                        },
                                        "snapshot_type": "CRASH_CONSISTENT"
                                    }
                                ],
                                "source_availability_zone_index": 0
                            },
                            {
                                "destination_availability_zone_index": 0,
                                "snapshot_schedule_list": [
                                    {
                                        "local_snapshot_retention_policy": {
                                            "num_snapshots": 1
                                        },
                                        "recovery_point_objective_secs": 3600,
                                        "remote_snapshot_retention_policy": {
                                            "num_snapshots": 1
                                        },
                                        "snapshot_type": "CRASH_CONSISTENT"
                                    }
                                ],
                                "source_availability_zone_index": 1
                            }
                        ],
                        "category_filter": {
                            "params": {
                                "Environment": [
                                    "Staging"
                                ]
                            },
                            "type": "CATEGORIES_MATCH_ANY"
                        },
                        "ordered_availability_zone_list": [
                            {
                                "availability_zone_url": "az1-url",
                                "cluster_uuid": "c1uuid"
                            },
                            {
                                "availability_zone_url": "az2-url",
                                "cluster_uuid": "c2uuid"
                            }
                        ],
                        "primary_location_list": [
                            0
                        ]
                    }
                },
                "status": {
                    "description": "",
                    "execution_context": {
                        "task_uuid": [
                            "asdasd-8d8d-4dc9-87ad-5e66530bcfab"
                        ]
                    },
                    "name": "test-check",
                    "resources": {
                        "availability_zone_connectivity_list": [
                            {
                                "destination_availability_zone_index": 1,
                                "snapshot_schedule_list": [
                                    {
                                        "local_snapshot_retention_policy": {
                                            "num_snapshots": 1
                                        },
                                        "recovery_point_objective_secs": 3600,
                                        "remote_snapshot_retention_policy": {
                                            "num_snapshots": 1
                                        },
                                        "snapshot_type": "CRASH_CONSISTENT"
                                    }
                                ],
                                "source_availability_zone_index": 0
                            },
                            {
                                "destination_availability_zone_index": 0,
                                "snapshot_schedule_list": [
                                    {
                                        "local_snapshot_retention_policy": {
                                            "num_snapshots": 1
                                        },
                                        "recovery_point_objective_secs": 3600,
                                        "remote_snapshot_retention_policy": {
                                            "num_snapshots": 1
                                        },
                                        "snapshot_type": "CRASH_CONSISTENT"
                                    }
                                ],
                                "source_availability_zone_index": 1
                            }
                        ],
                        "category_filter": {
                            "params": {
                                "Environment": [
                                    "Staging"
                                ]
                            },
                            "type": "CATEGORIES_MATCH_ANY"
                        },
                        "ordered_availability_zone_list": [
                            {
                                "availability_zone_url": "az1-url",
                                "cluster_uuid": "c1uuid"
                            },
                            {
                                "availability_zone_url": "az2-url",
                                "cluster_uuid": "c2uuid"
                            }
                        ],
                        "primary_location_list": [
                            0
                        ],
                        "start_time": ""
                    },
                    "state": "COMPLETE"
                }
            }
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.protection_rules import ProtectionRule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        rule_uuid=dict(type="str"),
        kind=dict(type="str", default="protection_rule"),
        sort_order=dict(type="str", choices=["ASCENDING", "DESCENDING"]),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_protection_rule(module, result):
    protection_rule = ProtectionRule(module)
    rule_uuid = module.params.get("rule_uuid")
    resp = protection_rule.read(rule_uuid)

    # get all affected entities
    affected_entities = protection_rule.get_affected_entities(rule_uuid)

    result["response"] = {
        "rule_info": resp,
        "rule_affected_entities": affected_entities,
    }


def get_protection_rules(module, result):
    protection_rule = ProtectionRule(module)
    spec, error = protection_rule.get_info_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating protection rules info spec", **result)
    resp = protection_rule.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("rule_uuid"):
        get_protection_rule(module, result)
    else:
        get_protection_rules(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
