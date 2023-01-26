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

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.maintenance_window import MaintenanceWindow  # noqa: E402


def get_module_spec():

    module_args = dict(
        uuid=dict(type="str"),
    )

    return module_args


def get_maintenance_windows(module, result):
    mw = MaintenanceWindow(module)
    resp = mw.read(uuid=module.params.get("uuid"))
    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    result = {"changed": False, "error": None, "response": None}
    get_maintenance_windows(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
