# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ansible_collections.nutanix.ncp.plugins.module_utils.foundation.foundation import (
    Foundation,
)

__metaclass__ = type


class DiscoverNodes(Foundation):
    def __init__(self, module):
        resource_type = "/discover_nodes"
        super(DiscoverNodes, self).__init__(module, resource_type=resource_type)

    def discover(self, include_configured=False):
        resp = self.read()
        if not resp:
            return None
        blocks = []
        for block in resp:
            nodes = block.get("nodes", [])
            result_nodes = []
            for n in nodes:
                configured = n.get("configured")
                if include_configured or (type(configured) == bool and not configured):
                    result_nodes.append(n)
            if len(result_nodes) > 0:
                block["nodes"] = result_nodes
                blocks.append(block)
        return blocks
