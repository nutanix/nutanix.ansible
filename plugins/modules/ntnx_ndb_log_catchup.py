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
from ..module_utils.ndb.time_machines import TimeMachine  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    module_args = dict(
        time_machine=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        database=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        for_restore=dict(type="bool", required=False, default=False)
    )
    return module_args

def log_catchup(module, result):
    time_machine_uuid = ""
    tm = TimeMachine(module)

    # fetch uuid from time machine or database
    if module.params.get("time_machine"):
        time_machine_uuid, err = tm.get_time_machine_uuid(module.params["time_machine"])
        if err:
            result["error"] = err
            module.fail_json(msg="Failed fetching time machine uuid", **result)
    else:
        database = Database(module)
        db, err = database.get_database(name=module.params["database"].get("name"), uuid=module.params["database"].get("uuid"))
        if err:
            result["error"] = err
            module.fail_json(msg="Failed fetching time machine uuid from database", **result)
        time_machine_uuid = db["timeMachineId"]

    for_restore = module.params.get("for_restore")
    spec = tm.get_log_catchup_spec(for_restore)
    if module.check_mode:
        result["response"] = spec
        return
    
    resp = tm.log_catchup(time_machine_uuid=time_machine_uuid, data=spec)
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        time.sleep(5)  # to get operation ID functional
        operations = Operation(module)
        resp = operations.wait_for_completion(ops_uuid)
        result["response"] = resp

    result["changed"] = True

def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[("time_machine", "database")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}

    log_catchup(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
