#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_learned_mac_addresses_by_layer2_stretch_ids_info_v2
short_description: Fetch learned MAC addresses of a Layer2 Stretch in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about LearnedMacAddressesByLayer2StretchId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific LearnedMacAddressesByLayer2StretchId.
  - If C(ext_id) is not provided, list multiple LearnedMacAddressesByLayer2StretchId optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get a learned MAC address of a Layer2Stretch by ext_id) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, VPC Admin
  - >-
    B(List learned MAC addresses of a Layer2Stretch) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, VPC Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - External ID of the learned MAC address to fetch.
      - When provided, the module fetches only the specified learned MAC address.
      - When omitted, the module lists all learned MAC addresses for the given Layer2Stretch.
    type: str
  layer2_stretch_ext_id:
    description:
      - External ID of the Layer2Stretch that owns the learned MAC addresses.
      - This field is mandatory for both C(get by ext_id) and C(list) operations because
        every learned MAC address is scoped to a specific Layer2Stretch.
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
- name: List all learned MAC addresses of a Layer2 Stretch
  nutanix.ncp.ntnx_learned_mac_addresses_by_layer2_stretch_ids_info_v2:
    layer2_stretch_ext_id: "6be8fe36-9612-4fab-aabb-2c02207c794d"
  register: result

- name: Fetch a specific learned MAC address by external ID
  nutanix.ncp.ntnx_learned_mac_addresses_by_layer2_stretch_ids_info_v2:
    layer2_stretch_ext_id: "6be8fe36-9612-4fab-aabb-2c02207c794d"
    ext_id: "d4f3f04f-1222-8544-7896-28b62bcc3e3e"
  register: result

- name: List learned MAC addresses with a filter on macType
  nutanix.ncp.ntnx_learned_mac_addresses_by_layer2_stretch_ids_info_v2:
    layer2_stretch_ext_id: "6be8fe36-9612-4fab-aabb-2c02207c794d"
    filter: "macType eq Networking.Config.MacType'LEARNED'"
  register: result

- name: List learned MAC addresses with a limit of 1
  nutanix.ncp.ntnx_learned_mac_addresses_by_layer2_stretch_ids_info_v2:
    layer2_stretch_ext_id: "6be8fe36-9612-4fab-aabb-2c02207c794d"
    limit: 1
  register: result

- name: List learned MAC addresses ordered by value ascending
  nutanix.ncp.ntnx_learned_mac_addresses_by_layer2_stretch_ids_info_v2:
    layer2_stretch_ext_id: "6be8fe36-9612-4fab-aabb-2c02207c794d"
    orderby: "value asc"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC LearnedMacAddressesByLayer2StretchId info v4 API.
    - It can be a single LearnedMacAddressesByLayer2StretchId if external ID is provided.
    - List of multiple LearnedMacAddressesByLayer2StretchId if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "d4f3f04f-1222-8544-7896-28b62bcc3e3e",
      "value": "50:6b:8d:9f:00:11",
      "mac_type": "LEARNED",
      "remote_gateway_reference": "2338b378-0cec-4894-ba06-dbecd72b851f",
      "vtep_ip_address": {
          "ipv4": {
              "value": "10.44.76.100",
              "prefix_length": 32
          },
          "ipv6": null
      },
      "metadata": null,
      "tenant_id": null,
      "links": null
    }

ext_id:
  description: External ID of the learned MAC address (only when C(ext_id) input was provided).
  type: str
  returned: when external ID is provided
  sample: "d4f3f04f-1222-8544-7896-28b62bcc3e3e"

layer2_stretch_ext_id:
  description: External ID of the parent Layer2Stretch.
  type: str
  returned: always
  sample: "6be8fe36-9612-4fab-aabb-2c02207c794d"

total_available_results:
  description: The total number of available learned MAC addresses on the specified Layer2Stretch.
  type: int
  returned: when all learned MAC addresses are fetched
  sample: 3

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Status/error message returned by the module.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching learned MAC addresses info"

error:
  description: Error details from the SDK/API call.
  type: str
  returned: when an error occurs
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_mac_addresses_api_instance,
)
from ..module_utils.v4.network.helpers import get_learned_mac_address  # noqa: E402
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
        layer2_stretch_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_learned_mac_address_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    layer2_stretch_ext_id = module.params.get("layer2_stretch_ext_id")
    result["ext_id"] = ext_id
    result["layer2_stretch_ext_id"] = layer2_stretch_ext_id
    resp = get_learned_mac_address(
        module=module,
        api_instance=api_instance,
        ext_id=ext_id,
        layer2_stretch_ext_id=layer2_stretch_ext_id,
    )
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_learned_mac_addresses(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    layer2_stretch_ext_id = module.params.get("layer2_stretch_ext_id")
    result["layer2_stretch_ext_id"] = layer2_stretch_ext_id
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating learned MAC addresses info spec", **result
        )

    # The list SDK method does not accept _select; drop it if BaseInfoModule added it.
    kwargs.pop("_select", None)

    try:
        resp = api_instance.list_learned_mac_addresses_by_layer2_stretch_id(
            layer2StretchExtId=layer2_stretch_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching learned MAC addresses info",
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
    api_instance = get_mac_addresses_api_instance(module)
    if module.params.get("ext_id"):
        get_learned_mac_address_by_ext_id(module, api_instance, result)
    else:
        list_learned_mac_addresses(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
