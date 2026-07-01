#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_BgpSession_info_v2
short_description: Fetch BGP session info in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to fetch BGP session info or list BGP sessions in Nutanix Prism Central.
  - If ext_id is provided, fetch a particular BGP session info using external ID.
  - If ext_id is not provided, fetch multiple BGP sessions with optional filter or limit.
  - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external identifier of the BGP session.
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
  nutanix.ncp.ntnx_BgpSession_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "c3d4e5f6-a7b8-9012-cdef-123456789012"
  register: result
  ignore_errors: true

- name: List all BGP sessions
  nutanix.ncp.ntnx_BgpSession_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List BGP sessions with filter
  nutanix.ncp.ntnx_BgpSession_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'bgp_session_1'"
  register: result
  ignore_errors: true

- name: List BGP sessions with limit
  nutanix.ncp.ntnx_BgpSession_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 5
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

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the BGP session
  type: str
  returned: when external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

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
    )

    return module_args


def get_bgp_session_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_bgp_session(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_bgp_sessions(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

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
