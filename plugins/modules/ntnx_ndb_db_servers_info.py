#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_db_servers_info
short_description: database server info module
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
            - db server vm ip
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

from ..module_utils.ndb.db_servers import DBServers  # noqa: E402
from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        server_ip=dict(type="str"),
    )

    return module_args


def get_db_server(module, result):
    db_server = DBServers(module)
    if module.params.get("uuid"):
        resp, err = db_server.get_db_server(uuid=module.params["uuid"])
    elif module.params.get("name"):
        resp, err = db_server.get_db_server(name=module.params["name"])
    else:
        resp, err = db_server.get_db_server(ip=module.params["server_ip"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching database server info", **result)

    result["response"] = resp


def get_db_servers(module, result):
    db_server = DBServers(module)

    resp = db_server.read()

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
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
