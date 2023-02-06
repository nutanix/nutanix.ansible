#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ndb_database_clone_refresh
short_description: write
version_added: 1.8.0-beta.1
description: 'write'
options:
      uuid:
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
        default: "Asia/Calcutta"
      pitr_timestamp:
        description:
            - write
        type: str
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
from ..module_utils.ndb.database_clones import DatabaseClone  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        uuid=dict(type="str", required=False),
        snapshot_uuid=dict(type="str", required=False),
        timezone=dict(type="str", default="Asia/Calcutta", required=False),
        pitr_timestamp=dict(type="str", required=False),
    )
    return module_args


def refresh_clone(module, result):
    db_clone = DatabaseClone(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(
            msg="uuid is required field for database clone refresh", **result
        )

    spec, err = db_clone.get_clone_refresh_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed getting spec for database clone refresh", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = db_clone.refresh(uuid=uuid, data=spec)
    result["response"] = resp
    result["uuid"] = uuid

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid)
        resp = db_clone.read(uuid)
        result["response"] = resp

    result["changed"] = True


def run_module():
    mutually_exclusive_list = [
        ("snapshot_uuid", "pitr_timestamp"),
    ]
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[("state", "present", ("snapshot_uuid", "pitr_timestamp"), True)],
        mutually_exclusive=mutually_exclusive_list,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    refresh_clone(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
