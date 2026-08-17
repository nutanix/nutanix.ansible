#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vnics_by_subnet_ids_info_v2
short_description: Fetch virtual NICs attached to a subnet in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about VnicsBySubnetId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VnicsBySubnetId.
  - If C(ext_id) is not provided, list multiple VnicsBySubnetId optionally filtered / paginated.
  - Underlying SDK method is C(list_vnics_by_subnet_id) on C(SubnetsApi).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List virtual NICs on a subnet) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer,
      Project Admin, Super Admin, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  subnet_ext_id:
    description:
      - The external ID (UUID) of the parent subnet whose virtual NICs will be listed.
      - Required.
    type: str
    required: true
  ext_id:
    description:
      - External ID of a specific virtual NIC on the subnet.
      - When provided, the module filters the returned list to only the matching virtual NIC.
      - The Nutanix v4 networking API does not expose a Get-vNIC-by-ID endpoint under this
        resource, so the filtering happens client-side after the list call.
    type: str
    required: false
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
- name: List all virtual NICs attached to a subnet
  nutanix.ncp.ntnx_vnics_by_subnet_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    subnet_ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
  register: result
  ignore_errors: true

- name: List virtual NICs on a subnet with a limit
  nutanix.ncp.ntnx_vnics_by_subnet_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    subnet_ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    limit: 1
  register: result
  ignore_errors: true

- name: List virtual NICs on a subnet using an OData filter (by MAC address)
  nutanix.ncp.ntnx_vnics_by_subnet_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    subnet_ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    filter: "macAddress eq '00:11:22:33:44:55'"
  register: result
  ignore_errors: true

- name: Fetch a specific virtual NIC on a subnet by its external ID
  nutanix.ncp.ntnx_vnics_by_subnet_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    subnet_ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    ext_id: "1e2f3a4b-5c6d-7e8f-9a0b-c1d2e3f4a5b6"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VnicsBySubnetId info v4 API.
    - It can be a single VnicsBySubnetId if external ID is provided.
    - List of multiple VnicsBySubnetId if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    [
        {
            "assigned_ipv4_addresses": null,
            "assigned_secondary_ipv4_addresses": null,
            "ext_id": "868f0ac7-5f6a-4f49-7003-788a8091841f",
            "learned_ipv4_addresses": null,
            "links": null,
            "mac_address": "50:6b:8d:90:dc:fd",
            "metadata": null,
            "tenant_id": null,
            "vm_reference": "4d5a5911-43f3-4788-8455-a28c81633900"
        },
        {
            "assigned_ipv4_addresses": null,
            "assigned_secondary_ipv4_addresses": null,
            "ext_id": "1a77788d-998a-4701-6fa2-9c4e839b8c44",
            "learned_ipv4_addresses": [
                {
                    "ipv4": {"prefix_length": null, "value": "10.44.76.28"},
                    "ipv6": null
                },
                {
                    "ipv4": {"prefix_length": null, "value": "10.44.76.29"},
                    "ipv6": null
                }
            ],
            "links": null,
            "mac_address": "50:6b:8d:de:93:08",
            "metadata": null,
            "tenant_id": null,
            "vm_reference": "ea75db92-0f0d-4dd5-8ad1-7feef385e797"
        }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching virtual NICs for subnet"

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
  description: External ID of the virtual NIC when a specific vNIC is requested.
  type: str
  returned: when ext_id is provided
  sample: "1a77788d-998a-4701-6fa2-9c4e839b8c44"

subnet_ext_id:
  description: External ID (UUID) of the parent subnet whose virtual NICs were listed.
  type: str
  returned: always
  sample: "c15625a4-a222-4351-a00a-ef51ffabe0d3"

total_available_results:
  description: The total number of available virtual NICs on the given subnet in PC.
  type: int
  returned: when the list operation is executed
  sample: 4
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import get_subnet_api_instance  # noqa: E402
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


def _list_vnics(module, subnets_api, subnet_ext_id):
    """Call the underlying list_vnics_by_subnet_id SDK method with OData params."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        return None, err

    try:
        resp = subnets_api.list_vnics_by_subnet_id(subnetExtId=subnet_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virtual NICs for subnet {0}".format(
                subnet_ext_id
            ),
        )
    return resp, None


def get_vnic_by_ext_id(module, subnets_api, result):
    """Return the vNIC matching module.params['ext_id'] from the subnet's vNIC list."""
    subnet_ext_id = module.params.get("subnet_ext_id")
    vnic_ext_id = module.params.get("ext_id")
    result["subnet_ext_id"] = subnet_ext_id
    result["ext_id"] = vnic_ext_id

    resp, err = _list_vnics(module, subnets_api, subnet_ext_id)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating virtual NICs info spec for subnet {0}".format(
                subnet_ext_id
            ),
            **result,
        )

    total_available_results = getattr(resp.metadata, "total_available_results", None)
    if total_available_results is not None:
        result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data") or []
    match = None
    for item in data:
        if item.get("ext_id") == vnic_ext_id:
            match = item
            break

    if not match:
        result["response"] = None
        module.fail_json(
            msg="Virtual NIC with ext_id '{0}' was not found on subnet '{1}'".format(
                vnic_ext_id, subnet_ext_id
            ),
            **result,
        )

    result["response"] = match


def get_vnics(module, subnets_api, result):
    """List all vNICs on the given subnet, with optional OData filter/limit/page/orderby/select."""
    subnet_ext_id = module.params.get("subnet_ext_id")
    result["subnet_ext_id"] = subnet_ext_id

    resp, err = _list_vnics(module, subnets_api, subnet_ext_id)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating virtual NICs info spec for subnet {0}".format(
                subnet_ext_id
            ),
            **result,
        )

    total_available_results = getattr(resp.metadata, "total_available_results", None)
    if total_available_results is not None:
        result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "subnet_ext_id": None,
    }
    subnets_api = get_subnet_api_instance(module)
    if module.params.get("ext_id"):
        get_vnic_by_ext_id(module, subnets_api, result)
    else:
        get_vnics(module, subnets_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
