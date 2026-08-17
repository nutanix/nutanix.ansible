#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_report_planned_capacity_v2
short_description: Generate a report for a planned capacity scenario in Nutanix Prism Central
version_added: 2.7.0
description:
    - This module allows you to trigger the generation of a report for a planned capacity scenario in Nutanix Prism Central.
    - The scenario must already exist and be referenced by its external ID.
    - The operation is asynchronous and returns a task reference which can be polled using the wait option.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Generate report for a planned capacity scenario) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported; when set the module triggers the report generation action.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - External ID (UUID) of the capacity planning scenario for which a report should be generated.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Generate a report for a planned capacity scenario
  nutanix.ncp.ntnx_report_planned_capacity_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "32459cae-43ca-4b6f-9bab-857895c1f867"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for generating a report for a planned capacity scenario.
        - Task details if C(wait) is true.
        - Task reference details if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
            ],
            "completed_time": "<need_to_add_sample>",
            "created_time": "<need_to_add_sample>",
            "entities_affected": [
                {
                    "ext_id": "32459cae-43ca-4b6f-9bab-857895c1f867",
                    "name": null,
                    "rel": "aiops:config:scenarios"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:be27ef78-d5aa-49a2-72c9-b090c4821780",
            "is_cancelable": false,
            "last_updated_time": "<need_to_add_sample>",
            "legacy_error_message": null,
            "operation": "GENERATE_SCENARIO_REPORT",
            "operation_description": "Generate report for a capacity planning scenario",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "<need_to_add_sample>",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

task_ext_id:
    description:
        - The external ID of the task that generates the report.
    returned: always
    type: str
    sample: "ZXJnb24=:be27ef78-d5aa-49a2-72c9-b090c4821780"

ext_id:
    description:
        - The external ID of the capacity planning scenario on which the report generation was triggered.
    returned: always
    type: str
    sample: "32459cae-43ca-4b6f-9bab-857895c1f867"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str
    sample: "Api Exception raised while generating report for capacity planning scenario"

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while generating report for capacity planning scenario"
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
    import ntnx_aiops_py_client as aiops_sdk  # noqa: F401
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as aiops_sdk  # noqa: F401

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
    )

    return module_args


def generate_report(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Report will be generated for capacity planning scenario "
            "with ext_id: {0}".format(ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.generate_report(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while generating report for capacity planning scenario",
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
    generate_report(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
