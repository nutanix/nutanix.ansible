#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_gpu_profiles_info_v2
short_description: Fetch physical and virtual GPU profiles info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module fetches the physical and/or virtual GPU profiles available on a
    cluster registered to Nutanix Prism Central.
  - Physical GPU profiles are automatically discovered from the installed GPU hardware
    across registered clusters and are attached to virtual machines in passthrough mode.
  - Virtual GPU profiles define the resource allocation (frame buffer, display heads,
    resolution and licensing) available to virtual machines across registered clusters.
  - If C(profile_type) is C(PHYSICAL), only physical GPU profiles are fetched.
  - If C(profile_type) is C(VIRTUAL), only virtual GPU profiles are fetched.
  - If C(profile_type) is not provided, both physical and virtual GPU profiles are fetched.
  - Supports OData C(filter), C(limit), C(page) and C(orderby) query parameters.
  - This module uses PC v4 APIs based SDKs.
notes:
  - This module talks to Nutanix Prism Central (PC), not to FCVM/Foundation.
  - The GPU profiles are scoped to a single cluster, so C(cluster_ext_id) is required.
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(List physical GPU profiles) / B(List virtual GPU profiles) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, Virtual Machine Admin,
    Virtual Machine Operator, Virtual Machine Viewer.
  - Refer to the SDK API documentation for the authoritative roles/permissions.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster whose GPU profiles are to be fetched.
    type: str
    required: true
  profile_type:
    description:
      - The type of GPU profile to fetch.
      - If not provided, both physical and virtual GPU profiles are fetched.
    type: str
    required: false
    choices:
      - PHYSICAL
      - VIRTUAL
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
- name: List all GPU profiles (physical and virtual) of a cluster
  nutanix.ncp.ntnx_gpu_profiles_info_v2:
    cluster_ext_id: "00065b6f-ec68-302b-185b-ac1f6b6f97e2"
  register: result

- name: List physical GPU profiles of a cluster
  nutanix.ncp.ntnx_gpu_profiles_info_v2:
    cluster_ext_id: "00065b6f-ec68-302b-185b-ac1f6b6f97e2"
    profile_type: PHYSICAL
  register: result

- name: List virtual GPU profiles of a cluster
  nutanix.ncp.ntnx_gpu_profiles_info_v2:
    cluster_ext_id: "00065b6f-ec68-302b-185b-ac1f6b6f97e2"
    profile_type: VIRTUAL
  register: result

- name: List physical GPU profiles with a filter
  nutanix.ncp.ntnx_gpu_profiles_info_v2:
    cluster_ext_id: "00065b6f-ec68-302b-185b-ac1f6b6f97e2"
    profile_type: PHYSICAL
    filter: "physicalGpuConfig/deviceName eq 'Tesla_M10'"
  register: result

- name: List virtual GPU profiles with a limit
  nutanix.ncp.ntnx_gpu_profiles_info_v2:
    cluster_ext_id: "00065b6f-ec68-302b-185b-ac1f6b6f97e2"
    profile_type: VIRTUAL
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix GPU profiles info v4 API. The host is Prism Central (PC).
    - When C(profile_type) is C(PHYSICAL), it is a list of physical GPU profiles.
    - When C(profile_type) is C(VIRTUAL), it is a list of virtual GPU profiles.
    - When C(profile_type) is not provided, it is a dict with C(physical_gpu_profiles)
      and C(virtual_gpu_profiles) keys, each holding a list of profiles.
    - GPU profiles are read-only entities discovered from the cluster hardware.
  returned: always
  type: dict
  sample:
    {
      "physical_gpu_profiles": [
        {
          "allocated_vm_ext_ids": null,
          "ext_id": "cbf788a1-2c1b-4c4e-8f0d-6f6a5b1c9d10",
          "links": null,
          "physical_gpu_config": {
            "assignable": true,
            "device_id": 5053,
            "device_name": "Tesla_M10",
            "frame_buffer_size_bytes": 8589934592,
            "is_in_use": false,
            "mode": "PASSTHROUGH_GRAPHICS",
            "numa_node": 0,
            "sbdf": "0000:08:00.0",
            "type": "PHYSICAL",
            "vendor_name": "NVIDIA"
          },
          "tenant_id": null
        }
      ],
      "virtual_gpu_profiles": [
        {
          "allocated_vm_ext_ids": null,
          "ext_id": "b0f2b3e4-1d2c-4a5b-9c6d-7e8f9a0b1c2d",
          "links": null,
          "tenant_id": null,
          "virtual_gpu_config": {
            "assignable": true,
            "device_id": 5053,
            "device_name": "GRID M10-8Q",
            "frame_buffer_size_bytes": 8589934592,
            "fraction": 1,
            "guest_driver_version": null,
            "is_in_use": false,
            "licenses": ["GRID-Virtual-WS"],
            "max_instances_per_vm": 1,
            "max_resolution": "4096x2160",
            "number_of_virtual_display_heads": 4,
            "numa_node": 0,
            "sbdf": "0000:08:00.0",
            "type": "VIRTUAL",
            "vendor_name": "NVIDIA"
          }
        }
      ]
    }
changed:
  description: This indicates whether the task resulted in any changes. Always False for info modules.
  returned: always
  type: bool
  sample: false
total_available_results:
  description:
    - The total number of available GPU profiles in the cluster.
    - When both physical and virtual profiles are fetched, this is a dict keyed by
      C(physical_gpu_profiles) and C(virtual_gpu_profiles).
  returned: always
  type: dict
  sample:
    {
      "physical_gpu_profiles": 1,
      "virtual_gpu_profiles": 1
    }
msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching physical GPU profiles info"
error:
  description: This field holds the error details, if any, that occurred during the task execution.
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
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    list_physical_gpu_profiles,
    list_virtual_gpu_profiles,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        profile_type=dict(type="str", choices=["PHYSICAL", "VIRTUAL"]),
    )

    return module_args


def _generate_query_kwargs(module, result):
    """Generate the OData query kwargs (_page, _limit, _filter, _orderby) for the list APIs."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating GPU profiles info spec", **result)
    return kwargs


def get_physical_gpu_profiles(module, api_instance, cluster_ext_id, kwargs):
    """Fetch the list of physical GPU profiles for a cluster and the total available count."""
    resp = list_physical_gpu_profiles(module, api_instance, cluster_ext_id, **kwargs)
    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    profiles = resp.get("data")
    if not profiles:
        profiles = []
    return profiles, total_available_results


def get_virtual_gpu_profiles(module, api_instance, cluster_ext_id, kwargs):
    """Fetch the list of virtual GPU profiles for a cluster and the total available count."""
    resp = list_virtual_gpu_profiles(module, api_instance, cluster_ext_id, **kwargs)
    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    profiles = resp.get("data")
    if not profiles:
        profiles = []
    return profiles, total_available_results


def get_gpu_profiles(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    profile_type = module.params.get("profile_type")
    kwargs = _generate_query_kwargs(module, result)

    if profile_type == "PHYSICAL":
        profiles, total = get_physical_gpu_profiles(
            module, api_instance, cluster_ext_id, kwargs
        )
        result["response"] = profiles
        result["total_available_results"] = total
    elif profile_type == "VIRTUAL":
        profiles, total = get_virtual_gpu_profiles(
            module, api_instance, cluster_ext_id, kwargs
        )
        result["response"] = profiles
        result["total_available_results"] = total
    else:
        physical_profiles, physical_total = get_physical_gpu_profiles(
            module, api_instance, cluster_ext_id, kwargs
        )
        virtual_profiles, virtual_total = get_virtual_gpu_profiles(
            module, api_instance, cluster_ext_id, kwargs
        )
        result["response"] = {
            "physical_gpu_profiles": physical_profiles,
            "virtual_gpu_profiles": virtual_profiles,
        }
        result["total_available_results"] = {
            "physical_gpu_profiles": physical_total,
            "virtual_gpu_profiles": virtual_total,
        }


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    get_gpu_profiles(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
