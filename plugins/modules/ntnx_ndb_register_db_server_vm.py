#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import time  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.ndb.db_server_vm import DBServerVM
from ..module_utils.ndb.operations import Operation


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    postgres = dict(
        listener_port=dict(type="str", default="5432", required=False),
        software_path=dict(type="str", required=True),
    )
    module_args = dict(
        ip=dict(type="str", required=True),
        desc=dict(type="str", required=False),
        reset_desc_in_ntnx_cluster=dict(type="bool", default=False, required=False),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        postgres=dict(type="dict", options=postgres, required=False),
        username=dict(type="str", required=True),
        password=dict(type="str", required=False),
        private_ssh_key=dict(type="str", required=False),
        working_directory=dict(type="str", default="/tmp", required=False),
    )
    return module_args


def get_register_spec(module, result):
    db_server_vms = DBServerVM(module)
    default_spec = db_server_vms.get_default_spec_for_registration()
    spec, err = db_server_vms.get_spec(old_spec=default_spec, register=True)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for db server vm registration",
            **result,
        )

    # populate database engine related spec
    spec, err = db_server_vms.get_db_engine_spec(spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting database engine related spec for database instance registration",
            **result,
        )

    return spec


def register_db_server(module, result):
    db_server_vms = DBServerVM(module)

    spec, err = get_register_spec(module, result)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for db server vm registration",
            **result,
        )

    if module.check_mode:
        result["response"] = spec
        return

    resp = db_server_vms.register(data=spec)
    result["response"] = resp
    result["uuid"] = resp["entityId"]
    db_uuid = resp["entityId"]

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid)
        resp = db_server_vms.read(db_uuid)
        result["response"] = resp

    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[("private_ssh_key", "password")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    register_db_server(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
