#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_static_routes_info
short_description: static routes info module
version_added: 1.0.0
description: 'Get static routes info for a vpc'
options:
    vpc_uuid:
        description:
            - vpc UUID whose static routes needs to be fetched
        type: str
        required: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
- name: get all static routes for a vpc
  ntnx_static_routes_info:
    vpc_uuid: "{{ vpc.uuid }}"
  register: result
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The vpc_route_table kind metadata
  returned: always
  type: dict
  sample: {
                "categories": {},
                "categories_mapping": {},
                "creation_time": "2022-07-01T08:20:39Z",
                "kind": "vpc_route_table",
                "last_update_time": "2022-07-01T10:30:41Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "spec_hash": "00000000000000000000000000000000000000000000000000",
                "spec_version": 8,
                "uuid": "528323ee-7c89-sb65-68a7-a66c0c4fc9d5"
            }
spec:
  description: An intentful representation of a vpc static routes spec
  returned: always
  type: dict
  sample: {
                "name": "Route Table for vpc",
                "resources": {
                    "default_route_nexthop": {
                        "external_subnet_reference": {
                            "kind": "subnet",
                            "uuid": "ace7f19a-a1a9-43ca-a11a-cbac200044b7"
                        }
                    },
                    "static_routes_list": [
                        {
                            "destination": "10.2.2.0/24",
                            "nexthop": {
                                "external_subnet_reference": {
                                    "kind": "subnet",
                                    "uuid": "ace7f19a-a1a9-43ca-c11a-9bac200044b7"
                                }
                            }
                        },
                        {
                            "destination": "10.2.3.0/24",
                            "nexthop": {
                                "external_subnet_reference": {
                                    "kind": "subnet",
                                    "uuid": "ace7f19a-d1a9-43ca-a11a-9bac200044b7"
                                }
                            }
                        }
                    ]
                }
            }
status:
  description: An intentful representation of a vpc static routes status
  returned: always
  type: dict
  sample: {
                "execution_context": {
                    "task_uuid": [
                        "bc6bdb00-18b3-sdab-8b03-701db6856e7f"
                    ]
                },
                "resources": {
                    "default_route": {
                        "destination": "0.0.0.0/0",
                        "is_active": true,
                        "nexthop": {
                            "external_subnet_reference": {
                                "kind": "subnet",
                                "name": "no-nat",
                                "uuid": "ace7f19a-a1a9-43ca-a11a-9bac200044b7"
                            }
                        },
                        "priority": 23455
                    },
                    "dynamic_routes_list": [],
                    "local_routes_list": [
                        {
                            "destination": "xx.xx.xx.xx/24",
                            "is_active": true,
                            "nexthop": {
                                "local_subnet_reference": {
                                    "kind": "subnet",
                                    "name": "integration_test_overlay_subnet",
                                    "uuid": "974234b1-3fd1-4525-adeb-bce069696d2e"
                                }
                            },
                            "priority": 65534
                        }
                    ],
                    "static_routes_list": [
                        {
                            "destination": "10.2.2.0/24",
                            "is_active": true,
                            "nexthop": {
                                "external_subnet_reference": {
                                    "kind": "subnet",
                                    "name": "no-nat",
                                    "uuid": "ave7f19a-a1a9-43ca-a11a-9bac200044b7"
                                }
                            },
                            "priority": 23455
                        },
                        {
                            "destination": "10.2.3.0/24",
                            "is_active": true,
                            "nexthop": {
                                "external_subnet_reference": {
                                    "kind": "subnet",
                                    "name": "no-nat",
                                    "uuid": "cce7f19a-a1a9-43ca-a11a-9bac200044b7"
                                }
                            },
                            "priority": 23455
                        }
                    ]
                },
                "state": "COMPLETE"
            }
vpc_uuid:
  description: vpc uuid
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.static_routes import StaticRoutes  # noqa: E402


def get_module_spec():

    module_args = dict(
        vpc_uuid=dict(type="str", required=True),
    )

    return module_args

def get_static_routes(module, result):
    vpc_uuid = module.params["vpc_uuid"]
    static_routes = StaticRoutes(module)
    result["response"] = static_routes.get_static_routes(vpc_uuid)
    result["vpc_uuid"] = vpc_uuid

def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    result = {"changed": False, "error": None, "response": None, "vpc_uuid": None}

    get_static_routes(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
