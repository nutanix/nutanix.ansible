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
            "desc": self._build_spec_desc,
            "vlan_type": self._build_spec_type,
            "ip_pools": self._build_spec_ip_pools,
            "gateway": self._build_spec_gateway,
            "subnet_mask": self._build_spec_subnet_mask,
            "primary_dns": self._build_spec_primary_dns,
            "secondary_dns": self._build_spec_secondary_dns,
            "dns_domain": self._build_spec_dns_domain,
            "cluster": self._build_spec_cluster,
        }

    def get_spec(self, old_spec=None, params=None):
        err = self._validate_module_params(old_spec)
        if err:
            return None, err
        return super().get_spec(old_spec=old_spec, params=params)

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

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, value):
        payload["description"] = value
        return payload, None

    def _build_spec_type(self, payload, vlan_type):
        payload["type"] = vlan_type
        return payload, None

    def _build_spec_cluster(self, payload, param):
        uuid, err = get_cluster_uuid(config=param, module=self.module)
        if err:
            return None, err
        payload["clusterId"] = uuid
        return payload, None

    def _build_spec_ip_pools(self, payload, ip_pools):
        ip_pools_spec = []
        for ip_pool in ip_pools:
            start_ip = ip_pool["start_ip"]
            end_ip = ip_pool.get("end_ip") or ip_pool["start_ip"]
            ip_pool = {"startIP": start_ip, "endIP": end_ip}
            ip_pools_spec.append(ip_pool)
        payload["ipPools"] = ip_pools_spec
        return payload, None

    def _build_spec_remove_ip_pools(self, ip_pools):
        payload = {"ipPools": []}
        for ip_pool_uuid in ip_pools:
            ip_pool = {"id": ip_pool_uuid}
            payload["ipPools"].append(ip_pool)
        return payload

    def _build_spec_gateway(self, payload, gateway):
        old_property = self._get_property_by_name(
            "VLAN_GATEWAY", payload["properties"]
        )
        if old_property:
            old_property["value"] = gateway
        else:
            payload["properties"].append({"name": "VLAN_GATEWAY", "value": gateway})
        return payload, None

    def _build_spec_subnet_mask(self, payload, subnet_mask):
        old_property = self._get_property_by_name(
            "VLAN_SUBNET_MASK", payload["properties"]
        )
        if old_property:
            old_property["value"] = subnet_mask
        else:
            payload["properties"].append(
                {"name": "VLAN_SUBNET_MASK", "value": subnet_mask}
            )
        return payload, None

    def _build_spec_primary_dns(self, payload, primary_dns):
        old_property = self._get_property_by_name(
            "VLAN_PRIMARY_DNS", payload["properties"]
        )
        if old_property:
            old_property["value"] = primary_dns
        else:
            payload["properties"].append(
                {"name": "VLAN_PRIMARY_DNS", "value": primary_dns}
            )
        return payload, None

    def _build_spec_secondary_dns(self, payload, secondary_dns):
        old_property = self._get_property_by_name(
            "VLAN_SECONDARY_DNS", payload["properties"]
        )
        if old_property:
            old_property["value"] = secondary_dns
        else:
            payload["properties"].append(
                {"name": "VLAN_SECONDARY_DNS", "value": secondary_dns}
            )
        return payload, None

    def _build_spec_dns_domain(self, payload, dns_domain):
        old_property = self._get_property_by_name(
            "VLAN_DNS_DOMAIN", payload["properties"]
        )
        if old_property:
            old_property["value"] = dns_domain
        else:
            payload["properties"].append(
                {"name": "VLAN_DNS_DOMAIN", "value": dns_domain}
            )
        return payload, None

    def _validate_module_params(self, payload=None):
        updated_vlan_type = self.module.params.get("vlan_type")
        old_vlan_type = payload.get("type") if payload else None
        vlan_type = updated_vlan_type or old_vlan_type
        if vlan_type == "DHCP":
            for item in [
                "gateway",
                "subnet_mask",
                "primary_dns",
                "secondary_dns",
                "dns_domain",
                "ip_pools",
            ]:
                if item in self.module.params:
                    err = "{0} cannot be provided if vlan_type is DHCP".format(item)
                    return err
        if updated_vlan_type == "Static" and updated_vlan_type != old_vlan_type:
            for item in ["gateway", "subnet_mask", "primary_dns"]:
                if item not in self.module.params:
                    err = "{0} is required if vlan_type is Static".format(item)
                    return err
        return None

    def _get_property_by_name(self, name, properties):
        for property in properties:
            if property["name"] == name:
                return property
        return None

    def add_ip_pools(self, vlan_uuid, ip_pools, old_spec=None):
        vlan_type = self.module.params.get("vlan_type") or old_spec.get("type", None)
        if vlan_type == "DHCP":
            err = "ip_pools cannot be provided if vlan_type is DHCP"
            return None, err

        spec, err = self._build_spec_ip_pools({}, ip_pools)
        if err:
            return None, err
        endpoint = "ip-pool"
        resp = self.update(
            uuid=vlan_uuid,
            data=spec,
            endpoint=endpoint,
            method="POST",
            raise_error=False,
        )
        if resp and resp.get("errorCode"):
            err = resp.get("message")
            return None, err
        return resp, None

    def remove_ip_pools(self, vlan_uuid, ip_pools):
        spec = self._build_spec_remove_ip_pools(ip_pools)
        endpoint = "ip-pool"
        return self.delete(uuid=vlan_uuid, data=spec, endpoint=endpoint)
