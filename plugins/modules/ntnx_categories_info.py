#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_categories_info
short_description: categories info module
version_added: 1.4.0
description: 'Get categories info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: category
    name:
        description:
            - The category name
            - Using this will also fetch all the category values associated with it
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: Test getting all categories
  ntnx_categories_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: false
  register: result
  ignore_errors: true

- name: Test getting the category with filter by it's name
  ntnx_categories_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: false
      filter:
          name: "{{category_name}}"
  register: result

- name: Test getting the category  by it's name
  ntnx_categories_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: false
      name: "{{category_name}}"
  register: result
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: Metadata for categories list output
  returned: always
  type: dict
  sample: {
                "filter": "",
                "kind": "category_key",
                "length": 2,
                "offset": 0,
                "total_matches": 2
            }
entities:
  description: categories intent response
  returned: always
  type: list
  sample: [
                {
                    "description": "Application type.",
                    "name": "AppType",
                    "system_defined": true
                },
                {
                    "description": "Environment type.",
                    "name": "Environment",
                    "system_defined": true
                }
            ]

"""


from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v3.prism.categories import Category, CategoryKey  # noqa: E402


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
    result["response"] = {"category_key": category_key, "category_values": values}


def get_categories(module, result):
    categories = Category(module)
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
