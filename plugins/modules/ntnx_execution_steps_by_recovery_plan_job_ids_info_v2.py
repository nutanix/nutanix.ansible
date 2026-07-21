#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_execution_steps_by_recovery_plan_job_ids_info_v2
short_description: Fetch execution steps of a recovery plan job in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ExecutionStepsByRecoveryPlanJobId in Nutanix Prism Central.
  - Use this module to list the granular execution steps of a specific recovery plan job.
  - The C(recovery_plan_job_ext_id) is mandatory and identifies the parent recovery plan job whose execution steps should be listed.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List Recovery Plan Job Execution Steps) -
    Required Roles: Internal Super Admin, Prism Admin, Self-Service Admin, Super Admin, Disaster Recovery Admin, Project Manager,
    Prism Viewer, Disaster Recovery Viewer, NCM Connector, Project Admin, Tenant Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
  recovery_plan_job_ext_id:
    description:
      - The external identifier of the recovery plan job whose execution steps should be listed.
    type: str
    required: true
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
- name: List all execution steps of a recovery plan job
  nutanix.ncp.ntnx_execution_steps_by_recovery_plan_job_ids_info_v2:
    recovery_plan_job_ext_id: "8c80727e-8fd7-4c00-83c7-ef0e55b7b236"
  register: result
  ignore_errors: true

- name: List execution steps of a recovery plan job with limit
  nutanix.ncp.ntnx_execution_steps_by_recovery_plan_job_ids_info_v2:
    recovery_plan_job_ext_id: "8c80727e-8fd7-4c00-83c7-ef0e55b7b236"
    limit: 5
  register: result
  ignore_errors: true

- name: List execution steps of a recovery plan job ordered by start time descending
  nutanix.ncp.ntnx_execution_steps_by_recovery_plan_job_ids_info_v2:
    recovery_plan_job_ext_id: "8c80727e-8fd7-4c00-83c7-ef0e55b7b236"
    orderby: "startTime desc"
  register: result
  ignore_errors: true

- name: List execution steps of a recovery plan job with page and limit
  nutanix.ncp.ntnx_execution_steps_by_recovery_plan_job_ids_info_v2:
    recovery_plan_job_ext_id: "8c80727e-8fd7-4c00-83c7-ef0e55b7b236"
    page: 0
    limit: 5
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ExecutionStepsByRecoveryPlanJobId info v4 API.
    - List of multiple ExecutionStepsByRecoveryPlanJobId for the given recovery plan job with optional filter, limit, page or orderby.
  returned: always
  type: dict
  sample:
    [
      {
        "affected_entities": null,
        "end_time": "2026-07-21T06:12:11.031000+00:00",
        "error_message": null,
        "execution_step_results": null,
        "ext_id": "8c80727e-8fd7-4c00-83c7-ef0e55b7b236:step-1",
        "links": null,
        "operation_type": "VALIDATE",
        "percentage_complete": 100,
        "phase": "PRE_PROCESSING",
        "stage_ext_id": null,
        "start_time": "2026-07-21T06:12:01.512000+00:00",
        "status": "COMPLETED",
        "step_description": "Validate the recovery plan and target cluster",
        "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

recovery_plan_job_ext_id:
  description: The external ID of the recovery plan job whose execution steps were fetched.
  returned: always
  type: str
  sample: "8c80727e-8fd7-4c00-83c7-ef0e55b7b236"

total_available_results:
  description: The total number of available execution steps for the recovery plan job in PC.
  type: int
  returned: when all execution steps are fetched
  sample: 12

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching execution steps of recovery plan job"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs
  sample: null

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_plan_jobs_api_instance,
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
        recovery_plan_job_ext_id=dict(type="str", required=True),
    )
    return module_args


def list_execution_steps(module, api_instance, result):
    recovery_plan_job_ext_id = module.params.get("recovery_plan_job_ext_id")
    result["recovery_plan_job_ext_id"] = recovery_plan_job_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating execution steps info Spec", **result)

    try:
        resp = api_instance.list_execution_steps_by_recovery_plan_job_id(
            recoveryPlanJobExtId=recovery_plan_job_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching execution steps of recovery plan job",
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
    api_instance = get_recovery_plan_jobs_api_instance(module)
    list_execution_steps(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
