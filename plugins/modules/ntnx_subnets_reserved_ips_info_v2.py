#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_subnets_reserved_ips_info_v2
short_description: List the currently reserved IPs on a managed subnet
version_added: 2.7.0
description:
  - This module lists every IP address that is currently reserved on a managed subnet in
    Nutanix Prism Central, together with the C(client_context) tag that owns each reservation.
  - Use this before invoking C(ntnx_subnets_unreserve_ips_v2) to confirm which IPs will be released.
  - Results can be filtered / paginated using C(filter), C(page), C(limit), C(orderby), C(select),
    or C(fetch_all).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(List reserved IPs of a managed subnet) -
    Required Roles: Network Infra Admin, Prism Admin, Super Admin, VPC Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  subnet_ext_id:
    description:
      - External ID (UUID) of the managed subnet whose reserved IPs are being listed.
      - Required — the v4 SDK C(list_reserved_ips_by_subnet_id) endpoint is scoped to a specific subnet.
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
- name: List all reserved IPs on a managed subnet
  nutanix.ncp.ntnx_subnets_reserved_ips_info_v2:
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
  register: result
  ignore_errors: true

- name: List reserved IPs owned by a specific client_context
  nutanix.ncp.ntnx_subnets_reserved_ips_info_v2:
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    filter: "clientContext eq 'ansible-context-tag'"
    limit: 25
  register: result
  ignore_errors: true

- name: Order reserved IPs by ipv4Address ascending
  nutanix.ncp.ntnx_subnets_reserved_ips_info_v2:
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    orderby: "ipv4Address"
  register: result
  ignore_errors: true

- name: List all reserved IPs with fetch_all
  nutanix.ncp.ntnx_subnets_reserved_ips_info_v2:
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - List of currently reserved IPs on the given subnet from the PC v4
      C(listReservedIpsBySubnetId) API.
    - Optionally filtered / paginated using C(filter), C(page), C(limit), C(orderby), C(select),
      or C(fetch_all).
    - The C(orderby) query parameter only supports C(ipv4Address). Sorting by C(clientContext)
      is rejected by the API with an OData error.
  returned: always
  type: list
  sample:
    - client_context: "example-range-setup"
      ext_id: null
      ipv4_address: "10.30.30.60"
      links: null
      tenant_id: null
    - client_context: "example-range-setup"
      ext_id: null
      ipv4_address: "10.30.30.61"
      links: null
      tenant_id: null

subnet_ext_id:
  description: External ID of the managed subnet whose reserved IPs were listed.
  type: str
  returned: always
  sample: "61959708-6efc-4d80-8c86-92c01f080672"

total_available_results:
  description:
    - Total number of currently reserved IPs on the given subnet
      (as reported by the PC pagination metadata).
  returned: when reserved IPs are fetched
  type: int
  sample: 7

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

error:
  description: This field typically holds information about any errors that occurred during the task execution.
  returned: when an error occurs
  type: str

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching reserved IPs on subnet"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_subnet_ip_reservation_api_instance,
)
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
        subnet_ext_id=dict(type="str", required=True),
    )
    return module_args


def list_reserved_ips(module, result, api_instance):
    """
    Fetch the list of reserved IPs on the given subnet and store it under
    result["response"]. Follows the same pagination / filter pattern as the
    other info modules in this collection.
    """
    subnet_ext_id = module.params.get("subnet_ext_id")
    result["subnet_ext_id"] = subnet_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating reserved IPs info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_reserved_ips_by_subnet_id,
            kwargs=kwargs,
            subnetExtId=subnet_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching reserved IPs on subnet",
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
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}

    api_instance = get_subnet_ip_reservation_api_instance(module)
    list_reserved_ips(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
