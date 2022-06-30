#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_image_placement_policies_info
short_description: image placement policies info module
version_added: 1.0.0
description: 'Get image placement policy info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: image_placement_policy
    policy_uuid:
        description:
            - policy UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
  - name: Get image placement policy using policy_uuid
    ntnx_image_placement_policies_info:
      policy_uuid: "<policy_uuid>"
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
        - name: test_policy
    register: result

  - name: List image placement policies using name filter criteria
    ntnx_image_placement_policies_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
        - name: test_policy
    register: result

  - name: List image placement policies using length, offset
    ntnx_image_placement_policies_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      length: 2
      offset: 1
    register: result
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: Metadata for image placement policies list output
  returned: always
  type: dict
  sample: {
                "filter": "",
                "kind": "image_placement_policy",
                "length": 2,
                "offset": 0,
                "total_matches": 2
            }
entities:
  description: image placement policies intent response
  returned: always
  type: list
  sample: [
      {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "creation_time": "2022-06-15T22:04:26Z",
                        "kind": "image_placement_policy",
                        "last_update_time": "2022-06-15T22:04:28Z",
                        "owner_reference": {
                            "kind": "user",
                            "name": "admin",
                            "uuid": "00000000-0000-0000-0000-000000000000"
                        },
                        "spec_hash": "00000000000000000000000000000000000000000000000000",
                        "spec_version": 0,
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec": {
                        "name": "test_policy_1",
                        "resources": {
                            "cluster_entity_filter": {
                                "params": {
                                    "AppTier": [
                                        "Default"
                                    ]
                                },
                                "type": "CATEGORIES_MATCH_ANY"
                            },
                            "image_entity_filter": {
                                "params": {
                                    "AppFamily": [
                                        "Backup"
                                    ]
                                },
                                "type": "CATEGORIES_MATCH_ANY"
                            },
                            "placement_type": "AT_LEAST"
                        }
                    },
                    "status": {
                        "description": "",
                        "execution_context": {
                            "task_uuid": [
                                "00000000-0000-0000-0000-000000000000"
                            ]
                        },
                        "name": "test_policy_1",
                        "resources": {
                            "cluster_entity_filter": {
                                "params": {
                                    "AppTier": [
                                        "Default"
                                    ]
                                },
                                "type": "CATEGORIES_MATCH_ANY"
                            },
                            "image_entity_filter": {
                                "params": {
                                    "AppFamily": [
                                        "Backup"
                                    ]
                                },
                                "type": "CATEGORIES_MATCH_ANY"
                            },
                            "placement_type": "AT_LEAST"
                        },
                        "state": "COMPLETE"
                    }
                },
                {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "creation_time": "2022-06-15T22:04:33Z",
                        "kind": "image_placement_policy",
                        "last_update_time": "2022-06-15T22:04:35Z",
                        "owner_reference": {
                            "kind": "user",
                            "name": "admin",
                            "uuid": "00000000-0000-0000-0000-000000000000"
                        },
                        "spec_hash": "00000000000000000000000000000000000000000000000000",
                        "spec_version": 0,
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec": {
                        "name": "test_policy_2",
                        "resources": {
                            "cluster_entity_filter": {
                                "params": {
                                    "AppTier": [
                                        "Default"
                                    ]
                                },
                                "type": "CATEGORIES_MATCH_ANY"
                            },
                            "image_entity_filter": {
                                "params": {
                                    "AppFamily": [
                                        "Backup"
                                    ]
                                },
                                "type": "CATEGORIES_MATCH_ANY"
                            },
                            "placement_type": "AT_LEAST"
                        }
                    },
                    "status": {
                        "description": "",
                        "execution_context": {
                            "task_uuid": [
                                "00000000-0000-0000-0000-000000000000"
                            ]
                        },
                        "name": "test_policy_2",
                        "resources": {
                            "cluster_entity_filter": {
                                "params": {
                                    "AppTier": [
                                        "Default"
                                    ]
                                },
                                "type": "CATEGORIES_MATCH_ANY"
                            },
                            "image_entity_filter": {
                                "params": {
                                    "AppFamily": [
                                        "Backup"
                                    ]
                                },
                                "type": "CATEGORIES_MATCH_ANY"
                            },
                            "placement_type": "AT_LEAST"
                        },
                        "state": "COMPLETE"
                    }
                },
  ]
"""


from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.image_placement_policy import (
    ImagePlacementPolicy,
)  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        policy_uuid=dict(type="str"),
        kind=dict(type="str", default="image_placement_policy"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_placement_policy(module, result):
    policy_obj = ImagePlacementPolicy(module)
    uuid = module.params.get("policy_uuid")
    resp = policy_obj.read(uuid)
    result["response"] = resp


def get_placement_policies(module, result):
    policy_obj = ImagePlacementPolicy(module)
    spec, err = policy_obj.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Image Placement Policies info Spec", **result
        )
    resp = policy_obj.list(spec)
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
        mutually_exclusive=[
            ("policy_uuid", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("policy_uuid"):
        get_placement_policy(module, result)
    else:
        get_placement_policies(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
