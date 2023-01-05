# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class Profile(NutanixDatabase):
    types = ["Database_Parameter", "Compute", "Network", "Software"]

    def __init__(self, module):
        resource_type = "/profiles"
        super(Profile, self).__init__(module, resource_type=resource_type)

    def get_profile_uuid(self, type, name):
        if type not in self.types:
            return None, "{0} is not a valid type. Allowed types are {1}".format(
                type, self.types
            )
        query = {"type": type, "name": name}
        resp = self.read(query=query)
        uuid = resp.get("id")
        return uuid

    def read(
        self,
        uuid=None,
        endpoint=None,
        query=None,
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        if uuid:
            if not query:
                query = {}
            query["id"] = uuid
        return super().read(
            uuid=None,
            endpoint=endpoint,
            query=query,
            raise_error=raise_error,
            no_response=no_response,
            timeout=timeout,
        )

    def get_profile_by_version(self, uuid, version_id="latest"):
        endpoint = "{0}/versions/{1}".format(uuid, version_id)
        resp = self.read(endpoint=endpoint)
        return resp

    def get_profiles(self, uuid=None, name=None, type=None):
        if name or uuid:
            query = {}
            if name:
                query["name"] = name
            else:
                query["id"] = uuid

            if type:
                query["type"] = type

            resp = self.read(query=query)
        elif type:
            query = {"type": type}
            resp = self.read(query=query)
            if not resp:
                return None, "Profiles with type {0} not found".format(type)
        else:
            return (
                None,
                "Please provide uuid, name or profile type for fetching profile details",
            )

        return resp, None
    
    def get_all_name_uuid_map(self, type=None):
        if type:
            query = {
                "type": type
            }

        name_uuid_map = {}
        resp = self.read(query=query)
        if not isinstance(resp, list):
            return None, "Invalid response type obtained from NDB server"
        
        for entity in resp:
            name_uuid_map[entity["name"]] = entity["id"]

        return name_uuid_map, None


# helper functions


def get_profile_uuid(module, type, config):
    uuid = ""
    if config.get("name"):
        profiles = Profile(module)
        uuid = profiles.get_profile_uuid(type, config["name"])
    elif config.get("uuid"):
        uuid = config["uuid"]
    else:
        error = "Profile config {0} doesn't have name or uuid key".format(config)
        return error, None
    return uuid, None
