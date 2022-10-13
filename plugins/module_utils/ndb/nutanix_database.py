from __future__ import absolute_import, division, print_function
from sys import api_version

from ..entity import Entity

__metaclass__ = type


class NutanixDatabase(Entity):
    __BASEURL__ = "/era"
    api_version = "/v0.9"

    def __init__(self, module, resource_type, additional_headers=None):
        resource_type = self.__BASEURL__ + self.api_version + resource_type
        host_ip = module.params.get("ndb_host")
        credentials = {
            "username": module.params.get("ndb_username"),
            "password": module.params.get("ndb_password"),
        }
        super(NutanixDatabase, self).__init__(
            module,
            resource_type,
            host_ip,
            additional_headers=additional_headers,
            credentials=credentials,
        )
