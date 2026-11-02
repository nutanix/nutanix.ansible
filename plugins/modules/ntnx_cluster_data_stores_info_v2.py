#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_data_stores_info_v2
short_description: Fetch datastores of a cluster in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about datastores of a cluster in Nutanix Prism Central.
  - The datastores returned correspond to Storage Containers mounted as NFS datastores on the ESXi hosts of the cluster.
  - If C(ext_id) is provided, fetch datastores whose parent Storage Container matches that external ID.
  - If C(ext_id) is not provided, fetch multiple datastores for the given cluster with/without using filters, limit, etc.
  - The Nutanix v4 API does not expose a get-by-id endpoint for datastores; C(ext_id) is applied as an OData filter
    on C(containerExtId).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View Storage Container Datastore) -
    Required Roles: CSI System, Kubernetes Data Services System, Prism Admin, Prism Viewer, Project Manager, Storage Admin, Storage Viewer,
    Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external identifier of the cluster whose datastores should be listed.
      - Required — the v4 SDK C(list_data_stores_by_cluster_id) endpoint is scoped to a specific cluster.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the parent Storage Container used to filter returned datastores.
      - The Nutanix v4 API does not expose a get-by-id endpoint for datastores.
      - When supplied, the module lists datastores with OData filter C(containerExtId eq '<ext_id>').
      - A Storage Container may be mounted on multiple hosts, so the response is a list of matching datastores.
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
- name: List all datastores of a cluster
  nutanix.ncp.ntnx_cluster_data_stores_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true

- name: List datastores of a cluster filtered by storage container ext_id (OData)
  nutanix.ncp.ntnx_cluster_data_stores_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    filter: "containerExtId eq '547c01c4-19c2-4293-8a9c-43441c18d0c7'"
  register: result
  ignore_errors: true

- name: List datastores of a cluster with limit
  nutanix.ncp.ntnx_cluster_data_stores_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    limit: 1
  register: result
  ignore_errors: true

- name: List all datastores of a cluster with fetch_all
  nutanix.ncp.ntnx_cluster_data_stores_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    fetch_all: true
  register: result
  ignore_errors: true

- name: Fetch datastores of a cluster by storage container ext_id
  nutanix.ncp.ntnx_cluster_data_stores_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    ext_id: "547c01c4-19c2-4293-8a9c-43441c18d0c7"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC datastores info v4 API.
    - List of matching datastores when C(ext_id) is provided (filtered by parent Storage Container).
    - List of multiple datastores when C(ext_id) is not provided, with optional filter or limit.
  returned: always
  type: list
  sample:
    [
      {
        "capacity_bytes": 4365702025514,
        "container_ext_id": "547c01c4-19c2-4293-8a9c-43441c18d0c7",
        "container_name": "SelfServiceContainer",
        "datastore_name": "ansible_datastore",
        "ext_id": null,
        "free_space_bytes": 4111102025514,
        "host_ext_id": "f28e7475-f835-42ef-ac35-ecbc48d5421e",
        "host_ip_address": {
          "value": "10.0.0.4"
        },
        "links": null,
        "tenant_id": null,
        "vm_names": ["vm-1", "vm-2"]
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External identifier of the parent Storage Container, when supplied on input.
  type: str
  returned: when external ID is provided
  sample: "547c01c4-19c2-4293-8a9c-43441c18d0c7"

cluster_ext_id:
  description: External identifier of the cluster whose datastores were listed.
  type: str
  returned: always
  sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while listing datastores for cluster with ext_id: 0006555e-4e63-4a5e-185b-ac1f6b6f97e2"

error:
  description: This field typically holds information about errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available datastores in the cluster (as reported by the PC pagination metadata).
  type: int
  returned: when all datastores are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_storage_containers_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )

    return module_args


def get_datastore_using_ext_id(module, api_instance, result):
    """Fetch datastores for a cluster filtered by parent Storage Container ext_id.

    There is no get-by-id API for datastores; this mirrors the PCIe devices
    pattern of applying an OData filter via C(list_entities).
    """
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = ext_id
    result["cluster_ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating cluster datastores info spec", **result)

    kwargs["_filter"] = "containerExtId eq '{0}'".format(ext_id)

    try:
        resp = list_entities(
            api_instance.list_data_stores_by_cluster_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching datastores for cluster with ext_id: {0}".format(
                cluster_ext_id
            ),
        )

    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        result["response"] = []
        result["msg"] = (
            "Datastore with container_ext_id '{0}' not found on cluster '{1}'".format(
                ext_id, cluster_ext_id
            )
        )
        return
    result["response"] = data


def get_datastores(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating cluster datastores info spec", **result)

    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id

    try:
        resp = list_entities(
            api_instance.list_data_stores_by_cluster_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing datastores for cluster with ext_id: {0}".format(
                cluster_ext_id
            ),
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=False,
        mutually_exclusive=[("ext_id", "filter")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_storage_containers_api_instance(module)
    if module.params.get("ext_id"):
        get_datastore_using_ext_id(module, api_instance, result)
    else:
        get_datastores(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
