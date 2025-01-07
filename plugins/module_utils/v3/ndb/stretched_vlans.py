# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .vlans import VLAN

__metaclass__ = type


class StretchedVLAN(VLAN):
    def __init__(self, module):
        super(StretchedVLAN, self).__init__(module)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "gateway": self._build_spec_gateway,
            "subnet_mask": self._build_spec_subnet_mask,
            "vlans": self._build_spec_vlans,
        }

    def get_spec(self, old_spec=None, params=None):
        return super().get_spec(old_spec=old_spec, params=params)

    def get_stretched_vlan(self, uuid=None):
        if uuid:
            endpoint = "stretched-vlan/{0}".format(uuid)
            resp = self.read(endpoint=endpoint)
            if not resp:
                return None, "stretched vlan with uuid {0} not found".format(uuid)
        else:
            return (
                None,
                "Please provide uuid for fetching stretched vlan details",
            )
        return resp, None

    def _get_default_spec(self):
        return deepcopy({"name": "", "type": "Static", "vlanIds": []})

    def get_default_update_spec(self, override_spec=None):
        spec = deepcopy(
            {
                "name": "",
                "type": "Static",
                "metadata": {"gateway": "", "subnetMask": ""},
                "vlanIds": [],
            }
        )
        if override_spec:
            for key in spec.keys():
                if override_spec.get(key):
                    spec[key] = deepcopy(override_spec[key])
            spec["vlanIds"] = [vlan["id"] for vlan in override_spec.get("vlans")]
        return spec

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, value):
        payload["description"] = value
        return payload, None

    def _build_spec_gateway(self, payload, gateway):
        payload["metadata"]["gateway"] = gateway
        return payload, None

    def _build_spec_subnet_mask(self, payload, subnet_mask):
        payload["metadata"]["subnetMask"] = subnet_mask
        return payload, None

    def _build_spec_vlans(self, payload, value):
        payload["vlanIds"] = value
        payload["type"] = "Static"
        return payload, None

    def create_stretched_vlan(self, data):
        endpoint = "stretched-vlan"
        return self.create(data=data, endpoint=endpoint)

    def update_stretched_vlan(self, data, uuid):
        endpoint = "stretched-vlan/{0}".format(uuid)
        return self.update(data=data, endpoint=endpoint)

    def delete_stretched_vlan(self, uuid):
        endpoint = "stretched-vlan/{0}".format(uuid)
        return self.delete(endpoint=endpoint)
