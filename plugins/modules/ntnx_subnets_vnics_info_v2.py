#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_subnets_vnics_info_v2
short_description: Fetch virtual NICs attached to a subnet in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about virtual NICs attached to a subnet
    in Nutanix Prism Central.
  - List virtual NICs on the subnet optionally filtered / paginated using C(filter),
    C(limit), C(page), C(orderby) and C(select).
  - The Nutanix v4 networking API exposes only a list endpoint for this resource
    (no Get-vNIC-by-ID).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(View Subnet Vnic) -
    Required Roles: Backup Admin, Network Infra Admin, Prism Admin, Project Admin,
    Project Manager, Super Admin, Tenant Admin, Tenant Consumer, VPC Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  subnet_ext_id:
    description:
      - The external ID (UUID) of the parent subnet whose virtual NICs will be listed.
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
- name: List all virtual NICs attached to a subnet
  nutanix.ncp.ntnx_subnets_vnics_info_v2:
    subnet_ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
  register: result
  ignore_errors: true

- name: List virtual NICs on a subnet with a limit
  nutanix.ncp.ntnx_subnets_vnics_info_v2:
    subnet_ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    limit: 1
  register: result
  ignore_errors: true

- name: List virtual NICs on a subnet using an OData filter (by VM reference)
  nutanix.ncp.ntnx_subnets_vnics_info_v2:
    subnet_ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    filter: "vmReference eq '9939114c-7551-48fd-b064-adbdc2879065'"
  register: result
  ignore_errors: true

- name: List virtual NICs on a subnet ordered by MAC address
  nutanix.ncp.ntnx_subnets_vnics_info_v2:
    subnet_ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    orderby: "macAddress"
  register: result
  ignore_errors: true

- name: List all virtual NICs on a subnet with fetch_all
  nutanix.ncp.ntnx_subnets_vnics_info_v2:
    subnet_ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - List of virtual NICs on the subnet from the Nutanix PC
      list-virtual-NICs-by-subnet v4 API.
    - Optionally filtered, limited, ordered, or projected using C(filter),
      C(limit), C(page), C(orderby), or C(select).
  returned: always
  type: list
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
  sample: "Api Exception raised while fetching virtual NICs info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

subnet_ext_id:
  description: External ID (UUID) of the parent subnet whose virtual NICs were listed.
  type: str
  returned: always
  sample: "c15625a4-a222-4351-a00a-ef51ffabe0d3"

total_available_results:
  description: The total number of available virtual NICs on the given subnet in PC.
  type: int
  returned: always
  sample: 4
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import get_subnet_api_instance  # noqa: E402
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


def get_vnics(module, subnets_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating virtual NICs info spec", **result)

    subnet_ext_id = module.params.get("subnet_ext_id")
    result["subnet_ext_id"] = subnet_ext_id

    try:
        resp = list_entities(
            subnets_api.list_vnics_by_subnet_id,
            kwargs=kwargs,
            subnetExtId=subnet_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virtual NICs info",
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
    subnets_api = get_subnet_api_instance(module)
    get_vnics(module, subnets_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
