#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_rackable_units_info_v2
short_description: Fetch rackable unit info from a Nutanix cluster via Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about rackable units of a Nutanix cluster from Prism Central.
  - If C(ext_id) is provided, fetch details of the specific rackable unit of the given cluster.
  - If C(ext_id) is not provided, list all rackable units of the given cluster.
  - A rackable unit represents a physical block/chassis containing one or more nodes that
    make up a Nutanix cluster. This module is a read-only info source.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get rackable unit by ext_id) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(Get list of rackable units for a cluster) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the Prism Element cluster whose rackable units
        should be fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external ID (UUID) of a specific rackable unit inside the cluster.
      - If provided, only that rackable unit's details are returned.
    type: str
    required: false
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
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all rackable units of a cluster
  nutanix.ncp.ntnx_rackable_units_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0005f5b1-2b2a-1cde-0000-000000012345"
  register: rackable_units

- name: Get a specific rackable unit using its external ID
  nutanix.ncp.ntnx_rackable_units_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0005f5b1-2b2a-1cde-0000-000000012345"
    ext_id: "9d2b1c04-4f5a-4e3a-9d3b-bf7b6f4a5c11"
  register: rackable_unit
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RackableUnit info v4 API.
    - It can be a single rackable unit if C(ext_id) is provided.
    - Otherwise, a list of rackable units for the given cluster.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "5879195f-5101-4d41-8e6d-af4a6aa52472",
      "id": 10,
      "model": "USELAYOUT",
      "model_name": "NX-1065-G5",
      "serial": "18FM6G460083",
      "rack": null,
      "links": null,
      "tenant_id": null,
      "nodes": [
        {
          "position": 4,
          "svm_id": 2,
          "uuid": "adf0c9e0-4051-4cd2-9f6f-ca9f962e941b"
        }
      ]
    }

changed:
  description: Whether the module made any change. Always false for an info module.
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the rackable unit (only when C(ext_id) is provided).
  returned: when ext_id is provided
  type: str
  sample: "5879195f-5101-4d41-8e6d-af4a6aa52472"

cluster_ext_id:
  description: The external ID of the cluster whose rackable units were fetched.
  returned: always
  type: str
  sample: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"

total_available_results:
  description:
    - The total number of rackable units available for the cluster.
    - Only present when listing (i.e. C(ext_id) is not provided).
  returned: when all rackable units are fetched
  type: int
  sample: 1

msg:
  description: Status/error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching rackable units info"

error:
  description: Error details if any error occurred during the API call.
  returned: when an error occurs
  type: str

failed:
  description: Whether the module failed.
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
from ..module_utils.v4.clusters_mgmt.helpers import get_rackable_unit  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )

    return module_args


def get_rackable_unit_by_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_rackable_unit(module, api_instance, ext_id, cluster_ext_id)
    result["ext_id"] = ext_id
    result["cluster_ext_id"] = cluster_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_rackable_units(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    try:
        resp = api_instance.list_rackable_units_by_cluster_id(
            clusterExtId=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching rackable units info",
        )

    total_available_results = getattr(
        getattr(resp, "metadata", None), "total_available_results", None
    )
    if total_available_results is not None:
        result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "cluster_ext_id": None,
    }
    api_instance = get_clusters_api_instance(module)
    if module.params.get("ext_id"):
        get_rackable_unit_by_ext_id(module, api_instance, result)
    else:
        list_rackable_units(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
