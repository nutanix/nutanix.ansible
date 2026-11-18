#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_layer2_stretches_learned_mac_addresses_info_v2
short_description: Fetch learned MAC addresses of a Layer2 Stretch in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch learned MAC addresses of a Layer2 Stretch in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch a particular learned MAC address info using its external ID.
  - If C(ext_id) is not provided, fetch multiple learned MAC addresses info with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(View Layer2 Stretch Mac Address) -
      Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin, Prism Viewer, Project Admin, Super Admin, Tenant Admin, User, VPC Admin
    - >-
      B(View Layer2 Stretch Mac Address) (List) -
      Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin, Prism Viewer, Project Admin, Super Admin, Tenant Admin, User, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the learned MAC address.
      - If provided, a single learned MAC address is returned.
    type: str
    required: false
  layer2_stretch_ext_id:
    description:
      - The external ID of the parent Layer2 Stretch whose learned MAC addresses should be fetched or listed.
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
- name: Get learned MAC address using ext_id
  nutanix.ncp.ntnx_layer2_stretches_learned_mac_addresses_info_v2:
    layer2_stretch_ext_id: "6be8fe36-9612-4fab-aabb-2c02207c794d"
    ext_id: "d4f3f04f-1222-8544-7896-28b62bcc3e3e"
  register: result
  ignore_errors: true

- name: List all learned MAC addresses for a given Layer2 Stretch
  nutanix.ncp.ntnx_layer2_stretches_learned_mac_addresses_info_v2:
    layer2_stretch_ext_id: "6be8fe36-9612-4fab-aabb-2c02207c794d"
  register: result
  ignore_errors: true

- name: List learned MAC addresses for a Layer2 Stretch with filter
  nutanix.ncp.ntnx_layer2_stretches_learned_mac_addresses_info_v2:
    layer2_stretch_ext_id: "6be8fe36-9612-4fab-aabb-2c02207c794d"
    filter: "remoteGatewayReference eq '1e9b42a2-a197-427c-b0ae-5ce89fb5fe42'"
  register: result
  ignore_errors: true

- name: List learned MAC addresses for a Layer2 Stretch with limit
  nutanix.ncp.ntnx_layer2_stretches_learned_mac_addresses_info_v2:
    layer2_stretch_ext_id: "6be8fe36-9612-4fab-aabb-2c02207c794d"
    limit: 1
  register: result
  ignore_errors: true

- name: List all learned MAC addresses for a Layer2 Stretch with fetch_all
  nutanix.ncp.ntnx_layer2_stretches_learned_mac_addresses_info_v2:
    layer2_stretch_ext_id: "6be8fe36-9612-4fab-aabb-2c02207c794d"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC learned MAC addresses info v4 API.
    - It can be a single learned MAC address if external ID is provided.
    - List of multiple learned MAC addresses if external ID is not provided with optional filter or limit.
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

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching learned MAC addresses info"

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
  description: External ID of the learned MAC address
  type: str
  returned: when external ID is provided
  sample: "d4f3f04f-1222-8544-7896-28b62bcc3e3e"

layer2_stretch_ext_id:
  description: External ID of the parent Layer2 Stretch
  type: str
  returned: always
  sample: "6be8fe36-9612-4fab-aabb-2c02207c794d"

total_available_results:
  description: The total number of available learned MAC addresses for the parent Layer2 Stretch.
  type: int
  returned: when all learned MAC addresses are fetched
  sample: 3
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
    list_entities,
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


def get_learned_mac_address_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    layer2_stretch_ext_id = module.params.get("layer2_stretch_ext_id")
    resp = get_learned_mac_address(module, api_instance, ext_id, layer2_stretch_ext_id)
    result["ext_id"] = ext_id
    result["layer2_stretch_ext_id"] = layer2_stretch_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_learned_mac_addresses(module, api_instance, result):
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
        resp = list_entities(
            api_instance.list_learned_mac_addresses_by_layer2_stretch_id,
            kwargs=kwargs,
            layer2StretchExtId=layer2_stretch_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching learned MAC addresses info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


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
        get_learned_mac_address_using_ext_id(module, api_instance, result)
    else:
        get_learned_mac_addresses(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
