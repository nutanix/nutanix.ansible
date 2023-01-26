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
from ..module_utils.ndb.database_instances import DatabaseInstance  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        db_instance_uuid=dict(type="str", required=True),
        database_uuid=dict(type="str", required=False),
        databases=dict(type="list", elements="str", required=False),
    )
    return module_args


def add_database(module, result):
    instance_uuid = module.params.get("db_instance_uuid")
    if not instance_uuid:
        return module.fail_json(
            msg="db_instance_uuid is required field for adding databases to database instance",
            **result,
        )
    result["db_instance_uuid"] = instance_uuid

    _databases = DatabaseInstance(module)
    databases = module.params.get("databases")
    if not databases:
        return module.exit_json(msg="No database to add", **result)

    spec = _databases.get_add_database_spec(databases)
    if module.check_mode:
        result["response"] = spec
        return

    resp = _databases.add_databases(instance_uuid, spec)
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        time.sleep(3)  # to get operation ID functional
        operations = Operation(module)
        operations.wait_for_completion(ops_uuid, delay=5)
        resp = _databases.read(uuid=instance_uuid)
        result["response"] = resp.get("linkedDatabases", [])

    result["changed"] = True


def remove_database(module, result):
    instance_uuid = module.params.get("db_instance_uuid")
    database_uuid = module.params.get("database_uuid")
    if not database_uuid or not instance_uuid:
        module.fail_json(
            msg="database_uuid and instance_uuid are required fields for deleting database from database instance",
            **result,
        )

    _databases = DatabaseInstance(module)
    resp = _databases.remove_linked_database(
        database_uuid=database_uuid, instance_uuid=instance_uuid
    )
    result["response"] = resp
    result["db_instance_uuid"] = instance_uuid

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get ops ID functional
        operations.wait_for_completion(ops_uuid, delay=5)
        resp = _databases.read(uuid=instance_uuid)
        result["response"] = resp.get("linkedDatabases", [])

    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[("databases", "database_uuid")],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "db_instance_uuid": None,
    }

    if module.params["state"] == "present":
        add_database(module, result)
    else:
        remove_database(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
