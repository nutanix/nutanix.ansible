# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from .discover_nodes import DiscoverNodes
from .node_network_details import NodeNetworkDetails

__metaclass__ = type


class NodeDiscovery:

    discovered_nodes = None

    def __init__(self, module):
        self.module = module

    def discover(
        self,
        include_configured=False,
        include_network_details=False,
        new_discovery=False,
        timeout=60,
    ):

        if self.discovered_nodes and not new_discovery:
            return self.discovered_nodes, None

        nodes = DiscoverNodes(self.module)
        blocks = nodes.discover(include_configured)
        if not blocks:
            error = "Failed to get blocks from node discovery"
            return None, error
        if include_network_details:
            blocks, error = self._add_network_details(blocks, timeout)
            if not blocks:
                return None, error

        # cache data for multiple calls
        self.discovered_nodes = {"blocks": blocks}
        return self.discovered_nodes, None

    def _add_network_details(self, blocks, timeout):
        ipv6_addresses = self._get_ipv6_address(blocks)
        node_network_details = NodeNetworkDetails(self.module)
        nodes = node_network_details.retrieve(ipv6_addresses, timeout)
        if not nodes:
            error = "Failed to retrieve node network details"
            return None, error
        node_network_spec = self._get_node_network_spec(nodes)
        for block in blocks:
            for node in block.get("nodes", []):
                ipv6 = node.get("ipv6_address")
                node_info = node_network_spec.get(ipv6, {})
                node.update(node_info)
        return blocks, None

    def _get_ipv6_address(self, blocks):
        ipv6_addresses = []
        for block in blocks:
            for node in block.get("nodes", []):
                ipv6 = node.get("ipv6_address")
                if ipv6:
                    ipv6_addresses.append(ipv6)
        return ipv6_addresses

    def _get_node_network_spec(self, nodes):
        spec = {}
        for node in nodes:
            ipv6 = node.get("ipv6_address")
            if ipv6:
                spec[ipv6] = node
        return spec
