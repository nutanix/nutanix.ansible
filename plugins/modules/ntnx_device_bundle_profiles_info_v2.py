#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_device_bundle_profiles_info_v2
short_description: Fetch device bundle profiles info in Nutanix Prism Central
version_added: "2.7.0"
description:
  - This module allows you to fetch information about device bundle profiles in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific device bundle profile.
  - If C(ext_id) is not provided, list multiple device bundle profiles optionally filtered or paginated.
  - This module uses PC v4 APIs based SDKs
notes:
  - This module talks to Nutanix Prism Central (PC).
  - >-
    A device bundle profile defines which device profiles can be bundled
    together, the interconnects between them and the number of NUMA nodes
    across which the devices are spread.
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get device bundle profile by ext_id) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Self-Service Admin (Deprecated), Super Admin
  - >-
    B(List device bundle profiles) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Self-Service Admin (Deprecated), Super Admin
  - Refer to the SDK API documentation for the authoritative roles/permissions.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the device bundle profile.
      - If provided, fetch details of the specific device bundle profile.
      - If not provided, list all device bundle profiles (with optional filter / limit / order).
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
- name: Get device bundle profile using ext_id
  nutanix.ncp.ntnx_device_bundle_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b2c3d4e5-6789-0abc-def1-234567890bcd"
  register: result
  ignore_errors: true

- name: List all device bundle profiles
  nutanix.ncp.ntnx_device_bundle_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List device bundle profiles with filter
  nutanix.ncp.ntnx_device_bundle_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'test-profile'"
  register: result
  ignore_errors: true

- name: List device bundle profiles with limit
  nutanix.ncp.ntnx_device_bundle_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: List all device bundle profiles with fetch_all
  nutanix.ncp.ntnx_device_bundle_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix device bundle profiles info v4 API.
    - It can be a single device bundle profile if external ID is provided.
    - List of multiple device bundle profiles if external ID is not provided with optional filter, limit, or fetch_all.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00065b6f-ec68-302b-185b-ac1f6b6f97e2"
      ],
      "device_profiles": [
        {
          "profile": {
            "ext_id": "c3d4e5f6-7890-abcd-ef12-34567890cdef"
          }
        }
      ],
      "ext_id": "b2c3d4e5-6789-0abc-def1-234567890bcd",
      "interconnects": [
        {
          "type": "NVLINK"
        }
      ],
      "links": null,
      "name": "device_bundle_profile_1",
      "num_numa_nodes": 2,
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
  sample: "Api Exception raised while fetching device bundle profiles info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the device bundle profile.
  returned: when external ID is provided
  type: str
  sample: "b2c3d4e5-6789-0abc-def1-234567890bcd"

total_available_results:
  description: The total number of available device bundle profiles in PC.
  returned: when all device bundle profiles are fetched
  type: int
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_device_bundles_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_device_bundle_profile,
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
        ext_id=dict(type="str"),
    )

    return module_args


def get_device_bundle_profile_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_device_bundle_profile(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_device_bundle_profiles(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating device bundle profiles info spec", **result
        )

    try:
        resp = list_entities(
            api_instance.list_device_bundle_profiles,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching device bundle profiles info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

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
    api_instance = get_device_bundles_api_instance(module)
    if module.params.get("ext_id"):
        get_device_bundle_profile_using_ext_id(module, api_instance, result)
    else:
        get_device_bundle_profiles(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
