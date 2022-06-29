#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from email.policy import default

__metaclass__ = type

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    nexthop_spec = dict(
        subnet = dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive, required=False),
        vpn = dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive, required=False)
    )
    static_route_spec = dict(
        destination = dict(type="str", required=True),
        next_hop = dict(
            type = "dict",
            options=nexthop_spec,
            required=True
        )
    ) 
    module_args = dict(
        static_routes_list = dict(
            type="dict",
            options=static_route_spec,
            required=False 
        ),
        remove_all_routes = dict(type="str", required=False, default=False)
    )
    return module_args


def update_static_routes(module, result):
    pass

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
