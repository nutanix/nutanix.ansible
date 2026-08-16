#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_scenarios_info_v2
short_description: Fetch information about capacity planning scenarios in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Scenario in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Scenario.
  - If C(ext_id) is not provided, list multiple Scenario optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Scenario by ext_id / List Scenarios) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, Self Service Admin, Internal Super Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  ext_id:
    description:
      - The external ID of the capacity planning scenario.
      - If provided, a single scenario is fetched.
    type: str
    required: false
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
- name: Get a scenario using ext_id
  nutanix.ncp.ntnx_scenarios_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b1e5a5b7-1234-4d3e-b0dc-1a2b3c4d5e6f"
  register: single_scenario
  ignore_errors: true

- name: List all scenarios
  nutanix.ncp.ntnx_scenarios_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: all_scenarios
  ignore_errors: true

- name: List scenarios with a filter
  nutanix.ncp.ntnx_scenarios_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'ansible_scenario_demo'"
  register: filtered_scenarios
  ignore_errors: true

- name: List scenarios with a limit
  nutanix.ncp.ntnx_scenarios_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: limited_scenarios
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Scenario info v4 API.
    - It can be a single Scenario if external ID is provided.
    - List of multiple Scenarios if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster_config": null,
      "cluster_ext_id": "0005f6f4-1c1c-6b3f-0000-0000000abcde",
      "ext_id": "b1e5a5b7-1234-4d3e-b0dc-1a2b3c4d5e6f",
      "links": null,
      "name": "ansible_scenario_demo",
      "runway": null,
      "target_runway_days": 90,
      "tenant_id": null,
      "updated_time": "2026-02-01T12:00:00Z",
      "vendors": ["NUTANIX", "DELL"],
      "workloads": [
        {
          "is_enabled": true,
          "projected_resource_requirement": null,
          "schedule_date": "2026-02-01",
          "workload_properties": {
            "change_type": "INCREASE",
            "percentage_change": 20
          }
        }
      ]
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching scenarios info"

error:
  description: Error details if any error occurred while fetching info.
  type: str
  returned: when an error occurs

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the scenario.
  type: str
  returned: when external ID is provided
  sample: "b1e5a5b7-1234-4d3e-b0dc-1a2b3c4d5e6f"

total_available_results:
  description: The total number of available scenarios in PC.
  type: int
  returned: when all scenarios are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import get_scenarios_api_instance  # noqa: E402
from ..module_utils.v4.aiops.helpers import get_scenario  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
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


def get_scenario_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_scenario(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_scenarios(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating scenarios info spec", **result)

    try:
        resp = api_instance.list_scenarios(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching scenarios info",
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
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_scenarios_api_instance(module)
    if module.params.get("ext_id"):
        get_scenario_using_ext_id(module, api_instance, result)
    else:
        get_scenarios(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
