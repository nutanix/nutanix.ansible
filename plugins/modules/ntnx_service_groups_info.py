#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_service_groups_info
short_description: service_group info module
version_added: 1.3.0
description: 'Get service_group info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: network_service_group
    service_group_uuid:
      description:
        - service_group UUID
      type: str
    sort_order:
        description:
        - The sort order in which results are returned
        type: str
        choices:
            - ASCENDING
            - DESCENDING
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
  - name: List service_group using name filter criteria
    ntnx_service_groups_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter: 
        name: "{{ service_group.name }}"
      kind: service_group
    register: result

  - name: List service_group using length, offset, sort order and name sort attribute
    ntnx_service_groups_info:
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
  description: Metadata for service_group_info list output
  returned: always
  type: dict
  sample: {
    "metadata": {
            "kind": "service_group",
            "length": 1,
            "offset": 2,
            "sort_attribute": "name",
            "sort_order": "DESCENDING",
            "total_matches": 3
        } }
entities:
  description: service_group intent response
  returned: always
  type: list
  sample: {
    "entities": [
                    {"service_group": {
                        "description": "desc",
                        "is_system_defined": false,
                        "name": "test_service",
                        "service_list": [
                            {
                                "protocol": "TCP",
                                "tcp_port_range_list": [
                                    {
                                        "end_port": 23,
                                        "start_port": 0
                                    }
                                ]
                            },
                            {
                                "protocol": "UDP",
                                "udp_port_range_list": [
                                    {
                                        "end_port": 50,
                                        "start_port": 10
                                    },
                                    {
                                        "end_port": 90,
                                        "start_port": 60
                                    },
                                    {
                                        "end_port": 99,
                                        "start_port": 99
                                    }
                                ]
                            },
                            {
                                "icmp_type_code_list": [
                                    {
                                        "code": 10
                                    },
                                    {
                                        "type": 1
                                    },
                                    {
                                        "code": 3,
                                        "type": 2
                                    }
                                ],
                                "protocol": "ICMP"
                            }
                        ]
                    },
                    "uuid": "00000000-0000-0000-0000-000000000000"
                }
            ]
            }
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.service_groups import ServiceGroup  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        service_group_uuid=dict(type="str"),
        kind=dict(type="str", default="service_group"),
        sort_order=dict(type="str", choices=["ASCENDING", "DESCENDING"]),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_service_group(module, result):
    service_group = ServiceGroup(module)
    service_group_uuid = module.params.get("service_group_uuid")
    resp = service_group.read(service_group_uuid)

    result["response"] = resp


def get_service_groups(module, result):
    service_group = ServiceGroup(module)
    spec, error = service_group.get_info_spec()

    resp = service_group.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("service_group_uuid"):
        get_service_group(module, result)
    else:
        get_service_groups(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
