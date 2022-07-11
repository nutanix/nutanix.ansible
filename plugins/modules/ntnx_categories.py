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

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.categories import CategoryKey, CategoryValue  # noqa: E402


def get_module_spec():
    module_args = dict(
        name = dict(type="str", required=True),
        desc = dict(type="str", required=False),
        values = dict(type="list", elements="str", required=False),
        remove_values = dict(type="bool", required=False, default=False)
    )
    return module_args

def create_categories(module, result):
    key_obj = CategoryKey(module)
    name = module.params["name"]

    # check if new category create is required or not
    category_key = key_obj.read(endpoint=name, raise_error=False)
    category_key_values = {}
    category_values_specs = []
    category_key_exists = False
    if not category_key or category_key.get("state") == "ERROR":
        category_key_create_spec, err = key_obj.get_spec()
        if err:
            result["error"] = err
            module.fail_json(msg="Failed generating create category key spec", **result)
    else:
        category_key_exists = True
        category_key_create_spec, err = key_obj.get_spec(category_key)
        if err:
            result["error"] = err
            module.fail_json(msg="Failed generating category key update spec", **result)
        utils.strip_extra_attrs(category_key, category_key_create_spec)
        category_key_values = key_obj.list(name)

    # create spec for all the values which needed to be added to category key
    values = module.params.get("values")
    if values:
        value_obj = CategoryValue(module)
        for value in values:
            if value not in category_key_values:
                category_values_specs.append(value_obj.get_spec(value))

    # indempotency check
    if not category_values_specs and (category_key_exists and (category_key == category_key_create_spec)):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to update."
        )

    # check mode
    if module.check_mode:
        response = {
            "category_key": {},
            "category_values": {}
        }
        if (category_key_exists and (category_key == category_key_create_spec)):
            response["category_key"] = {
                "msg": "Nothing to update."
            }
        else:
            response["category_key"] = category_key_create_spec
        
        if not category_values_specs:
            response["category_values"] = {
                "msg": "Nothing to update."
            }
        else:
            response["category_values"] = category_values_specs
        
        result["response"] = response
        return

    # create/update category
    if not category_key_exists or (category_key != category_key_create_spec):
        resp = key_obj.create(name, category_key_create_spec)
        result["response"]["category_key"] = resp
    result["changed"] = True

    # add category values
    if category_values_specs:
        value_obj = CategoryValue(module)
        responses = []
        for value_spec in category_values_specs:
            resp = value_obj.create(name, value_spec)
            responses.append(resp)
        result["response"]["category_values"] = responses

def delete_category_values(module, name, values):
    responses = []
    value_obj = CategoryValue(module)
    for value in values:
        resp = value_obj.delete(name, value)
        responses.append(resp)
    return responses

def delete_categories(module, result):
    name = module.params["name"]
    key_obj = CategoryKey(module)
    if module.params.get("remove_values", False):
        values = key_obj.list(name)
        result["response"] = delete_category_values(module, name, values)
    elif module.params.get("values"):
        values = module.params["values"]
        result["response"] = delete_category_values(module, name, values)
    else:
        #first delete all values if exists
        values = key_obj.list(name)
        delete_category_values(module, name, values)
        #delete the category
        resp = key_obj.delete(uuid=name, no_response=True)
        result["response"] = resp
    result["changed"] = True
        
def run_module():
    
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    utils.remove_param_with_none_value(module.params)
    result = {
        "response": None,
        "error": None,
        "changed": False,
    }
    state = module.params["state"]
    if state == "present":
        create_categories(module, result)
    else:
        delete_categories(module, result)

    module.exit_json(**result)

def main():
    run_module()


if __name__ == "__main__":
    main()
