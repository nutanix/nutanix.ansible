#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_remote_vpn_connections_by_cluster_id_v2
short_description: Fetch a remote VPN connection for a Prism Central cluster
version_added: 2.5.0
description:
  - This module allows you to fetch a specific remote VPN connection scoped to
    a Prism Central cluster in Nutanix Prism Central.
  - The underlying V4 API C(GET /networking/v4.3/config/clusters/{clusterExtId}/remote-vpn-connections/{extId})
    is read-only, so this module only supports fetching (get by external ID) and
    does not implement create, update, or delete operations.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get a remote VPN connection) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin,
      Super Admin, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  cluster_ext_id:
    description:
      - The external ID of the Prism Central cluster that owns the remote VPN connection.
      - Required for get operation.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the remote VPN connection to fetch.
      - Required for get operation.
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
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get remote VPN connection by cluster ext_id and ext_id
  nutanix.ncp.ntnx_remote_vpn_connections_by_cluster_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "3f2504e0-4f89-11d3-9a0c-0305e82c3301"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for fetching a remote VPN connection scoped to a Prism Central cluster.
    - A single remote VPN connection is returned when the requested C(ext_id) is found.
  returned: always
  type: dict
  sample:
    {
      "advertised_prefixes": null,
      "cluster_name": "PC-Cluster",
      "cluster_reference": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
      "description": "Remote VPN connection managed by Nutanix",
      "dpd_config": {
          "interval_secs": 30,
          "operation": "RESTART",
          "timeout_secs": 120
      },
      "dynamic_route_priority": 100,
      "ebgp_status": "UP",
      "ext_id": "3f2504e0-4f89-11d3-9a0c-0305e82c3301",
      "ipsec_config": {
          "esp_pfs_dh_group_number": 14,
          "ike_authentication_algorithm": "SHA256",
          "ike_encryption_algorithm": "AES256",
          "ike_lifetime_secs": 28800,
          "ipsec_authentication_algorithm": "SHA256",
          "ipsec_encryption_algorithm": "AES256",
          "ipsec_lifetime_secs": 3600,
          "local_authentication_id": "local-id",
          "local_vti_ip": {"ipv4": {"prefix_length": 30, "value": "169.254.0.1"}},
          "pre_shared_key": null,
          "remote_authentication_id": "remote-id",
          "remote_vti_ip": {"ipv4": {"prefix_length": 30, "value": "169.254.0.2"}}
      },
      "ipsec_tunnel_status": "UP",
      "learned_prefixes": null,
      "links": null,
      "local_gateway_reference": "9c1c8b3a-1234-4bcd-9abc-000000000001",
      "local_gateway_role": "PRIMARY",
      "metadata": null,
      "name": "remote-vpn-connection-1",
      "qos_config": {"egress_limit_mbps": 100, "ingress_limit_mbps": 100},
      "remote_gateway_reference": "9c1c8b3a-1234-4bcd-9abc-000000000002",
      "tenant_id": null,
      "vpc_name": "my-vpc",
      "vpc_reference": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    }

ext_id:
  description:
    - The external ID of the remote VPN connection that was fetched.
  returned: always
  type: str
  sample: "3f2504e0-4f89-11d3-9a0c-0305e82c3301"

changed:
  description: This indicates whether the task resulted in any changes. Always false for this read-only module.
  returned: always
  type: bool
  sample: false

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

error:
  description: Error message if any error occurred while fetching the remote VPN connection.
  returned: When an error occurs
  type: str

msg:
  description: Informational or error message set by the module.
  returned: When there is an error or informational output
  type: str
  sample: "Api Exception raised while fetching remote VPN connection info using cluster ext_id and ext_id"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_remote_entities_api_instance,
)
from ..module_utils.v4.network.helpers import (  # noqa: E402
    get_remote_vpn_connection_by_cluster_id,
)
from ..module_utils.v4.utils import (  # noqa: E402
    strip_internal_attributes,
    validate_required_params,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_remote_vpn_connections_by_cluster_id(module, api_instance, result):
    """Fetch the specified remote VPN connection under the given cluster."""
    validate_required_params(module, ["cluster_ext_id", "ext_id"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_remote_vpn_connection_by_cluster_id(
        module, api_instance, cluster_ext_id, ext_id
    )
    if resp is None:
        module.fail_json(
            msg=(
                "Remote VPN connection with cluster_ext_id '{0}' and ext_id '{1}' "
                "not found."
            ).format(cluster_ext_id, ext_id),
            **result,
        )
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_remote_entities_api_instance(module)
    get_remote_vpn_connections_by_cluster_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
