# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .prism import Prism


class Users(Prism):
    def __init__(self, module):
        resource_type = "/users"
        super(Users, self).__init__(module, resource_type=resource_type)

    def get_uuid(self, value, key="username", raise_error=True, no_response=False):
        data = {"filter": "{0}=={1}".format(key, value), "length": 1}
        resp = self.list(data, raise_error=raise_error, no_response=no_response)
        entities = resp.get("entities") if resp else None
        if entities:
            for entity in entities:
                if entity["status"]["name"] == value:
                    return entity["metadata"]["uuid"]
        return None


def get_user_uuid(config, module):
    if "name" in config:
        users = Users(module)
        name = config["name"]
        uuid = users.get_uuid(name)
        if not uuid:

            error = "User {0} not found.".format(name)
            return None, error

    elif "uuid" in config:
        uuid = config["uuid"]

    return uuid
