#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

__metaclass__ = type

DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils.ndb.databases import Database
from ..module_utils.ndb.operations import Operation
from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.utils import check_for_idempotency, remove_param_with_none_value, strip_extra_attrs


def get_module_spec():
    default_db_arguments = dict(
        db_size=dict(type="str", required=True),
        pre_create_script=dict(type="str", required=False),
        post_create_script=dict(type="str", required=False),
    )
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    new_server = dict(
        name=dict(type="str", required=True),
        pub_ssh_key=dict(type="str", required=True),
        password=dict(type="str", required=True),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        software_profile=dict(
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
        create_new_server=dict(type="dict", options=new_server),
        use_registered_server=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
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
        auto_tune_log_drive=dict(type="dict", required=False, default=True),
    )

    postgress = dict(
        listener_port=dict(type=int, required=True),
        db_name=dict(type="str", required=True),
        db_password=dict(type="str", required=True),
        auto_tune_staging_drive=dict(type="bool", default=True, required=False),
        allocate_pg_hugepage=dict(type="bool", default=False, required=False),
        auth_method=dict(type="str", default="md5", required=False),
        cluster_database=dict(type="bool", default=False, required=False),
    )
    postgress.update(deepcopy(default_db_arguments))

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
            mutually_exclusive=[("create_new_server", "create_new_server")],
            required=False,
        ),
        time_machine=dict(type="dict", options=time_machine, required=False),
        postgress=dict(type="dict", options=postgress, required=False),
        tags=dict(type="dict", required=False),
        auto_tune_staging_drive=dict(type="dict", required=False, default=True),
        soft_delete=dict(type="bool", required=False)
        delete_time_machine=dict(type="bool", required=False)
    )
    return module_args


def create_instance(module, result):
    _databases = Database(module)

    name = module.params["name"]
    uuid, err = _databases.get_uuid(name)
    if uuid:
        module.fail_json(msg="Database instance with given name already exists", **result)

    spec, err = _databases.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create database instance spec", **result)
    
    if module.check_mode:
        result["response"] = spec
        return
    
    resp = _databases.create(data=spec)
    result["response"] = resp
    result["uuid"] = resp["dbserverId"]
    db_uuid = resp["dbserverId"]

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        operations.wait_for_completion(ops_uuid)
        resp = _databases.read(db_uuid)
        result["response"] = resp

    result["changed"] = True

def check_for_idempotency(old_spec, update_spec):
    if old_spec["name"] != update_spec["name"] or old_spec["description"]!=update_spec["description"]:
        return False
    
    if len(old_spec["tags"]) != len(update_spec["tags"]):
        return False

    old_tag_values = {}
    new_tag_values = {}
    for i in range(len(old_spec["tags"])):
        old_tag_values[old_spec["tags"][i]["tagName"]] = old_tag_values[old_spec["tags"][i]["value"]]
        new_tag_values[update_spec["tags"][i]["tagName"]] =  new_tag_values[update_spec["tags"][i]["value"]]

    if old_tag_values != new_tag_values:
        return False
    
    return True

def update_instance(module, result):
    _databases = Database(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for update", **result)

    # only certain fields are allowed to update
    resp = _databases.read(uuid)
    default_update_spec = _databases.get_update_spec()
    strip_extra_attrs(resp, default_update_spec)
    update_spec, err = _databases.get_spec(old_spec=resp)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update database instance spec", **result)
    
    if module.check_mode:
        result["response"] = update_spec
        return
    
    if check_for_idempotency(resp, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to update.")

    resp = _databases.update(data=update_spec)
    result["response"] = resp
    result["uuid"] = uuid
    result["changed"] = True


def delete_instance(module, result):
    _databases = Database(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for delete", **result)

    spec = _databases.get_delete_spec()
    if module.params.get("soft_delete"):
        spec["remove"] = True
        spec["delete"] = False
    else:
        spec["delete"] = True
        spec["remove"] = False
    
    if module.params.get("delete_time_machine"):
        spec["deleteTimeMachine"] = True
    
    resp = _databases.delete(uuid)

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        resp = operations.wait_for_completion(ops_uuid)

    result["response"] = resp
    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    if module.params["state"] == "present":
        if module.params.get("uuid"):
            update_instance(module, result)
        else:
            create_instance(module, result)
    else:
        delete_instance(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
