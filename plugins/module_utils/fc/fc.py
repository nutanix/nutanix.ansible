from __future__ import absolute_import, division, print_function

from ..entity import Entity

__metaclass__ = type


class FoundationCentral(Entity):
    __BASEURL__ = "/api/fc/v1"

    def __init__(self, module, resource_type):
        resource_type = self.__BASEURL__ + resource_type
        super(FoundationCentral, self).__init__(module, resource_type)
