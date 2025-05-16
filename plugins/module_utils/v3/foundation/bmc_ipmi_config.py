from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .foundation import Foundation

__metaclass__ = type


class BMC(Foundation):
    def __init__(self, module):
        resource_type = "/ipmi_config"
        super(BMC, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "ipmi_user": self._build_spec_ipmi_user,
            "ipmi_netmask": self._build_spec_ipmi_netmask,
            "blocks": self._build_spec_blocks,
            "ipmi_gateway": self._build_spec_ipmi_gateway,
            "ipmi_password": self._build_spec_ipmi_password,
        }

    def configure_ipmi(self, spec, timeout=120):
        return self.create(spec, timeout=timeout)

    def _get_default_spec(self):
        return deepcopy(
            {
                "ipmi_user": None,
                "ipmi_netmask": None,
                "blocks": None,
                "ipmi_gateway": None,
                "ipmi_password": None,
            }
        )

    def _build_spec_ipmi_user(self, payload, username):
        payload["ipmi_user"] = username
        return payload, None

    def _build_spec_ipmi_netmask(self, payload, netmask):
        payload["ipmi_netmask"] = netmask
        return payload, None

    def _build_spec_blocks(self, payload, blocks):
        payload["blocks"] = blocks
        return payload, None

    def _build_spec_ipmi_gateway(self, payload, gateway):
        payload["ipmi_gateway"] = gateway
        return payload, None

    def _build_spec_ipmi_password(self, payload, passwd):
        payload["ipmi_password"] = passwd
        return payload, None
