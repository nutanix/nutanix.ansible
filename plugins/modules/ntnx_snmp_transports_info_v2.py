#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_transports_info_v2
short_description: Retrieve SNMP transport configuration info for Nutanix clusters
description:
    - This module retrieves SNMP transport configuration details for a Nutanix cluster.
    - Fetch all SNMP transports configured on a cluster by providing the cluster external ID.
    - This module uses PC v4 APIs based SDKs
version_added: "2.6.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get SNMP config) -
      Operation Name: View SNMP Config -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster to fetch SNMP transport details for.
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
- name: Fetch all SNMP transports for a cluster
  nutanix.ncp.ntnx_snmp_transports_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
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
                "protocol": "UDP",
                "port": 161
            },
            {
                "protocol": "UDP",
                "port": 162
            }
        ]
ext_id:
    description:
        - The external ID of the cluster.
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
changed:
    description:
        - Indicates if any changes were made during the operation.
        - Always false for info modules.
    type: bool
    returned: always
    sample: false
msg:
    description:
        - A message describing the result of the operation.
    type: str
    returned: when an error occurs
error:
    description:
        - The error message if an error occurs.
    type: str
    returned: when an error occurs
failed:
    description:
        - Whether the operation failed.
    type: bool
    returned: when an error occurs
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_snmp_config  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client  # noqa: E402, F401
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402, F401
        mock_sdk as ntnx_clustermgmt_py_client,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_snmp_transports(module, api_instance, result):
    """Fetch SNMP transports for a cluster."""
    cluster_ext_id = module.params["cluster_ext_id"]
    result["ext_id"] = cluster_ext_id

    snmp_config = get_snmp_config(module, api_instance, cluster_ext_id)

    transports = snmp_config.transports if snmp_config else []
    if transports:
        transports_list = [strip_internal_attributes(t.to_dict()) for t in transports]
        result["response"] = transports_list
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )

    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }

    api_instance = get_clusters_api_instance(module)
    get_snmp_transports(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
