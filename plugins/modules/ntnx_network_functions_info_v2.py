#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_network_functions_info_v2
short_description: Fetch information about network function(s)
description:
    - This module fetches information about Nutanix network function(s).
    - Fetch specific network function using external ID.
    - Fetch list of multiple network functions if external ID is not provided with optional filter.
    - This module uses PC v4 APIs based SDKs.
version_added: "2.5.0"
options:
    ext_id:
        description:
            - The external ID of the network function.
        type: str
        required: false
author:
    - George Ghawali (@george-ghawali)
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
"""

EXAMPLES = r"""
- name: List all network functions
  nutanix.ncp.ntnx_network_functions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List network functions with filter
  nutanix.ncp.ntnx_network_functions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'my-network-function'"
  register: result

- name: List network functions with limit
  nutanix.ncp.ntnx_network_functions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 10
  register: result

- name: Get details of a specific network function
  nutanix.ncp.ntnx_network_functions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "a3265671-de53-41be-af9b-f06241b95356"
  register: result
"""

RETURN = r"""
response:
    description:
        - The response for fetching network function(s).
        - Single network function if external ID is provided.
        - List of multiple network functions if external ID is not provided with optional filter.
    type: dict
    returned: always

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching network functions info"
error:
    description: Error message if something goes wrong.
    type: str
    returned: always
ext_id:
    description: The external ID of the network function that was fetched.
    type: str
    returned: when fetching a specific network function
    sample: "a3265671-de53-41be-af9b-f06241b95356"
total_available_results:
    description: The total number of available network functions in PC.
    type: int
    returned: when all network functions are fetched
    sample: 10
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_network_function_api_instance,
)
from ..module_utils.v4.network.helpers import get_network_function  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_network_function_using_ext_id(module, network_functions, result):
    ext_id = module.params.get("ext_id")

    resp = get_network_function(
        module=module,
        api_instance=network_functions,
        ext_id=ext_id,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_network_functions(module, network_functions, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating network functions info Spec", **result)

    try:
        resp = network_functions.list_network_functions(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network functions info",
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
    network_functions = get_network_function_api_instance(module)
    if module.params.get("ext_id"):
        get_network_function_using_ext_id(module, network_functions, result)
    else:
        get_network_functions(module, network_functions, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
