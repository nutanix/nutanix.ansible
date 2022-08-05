from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..entity import Entity


class Karbon(Entity):
    __BASEURL__ = "/karbon/v1/k8s"

    def __init__(self, module, resource_type, additional_headers=None):
        resource_type = self.__BASEURL__ + resource_type
        super(Karbon, self).__init__(
            module, resource_type, additional_headers=additional_headers
        )
