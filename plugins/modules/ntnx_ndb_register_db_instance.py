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
from copy import deepcopy  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.databases import Database  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    registered_vm = dict(
        name=dict(type="str", required=False), 
        uuid=dict(type="str", required=False), 
        ip=dict(type="str", required=False)
    )

    unregistered_vm = dict(
        ip = dict(type="str", required=True),
        username = dict(type="str", required=True),
        private_key = dict(type="str", required=False),
        password = dict(type="str", required=False),
        desc = dict(type="str", required=False),
    )

    db_vm = dict(
        registered=dict(type="dict", options=registered_vm, mutually_exclusive=["name", "uuid", "ip"], required=False),
        unregistered=dict(type="dict", options=unregistered_vm, mutually_exclusive=["password", "private_key"], required=False),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        )
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
        db_password=dict(type="str", required=True, no_log=True),
        db_user=dict(type="str", default="postgres", required=False),
        backup_policy=dict(type="str", choices=["primary_only", "prefer_secondary", "secondary_only"], default="prefer_secondary", required=False), # check if required
        software_path=dict(type="str", required=True),
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
        postgres=dict(type="dict", options=postgres, required=True),
        tags=dict(type="dict", required=False),
        auto_tune_staging_drive=dict(type="bool", required=False),
        working_dir=dict(type="str", default="/tmp"),
    )
    return module_args


def register_instance(module, result):
    pass


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
