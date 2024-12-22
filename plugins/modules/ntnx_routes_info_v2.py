#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_routes_info_v2
short_description: Routes info module
version_added: 2.0.0
description: This module fetches routes information
options:
    ext_id:
        description:
            - Route external ID
        type: str
    route_table_ext_id:
        description:
            - Route table external ID
        type: str
        required: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: List all routes
  nutanix.ncp.ntnx_routes_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    route_table_ext_id: "13a6657d-fa96-49e3-7307-87e93a1fec3d"
  register: result

- name: Fetch route by external ID
  nutanix.ncp.ntnx_routes_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: 5d4f9c3b-7ea1-4a92-bfae-9d3e7c2a1b45
    route_table_ext_id: 82b71a8c-2d9f-4f7c-ae65-2b4c2c3e3fbd
  register: result
  ignore_errors: true

- name: List all routes with filter
  nutanix.ncp.ntnx_routes_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    route_table_ext_id: "13a6657d-fa96-49e3-7307-87e93a1fec3d"
    filter: name eq 'route_name'
  register: result

- name: List all routes with limit
  nutanix.ncp.ntnx_routes_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    route_table_ext_id: "13a6657d-fa96-49e3-7307-87e93a1fec3d"
    limit: 1
  register: result
"""
RETURN = r"""
response:
    description:
        - Response for fetching routes info
        - Returns route or list of multiple routes details.
    type: dict
    returned: always
    sample:
        {
          "extId": "ed3cf052-a96a-4222-8d60-143a33c77e9f",
          "isActive": true,
          "priority": 32768,
          "metadata": { "ownerReferenceId": "00000000-0000-0000-0000-000000000000" },
          "name": "route_test",
          "destination":
            { "ipv4": { "ip": { "value": "10.0.0.1" }, "prefixLength": 32 } },
          "nexthop":
            {
              "nexthopName": "integration_test_Ext-Nat1",
              "nexthopType": "EXTERNAL_SUBNET",
              "nexthopReference": "5e98d574-c54c-4775-9f7a-8ebb2bc77d2c",
              "nexthopIpAddress":
                { "ipv4": { "value": "10.44.3.193", "prefixLength": 32 } },
            },
          "routeTableReference": "7f9a76a3-922b-4aba-8d79-e7eb5cdaf201",
          "vpcReference": "66a926de-c188-4121-8456-0b97cdf0f807",
          "routeType": "STATIC",
        }

ext_id:
    description: route external ID
    type: str
    returned: always
    sample: "63acaca5-ed45-415e-bfbd-19c9d9fd3dfd"

route_table_ext_id:
    description: route table external ID
    type: str
    returned: always
    sample: "7f9a76b3-922b-4aba-9d79-e7eb5cdab236"

failed:
    description: Indicates if the request failed
    type: bool
    returned: always

error:
  description: Error message
  type: str
  returned: always

changed:
  description: Indicates if any changes were made during the operation
  type: bool
  returned: always
  sample: False
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import get_routes_api_instance  # noqa: E402
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
        route_table_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_route(module, route_api_instance, result):
    ext_id = module.params.get("ext_id")
    route_table_ext_id = module.params.get("route_table_ext_id")
    result["ext_id"] = ext_id
    result["route_table_ext_id"] = route_table_ext_id
    try:
        resp = route_api_instance.get_route_for_route_table_by_id(
            extId=ext_id, routeTableExtId=route_table_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching route info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_routes(module, route_api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])
    route_table_ext_id = module.params.get("route_table_ext_id")
    result["route_table_ext_id"] = route_table_ext_id
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating route info Spec", **result)

    try:
        resp = route_api_instance.list_routes_by_route_table_id(
            routeTableExtId=route_table_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching routes info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


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
    route_api_instance = get_routes_api_instance(module)
    if module.params.get("ext_id") and module.params.get("route_table_ext_id"):
        get_route(module, route_api_instance, result)
    else:
        get_routes(module, route_api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
