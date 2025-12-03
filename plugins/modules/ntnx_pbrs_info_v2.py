#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_pbrs_info_v2
short_description: Routing Policies info module
version_added: 2.0.0
description:
    - Fetch a single or list of all routing policies
    - if ext_id is provided, it will return the routing policy info
    - if ext_id is not provided, it will return the list of all routing policies
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - Routing policy external ID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List all pbrs
  nutanix.ncp.ntnx_pbrs_info_v2:
  register: result
  ignore_errors: true

- name: List pbrs using name filter criteria
  nutanix.ncp.ntnx_pbrs_info_v2:
    filter: "name eq 'test_policy_name'"
  register: result
  ignore_errors: true

- name: List pbrs using ext_id
  nutanix.ncp.ntnx_pbrs_info_v2:
    ext_id: '47ca25c3-9d27-4b94-b6b1-dfa5b25660b4'
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
      - The response from the routing policy v4 API.
      - it can be routing policy or list of routing policies as per spec.
  returned: always
  type: dict
  sample:
    {
        "description": null,
        "ext_id": "44ad2150-b103-4346-a26b-4d0ad858cddf",
        "links": null,
        "metadata": {
            "category_ids": null,
            "owner_reference_id": "00000000-0000-0000-0000-000000000000",
            "owner_user_name": "admin",
            "project_name": null,
            "project_reference_id": null
        },
        "name": "virtual-network-deny-all",
        "policies": [
            {
                "is_bidirectional": false,
                "policy_action": {
                    "action_type": "DENY",
                    "nexthop_ip_address": null,
                    "reroute_params": null
                },
                "policy_match": {
                    "destination": {
                        "address_type": "ANY",
                        "subnet_prefix": null
                    },
                    "protocol_parameters": null,
                    "protocol_type": "ANY",
                    "source": {
                        "address_type": "ANY",
                        "subnet_prefix": null
                    }
                }
            }
        ],
        "priority": 1,
        "tenant_id": null,
        "vpc": null,
        "vpc_ext_id": "69665951-76db-401c-8b92-9a60af7d024e",
    }
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching routing policies info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

total_available_results:
    description:
        - The total number of available routing policies in PC.
    type: int
    returned: when all routing policies are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_routing_policies_api_instance,
)
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


def get_pbr(module, result):
    pbrs = get_routing_policies_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = pbrs.get_routing_policy_by_id(ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching routing policies info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_pbrs(module, result):
    pbrs = get_routing_policies_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating pbrs info Spec", **result)

    try:
        resp = pbrs.list_routing_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching pbrs info",
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
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_pbr(module, result)
    else:
        get_pbrs(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
