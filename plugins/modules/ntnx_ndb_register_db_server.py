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




def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    postgres = dict(
        listener_port = dict(type="str", default="5432", required=False),
        software_path = dict(type="str", required=False)
    )
    module_args = dict(
        ip = dict(type="str", required=False),
        desc = dict(type="str", required=False),
        reset_desc_in_ntnx_cluster = dict(type="bool", default=False, required=False),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        postgres = dict(type="dict", options=postgres, required=False),
        password=dict(type="str", required=False),
        private_ssh_key = dict(type="str", required=False),
        time_zone = dict(type="str", default="Asia/Calcutta", required=False),
        working_directory = dict(type="str", default="/tmp", required=False),
    )
    return module_args

def register_db_server(module, result):
    pass


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    register_db_server(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
