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
from ..module_utils.prism.categories import Categories, CategoryKey
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        kind=dict(type="str", default="category"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_category(module, result):
    key_obj = CategoryKey(module)
    name = module.params.get("name")
    category_key = key_obj.read(endpoint=name, raise_error=False)
    if not category_key or category_key.get("state") == "ERROR":
        result["response"] = {}
        return
    values = key_obj.list(name)
    result["response"] = {
        "category_key": category_key,
        "category_values": values
    }


def get_categories(module, result):
    categories = Categories(module)
    spec, err = categories.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Categories info Spec", **result)
    resp = categories.list(spec)
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
        mutually_exclusive=[
            ("name", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name"):
        get_category(module, result)
    else:
        get_categories(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
