#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_runway_v2
short_description: Generate the capacity planning runway for a scenario in Nutanix Prism Central
version_added: 2.7.0
description:
    - Trigger asynchronous generation of the capacity planning runway for an
      existing capacity planning scenario in Nutanix Prism Central AIOps.
    - The Runway feature forecasts how many days a cluster can sustain its
      existing (and simulated) workloads before running out of CPU, memory,
      or storage effective capacity.
    - The API dispatches an Ergon task which recalculates the runway using
      the X-FIT machine-learning engine and stores the new runway payload on
      the scenario. When C(wait) is true, this module waits for the task to
      complete and returns the final task/scenario response.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Generate runway for a capacity planning scenario) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will trigger runway
              generation for the scenario identified by C(ext_id).
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - External ID (UUID) of the capacity planning scenario for which
              the runway should be generated.
            - Required for the operation.
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
- name: Generate runway for a capacity planning scenario
  nutanix.ncp.ntnx_runway_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "5b3d1f7c-2b6a-4b64-8b6a-1b0a5f3d8e4c"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for the generate-runway action on a capacity planning scenario.
        - When C(wait) is true, this contains the final task details.
        - When C(wait) is false, this contains the initial task reference returned by the API.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-21T11:35:47.501181+00:00",
            "created_time": "2026-07-21T11:35:44.212934+00:00",
            "entities_affected": [
                {
                    "ext_id": "5b3d1f7c-2b6a-4b64-8b6a-1b0a5f3d8e4c",
                    "rel": "aiops:config:scenario"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:8b2fbf4e-8d47-4c26-9df5-63cf8d1af51a",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T11:35:47.501181+00:00",
            "legacy_error_message": null,
            "operation": "GenerateRunway",
            "operation_description": "Generate runway for a capacity planning scenario",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T11:35:44.284002+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error or check mode is used
    type: str
    sample: "Api Exception raised while generating runway for capacity planning scenario"

error:
    description: This field typically holds information about any error that occurred during task execution.
    returned: When an error occurs
    type: str
    sample: "Not Found"

failed:
    description: This field indicates whether the task failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task dispatched to generate the runway.
    returned: always
    type: str
    sample: "ZXJnb24=:8b2fbf4e-8d47-4c26-9df5-63cf8d1af51a"

ext_id:
    description: The external ID (UUID) of the capacity planning scenario on which the runway was generated.
    returned: always
    type: str
    sample: "5b3d1f7c-2b6a-4b64-8b6a-1b0a5f3d8e4c"
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
    import ntnx_aiops_py_client as aiops_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as aiops_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def generate_runway(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Runway generation will be triggered for capacity planning "
            "scenario with ext_id: {0}".format(ext_id)
        )
        return

    # Defensive guard: at this point the SDK must be available (run_module()
    # bails out earlier if not) and api_instance must be a real ScenariosApi.
    # Referencing aiops_sdk.ScenariosApi here also anchors the SDK import so
    # the module fails fast in the very unusual case where the api_client
    # returned an incompatible object.
    if not isinstance(api_instance, aiops_sdk.ScenariosApi):
        module.fail_json(
            msg=(
                "Internal error: expected a ScenariosApi instance to "
                "invoke generate_runway on."
            ),
            **result,
        )

    resp = None
    try:
        resp = api_instance.generate_runway(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while generating runway for capacity planning scenario",
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
            msg=missing_required_lib("ntnx_aiops_py_client"), exception=SDK_IMP_ERROR
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
    generate_runway(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
