#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from email.policy import default

__metaclass__ = type

import time  # noqa: E402
from copy import deepcopy  # noqa: E402
from ..module_utils.ndb.base_module import NdbBaseModule
from ..module_utils.ndb.database_clones import DatabaseClones
from ..module_utils.ndb.db_server_vm import DBServerVM
from ..module_utils.ndb.operations import Operation
from ..module_utils.ndb.tags import Tag
from ..module_utils.ndb.time_machines import TimeMachine
from ..module_utils.utils import remove_param_with_none_value

def get_module_spec():

    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    new_server = dict(
        name=dict(type="str", required=True),
        desc=dict(type="str", required=False),
        pub_ssh_key=dict(type="str", required=True, no_log=True),
        password=dict(type="str", required=True, no_log=True),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        network_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        compute_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
    )

    db_vm = dict(
        create_new_server=dict(type="dict", options=new_server, required=False),
        use_authorized_server=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
    )


    time_machine = dict(
        name=dict(type="str", required=False),
        uuid=dict(type="str", required=False),
        snapshot_uuid=dict(type="str", required=False),
        pitr_timestamp=dict(type="str",required=False),
        timezone=dict(type="str", default="Asia/Calcutta", required=False),
    )

    postgres = dict(
        db_password=dict(type="str", required=True, no_log=True),
        pre_clone_cmd=dict(type="str", required=False),
        post_clone_cmd=dict(type="str", required=False),
    )

    removal_schedule = dict(
        days=dict(type="int", required=False),
        timezone=dict(type="str", default="Asia/Calcutta", required=False),
        delete_database=dict(type="bool", default=False, required=False)
    )

    refresh_schedule = dict(
        days=dict(type="int", required=False),
        timezone=dict(type="str", default="Asia/Calcutta", required=False),
        time=dict(type="str", required=False),
    )

    module_args = dict(
        uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        db_params_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        db_vm=dict(
            type="dict",
            options=db_vm,
            mutually_exclusive=[("create_new_server", "use_authorized_server")],
            required=False,
        ),
        time_machine=dict(type="dict", options=time_machine, required=False),
        postgres=dict(type="dict", options=postgres, required=False),
        tags=dict(type="dict", required=False),
        removal_schedule=dict(type="dict", options=removal_schedule, required=False),
        refresh_schedule=dict(type="dict", options=refresh_schedule, required=False)
    )
    return module_args


def get_clone_spec(module, result, time_machine_uuid):

    # create database instance obj
    db_clone = DatabaseClones(module=module)

    spec, err = db_clone.get_spec()
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting database clone spec",
            **result,
        )

    # populate database engine related spec
    spec, err = db_clone.get_db_engine_spec(spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting database engine related spec for database clone",
            **result,
        )

    # populate database instance related spec
    db_server_vms = DBServerVM(module)
    spec, err = db_server_vms.get_spec(old_spec=spec, db_clone=True, time_machine_uuid=time_machine_uuid)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed getting spec for db server hosting database clone", **result)


    # populate tags related spec
    tags = Tag(module)
    spec, err = tags.get_spec(old_spec=spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for tags for database clone",
            **result,
        )

    return spec


def create_db_clone(module, result):
    db_clone = DatabaseClones(module)
    time_machine = TimeMachine(module)

    time_machine_config = module.params.get("time_machine")
    if not time_machine_config:
        return module.fail_json(msg="time_machine is required field for create", **result)
    time_machine_uuid, err = time_machine.get_time_machine_uuid(time_machine_config)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting time machine uuid for database clone",
            **result,
        )
    spec = get_clone_spec(module, result, time_machine_uuid=time_machine_uuid)

    if module.check_mode:
        result["response"] = spec
        return

    resp = db_clone.clone(data=spec, time_machine_uuid=time_machine_uuid)
    result["response"] = resp
    result["db_uuid"] = resp["entityId"]
    db_uuid = resp["entityId"]

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid)
        resp = db_clone.read(db_uuid)
        result["response"] = resp

    result["changed"] = True

def update_db_clone(module, result):
    pass

def delete_db_clone(module, result):
    pass

def run_module():

    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    if module.params["state"] == "present":
        if module.params.get("uuid"):
            update_db_clone(module, result)
        else:
            create_db_clone(module, result)
    else:
        delete_db_clone(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
