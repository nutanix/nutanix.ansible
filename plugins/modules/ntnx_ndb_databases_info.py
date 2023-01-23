#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_databases_info
short_description: database  info module
version_added: 1.8.0-beta.1
description: 'Get database info'
options:
      name:
        description:
            - database name
        type: str
      uuid:
        description:
            - database id
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

from ..module_utils.ndb.databases import Database  # noqa: E402
from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402


def get_module_spec():

    queries_spec = dict(
        detailed=dict(type="bool"),
        load_dbserver_cluster=dict(type="bool"),
        order_by_dbserver_cluster=dict(type="bool"),
        order_by_dbserver_logical_cluster=dict(type="bool"),
        value=dict(type="str"),
        value_type=dict(
            type="str",
            choices=[
                "ip",
                "name",
                "database-name",
            ]
        ),
        time_zone=dict(type="str"),
    )
    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
    )

    return module_args


def get_database(module, result):
    database = Database(module)
    database.queries_map()
    query_params = module.params.get("queries")

    if module.params.get("name"):
        name = module.params["name"]
        resp, err = database.get_database(name=name, query=query_params)
    else:
        uuid = module.params["uuid"]
        resp, err = database.get_database(uuid=uuid, query=query_params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching database info", **result)
    result["response"] = resp


def get_databases(module, result):
    database = Database(module)
    database.queries_map()
    query_params = module.params.get("queries")

    resp = database.read(query=query_params)

    result["response"] = resp


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_database(module, result)
    else:
        get_databases(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
