# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from .foundation import Foundation

__metaclass__ = type


class NodeNetworkDetails(Foundation):
    def __init__(self, module):
        resource_type = "/node_network_details"
        super(NodeNetworkDetails, self).__init__(module, resource_type=resource_type)

    def retrieve(self, nodes, timeout=60):
        nodes_query = {"nodes": list(map(lambda e: {"ipv6_address": e}, nodes))}
        if timeout:
            nodes_query["timeout"] = str(timeout)
        resp = self.create(data=nodes_query, timeout=timeout)

        nodes = resp.get("nodes", [])
        return nodes
