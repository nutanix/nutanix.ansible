#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_subnets_info
short_description: subnet info module
version_added: 1.0.0
description: 'Get subnet info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: subnet
    subnet_uuid:
        description:
            - subnet UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
"""
EXAMPLES = r"""
  - name: List subnets using type filter criteria
    ntnx_subnets_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
         subnet_type: "{{ subnet.type }}"
      kind: subnet
    register: result

  - name: List subnets using length, offset, sort order and sort attribute
    ntnx_subnets_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      length: 2
      offset: 1
      sort_order: "DESCENDING"
      sort_attribute: "vlan_id"
    register: result

"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: Metadata for subnet list output
  returned: always
  type: dict
  sample: {
    "metadata": {
            "filter": "subnet_type==VLAN",
            "kind": "subnet",
            "length": 1,
            "offset": 0,
            "total_matches": 4
        }
    }
entities:
  description: Subnet intent response
  returned: always
  type: list
  sample: {
    "entities": [
            {
                "metadata": {
                    "categories": {},
                    "categories_mapping": {},
                    "creation_time": "2022-03-08T06:57:14Z",
                    "kind": "subnet",
                    "last_update_time": "2022-03-08T06:57:17Z",
                    "owner_reference": {
                        "kind": "user",
                        "name": "admin",
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec_version": 1,
                    "uuid": "0cf3f1de-88d2-41e9-9370-f94d80d1a2e3"
                },
                "spec": {
                    "cluster_reference": {
                        "kind": "cluster",
                        "name": "auto_cluster_prod_1a642ea0a5c3",
                        "uuid": "0005d734-09d4-0462-185b-ac1f6b6f97e2"
                    },
                    "name": "test_1",
                    "resources": {
                        "ip_config": {
                            "default_gateway_ip": "10.10.1.1",
                            "dhcp_options": {
                                "domain_name": "calm.nutanix.com",
                                "domain_name_server_list": [
                                    "8.8.8.8",
                                    "8.8.8.4"
                                ],
                                "domain_search_list": [
                                    "calm.nutanix.com",
                                    "eng.nutanix.com"
                                ]
                            },
                            "dhcp_server_address": {
                                "ip": "10.10.1.254"
                            },
                            "pool_list": [
                                {
                                    "range": "10.10.1.10 10.10.1.20"
                                }
                            ],
                            "prefix_length": 24,
                            "subnet_ip": "10.10.1.0"
                        },
                        "subnet_type": "VLAN",
                        "virtual_switch_uuid": "91639374-c0b9-48c3-bfc1-f9c89343b3e7",
                        "vlan_id": 28,
                        "vswitch_name": "br0"
                    }
                },
                "status": {
                    "cluster_reference": {
                        "kind": "cluster",
                        "name": "auto_cluster_prod_1a642ea0a5c3",
                        "uuid": "0005d734-09d4-0462-185b-ac1f6b6f97e2"
                    },
                    "execution_context": {
                        "task_uuids": [
                            "2b4928f0-0849-4ed0-ba52-16eaed3962c7"
                        ]
                    },
                    "name": "test_1",
                    "resources": {
                        "ip_config": {
                            "default_gateway_ip": "10.10.1.1",
                            "dhcp_options": {
                                "domain_name": "calm.nutanix.com",
                                "domain_name_server_list": [
                                    "8.8.8.8",
                                    "8.8.8.4"
                                ],
                                "domain_search_list": [
                                    "calm.nutanix.com",
                                    "eng.nutanix.com"
                                ]
                            },
                            "dhcp_server_address": {
                                "ip": "10.10.1.254"
                            },
                            "pool_list": [
                                {
                                    "range": "10.10.1.10 10.10.1.20"
                                }
                            ],
                            "prefix_length": 24,
                            "subnet_ip": "10.10.1.0"
                        },
                        "subnet_type": "VLAN",
                        "virtual_switch_uuid": "91639374-c0b9-48c3-bfc1-f9c89343b3e7",
                        "vlan_id": 28,
                        "vswitch_name": "br0"
                    },
                    "state": "COMPLETE"
                }
            }
        ],
        }
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.subnets import Subnet  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        subnet_uuid=dict(type="str"),
        kind=dict(type="str", default="subnet"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_subnet(module, result):
    subnet = Subnet(module)
    subnet_uuid = module.params.get("subnet_uuid")
    resp = subnet.read(subnet_uuid)

    result["response"] = resp


def get_subnets(module, result):
    subnet = Subnet(module)
    spec, error = subnet.get_info_spec()

    resp = subnet.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("subnet_uuid"):
        get_subnet(module, result)
    else:
        get_subnets(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
