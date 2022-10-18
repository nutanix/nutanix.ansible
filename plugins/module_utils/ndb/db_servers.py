# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class DBServers(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/dbservers"
        super(DBServers, self).__init__(module, resource_type=resource_type)

    def get_uuid(
        self,
        value,
        key="name",
        data=None,
        entity_type=None,
        raise_error=True,
        no_response=False,
    ):
        query = {"value-type": key, "value": value}
        resp = self.read(query=query, raise_error=False)

        if not resp:
            return None, "DB server vm with name {0} not found.".format(value)
        elif isinstance(resp, dict) and resp.get("errorCode"):
            self.module.fail_json(
                msg="Failed fetching DB server VM",
                error=resp.get("message"),
                response=resp,
            )

        uuid = resp[0].get("id")
        return uuid, None

    def get_db_server(self, name=None, uuid=None, ip=None):
        resp = None
        if uuid:
            resp = self.read(uuid=uuid, raise_error=False)
        elif name or ip:
            key = "name" if name else "ip"
            val = name if name else ip
            query = {"value-type": key, "value": val}
            resp = self.read(query=query)
            if not resp:
                return None, "Database server with {0} {1} not found".format(key, val)
            resp = resp[0]
        else:
            return (
                None,
                "Please provide uuid, name or server IP for fetching database server details",
            )

        if isinstance(resp, dict) and resp.get("errorCode"):
            self.module.fail_json(
                msg="Failed fetching database server info",
                error=resp.get("message"),
                response=resp,
            )

        return resp, None


# Helper functions


def get_db_server_uuid(module, config):
    if "name" in config:
        db_servers = DBServers(module)
        name = config["name"]
        uuid, err = db_servers.get_uuid(name)
        if err:
            return None, err
    elif "uuid" in config:
        uuid = config["uuid"]
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        return None, error

    return uuid, None
