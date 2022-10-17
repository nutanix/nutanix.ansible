#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_tms_info
short_description: tm  info module
version_added: 1.7.0
description: 'Get tm info'
options:
      tm_name:
        description:
            - tm name
        type: str
      tm_id:
        description:
            - tm id
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""

"""
RETURN = r"""

"""

from ..module_utils.ndb.nutanix_database import NutanixDatabase  # noqa: E402
from ..module_utils.ndb.time_machines import TM  # noqa: E402


def get_module_spec():

    module_args = dict(
        tm_name=dict(type="str"),
        tm_id=dict(type="str"),
    )

    return module_args


def get_tm(module, result):
    tm = TM(module)
    if module.params.get("tm_name"):
        tm_name = module.params["tm_name"]
        tm_option = "{0}/{1}".format("name", tm_name)
    else:
        tm_option = "{0}".format(module.params["tm_id"])

    resp = tm.read(tm_option)

    result["response"] = resp


def get_tms(module, result):
    tm = TM(module)

    resp = tm.read()

    result["response"] = resp


def run_module():
    module = NutanixDatabase(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
        mutually_exclusive=[("tm_name", "tm_id")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("tm_name") or module.params.get("tm_id"):
        get_tm(module, result)
    else:
        get_tms(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
