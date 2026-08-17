#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_runways_info_v2
short_description: Fetch capacity planning (Runway) scenarios info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Runway in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Runway.
  - If C(ext_id) is not provided, list multiple Runway optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs (ntnx_aiops_py_client).
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get capacity planning scenario by ext_id) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer,
    Project Admin, Super Admin
  - >-
    B(Get list of capacity planning scenarios) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer,
    Project Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the capacity planning scenario.
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
- name: Get capacity planning scenario using ext_id
  nutanix.ncp.ntnx_runways_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all capacity planning scenarios
  nutanix.ncp.ntnx_runways_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List capacity planning scenarios with filter
  nutanix.ncp.ntnx_runways_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'runway_scenario_ansible'"
  register: result
  ignore_errors: true

- name: List capacity planning scenarios with limit
  nutanix.ncp.ntnx_runways_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Runway info v4 API.
    - It can be a single Runway if external ID is provided.
    - List of multiple Runway if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster_config": {
        "data_store_config": {
          "compression_saving_percent": 25.81,
          "cpu_over_commit_ratio": 1.0,
          "cpu_reservation_percentage": 0.0,
          "dedup_saving_percent": 35.86,
          "erasure_coding_saving_percent": 15.17,
          "overall_saving_percent": 59.64,
          "ram_over_commit_ratio": 1.0,
          "ram_reservation_percentage": 0.0,
          "replication_factor": "RF_2",
          "storage_reservation_percentage": 0.0
        },
        "node_configs": null
      },
      "cluster_ext_id": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "links": null,
      "name": "runway_scenario_ansible",
      "runway": {
        "cpu_runway_days": 240,
        "memory_runway_days": 300,
        "minimum_runway_days": 240,
        "runway_start_time": "2026-01-01T00:00:00+00:00",
        "storage_runway_days": 366
      },
      "target_runway_days": 90,
      "tenant_id": null,
      "updated_time": "2026-01-01T00:00:00+00:00",
      "vendors": null,
      "workloads": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching capacity planning scenarios info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the capacity planning scenario
  type: str
  returned: when external ID is provided
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

total_available_results:
  description: The total number of available capacity planning scenarios in PC.
  type: int
  returned: when all capacity planning scenarios are fetched
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

# Suppress the InsecureRequestWarning
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
        module.fail_json(
            msg="Failed generating capacity planning scenarios info spec",
            **result,
        )

    try:
        resp = api_instance.list_scenarios(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching capacity planning scenarios info",
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
