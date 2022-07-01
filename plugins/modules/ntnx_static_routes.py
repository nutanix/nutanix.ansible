#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.static_routes import StaticRoutes
from ..module_utils import utils
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402



def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    nexthop_spec = dict(
        external_subnet_ref = dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive, required=False),
        vpn_connection_ref = dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive, required=False)
    )
    static_route_spec = dict(
        destination = dict(type="str", required=True),
        next_hop = dict(
            type = "dict",
            options=nexthop_spec,
            required=True,
            mutually_exclusive = [("external_subnet_ref", "vpn_connection_ref")]
        )
    ) 
    module_args = dict(
        vpc_uuid = dict(type="str", required=True),
        static_routes_list = dict(
            type="list",
            elements="dict",
            options=static_route_spec,
            required=False 
        ),
        remove_all_routes = dict(type="bool", required=False, default=False)
    )
    return module_args


def update_static_routes(module, result):
    static_routes = StaticRoutes(module)
    vpc_uuid = module.params["vpc_uuid"]
    curr_routes = static_routes.get_static_routes(vpc_uuid)
    result["response"] = curr_routes
    result["vpc_uuid"] = vpc_uuid

    # status and spec have field name different schema for default static routes
    if curr_routes["status"]["resources"].get("default_route"):
        curr_routes["status"]["resources"]["default_route_nexthop"] = curr_routes["status"]["resources"]["default_route"]["nexthop"]
    
    utils.strip_extra_attrs_from_status(curr_routes["status"], curr_routes["spec"])
    curr_routes["spec"] = curr_routes.pop("status")
    
    # new spec for updating static routes
    update_spec, err = static_routes.get_spec(curr_routes)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating static routes update spec", **result)

    if update_spec == curr_routes:
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to update"
        )

    if module.check_mode:
        result["response"] = update_spec
        result["params"] = module.params
        result["current_spec"] = curr_routes
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
