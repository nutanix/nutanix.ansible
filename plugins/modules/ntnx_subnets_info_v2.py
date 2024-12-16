#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Gevorg Khachatryan
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_subnets_info_v2
short_description: subnet info module
version_added: 2.0.0
description: 'Fetch list of subnets or subnet info using subnet external ID'
options:
    ext_id:
        description:
            - subnet external ID
        type: str
    expand:
        description:
            - Expand the response with additional information
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: List all subnets
  ntnx_subnets_info:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
  register: result

- name: List subnet using uuid criteria
  ntnx_subnets_info:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    ext_id: "{{ subnet_ext_id }}"
  register: result

- name: List subnets using filter criteria and filter for subnet name
  ntnx_subnets_info:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    filter: "name eq '{{ test_subnet_name }}'"

- name: List subnet using filter criteria and filter for cluster uuid
  ntnx_subnets_info:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    filter: "clusterReference eq '{{ cluster_uuid }}'"
"""
RETURN = r"""
response:
    description:
        - Response for fetching subnets
        - Returns subnet details
    type: dict
    returned: always
    sample:
        {
            "bridge_name": "br0",
            "cluster_name": null,
            "cluster_reference": "0006197f-3d06-ce49-1fc3-ac1f6b6029c1",
            "description": null,
            "dhcp_options": {
                "boot_file_name": "pxelinux.0",
                "domain_name": "nutanix.com",
                "domain_name_servers": [
                    {
                        "ipv4": {
                            "prefix_length": 32,
                            "value": "8.8.8.8"
                        },
                        "ipv6": null
                    },
                    {
                        "ipv4": {
                            "prefix_length": 32,
                            "value": "8.8.4.4"
                        },
                        "ipv6": null
                    }
                ],
                "ntp_servers": null,
                "search_domains": [
                    "calm.nutanix.com",
                    "eng.nutanix.com"
                ],
                "tftp_server_name": "['10.5.0.10']"
            },
            "dynamic_ip_addresses": null,
            "ext_id": "9cc4abba-f27d-40db-90ba-c1592dccaedf",
            "hypervisor_type": "acropolis",
            "ip_config": [
                {
                    "ipv4": {
                        "default_gateway_ip": {
                            "prefix_length": 32,
                            "value": "192.168.0.254"
                        },
                        "dhcp_server_address": {
                            "prefix_length": 32,
                            "value": "192.168.0.253"
                        },
                        "ip_subnet": {
                            "ip": {
                                "prefix_length": 32,
                                "value": "192.168.0.0"
                            },
                            "prefix_length": 24
                        },
                        "pool_list": [
                            {
                                "end_ip": {
                                    "prefix_length": 32,
                                    "value": "192.168.0.30"
                                },
                                "start_ip": {
                                    "prefix_length": 32,
                                    "value": "192.168.0.20"
                                }
                            }
                        ]
                    },
                    "ipv6": null
                }
            ],
            "ip_prefix": null,
            "ip_usage": null,
            "is_advanced_networking": null,
            "is_external": false,
            "is_nat_enabled": null,
            "links": null,
            "metadata": {
                "category_ids": null,
                "owner_reference_id": "00000000-0000-0000-0000-000000000000",
                "owner_user_name": null,
                "project_name": null,
                "project_reference_id": null
            },
            "migration_state": null,
            "name": "KTTRilWFptZc_subnet_test_3",
            "network_function_chain_reference": null,
            "network_id": 226,
            "reserved_ip_addresses": null,
            "subnet_type": "VLAN",
            "tenant_id": null,
            "virtual_switch": null,
            "virtual_switch_reference": "3a9be61d-f5c1-4fe0-8a5a-9832d747b4f8",
            "vpc": null,
            "vpc_reference": null
        }

failed:
    description: Indicates if the request failed
    type: bool
    returned: always

error:
  description: Error message
  type: str
  returned: always

changed:
  description: Indicates if any changes were made during the operation
  type: bool
  returned: always
  sample: False
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
        expand=dict(type="str"),
    )

    return module_args


def get_subnet(module, result):
    subnets = get_subnet_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = subnets.get_subnet_by_id(ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching subnet info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_subnets(module, result):
    subnets = get_subnet_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating subnets info Spec", **result)

    try:
        resp = subnets.list_subnets(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching subnets info",
        )
    if not resp or not resp.to_dict().get("data"):
        result["response"] = []
    else:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


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
        get_subnet(module, result)
    else:
        get_subnets(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
