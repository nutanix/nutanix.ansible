#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_routes_by_bgp_session_id_v2
short_description: Fetch a single BGP route advertised or received on a BGP session in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module fetches a single BGP route associated with a BGP session in Nutanix Prism Central.
  - Routes learned over a BGP session (advertised, received, or received-and-ignored) are managed by the
    BGP gateway serving the session and are surfaced by the Nutanix networking v4 API as a read-only
    collection - there are no SDK operations to create, update, or delete a BGP route.
  - As a result, this module only supports C(state=present) together with C(ext_id) and
    C(bgp_session_ext_id) to fetch the specified BGP route by its external ID. Any other combination
    (C(state=present) without C(ext_id), or C(state=absent)) fails fast with a descriptive error
    explaining that BGP routes are read-only and pointing the operator at
    M(nutanix.ncp.ntnx_routes_by_bgp_session_ids_info_v2) for listing.
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
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and both C(ext_id) and C(bgp_session_ext_id) are provided,
        the module fetches the specified BGP route.
      - If C(state) is set to C(present) and C(ext_id) is not provided, the module fails because
        BGP routes cannot be created through the API.
      - If C(state) is set to C(absent), the module fails because BGP routes cannot be deleted
        through the API.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the BGP route to fetch.
      - Required for the fetch operation (C(state=present)).
    type: str
    required: false
  bgp_session_ext_id:
    description:
      - The external ID of the parent BGP session that owns the BGP route.
      - Required for the fetch operation (C(state=present)).
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch a BGP route by external ID for a given BGP session
  nutanix.ncp.ntnx_routes_by_bgp_session_id_v2:
    state: present
    bgp_session_ext_id: "8a3cf052-1234-4222-8d60-143a33c77e9f"
    ext_id: "ed3cf052-a96a-4222-8d60-143a33c77e9f"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The BGP route detail returned by the Nutanix PC networking v4 API for the given BGP session.
    - Present whenever a route is successfully fetched.
  returned: always
  type: dict
  sample:
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

task_ext_id:
  description:
    - The external ID of the task.
    - BGP routes are read-only, so this value is always C(None) for this module.
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the BGP route that was fetched.
  returned: always
  type: str
  sample: "ed3cf052-a96a-4222-8d60-143a33c77e9f"

bgp_session_ext_id:
  description:
    - The external ID of the parent BGP session.
  returned: when C(bgp_session_ext_id) is provided
  type: str
  sample: "8a3cf052-1234-4222-8d60-143a33c77e9f"

changed:
  description:
    - This indicates whether the task resulted in any changes.
    - Always C(False) because the BGP routes API only supports read operations.
  returned: always
  type: bool
  sample: false

skipped:
  description:
    - This indicates whether the task was skipped.
    - Always C(False) because the module either fetches the route or fails.
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or when the operation is not supported by the API
  type: str
  sample: "BGP routes are read-only. Use ntnx_routes_by_bgp_session_ids_info_v2 to fetch or list them."
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_bgp_routes_api_instance,
)
from ..module_utils.v4.network.helpers import get_bgp_route  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    strip_internal_attributes,
    validate_required_params,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

READ_ONLY_MSG = (
    "BGP routes are read-only. The Nutanix networking v4 SDK does not expose "
    "create, update, or delete operations for routes advertised or received "
    "over a BGP session. Use nutanix.ncp.ntnx_routes_by_bgp_session_ids_info_v2 "
    "to list or fetch BGP routes."
)


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        bgp_session_ext_id=dict(type="str"),
    )
    return module_args


def _fetch_route(module, result, api_instance):
    """Fetch a single BGP route by (bgp_session_ext_id, ext_id).

    Semantics: BGP routes are a read-only collection surfaced by the
    networking v4 API, so this is the only operation supported by this
    module. ``changed`` remains ``False`` because no server-side state is
    modified.
    """
    validate_required_params(module, ["ext_id", "bgp_session_ext_id"])
    ext_id = module.params.get("ext_id")
    bgp_session_ext_id = module.params.get("bgp_session_ext_id")
    result["ext_id"] = ext_id
    result["bgp_session_ext_id"] = bgp_session_ext_id

    if module.check_mode:
        result["msg"] = (
            "BGP route with ext_id:{0} for BGP session ext_id:{1} would be fetched.".format(
                ext_id, bgp_session_ext_id
            )
        )
        return

    resp = get_bgp_route(module, api_instance, ext_id, bgp_session_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def create_RoutesByBgpSessionId(module, result, api_instance):
    """BGP routes cannot be created via the API - fail with a descriptive error."""
    module.fail_json(msg=READ_ONLY_MSG, **result)


def update_RoutesByBgpSessionId(module, result, api_instance):
    """BGP routes cannot be updated via the API - fetch and return the current
    state instead. ``changed`` stays ``False`` to reflect that no mutation
    happened server-side.
    """
    _fetch_route(module, result, api_instance)


def delete_RoutesByBgpSessionId(module, result, api_instance):
    """BGP routes cannot be deleted via the API - fail with a descriptive error."""
    module.fail_json(msg=READ_ONLY_MSG, **result)


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
        "failed": False,
    }
    api_instance = get_bgp_routes_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_RoutesByBgpSessionId(module, result, api_instance)
        else:
            create_RoutesByBgpSessionId(module, result, api_instance)
    else:
        delete_RoutesByBgpSessionId(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
