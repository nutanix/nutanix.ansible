from __future__ import absolute_import, division, print_function

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

    def queries_map(self, except_keys=None):
        queries = self.module.params.get("queries")
        if queries:
            mapped_queries = {}
            for key, value in queries.items():
                if value is not None:
                    if except_keys and key not in except_keys:
                        key = key.replace("_", "-")
                    mapped_queries.update({key: value})
            self.module.params["queries"] = mapped_queries
