#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_host_gpus_info_v2
short_description: Fetch host GPUs info in Nutanix Prism Central
version_added: "2.7.0"
description:
  - This module allows you to fetch information about host GPUs in Nutanix Prism Central.
  - If C(cluster_ext_id) and C(host_ext_id) are both provided, fetch host GPUs for that host.
  - If only C(cluster_ext_id) is provided, fetch host GPUs for that cluster.
  - If neither is provided, fetch all host GPUs across Prism Central.
  - This module supports pagination and filtering via C(filter), C(limit), C(page), C(orderby) and C(select).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List Host Gpus) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(List Host Gpus By Cluster Id) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(List Host Gpus By Host Id) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The External ID of the cluster to filter host GPUs.
      - If provided without C(host_ext_id), host GPUs are listed for that cluster.
      - If provided together with C(host_ext_id), host GPUs are listed for that specific host.
    type: str
    required: false
  host_ext_id:
    description:
      - The External ID of the host to filter host GPUs.
      - Requires C(cluster_ext_id) when provided.
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
- name: List all host GPUs across Prism Central
  nutanix.ncp.ntnx_cluster_host_gpus_info_v2:
  register: result
  ignore_errors: true

- name: List host GPUs for a specific cluster
  nutanix.ncp.ntnx_cluster_host_gpus_info_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
  register: result
  ignore_errors: true

- name: List host GPUs for a specific host
  nutanix.ncp.ntnx_cluster_host_gpus_info_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
  register: result
  ignore_errors: true

- name: List host GPUs with filter
  nutanix.ncp.ntnx_cluster_host_gpus_info_v2:
    filter: "extId eq '7050d2f7-63eb-4c42-9415-53396a9576f8'"
  register: result
  ignore_errors: true

- name: List host GPUs with limit
  nutanix.ncp.ntnx_cluster_host_gpus_info_v2:
    limit: 1
  register: result
  ignore_errors: true

- name: List all host GPUs with fetch_all
  nutanix.ncp.ntnx_cluster_host_gpus_info_v2:
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC host GPUs info v4 API.
    - List of host GPUs optionally filtered or paginated.
  returned: always
  type: dict
  sample:
    {
        "cluster": {
            "ext_id": "0006361b-6855-3644-7458-2268f8ffb2bd",
            "name": "auto_cluster_prod"
        },
        "config": {
            "device_id": 1234,
            "device_name": "NVIDIA A100",
            "gpu_type": "PASSTHROUGH",
            "vendor_name": "NVIDIA"
        },
        "ext_id": "7050d2f7-63eb-4c42-9415-53396a9576f8",
        "links": null,
        "node_id": "1",
        "node_uuid": "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9",
        "number_of_vgpus_allocated": 2,
        "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching host GPUs info"

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
  description: The total number of available host GPUs matching the query.
  type: int
  returned: When a list call is made.
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
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
        cluster_ext_id=dict(type="str"),
        host_ext_id=dict(type="str"),
    )

    return module_args


def get_host_gpus(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating host GPUs info spec", **result)

    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")

    if cluster_ext_id and host_ext_id:
        try:
            resp = list_entities(
                api_instance.list_host_gpus_by_host_id,
                kwargs=kwargs,
                clusterExtId=cluster_ext_id,
                hostExtId=host_ext_id,
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while fetching host GPUs info",
            )
    elif cluster_ext_id:
        try:
            resp = list_entities(
                api_instance.list_host_gpus_by_cluster_id,
                kwargs=kwargs,
                clusterExtId=cluster_ext_id,
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while fetching host GPUs info",
            )
    elif host_ext_id:
        module.fail_json(msg="host_ext_id requires cluster_ext_id to be set", **result)
    else:
        try:
            resp = list_entities(
                api_instance.list_host_gpus,
                kwargs=kwargs,
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while fetching host GPUs info",
            )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    data = resp.get("data") or []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_clusters_api_instance(module)
    get_host_gpus(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
