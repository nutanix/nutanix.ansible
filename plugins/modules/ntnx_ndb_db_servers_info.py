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
version_added: 1.7.0
description: 'Get database server info'
options:
      server_name:
        description:
            - server name
        type: str
      server_id:
        description:
            - server id
        type: str
      server_ip:
        description:
            - server ip
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

from ..module_utils.ndb.nutanix_database import NutanixDatabase  # noqa: E402
from ..module_utils.ndb.db_servers import DBServers  # noqa: E402


def get_module_spec():

    module_args = dict(
        server_name=dict(type="str"),
        server_id=dict(type="str"),
        server_ip=dict(type="str"),
    )

    return module_args


def get_db_server(module, result):
    db_server = DBServers(module)
    if module.params.get("server_name"):
        db_name = module.params["server_name"]
        db_option = "{0}/{1}".format("name", db_name)
    elif module.params.get("server_ip"):
        db_ip = module.params["server_ip"]
        db_option = "{0}/{1}".format("ip", db_ip)
    else:
        db_option = "{0}".format(module.params["server_id"])

    resp = db_server.read(db_option, raise_error=False)

    result["response"] = resp


def get_db_servers(module, result):
    db_server = DBServers(module)

    resp = db_server.read()

    result["response"] = resp


def run_module():
    module = NutanixDatabase(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
        mutually_exclusive=[("server_name", "server_id", "server_ip")],
    )
    result = {"changed": False, "error": None, "response": None}
    if (
        module.params.get("server_name")
        or module.params.get("server_id")
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
