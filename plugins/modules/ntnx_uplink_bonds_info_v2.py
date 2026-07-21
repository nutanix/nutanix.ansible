#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_uplink_bonds_info_v2
short_description: Fetch uplink bonds info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about UplinkBond in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific UplinkBond.
  - If C(ext_id) is not provided, list multiple UplinkBond optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get uplink bond by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, Virtual Machine Admin,
      Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - >-
      B(Get list of Uplink Bonds) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, Virtual Machine Admin,
      Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the uplink bond.
      - If provided, fetch details of the specific uplink bond.
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
- name: Get uplink bond using ext_id
  nutanix.ncp.ntnx_uplink_bonds_info_v2:
    ext_id: "b46b8d21-79ad-4cd2-a770-181a97e9e689"
  register: result
  ignore_errors: true

- name: List all uplink bonds
  nutanix.ncp.ntnx_uplink_bonds_info_v2:
  register: result
  ignore_errors: true

- name: List uplink bonds with filter
  nutanix.ncp.ntnx_uplink_bonds_info_v2:
    filter: "name eq 'br0-up'"
  register: result
  ignore_errors: true

- name: List uplink bonds with limit
  nutanix.ncp.ntnx_uplink_bonds_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC UplinkBond info v4 API.
    - It can be a single UplinkBond if external ID is provided.
    - List of multiple UplinkBond if external ID is not provided.
  returned: always
  type: dict
  sample:
    {
      "cluster_reference": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "ext_id": "b46b8d21-79ad-4cd2-a770-181a97e9e689",
      "host_nic_references": [
          "94b24cd7-f4ff-4164-ba7a-fc69e35f8b6c",
          "084af8fb-87f8-46e6-a2f4-cabeffc81850",
          "efc40201-750e-49b1-9e52-f64c05121b61",
          "8ae64a0e-bf81-4424-b57f-5cbc8e8f24ac"
      ],
      "host_reference": "adf0c9e0-4051-4cd2-9f6f-ca9f962e941b",
      "lacp_status": "NIL",
      "links": null,
      "metadata": null,
      "name": "br0-up",
      "project_ext_id": null,
      "tenant_id": null,
      "type": "ACTIVE_BACKUP",
      "virtual_switch_info": {
          "name": "vs0",
          "reference": "22672efd-210f-41dc-9934-d3cb5908b727"
      }
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error.
  type: str
  sample: "Api Exception raised while fetching uplink bonds info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the uplink bond.
  type: str
  returned: when external ID is provided
  sample: "b46b8d21-79ad-4cd2-a770-181a97e9e689"

total_available_results:
  description: The total number of available uplink bonds in PC.
  type: int
  returned: when all uplink bonds are fetched
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_uplink_bonds_api_instance,
)
from ..module_utils.v4.network.helpers import get_uplink_bond  # noqa: E402
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


def get_uplink_bond_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_uplink_bond(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_uplink_bonds(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating uplink bonds info spec", **result)

    try:
        resp = api_instance.list_uplink_bonds(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching uplink bonds info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

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
    api_instance = get_uplink_bonds_api_instance(module)
    if module.params.get("ext_id"):
        get_uplink_bond_using_ext_id(module, api_instance, result)
    else:
        get_uplink_bonds(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
