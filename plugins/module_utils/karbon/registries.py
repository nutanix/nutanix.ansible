# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from ..prism.clusters import get_cluster_uuid
from ..prism.subnets import get_subnet_uuid
from .karbon import Karbon


class Registry(Karbon):
    kind = "registry"

    def __init__(self, module, resource_type="/v1-alpha.1/registries"):
        super(Registry, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "cert": self._build_spec_cert,
            "username": self._build_spec_username,
            "password": self._build_spec_password,
            "url": self._build_spec_url,
            "port": self._build_spec_port,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "name": "",
                "cert": "",
                "username": "",
                "password": "",
                "url": "",
                "port": 0,
            }
        )

    def _build_spec_name(self, payload, value):
        payload["name"] = value
        return payload, None

    def _build_spec_cert(self, payload, value):
        payload["cert"] = value
        return payload, None

    def _build_spec_username(self, payload, value):
        payload["username"] = value
        return payload, None

    def _build_spec_password(self, payload, value):
        payload["password"] = value
        return payload, None

    def _build_spec_url(self, payload, value):
        payload["url"] = value
        return payload, None

    def _build_spec_port(self, payload, value):
        payload["port"] = value
        return payload, None
