#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_virtual_gpu_profiles_info_v2
short_description: Fetch virtual GPU profiles info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about virtual GPU profiles in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific virtual GPU profile.
  - If C(ext_id) is not provided, list multiple virtual GPU profiles optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View Cluster Vgpu Profiles) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer,
    Project Manager, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the virtual GPU profile.
      - If provided, only the matching profile is returned.
    type: str
    required: false
  cluster_ext_id:
    description:
      - External ID (UUID) of the parent cluster whose virtual GPU profiles should be fetched.
      - Required for both list and get-by-ext_id flows.
    type: str
    required: true
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
- name: List all virtual GPU profiles on a cluster
  nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: Get a virtual GPU profile by external ID
  nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "0005a1ef-b3aa-4fc4-9c8c-1c8c8f3a0000"
  register: result
  ignore_errors: true

- name: List virtual GPU profiles filtered by device name
  nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    filter: "virtualGpuConfig/deviceName eq 'GRID V100D-8Q'"
  register: result
  ignore_errors: true

- name: List virtual GPU profiles with page and limit
  nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    page: 0
    limit: 5
  register: result
  ignore_errors: true

- name: List virtual GPU profiles ordered by frame buffer size
  nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    orderby: "virtualGpuConfig/frameBufferSizeBytes desc"
  register: result
  ignore_errors: true

- name: List all virtual GPU profiles with fetch_all
  nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC virtual GPU profiles info v4 API.
    - It can be a single virtual GPU profile if C(ext_id) is provided.
    - List of multiple virtual GPU profiles if C(ext_id) is not provided,
      optionally filtered / limited.
  returned: always
  type: dict
  sample:
    {
      "allocated_vm_ext_ids": null,
      "ext_id": "0005a1ef-b3aa-4fc4-9c8c-1c8c8f3a0000",
      "links": null,
      "tenant_id": null,
      "virtual_gpu_config": {
          "assignable": 4,
          "device_id": 8264,
          "device_name": "GRID V100D-8Q",
          "fraction": 8,
          "frame_buffer_size_bytes": 8589934592,
          "guest_driver_version": "470.63.01",
          "is_in_use": false,
          "licenses": ["GRID-Virtual-WS", "GRID-Virtual-WS-Ext"],
          "max_instances_per_vm": 1,
          "max_resolution": "4096x2160",
          "number_of_virtual_display_heads": 4,
          "numa_node": null,
          "sbdf": "0000:af:00.4",
          "type": "VIRTUAL",
          "vendor_name": "NVIDIA"
      }
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
  sample: "Api Exception raised while fetching virtual GPU profiles info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the virtual GPU profile.
  type: str
  returned: when external ID is provided
  sample: "0005a1ef-b3aa-4fc4-9c8c-1c8c8f3a0000"

total_available_results:
  description: The total number of available virtual GPU profiles on the cluster.
  type: int
  returned: when all virtual GPU profiles are fetched
  sample: 4
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_virtual_gpu_profile,
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


def get_virtual_gpu_profile_using_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_virtual_gpu_profile(module, api_instance, ext_id, cluster_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_virtual_gpu_profiles(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating virtual GPU profiles info spec", **result
        )

    try:
        resp = list_entities(
            api_instance.list_virtual_gpu_profiles,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virtual GPU profiles info",
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
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    if module.params.get("ext_id"):
        get_virtual_gpu_profile_using_ext_id(module, api_instance, result)
    else:
        get_virtual_gpu_profiles(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
