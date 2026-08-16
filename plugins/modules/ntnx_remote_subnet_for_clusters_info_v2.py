#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_remote_subnet_for_clusters_info_v2
short_description: Fetch information about remote subnets visible from a Prism Central cluster
version_added: 2.5.0
description:
  - This module allows you to fetch information about RemoteSubnetForCluster in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific RemoteSubnetForCluster.
  - If C(ext_id) is not provided, list multiple RemoteSubnetForCluster optionally filtered / paginated.
  - RemoteSubnetForCluster is a read-only construct exposed by the Networking v4.3 RemoteEntitiesApi.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get remote subnet by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin,
      Prism Viewer, Project Admin, Super Admin, VPC Admin
    - >-
      B(List remote subnets) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin,
      Prism Viewer, Project Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  cluster_ext_id:
    description:
      - Reference to the Prism Central cluster to query for remote subnets.
      - Required for all operations (both get-by-id and list).
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the remote subnet.
      - When provided, the module fetches the specific remote subnet.
      - When omitted, the module lists remote subnets on the given cluster.
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
- name: Get remote subnet using ext_id
  nutanix.ncp.ntnx_remote_subnet_for_clusters_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all remote subnets for a Prism Central cluster
  nutanix.ncp.ntnx_remote_subnet_for_clusters_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: List remote subnets with filter
  nutanix.ncp.ntnx_remote_subnet_for_clusters_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    filter: "name eq 'remote_subnet_ansible'"
  register: result
  ignore_errors: true

- name: List remote subnets with limit and page
  nutanix.ncp.ntnx_remote_subnet_for_clusters_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    limit: 1
    page: 0
  register: result
  ignore_errors: true

- name: List remote subnets ordered by name
  nutanix.ncp.ntnx_remote_subnet_for_clusters_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    orderby: "name desc"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RemoteSubnetForCluster info v4 API.
    - It can be a single RemoteSubnetForCluster if external ID is provided.
    - List of multiple RemoteSubnetForCluster if external ID is not provided with optional filter/limit/page/orderby.
  returned: always
  type: dict
  sample:
    {
      "bridge_name": null,
      "cluster_name": null,
      "cluster_name_list": null,
      "cluster_reference": null,
      "cluster_reference_list": null,
      "description": null,
      "dhcp_options": null,
      "dynamic_ip_addresses": null,
      "external_dhcp_servers": null,
      "ext_id": "b57a5527-72ca-45aa-be07-829ba18f9f8b",
      "hypervisor_type": null,
      "ip_config": [
          {
              "ipv4": {
                  "default_gateway_ip": {
                      "prefix_length": 32,
                      "value": "192.168.170.1"
                  },
                  "dhcp_server_address": null,
                  "ip_subnet": {
                      "ip": {
                          "prefix_length": 32,
                          "value": "192.168.170.0"
                      },
                      "prefix_length": 24
                  },
                  "pool_list": null
              },
              "ipv6": null
          }
      ],
      "ip_prefix": null,
      "ip_usage": null,
      "is_advanced_networking": null,
      "is_external": null,
      "is_nat_enabled": null,
      "layer2_stretch_reference": null,
      "links": null,
      "metadata": null,
      "migration_state": null,
      "name": "GNHQMOOkSSrI_ansible-clear-rp-counter_subnet",
      "network_function_chain_reference": null,
      "network_id": null,
      "reserved_ip_addresses": null,
      "subnet_type": null,
      "tenant_id": null,
      "virtual_switch": null,
      "virtual_switch_reference": null,
      "vpc": null,
      "vpc_name": "GNHQMOOkSSrI_ansible-clear-rp-counter_vpc",
      "vpc_reference": "305ed978-23d3-4d4d-8f5d-c49bf8ab5ecd"
    }

changed:
  description: Always false for info modules. No changes are made to the target system.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching remote subnets info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task has failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the remote subnet.
  type: str
  returned: when external ID is provided
  sample: "b57a5527-72ca-45aa-be07-829ba18f9f8b"

total_available_results:
  description: The total number of available remote subnets on the given cluster.
  type: int
  returned: when all remote subnets are fetched (list operation)
  sample: 11
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_remote_entities_api_instance,
)
from ..module_utils.v4.network.helpers import (  # noqa: E402
    get_remote_subnet_for_cluster,
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
        ext_id=dict(type="str"),
    )
    return module_args


def get_remote_subnet_using_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_remote_subnet_for_cluster(module, api_instance, cluster_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_remote_subnets(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating remote subnets info spec", **result)

    cluster_ext_id = module.params.get("cluster_ext_id")
    try:
        resp = api_instance.list_remote_subnets_by_cluster_id(
            clusterExtId=cluster_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching remote subnets info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_remote_entities_api_instance(module)
    if module.params.get("ext_id"):
        get_remote_subnet_using_ext_id(module, api_instance, result)
    else:
        get_remote_subnets(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
