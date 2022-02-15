# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from copy import deepcopy

from .prism import Prism
from .vpcs import get_vpc_uuid


class Pbr(Prism):
    def __init__(self, module):
        resource_type = "/routing_policies"
        super(Pbr, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "priority": self._build_spec_priority,
            # "pbr_uuid": self.build_spec_pbr_uuid,
            "vpc": self._build_spec_vpc,
            "source": self._build_spec_source,
            "destination": self._build_spec_destination,
            "protocol": self._build_spec_protocol,
            "action": self._build_spec_action
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "routing_policy"},
                "spec": {
                    "resources": {
                    },
                },
            }
        )

    def _build_spec_priority(self, payload, config):
        payload["spec"]["resources"]["priority"] = config
        payload["spec"]["name"] = "Policy with priority{0}".format(config)

        return payload, None

    def _build_spec_vpc(self, payload, config):
        uuid, error = get_vpc_uuid(config, self.module)
        if error:
            return None, error
        payload["spec"]["resources"]["vpc_reference"] = self._get_vpc_ref(uuid)
        return payload, None

    def _get_vpc_ref(self, uuid):
        return deepcopy({"kind": "vpc", "uuid": uuid})

    def _build_spec_source(self, payload, config):
        source = {}
        if config.get("any"):
            source["address_type"] = "ALL"
        elif config.get("external"):
            source["address_type"] = "INTERNET"
        elif config.get("network"):
            source["ip_subnet"] = {"ip": config["network"].get("ip"),
                                   "prefix_length": config["network"].get("prefix")}

        payload["spec"]["resources"]["source"] = source

        return payload, None

    def _build_spec_destination(self, payload, config):
        destination = {}
        if config.get("any"):
            destination["address_type"] = "ALL"
        elif config.get("external"):
            destination["address_type"] = "INTERNET"
        elif config.get("network"):
            destination["ip_subnet"] = {"ip": config["network"].get("ip"),
                                        "prefix_length": config["network"].get("prefix")}

        payload["spec"]["resources"]["destination"] = destination

        return payload, None

    def _build_spec_protocol(self, payload, config):
        protocol_type = None
        protocol_parameters = {}
        if config.get("tcp"):
            protocol_type = "TCP"
            src_port_range_list = []
            if "*" not in config["tcp"]["src"]:
                for port in config["tcp"]["src"]:
                    port = port.split("-")
                    src_port_range_list.append({"start_port": int(port[0]), "end_port": int(port[-1])})
            dest_port_range_list = []
            if "*" not in config["tcp"]["dst"]:
                for port in config["tcp"]["dst"]:
                    port = port.split("-")
                    dest_port_range_list.append({"start_port": int(port[0]), "end_port": int(port[-1])})
            if src_port_range_list:
                protocol_parameters["tcp"]["source_port_range_list"] = src_port_range_list
            if dest_port_range_list:
                protocol_parameters["tcp"]["destination_port_range_list"] = dest_port_range_list

        elif config.get("udp"):
            protocol_type = "UDP"
            src_port_range_list = []
            if "*" not in config["udp"]["src"]:
                for port in config["udp"]["src"]:
                    port = port.split("-")
                    src_port_range_list.append({"start_port": int(port[0]), "end_port": int(port[-1])})
            dest_port_range_list = []
            if "*" not in config["udp"]["dst"]:
                for port in config["udp"]["dst"]:
                    port = port.split("-")
                    dest_port_range_list.append({"start_port": int(port[0]), "end_port": int(port[-1])})
            if src_port_range_list:
                protocol_parameters["udp"]["source_port_range_list"] = src_port_range_list
            if dest_port_range_list:
                protocol_parameters["udp"]["destination_port_range_list"] = dest_port_range_list

        elif config.get("icmp"):
            protocol_type = "ICMP"
            if config["icmp"].get("code"):
                protocol_parameters["icmp"]["icmp_code"] = config["icmp"]["code"]
                if config["icmp"].get("type"):
                    protocol_parameters["icmp"]["icmp_type"] = config["icmp"]["type"]

        elif config.get("number"):
            protocol_type = "PROTOCOL_NUMBER"
            protocol_parameters["protocol_number"] = config["number"]

        elif config.get("any"):
            protocol_type = "ALL"

        payload["spec"]["resources"]["protocol_type"] = protocol_type
        if protocol_parameters:
            payload["spec"]["resources"]["protocol_parameters"] = protocol_parameters

        return payload, None

    def _build_spec_action(self, payload, config):
        action = {}

        if config.get("allow"):
            action["action"] = "PERMIT"
        if config.get("deny"):
            action["action"] = "DENY"  # TODO check
        if config.get("reroute"):
            action["action"] = "REROUTE"
            action["service_ip_list"] = [config.get("reroute")]

        payload["spec"]["resources"]["action"] = action

        return payload, None
