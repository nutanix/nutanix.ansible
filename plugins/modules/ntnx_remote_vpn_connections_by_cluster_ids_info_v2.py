#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_remote_vpn_connections_by_cluster_ids_info_v2
short_description: Fetch information about remote VPN connections scoped to a Prism Central cluster
version_added: 2.5.0
description:
  - This module allows you to fetch information about remote VPN connections in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific remote VPN connection under the given cluster.
  - If C(ext_id) is not provided, list multiple remote VPN connections optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get remote VPN connection by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin,
      Super Admin, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - >-
      B(List remote VPN connections for a cluster) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin,
      Super Admin, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  cluster_ext_id:
    description:
      - The external ID of the Prism Central cluster whose remote VPN connections are being listed or fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of a specific remote VPN connection to fetch.
      - If provided, a single remote VPN connection is returned.
      - If not provided, all remote VPN connections for the given cluster are listed.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get remote VPN connection by ext_id for a Prism Central cluster
  nutanix.ncp.ntnx_remote_vpn_connections_by_cluster_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "3f2504e0-4f89-11d3-9a0c-0305e82c3301"
  register: single_result
  ignore_errors: true

- name: List all remote VPN connections for a Prism Central cluster
  nutanix.ncp.ntnx_remote_vpn_connections_by_cluster_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: list_result
  ignore_errors: true

- name: List remote VPN connections with a filter
  nutanix.ncp.ntnx_remote_vpn_connections_by_cluster_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    filter: "name eq 'remote-vpn-connection-1'"
  register: filtered_result
  ignore_errors: true

- name: List remote VPN connections with limit
  nutanix.ncp.ntnx_remote_vpn_connections_by_cluster_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    limit: 1
  register: limited_result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RemoteVpnConnectionsByClusterId info v4 API.
    - A single remote VPN connection is returned when C(ext_id) is provided.
    - A list of remote VPN connections is returned when C(ext_id) is not provided (optionally filtered / paginated).
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
      "ipsec_config": null,
      "ipsec_tunnel_status": "UP",
      "learned_prefixes": null,
      "links": null,
      "local_gateway_reference": "9c1c8b3a-1234-4bcd-9abc-000000000001",
      "local_gateway_role": "PRIMARY",
      "metadata": null,
      "name": "remote-vpn-connection-1",
      "qos_config": null,
      "remote_gateway_reference": "9c1c8b3a-1234-4bcd-9abc-000000000002",
      "tenant_id": null,
      "vpc_name": "my-vpc",
      "vpc_reference": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Informational or error message set by the module.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching remote VPN connections info"

error:
  description: This field typically holds information about errors during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: Whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the remote VPN connection (only when a single entity is fetched).
  type: str
  returned: when external ID is provided
  sample: "3f2504e0-4f89-11d3-9a0c-0305e82c3301"

total_available_results:
  description: The total number of available remote VPN connections for the given cluster.
  type: int
  returned: when all remote VPN connections are fetched
  sample: 5
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
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_remote_vpn_connection_by_ext_id(module, api_instance, result):
    """Get a single remote VPN connection by cluster_ext_id + ext_id."""
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
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
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_remote_vpn_connections_by_cluster_id(module, api_instance, result):
    """List remote VPN connections for a Prism Central cluster."""
    cluster_ext_id = module.params.get("cluster_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating remote VPN connections info spec", **result
        )
    kwargs["clusterExtId"] = cluster_ext_id
    try:
        resp = api_instance.list_remote_vpn_connections_by_cluster_id(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching remote VPN connections info",
        )

    total_available_results = getattr(resp.metadata, "total_available_results", None)
    result["total_available_results"] = total_available_results
    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_remote_entities_api_instance(module)
    if module.params.get("ext_id"):
        get_remote_vpn_connection_by_ext_id(module, api_instance, result)
    else:
        list_remote_vpn_connections_by_cluster_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
