# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .clusters import get_cluster_uuid
from .nutanix_database import NutanixDatabase

__metaclass__ = type


class VLAN(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/resources/networks"
        super(VLAN, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "vlan_type": self._build_spec_type,
            "ip_pool": self._build_spec_ip_pool,
            "gateway": self._build_spec_gateway,
            "subnet_mask": self._build_spec_subnet_mask,
            "primary_dns": self._build_spec_primary_dns,
            "secondary_dns": self._build_spec_secondary_dns,
            "dns_domain": self._build_spec_dns_domain,
        }

    def get_uuid(
        self,
        value,
        key="name",
        data=None,
        entity_type=None,
        raise_error=True,
        no_response=False,
    ):
        query = {key: value}
        resp = self.read(query=query, raise_error=False)
        if resp is None:
            return None, "vlan instance with name {0} not found.".format(value)
        uuid = resp.get("id")
        return uuid, None

    def get_vlan(self, name=None, uuid=None, detailed=True):
        default_query = {"detailed": detailed}
        if uuid:
            query = {"id": uuid}
            query.update(deepcopy(default_query))
            resp = self.read(query=query)
            if not resp:
                return None, "vlan with uuid {0} not found".format(uuid)
        elif name:
            query = {"name": name}
            query.update(deepcopy(default_query))
            resp = self.read(query=query)
            if not resp:
                return None, "vlan with name {0} not found".format(name)
        else:
            return (
                None,
                "Please provide either uuid or name for fetching vlan details",
            )

        return resp, None

    def _get_default_spec(self):
        return deepcopy(
            {
                "name": "",
                "type": "",
                "properties": [],
                "ipPools": [],
                "clusterId": "",
            }
        )

    def get_default_update_spec(self, override_spec=None):
        spec = deepcopy(
            {
                "name": "",
                "type": "",
                "properties": [],
                "clusterId": "",
            }
        )
        if override_spec:
            for key in spec.keys():
                if override_spec.get(key):
                    spec[key] = deepcopy(override_spec[key])

        return spec

    def get_default_delete_spec(self):
        return deepcopy(
            {
                "delete": False,
                "remove": False,
                "deleteTimeMachine": False,
                "deleteLogicalCluster": True,
            }
        )

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_type(self, payload, vlan_type):
        payload["type"] = vlan_type
        return payload, None

    def _build_spec_cluster(self, payload, param):
        uuid, err = get_cluster_uuid(param, self.module)
        if err:
            return None, err
        payload["clusterId"] = uuid
        return payload, None

    def _build_spec_ip_pool(self, payload, params):
        ip_pool = {"startIP": params["start_ip"], "endIP": params["end_ip"]}
        if payload.get("ipPools"):
            payload["ipPools"].append(ip_pool)
        else:
            payload["ipPools"] = []
            payload["ipPools"].append(ip_pool)
        return payload, None

    def _build_spec_gateway(self, payload, gateway):
        old_property = self.get_property_by_name("VLAN_GATEWAY", payload["properties"])
        if old_property:
            old_property["value"] = gateway
        else:
            payload["properties"].append({"name": "VLAN_GATEWAY", "value": gateway})
        return payload, None

    def _build_spec_subnet_mask(self, payload, subnet_mask):
        old_property = self.get_property_by_name("VLAN_SUBNET_MASK", payload["properties"])
        if old_property:
            old_property["value"] = subnet_mask
        else:
            payload["properties"].append({"name": "VLAN_SUBNET_MASK", "value": subnet_mask})
        return payload, None

    def _build_spec_primary_dns(self, payload, primary_dns):
        old_property = self.get_property_by_name("VLAN_PRIMARY_DNS", payload["properties"])
        if old_property:
            old_property["value"] = primary_dns
        else:
            payload["properties"].append({"name": "VLAN_PRIMARY_DNS", "value": primary_dns})
        return payload, None

    def _build_spec_secondary_dns(self, payload, secondary_dns):
        old_property = self.get_property_by_name("VLAN_SECONDARY_DNS", payload["properties"])
        if old_property:
            old_property["value"] = secondary_dns
        else:
            payload["properties"].append(
                {"name": "VLAN_SECONDARY_DNS", "value": secondary_dns}
            )
        return payload, None

    def _build_spec_dns_domain(self, payload, dns_domain):
        old_property = self.get_property_by_name("VLAN_DNS_DOMAIN", payload["properties"])
        if old_property:
            old_property["value"] = dns_domain
            raise ValueError(payload["properties"], old_property, old_property in payload["properties"])
        else:
            payload["properties"].append({"name": "VLAN_DNS_DOMAIN", "value": dns_domain})
        return payload, None

    def get_property_by_name(self, name, properties):
        for property in properties:
            if property["name"] == name:
                return property
        return None
