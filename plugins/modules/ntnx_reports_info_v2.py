#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_reports_info_v2
short_description: Fetch the generated report for a planned capacity scenario in Nutanix Prism Central
version_added: 2.7.0
description:
    - This module allows you to fetch information about Report in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch the generated report for the specific capacity planning scenario.
    - The generated report is returned as raw response data.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Fetch generated report for a capacity planning scenario) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
    ext_id:
        description:
            - The external ID of the capacity planning scenario whose generated report should be fetched.
            - This is the same as C(scenarioExtId) in the underlying v4 API.
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
- name: Fetch the generated report for a capacity planning scenario
  nutanix.ncp.ntnx_reports_info_v2:
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
        - The response from the Nutanix PC Report info v4 API.
        - Returns the generated report for the capacity planning scenario referenced by C(ext_id).
    returned: always
    type: dict
    sample:
        {
            "data": "<need_to_add_sample>",
            "metadata": {
                "flags": [
                    {
                        "name": "hasError",
                        "value": false
                    }
                ],
                "total_available_results": 1
            }
        }

ext_id:
    description: The external ID of the capacity planning scenario used to fetch the report.
    returned: when external ID is provided
    type: str
    sample: "32459cae-43ca-4b6f-9bab-857895c1f867"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching scenario report using scenario ext_id"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: when an error occurs

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import get_scenarios_api_instance  # noqa: E402
from ..module_utils.v4.aiops.helpers import get_scenario_report  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

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
        ext_id=dict(type="str", required=True),
    )

    return module_args


def get_scenario_report_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_scenario_report(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    if hasattr(resp, "to_dict"):
        result["response"] = strip_internal_attributes(resp.to_dict())
    else:
        result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_aiops_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "ext_id": None, "failed": False}
    api_instance = get_scenarios_api_instance(module)
    get_scenario_report_using_ext_id(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
