#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_route_for_bgp_sessions_info_v2
short_description: Fetch BGP routes for a BGP session in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about RouteForBgpSession in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific RouteForBgpSession for the given BGP session.
  - If C(ext_id) is not provided, list multiple RouteForBgpSession optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Get the specified route of the specified BGP session) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, VPC Admin
    - >-
      B(List routes of the specified BGP session) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the BGP route.
      - When provided together with C(bgp_session_ext_id), fetch a single route by ID.
    type: str
  bgp_session_ext_id:
    description:
      - The external ID of the BGP session that owns the BGP routes.
      - Required to list routes for a BGP session or to fetch a single BGP route by ID.
    type: str
    required: true
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
- name: List all BGP routes for the specified BGP session
  nutanix.ncp.ntnx_route_for_bgp_sessions_info_v2:
    bgp_session_ext_id: "0005c73f-8fdb-4c86-83a3-a97e7a5e8ff2"
  register: result
  ignore_errors: true

- name: Fetch a specific BGP route by ext_id
  nutanix.ncp.ntnx_route_for_bgp_sessions_info_v2:
    bgp_session_ext_id: "0005c73f-8fdb-4c86-83a3-a97e7a5e8ff2"
    ext_id: "8b2bf3d0-6c5f-42d2-8b0a-9f2fbc7a2b17"
  register: result
  ignore_errors: true

- name: List BGP routes advertised by the specified BGP session
  nutanix.ncp.ntnx_route_for_bgp_sessions_info_v2:
    bgp_session_ext_id: "0005c73f-8fdb-4c86-83a3-a97e7a5e8ff2"
    filter: "bgpRouteType eq Networking.Config.BgpRouteType'ADVERTISED'"
  register: result
  ignore_errors: true

- name: List first BGP route for the specified BGP session
  nutanix.ncp.ntnx_route_for_bgp_sessions_info_v2:
    bgp_session_ext_id: "0005c73f-8fdb-4c86-83a3-a97e7a5e8ff2"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RouteForBgpSession info v4 API.
    - It can be a single RouteForBgpSession if external ID is provided.
    - List of multiple RouteForBgpSession if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "bgp_communities": null,
      "bgp_route_type": "ADVERTISED",
      "bgp_session_reference": "0005c73f-8fdb-4c86-83a3-a97e7a5e8ff2",
      "description": null,
      "destination": {
        "ipv4": {
          "prefix_length": 24,
          "value": "10.0.0.0"
        },
        "ipv6": null
      },
      "ext_id": "8b2bf3d0-6c5f-42d2-8b0a-9f2fbc7a2b17",
      "links": null,
      "metadata": null,
      "name": null,
      "nexthop": {
        "nexthop_ip_address": {
          "ipv4": {
            "prefix_length": 32,
            "value": "10.44.0.1"
          },
          "ipv6": null
        },
        "nexthop_name": null,
        "nexthop_reference": null,
        "nexthop_type": null
      },
      "nexthops": null,
      "project_ext_id": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the BGP route (only returned when a single BGP route is fetched by ext_id).
  type: str
  returned: when external ID is provided
  sample: "8b2bf3d0-6c5f-42d2-8b0a-9f2fbc7a2b17"

bgp_session_ext_id:
  description: External ID of the BGP session used to scope the request.
  type: str
  returned: always
  sample: "0005c73f-8fdb-4c86-83a3-a97e7a5e8ff2"

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching BGP route info"

error:
  description: This field typically holds information about the error that occurred during the task execution.
  type: str
  returned: when an error occurs

total_available_results:
  description: The total number of available BGP routes in the BGP session.
  type: int
  returned: when all BGP routes are fetched
  sample: 8
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_bgp_routes_api_instance,
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
        bgp_session_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_bgp_route_by_ext_id(module, bgp_routes_api, result):
    ext_id = module.params.get("ext_id")
    bgp_session_ext_id = module.params.get("bgp_session_ext_id")
    result["ext_id"] = ext_id
    result["bgp_session_ext_id"] = bgp_session_ext_id
    try:
        resp = bgp_routes_api.get_route_for_bgp_session_by_id(
            extId=ext_id, bgpSessionExtId=bgp_session_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching BGP route info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def list_bgp_routes(module, bgp_routes_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    bgp_session_ext_id = module.params.get("bgp_session_ext_id")
    result["bgp_session_ext_id"] = bgp_session_ext_id
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating BGP routes info spec", **result)

    try:
        resp = bgp_routes_api.list_routes_by_bgp_session_id(
            bgpSessionExtId=bgp_session_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching BGP routes info",
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
    bgp_routes_api = get_bgp_routes_api_instance(module)
    if module.params.get("ext_id"):
        get_bgp_route_by_ext_id(module, bgp_routes_api, result)
    else:
        list_bgp_routes(module, bgp_routes_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
