#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ..module_utils.base_module import BaseModule
from ..module_utils.prism.static_routes import StaticRoutes

__metaclass__ = type

DOCUMENTATION = r"""
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""


def get_module_spec():

    module_args = dict(
        vpc_uuid=dict(type="str", required=True),
    )

    return module_args


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    result = {"changed": False, "error": None, "response": None}

    vpc_uuid = module.params["vpc_uuid"]
    static_routes = StaticRoutes(module)
    result["response"] = static_routes.get_static_routes(vpc_uuid)
    result["vpc_uuid"] = vpc_uuid
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
