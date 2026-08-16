#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_remote_vtep_gateway_for_clusters_info_v2
short_description: Fetch remote VTEP gateway info scoped to a Prism Central cluster
version_added: 2.7.0
description:
  - This module allows you to fetch information about RemoteVtepGatewayForCluster in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific RemoteVtepGatewayForCluster.
  - If C(ext_id) is not provided, list multiple RemoteVtepGatewayForCluster optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  cluster_ext_id:
    description:
      - The external ID of the Prism Central cluster the remote VTEP gateway is scoped to.
      - This is a required path parameter for every list and get-by-id call.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the remote VTEP gateway.
      - When provided, a single remote VTEP gateway is fetched using get-by-id.
      - When omitted, the module lists remote VTEP gateways for the cluster, with optional filter / limit / page / orderby.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all remote VTEP gateways for a cluster
  nutanix.ncp.ntnx_remote_vtep_gateway_for_clusters_info_v2:
    cluster_ext_id: "cae459ec-08db-475e-a5e5-151e390c9484"
  register: remote_vtep_gateways

- name: Fetch a specific remote VTEP gateway by ext_id
  nutanix.ncp.ntnx_remote_vtep_gateway_for_clusters_info_v2:
    cluster_ext_id: "cae459ec-08db-475e-a5e5-151e390c9484"
    ext_id: "5b2e4e93-2222-3333-7777-a015d302eec2"
  register: remote_vtep_gateway

- name: List remote VTEP gateways with a filter
  nutanix.ncp.ntnx_remote_vtep_gateway_for_clusters_info_v2:
    cluster_ext_id: "cae459ec-08db-475e-a5e5-151e390c9484"
    filter: "name eq 'gateway-1'"
  register: filtered_gateways

- name: List remote VTEP gateways with a limit
  nutanix.ncp.ntnx_remote_vtep_gateway_for_clusters_info_v2:
    cluster_ext_id: "cae459ec-08db-475e-a5e5-151e390c9484"
    limit: 10
  register: limited_gateways
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RemoteVtepGatewayForCluster info v4 API.
    - It can be a single RemoteVtepGatewayForCluster if external ID is provided.
    - List of multiple RemoteVtepGatewayForCluster if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster_name": "auto_cluster_prod_36acf9b012ca",
      "cluster_reference": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "ext_id": "5b2e4e93-2222-3333-7777-a015d302eec2",
      "high_availability_group": null,
      "is_active": true,
      "is_local": false,
      "links": null,
      "metadata": null,
      "name": "remote-vtep-gateway-example",
      "tenant_id": null,
      "vpc_name": "vpc-example",
      "vpc_reference": "6125d91e-4788-4125-6355-27d5e7667b93",
      "vxlan_port": 4789
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the remote VTEP gateway.
  returned: when external ID is provided
  type: str
  sample: "5b2e4e93-2222-3333-7777-a015d302eec2"

msg:
  description: This indicates the message if any message occurred.
  returned: when there is an error
  type: str
  sample: "Api Exception raised while fetching remote VTEP gateway info using ext_id"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available remote VTEP gateways for the cluster.
  type: int
  returned: when all remote VTEP gateways are fetched
  sample: 0
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_remote_entities_api_instance,
)
from ..module_utils.v4.network.helpers import (  # noqa: E402
    get_remote_vtep_gateway_for_cluster,
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


def get_remote_vtep_gateway_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = ext_id
    resp = get_remote_vtep_gateway_for_cluster(
        module, api_instance, cluster_ext_id, ext_id
    )
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_remote_vtep_gateways(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating remote VTEP gateways info spec", **result
        )

    # The list SDK method does not support _select — drop it to avoid TypeError.
    kwargs.pop("_select", None)

    try:
        resp = api_instance.list_remote_vtep_gateways_by_cluster_id(
            clusterExtId=cluster_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching remote VTEP gateways info",
        )

    total_available_results = (
        resp.metadata.total_available_results if resp.metadata else 0
    )
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
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_remote_entities_api_instance(module)
    if module.params.get("ext_id"):
        get_remote_vtep_gateway_using_ext_id(module, api_instance, result)
    else:
        get_remote_vtep_gateways(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
