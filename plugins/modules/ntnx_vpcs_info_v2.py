#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpcs_info_v2
short_description: vpc info module
version_added: 2.0.0
description:
    - This module fetches information about Nutanix vpcs.
    - The module can fetch information about all vpcs or a specific vpc.
options:
    ext_id:
        description:
            - vpc external ID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List VPCs
  nutanix.ncp.ntnx_vpcs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: vpcs

- name: List VPC using name filter criteria
  nutanix.ncp.ntnx_vpcs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'test_vpc'"
  register: result

- name: List VPC using ext_id
  nutanix.ncp.ntnx_vpcs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
  register: result
"""
RETURN = r"""
response:
  description:
      - The response from the vpc v4 API.
      - it can be vpc or list of vpcs as per spec.
  returned: always
  type: dict
  sample:
    {
            "common_dhcp_options": {
                "domain_name_servers": null
            },
            "description": null,
            "ext_id": "ce14a4cc-5a9a-4dd0-8f82-daadc1045e57",
            "external_routing_domain_reference": null,
            "external_subnets": [
                {
                    "active_gateway_count": 1,
                    "active_gateway_node": {
                        "node_id": "a9b4cb02-2487-4878-a6b6-395bd4f5fb61",
                        "node_ip_address": {
                            "ipv4": {
                                "prefix_length": 32,
                                "value": "000.000.000.000"
                            },
                            "ipv6": null
                        }
                    },
                    "active_gateway_nodes": [
                        {
                            "node_id": "a9b4cb02-2487-4878-a6b6-395bd4f5fb61",
                            "node_ip_address": {
                                "ipv4": {
                                    "prefix_length": 32,
                                    "value": "000.000.000.000"
                                },
                                "ipv6": null
                            }
                        }
                    ],
                    "external_ips": [
                        {
                            "ipv4": {
                                "prefix_length": 32,
                                "value": "000.000.000.000"
                            },
                            "ipv6": null
                        }
                    ],
                    "gateway_nodes": null,
                    "subnet_reference": "b000b263-8662-4a7f-a841-32eaf5b97d5d"
                }
            ],
            "externally_routable_prefixes": null,
            "links": null,
            "metadata": {
                "category_ids": null,
                "owner_reference_id": "00000000-0000-0000-0000-000000000000",
                "owner_user_name": null,
                "project_name": null,
                "project_reference_id": null
            },
            "name": "rohcTvGipSJQansible-ag2",
            "snat_ips": null,
            "tenant_id": null,
            "vpc_type": "REGULAR"
        }


changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

ext_id:
    description:
        - The external ID of the vpc when specific vpc is fetched.
    type: str
    returned: always
    sample: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
"""
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import get_vpc_api_instance  # noqa: E402
from ..module_utils.v4.network.helpers import get_vpc  # noqa: E402
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
    )

    return module_args


def get_vpcs(module, result):
    vpcs = get_vpc_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vpcs info Spec", **result)

    try:
        resp = vpcs.list_vpcs(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vpcs info",
        )

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def get_vpc_by_ext_id(module, result):
    vpcs = get_vpc_api_instance(module)
    ext_id = module.params.get("ext_id")

    resp = get_vpc(module, vpcs, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_vpc_by_ext_id(module, result)
    else:
        get_vpcs(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
