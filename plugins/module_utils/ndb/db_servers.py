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
        elif resp.get("errorCode"):
            self.module.fail_json(
                msg="Failed fetching DB server VM",
                error=resp.get("message"),
                response=resp,
            )

        uuid = resp[0]["id"]
        return uuid, None


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
