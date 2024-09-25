#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_acps_info
short_description: acp info module
version_added: 1.4.0
description: 'Get acp info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: access_control_policy
    acp_uuid:
      description:
        - acp UUID
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
- name: List acp using name filter criteria
  ntnx_acps_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter:
      name: "{{ acp.name }}"
    kind: access_control_policy
  register: result

- name: List acp using length, offset, sort order and name sort attribute
  ntnx_acps_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
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
  description: Metadata for acp_info list output
  returned: always
  type: dict
  sample: {
    "metadata": {
            "kind": "access_control_policy",
            "length": 1,
            "offset": 2,
            "sort_attribute": "name",
            "sort_order": "DESCENDING",
            "total_matches": 3
        } }
entities:
  description: acp intent response
  returned: always
  type: list
  sample: {
    "entities": [
                {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "creation_time": "",
                        "entity_version": "",
                        "kind": "access_control_policy",
                        "last_update_time": "",
                        "spec_hash": "",
                        "spec_version": 0,
                        "uuid": ""
                    },
                    "spec": {
                        "description": "",
                        "name": "",
                        "resources": {
                            "filter_list": {
                                "context_list": [
                                    {
                                        "entity_filter_expression_list": [
                                            {
                                                "left_hand_side": {
                                                    "entity_type": "ALL"
                                                },
                                                "operator": "IN",
                                                "right_hand_side": {
                                                    "collection": "ALL"
                                                }
                                            }
                                        ],
                                        "scope_filter_expression_list": [
                                            {
                                                "left_hand_side": "PROJECT",
                                                "operator": "IN",
                                                "right_hand_side": {
                                                    "uuid_list": [
                                                        ""
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            "role_reference": {
                                "kind": "role",
                                "uuid": ""
                            },
                            "user_group_reference_list": [],
                            "user_reference_list": [
                                {
                                    "kind": "user",
                                    "name": "",
                                    "uuid": ""
                                }
                            ]
                        }
                    },
                    "status": {
                        "description": "",
                        "is_system_defined": false,
                        "name": "",
                        "resources": {
                            "filter_list": {
                                "context_list": [
                                    {
                                        "entity_filter_expression_list": [
                                            {
                                                "left_hand_side": {
                                                    "entity_type": "ALL"
                                                },
                                                "operator": "IN",
                                                "right_hand_side": {
                                                    "collection": "ALL"
                                                }
                                            }
                                        ],
                                        "scope_filter_expression_list": [
                                            {
                                                "left_hand_side": "PROJECT",
                                                "operator": "IN",
                                                "right_hand_side": {
                                                    "uuid_list": [
                                                        ""
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                ]
                            },
                            "role_reference": {
                                "kind": "role",
                                "name": "test_role",
                                "uuid": ""
                            },
                            "user_group_reference_list": [],
                            "user_reference_list": []
                        },
                        "state": "COMPLETE"
                    }
                }
            ]
            }
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.acps import ACP  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        acp_uuid=dict(type="str"),
        kind=dict(type="str", default="access_control_policy"),
        sort_order=dict(type="str", choices=["ASCENDING", "DESCENDING"]),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_acp(module, result):
    acp = ACP(module)
    acp_uuid = module.params.get("acp_uuid")
    resp = acp.read(acp_uuid)

    result["response"] = resp


def get_acps(module, result):
    acp = ACP(module)
    spec, error = acp.get_info_spec()

    resp = acp.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("acp_uuid"):
        get_acp(module, result)
    else:
        get_acps(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
