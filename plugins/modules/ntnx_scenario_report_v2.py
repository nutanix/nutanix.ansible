#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_scenario_report_v2
short_description: Generate a capacity planning scenario report in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module triggers the generation of a capacity planning scenario report in Nutanix Prism Central.
  - Report generation is asynchronous. When C(wait) is C(true) (default) the module waits for the
    underlying task to complete before returning.
  - Use M(nutanix.ncp.ntnx_scenario_reports_info_v2) to download the generated PDF report afterwards.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Generate a scenario report) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported; the module triggers report generation for the given scenario.
        type: str
        choices:
            - present
        default: present
    scenario_ext_id:
        description:
            - The external ID (UUID) of the capacity planning scenario for which to generate the report.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - George Ghawali (@george-ghawali)
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Generate report for a capacity planning scenario
  nutanix.ncp.ntnx_scenario_report_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    scenario_ext_id: "b1d6e7cc-1234-4b56-8ce0-8c19d7c8f0a1"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for triggering scenario report generation.
        - Task details (final status) when C(wait) is C(true).
        - Initial TaskReference dict (containing the task ext_id) when C(wait) is C(false).
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2026-07-21T08:20:14.512381+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T08:20:03.101002+00:00",
            "entities_affected": [
                {
                    "ext_id": "b1d6e7cc-1234-4b56-8ce0-8c19d7c8f0a1",
                    "rel": "aiops:config:scenario"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T08:20:14.512381+00:00",
            "legacy_error_message": null,
            "operation": "GenerateScenarioReport",
            "operation_description": "Generate a capacity planning scenario report",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T08:20:03.130000+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: Whether the task resulted in any changes on the server.
    returned: always
    type: bool
    sample: true

msg:
    description: Message describing the outcome (error / info).
    returned: When there is an error
    type: str
    sample: "Api Exception raised while generating scenario report"

error:
    description: Error details if the operation failed.
    returned: when an error occurs
    type: str
    sample: "Failed to generate report for scenario ext_id"

failed:
    description: Whether the task failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the underlying report-generation task.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the capacity planning scenario.
    returned: always
    type: str
    sample: "b1d6e7cc-1234-4b56-8ce0-8c19d7c8f0a1"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import get_scenarios_api_instance  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_aiops_py_client  # noqa: F401,E402  pylint: disable=unused-import
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: F401,E402  pylint: disable=unused-import
        mock_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        scenario_ext_id=dict(type="str", required=True),
    )
    return module_args


def generate_scenario_report(module, api_instance, result):
    scenario_ext_id = module.params.get("scenario_ext_id")
    result["ext_id"] = scenario_ext_id

    if module.check_mode:
        result["msg"] = (
            "Report generation for scenario ext_id:{0} would be triggered.".format(
                scenario_ext_id
            )
        )
        return

    try:
        resp = api_instance.generate_report(extId=scenario_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while generating scenario report",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_aiops_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }
    api_instance = get_scenarios_api_instance(module)
    generate_scenario_report(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
