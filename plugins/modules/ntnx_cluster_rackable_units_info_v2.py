#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_rackable_units_info_v2
short_description: Fetch rackable units of a cluster in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about RackableUnitsByClusterId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific RackableUnitsByClusterId.
  - If C(ext_id) is not provided, list multiple RackableUnitsByClusterId for the specified cluster.
  - A rackable unit is the physical block or chassis that houses one or more Nutanix nodes.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Get rackable unit by ext_id) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(Get the list of rackable units for a cluster) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the rackable unit.
      - When provided, fetches the details of the specific rackable unit.
    type: str
    required: false
  cluster_ext_id:
    description:
      - The external ID (UUID) of the parent cluster.
      - Required for both list and get-by-ID operations because the v4 API is scoped by cluster.
    type: str
    required: true
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
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch a specific rackable unit by external ID
  nutanix.ncp.ntnx_cluster_rackable_units_info_v2:
    cluster_ext_id: "0005e2f7-8ee2-6bbb-0000-000000012345"
    ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
  register: rackable_unit

- name: List all rackable units for a cluster
  nutanix.ncp.ntnx_cluster_rackable_units_info_v2:
    cluster_ext_id: "0005e2f7-8ee2-6bbb-0000-000000012345"
  register: rackable_units
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RackableUnitsByClusterId info v4 API.
    - It can be a single RackableUnitsByClusterId if external ID is provided.
    - List of multiple RackableUnitsByClusterId if external ID is not provided.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "5879195f-5101-4d41-8e6d-af4a6aa52472",
      "id": 10,
      "serial": "18FM6G460083",
      "model": "USELAYOUT",
      "model_name": "NX-1065-G5",
      "nodes": [
        {
          "uuid": "adf0c9e0-4051-4cd2-9f6f-ca9f962e941b",
          "svm_id": 2,
          "position": 4
        }
      ],
      "rack": null,
      "links": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the rackable unit
  returned: when external ID is provided
  type: str
  sample: "5879195f-5101-4d41-8e6d-af4a6aa52472"

msg:
  description: Status/error message when applicable
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching rackable unit info using ext_id"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when an error occurs
  type: str

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available rackable units for the cluster.
  returned: when list of rackable units is fetched
  type: int
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_rackable_unit  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_rackable_unit_by_ext_id(module, clusters_api, result):
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    resp = get_rackable_unit(module, clusters_api, ext_id, cluster_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_rackable_units(module, clusters_api, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    try:
        resp = clusters_api.list_rackable_units_by_cluster_id(
            clusterExtId=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching rackable units info",
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
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    clusters_api = get_clusters_api_instance(module)
    if module.params.get("ext_id"):
        get_rackable_unit_by_ext_id(module, clusters_api, result)
    else:
        get_rackable_units(module, clusters_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
