#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_reserved_ips_by_subnet_ids_info_v2
short_description: Fetch reserved IP addresses on a managed subnet in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about ReservedIpsBySubnetId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ReservedIpsBySubnetId.
  - If C(ext_id) is not provided, list multiple ReservedIpsBySubnetId optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List reserved IPs on a Subnet) -
    Required Permissions: View_Subnet_Reserved_Ip. VPC Admin and Network Infra Admin roles include this by default.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  subnet_ext_id:
    description:
      - The external ID (UUID) of the managed subnet whose reserved IPs are being listed.
    type: str
    required: true
  ext_id:
    description:
      - External ID of a specific reserved IP entry on the subnet.
      - When provided, the module filters the list by that IP entry's ext_id and returns
        just that entry (or an empty list if it does not exist).
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
- name: List all reserved IPs on a subnet
  nutanix.ncp.ntnx_reserved_ips_by_subnet_ids_info_v2:
    subnet_ext_id: "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d"
  register: result

- name: List reserved IPs on a subnet with limit
  nutanix.ncp.ntnx_reserved_ips_by_subnet_ids_info_v2:
    subnet_ext_id: "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d"
    limit: 10
  register: result

- name: List reserved IPs on a subnet filtered by client_context
  nutanix.ncp.ntnx_reserved_ips_by_subnet_ids_info_v2:
    subnet_ext_id: "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d"
    filter: "clientContext eq 'ansible-count'"
  register: result

- name: Fetch a specific reserved IP entry by ext_id
  nutanix.ncp.ntnx_reserved_ips_by_subnet_ids_info_v2:
    subnet_ext_id: "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d"
    ext_id: "6c1f5c65-4b47-4b0a-8b21-2fb9dd1a4d55"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ReservedIpsBySubnetId info v4 API.
    - It can be a single ReservedIpsBySubnetId if external ID is provided.
    - List of multiple ReservedIpsBySubnetId if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    [
      {
        "client_context": "ansible-count",
        "ext_id": "6c1f5c65-4b47-4b0a-8b21-2fb9dd1a4d55",
        "ipv4_address": "10.44.10.50",
        "links": null,
        "tenant_id": null
      },
      {
        "client_context": "ansible-list",
        "ext_id": "3f8c4e0a-6f34-4dbb-91f9-9a6da223dc42",
        "ipv4_address": "10.44.10.51",
        "links": null,
        "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes (always False for info modules).
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching reserved IPs by subnet id info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the reserved IP entry when a single entity is requested.
  type: str
  returned: when ext_id is provided
  sample: "6c1f5c65-4b47-4b0a-8b21-2fb9dd1a4d55"

total_available_results:
  description: The total number of reserved IPs available on the target subnet.
  type: int
  returned: when reserved IPs are listed
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_subnet_ip_reservation_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        subnet_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_reserved_ip_by_ext_id(module, api_instance, result):
    """
    The SubnetIPReservationApi only offers a list method; there is no dedicated
    "get reserved ip by ext_id" endpoint. We list with an OData $filter on
    ``extId`` and return the single matching entry.
    """
    subnet_ext_id = module.params.get("subnet_ext_id")
    reserved_ip_ext_id = module.params.get("ext_id")
    result["ext_id"] = reserved_ip_ext_id

    kwargs = {"_filter": "extId eq '{0}'".format(reserved_ip_ext_id)}
    try:
        resp = api_instance.list_reserved_ips_by_subnet_id(
            subnetExtId=subnet_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching reserved IP by ext_id",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data[0] if data else {}


def get_reserved_ips(module, api_instance, result):
    subnet_ext_id = module.params.get("subnet_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating reserved IPs info spec", **result)

    try:
        resp = api_instance.list_reserved_ips_by_subnet_id(
            subnetExtId=subnet_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching reserved IPs by subnet id info",
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
    api_instance = get_subnet_ip_reservation_api_instance(module)
    if module.params.get("ext_id"):
        get_reserved_ip_by_ext_id(module, api_instance, result)
    else:
        get_reserved_ips(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
