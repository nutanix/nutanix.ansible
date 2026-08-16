#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_virtual_gpu_profiles_info_v2
short_description: Fetch Virtual GPU Profile info from a Nutanix Prism Central managed cluster
version_added: 2.7.0
description:
  - This module allows you to fetch information about VirtualGpuProfile in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VirtualGpuProfile.
  - If C(ext_id) is not provided, list multiple VirtualGpuProfile optionally filtered / paginated.
  - Virtual GPU profiles describe functionally equivalent vGPU devices (frame buffer size,
    number of virtual display heads, max resolution, licenses, etc.) that can be assigned to
    virtual machines. They are discovered from the AHV Acropolis Device Manager (ADM) and
    aggregated at Prism Central per cluster.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(List Virtual GPU Profiles) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin,
      Prism Viewer, Project Admin, Super Admin, Virtual Machine Admin, Virtual Machine
      Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - External ID (UUID) of the Prism Element cluster whose Virtual GPU profiles are
        being fetched.
      - This maps to the C(clusterExtId) path parameter of the underlying V4 API
        C(GET /api/clustermgmt/v4.2/config/clusters/{clusterExtId}/virtual-gpu-profiles).
    type: str
    required: true
  ext_id:
    description:
      - External ID of a Virtual GPU profile to fetch.
      - When provided, the module returns a single matching profile from the cluster.
      - When not provided, the module lists all profiles for the given cluster.
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
- name: List all Virtual GPU profiles on a cluster
  nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: Fetch a Virtual GPU profile by external ID
  nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "0005a1ef-b3aa-4fc4-9c8c-1c8c8f3a0000"
  register: result
  ignore_errors: true

- name: List Virtual GPU profiles with a limit
  nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    limit: 5
  register: result
  ignore_errors: true

- name: List Virtual GPU profiles using a filter (OData)
  nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    filter: "virtualGpuConfig/deviceName eq 'GRID V100D-8Q'"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VirtualGpuProfile info v4 API.
    - It can be a single VirtualGpuProfile if external ID is provided.
    - List of multiple VirtualGpuProfile if external ID is not provided
      with optional filter or limit.
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

ext_id:
  description:
    - The external ID of the Virtual GPU profile.
  returned: when external ID is provided
  type: str
  sample: "0005a1ef-b3aa-4fc4-9c8c-1c8c8f3a0000"

total_available_results:
  description: The total number of available Virtual GPU profiles on the cluster.
  type: int
  returned: when all profiles are fetched (no ext_id given)
  sample: 4

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching Virtual GPU profiles info"

error:
  description: The error message if any error occurred.
  type: str
  returned: When an error occurs

failed:
  description: This indicates whether the task failed.
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
    get_virtual_gpu_profile,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
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
    resp = get_virtual_gpu_profile(module, api_instance, cluster_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_virtual_gpu_profiles(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Virtual GPU profiles info spec", **result
        )

    try:
        resp = api_instance.list_virtual_gpu_profiles(
            clusterExtId=module.params.get("cluster_ext_id"), **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Virtual GPU profiles info",
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
