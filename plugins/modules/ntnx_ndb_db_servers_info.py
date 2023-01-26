#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_db_servers_info
short_description: database server  info module
version_added: 1.8.0-beta.1
description: 'Get database server info'
options:
      name:
        description:
            - server name
        type: str
      uuid:
        description:
            - server id
        type: str
      server_ip:
        description:
            - server ip
        type: str
      filters:
        description:
            - write
        type: dict
        suboptions:
            detailed:
                description:
                    - write
                type: bool
            load_clones:
                description:
                    - write
                type: bool
            load_databases:
                description:
                    - write
                type: bool
            load_dbserver_cluster:
                description:
                    - write
                type: bool
            load_metrics:
                description:
                    - write
                type: bool
            curator:
                description:
                    - write
                type: bool
            value:
                description:
                    - write
                type: str
            value_type:
                description:
                    - write
                type: str
                choices: ["ip","name","vm-cluster-name","vm-cluster-uuid", "dbserver-cluster-id","nx-cluster-id", "fqdn",]
            time_zone:
                description:
                    - write
                type: str
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
from ..module_utils.ndb.db_servers import DBServers  # noqa: E402


def get_module_spec():

    filters_spec = dict(
        detailed=dict(type="bool"),
        load_clones=dict(type="bool"),
        load_databases=dict(type="bool"),
        load_dbserver_cluster=dict(type="bool"),
        load_metrics=dict(type="bool"),
        curator=dict(type="bool"),
        value=dict(type="str"),
        value_type=dict(
            type="str",
            choices=[
                "ip",
                "name",
                "vm-cluster-name",
                "vm-cluster-uuid",
                "dbserver-cluster-id",
                "nx-cluster-id",
                "fqdn",
            ],
        ),
        time_zone=dict(type="str"),
    )

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        server_ip=dict(type="str"),
        filters=dict(
            type="dict",
            options=filters_spec,
        ),
    )

    return module_args


def get_db_server(module, result):
    db_server = DBServers(module)
    db_server.filters_map()
    query_params = module.params.get("filters")

    if module.params.get("uuid"):
        resp, err = db_server.get_db_server(
            uuid=module.params["uuid"], query=query_params
        )
    elif module.params.get("name"):
        resp, err = db_server.get_db_server(
            name=module.params["name"], query=query_params
        )
    else:
        resp, err = db_server.get_db_server(
            ip=module.params["server_ip"], query=query_params
        )

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching database server info", **result)

    result["response"] = resp


def get_db_servers(module, result):
    db_server = DBServers(module)
    db_server.filters_map()
    query_params = module.params.get("filters")

    resp = db_server.read(query=query_params)

    result["response"] = resp


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid", "server_ip")],
    )
    result = {"changed": False, "error": None, "response": None}
    if (
        module.params.get("name")
        or module.params.get("uuid")
        or module.params.get("server_ip")
    ):
        get_db_server(module, result)
    else:
        get_db_servers(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
