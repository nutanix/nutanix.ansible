#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_learned_mac_address_for_layer2_stretches_info_v2
short_description: Fetch learned MAC address(es) for a Layer2Stretch in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about LearnedMacAddressForLayer2Stretch in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific LearnedMacAddressForLayer2Stretch.
  - If C(ext_id) is not provided, list multiple LearnedMacAddressForLayer2Stretch optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get a specified learned MAC address of the specified Layer2Stretch) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, VPC Admin
  - >-
    B(Get learned MAC addresses of the specified Layer2Stretch) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, VPC Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - External ID of the specified learned MAC address.
      - When provided, the module fetches a single learned MAC address entry.
    type: str
  layer2_stretch_ext_id:
    description:
      - External ID of the parent Layer2Stretch configuration whose learned MAC addresses are being fetched.
      - Required for both fetching a single learned MAC address and listing all learned MAC addresses of a Layer2Stretch.
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
- name: List all learned MAC addresses for a Layer2Stretch
  nutanix.ncp.ntnx_learned_mac_address_for_layer2_stretches_info_v2:
    layer2_stretch_ext_id: "b6b7f96d-5a5f-4d1a-8b57-8a4c56d1abcd"
  register: result
  ignore_errors: true

- name: Get a specific learned MAC address for a Layer2Stretch using ext_id
  nutanix.ncp.ntnx_learned_mac_address_for_layer2_stretches_info_v2:
    layer2_stretch_ext_id: "b6b7f96d-5a5f-4d1a-8b57-8a4c56d1abcd"
    ext_id: "8c3f01f2-7d1c-46b8-91e6-4c1e2d47aaaa"
  register: result
  ignore_errors: true

- name: List learned MAC addresses for a Layer2Stretch with a filter
  nutanix.ncp.ntnx_learned_mac_address_for_layer2_stretches_info_v2:
    layer2_stretch_ext_id: "b6b7f96d-5a5f-4d1a-8b57-8a4c56d1abcd"
    filter: "macType eq Networking.Config.MacType'LEARNED'"
  register: result
  ignore_errors: true

- name: List learned MAC addresses for a Layer2Stretch with a limit
  nutanix.ncp.ntnx_learned_mac_address_for_layer2_stretches_info_v2:
    layer2_stretch_ext_id: "b6b7f96d-5a5f-4d1a-8b57-8a4c56d1abcd"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC LearnedMacAddressForLayer2Stretch info v4 API.
    - It can be a single LearnedMacAddressForLayer2Stretch if external ID is provided.
    - List of multiple LearnedMacAddressForLayer2Stretch if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "8c3f01f2-7d1c-46b8-91e6-4c1e2d47aaaa",
        "links": null,
        "mac_type": "LEARNED",
        "metadata": null,
        "remote_gateway_reference": "7f9a76a3-922b-4aba-8d79-e7eb5cdaf201",
        "tenant_id": null,
        "value": "50:6b:8d:12:34:56",
        "vtep_ip_address": {
            "ipv4": {
                "prefix_length": 32,
                "value": "10.44.76.30"
            },
            "ipv6": null
        }
    }

changed:
  description: Whether the task resulted in any changes. Always False for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the learned MAC address entry (only when a single entity was requested).
  type: str
  returned: when external ID is provided
  sample: "8c3f01f2-7d1c-46b8-91e6-4c1e2d47aaaa"

layer2_stretch_ext_id:
  description: External ID of the parent Layer2Stretch whose learned MAC addresses were fetched.
  type: str
  returned: always
  sample: "b6b7f96d-5a5f-4d1a-8b57-8a4c56d1abcd"

total_available_results:
  description: The total number of learned MAC addresses available for the specified Layer2Stretch.
  type: int
  returned: when learned MAC addresses are listed (no ext_id provided)
  sample: 5

msg:
  description: Status/error message from the module.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching learned MAC addresses info for Layer2Stretch"

error:
  description: Error details when an API call fails.
  type: str
  returned: when an error occurs

failed:
  description: Whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_mac_addresses_api_instance,
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
        layer2_stretch_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_learned_mac_address_for_layer2_stretch_using_ext_id(
    module, mac_addresses_api, result
):
    ext_id = module.params.get("ext_id")
    layer2_stretch_ext_id = module.params.get("layer2_stretch_ext_id")
    result["ext_id"] = ext_id
    result["layer2_stretch_ext_id"] = layer2_stretch_ext_id
    try:
        resp = mac_addresses_api.get_learned_mac_address_for_layer2_stretch_by_id(
            extId=ext_id, layer2StretchExtId=layer2_stretch_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching learned MAC address info for "
                "Layer2Stretch using ext_id"
            ),
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_learned_mac_addresses_for_layer2_stretch(module, mac_addresses_api, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    layer2_stretch_ext_id = module.params.get("layer2_stretch_ext_id")
    result["layer2_stretch_ext_id"] = layer2_stretch_ext_id
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating learned MAC addresses info spec", **result
        )

    try:
        resp = mac_addresses_api.list_learned_mac_addresses_by_layer2_stretch_id(
            layer2StretchExtId=layer2_stretch_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching learned MAC addresses info for "
                "Layer2Stretch"
            ),
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
    mac_addresses_api = get_mac_addresses_api_instance(module)
    if module.params.get("ext_id"):
        get_learned_mac_address_for_layer2_stretch_using_ext_id(
            module, mac_addresses_api, result
        )
    else:
        get_learned_mac_addresses_for_layer2_stretch(module, mac_addresses_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
