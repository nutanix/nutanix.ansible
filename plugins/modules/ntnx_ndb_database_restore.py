#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_database_restore
short_description: write
version_added: 1.8.0
description: 'write'
options:
      pitr_timestamp:
        description:
            - write
        type: str
      snapshot_uuid:
        description:
            - write
        type: str
      timezone:
        description:
            - write
        type: str
      db_uuid:
        description:
            - write
        type: str
        required: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
"""

EXAMPLES = r"""
"""
RETURN = r"""


"""
import time  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.database_instances import DatabaseInstance  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        snapshot_uuid=dict(type="str", required=False),
        pitr_timestamp=dict(type="str", required=False),
        db_uuid=dict(type="str", required=True),
        timezone=dict(type="str", required=False),
    )
    return module_args


def restore_database(module, result):
    db = DatabaseInstance(module)
    db_uuid = module.params.get("db_uuid")
    if not db_uuid:
        module.fail_json(msg="db_uuid is required field for restoring", **result)

    spec = db.get_restore_spec(module.params)

    if module.check_mode:
        result["response"] = spec
        return

    resp = db.restore(uuid=db_uuid, data=spec)
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        time.sleep(5)  # to get operation ID functional
        operations = Operation(module)
        resp = operations.wait_for_completion(ops_uuid)
        result["response"] = resp

    result["changed"] = True
    result["db_uuid"] = db_uuid


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_together=[("pitr_timestamp", "timezone")],
        mutually_exclusive=[("snapshot_uuid", "pitr_timestamp")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "db_uuid": None}

    restore_database(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()