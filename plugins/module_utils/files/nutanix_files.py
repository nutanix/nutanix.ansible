from __future__ import absolute_import, division, print_function

from ..entity import Entity

__metaclass__ = type


class NutanixFiles(Entity):
    __BASEURL__ = "/api/files"
    api_version = "/v4.0.a2"

    def __init__(self, module, resource_type, api_version=None, additional_headers=None):
        if api_version:
            self.api_version = api_version
        resource_type = self.__BASEURL__ + self.api_version + resource_type
        super(NutanixFiles, self).__init__(
            module,
            resource_type,
            additional_headers=additional_headers,
        )
