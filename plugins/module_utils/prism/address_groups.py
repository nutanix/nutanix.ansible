# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

from .prism import Prism

__metaclass__ = type

class AddressGroup(Prism):
    def __init__(self, module):
        resource_type = "/address_groups"
        super(AddressGroup, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "subnet_details": self._build_spec_subnet_details
        }

    def get_uuid(self, value, key="name", raise_error=True, no_response=False):
        data = {"filter": "{0}=={1}".format(key, value), "length": 1}
        resp = self.list(data, raise_error=raise_error, no_response=no_response)
        entities = resp.get("entities") if resp else None
        if entities:
            for entity in entities:
                if entity["address_group"]["name"] == value:
                    return entity["uuid"]
        return None

    def _get_default_spec(self):
        return deepcopy(
            {
                "name": None,
                "ip_address_block_list": []
            }
        )

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["description"] = desc
        return payload, None

    def _build_spec_subnet_details(self, payload, subnet_details):
        ip_address_block_list = []
        for subnet in subnet_details:
            ip_address_block_list.append(self._get_ip_address_block(subnet["network_ip"], subnet["network_prefix"]))
        payload["ip_address_block_list"] = ip_address_block_list
        return payload, None

    def _get_ip_address_block(self, ip, prefix):
        spec = {
            "ip": ip,
            "prefix_length": prefix
        }
        return spec


# Helper functions


def get_address_uuid(config, module):
    if "name" in config:
        address_group = AddressGroup(module)
        name = config["name"]
        uuid = address_group.get_uuid(name)
        if not uuid:
            error = "Address {0} not found.".format(name)
            return None, error
    elif "uuid" in config:
        uuid = config["uuid"]
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        return None, error

    return uuid, None
