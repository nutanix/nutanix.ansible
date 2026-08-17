#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_simulations_info_v2
short_description: Fetch VM simulations info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Simulation in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Simulation.
  - If C(ext_id) is not provided, list multiple Simulation optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get a VM Simulation by ext_id) -
    Required Roles: Prism Viewer, Prism Admin, Super Admin
  - >-
    B(List VM Simulations) -
    Required Roles: Prism Viewer, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  ext_id:
    description:
      - The external ID of the simulation.
      - If provided, fetch a specific simulation.
    type: str
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
- name: Get VM simulation using ext_id
  nutanix.ncp.ntnx_simulations_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result

- name: List all VM simulations
  nutanix.ncp.ntnx_simulations_info_v2:
  register: result

- name: List VM simulations with filter
  nutanix.ncp.ntnx_simulations_info_v2:
    filter: "name eq 'vdi_medium_workload'"
  register: result

- name: List VM simulations with limit
  nutanix.ncp.ntnx_simulations_info_v2:
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Simulation info v4 API.
    - It can be a single Simulation if external ID is provided.
    - List of multiple Simulation if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "8e2b45a3-15cf-4a2e-b40c-3d1c42908b12",
      "name": "vdi_medium_workload",
      "simulation_spec": {
        "vcpu_count": 4,
        "ram_gb": 8.0,
        "hdd_gb": 100.0,
        "ssd_gb": 200.0
      },
      "links": null,
      "tenant_id": null
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
  sample: "Api Exception raised while fetching simulations info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the simulation.
  type: str
  returned: When external ID is provided
  sample: "8e2b45a3-15cf-4a2e-b40c-3d1c42908b12"

total_available_results:
  description: The total number of available simulations in PC.
  type: int
  returned: When all simulations are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import get_scenarios_api_instance  # noqa: E402
from ..module_utils.v4.aiops.helpers import get_simulation  # noqa: E402
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


def get_simulation_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_simulation(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_simulations(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating simulations info spec", **result)

    try:
        resp = api_instance.list_simulations(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching simulations info",
        )

    total_available_results = 0
    if resp is not None and resp.metadata is not None:
        total_available_results = (
            getattr(resp.metadata, "total_available_results", 0) or 0
        )
    result["total_available_results"] = total_available_results

    data = None
    if resp is not None and resp.data is not None:
        data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


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
        get_simulation_using_ext_id(module, api_instance, result)
    else:
        get_simulations(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
