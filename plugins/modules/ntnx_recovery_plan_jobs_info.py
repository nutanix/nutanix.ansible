#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: ntnx_recovery_plan_jobs_info
short_description: recovery plan jobs info module
version_added: 1.5.0
description: 'Get recovery plan jobs info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: recovery_plan_job
    job_uuid:
        description:
            - recovery plan job  UUID
        type: str
    sort_order:
        description:
            - The sort order in which results are returned
        type: str
        choices: ["ASCENDING", "DESCENDING"]
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
      - nutanix.ncp.ntnx_logger
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""

- name: List all recovery plan jobs
  ntnx_recovery_plan_jobs_info:
    nutanix_host: "{{ recovery_site_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
  register: result
  ignore_errors: true

- name: List recovery plan job using uuid criteria
  ntnx_recovery_plan_jobs_info:
    nutanix_host: "{{ recovery_site_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
    job_uuid: "{{ job_uuid }}"
  register: result
"""
RETURN = r"""
api_version:
  description:
    - API Version of the Nutanix v3 API framework.
    - only when when job info is obtained using uuid
  returned: always
  type: str
  sample: "3.1"
metadata:
  description:
    - The recovery plan jobs's kind metadata
    - only when when job info is obtained using uuid
  returned: always
  type: dict
  sample: {
                "kind": "recovery_plan_job",
                "name": "test-failover-123",
                "uuid": "adasds-d541-4df8-ab0e-53b2b62519b3"
            }
status:
  description:
    - An intentful job and its execution status of a recovery plan job
    - only when when job info is obtained using uuid
  returned: always
  type: dict
  sample: {
                "end_time": "2022-08-26T11:35:49Z",
                "execution_status": {
                    "operation_status": {
                        "percentage_complete": 100,
                        "status": "COMPLETED"
                    },
                    "percentage_complete": 100,
                    "postprocessing_status": {
                        "percentage_complete": 100,
                        "status": "COMPLETED"
                    },
                    "preprocessing_status": {
                        "percentage_complete": 100,
                        "status": "COMPLETED"
                    },
                    "status": "COMPLETED_WITH_WARNING"
                },
                "name": "test-failover-123",
                "recovery_plan_specification": {
                    "description": "recovery plan desc updated",
                    "name": "example-rp-updated",
                    "resources": {
                        "parameters": {
                            "availability_zone_list": [
                                {
                                    "availability_zone_url": "az1-url"
                                },
                                {
                                    "availability_zone_url":"az2-url"
                                }
                            ],
                            "network_mapping_list": [
                                {
                                    "are_networks_stretched": false,
                                    "availability_zone_network_mapping_list": [
                                        {
                                            "availability_zone_url": "az1-url",
                                            "recovery_network": {
                                                "name": "vlan"
                                            },
                                            "test_network": {
                                                "name": "vlan"
                                            }
                                        },
                                        {
                                            "availability_zone_url":"az2-url",
                                            "recovery_network": {
                                                "name": "vlan"
                                            },
                                            "test_network": {
                                                "name": "vlan"
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
                                "stage_uuid": "3aa0a257-ca5d-4a17-b19f-36918cfa7dd0",
                                "stage_work": {
                                    "recover_entities": {
                                        "entity_info_list": [
                                            {
                                                "any_entity_reference": {
                                                    "kind": "vm",
                                                    "name": "test-check",
                                                    "uuid": "asdasds-490b-498a-a51c-2a13c38582cc"
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
                                "stage_uuid": "e9bb2595-9bc7-4630-a87c-8499203d8c23",
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
                "resources": {
                    "execution_parameters": {
                        "action_type": "MIGRATE",
                        "failed_availability_zone_list": [
                            {
                                "availability_zone_url": "az1-url"
                            }
                        ],
                        "recovery_availability_zone_list": [
                            {
                                "availability_zone_url":"az2-url"
                            }
                        ]
                    },
                    "recovery_plan_reference": {
                        "kind": "recovery_plan",
                        "uuid": "adasdsd-9afe-477d-90c3-8cd6bec88b2d"
                    }
                },
                "start_time": "2022-08-26T11:33:51Z",
                "validation_information": {
                    "errors_list": [],
                    "warnings_list": [
                        {
                            "affected_any_reference_list": [
                                {
                                    "kind": "vm",
                                    "name": "test-check",
                                    "uuid": "asdasds-490b-498a-a51c-2a13c38582cc"
                                }
                            ],
                            "cause_and_resolution_message_list": [
                                {
                                    "cause": "VMs are unprotected.",
                                    "resolution_list": ["xx", "xx"]
                                }
                            ],
                            "impact_message_list": ["xx", "xx"],
                            "message": "xyz",
                            "validation_type": "ENTITY"
                        },
                        {
                            "affected_any_reference_list": [
                                {
                                    "kind": "vm",
                                    "name": "test-check",
                                    "uuid": "dasdadasd-490b-498a-a51c-2a13c38582cc"
                                }
                            ],
                            "cause_and_resolution_message_list": [
                                {
                                    "cause": "xyz",
                                    "resolution_list": ["xx", "xx"]
                                }
                            ],
                            "impact_message_list": [
                                "The post recovery script execution will fail."
                            ],
                            "message": "xyz",
                            "validation_type": "ENTITY"
                        },
                        {
                            "affected_any_reference_list": [
                                {
                                    "kind": "vm",
                                    "name": "test-check",
                                    "uuid": "adssasd-490b-498a-a51c-2a13c38582cc"
                                }
                            ],
                            "cause_and_resolution_message_list": [
                                {
                                    "cause": "xyz",
                                    "resolution_list": ["xx", "xx"]
                                }
                            ],
                            "impact_message_list": [
                                "xyz"
                            ],
                            "message": "Duplicate instances exist for one or more of the entities in the Recovery Plan.",
                            "validation_type": "ENTITY"
                        },
                        {
                            "affected_any_reference_list": [],
                            "cause_and_resolution_message_list": [
                                {
                                    "cause": "xyz",
                                    "resolution_list": ["xx", "xx"]
                                }
                            ],
                            "impact_message_list": [
                                "No entity will be recovered for stage 2"
                            ],
                            "message": "No entity found for recovery for a stage 2.",
                            "validation_type": "ENTITY"
                        },
                        {
                            "affected_any_reference_list": [],
                            "cause_and_resolution_message_list": [
                                {
                                    "cause": "The categories might no longer be in use.",
                                    "resolution_list": ["xx", "xx"]
                                }
                            ],
                            "impact_message_list": [
                                "No entities will be recovered for these categories."
                            ],
                            "message": "xxxxxxx",
                            "validation_type": "CATEGORY"
                        }
                    ]
                }
            }
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v3.prism.recovery_plan_jobs import RecoveryPlanJob  # noqa: E402


def get_module_spec():

    module_args = dict(
        job_uuid=dict(type="str"),
        kind=dict(type="str", default="recovery_plan_job"),
        sort_order=dict(type="str", choices=["ASCENDING", "DESCENDING"]),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_recovery_plan_job(module, result):
    recovery_plan_job = RecoveryPlanJob(module)
    uuid = module.params.get("job_uuid")
    resp = recovery_plan_job.read(uuid)

    result["response"] = resp


def get_recovery_plan_jobs(module, result):
    recovery_plan_job = RecoveryPlanJob(module)
    spec, error = recovery_plan_job.get_info_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating recovery plan job info spec", **result)
    resp = recovery_plan_job.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("job_uuid"):
        get_recovery_plan_job(module, result)
    else:
        get_recovery_plan_jobs(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
