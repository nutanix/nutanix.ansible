# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ansible_collections.nutanix.ncp.plugins.module_utils.foundation.foundation import (
    Foundation,
)

__metaclass__ = type

import base64
import os
from copy import deepcopy

from ansible_collections.nutanix.ncp.plugins.module_utils.foundation.discover_nodes import (  # noqa: E402
    DiscoverNodes,
)
from ansible_collections.nutanix.ncp.plugins.module_utils.foundation.node_network_details import (  # noqa: E402
    NodeNetworkDetails,
)


class NodeDiscovery:
    def __init__(self, module):
       self.module = module

    def discover(self, include_configured=False, include_network_details=False, timeout=60): 
        nodes = DiscoverNodes(self.module)
        resp, status = nodes.discover(include_configured)
        if status["error"]:
                return resp, status
        if include_network_details:
            resp, status = self._add_network_details(resp, timeout)
            if status["error"]:
                return resp, status
        return {
            "blocks": resp
            }, status

    def _add_network_details(self, blocks, timeout):
        node_network_details = NodeNetworkDetails(self.module)
        ipv6_addresses = self._get_ipv6_address(blocks)
        resp, status = node_network_details.retrieve_network_info(ipv6_addresses, timeout)
        if status.get("error"):
               return resp,status
        node_network_info = self._create_network_details_dict(resp)
        for b in blocks:
            for n in b.get("nodes",[]):
                ipv6 = n.get("ipv6_address")
                node_info = node_network_info.get(ipv6,{})
                n.update(node_info)
        return blocks, status

    def _get_ipv6_address(self, blocks):
        ipv6_addresses = []
        for b in blocks:
            for n in b.get("nodes",[]):
                ipv6 = n.get("ipv6_address")
                if ipv6:
                    ipv6_addresses.append(ipv6)
        return ipv6_addresses

    def _create_network_details_dict(self, node_network_info):
        result = {}
        for n in node_network_info:
            ipv6 = n.get("ipv6_address")
            if ipv6:
                result[ipv6] = n
        return result
