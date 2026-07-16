#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_bgp_sessions_info_v2
short_description: Fetch BGP session info in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to fetch information about BGP sessions in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific BGP session.
  - If C(ext_id) is not provided, list multiple BGP sessions optionally filtered / paginated
    / limited / ordered / expanded.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get BGP session by ext_id) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, VPC Admin
    - >-
      B(List BGP sessions) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the BGP session.
      - If provided, only that single BGP session is returned.
    type: str
  expand:
    description:
      - OData $expand system query option — request related resources for each returned BGP session.
      - Applies only to list operations.
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
- name: Get BGP session using ext_id
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all BGP sessions
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List BGP sessions with filter
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'bgp_session_ansible_min'"
  register: result
  ignore_errors: true

- name: List BGP sessions with limit
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: List BGP sessions ordered by name descending
  nutanix.ncp.ntnx_bgp_sessions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    orderby: "name desc"
  register: result
  ignore_errors: true
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
      "name": "bgp_session_ansible_full",
      "description": "BGP session created by Ansible with full attributes",
      "local_gateway_reference": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
      "remote_gateway_reference": "8300384a-56ee-4750-aeb8-3d1c42908bee",
      "local_gateway_interface_ip_address": {
          "ipv4": {"value": "10.10.10.1", "prefix_length": 32},
          "ipv6": null
      },
      "dynamic_route_priority": 500,
      "should_advertise_all_externally_routable_prefixes": false,
      "externally_routable_prefixes_to_advertise": [
          {
              "ipv4": {"ip": {"value": "192.168.10.0", "prefix_length": 32}, "prefix_length": 24},
              "ipv6": null
          }
      ],
      "prepended_autonomous_system_path": [65001, 65002],
      "advertised_routes_communities": [
          {"autonomous_system_number": 65001, "community_value": 100}
      ],
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "status": null,
      "local_gateway": null,
      "remote_gateway": null,
      "metadata": null,
      "links": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Human-readable status/error message if any.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching BGP sessions info"

error:
  description: Error details if any error occurred.
  type: str
  returned: when an error occurs

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the BGP session.
  type: str
  returned: when external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description: The total number of BGP sessions available in the PC.
  type: int
  returned: when listing BGP sessions
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
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
            ("ext_id", "expand"),
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
