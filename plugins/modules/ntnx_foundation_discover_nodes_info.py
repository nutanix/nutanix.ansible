#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ..module_utils.foundation.base_module import FoundationBaseModule
from ..module_utils.foundation.node_discovery import NodeDiscovery
from ..module_utils.utils import remove_param_with_none_value

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_discover_nodes_info
short_description: Nutanix module which returns nodes discovered by Foundation
version_added: 1.1.0
description: 'Discover nodes eligible for Foundation'
options:
  nutanix_host:
    description:
      - Foundation VM hostname or IP address
    type: str
    required: true
  nutanix_port:
    description:
      - PC port
    type: str
    default: 8000
    required: false
  include_configured:
    description: Shows all discovered nodes, including configured nodes
    type: bool
    required: false
    default: false
  include_network_details:
    description: Detects node network configuration
    type: bool
    required: false
    default: false
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
"""

EXAMPLES = r"""
  - name: Discover nodes
    ntnx_foundation_discover_nodes_info:
      nutanix_host: "{{ ip }}"

  - name: Discover all nodes
    ntnx_foundation_discover_nodes_info:
      nutanix_host: "{{ ip }}"
      include_configured: true
  - name: Discover nodes and include network info
    ntnx_foundation_discover_nodes_info:
      nutanix_host: "{{ ip }}"
      include_network_details: true
"""

RETURN = r"""
blocks:
  description: Discovered blocks/nodes by Foundation
  returned: always
  type: list
  sample: [
    {
      "foundation_version": "<foundation_version>",
      "ipmi_mac": null,
      "ipv6_address": "<ipv6_address>",
      "node_uuid": "<node_uuid>",
      "node_serial": "",
      "current_network_interface": "eth0",
      "node_position": "A",
      "hypervisor": "<hypervisor>",
      "svm_ip": "<svm_ip>",
      "nos_version": "a.a.a",
      "cluster_id": "",
      "current_cvm_vlan_tag": null,
      "hypervisor_version": "<hypervisor_version>",
      "attributes": {},
      "model": "YY-XXXX",
      "configured": true
    },
  ]
"""


def get_module_spec():
    module_args = dict(
        include_configured=dict(type="bool", required=False, default=False),
        include_network_details=dict(type="bool", required=False, default=False),
    )

    return module_args


def discover_nodes(module, result):
    include_configured = module.params["include_configured"]
    include_network_details = module.params.get("include_network_details")
    timeout = module.params.get("timeout")
    node_discovery = NodeDiscovery(module)
    resp, err = node_discovery.discover(
        include_configured, include_network_details, timeout=timeout
    )
    if err:
        result["error"] = err
        module.fail_json(msg="Failed discover nodes via foundation", **result)
    result["blocks"] = resp["blocks"]


def run_module():
    module = FoundationBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {}
    discover_nodes(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
