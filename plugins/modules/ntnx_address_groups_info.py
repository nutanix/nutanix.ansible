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

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.address_groups import AddressGroup  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        address_group_uuid=dict(type="str"),
        kind=dict(type="str", default="address_group"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_address_group(module, result):
    address_group = AddressGroup(module)
    address_group_uuid = module.params.get("address_group_uuid")
    resp = address_group.read(address_group_uuid)

    result["response"] = resp["address_group"]


def get_address_groups(module, result):
    address_group = AddressGroup(module)
    spec, err = address_group.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating info spec for Address group", **result)
    resp = address_group.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("address_group_uuid"):
        get_address_group(module, result)
    else:
        get_address_groups(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
