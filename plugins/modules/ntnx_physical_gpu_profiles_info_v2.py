#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_physical_gpu_profiles_info_v2
short_description: Fetch physical GPU profiles info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about physical GPU profiles in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific physical GPU profile.
  - If C(ext_id) is not provided, list multiple physical GPU profiles optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List Physical GPU profiles) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin,
    Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the physical GPU profile.
      - If provided, only the matching profile is returned.
    type: str
    required: false
  cluster_ext_id:
    description:
      - External ID (UUID) of the parent cluster whose physical GPU profiles should be fetched.
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
- name: List all physical GPU profiles on a cluster
  nutanix.ncp.ntnx_physical_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: Get a physical GPU profile by external ID
  nutanix.ncp.ntnx_physical_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "ca1f8f73-88f2-4ded-879e-da623c374bd4"
  register: result
  ignore_errors: true

- name: List physical GPU profiles filtered by GPU type
  nutanix.ncp.ntnx_physical_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    filter: "physicalGpuConfig/type eq Clustermgmt.Config.GpuType'PASSTHROUGH_GRAPHICS'"
  register: result
  ignore_errors: true

- name: List physical GPU profiles with page and limit
  nutanix.ncp.ntnx_physical_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    page: 0
    limit: 5
  register: result
  ignore_errors: true

- name: List physical GPU profiles ordered by device id
  nutanix.ncp.ntnx_physical_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    orderby: "physicalGpuConfig/deviceId asc"
  register: result
  ignore_errors: true

- name: List all physical GPU profiles with fetch_all
  nutanix.ncp.ntnx_physical_gpu_profiles_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC physical GPU profiles info v4 API.
    - It can be a single physical GPU profile if C(ext_id) is provided.
    - List of multiple physical GPU profiles if C(ext_id) is not provided,
      optionally filtered / limited.
  returned: always
  type: dict
  sample:
    {
      "allocated_vm_ext_ids": null,
      "ext_id": "ca1f8f73-88f2-4ded-879e-da623c374bd4",
      "links": null,
      "physical_gpu_config":
        {
          "assignable": 1,
          "device_id": 8757,
          "device_name": "Tesla_M10",
          "frame_buffer_size_bytes": 0,
          "is_in_use": false,
          "mode": "GRAPHICS_MODE",
          "numa_node": null,
          "sbdf": "0000:04:00.0",
          "type": "PASSTHROUGH_GRAPHICS",
          "vendor_name": "NVIDIA",
        },
      "tenant_id": null,
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
  sample: "Api Exception raised while fetching physical GPU profiles info"

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
  description: External ID of the physical GPU profile.
  type: str
  returned: when external ID is provided
  sample: "ca1f8f73-88f2-4ded-879e-da623c374bd4"

total_available_results:
  description: The total number of available physical GPU profiles on the cluster.
  type: int
  returned: when all physical GPU profiles are fetched
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_physical_gpu_profile,
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


def get_physical_gpu_profile_using_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_physical_gpu_profile(module, api_instance, ext_id, cluster_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_physical_gpu_profiles(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating physical GPU profiles info spec", **result
        )

    try:
        resp = list_entities(
            api_instance.list_physical_gpu_profiles,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching physical GPU profiles info",
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
        get_physical_gpu_profile_using_ext_id(module, api_instance, result)
    else:
        get_physical_gpu_profiles(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
