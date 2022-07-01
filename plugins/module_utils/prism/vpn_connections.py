# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .prism import Prism


class VpnConnection(Prism):
    def __init__(self, module):
        resource_type = "/vpn_connections"
        super(VpnConnection, self).__init__(module, resource_type=resource_type)

# Helper functions


def get_vpn_connection_uuid(module, config):
    if "name" in config:
        vpn_obj = VpnConnection(module)
        name = config.get("name")
        uuid = vpn_obj.get_uuid(name)
        if not uuid:
            error = "VPN connection {0} not found.".format(name)
            return None, error
    elif "uuid" in config:
        uuid = config.get("uuid")
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        None, error

    return uuid, None
