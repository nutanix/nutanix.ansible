#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_floating_ips_info
short_description: 
version_added: 1.0.0
description: 'Create, Update, Delete, Power-on, Power-off Nutanix VM''s'
options:
  nutanix_host:
    description:
      - Prism central hostname or IP address
      - C(nutanix_host). If not set then the value of the C(NUTANIX_HOST), environment variable is used.
    type: str
    required: true
  nutanix_port:
    description:
      - Prism central port
      - C(nutanix_port). If not set then the value of the C(NUTANIX_PORT), environment variable is used.
    type: str
    default: 9440
  nutanix_username:
    description:
      - Prism central username
      - C(nutanix_username). If not set then the value of the C(NUTANIX_USERNAME), environment variable is used.
    type: str
    required: true
  nutanix_password:
    description:
      - Prism central password
      - C(nutanix_password). If not set then the value of the C(NUTANIX_PASSWORD), environment variable is used.
    required: true
    type: str
  validate_certs:
    description:
        - Set value to C(False) to skip validation for self signed certificates
        - This is not recommended for production setup
        - C(validate_certs). If not set then the value of the C(VALIDATE_CERTS), environment variable is used.
    type: bool
    default: true
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

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.floating_ips import FloatingIP  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        kind=dict(type="str", default="floating_ip"),
        offset=dict(type="int"),
        length=dict(type="int"),
        filter=dict(type="str"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def list_vm(module, result):
    floating_ip = FloatingIP(module)
    spec, error = floating_ip.get_info_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating filter Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp, status = floating_ip.list(spec)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed to get information", **result)

    result["changed"] = False
    result["response"] = resp


def run_module():
    module = BaseModule(argument_spec=get_module_spec(), supports_check_mode=True)
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    list_vm(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
