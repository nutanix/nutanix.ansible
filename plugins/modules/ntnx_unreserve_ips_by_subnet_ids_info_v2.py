#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_unreserve_ips_by_subnet_ids_info_v2
short_description: List the currently reserved IPs on a managed subnet
version_added: 2.5.0
description:
  - This module allows you to fetch information about UnreserveIpsBySubnetId in Nutanix Prism Central.
  - It lists every IP address that is currently reserved on the given managed subnet, together with the
    C(client_context) tag that owns each reservation.
  - Use this before invoking C(ntnx_unreserve_ips_by_subnet_id_v2) to confirm which IPs will be released.
  - If C(ext_id) is not provided, list multiple UnreserveIpsBySubnetId optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(List reserved IPs of a managed subnet) -
    Required Roles: Account Owner, Administrator, Consumer, Developer, Network Infra Admin,
    Network Shared Resources Viewer, Operator, Prism Admin, Prism Viewer, Project Admin,
    Project Manager, Super Admin, VPC Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  subnet_ext_id:
    description:
      - External ID (UUID) of the managed subnet whose reserved IPs are being listed.
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
  nutanix.ncp.ntnx_unreserve_ips_by_subnet_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
  register: result

- name: List reserved IPs owned by a specific client_context
  nutanix.ncp.ntnx_unreserve_ips_by_subnet_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    filter: "clientContext eq 'ansible-context-tag'"
    limit: 25

- name: Order reserved IPs by client_context descending
  nutanix.ncp.ntnx_unreserve_ips_by_subnet_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    orderby: "clientContext desc"
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC UnreserveIpsBySubnetId info v4 API.
    - It is a list of currently reserved IPs on the given subnet.
    - Optionally filtered / paginated using C(filter), C(page), C(limit), C(orderby), or C(select).
    - The C(orderby) query parameter only supports fields the SDK exposes for sorting — namely
      C(ipv4Address). Sorting by C(clientContext) is rejected by the API with an OData error.
  returned: always
  type: dict
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

total_available_results:
  description:
    - Total number of currently reserved IPs on the given subnet.
  returned: always
  type: int
  sample: 7

changed:
  description: Info modules never change cluster state.
  returned: always
  type: bool
  sample: false

failed:
  description: Whether the module failed.
  returned: always
  type: bool
  sample: false

error:
  description: Error details when the module fails.
  returned: When an error occurs
  type: str

msg:
  description: Status or error message emitted by the module.
  returned: contextual
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
    raise_api_exception,
    strip_internal_attributes,
)

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
            msg="Api Exception raised while fetching reserved IPs on subnet",
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
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}

    api_instance = get_subnet_ip_reservation_api_instance(module)
    list_reserved_ips(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
