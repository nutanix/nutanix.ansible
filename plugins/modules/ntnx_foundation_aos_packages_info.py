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
version_added: 1.0.0
description: 'List AOS packages uploaded to Foundation'
options:
  nutanix_host:
    description:
      - Foundation VM hostname or IP address
    type: str
    required: true
  nutanix_port:
    description:
      - PC port
    type: str
    default: 8000
    required: false
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
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

from ansible_collections.nutanix.ncp.plugins.module_utils.foundation.base_module import (  # noqa: E402
    FoundationBaseModule,
)
from ansible_collections.nutanix.ncp.plugins.module_utils.foundation.enumerate_aos_packages import (  # noqa: E402
    EnumerateAOSPackages,
)
from ansible_collections.nutanix.ncp.plugins.module_utils.foundation.foundation import (  # noqa: E402
    Foundation,
)
from ansible_collections.nutanix.ncp.plugins.module_utils.utils import (  # noqa: E402
    remove_param_with_none_value,
)


def get_module_spec():
    module_args = dict()

    return module_args


def list_aos_packages(module, result):
  packages = EnumerateAOSPackages(module)
  resp, status = packages.list()
  if status["error"]:
        result["error"] = status["error"]
        module.fail_json(msg="Failed list AOS packages", **result)
  result["aos_packages"] = resp


def run_module():
    module = FoundationBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {}
    list_aos_packages(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
