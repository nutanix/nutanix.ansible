#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_routes_by_bgp_session_ids_info_v2
short_description: Fetch BGP routes info for a BGP session in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about RoutesByBgpSessionId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific RoutesByBgpSessionId.
  - If C(ext_id) is not provided, list multiple RoutesByBgpSessionId optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Get the specified route of the specified BGP session) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer,
      Project Admin, Super Admin, Virtual Machine Admin, Virtual Machine Operator,
      Virtual Machine Viewer, VPC Admin
    - >-
      B(Lists routes of the specified BGP session) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer,
      Project Admin, Super Admin, Virtual Machine Admin, Virtual Machine Operator,
      Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the BGP route to fetch.
      - When provided together with C(bgp_session_ext_id), the module fetches only that route.
    type: str
    required: false
  bgp_session_ext_id:
    description:
      - The external ID of the parent BGP session whose routes should be fetched or listed.
    type: str
    required: true
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
- name: List all BGP routes for a given BGP session
  nutanix.ncp.ntnx_routes_by_bgp_session_ids_info_v2:
    bgp_session_ext_id: "8a3cf052-1234-4222-8d60-143a33c77e9f"
  register: result
  ignore_errors: true

- name: Fetch a specific BGP route for a BGP session by external ID
  nutanix.ncp.ntnx_routes_by_bgp_session_ids_info_v2:
    bgp_session_ext_id: "8a3cf052-1234-4222-8d60-143a33c77e9f"
    ext_id: "ed3cf052-a96a-4222-8d60-143a33c77e9f"
  register: result
  ignore_errors: true

- name: List BGP routes for a BGP session with a filter (only received routes)
  nutanix.ncp.ntnx_routes_by_bgp_session_ids_info_v2:
    bgp_session_ext_id: "8a3cf052-1234-4222-8d60-143a33c77e9f"
    filter: "bgpRouteType eq Nutanix.Networking.Config.BgpRouteType'RECEIVED'"
  register: result
  ignore_errors: true

- name: List BGP routes for a BGP session with pagination (page 0, limit 10)
  nutanix.ncp.ntnx_routes_by_bgp_session_ids_info_v2:
    bgp_session_ext_id: "8a3cf052-1234-4222-8d60-143a33c77e9f"
    page: 0
    limit: 10
  register: result
  ignore_errors: true

- name: List BGP routes for a BGP session sorted by name
  nutanix.ncp.ntnx_routes_by_bgp_session_ids_info_v2:
    bgp_session_ext_id: "8a3cf052-1234-4222-8d60-143a33c77e9f"
    orderby: "name asc"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RoutesByBgpSessionId info v4 API.
    - It can be a single RoutesByBgpSessionId if external ID is provided.
    - List of multiple RoutesByBgpSessionId if external ID is not provided
      with optional filter or limit.
  returned: always
  type: dict
  sample:
    [
      {
        "bgp_communities": null,
        "bgp_route_type": "ADVERTISED",
        "bgp_session_reference": "8a3cf052-1234-4222-8d60-143a33c77e9f",
        "description": null,
        "destination": {
            "ipv4": {"ip": {"prefix_length": 32, "value": "10.0.0.0"}, "prefix_length": 24},
            "ipv6": null
        },
        "ext_id": "ed3cf052-a96a-4222-8d60-143a33c77e9f",
        "links": null,
        "metadata": null,
        "name": "advertised_route",
        "nexthop": {
            "nexthop_ip_address": {"ipv4": {"prefix_length": 32, "value": "10.44.3.1"}, "ipv6": null},
            "nexthop_name": "local-bgp-gateway",
            "nexthop_reference": "5e98d574-c54c-4775-9f7a-8ebb2bc77d2c",
            "nexthop_type": "EXTERNAL_SUBNET"
        },
        "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always C(False) for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching BGP routes info"

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
  description: External ID of the BGP route when a single route is fetched.
  type: str
  returned: when external ID is provided
  sample: "ed3cf052-a96a-4222-8d60-143a33c77e9f"

bgp_session_ext_id:
  description: External ID of the parent BGP session.
  type: str
  returned: always
  sample: "8a3cf052-1234-4222-8d60-143a33c77e9f"

total_available_results:
  description: The total number of BGP routes available for the parent BGP session.
  type: int
  returned: when all BGP routes are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_bgp_routes_api_instance,
)
from ..module_utils.v4.network.helpers import get_bgp_route  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        bgp_session_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_bgp_route_by_ext_id(module, api_instance, result):
    """Fetch a single BGP route by (bgp_session_ext_id, ext_id)."""
    ext_id = module.params.get("ext_id")
    bgp_session_ext_id = module.params.get("bgp_session_ext_id")
    result["ext_id"] = ext_id
    result["bgp_session_ext_id"] = bgp_session_ext_id
    resp = get_bgp_route(module, api_instance, ext_id, bgp_session_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_bgp_routes(module, api_instance, result):
    """List BGP routes for a given BGP session (supports filter/limit/page/orderby)."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    bgp_session_ext_id = module.params.get("bgp_session_ext_id")
    result["bgp_session_ext_id"] = bgp_session_ext_id
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating BGP routes info Spec", **result)

    try:
        resp = api_instance.list_routes_by_bgp_session_id(
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
    result = {"changed": False, "error": None, "response": None}
    api_instance = get_bgp_routes_api_instance(module)
    if module.params.get("ext_id"):
        get_bgp_route_by_ext_id(module, api_instance, result)
    else:
        list_bgp_routes(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
