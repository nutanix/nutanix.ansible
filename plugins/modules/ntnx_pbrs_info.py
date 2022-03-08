#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_pbrs_info
short_description: PBR  info module
version_added: 1.0.0
description: 'Get PBR"s info'
options:
      kind:
        description:
          - The kind name
        type: str
        default: routing_policy
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.pbrs import Pbr  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        kind=dict(type="str", default="routing_policy"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def list_vm(module, result):
    pbr = Pbr(module)
    spec, error = pbr.get_info_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating filter Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp, status = pbr.list(spec)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed to get information", **result)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_together=[
            ("sort_order", "sort_attribute"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_uuid": None,
        "task_uuid": None,
    }
    list_vm(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
