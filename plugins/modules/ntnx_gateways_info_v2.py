#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_gateways_info_v2
short_description: Fetch network gateways information in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Gateway in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Gateway.
  - If C(ext_id) is not provided, list multiple Gateway optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get network gateway by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
      Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - >-
      B(Get list of Network Gateways) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
      Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the network gateway.
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
- name: Get network gateway using ext_id
  nutanix.ncp.ntnx_gateways_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result

- name: List all network gateways
  nutanix.ncp.ntnx_gateways_info_v2:
  register: result

- name: List network gateways with filter
  nutanix.ncp.ntnx_gateways_info_v2:
    filter: "name eq 'gw_local_vpn_ansible'"
  register: result

- name: List network gateways with limit
  nutanix.ncp.ntnx_gateways_info_v2:
    limit: 1
  register: result

- name: List network gateways with expand and select
  nutanix.ncp.ntnx_gateways_info_v2:
    expand: "vpc"
    select: "name,extId"
  register: result
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
      "deployment": null,
      "description": "Remote BGP gateway created by Ansible example playbook",
      "ext_id": "c13bf194-4017-4efb-abbf-d44c837818a9",
      "gateway_device_vendor": "GENERIC",
      "high_availability_group": null,
      "installed_software_version": null,
      "is_active": null,
      "links": null,
      "metadata": {
          "category_ids": null,
          "owner_reference_id": "00000000-0000-0000-0000-000000000000",
          "owner_user_name": "admin",
          "project_name": "_internal",
          "project_reference_id": "00000000-0000-0000-0000-000000000000"
      },
      "name": "gateway_ansible_example",
      "projectExtId": "00000000-0000-0000-0000-000000000000",
      "services": {
          "remote_bgp_service": {
              "address": {"ipv4": {"prefix_length": 32, "value": "192.0.2.10"}, "ipv6": null},
              "asn": 65001
          },
          "remote_vpn_service": null,
          "remote_vtep_service": null
      },
      "status": null,
      "supported_software_version": null,
      "tenant_id": null,
      "vm": null,
      "vm_reference": null,
      "vpc": null,
      "vpc_reference": null
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
  sample: "Api Exception raised while fetching gateways info"

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
    )

    return module_args


def get_gateway_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_gateway(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_gateways(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating gateways info spec", **result)

    try:
        resp = api_instance.list_gateways(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching gateways info",
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
    api_instance = get_gateways_api_instance(module)
    if module.params.get("ext_id"):
        get_gateway_using_ext_id(module, api_instance, result)
    else:
        get_gateways(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
