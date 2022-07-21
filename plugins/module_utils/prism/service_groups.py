# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism


class ServiceGroup(Prism):
    def __init__(self, module):
        resource_type = "/service_groups"
        super(ServiceGroup, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "service_details": self._build_spec_service_details,
        }

    def get_uuid(self, value, key="name", raise_error=True, no_response=False):
        data = {"filter": "{0}=={1}".format(key, value)}
        resp = self.list(data, raise_error=raise_error, no_response=no_response)
        entities = resp.get("entities") if resp else None
        if entities:
            for entity in entities:
                if entity["service_group"]["name"] == value:
                    return entity["uuid"]
        return None

    def _get_default_spec(self):
        return deepcopy(
            {
                "name": None,
                "service_list": [],
            }
        )

    def _build_spec_name(self, payload, value):
        payload["name"] = value
        return payload, None

    def _build_spec_desc(self, payload, value):
        payload["description"] = value
        return payload, None

    def _build_spec_service_details(self, payload, config):
        service_list = []

        if config.get("tcp"):
            service = {}
            service["protocol"] = "TCP"
            port_range_list = self._generate_port_range_list(config["tcp"])
            service["tcp_port_range_list"] = port_range_list
            service_list.append(service)

        if config.get("udp"):
            service = {}
            service["protocol"] = "UDP"
            port_range_list = self._generate_port_range_list(config["udp"])
            service["udp_port_range_list"] = port_range_list
            service_list.append(service)

        if config.get("icmp"):
            service = {}
            service["protocol"] = "ICMP"
            service["icmp_type_code_list"] = config["icmp"]
            service_list.append(service)
        elif config.get("any_icmp"):
            service = {}
            service["protocol"] = "ICMP"
            service["icmp_type_code_list"] = []
            service_list.append(service)

        payload["service_list"] = service_list

        return payload, None

    @staticmethod
    def _generate_port_range_list(config):
        port_range_list = []
        if "*" not in config:
            for port in config:
                port = port.split("-")
                port_range_list.append(
                    {"start_port": int(port[0]), "end_port": int(port[-1])}
                )
        else:
            port_range_list.append({"start_port": 0, "end_port": 65535})
        return port_range_list


# Helper functions


def get_service_uuid(config, module):
    if "name" in config:
        service_group = ServiceGroup(module)
        name = config["name"]
        uuid = service_group.get_uuid(name)
        if not uuid:
            error = "Service {0} not found.".format(name)
            return None, error
    elif "uuid" in config:
        uuid = config["uuid"]
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        return None, error

    return uuid, None
