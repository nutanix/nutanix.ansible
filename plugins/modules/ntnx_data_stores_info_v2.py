#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_data_stores_info_v2
short_description: Fetch Data Stores info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about DataStore in Nutanix Prism Central.
  - If C(ext_id) is provided (Storage Container ext_id), fetch details of the specific DataStore mapped to that container on the cluster.
  - If C(ext_id) is not provided, list multiple DataStore on the cluster optionally filtered.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List Data Stores on a cluster) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Storage Admin, Storage Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  ext_id:
    description:
      - The external ID of the Storage Container whose Data Store you want to fetch.
      - When set, the module filters the cluster's Data Stores to the one that maps to this container.
    type: str
    required: false
  cluster_ext_id:
    description:
      - The external ID of the Prism Element cluster from which the Data Stores should be fetched.
      - Required — the underlying v4 API is scoped to a single cluster.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all Data Stores on a cluster
  nutanix.ncp.ntnx_data_stores_info_v2:
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
  register: result
  ignore_errors: true

- name: Fetch Data Store for a specific Storage Container on a cluster
  nutanix.ncp.ntnx_data_stores_info_v2:
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
    ext_id: "57516342-7d8e-470f-91b8-ae310737ff8c"
  register: result
  ignore_errors: true

- name: List Data Stores with filter
  nutanix.ncp.ntnx_data_stores_info_v2:
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
    filter: "containerExtId eq '57516342-7d8e-470f-91b8-ae310737ff8c'"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC DataStore info v4 API.
    - It can be a single DataStore if external ID is provided.
    - List of multiple DataStore if external ID is not provided with optional filter.
  returned: always
  type: dict
  sample:
    [
      {
        "capacity_bytes": 4291605771923,
        "container_ext_id": "57516342-7d8e-470f-91b8-ae310737ff8c",
        "container_name": "ansible_storage_container",
        "datastore_name": "ansible_ds",
        "ext_id": "b4bb1a51-1a5d-4a2c-9c8b-63c96c74ffe6",
        "free_space_bytes": 4290000000000,
        "host_ext_id": "f28e7475-f835-42ef-ac35-ecbc48d5421e",
        "host_ip_address": "10.44.76.55",
        "links": null,
        "tenant_id": null,
        "vm_names": []
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching Data Stores for cluster"

error:
  description: The error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the Storage Container filter (when provided).
  returned: when Storage Container ext_id is provided
  type: str
  sample: "57516342-7d8e-470f-91b8-ae310737ff8c"

total_available_results:
  description: The total number of Data Stores returned on the cluster.
  returned: when Data Stores are fetched (list operation)
  type: int
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_storage_container_api_instance,
)
from ..module_utils.v4.storage.helpers import get_data_stores_by_cluster  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str", required=True),
    )
    return module_args


def _build_filter(module):
    parts = []
    ext_id = module.params.get("ext_id")
    user_filter = module.params.get("filter")
    if ext_id:
        parts.append("containerExtId eq '{0}'".format(ext_id))
    if user_filter:
        parts.append(user_filter)
    if not parts:
        return None
    return " and ".join(parts)


def get_data_stores(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    _filter = _build_filter(module)

    resp = get_data_stores_by_cluster(
        module=module,
        api_instance=api_instance,
        cluster_ext_id=cluster_ext_id,
        _filter=_filter,
    )

    resp_dict = strip_internal_attributes(resp.to_dict())
    metadata = resp_dict.get("metadata") or {}
    total_available_results = metadata.get("total_available_results")
    if total_available_results is not None:
        result["total_available_results"] = total_available_results

    data = resp_dict.get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}

    api_instance = get_storage_container_api_instance(module)
    if module.params.get("ext_id"):
        result["ext_id"] = module.params.get("ext_id")

    get_data_stores(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
