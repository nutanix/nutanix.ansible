#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ..module_utils.foundation.base_module import FoundationBaseModule
from ..module_utils.foundation.node_network_details import NodeNetworkDetails
from ..module_utils.utils import remove_param_with_none_value

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_node_network_info
short_description: Nutanix module which returns node network information discovered by Foundation
version_added: 1.1.0
description: 'Discover nodes network information via Foundation'
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
  nodes:
    description: IPv6 addresses for nodes that require network discovery
    type: list
    required: true
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
"""

EXAMPLES = r"""
  - name: Get node network info
    ntnx_foundation_node_network_info:
      nutanix_host: "{{ ip }}"
      nodes:
       - node_1_ipv6
       - node_2_ipv6
       - node_3_ipv6


"""

RETURN = r"""
nodes:
  description: Discovered network information by Foundation
  returned: always
  type: list
  sample:
    [
      {
        "cvm_gateway": "192.168.0.1",
        "ipmi_netmask": "192.168.0.1",
        "ipv6_address": "string",
        "cvm_vlan_id": "string",
        "hypervisor_hostname": "string",
        "hypervisor_netmask": "192.168.0.1",
        "cvm_netmask": "192.168.0.1",
        "ipmi_ip": "192.168.0.1",
        "hypervisor_gateway": "192.168.0.1",
        "error": "string",
        "cvm_ip": "192.168.0.1",
        "hypervisor_ip": "192.168.0.1",
        "ipmi_gateway": "192.168.0.1"
      }
    ]
"""


def get_module_spec():
    module_args = dict(
        nodes=dict(type="list", elements="str", required=True),
    )

    return module_args


def get_node_network_details(module, result):
    node_network_details = NodeNetworkDetails(module)
    nodes = module.params.get("nodes")
    timeout = module.params.get("timeout")
    resp = node_network_details.retrieve(nodes, timeout)
    if not resp:
        result["error"] = "Faied to retrieve node network details"
        module.fail_json(
            msg="Failed to retrieve node network details via foundation", **result
        )
    result["nodes"] = resp


def run_module():
    module = FoundationBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {}
    get_node_network_details(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
