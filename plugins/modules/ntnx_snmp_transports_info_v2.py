#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_transports_info_v2
short_description: Retrieve SNMP transport details for a Nutanix cluster
description:
    - This module retrieves SNMP transport configuration details for a specific Nutanix cluster.
    - Fetches SNMP config by cluster external ID and returns the transport entries.
    - This module uses PC v4 APIs based SDKs
version_added: "2.6.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get SNMP config details for a specified cluster) -
      Operation Name: View SNMP Configuration -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
        - The external ID of the cluster.
        - Required for fetching SNMP transport details.
    type: str
    required: true
  read_timeout:
    description: Read timeout in milliseconds for API calls.
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
- name: Fetch SNMP transports for a cluster
  nutanix.ncp.ntnx_snmp_transports_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: <cluster_ext_id>
  register: result
"""

RETURN = r"""
response:
    description:
        - List of SNMP transport details for the cluster.
    type: list
    returned: always
    sample:
        [
            {
                "port": 162,
                "protocol": "UDP"
            },
            {
                "port": 161,
                "protocol": "TCP"
            }
        ]
ext_id:
    description:
        - The external ID of the cluster.
    type: str
    returned: always
    sample: "00064079-9b02-8c5e-185b-ac1f6b6f97e2"
changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false
error:
    description: This field holds information about errors that occurred during the task execution.
    returned: always
    type: bool
    sample: false
failed:
    description: This field holds information about if the task has failed.
    returned: always
    type: bool
    sample: false
msg:
    description: A message describing the result.
    returned: when applicable
    type: str
    sample: "Api Exception raised while fetching SNMP transports info"
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
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_snmp_transports_info(module, result):
    """Fetch SNMP transport details for a cluster."""
    clusters_api = get_clusters_api_instance(module)
    cluster_ext_id = module.params.get("ext_id")
    result["ext_id"] = cluster_ext_id

    resp = get_snmp_config(module, clusters_api, cluster_ext_id)
    transports = resp.transports or []

    result["response"] = [strip_internal_attributes(t.to_dict()) for t in transports]


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "failed": False,
        "msg": None,
    }
    get_snmp_transports_info(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
