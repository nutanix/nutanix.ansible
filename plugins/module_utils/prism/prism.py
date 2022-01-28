from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..entity import Entity


class Prism(Entity):
    __BASEURL__ = "/api/nutanix/v3"

    def __init__(self, module, resource_type):
        resource_type = self.__BASEURL__ + resource_type
        super(Prism, self).__init__(module, resource_type)
