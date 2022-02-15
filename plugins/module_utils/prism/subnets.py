# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .clusters import get_cluster_uuid
from .prism import Prism
from .virtual_switches import get_dvs_uuid
from .vpcs import get_vpc_uuid


class Subnet(Prism):
    def __init__(self, module):
        resource_type = "/subnets"
        super(Subnet, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "vlan_subnet": self._build_spec_vlan_subnet,
            "external_subnet": self._build_spec_external_subnet,
            "overlay_subnet": self._build_spec_overlay_subnet,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "subnet"},
                "spec": {
                    "name": "",
                    "resources": {"ip_config": {}, "subnet_type": None},
                },
            }
        )

    def _build_spec_name(self, payload, value):
        payload["spec"]["name"] = value
        return payload, None

    def _build_spec_vlan_subnet(self, payload, config):
        payload["spec"]["resources"]["subnet_type"] = "VLAN"
        payload["spec"]["resources"]["vlan_id"] = config["vlan_id"]
        payload["spec"]["resources"]["is_external"] = False

        dvs_uuid, error = get_dvs_uuid(config["virtual_switch"], self.module)
        if error:
            return None, error
        payload["spec"]["resources"]["virtual_switch_uuid"] = dvs_uuid
        cluster_uuid, error = get_cluster_uuid(config["cluster"], self.module)
        if error:
            return None, error
        payload["spec"]["cluster_reference"] = self._get_cluster_ref_spec(cluster_uuid)

        if "ipam" in config:
            payload["spec"]["resources"]["ip_config"] = self._get_ipam_spec(config)

        return payload, None

    def _build_spec_external_subnet(self, payload, config):
        payload["spec"]["resources"]["subnet_type"] = "VLAN"
        payload["spec"]["resources"]["vlan_id"] = config["vlan_id"]
        payload["spec"]["resources"]["is_external"] = True
        payload["spec"]["resources"]["enable_nat"] = config["enable_nat"]
        payload["spec"]["resources"]["ip_config"] = self._get_ipam_spec(config)
        cluster_uuid, error = get_cluster_uuid(config["cluster"], self.module)
        if error:
            return None, error
        payload["spec"]["cluster_reference"] = self._get_cluster_ref_spec(cluster_uuid)

        return payload, None

    def _build_spec_overlay_subnet(self, payload, config):
        payload["spec"]["resources"]["subnet_type"] = "OVERLAY"
        vpc_uuid, error = get_vpc_uuid(config["vpc"], self.module)
        if error:
            return None, error
        payload["spec"]["resources"]["vpc_reference"] = self._get_vpc_ref_spec(vpc_uuid)
        payload["spec"]["resources"]["ip_config"] = self._get_ipam_spec(config)

        return payload, None

    def _get_cluster_ref_spec(self, uuid):
        return deepcopy({"kind": "cluster", "uuid": uuid})

    def _get_vpc_ref_spec(self, uuid):
        return deepcopy({"kind": "vpc", "uuid": uuid})

    def _get_ipam_spec(self, config):
        ipam_spec = self._get_default_ipconfig_spec()
        ipam_config = config["ipam"]
        ipam_spec["subnet_ip"] = ipam_config["network_ip"]
        ipam_spec["prefix_length"] = ipam_config["network_prefix"]
        ipam_spec["default_gateway_ip"] = ipam_config["gateway_ip"]
        if "ip_pools" in ipam_config:
            pools = []
            for ip_pool in ipam_config["ip_pools"]:
                range = {"range": ip_pool["start_ip"] + " " + ip_pool["end_ip"]}
                pools.append(range)
            ipam_spec["pool_list"] = pools
        if "dhcp" in ipam_config:
            dhcp_spec = self._get_default_dhcp_spec()
            dhcp_config = ipam_config["dhcp"]
            if "dns_servers" in dhcp_config:
                dhcp_spec["domain_name_server_list"] = dhcp_config["dns_servers"]
            if "domain_search" in dhcp_config:
                dhcp_spec["domain_search_list"] = dhcp_config["domain_search"]
            if "domain_name" in dhcp_config:
                dhcp_spec["domain_name"] = dhcp_config["domain_name"]
            if "boot_file" in dhcp_config:
                dhcp_spec["boot_file_name"] = dhcp_config["boot_file"]
            if "tftp_server_ip" in dhcp_config:
                dhcp_spec["tftp_server_name"] = dhcp_config["tftp_server_ip"]
            if "dhcp_server_ip" in dhcp_config:
                ipam_spec["dhcp_server_address"] = {"ip": dhcp_config["dhcp_server_ip"]}

            ipam_spec["dhcp_options"] = dhcp_spec
        return ipam_spec

    def _get_default_ipconfig_spec(self):
        return deepcopy(
            {
                "subnet_ip": None,
                "prefix_length": None,
                "default_gateway_ip": None,
                "pool_list": [],
            }
        )

    def _get_default_dhcp_spec(self):
        return deepcopy(
            {
                "domain_name_server_list": [],
                "domain_search_list": [],
                "domain_name": "",
                "boot_file_name": "",
                "tftp_server_name": "",
            }
        )


# Helper functions


def get_subnet_uuid(config, module):
    if "name" in config or "subnet_name" in config:
        subnet = Subnet(module)
        name = config.get("name") or config.get("subnet_name")
        uuid = subnet.get_uuid(name)
        if not uuid:
            error = "Subnet {0} not found.".format(name)
            return None, error
    elif "uuid" in config or "subnet_uuid" in config:
        uuid = config.get("uuid") or config.get("subnet_uuid")
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        None, error

    return uuid, None
