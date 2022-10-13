from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..entity import Entity


class Prism(Entity):
    __BASEURL__ = "/api/nutanix/v3"

    def __init__(self, module, resource_type, additional_headers=None):
        resource_type = self.__BASEURL__ + resource_type
        host_ip = module.params.get("nutanix_host")
        port = module.params.get("nutanix_port")
        credentials = {
            "username": module.params.get("nutanix_username"),
            "password": module.params.get("nutanix_password"),
        }
        super(Prism, self).__init__(
            module,
            resource_type,
            host_ip,
            additional_headers=additional_headers,
            port=port,
            credentials=credentials,
        )
