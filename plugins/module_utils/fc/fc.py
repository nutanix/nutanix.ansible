from __future__ import absolute_import, division, print_function

from ..entity import Entity

__metaclass__ = type


class FoundationCentral(Entity):
    __BASEURL__ = "/api/fc/v1"

    def __init__(self, module, resource_type):
        resource_type = self.__BASEURL__ + resource_type
        host_ip = module.params.get("nutanix_host")
        port = module.params.get("nutanix_port")
        credentials = {
            "username": module.params.get("nutanix_username"),
            "password": module.params.get("nutanix_password"),
        }
        super(FoundationCentral, self).__init__(
            module, resource_type, host_ip, port=port, credentials=credentials
        )
