#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_reserve_ips_by_subnet_ids_info_v2
short_description: Fetch reserved IPs on a managed subnet in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about reserved IPs on a managed subnet in Nutanix Prism Central.
  - The subnet ext_id (C(ext_id)) is required — reservations are always scoped to a subnet.
  - Supports OData pagination and filtering via the standard v4 API query parameters.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List reserved IPs on a subnet) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer,
      Project Admin, Super Admin, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the managed subnet whose reserved IPs are being fetched.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all reserved IPs on a subnet
  nutanix.ncp.ntnx_reserve_ips_by_subnet_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
  register: result

- name: List reserved IPs on a subnet with pagination
  nutanix.ncp.ntnx_reserve_ips_by_subnet_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    limit: 5
    page: 0
  register: result

- name: List reserved IPs on a subnet filtered by client_context
  nutanix.ncp.ntnx_reserve_ips_by_subnet_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    filter: "clientContext eq 'ansible_reserve_test'"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ReserveIpsBySubnetId info v4 API.
    - It is the list of reserved IPs on the subnet identified by C(ext_id).
  returned: always
  type: dict
  sample:
    [
      {
        "client_context": "ansible_example_reserve",
        "ext_id": null,
        "ipv4_address": "192.168.214.22",
        "links": null,
        "tenant_id": null
      },
      {
        "client_context": "ansible_example_reserve",
        "ext_id": null,
        "ipv4_address": "192.168.214.21",
        "links": null,
        "tenant_id": null
      }
    ]

ext_id:
  description: External ID of the subnet whose reserved IPs were fetched.
  type: str
  returned: always
  sample: "6be3e46b-794a-43f9-ab3e-04b94acf9f2e"

changed:
  description: This indicates whether the task resulted in any changes. Info modules never change state.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while listing reserved IPs on subnet"

error:
  description: Error message.
  type: str
  returned: When an error occurs

failed:
  description: Indicates if the request failed.
  type: bool
  returned: always
  sample: false

total_available_results:
  description: The total number of reserved IPs available on the subnet.
  type: int
  returned: always
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_subnet_ip_reservation_api_instance,
)
from ..module_utils.v4.network.helpers import list_reserved_ips_by_subnet  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_reserved_ips_by_subnet_id(module, api_instance, result):
    subnet_ext_id = module.params.get("ext_id")
    result["ext_id"] = subnet_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating reserved IPs by subnet info spec", **result
        )
    kwargs.pop("_ext_id", None)

    resp = list_reserved_ips_by_subnet(
        module=module,
        api_instance=api_instance,
        subnet_ext_id=subnet_ext_id,
        **kwargs,
    )

    total_available_results = 0
    if resp is not None and getattr(resp, "metadata", None) is not None:
        total_available_results = (
            getattr(resp.metadata, "total_available_results", None) or 0
        )
    result["total_available_results"] = total_available_results

    data = None
    if resp is not None:
        data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_subnet_ip_reservation_api_instance(module)
    get_reserved_ips_by_subnet_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
