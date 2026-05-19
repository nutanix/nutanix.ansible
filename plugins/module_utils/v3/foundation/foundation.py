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

    def _build_headers(self, module, additional_headers):
        """Foundation API is unauthenticated — no credentials required."""
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if additional_headers:
            headers.update(additional_headers)
        return headers
