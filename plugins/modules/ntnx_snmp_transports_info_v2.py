#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_transports_info_v2
short_description: Retrieve SNMP transport information from a Nutanix cluster
description:
    - This module retrieves SNMP transport information from a Nutanix cluster.
    - Fetch a specific SNMP transport by port and protocol.
    - Fetch all SNMP transports configured on a cluster.
    - This module uses PC v4 APIs based SDKs
version_added: 2.6.0
notes:
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
        - The external ID of the cluster.
    type: str
    required: true
  port:
    description:
        - The port number of the SNMP transport to fetch.
        - If provided along with C(protocol), returns specific transport info.
    type: int
    required: false
  protocol:
    description:
        - The protocol of the SNMP transport to fetch.
        - If provided along with C(port), returns specific transport info.
    type: str
    required: false
    choices: ['UDP', 'UDP6', 'TCP', 'TCP6']
  read_timeout:
    description:
        - Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch all SNMP transports for a cluster
  nutanix.ncp.ntnx_snmp_transports_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
  register: result

- name: Fetch specific SNMP transport by port and protocol
  nutanix.ncp.ntnx_snmp_transports_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    port: 162
    protocol: "UDP"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching SNMP transport info.
        - Returns a single transport dict if port and protocol are specified.
        - Returns a list of transports if only cluster_ext_id is given.
    type: dict
    returned: always
    sample:
      [
        {
          "port": 162,
          "protocol": "UDP"
        }
      ]
ext_id:
    description:
        - The external ID of the cluster.
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching SNMP config"
error:
    description: The error message if an error occurs.
    type: str
    returned: when an error occurs
failed:
    description: This field indicates whether the task failed.
    returned: always
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_snmp_config  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        port=dict(type="int", required=False),
        protocol=dict(
            type="str", required=False, choices=["UDP", "UDP6", "TCP", "TCP6"]
        ),
    )
    return module_args


def get_snmp_transport_by_port_protocol(module, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    port = module.params.get("port")
    protocol = module.params.get("protocol")
    clusters_api = get_clusters_api_instance(module)
    snmp_config = get_snmp_config(module, clusters_api, cluster_ext_id)

    result["ext_id"] = cluster_ext_id
    transports = snmp_config.transports or []
    for t in transports:
        if t.port == port and t.protocol == protocol:
            result["response"] = strip_internal_attributes(t.to_dict())
            return

    result["msg"] = "SNMP transport with port {0} and protocol {1} not found.".format(
        port, protocol
    )
    module.fail_json(**result)


def get_snmp_transports(module, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    clusters_api = get_clusters_api_instance(module)
    snmp_config = get_snmp_config(module, clusters_api, cluster_ext_id)

    result["ext_id"] = cluster_ext_id
    transports = snmp_config.transports or []

    resp = []
    for t in transports:
        resp.append(strip_internal_attributes(t.to_dict()))

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
        required_together=[
            ("port", "protocol"),
        ],
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("port") and module.params.get("protocol"):
        get_snmp_transport_by_port_protocol(module, result)
    else:
        get_snmp_transports(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
