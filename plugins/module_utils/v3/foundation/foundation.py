from __future__ import absolute_import, division, print_function

from ..entity import Entity

__metaclass__ = type


class Foundation(Entity):
    __BASEURL__ = "/foundation"

    def __init__(self, module, resource_type, additional_headers=None):
        resource_type = self.__BASEURL__ + resource_type
        super(Foundation, self).__init__(
            module, resource_type, scheme="http", additional_headers=additional_headers
        )
