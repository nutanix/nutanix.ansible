#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_aos_packages_info
short_description: Nutanix module which returns the AOS packages uploaded to Foundation
version_added: 1.1.0-beta.1
description: 'List AOS packages uploaded to Foundation'

extends_documentation_fragment:
      - nutanix.ncp.ntnx_foundation_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: List packages
  ntnx_foundation_aos_packages_info:
    nutanix_host: "{{ ip }}"
"""

RETURN = r"""
aos_packages:
  description: Uploaded AOS packages
  returned: always
  type: list
  sample: [
    "package1",
    "package2",s
  ]
"""
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.foundation.base_module import FoundationBaseModule  # noqa: E402
from ..module_utils.v3.foundation.enumerate_aos_packages import (  # noqa: E402
    EnumerateAOSPackages,
)


def get_module_spec():
    module_args = dict()
    return module_args


def list_aos_packages(module, result):
    packages = EnumerateAOSPackages(module)
    resp = packages.list()
    result["aos_packages"] = resp
    result["response"] = resp


def run_module():
    module = FoundationBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
    }
    list_aos_packages(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
