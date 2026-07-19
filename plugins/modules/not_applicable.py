#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: not_applicable
short_description: Fetch Subnet info in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to fetch information about Subnet in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Subnet.
  - If C(ext_id) is not provided, list multiple Subnet optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - External ID (UUID) of the subnet to fetch.
      - If provided, the module returns the specific subnet.
      - If omitted, the module returns a paginated list of subnets.
    type: str
    required: false
  expand:
    description:
      - OData C($expand) system query option.
      - Expands related resources inline in the response.
    type: str
    required: false
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
- name: Fetch a specific subnet by external ID
  nutanix.ncp.not_applicable:
    ext_id: "1d42d222-a065-4ed8-9f74-dc5818dfab41"
  register: result

- name: List all subnets
  nutanix.ncp.not_applicable:
  register: result

- name: List subnets with an OData filter
  nutanix.ncp.not_applicable:
    filter: "name eq 'subnet-name'"
  register: result

- name: List subnets with a page limit
  nutanix.ncp.not_applicable:
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Subnet info v4 API.
    - It can be a single Subnet if external ID is provided.
    - List of multiple Subnet if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "bridge_name": null,
      "cluster_name": null,
      "cluster_name_list": null,
      "cluster_reference": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "cluster_reference_list": [
          "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
      ],
      "description": null,
      "dhcp_options": null,
      "dynamic_ip_addresses": null,
      "ext_id": "c9b8886d-3929-4e03-90ef-49c6d6f7e349",
      "external_dhcp_servers": null,
      "hypervisor_type": "acropolis",
      "ip_config": null,
      "ip_prefix": null,
      "ip_usage": {
          "ip_pool_usages": null,
          "num_assigned_i_ps": 0,
          "num_free_i_ps": 0,
          "num_macs": 0
      },
      "is_advanced_networking": true,
      "is_external": false,
      "is_nat_enabled": null,
      "layer2_stretch_reference": null,
      "links": null,
      "metadata": {
          "category_ids": null,
          "owner_reference_id": "00000000-0000-0000-0000-000000000000",
          "owner_user_name": "admin",
          "project_name": "_internal",
          "project_reference_id": "00000000-0000-0000-0000-000000000000"
      },
      "migration_state": null,
      "name": "subnet_ansible_test_aMalTKAYZbhp",
      "network_function_chain_reference": null,
      "network_id": 0,
      "reserved_ip_addresses": null,
      "subnet_type": "VLAN",
      "tenant_id": null,
      "virtual_switch": null,
      "virtual_switch_reference": "22672efd-210f-41dc-9934-d3cb5908b727",
      "vpc": null,
      "vpc_reference": null
    }

changed:
  description:
    - This indicates whether the task resulted in any changes.
    - Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - External ID of the subnet.
    - Returned only when C(ext_id) is provided in the input.
  returned: when external ID is provided
  type: str
  sample: "1d42d222-a065-4ed8-9f74-dc5818dfab41"

total_available_results:
  description:
    - Total number of subnets available in Prism Central.
    - Returned only when listing multiple subnets (C(ext_id) not provided).
  returned: when listing multiple subnets
  type: int
  sample: 42

msg:
  description:
    - Status/error message describing the operation outcome.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching subnet info using ext_id"

error:
  description:
    - Error details when the operation fails, C(None) on success.
  returned: always
  type: str

failed:
  description:
    - Indicates whether the operation failed.
  returned: when something fails
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import get_subnet_api_instance  # noqa: E402
from ..module_utils.v4.network.helpers import get_subnet  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        expand=dict(type="str"),
    )
    return module_args


def get_subnet_using_ext_id(module, subnets_api, result):
    ext_id = module.params.get("ext_id")
    resp = get_subnet(module, subnets_api, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_subnets(module, subnets_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating subnets info spec", **result)

    try:
        resp = subnets_api.list_subnets(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching subnets info",
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
    result = {"changed": False, "response": None, "error": None, "failed": False}
    subnets_api = get_subnet_api_instance(module)
    if module.params.get("ext_id"):
        get_subnet_using_ext_id(module, subnets_api, result)
    else:
        get_subnets(module, subnets_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
