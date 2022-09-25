from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..entity import Entity


class Era(Entity):
    __BASEURL__ = "/era"

    def __init__(self, module, resource_type, additional_headers=None):
        resource_type = self.__BASEURL__ + resource_type
        super(Era, self).__init__(
            module, resource_type, additional_headers=additional_headers
        )
