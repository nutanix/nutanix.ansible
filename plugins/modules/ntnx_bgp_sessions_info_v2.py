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
version_added: 2.6.0
description:
  - This module allows you to fetch information about BgpSession in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific BgpSession.
  - If C(ext_id) is not provided, list multiple BgpSession optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
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
        (e.g. C(localGateway), C(remoteGateway)) alongside the BGP session.
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
- name: Get BGP session using ext_id
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result

- name: List all BGP sessions
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
  register: result

- name: List BGP sessions with filter
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    filter: "name eq 'bgp_session_full'"
  register: result

- name: List BGP sessions with limit
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    limit: 1
  register: result

- name: List BGP sessions expanding gateway projections
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    expand: "localGateway,remoteGateway"
  register: result
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
      "name": "bgp_session_full",
      "description": "BGP session created by Ansible",
      "local_gateway_reference": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
      "remote_gateway_reference": "1d63b7e2-3d1e-4c37-9d2c-6c1b2a48f4a1",
      "local_gateway_interface_ip_address": {
          "ipv4": {"value": "10.10.10.1", "prefix_length": 24},
          "ipv6": null
      },
      "dynamic_route_priority": 500,
      "password": null,
      "status": {"message": "BGP session is up.", "state": "UP"},
      "local_gateway": null,
      "remote_gateway": null,
      "should_advertise_all_externally_routable_prefixes": false,
      "externally_routable_prefixes_to_advertise": null,
      "prepended_autonomous_system_path": [64512],
      "advertised_routes_communities": [
          {"autonomous_system_number": 64512, "community_value": 100}
      ],
      "metadata": null,
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "links": null,
      "tenant_id": null
    }

changed:
  description:
    - This indicates whether the task resulted in any changes.
    - Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching BGP sessions info"

error:
  description: This field typically holds information about errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the BGP session.
  type: str
  returned: when external ID is provided
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

total_available_results:
  description: The total number of available BGP sessions in PC.
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


def get_bgp_session_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    kwargs = {}
    if module.params.get("expand"):
        kwargs["_expand"] = module.params.get("expand")
    try:
        resp = api_instance.get_bgp_session_by_id(extId=ext_id, **kwargs).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching BGP session info using ext_id",
        )
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
