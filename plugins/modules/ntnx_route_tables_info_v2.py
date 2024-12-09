#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_route_tables_info_v2
short_description: Route tables info module
version_added: 2.0.0
description: This module fetches route tables information
options:
    ext_id:
        description:
            - Route table external ID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: List all route tables
  ntnx_route_tables_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: route_tables

- name: Fetch route table by external_id
  ntnx_route_tables_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "251d4a4f-244f-4c84-70a9-8c8f68f9dff0"
  register: route_table

- name: List all route tables with filter
  ntnx_route_tables_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: vpcReference eq '251d4a4f-244f-4c84-70a9-8c8f68f9dff0'
  register: route_tables_filter
"""
RETURN = r"""
response:
    description:
        - Response for fetching route table info
        - Returns route table or list of multiple route tables details.
    type: dict
    returned: always
    sample:
        {
            "extId": "7f9a76a3-922b-4aba-8d79-e7eb5cdaf201",
            "metadata": {
                "ownerReferenceId": "00000000-0000-0000-0000-000000000000",
                "ownerUserName": "admin"
            },
            "vpcReference": "66a926de-c188-4121-8456-0b97cdf0f807"
        }

ext_id:
    description: route table external ID
    type: str
    returned: always
    sample: "63acaca5-ed45-415e-bfbd-19c9d9fd3dfd"

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
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_route_tables_api_instance,
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


def get_route_table_using_ext_id(module, route_table_api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    try:
        resp = route_table_api_instance.get_route_table_by_id(ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching route table info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_route_tables(module, route_table_api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating route table info Spec", **result)

    try:
        resp = route_table_api_instance.list_route_tables(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching route tables info",
        )
    if (resp is None) or (resp.to_dict().get("data") is None):
        result["response"] = []
    else:
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
    route_table_api_instance = get_route_tables_api_instance(module)
    if module.params.get("ext_id"):
        get_route_table_using_ext_id(module, route_table_api_instance, result)
    else:
        get_route_tables(module, route_table_api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
