#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_scenario_reports_info_v2
short_description: Fetch the generated capacity planning scenario report from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ScenarioReport in Nutanix Prism Central.
  - If C(scenario_ext_id) is provided, download the PDF report generated for that scenario.
  - The AIOps ScenarioReport API does not support listing multiple reports; it always returns the
    single report for the given scenario.
  - The SDK downloads the report to a local temporary file. The path to that file is returned
    in C(report_file_path). Callers can optionally copy it to a stable location via C(dest).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get a scenario report) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
    scenario_ext_id:
        description:
            - The external ID (UUID) of the capacity planning scenario whose report should be fetched.
        type: str
        required: true
    dest:
        description:
            - Optional local file path where the downloaded PDF report should be copied.
            - If not provided, the report will remain at the temporary path returned in
              C(report_file_path).
        type: path
        required: false
    read_timeout:
        description: Read timeout in milliseconds for API calls.
        type: int
        required: false
        default: 30000
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - George Ghawali (@george-ghawali)
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch the generated report for a capacity planning scenario
  nutanix.ncp.ntnx_scenario_reports_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    scenario_ext_id: "b1d6e7cc-1234-4b56-8ce0-8c19d7c8f0a1"
  register: result
  ignore_errors: true

- name: Fetch the report and copy it to a stable destination
  nutanix.ncp.ntnx_scenario_reports_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    scenario_ext_id: "b1d6e7cc-1234-4b56-8ce0-8c19d7c8f0a1"
    dest: "/tmp/scenario_report.pdf"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC ScenarioReport info v4 API.
        - Contains the local filesystem path to the downloaded PDF report.
        - The AIOps ScenarioReport API returns a single report for the given scenario;
          listing / filtering is not supported by the SDK.
    returned: always
    type: dict
    sample:
        {
            "report_file_path": "/tmp/tmp_scenario_report_b1d6e7cc.pdf",
            "content_type": "application/pdf",
            "size_bytes": 24815
        }

report_file_path:
    description:
        - Absolute local path to the downloaded PDF report.
        - Equal to the value of C(dest) if C(dest) was provided; otherwise the temporary
          path returned by the SDK.
    returned: when the report was downloaded successfully
    type: str
    sample: "/tmp/tmp_scenario_report_b1d6e7cc.pdf"

changed:
    description: Whether the task resulted in any changes. Info modules never change state.
    returned: always
    type: bool
    sample: false

msg:
    description: Message describing the outcome (error / info).
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching scenario report using scenario ext_id"

error:
    description: Error details if the operation failed.
    returned: when an error occurs
    type: str
    sample: "SDK returned no report data"

failed:
    description: Whether the task failed.
    returned: always
    type: bool
    sample: false

ext_id:
    description: The external ID of the capacity planning scenario whose report was fetched.
    returned: when scenario_ext_id is provided
    type: str
    sample: "b1d6e7cc-1234-4b56-8ce0-8c19d7c8f0a1"
"""

import os  # noqa: E402
import shutil  # noqa: E402
import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import get_scenarios_api_instance  # noqa: E402
from ..module_utils.v4.aiops.helpers import get_scenario_report  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        scenario_ext_id=dict(type="str", required=True),
        dest=dict(type="path", required=False),
    )
    return module_args


def _resolve_report_path(data):
    """Return an absolute string path for whatever the SDK gave us as the report body.

    The AIOps SDK usually returns a ``pathlib.Path``; some builds may return a
    plain string. Anything else is unexpected and treated as missing.
    """
    if data is None:
        return None
    if isinstance(data, Path):
        return str(data)
    if isinstance(data, str):
        return data
    return None


def _summarize_report(path_str):
    """Build a small dict describing the downloaded PDF file (path, content type, size)."""
    info = {"report_file_path": path_str, "content_type": "application/pdf"}
    try:
        info["size_bytes"] = os.path.getsize(path_str)
    except OSError:
        info["size_bytes"] = None
    return info


def get_scenario_report_using_ext_id(module, api_instance, result):
    scenario_ext_id = module.params.get("scenario_ext_id")
    dest = module.params.get("dest")
    result["ext_id"] = scenario_ext_id

    data = get_scenario_report(module, api_instance, scenario_ext_id)
    source_path = _resolve_report_path(data)
    if not source_path or not os.path.exists(source_path):
        result["failed"] = True
        result["error"] = "SDK returned no report data"
        module.fail_json(
            msg="Failed to download report for scenario ext_id:{0}".format(
                scenario_ext_id
            ),
            **result,
        )

    final_path = source_path
    if dest:
        dest_dir = os.path.dirname(os.path.abspath(dest))
        if dest_dir:
            try:
                os.makedirs(dest_dir, exist_ok=True)
            except OSError as e:
                result["failed"] = True
                result["error"] = str(e)
                module.fail_json(
                    msg="Failed to create destination directory: {0}".format(dest_dir),
                    **result,
                )
        try:
            shutil.copyfile(source_path, dest)
        except OSError as e:
            result["failed"] = True
            result["error"] = str(e)
            module.fail_json(
                msg="Failed to copy report to destination: {0}".format(dest), **result
            )
        final_path = dest

    result["response"] = _summarize_report(final_path)
    result["report_file_path"] = final_path


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_scenarios_api_instance(module)
    get_scenario_report_using_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
