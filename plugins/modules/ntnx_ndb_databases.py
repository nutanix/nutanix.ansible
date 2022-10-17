#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_databases
short_description: write
version_added: 1.7.0
description: write
options:
  db_uuid:
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
      name:
        type: str
        description: write
      uuid:
        type: str
        description: write
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
            type: str
            description: write
            required: true
          pub_ssh_key:
            type: str
            description: write
            required: true
          password:
            type: str
            description: write
            required: true
          cluster:
            description:
              - write
            type: dict
            required: true
            suboptions:
              name:
                type: str
                description: write
              uuid:
                type: str
                description: write
          software_profile:
            description:
              - write
            type: dict
            required: true
            suboptions:
              name:
                type: str
                description: write
              uuid:
                type: str
                description: write
          network_profile:
            description:
              - write
            type: dict
            required: true
            suboptions:
              name:
                type: str
                description: write
              uuid:
                type: str
                description: write
          compute_profile:
            description:
              - write
            type: dict
            required: true
            suboptions:
              name:
                type: str
                description: write
              uuid:
                type: str
                description: write
      use_registered_server:
        description:
          - write
        type: dict
        suboptions:
          name:
            type: str
            description: write
          uuid:
            type: str
            description: write
  time_machine:
        description:
          - write
        type: dict
        suboptions:
          name:
            type: str
            description: write
            required: True
          desc:
            type: str
            description: write
          sla:
            type: dict
            description: write
            required: True
            suboptions:
                name:
                    type: str
                    description: write
                uuid:
                    type: str
                    description: write
          schedule:
                type: dict
                description: write
                required: True
                suboptons:
                    daily:
                        type: str
                        description: write
                    weekly:
                        type: str
                        description: write
                    monthly:
                        type: int
                        description: write
                    quaterly:
                        type: str
                        description: write
                    yearly:
                        type: str
                        description: write
                    log_catchup:
                        type: int
                        description: write
                        choices: [15, 30, 60, 90, 120]
                    snapshots_per_day:
                        type: int
                        description: write
                        default: 1
          auto_tune_log_drive:
            type: bool
            default: true
            description: write
  postgres:
    type: dict
    description: write
    suboptions:
                    listener_port:
                        type: str
                        description: write
                        required: true
                    db_name:
                        type: int
                        description: write
                        required: true
                    db_password:
                        type: str
                        description: write
                        required: true
                    auto_tune_staging_drive:
                        type: bool
                        default: true
                        description: write
                    allocate_pg_hugepage:
                        type: bool
                        default: false
                        description: write
                    auth_method:
                        type: str
                        default: md5
                        description: write
                    cluster_database:
                        type: bool
                        default: false
                        description: write
  tags:
    type: dict
    description: write
  auto_tune_staging_drive:
    type: bool
    description: write
  soft_delete:
    type: bool
    description: write
  delete_time_machine:
    type: bool
    description: write
extends_documentation_fragment:
#   - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Pradeepsingh Bhati (@bhati-pradeep)

"""
EXAMPLES = r"""
"""

RETURN = r"""
"""
import time  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.databases import Database  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.utils import (  # noqa: E402
    check_for_idempotency,
    remove_param_with_none_value,
)


def get_module_spec():
    default_db_arguments = dict(
        db_size=dict(type="int", required=True),
        pre_create_script=dict(type="str", required=False),
        post_create_script=dict(type="str", required=False),
    )
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    new_server = dict(
        name=dict(type="str", required=True),
        pub_ssh_key=dict(type="str", required=True, no_log=True),
        password=dict(type="str", required=True, no_log=True),  # Add no log
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
        create_new_server=dict(type="dict", options=new_server, required=False),
        use_registered_server=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
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
        listener_port=dict(type="str", required=True),
        db_name=dict(type="str", required=True),
        db_password=dict(type="str", required=True, no_log=True),  # Add no log
        auto_tune_staging_drive=dict(type="bool", default=True, required=False),
        allocate_pg_hugepage=dict(type="bool", default=False, required=False),
        auth_method=dict(type="str", default="md5", required=False),
        cluster_database=dict(type="bool", default=False, required=False),
    )
    postgres.update(deepcopy(default_db_arguments))

    module_args = dict(
        db_uuid=dict(type="str", required=False),
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
            mutually_exclusive=[("create_new_server", "use_registered_server")],
            required=False,
        ),
        time_machine=dict(type="dict", options=time_machine, required=False),
        postgres=dict(type="dict", options=postgres, required=False),
        tags=dict(type="dict", required=False),
        auto_tune_staging_drive=dict(type="bool", required=False),
        soft_delete=dict(type="bool", required=False),
        delete_time_machine=dict(type="bool", required=False),
    )
    return module_args


def create_instance(module, result):
    _databases = Database(module)

    name = module.params["name"]
    uuid, err = _databases.get_uuid(name)
    if uuid:
        module.fail_json(
            msg="Database instance with given name already exists", **result
        )

    spec, err = _databases.get_spec()
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create database instance spec", **result
        )

    if module.check_mode:
        result["response"] = spec
        return

    resp = _databases.create(data=spec)
    result["response"] = resp
    result["db_uuid"] = resp["entityId"]
    db_uuid = resp["entityId"]

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid)
        resp = _databases.read(db_uuid)
        result["response"] = resp

    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):
    if (
        old_spec["name"] != update_spec["name"]
        or old_spec["description"] != update_spec["description"]
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


def update_instance(module, result):
    _databases = Database(module)

    uuid = module.params.get("db_uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for update", **result)

    resp = _databases.read(uuid)
    old_spec = _databases.get_default_update_spec(override_spec=resp)

    update_spec, err = _databases.get_spec(old_spec=old_spec)

    # due to field name changes
    if update_spec.get("databaseDescription"):
        update_spec["description"] = update_spec.pop("databaseDescription")

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update database instance spec", **result
        )

    if module.check_mode:
        result["response"] = update_spec
        return

    if check_for_idempotency(old_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = _databases.update(data=update_spec, uuid=uuid)
    result["response"] = resp
    result["db_uuid"] = uuid
    result["changed"] = True


def delete_instance(module, result):
    _databases = Database(module)

    uuid = module.params.get("db_uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for delete", **result)

    spec = _databases.get_default_delete_spec()
    if module.params.get("soft_delete"):
        spec["remove"] = True
        spec["delete"] = False
    else:
        spec["delete"] = True
        spec["remove"] = False

    if module.params.get("delete_time_machine"):
        spec["deleteTimeMachine"] = True

    if module.check_mode:
        result["response"] = spec
        return

    resp = _databases.delete(uuid, data=spec)

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        time.sleep(5)  # to get operation ID functional
        operations = Operation(module)
        resp = operations.wait_for_completion(ops_uuid)

    result["response"] = resp
    result["changed"] = True


def run_module():
    mutually_exclusive_list = [
        ("db_uuid", "db_params_profile"),
        ("db_uuid", "db_vm"),
        ("db_uuid", "postgres"),
        ("db_uuid", "time_machine"),
        ("db_uuid", "auto_tune_staging_drive"),
    ]
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        mutually_exclusive=mutually_exclusive_list,
        required_if=[
            ("state", "present", ("name", "db_uuid"), True),
            ("state", "absent", ("db_uuid",)),
        ],
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "db_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("db_uuid"):
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
