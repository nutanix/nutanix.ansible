#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ndb_database_clones
short_description: write
version_added: 1.8.0-beta.1
description: 'write'
options:
      uuid:
        description:
            - write
        type: str
      name:
        description:
            - write
        type: str
      desc:
        description:
            - write
        type: str
      db_params_profile:
        description:
            - write
        type: dict
        suboptions:
            uuid:
                description:
                    - write
                type: str
            name:
                description:
                    - write
                type: str
      db_vm:
        description:
            - write
        type: dict
        suboptions:
            create_new_server:
                description:
                    - write
                type: dict
                suboptions:
                    name:
                        description:
                            - write
                        type: str
                        required: true
                    desc:
                        description:
                            - write
                        type: str
                    pub_ssh_key:
                        description:
                            - write
                        type: str
                        required: true
                    password:
                        description:
                            - write
                        type: str
                        required: true
                    cluster:
                        description:
                            - write
                        type: dict
                        required: true
                        suboptions:
                            uuid:
                                description:
                                    - write
                                type: str
                            name:
                                description:
                                    - write
                                type: str
                    network_profile:
                        description:
                            - write
                        type: dict
                        required: true
                        suboptions:
                            uuid:
                                description:
                                    - write
                                type: str
                            name:
                                description:
                                    - write
                                type: str
                    compute_profile:
                        description:
                            - write
                        type: dict
                        required: true
                        suboptions:
                            uuid:
                                description:
                                    - write
                                type: str
                            name:
                                description:
                                    - write
                                type: str

            use_authorized_server:
                description:
                    - write
                type: dict
                suboptions:
                    uuid:
                        description:
                            - write
                        type: str
                    name:
                        description:
                            - write
                        type: str
      time_machine:
        description:
            - write
        type: dict
        suboptions:
            name:
                description:
                    - write
                type: str
                required: true
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
      postgres:
        description:
            - write
        type: dict
        suboptions:
            db_password:
                description:
                    - write
                type: str
                required: true
            pre_clone_cmd:
                description:
                    - write
                type: str
            post_clone_cmd:
                description:
                    - write
                type: str
      tags:
        description:
            - write
        type: dict
      removal_schedule:
        description:
            - write
        type: dict
        suboptions:
            state:
                description:
                    - write
                type: str
                choices: ["present", "absent"]
                default: "present"
            days:
                description:
                    - write
                type: int
            timezone:
                description:
                    - write
                type: str
            delete_database:
                description:
                    - write
                type: bool
                default: false
            timestamp:
                description:
                    - write
                type: str
            remind_before_in_days:
                description:
                    - write
                type: int
      refresh_schedule:
        description:
            - write
        type: dict
        suboptions:
            state:
                description:
                    - write
                type: str
                choices: ["present", "absent"]
                default: "present"
            days:
                description:
                    - write
                type: int
            timezone:
                description:
                    - write
                type: str
            time:
                description:
                    - write
                type: str
      delete_from_vm:
        description:
            - write
        type: bool
      soft_remove:
        description:
            - write
        type: bool
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
from ..module_utils.ndb.db_server_vm import DBServerVM  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.ndb.tags import Tag  # noqa: E402
from ..module_utils.ndb.time_machines import TimeMachine  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


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
        pitr_timestamp=dict(type="str", required=False),
        timezone=dict(type="str", default="Asia/Calcutta", required=False),
    )

    postgres = dict(
        db_password=dict(type="str", required=True, no_log=True),
        pre_clone_cmd=dict(type="str", required=False),
        post_clone_cmd=dict(type="str", required=False),
    )

    removal_schedule = dict(
        state=dict(
            type="str", choices=["present", "absent"], default="present", required=False
        ),
        days=dict(type="int", required=False),
        timezone=dict(type="str", required=False),
        delete_database=dict(type="bool", default=False, required=False),
        timestamp=dict(type="str", required=False),
        remind_before_in_days=dict(type="int", required=False),
    )

    refresh_schedule = dict(
        state=dict(
            type="str", choices=["present", "absent"], default="present", required=False
        ),
        days=dict(type="int", required=False),
        timezone=dict(type="str", required=False),
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
        time_machine=dict(
            type="dict",
            options=time_machine,
            mutually_exclusive=[("snapshot_uuid", "pitr_snapshot")],
            required=False,
        ),
        postgres=dict(type="dict", options=postgres, required=False),
        tags=dict(type="dict", required=False),
        removal_schedule=dict(
            type="dict",
            options=removal_schedule,
            mutually_exclusive=[
                ("days", "timestamp"),
            ],
            required=False,
        ),
        refresh_schedule=dict(type="dict", options=refresh_schedule, required=False),
        delete_from_vm=dict(type="bool", required=False),
        soft_remove=dict(type="bool", required=False),
    )
    return module_args


def get_clone_spec(module, result, time_machine_uuid):

    # create database instance obj
    db_clone = DatabaseClone(module=module)

    spec, err = db_clone.get_spec(create=True)
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

    provision_new_server = (
        True if module.params.get("db_vm", {}).get("create_new_server") else False
    )
    use_athorized_server = not provision_new_server

    kwargs = {
        "time_machine_uuid": time_machine_uuid,
        "db_clone": True,
        "provision_new_server": provision_new_server,
        "use_authorized_server": use_athorized_server,
    }

    spec, err = db_server_vms.get_spec(old_spec=spec, **kwargs)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting vm spec for database clone",
            **result,
        )

    # populate tags related spec
    tags = Tag(module)
    spec, err = tags.get_spec(old_spec=spec, associate_to_entity=True, type="CLONE")
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for tags for database clone",
            **result,
        )

    return spec


def create_db_clone(module, result):
    db_clone = DatabaseClone(module)
    time_machine = TimeMachine(module)

    time_machine_config = module.params.get("time_machine")
    if not time_machine_config:
        return module.fail_json(
            msg="time_machine is required field for create", **result
        )
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

    resp = db_clone.create(time_machine_uuid=time_machine_uuid, data=spec)
    result["response"] = resp
    result["uuid"] = resp["entityId"]
    uuid = resp["entityId"]

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=15)
        resp = db_clone.read(uuid)
        result["response"] = resp

    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):
    if (
        old_spec["name"] != update_spec["name"]
        or old_spec["description"] != update_spec["description"]
    ):
        return False

    if update_spec.get("removeRefreshConfig") or update_spec.get("removeExpiryConfig"):
        return False

    if old_spec["lcmConfig"].get("expiryDetails") != update_spec["lcmConfig"].get(
        "expiryDetails"
    ):
        return False

    if old_spec["lcmConfig"].get("refreshDetails") != update_spec["lcmConfig"].get(
        "refreshDetails"
    ):
        return False

    if len(old_spec["tags"]) != len(update_spec["tags"]):
        return False

    old_tag_values = {}
    new_tag_values = {}
    for i in range(len(old_spec["tags"])):
        old_tag_values[old_spec["tags"][i]["tagName"]] = old_spec["tags"][i]["value"]
        new_tag_values[update_spec["tags"][i]["tagName"]] = update_spec["tags"][i][
            "value"
        ]

    if old_tag_values != new_tag_values:
        return False

    return True


def update_db_clone(module, result):
    _clones = DatabaseClone(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for update", **result)
    result["uuid"] = uuid

    resp = _clones.read(uuid)
    old_spec = _clones.get_default_update_spec(override_spec=resp)

    spec, err = _clones.get_spec(old_spec=old_spec, update=True)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update database clone spec", **result)

    # populate tags related spec
    if module.params.get("tags"):
        tags = Tag(module)
        spec, err = tags.get_spec(old_spec=spec, associate_to_entity=True, type="CLONE")
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed getting spec for tags for updating database clone",
                **result,
            )

    if module.check_mode:
        result["response"] = spec
        return

    if check_for_idempotency(old_spec, spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = _clones.update(data=spec, uuid=uuid)
    result["response"] = resp
    result["uuid"] = uuid
    result["changed"] = True


def delete_db_clone(module, result):
    _clones = DatabaseClone(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for delete", **result)

    default_spec = _clones.get_default_delete_spec()
    spec, err = _clones.get_spec(old_spec=default_spec, delete=True)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for deleting database clone",
            **result,
        )

    if module.check_mode:
        result["response"] = spec
        return

    resp = _clones.delete(uuid, data=spec)

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        time.sleep(5)  # to get operation ID functional
        operations = Operation(module)
        resp = operations.wait_for_completion(ops_uuid, delay=5)

    result["response"] = resp
    result["changed"] = True


def run_module():
    mutually_exclusive_list = [
        ("uuid", "db_params_profile"),
        ("uuid", "db_vm"),
        ("uuid", "postgres"),
        ("uuid", "time_machine"),
        ("delete_from_vm", "soft_remove"),
    ]
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=mutually_exclusive_list,
        required_if=[
            ("state", "present", ("name", "uuid"), True),
            ("state", "absent", ("uuid",)),
        ],
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
