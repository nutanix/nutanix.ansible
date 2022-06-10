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
from ..module_utils.prism.images import Image  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        image_uuid=dict(type="str"),
        kind=dict(type="str", default="image"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_image(module, result):
    image = Image(module)
    uuid = module.params.get("image_uuid")
    resp = image.read(uuid)
    result["response"] = resp


def get_all_images(module, result):
    image = Image(module)
    spec, _ = image.get_info_spec()
    resp = image.list(spec)
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
        mutually_exclusive=[
            ("image_uuid", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("image_uuid"):
        get_image(module, result)
    else:
        get_all_images(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
