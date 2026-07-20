#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_bgp_sessions_info_v2
short_description: Fetch BGP sessions info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about BgpSession in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific BgpSession.
  - If C(ext_id) is not provided, list multiple BgpSession optionally filtered / paginated.
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the BGP session.
    type: str
  expand:
    description:
      - A URL query parameter that allows clients to request related resources
        along with the primary entity.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get BGP session using ext_id
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"

- name: List all BGP sessions
  nutanix.ncp.ntnx_bgp_sessions_info_v2:

- name: List BGP sessions with filter
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    filter: "name eq 'bgp_session_ansible'"

- name: List BGP sessions with limit
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    limit: 1
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC BgpSession info v4 API.
    - It can be a single BgpSession if external ID is provided.
    - List of multiple BgpSession if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "advertised_routes_communities": null,
      "description": "BGP session created by Ansible",
      "dynamic_route_priority": 100,
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "externally_routable_prefixes_to_advertise": null,
      "links": null,
      "local_gateway": null,
      "local_gateway_interface_ip_address": {
        "ipv4": {"prefix_length": 32, "value": "10.44.76.10"},
        "ipv6": null
      },
      "local_gateway_reference": "b3d1f3a4-5b6c-4d1a-9e2b-1234567890ab",
      "metadata": null,
      "name": "bgp_session_ansible",
      "password": null,
      "prepended_autonomous_system_path": null,
      "remote_gateway": null,
      "remote_gateway_reference": "9a8f7c6b-5432-4d1a-9e2b-fedcba098765",
      "should_advertise_all_externally_routable_prefixes": false,
      "status": null,
      "tenant_id": null
    }

changed:
  description:
    - This indicates whether the task resulted in any changes.
    - Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the BGP session.
  type: str
  returned: when external ID is provided
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching BGP sessions info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of BGP sessions available in PC.
  type: int
  returned: when all BGP sessions are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_bgp_sessions_api_instance,
)
from ..module_utils.v4.network.helpers import get_bgp_session  # noqa: E402
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
        expand=dict(type="str"),
    )

    return module_args


def get_bgp_session_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_bgp_session(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_bgp_sessions(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating BGP sessions info spec", **result)

    try:
        resp = api_instance.list_bgp_sessions(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching BGP sessions info",
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
    api_instance = get_bgp_sessions_api_instance(module)
    if module.params.get("ext_id"):
        get_bgp_session_using_ext_id(module, api_instance, result)
    else:
        get_bgp_sessions(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
