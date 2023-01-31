#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

import time

__metaclass__ = type

DOCUMENTATION = r"""
"""

EXAMPLES = r"""

"""

RETURN = r"""

"""
from copy import deepcopy  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.database_instances import DatabaseInstance
from ..module_utils.ndb.db_server_vm import DBServerVM
from ..module_utils.ndb.maintenance_window import (
    AutomatedPatchingSpec,
    MaintenanceWindow,
)
from ..module_utils.ndb.operations import Operation
from ..module_utils.ndb.tags import Tag
from ..module_utils.ndb.time_machines import TimeMachine
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    automated_patching = deepcopy(
        AutomatedPatchingSpec.automated_patching_argument_spec
    )
    registered_vm = dict(
        name=dict(type="str", required=False),
        uuid=dict(type="str", required=False),
        ip=dict(type="str", required=False),
    )

    unregistered_vm = dict(
        ip=dict(type="str", required=True),
        username=dict(type="str", required=True),
        private_key=dict(type="str", required=False),
        password=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        reset_desc_in_ntnx_cluster=dict(type="bool", default=False, required=False),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
    )

    db_vm = dict(
        registered=dict(
            type="dict",
            options=registered_vm,
            mutually_exclusive=["name", "uuid", "ip"],
            required=False,
        ),
        unregistered=dict(
            type="dict",
            options=unregistered_vm,
            mutually_exclusive=["password", "private_key"],
            required=False,
        ),
    )

    sla = dict(
        uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
    )

    schedule = dict(
        daily=dict(type="str", required=False),
        weekly=dict(type="str", required=False),
        monthly=dict(type="int", required=False),
        quaterly=dict(type="str", required=False),
        yearly=dict(type="str", required=False),
        log_catchup=dict(type="int", choices=[15, 30, 60, 90, 120], required=False),
        snapshots_per_day=dict(type="int", required=False, default=1),
    )

    time_machine = dict(
        name=dict(type="str", required=True),
        desc=dict(type="str", required=False),
        sla=dict(
            type="dict",
            options=sla,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        schedule=dict(type="dict", options=schedule, required=True),
        auto_tune_log_drive=dict(type="bool", required=False, default=True),
    )

    postgres = dict(
        listener_port=dict(type="str", default="5432", required=False),
        db_name=dict(type="str", required=True),
        db_password=dict(type="str", required=True, no_log=True),
        db_user=dict(type="str", default="postgres", required=False),
        backup_policy=dict(
            type="str",
            choices=["primary_only", "prefer_secondary", "secondary_only"],
            default="prefer_secondary",
            required=False,
        ),  # check if required
        software_path=dict(type="str", required=True),
        type=dict(dict="str", choices=["single"], default="single", required=False),
    )

    module_args = dict(
        name=dict(type="str", required=True),
        desc=dict(type="str", required=False),
        db_vm=dict(
            type="dict",
            options=db_vm,
            mutually_exclusive=["registered", "unregistered"],
            required=True,
        ),
        time_machine=dict(type="dict", options=time_machine, required=True),
        postgres=dict(type="dict", options=postgres, required=False),
        tags=dict(type="dict", required=False),
        auto_tune_staging_drive=dict(type="bool", required=False),
        working_directory=dict(type="str", default="/tmp", required=False),
        automated_patching=dict(
            type="dict", options=automated_patching, required=False
        ),
    )
    return module_args


def get_registration_spec(module, result):

    # create database instance obj
    db_instance = DatabaseInstance(module=module)

    # get default spec
    spec = db_instance.get_default_registration_spec()

    # populate VM related spec
    db_vm = DBServerVM(module=module)

    use_registered_server = True if module.params.get("db_vm", {}).get("registered") else False
    register_server = not use_registered_server

    kwargs = {
        "use_registered_server": use_registered_server,
        "register_server": register_server,
        "db_instance_register": True,
    }
    spec, err = db_vm.get_spec(old_spec=spec, **kwargs)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting vm spec for new database instance registration",
            **result,
        )

    # populate database engine related spec
    spec, err = db_instance.get_db_engine_spec(spec, register=True)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting database engine related spec for database instance registration",
            **result,
        )

    # populate database instance related spec
    spec, err = db_instance.get_spec(spec, register=True)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for database instance registration", **result
        )

    # populate time machine related spec
    time_machine = TimeMachine(module)
    spec, err = time_machine.get_spec(spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for time machine for database instance registration",
            **result,
        )

    # populate tags related spec
    tags = Tag(module)
    spec, err = tags.get_spec(spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for tags for database instance registration",
            **result,
        )

    # configure automated patching
    if module.params.get("automated_patching"):
        mw = MaintenanceWindow(module)
        mw_spec, err = mw.get_spec(configure_automated_patching=True)
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed getting spec for automated patching in database instance",
                **result,
            )
        spec["maintenanceTasks"] = mw_spec

    return spec


def register_instance(module, result):
    db_instance = DatabaseInstance(module)

    spec = get_registration_spec(module, result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = db_instance.register(data=spec)
    result["response"] = resp
    result["db_uuid"] = resp["entityId"]
    db_uuid = resp["entityId"]

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid)
        resp = db_instance.read(db_uuid)
        result["response"] = resp

    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "db_uuid": None}
    register_instance(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
