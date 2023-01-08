#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
import time


__metaclass__ = type

from ..module_utils.ndb.db_server_vm import DBServerVM
from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.utils import (
    remove_param_with_none_value,
    strip_extra_attrs,
)  # noqa: E402
from ..module_utils.ndb.tags import Tag
from ..module_utils.ndb.operations import Operation


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    software_profile = dict(
        name=dict(type="str"), uuid=dict(type="str"), version_id=dict(type="str")
    )
    time_machine = dict(
        name=dict(type="str", required=False),
        uuid=dict(type="str", required=False),
        snapshot_uuid=dict(type="str", required=False),
    )
    credential = dict(
        username=dict(type="str", required=False),
        password=dict(type="str", required=False),
    )
    module_args = dict(
        uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        reset_name_in_ntnx_cluster=dict(type="bool", default=False, required=False),
        reset_desc_in_ntnx_cluster=dict(type="bool", default=False, required=False),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        network_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        compute_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        software_profile=dict(
            type="dict",
            options=software_profile,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        time_machine=dict(
            type="dict",
            options=time_machine,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        password=dict(type="str", required=False),
        pub_ssh_key=dict(type="str", required=False),
        time_zone=dict(type="str", default="Asia/Calcutta", required=False),
        database_type=dict(type="str", choices=["postgres_database"], required=False),
        tags=dict(type="dict", required=False),
        update_credentials=dict(
            type="list", elements="dict", options=credential, required=False
        ),
        delete_from_cluster=dict(type="bool", default=False, required=False),
        delete_vgs=dict(type="bool", default=False, required=False),
        delete_vm_snapshots=dict(type="bool", default=False, required=False),
    )
    return module_args


def create_db_server(module, result):
    db_servers = DBServerVM(module)

    default_spec = db_servers.get_default_spec_for_provision()
    spec, err = db_servers.get_spec(old_spec=default_spec, provision=True)

    if err:
        result["error"] = err
        module.fail_json("Failed getting DB server vm create spec", **result)

    # populate tags related spec
    tags = Tag(module)
    spec, err = tags.get_spec(spec, type="DATABASE_SERVER")
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for tags for new db server vm",
            **result,
        )

    if module.check_mode:
        result["response"] = spec
        return

    resp = db_servers.provision(data=spec)
    result["response"] = resp
    result["uuid"] = resp["entityId"]
    db_uuid = resp["entityId"]

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid)
        resp = db_servers.read(db_uuid)
        result["response"] = resp

    result["changed"] = True


def check_idempotency(old_spec, new_spec):

    # check for arguments
    args = ["name", "description"]
    for arg in args:
        if old_spec[arg] != new_spec[arg]:
            return False

    # check for resets
    args = ["resetDescriptionInNxCluster", "resetNameInNxCluster", "resetCredential"]
    for arg in args:
        if new_spec.get(arg, False):
            return False

    # check for new tags
    if len(old_spec["tags"]) != len(new_spec["tags"]):
        return False

    old_tag_values = {}
    new_tag_values = {}
    for i in range(len(old_spec["tags"])):
        old_tag_values[old_spec["tags"][i]["tagName"]] = old_spec["tags"][i]["value"]
        new_tag_values[new_spec["tags"][i]["tagName"]] = new_spec["tags"][i]["value"]

    if old_tag_values != new_tag_values:
        return False

    return True


def update_db_server(module, result):
    db_servers = DBServerVM(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json("'uuid' is required for updating db server vm")

    db_server = db_servers.read(uuid=uuid)
    update_spec = db_servers.get_default_spec_for_update(old_spec=db_server)
    update_spec, err = db_servers.get_spec(old_spec=update_spec, update=True)
    if err:
        result["error"] = err
        module.fail_json("Failed getting db server vm update spec", **result)

    # populate tags related spec
    if module.params.get("tags"):
        tags = Tag(module)
        update_spec, err = tags.get_spec(update_spec, type="DATABASE_SERVER")
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed getting spec for tags for db server vm update",
                **result,
            )
        update_spec["resetTags"] = True

    if module.check_mode:
        result["response"] = update_spec
        return

    if check_idempotency(old_spec=db_server, new_spec=update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = db_servers.update(data=update_spec, uuid=uuid)
    result["response"] = resp
    result["uuid"] = uuid
    result["changed"] = True


def delete_db_server(module, result):
    db_servers = DBServerVM(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json("'uuid' is required for deleting db server vm")

    spec = db_servers.get_default_delete_spec()
    spec, err = db_servers.get_spec(old_spec=spec, delete=True)
    if err:
        result["error"] = err
        module.fail_json("Failed getting db server delete update spec", **result)

    spec["remove"] = not spec["delete"]

    if module.check_mode:
        result["response"] = spec
        return

    resp = db_servers.delete(data=spec, uuid=uuid)
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
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
            update_db_server(module, result)
        else:
            create_db_server(module, result)
    else:
        delete_db_server(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
