#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_plans_info
short_description: recovery plan info module
version_added: 1.5.0
description: 'Get recovery plan info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: recovery_plan
    plan_uuid:
        description:
            - recovery plan UUID
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
- name: List all recovery plans
  ntnx_recovery_plans_info:
    nutanix_host: "{{ recovery_site_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
  register: result

- name: List recovery plans using uuid criteria
  ntnx_recovery_plans_info:
    nutanix_host: "{{ recovery_site_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
    plan_uuid: "{{ plan_uuid }}"
  register: result
"""
RETURN = r"""
associated_entities:
  description:
    - associated entities to recovery plan
    - only obtained when uuid is used for getting info of recovery plan
  returned: always
  type: dict
  sample: {
                "entities_per_availability_zone_list": [
                    {
                        "availability_zone_order_list": [
                            {
                                "availability_zone_list": [
                                    {
                                        "availability_zone_url": "az1-url"
                                    },
                                    {
                                        "availability_zone_url": "az2-url"
                                    }
                                ]
                            }
                        ],
                        "availability_zone_url": "az1-url",
                        "entity_list": [
                            {
                                "any_entity_reference": {
                                    "kind": "vm",
                                    "name": "test-check-63",
                                    "uuid": "da240e012e-d099-4acd-a8b0-ee33f4d45a25"
                                },
                                "is_recovery_point": false,
                                "recovery_availability_zone_order_index": 0
                            },
                            {
                                "any_entity_reference": {
                                    "kind": "vm",
                                    "name": "integration_test_dr_vm",
                                    "uuid": "da76qwe13-4ad0-4231-b376-16b3fa2da0cf"
                                },
                                "is_recovery_point": true,
                                "recovery_availability_zone_order_index": 0
                            },
                            {
                                "any_entity_reference": {
                                    "kind": "vm",
                                    "name": "integration_test_dr_vm",
                                    "uuid": "da76qwe13-4ad0-4231-b376-16b3fa2da0cf"
                                },
                                "is_recovery_point": false,
                                "recovery_availability_zone_order_index": 0
                            }
                        ]
                    }
                ]
            }
recovery_plan_info:
  description:
    - recovery plan intent response
    - only obtained when uuid is used for getting info of recovery plan
  returned: always
  type: dict
  sample: {
                "api_version": "3.1",
                "metadata": {
                    "categories": {},
                    "categories_mapping": {},
                    "creation_time": "2022-08-26T11:16:33Z",
                    "kind": "recovery_plan",
                    "last_update_time": "2022-08-26T11:16:48Z",
                    "owner_reference": {
                        "kind": "user",
                        "name": "admin",
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec_hash": "00000000000000000000000000000000000000000000000000",
                    "spec_version": 1,
                    "uuid": "4312fc47-6d3a-44df-bb64-d17e095203f2"
                },
                "spec": {
                    "description": "recovery plan desc updated",
                    "name": "example-rp-updated",
                    "resources": {
                        "parameters": {
                            "availability_zone_list": [
                                {
                                    "availability_zone_url": "az1-url"
                                },
                                {
                                    "availability_zone_url": "az2-url"
                                }
                            ],
                            "network_mapping_list": [
                                {
                                    "are_networks_stretched": false,
                                    "availability_zone_network_mapping_list": [
                                        {
                                            "availability_zone_url": "az1-url",
                                            "recovery_network": {
                                                "name": "vlan1"
                                            },
                                            "test_network": {
                                                "name": "vlan1"
                                            }
                                        },
                                        {
                                            "availability_zone_url": "az2-url",
                                            "recovery_network": {
                                                "name": "vlan1"
                                            },
                                            "test_network": {
                                                "name": "vlan2"
                                            }
                                        }
                                    ]
                                }
                            ],
                            "primary_location_index": 0
                        },
                        "stage_list": [
                            {
                                "delay_time_secs": 2,
                                "stage_uuid": "da6a7469-2b6a-4b69-a181-53814fb08e0b",
                                "stage_work": {
                                    "recover_entities": {
                                        "entity_info_list": [
                                            {
                                                "any_entity_reference": {
                                                    "kind": "vm",
                                                    "name": "test-check",
                                                    "uuid": "asdsadsd-7c0e-4214-9785-6949a2c7369a"
                                                },
                                                "script_list": [
                                                    {
                                                        "enable_script_exec": true
                                                    }
                                                ]
                                            },
                                            {
                                                "categories": {
                                                    "Environment": "Staging"
                                                },
                                                "script_list": [
                                                    {
                                                        "enable_script_exec": true
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "stage_uuid": "ad914f0a-1ec3-4eb1-a8ce-ce6de230477f",
                                "stage_work": {
                                    "recover_entities": {
                                        "entity_info_list": [
                                            {
                                                "categories": {
                                                    "Environment": "Dev"
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                },
                "status": {
                    "description": "recovery plan desc updated",
                    "execution_context": {
                        "task_uuid": [
                            "946336ac-9ee9-4df2-bfe2-7e9ff4f3ce25"
                        ]
                    },
                    "latest_test_time": "",
                    "latest_validation_time": "",
                    "name": "example-rp-updated",
                    "recovery_availability_zone_order_list": [
                        {
                            "availability_zone_order_list": [
                                [
                                    {
                                        "availability_zone_url": "az1-url"
                                    },
                                    {
                                        "availability_zone_url": "az2-url"
                                    }
                                ]
                            ],
                            "availability_zone_url": "az1-url"
                        }
                    ],
                    "resources": {
                        "parameters": {
                            "availability_zone_list": [
                                {
                                    "availability_zone_url": "az1-url"
                                },
                                {
                                    "availability_zone_url": "az2-url"
                                }
                            ],
                            "network_mapping_list": [
                                {
                                    "are_networks_stretched": false,
                                    "availability_zone_network_mapping_list": [
                                        {
                                            "availability_zone_url": "az1-url",
                                            "recovery_network": {
                                                "name": "vlan1"
                                            },
                                            "test_network": {
                                                "name": "vlan1"
                                            }
                                        },
                                        {
                                            "availability_zone_url": "az2-url",
                                            "recovery_network": {
                                                "name": "vlan1"
                                            },
                                            "test_network": {
                                                "name": "vlan1"
                                            }
                                        }
                                    ]
                                }
                            ],
                            "primary_location_index": 0
                        },
                        "stage_list": [
                            {
                                "delay_time_secs": 2,
                                "stage_uuid": "da6a7469-2b6a-4b69-a181-53814fb08e0b",
                                "stage_work": {
                                    "recover_entities": {
                                        "entity_info_list": [
                                            {
                                                "any_entity_reference": {
                                                    "kind": "vm",
                                                    "name": "test-check",
                                                    "uuid": "asasda-7c0e-4214-9785-6949a2c7369a"
                                                },
                                                "script_list": [
                                                    {
                                                        "enable_script_exec": true
                                                    }
                                                ]
                                            },
                                            {
                                                "categories": {
                                                    "Environment": "Staging"
                                                },
                                                "script_list": [
                                                    {
                                                        "enable_script_exec": true
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "stage_uuid": "ad914f0a-1ec3-4eb1-a8ce-ce6de230477f",
                                "stage_work": {
                                    "recover_entities": {
                                        "entity_info_list": [
                                            {
                                                "categories": {
                                                    "Environment": "Dev"
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        ]
                    },
                    "state": "COMPLETE"
                }
            }
"""


from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.recovery_plans import RecoveryPlan  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        plan_uuid=dict(type="str"),
        kind=dict(type="str", default="recovery_plan"),
        sort_order=dict(type="str", choices=["ASCENDING", "DESCENDING"]),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_recovery_plan(module, result):
    recovery_plan = RecoveryPlan(module)
    uuid = module.params.get("plan_uuid")
    resp = recovery_plan.read(uuid)

    # get all associated entities
    associated_entities = recovery_plan.get_associated_entities(uuid)

    result["response"] = {
        "recovery_plan_info": resp,
        "associated_entities": associated_entities,
    }


def get_recovery_plans(module, result):
    recovery_plan = RecoveryPlan(module)
    spec, error = recovery_plan.get_info_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating recovery plan info spec", **result)
    resp = recovery_plan.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("plan_uuid"):
        get_recovery_plan(module, result)
    else:
        get_recovery_plans(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
