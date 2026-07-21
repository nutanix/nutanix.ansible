#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vnics_info_v2
short_description: Fetch information about virtual NICs (vNICs) attached to a subnet in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Vnic in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Vnic (looked up under its parent
    C(subnet_ext_id)).
  - If C(ext_id) is not provided, list multiple Vnic optionally filtered / paginated on the subnet
    identified by C(subnet_ext_id).
  - The Nutanix Networking v4 API does not expose a stand-alone C(get_vnic_by_id) endpoint; vNICs
    are always fetched in the context of their parent subnet, hence C(subnet_ext_id) is always
    required.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List virtual NICs on a subnet) -
    Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer,
    Project Admin, Super Admin, Virtual Machine Admin, Virtual Machine Operator,
    Virtual Machine Viewer, VPC Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - External ID (UUID) of the vNIC to fetch.
      - When provided, the module returns the single matching vNIC on
        C(subnet_ext_id).
    type: str
    required: false
  subnet_ext_id:
    description:
      - External ID (UUID) of the parent subnet whose vNICs should be listed / fetched.
      - Required for all operations because the networking v4 API scopes vNIC reads to a subnet.
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
- name: List all vNICs on a subnet
  nutanix.ncp.ntnx_vnics_info_v2:
    subnet_ext_id: "7131f3ca-47ce-4f1d-990c-fa17800bd94d"
  register: result

- name: Get a specific vNIC on a subnet using its ext_id
  nutanix.ncp.ntnx_vnics_info_v2:
    subnet_ext_id: "7131f3ca-47ce-4f1d-990c-fa17800bd94d"
    ext_id: "7147b563-7b80-4be5-96b5-d8ff63187a5c"
  register: result

- name: List vNICs on a subnet with a limit
  nutanix.ncp.ntnx_vnics_info_v2:
    subnet_ext_id: "7131f3ca-47ce-4f1d-990c-fa17800bd94d"
    limit: 5
  register: result

- name: List vNICs on a subnet with a filter
  nutanix.ncp.ntnx_vnics_info_v2:
    subnet_ext_id: "7131f3ca-47ce-4f1d-990c-fa17800bd94d"
    filter: "macAddress eq '50:6b:8d:f9:de:e7'"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Vnic info v4 API.
    - It can be a single Vnic if external ID is provided.
    - List of multiple Vnic if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    [
      {
        "assigned_ipv4_addresses": [
            {
                "prefix_length": 32,
                "value": "10.51.144.137"
            }
        ],
        "assigned_secondary_ipv4_addresses": null,
        "ext_id": "7147b563-7b80-4be5-96b5-d8ff63187a5c",
        "learned_ipv4_addresses": null,
        "links": null,
        "mac_address": "50:6b:8d:f9:de:e7",
        "metadata": null,
        "project_ext_id": null,
        "tenant_id": null,
        "vm_reference": "521ab899-2398-4a23-62cb-8cd5e46ee5d2"
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching vnics info"

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
  description: External ID of the vNIC
  type: str
  returned: when external ID is provided
  sample: "7147b563-7b80-4be5-96b5-d8ff63187a5c"

subnet_ext_id:
  description: External ID of the parent subnet whose vNICs were listed/fetched.
  type: str
  returned: always
  sample: "7131f3ca-47ce-4f1d-990c-fa17800bd94d"

total_available_results:
  description: The total number of vNICs available on the subnet in PC.
  type: int
  returned: when all vNICs on the subnet are fetched
  sample: 3
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        subnet_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_vnic_by_ext_id(module, subnets_api, result):
    """Fetch a single vNIC on the given subnet by external ID.

    The networking v4 SDK does not expose a direct get-by-id for vNICs, so
    we iterate the list of vNICs on the parent subnet and pick the match.
    """
    subnet_ext_id = module.params.get("subnet_ext_id")
    vnic_ext_id = module.params.get("ext_id")
    result["ext_id"] = vnic_ext_id
    result["subnet_ext_id"] = subnet_ext_id

    try:
        resp = subnets_api.list_vnics_by_subnet_id(subnetExtId=subnet_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vnic info using ext_id",
        )

    data = getattr(resp, "data", None) or []
    match = None
    for vnic in data:
        if getattr(vnic, "ext_id", None) == vnic_ext_id:
            match = vnic
            break

    if match is None:
        result["msg"] = "vNIC with ext_id '{0}' was not found on subnet '{1}'.".format(
            vnic_ext_id, subnet_ext_id
        )
        result["response"] = None
        module.fail_json(**result)

    result["response"] = strip_internal_attributes(match.to_dict())


def list_vnics_by_subnet(module, subnets_api, result):
    """List all vNICs attached to the given subnet, honoring info filters."""
    subnet_ext_id = module.params.get("subnet_ext_id")
    result["subnet_ext_id"] = subnet_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vnics info spec", **result)

    kwargs["subnetExtId"] = subnet_ext_id

    try:
        resp = subnets_api.list_vnics_by_subnet_id(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vnics info",
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
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "subnet_ext_id": None,
    }
    subnets_api = get_subnet_api_instance(module)
    if module.params.get("ext_id"):
        get_vnic_by_ext_id(module, subnets_api, result)
    else:
        list_vnics_by_subnet(module, subnets_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
