from __future__ import absolute_import, division, print_function

from ..entity import Entity

__metaclass__ = type


class NutanixDatabase(Entity):
    __BASEURL__ = "/era"
    api_version = "/v0.9"

    def __init__(self, module, resource_type, additional_headers=None):
        resource_type = self.__BASEURL__ + self.api_version + resource_type
        super(NutanixDatabase, self).__init__(
            module,
            resource_type,
            additional_headers=additional_headers,
        )

    def filters_map(self, except_keys=None):
        filters = self.module.params.get("filters")
        if filters:
            mapped_filters = {}
            for key, value in filters.items():
                if value is not None:
                    if not except_keys or key not in except_keys:
                        key = key.replace("_", "-")
                    mapped_filters.update({key: value})
