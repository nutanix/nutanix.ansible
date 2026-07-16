#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_Gateway_info_v2
short_description: Fetch network gateways info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch network gateway info or specific network gateway in Nutanix Prism Central.
  - If ext_id is provided, fetch particular network gateway info using external ID.
  - If ext_id is not provided, fetch multiple network gateways info with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get network gateway by ext_id) -
      Required Roles: Consumer, Developer, Prism Admin, Prism Viewer, Super Admin, VPC Admin
    - >-
      B(Get list of network gateways) -
      Required Roles: Consumer, Developer, Prism Admin, Prism Viewer, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the network gateway.
    type: str
    required: false
  expand:
    description:
      - A URL query parameter that allows clients to request related resources
        (e.g., C(vpc), C(vm)) when the resource is retrieved.
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
- name: Get network gateway using ext_id
  nutanix.ncp.ntnx_Gateway_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all network gateways
  nutanix.ncp.ntnx_Gateway_info_v2:
  register: result
  ignore_errors: true

- name: List network gateways with filter
  nutanix.ncp.ntnx_Gateway_info_v2:
    filter: "name eq 'gateway_name'"
  register: result
  ignore_errors: true

- name: List network gateways with limit
  nutanix.ncp.ntnx_Gateway_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Gateway info v4 API.
    - It can be a single Gateway if external ID is provided.
    - List of multiple Gateway if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cloud_network_reference": null,
      "deployment": {
          "cluster_reference": "9a5a3f5a-1234-4d2b-b179-298db969c20d",
          "dns_servers": null,
          "interfaces": null,
          "management_interface": {
              "address": {"ipv4": {"prefix_length": 32, "value": "10.0.0.10"}, "ipv6": null},
              "default_gateway": {"ipv4": {"prefix_length": 32, "value": "10.0.0.1"}, "ipv6": null},
              "mtu": 1500,
              "subnet_reference": "1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p",
              "vlan_id": null
          },
          "ntp_servers": null,
          "should_synchronize_system_dns_servers": null,
          "should_synchronize_system_ntp_servers": null,
          "vcenter_datastore_name": null
      },
      "description": "Local BGP gateway created by Ansible",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "gateway_device_vendor": null,
      "high_availability_group": null,
      "installed_software_version": null,
      "is_active": true,
      "links": null,
      "metadata": null,
      "name": "local_gateway_ansible",
      "project_ext_id": null,
      "services": {
          "local_bgp_service": {
              "asn": 65001,
              "is_bgp_add_path_enabled": false,
              "vpc_reference": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
          },
          "local_vpn_service": null,
          "local_vtep_service": null,
          "service_address": null,
          "service_addresses": null
      },
      "status": {"message": "Gateway is up", "state": "UP"},
      "supported_software_version": null,
      "tenant_id": null,
      "vm": null,
      "vm_reference": null,
      "vpc": null,
      "vpc_reference": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching network gateways info"

error:
  description: Error details when an error occurs
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the network gateway
  type: str
  returned: when external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description: The total number of available network gateways in PC.
  type: int
  returned: when all network gateways are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import get_gateways_api_instance  # noqa: E402
from ..module_utils.v4.network.helpers import get_gateway  # noqa: E402
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


def get_gateway_using_ext_id(module, gateways_api, result):
    ext_id = module.params.get("ext_id")
    resp = get_gateway(module, gateways_api, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_gateways(module, gateways_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating network gateways info spec", **result)

    try:
        resp = gateways_api.list_gateways(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network gateways info",
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
    result = {"changed": False, "response": None, "failed": False, "error": None}
    gateways_api = get_gateways_api_instance(module)
    if module.params.get("ext_id"):
        get_gateway_using_ext_id(module, gateways_api, result)
    else:
        get_gateways(module, gateways_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
