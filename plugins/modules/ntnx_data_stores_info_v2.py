#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_data_stores_info_v2
short_description: Fetch Data Stores mounted on a Nutanix cluster
version_added: 2.7.0
description:
  - This module allows you to fetch information about DataStoreForCluster in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific DataStoreForCluster.
  - If C(ext_id) is not provided, list multiple DataStoreForCluster optionally filtered / paginated.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get Data Stores for a cluster) -
    Required Roles: Prism Admin, Prism Viewer, Storage Admin, Storage Viewer, Super Admin
  - The underlying v4 storage SDK exposes only the list operation
    (C(GetDataStores)) for Data Stores; there is no dedicated
    get-by-ext_id API. When C(ext_id) is supplied this module lists the
    Data Stores for the cluster and filters client-side.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  ext_id:
    description:
      - The external ID of the Data Store to look up.
      - When supplied, the module returns the single matching entity
        (filtered client-side over the list returned by the v4 API).
    type: str
    required: false
  cluster_ext_id:
    description:
      - The external ID of the cluster whose Data Stores should be listed.
      - Required because the underlying v4 API is cluster-scoped.
    type: str
    required: true
  filter:
    description:
      - OData V4.01 style C($filter) expression forwarded to the v4 API.
      - Only the C(containerExtId) attribute is supported by the API.
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
- name: List all Data Stores mounted on a cluster
  nutanix.ncp.ntnx_data_stores_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
  register: result

- name: List Data Stores for a particular container
  nutanix.ncp.ntnx_data_stores_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
    filter: "containerExtId eq '57516342-7d8e-470f-91b8-ae310737ff8c'"
  register: result

- name: Fetch a specific Data Store by its external ID
  nutanix.ncp.ntnx_data_stores_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
    ext_id: "1a68c1cd-8f38-4d64-8fd1-01d34e94b1a2"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC DataStoreForCluster info v4 API.
    - It can be a single DataStoreForCluster if external ID is provided.
    - List of multiple DataStoreForCluster if external ID is not provided
      with optional filter.
  returned: always
  type: dict
  sample:
    [
      {
        "capacity_bytes": 4291605771923,
        "container_ext_id": "57516342-7d8e-470f-91b8-ae310737ff8c",
        "container_name": "SelfServiceContainer",
        "datastore_name": "ansible_ds",
        "ext_id": "1a68c1cd-8f38-4d64-8fd1-01d34e94b1a2",
        "free_space_bytes": 4200000000000,
        "host_ext_id": "8300384a-56ee-4750-aeb8-3d1c42908bee",
        "host_ip_address": "10.44.76.51",
        "links": null,
        "tenant_id": null,
        "vm_names": []
      }
    ]

changed:
  description: Always false; info modules never mutate state.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the Data Store that was looked up.
  returned: when external ID is provided
  type: str
  sample: "1a68c1cd-8f38-4d64-8fd1-01d34e94b1a2"

total_available_results:
  description: Total number of Data Stores returned by the v4 API for the cluster.
  returned: when Data Stores are fetched
  type: int
  sample: 3

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, or a specific Data Store cannot be found.
  type: str
  sample: "Api Exception raised while fetching Data Stores info"

error:
  description: The error message if an error occurs.
  returned: when an error occurs
  type: str

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_storage_container_api_instance,
)
from ..module_utils.v4.storage.helpers import get_data_stores_by_cluster  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_data_store_by_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_data_stores_by_cluster(module, api_instance, cluster_ext_id)
    total_available_results = getattr(resp.metadata, "total_available_results", None)
    if total_available_results is not None:
        result["total_available_results"] = total_available_results
    match = None
    for item in getattr(resp, "data", None) or []:
        if getattr(item, "ext_id", None) == ext_id:
            match = item
            break
    if match is None:
        result["ext_id"] = ext_id
        result["response"] = None
        result["msg"] = (
            "No Data Store with ext_id '{0}' was found on cluster '{1}'.".format(
                ext_id, cluster_ext_id
            )
        )
        module.fail_json(**result)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(match.to_dict())


def get_data_stores(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    _filter = module.params.get("filter")
    resp = get_data_stores_by_cluster(
        module, api_instance, cluster_ext_id, _filter=_filter
    )
    total_available_results = getattr(resp.metadata, "total_available_results", None)
    if total_available_results is not None:
        result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("ext_id", "filter")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_storage_container_api_instance(module)
    if module.params.get("ext_id"):
        get_data_store_by_ext_id(module, api_instance, result)
    else:
        get_data_stores(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
