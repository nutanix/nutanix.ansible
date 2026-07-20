#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_capabilities_info_v2
short_description: Fetch cluster capabilities info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about ClusterCapability in Nutanix Prism Central.
  - If C(cluster_id) is provided, list capabilities filtered to the given Prism Element cluster UUID.
  - If C(cluster_id) is not provided, list capabilities for all registered clusters optionally filtered / paginated.
  - The underlying v4 API only exposes a list operation (there is no get-by-id, create, update or delete endpoint for cluster capabilities).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List cluster capabilities) -
      Required Roles: Super Admin, Prism Admin, Prism Viewer, Project Admin, Network Infra Admin, VPC Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  cluster_id:
    description:
      - Prism Element cluster UUID whose networking capabilities should be retrieved.
      - Convenience option that translates to an OData C(clusterId eq '<cluster_id>') filter on the list API.
      - Mutually exclusive with C(filter) since both target the C($filter) query parameter.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all cluster capabilities
  nutanix.ncp.ntnx_cluster_capabilities_info_v2:
  register: result
  ignore_errors: true

- name: List cluster capabilities for a specific Prism Element cluster
  nutanix.ncp.ntnx_cluster_capabilities_info_v2:
    cluster_id: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true

- name: List cluster capabilities using an explicit OData filter
  nutanix.ncp.ntnx_cluster_capabilities_info_v2:
    filter: "clusterId eq '0006555e-4e63-4a5e-185b-ac1f6b6f97e2'"
  register: result
  ignore_errors: true

- name: List cluster capabilities with a limit
  nutanix.ncp.ntnx_cluster_capabilities_info_v2:
    limit: 1
  register: result
  ignore_errors: true

- name: List cluster capabilities with orderby
  nutanix.ncp.ntnx_cluster_capabilities_info_v2:
    orderby: "clusterId"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ClusterCapability info v4 API.
    - List of ClusterCapability objects (one per cluster) with the networking capabilities the cluster supports.
    - When C(cluster_id) is provided the list is filtered down to that specific cluster.
  returned: always
  type: dict
  sample:
    [
      {
        "capabilities": [
          {
            "capability_name": "NIC_TEAM_TBL_SYNC_ENABLE",
            "is_supported": true
          },
          {
            "capability_name": "SUPPORTS_ADVANCED_NETWORK_FUNCTION_NICS",
            "is_supported": true
          },
          {
            "capability_name": "SUPPORTS_PC_DVS_V1",
            "is_supported": true
          },
          {
            "capability_name": "SUPPORTS_SPAN_V3",
            "is_supported": true
          }
        ],
        "cluster_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
        "ext_id": null,
        "links": null,
        "metadata": null,
        "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always False for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching cluster capabilities info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: When an error occurs
  type: str

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

total_available_results:
  description:
    - The total number of available cluster capabilities entries in PC.
    - May be C(None) when the list API does not populate this field for cluster capabilities.
  type: int
  returned: when the list operation is invoked
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_cluster_capabilities_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_id=dict(type="str"),
    )

    return module_args


def _merge_cluster_id_filter(module_params):
    """Fold the cluster_id convenience option into an OData $filter expression."""
    cluster_id = module_params.get("cluster_id")
    if not cluster_id:
        return
    cluster_filter = "clusterId eq '{0}'".format(cluster_id)
    existing_filter = module_params.get("filter")
    if existing_filter:
        module_params["filter"] = "({0}) and {1}".format(
            existing_filter, cluster_filter
        )
    else:
        module_params["filter"] = cluster_filter


def get_cluster_capabilities(module, api_instance, result):
    _merge_cluster_id_filter(module.params)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating cluster capabilities info spec", **result
        )

    try:
        resp = api_instance.list_cluster_capabilities(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster capabilities info",
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
            ("cluster_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_cluster_capabilities_api_instance(module)
    get_cluster_capabilities(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
