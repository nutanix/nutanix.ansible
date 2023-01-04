#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402




def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    software_profile = dict(name=dict(type="str"), uuid=dict(type="str"), version_id=dict(type="str"))
    time_machine = dict(
        name = dict(type="str", required=False),
        uuid = dict(type="str", required=False),
        snapshot_uuid = dict(type="str", required=False),
    )
    source = dict(
        time_machine = dict(type="dict", options=time_machine, mutually_exclusive=mutually_exclusive, required=False),
        software_profile = dict(type="dict", options=software_profile, mutually_exclusive=mutually_exclusive, required=False)
    )
    module_args = dict(
        uuid = dict(type="str", required=False),
        name = dict(type="str", required=False),
        desc = dict(type="str", required=False),
        source = dict(type="dict", options=source, mutually_exclusive=[("time_machine", "software_profile")], required=False),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        network_profile = dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        compute_profile = dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        password=dict(type="str", required=False),
        public_ssh_key = dict(type="str", required=False),
        time_zone = dict(type="str", default="Asia/Calcutta", required=False),
        database_type = dict(type="str", choices = ["postgres"], required=False),
    )
    return module_args

def create_db_server(module, result):
    pass

def update_db_server(module, result):
    pass

def delete_db_server(module, result):
    pass


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    if module.params["state"] == "present":
        if module.params.get("db_uuid"):
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
