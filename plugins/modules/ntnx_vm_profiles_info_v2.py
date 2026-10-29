#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_profiles_info_v2
short_description: Fetch information about VM profiles in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Fetch a VM profile by external ID or list all VM profiles with optional filtering and pagination.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get a Virtual Machine Profile) -
      Required Roles: Super Admin, Virtual Machine Admin, Virtual Machine Operator
    - >-
      B(List Virtual Machine Profiles) -
      Required Roles: Super Admin, Virtual Machine Admin, Virtual Machine Operator
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - The external ID (UUID) of the VM profile.
            - If provided, fetches a single VM profile by its external ID.
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
- name: Get a VM profile by ext_id
  nutanix.ncp.ntnx_vm_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11"
  register: result

- name: List all VM profiles
  nutanix.ncp.ntnx_vm_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List VM profiles with filter
  nutanix.ncp.ntnx_vm_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'test-vm-profile'"
  register: result

- name: List VM profiles with limit
  nutanix.ncp.ntnx_vm_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: List all VM profiles with fetch_all
  nutanix.ncp.ntnx_vm_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching VM profile information.
        - One VM profile if C(ext_id) is provided.
        - List of VM profiles if C(ext_id) is not provided.
    type: dict
    returned: always
    sample:
        {
            "description": "VM profile for GPU workloads",
            "ext_id": "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11",
            "links": null,
            "name": "ai.xlarge.h100.8gpu",
            "project_ext_id": "26ff200c-e24c-47f7-809b-00a571fe7ecc",
            "shared_with_projects": [
                "e11759c8-f368-4bf4-99d8-e3e128891c98"
            ],
            "tenant_id": null,
            "update_time": "2027-01-12T07:13:52.055646+00:00",
            "updated_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000"
            },
            "vm_configuration": {
                "memory_size_bytes": 68719476736,
                "nics": [
                    {
                        "backing_info": {
                            "nic_profile_reference": {
                                "ext_id": "8f897185-e5ee-46ac-82ad-e8945f8687f4"
                            }
                        },
                        "ext_id": "5d0c9a4b-7a43-4d0e-9a2e-0d1b9f6a3c21"
                    }
                ],
                "num_cores": 8
            }
        }
ext_id:
    description: The external ID of the VM profile.
    type: str
    returned: when C(ext_id) is provided
    sample: "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: false
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error
    sample: "Failed generating VM profiles info spec"
total_available_results:
    description: The total number of available VM profiles in PC.
    type: int
    returned: when C(ext_id) is not provided
    sample: 10
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_profile_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_vm_profile  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_vm_profile_using_ext_id(module, api_instance, result):
    """Fetch a single VM profile by ext_id."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_vm_profile(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_vm_profiles(module, api_instance, result):
    """List VM profiles with pagination support."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VM profiles info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_vm_profiles,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM profiles info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
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
    api_instance = get_vm_profile_api_instance(module)
    if module.params.get("ext_id"):
        get_vm_profile_using_ext_id(module, api_instance, result)
    else:
        get_vm_profiles(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
