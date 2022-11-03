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
import time  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.databases import Database  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        snapshot_uuid=dict(type="str", required=False),
        point_in_time=dict(type="str", required=False),
        db_uuid=dict(type="str", required=True),
        time_zone=dict(type="str", required=False),
    )
    return module_args


# restore database from following:
# 1. Snapshot UUID
# 2. Latest snapshot
# 3. Point in time recovery timestamp
def restore_database(module, result):
    pass


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[("snapshot_uuid", "pitr_timestamp")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}

    restore_database(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
