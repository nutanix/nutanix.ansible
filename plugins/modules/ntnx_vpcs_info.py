#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpcs_info
short_description: vpc info module
version_added: 1.0.0
description: 'Get vpc info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: vpc
    vpc_uuid:
        description:
            - vpc UUID
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
  - name: List VPC using name filter criteria
    ntnx_vpcs_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
        name: "{{ vpc.name }}"
      kind: vpc
    register: result

  - name: List VPC using length, offset, sort order and name sort attribute
    ntnx_vpcs_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      length: 1
      offset: 1
      sort_order: "ASCENDING"
      sort_attribute: "name"
    register: result
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: Metadata for vpc list output
  returned: always
  type: dict
  sample: {
    "metadata": {
            "kind": "vpc",
            "length": 1,
            "offset": 2,
            "sort_attribute": "name",
            "sort_order": "DESCENDING",
            "total_matches": 3
        } }
entities:
  description: VPC intent response
  returned: always
  type: list
  sample: {
    "entities": [
            {
                "metadata": {
                    "categories": {},
                    "categories_mapping": {},
                    "creation_time": "2022-03-09T08:37:15Z",
                    "kind": "vpc",
                    "last_update_time": "2022-03-09T08:37:17Z",
                    "owner_reference": {
                        "kind": "user",
                        "name": "admin",
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec_version": 0,
                    "uuid": "7ee05b9d-4021-4f57-8a03-df9503adea9d"
                },
                "spec": {
                    "name": "integration_test_vpc",
                    "resources": {
                        "common_domain_name_server_ip_list": [],
                        "external_subnet_list": [
                            {
                                "external_subnet_reference": {
                                    "kind": "subnet",
                                    "uuid": "946d59d1-65fe-48cc-9882-e93439404e89"
                                }
                            }
                        ],
                        "externally_routable_prefix_list": []
                    }
                },
                "status": {
                    "execution_context": {
                        "task_uuids": [
                            "b3d99b77-dfe0-4067-b2ec-4fbaca6c30ac"
                        ]
                    },
                    "name": "integration_test_vpc",
                    "resources": {
                        "availability_zone_reference_list": [],
                        "common_domain_name_server_ip_list": [],
                        "external_subnet_list": [
                            {
                                "active_gateway_node": {
                                    "host_reference": {
                                        "kind": "host",
                                        "uuid": "e16b6989-a149-4f93-989f-bc3e96f88a40"
                                    },
                                    "ip_address": "10.46.136.28"
                                },
                                "external_ip_list": [
                                    "10.44.3.198"
                                ],
                                "external_subnet_reference": {
                                    "kind": "subnet",
                                    "uuid": "946d59d1-65fe-48cc-9882-e93439404e89"
                                }
                            }
                        ],
                        "externally_routable_prefix_list": []
                    },
                    "state": "COMPLETE"
                }
            }
        ],
        }
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.vpcs import Vpc  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        vpc_uuid=dict(type="str"),
        kind=dict(type="str", default="vpc"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_vpc(module, result):
    vpc = Vpc(module)
    vpc_uuid = module.params.get("vpc_uuid")
    resp = vpc.read(vpc_uuid)

    result["response"] = resp


def get_vpcs(module, result):
    vpc = Vpc(module)
    spec, error = vpc.get_info_spec()

    resp = vpc.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("vpc_uuid"):
        get_vpc(module, result)
    else:
        get_vpcs(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
