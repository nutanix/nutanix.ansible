# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

__metaclass__ = type


from ..nutanix_database import NutanixDatabase

class Profile(NutanixDatabase):
    types = ["Database_Parameter", "Compute", "Network", "Software"]
    _type = None

    def __init__(self, module):
        resource_type = "/profiles"
        super(Profile, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self.build_spec_name,
            "desc": self.build_spec_desc,
            "database_type": self.build_spec_database_type
        }

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

    def create_version(self, profile_uuid, data):
        endpoint = "versions"
        resp = self.update(uuid=profile_uuid, endpoint=endpoint, data=data, method="POST")
        return resp

    def delete_version(self, profile_uuid, version_uuid):
        endpoint = "versions/{0}".format(version_uuid)
        resp = self.delete(uuid=profile_uuid, endpoint=endpoint, data={})
        return resp

    def update_version(self, profile_uuid, version_uuid, data):
        endpoint = "versions/{0}".format(version_uuid)
        resp = self.update(uuid=profile_uuid, endpoint=endpoint, data=data)
        return resp

    def get_profile_by_version(self, uuid, version_uuid="latest"):
        endpoint = "{0}/versions/{1}".format(uuid, version_uuid)
        resp = self.read(endpoint=endpoint)
        return resp

    def get_profiles(self, uuid=None, name=None, type=None):

        if not type:
            type=self._type
        
        query = {}
        if name:
            query["name"] = name
        else:
            query["id"] = uuid

        if type:
            query["type"] = type

        resp = self.read(query=query)
        return resp

    def get_all_name_uuid_map(self):
        if self._type:
            query = {"type": self._type}

        name_uuid_map = {}
        resp = self.read(query=query)
        if not isinstance(resp, list):
            return None, "Invalid response type obtained from NDB server"

        for entity in resp:
            name_uuid_map[entity["name"]] = entity["id"]

        return name_uuid_map, None

    def _get_default_spec(self):
        return deepcopy(
            {
                "type": "",
                "systemProfile": False,
                "properties": [],
                "name": "",
                "description": "",
            }
        )

    def get_default_update_spec(self, override_spec=None):
        spec = {
            "name": "",
            "description": ""
        }
        for key in spec:
            if key in override_spec:
                spec[key] = override_spec[key]

        return spec

    def get_default_version_update_spec(self, override_spec=None):
        spec = {"name": "", "description": "", "published": None, "properties": [], "propertiesMap": {}}

        for key in spec:
            if key in override_spec:
                spec[key] = override_spec[key]

        return spec

    def get_create_profile_spec(self, old_spec=None, params=None, **kwargs):
        payload, err = super().get_spec(old_spec=old_spec, params=params, **kwargs)
        if err:
            return None, err

        payload["type"] = self._type
        return payload, None

    def get_update_profile_spec(self, old_spec=None, params=None, **kwargs):
        return super().get_spec(old_spec=old_spec, params=params, **kwargs)

    def get_create_version_spec(self, old_spec=None, params=None, **kwargs):
        """
        Implement this method to support profile version create
        """
        return old_spec, None

    def get_update_version_spec(self, old_spec=None, params=None, **kwargs):
        """
        Implement this method to support profile version update
        """
        return old_spec, None

    def get_delete_version_spec(self, old_spec=None, params=None, **kwargs):
        """
        Implement this method to support profile version delete
        """
        return old_spec, None
    
    def get_property_spec(self, name, value):
        return deepcopy({"name": name, "value": value})

    # common builders
    def build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None
    
    def build_spec_desc(self, payload, desc):
        payload["description"] = desc
        return payload, None

    def build_spec_database_type(self, payload, type):
        if self._type!="compute":
            payload["engineType"] = type + "_database"
        return payload, None 
    
    def build_spec_status(self, payload):
        if self.module.params.get("publish") is not None:
            payload["published"] = self.module.params.get("publish")
        return payload, None


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
