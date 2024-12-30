#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_protected_resources_info_v2
short_description: Module to fetch protected resource in Nutanix Prism Central.
description:
  - This module can be used to fetch protected resource in Nutanix Prism Central.
options:
  ext_id:
    description:
      - The external identifier of a protected VM or volume group used to retrieve the protected resource.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_protected_resource_api_instance,
)
from ..module_utils.v4.data_protection.helpers import (  # noqa: E402
    get_protected_resource,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_protected_resource_by_id(module, result):
    protected_resource = get_protected_resource_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_protected_resource(module, protected_resource, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


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
        "ext_id": None,
    }
    ext_id = module.params.get("ext_id")
    if ext_id:
        get_protected_resource_by_id(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
