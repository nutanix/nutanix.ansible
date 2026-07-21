#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_report_configs_info_v2
short_description: Fetch report configurations info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ReportConfig in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ReportConfig.
  - If C(ext_id) is not provided, list multiple ReportConfig optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get report configuration by ext_id) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(Get list of Report Configurations) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=opsmgmt)"
options:
  ext_id:
    description:
      - The external ID of the report configuration.
      - When provided, the module fetches the specific report configuration.
    type: str
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
- name: Get report configuration using ext_id
  nutanix.ncp.ntnx_report_configs_info_v2:
    ext_id: "d05b9c00-3d0e-4bab-9d18-2d5c8bd7d55c"
  register: result
  ignore_errors: true

- name: List all report configurations
  nutanix.ncp.ntnx_report_configs_info_v2:
  register: result
  ignore_errors: true

- name: List report configurations with filter
  nutanix.ncp.ntnx_report_configs_info_v2:
    filter: "name eq 'ansible_report_config'"
  register: result
  ignore_errors: true

- name: List report configurations with limit
  nutanix.ncp.ntnx_report_configs_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ReportConfig info v4 API.
    - It can be a single ReportConfig if external ID is provided.
    - List of multiple ReportConfig if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "creation_time": "2026-07-21T08:15:00.000Z",
      "default_section_entity_type": "VM",
      "description": "Report configuration created by Ansible",
      "end_time_offset_secs": 0,
      "ext_id": "d05b9c00-3d0e-4bab-9d18-2d5c8bd7d55c",
      "is_imported": false,
      "is_private": false,
      "is_system_defined": false,
      "links": null,
      "name": "ansible_report_config",
      "notification_policy": {
        "email_body": "Please find the attached VM report.",
        "email_subject": "Daily VM report",
        "recipient_formats": ["PDF"],
        "recipients": [
          {"email_address": "reports@example.com", "recipient_name": "Reports Team"}
        ]
      },
      "retention_config": {"retention_count": 10, "retention_period_seconds": null},
      "schedule": {
        "end_time": null,
        "frequency": 1,
        "schedule_interval": "DAILY",
        "start_time": "2026-01-01T00:00:00.000Z"
      },
      "sections": [
        {
          "description": "Overview of virtual machines",
          "name": "vm_overview",
          "repeat_criteria": {"entity_type": "VM", "repetition_rule": null},
          "rows": [
            {
              "widgets": [
                {"widget_info": {"entity_type": "VM", "heading": "VM Count", "size": "SMALL", "type": "COUNT_SUMMARY", "widget_id": "vm_count"}}
              ]
            }
          ],
          "time_filter": "CREATED_TIME"
        }
      ],
      "start_time_offset_secs": 86400,
      "supported_formats": ["PDF", "CSV"],
      "tenant_id": null,
      "timezone": "UTC"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Contextual status/error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching report configurations info"

error:
  description: This field typically holds information about the errors that occurred during task execution.
  returned: When an error occurs
  type: str

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the report configuration.
  returned: When external ID is provided
  type: str
  sample: "d05b9c00-3d0e-4bab-9d18-2d5c8bd7d55c"

total_available_results:
  description: The total number of available report configurations in PC.
  returned: When all report configurations are fetched
  type: int
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.opsmgmt.api_client import (  # noqa: E402
    get_report_config_api_instance,
)
from ..module_utils.v4.opsmgmt.helpers import get_report_config  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_report_config_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_report_config(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_report_configs(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating report configurations info spec", **result
        )

    try:
        resp = api_instance.list_report_configs(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching report configurations info",
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
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
            ("ext_id", "select"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_report_config_api_instance(module)
    if module.params.get("ext_id"):
        get_report_config_using_ext_id(module, api_instance, result)
    else:
        list_report_configs(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
