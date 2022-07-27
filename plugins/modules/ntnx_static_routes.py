#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_static_routes
short_description: module for create/update static routes of vpc
version_added: 1.0.0
description: "Create/Update static routes of vpc"
options:
    wait:
        description: Wait for the create/update operations to complete.
        type: bool
        required: false
        default: True
    vpc_uuid:
        description: vpc uuid whose static routes has to be created/updated
        required: true
        type: str
    remove_all_routes:
        description:
            - set this flag to remove all static routes
            - this will only remove all static routes except local and dynamic routes
            - mutually_exclusive with C(static_routes)
        type: bool
        required: false
        default: false
    static_routes:
        description:
            - list of static routes to be overriden in vpc.
            - mutually exclusive with C(remove_all_routes)
            - required incase remove_all_categories is not given
            - default static route can be mentioned in this with destination - 0.0.0.0/0
            - Only one default static route is allowed
        required: false
        type: list
        elements: dict
        suboptions:
            destination:
                description:
                    - destination prefix eg. 10.2.3.0/24
                    - for defaut static route give 0.0.0.0/0
                required: true
                type: str
            next_hop:
                description:
                    - info about next hop in static route
                type: dict
                required: true
                suboptions:
                    vpn_connection_ref:
                        description:
                            - vpn connection reference
                            - mutually exclusive with C(external_subnet_ref)
                        type: dict
                        required: false
                        suboptions:
                            name:
                                description:
                                    - vpn connection Name
                                    - Mutually exclusive with C(uuid)
                                type: str
                                required: false
                            uuid:
                                description:
                                    - vpn connection UUID
                                    - Mutually exclusive with C(name)
                                type: str
                                required: false
                    external_subnet_ref:
                        description:
                                - external subnet reference
                                - mutually exclusive with C(vpn_connection_ref)
                        type: dict
                        required: false
                        suboptions:
                            name:
                                description:
                                    - subnet connection Name
                                    - Mutually exclusive with C(uuid)
                                type: str
                                required: false
                            uuid:
                                description:
                                    - subnet connection UUID
                                    - Mutually exclusive with C(name)
                                type: str
                                required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
- name: create static routes and default static routes with external nat subnet
  ntnx_static_routes:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    vpc_uuid: "{{ vpc.uuid }}"
    static_routes:
      - destination: "0.0.0.0/0"
        next_hop:
          external_subnet_ref:
            name: "{{ external_nat_subnet.name }}"
      - destination: "10.2.2.0/24"
        next_hop:
          external_subnet_ref:
            uuid: "{{ external_nat_subnet.uuid }}"
      - destination: "10.2.3.0/24"
        next_hop:
          external_subnet_ref:
            uuid: "{{ external_nat_subnet.uuid }}"
      - destination: "10.2.4.0/24"
        next_hop:
          vpn_connection_ref:
            uuid: "{{ vpn.uuid }}"
  register: result

- name: remove all routes excluding dynamic and local routes
  ntnx_static_routes:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    vpc_uuid: "{{ vpc.uuid }}"
    remove_all_routes: true
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
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.utils import (  # noqa: E402
    remove_param_with_none_value,
    strip_extra_attrs,
)


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    nexthop_spec = dict(
        external_subnet_ref=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        vpn_connection_ref=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
    )
    static_route_spec = dict(
        destination=dict(type="str", required=True),
        next_hop=dict(
            type="dict",
            options=nexthop_spec,
            required=True,
            mutually_exclusive=[("external_subnet_ref", "vpn_connection_ref")],
        ),
    )
    module_args = dict(
        vpc_uuid=dict(type="str", required=True),
        static_routes=dict(
            type="list", elements="dict", options=static_route_spec, required=False
        ),
        remove_all_routes=dict(type="bool", required=False, default=False),
    )
    return module_args


def check_static_routes_idempotency(routes1, routes2):
    # check default route
    if routes1["spec"]["resources"].get("default_route_nexthop") != routes2["spec"][
        "resources"
    ].get("default_route_nexthop"):
        return False

    # check static routes length
    if len(routes1["spec"]["resources"]["static_routes_list"]) != len(
        routes2["spec"]["resources"]["static_routes_list"]
    ):
        return False

    # check static routes contents
    for route in routes1["spec"]["resources"]["static_routes_list"]:
        if route not in routes2["spec"]["resources"]["static_routes_list"]:
            return False

    return True


def update_static_routes(module, result):
    static_routes = StaticRoutes(module)
    vpc_uuid = module.params["vpc_uuid"]
    curr_routes = static_routes.get_static_routes(vpc_uuid)
    result["response"] = curr_routes
    result["vpc_uuid"] = vpc_uuid

    # status and spec have field name different schema for default static routes
    if curr_routes["status"]["resources"].get("default_route"):
        curr_routes["status"]["resources"]["default_route_nexthop"] = curr_routes[
            "status"
        ]["resources"]["default_route"]["nexthop"]

    strip_extra_attrs(curr_routes["status"], curr_routes["spec"])
    curr_routes["spec"] = curr_routes.pop("status")

    # new spec for updating static routes
    update_spec, err = static_routes.get_spec(curr_routes)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating static routes update spec", **result)

    if check_static_routes_idempotency(curr_routes, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to update")

    if module.check_mode:
        result["response"] = update_spec
        return

    # update static routes
    resp = static_routes.update_static_routes(update_spec, vpc_uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]

    # wait for static routes update to finish
    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        # get the current static routes
        resp = static_routes.get_static_routes(vpc_uuid)

    result["changed"] = True
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_one_of=[("static_routes", "remove_all_routes")],
        mutually_exclusive=[("static_routes", "remove_all_routes")],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vpc_uuid": None,
    }
    update_static_routes(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
