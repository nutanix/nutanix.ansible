#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_tms_info
short_description: tm  info module
version_added: 1.8.0-beta.1
description: 'Get tm info'
options:
      name:
        description:
            - time machine name
        type: str
      uuid:
        description:
            - time machine id
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""

"""
RETURN = r"""

"""

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.time_machines import TimeMachine  # noqa: E402


def get_module_spec():

    queries_spec = dict(
        detailed=dict(type="bool"),
        load_clones=dict(type="bool"),
        load_databases=dict(type="bool"),
        clone_tms=dict(type="bool"),
        database_tms=dict(type="bool"),
        value=dict(type="str"),
        value_type=dict(
            type="str",
            choices=[
                "ip",
                "name",
            ]
        ),
        time_zone=dict(type="str"),
    )

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        queries=dict(
            type="dict",
            options=queries_spec,
        )
    )

    return module_args


def get_tm(module, result):
    tm = TimeMachine(module)
    tm.queries_map()

    uuid = module.params.get("uuid")
    name = module.params.get("name")
    query_params = module.params.get("queries")
    resp, err = tm.get_time_machine(uuid=uuid, name=name, query=query_params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching sla info", **result)
    result["response"] = resp


def get_tms(module, result):
    tm = TimeMachine(module)
    tm.queries_map()

    query_params = module.params.get("queries")

    resp = tm.read(query=query_params)

    result["response"] = resp


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_tm(module, result)
    else:
        get_tms(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
