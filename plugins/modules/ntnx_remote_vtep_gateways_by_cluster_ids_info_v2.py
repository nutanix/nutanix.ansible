#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_remote_vtep_gateways_by_cluster_ids_info_v2
short_description: Fetch remote VTEP gateways info discovered under a Prism Element cluster in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about RemoteVtepGatewaysByClusterId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific RemoteVtepGatewaysByClusterId.
  - If C(ext_id) is not provided, list multiple RemoteVtepGatewaysByClusterId optionally filtered / paginated.
  - C(cluster_ext_id) is always required — the Nutanix v4 Prism Central discovery
    endpoint for remote VTEP gateways is always scoped to a single Prism Element
    cluster external ID.
  - The RemoteVtepGateway resource is a B(read-only) discovery surface used for
    Layer 2 subnet extension (L2 stretch) peer selection. The underlying SDK
    exposes only C(get_remote_vtep_gateway_for_cluster_by_id) and
    C(list_remote_vtep_gateways_by_cluster_id); there are no create / update /
    delete APIs for this entity.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get remote VTEP gateway by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
      Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - >-
      B(List remote VTEP gateways) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
      Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  cluster_ext_id:
    description:
      - External ID of the Prism Element cluster that owns the remote VTEP gateway(s).
      - Required for both list and get-by-id operations.
    type: str
    required: true
  ext_id:
    description:
      - External ID of a specific remote VTEP gateway to fetch.
      - When provided, the module fetches only that gateway (get-by-id).
      - When omitted, the module lists all discovered remote VTEP gateways for the cluster.
    type: str
    required: false
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
- name: Fetch a remote VTEP gateway using its external ID
  nutanix.ncp.ntnx_remote_vtep_gateways_by_cluster_ids_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true

- name: List all remote VTEP gateways discovered on a Prism Element cluster
  nutanix.ncp.ntnx_remote_vtep_gateways_by_cluster_ids_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: List remote VTEP gateways with a filter
  nutanix.ncp.ntnx_remote_vtep_gateways_by_cluster_ids_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    filter: "name eq 'remote-vtep-gw-ansible'"
  register: result
  ignore_errors: true

- name: List remote VTEP gateways with a limit
  nutanix.ncp.ntnx_remote_vtep_gateways_by_cluster_ids_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    limit: 1
  register: result
  ignore_errors: true

- name: List remote VTEP gateways sorted by name descending
  nutanix.ncp.ntnx_remote_vtep_gateways_by_cluster_ids_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    orderby: "name desc"
  register: result
  ignore_errors: true

- name: List remote VTEP gateways using pagination
  nutanix.ncp.ntnx_remote_vtep_gateways_by_cluster_ids_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    page: 0
    limit: 10
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RemoteVtepGatewaysByClusterId info v4 API.
    - It can be a single RemoteVtepGatewaysByClusterId if external ID is provided.
    - List of multiple RemoteVtepGatewaysByClusterId if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    [
      {
        "cluster_name": "PE-cluster-01",
        "cluster_reference": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
        "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
        "high_availability_group": {
            "algorithm": "ACTIVE_BACKUP",
            "is_ha_enabled": true,
            "peered_gateways": [
                {
                    "ext_id": "9f6cca9c-4a53-4ad5-9f4d-3f5a8a1e7db1",
                    "status": "UP"
                }
            ]
        },
        "is_active": true,
        "is_local": false,
        "links": null,
        "metadata": null,
        "name": "remote-vtep-gw-ansible",
        "tenant_id": null,
        "vpc_name": "vpc_ansible",
        "vpc_reference": "1c6bc5f3-c18c-4702-4c2d-b769fd5f9401",
        "vxlan_port": 4789
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

msg:
  description: This indicates the message associated with the operation, primarily on error.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching remote VTEP gateways info"

ext_id:
  description: External ID of the remote VTEP gateway that was fetched (only when ext_id was provided).
  type: str
  returned: when external ID is provided
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

cluster_ext_id:
  description: External ID of the Prism Element cluster used to scope the fetch/list.
  type: str
  returned: always
  sample: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"

total_available_results:
  description: The total number of remote VTEP gateways discovered on the given Prism Element cluster.
  type: int
  returned: when all remote VTEP gateways are fetched
  sample: 5
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
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_remote_vtep_gateway_for_cluster(
        module, api_instance, cluster_ext_id, ext_id
    )
    result["cluster_ext_id"] = cluster_ext_id
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_remote_vtep_gateways(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating remote VTEP gateways info spec", **result
        )

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
        get_remote_vtep_gateway_using_ext_id(module, api_instance, result)
    else:
        get_remote_vtep_gateways(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
