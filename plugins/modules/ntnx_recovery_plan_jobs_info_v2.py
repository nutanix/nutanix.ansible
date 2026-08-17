#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_plan_jobs_info_v2
short_description: Fetch Recovery Plan Jobs info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about RecoveryPlanJob in Nutanix Prism Central.
  - If C(ext_id) is provided and no sub-resource flag is set, fetch details of the specific RecoveryPlanJob.
  - If C(ext_id) is not provided, list multiple RecoveryPlanJob optionally filtered / paginated.
  - If C(ext_id) is provided together with C(fetch_execution_steps), list all execution steps of the given Recovery Plan Job.
  - If C(ext_id) is provided together with C(fetch_validation_errors), list all validation errors of the given Recovery Plan Job.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Get Recovery Plan Job by ext_id) -
      Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin,
      Prism Viewer, Super Admin
    - >-
      B(List Recovery Plan Jobs) -
      Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin,
      Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
    ext_id:
        description:
            - External ID of the Recovery Plan Job.
            - If provided, fetches the specific Recovery Plan Job (or its execution
              steps / validation errors when the corresponding flag is set).
        type: str
    fetch_execution_steps:
        description:
            - When true, list the execution steps of the Recovery Plan Job identified by C(ext_id).
            - Requires C(ext_id).
            - Mutually exclusive with C(fetch_validation_errors).
        type: bool
    fetch_validation_errors:
        description:
            - When true, list the validation errors of the Recovery Plan Job identified by C(ext_id).
            - Requires C(ext_id).
            - Mutually exclusive with C(fetch_execution_steps).
        type: bool
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - George Ghawali (@george-ghawali)
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch Recovery Plan Job using ext_id
  nutanix.ncp.ntnx_recovery_plan_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "0d9d8f39-2e6b-4a19-8d33-6a2bde7ac1f2"
  register: result
  ignore_errors: true

- name: List all Recovery Plan Jobs
  nutanix.ncp.ntnx_recovery_plan_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
  register: result
  ignore_errors: true

- name: List Recovery Plan Jobs with filter
  nutanix.ncp.ntnx_recovery_plan_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    filter: "actionType eq Nutanix.DataProtection.Config.RecoveryPlanActionType'VALIDATE'"
  register: result
  ignore_errors: true

- name: List Recovery Plan Jobs with limit
  nutanix.ncp.ntnx_recovery_plan_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    limit: 1
  register: result
  ignore_errors: true

- name: Fetch execution steps for a Recovery Plan Job
  nutanix.ncp.ntnx_recovery_plan_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "0d9d8f39-2e6b-4a19-8d33-6a2bde7ac1f2"
    fetch_execution_steps: true
  register: result
  ignore_errors: true

- name: Fetch validation errors for a Recovery Plan Job
  nutanix.ncp.ntnx_recovery_plan_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "0d9d8f39-2e6b-4a19-8d33-6a2bde7ac1f2"
    fetch_validation_errors: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC RecoveryPlanJob info v4 API.
        - It can be a single RecoveryPlanJob if external ID is provided.
        - List of multiple RecoveryPlanJob if external ID is not provided with optional filter or limit.
        - List of execution steps if C(fetch_execution_steps=true) with C(ext_id).
        - List of validation errors if C(fetch_validation_errors=true) with C(ext_id).
    returned: always
    type: dict
    sample:
        {
            "action_type": "VALIDATE",
            "end_time": "2026-07-21T07:12:35.000000+00:00",
            "execution_phases": [
                {
                    "phase": "VALIDATION",
                    "status": "SUCCEEDED"
                }
            ],
            "ext_id": "0d9d8f39-2e6b-4a19-8d33-6a2bde7ac1f2",
            "failover_directions": [
                {
                    "clusters": null,
                    "from_availability_zone": {
                        "cluster_ext_id": null,
                        "pc_ext_id": "1a5cb2c9-8b0f-49f2-b6bc-1234567890ab"
                    },
                    "to_availability_zone": {
                        "cluster_ext_id": null,
                        "pc_ext_id": "1a5cb2c9-8b0f-49f2-b6bc-abcdef123456"
                    }
                }
            ],
            "is_initiated_by_witness": false,
            "is_instant_restore": false,
            "is_live_migrate_v_ms": false,
            "links": null,
            "name": "test-validate-job",
            "owner_ext_id": "00000000-0000-0000-0000-000000000000",
            "percentage_complete": 100,
            "recovery_plan_ext_id": "9c3f2d54-b9dc-4b2a-89e5-1234567890ab",
            "recovery_reference_time": null,
            "start_time": "2026-07-21T07:12:32.000000+00:00",
            "status": "SUCCEEDED",
            "tenant_id": null,
            "validation_status": {
                "error_count": 0,
                "warning_count": 0
            }
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
    sample: "Api Exception raised while fetching recovery plan jobs info"

error:
    description: This field typically holds information about if the task has errors that occurred during execution.
    type: str
    returned: when an error occurs

failed:
    description: This field typically holds information about if the task has failed.
    returned: always
    type: bool
    sample: false

ext_id:
    description: External ID of the Recovery Plan Job.
    type: str
    returned: when external ID is provided
    sample: "0d9d8f39-2e6b-4a19-8d33-6a2bde7ac1f2"

total_available_results:
    description: The total number of available Recovery Plan Jobs (or sub-resources) in PC.
    type: int
    returned: when a list operation is performed
    sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_plan_jobs_api_instance,
)
from ..module_utils.v4.data_protection.helpers import (  # noqa: E402
    get_recovery_plan_job,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        fetch_execution_steps=dict(type="bool"),
        fetch_validation_errors=dict(type="bool"),
    )
    return module_args


def get_recovery_plan_job_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_recovery_plan_job(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_recovery_plan_jobs(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating recovery plan jobs info spec", **result)

    try:
        resp = api_instance.list_recovery_plan_jobs(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recovery plan jobs info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def list_recovery_plan_job_execution_steps(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating recovery plan job execution steps info spec",
            **result,
        )

    try:
        resp = api_instance.list_execution_steps_by_recovery_plan_job_id(
            recoveryPlanJobExtId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recovery plan job execution steps",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def list_recovery_plan_job_validation_errors(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating recovery plan job validation errors info spec",
            **result,
        )

    try:
        resp = api_instance.list_validation_errors_by_recovery_plan_job_id(
            recoveryPlanJobExtId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recovery plan job validation errors",
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
            ("fetch_execution_steps", "fetch_validation_errors"),
        ],
        required_if=[
            ("fetch_execution_steps", True, ("ext_id",)),
            ("fetch_validation_errors", True, ("ext_id",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_recovery_plan_jobs_api_instance(module)

    ext_id = module.params.get("ext_id")
    fetch_steps = module.params.get("fetch_execution_steps")
    fetch_errors = module.params.get("fetch_validation_errors")

    if ext_id and fetch_steps:
        list_recovery_plan_job_execution_steps(module, api_instance, result)
    elif ext_id and fetch_errors:
        list_recovery_plan_job_validation_errors(module, api_instance, result)
    elif ext_id:
        get_recovery_plan_job_using_ext_id(module, api_instance, result)
    else:
        list_recovery_plan_jobs(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
