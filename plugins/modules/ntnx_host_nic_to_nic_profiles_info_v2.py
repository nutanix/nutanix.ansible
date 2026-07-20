#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_host_nic_to_nic_profiles_info_v2
short_description: Fetch NIC Profile information (and their Host NIC associations) in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about HostNicToNicProfile in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific HostNicToNicProfile.
  - If C(ext_id) is not provided, list multiple HostNicToNicProfile optionally filtered / paginated.
  - The list of Host NICs associated with a NIC Profile is available on each returned NIC Profile via the
    C(host_nic_references) field.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get NIC Profile by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer,
      Project Admin, Super Admin, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer,
      VPC Admin
    - >-
      B(List all NIC Profiles) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer,
      Project Admin, Super Admin, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer,
      VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the NIC Profile.
      - If provided, only the specific NIC Profile is fetched.
      - If not provided, the module lists NIC Profiles.
    type: str
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
- name: Get NIC Profile using ext_id
  nutanix.ncp.ntnx_host_nic_to_nic_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
  register: result
  ignore_errors: true

- name: List all NIC Profiles
  nutanix.ncp.ntnx_host_nic_to_nic_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List NIC Profiles with filter
  nutanix.ncp.ntnx_host_nic_to_nic_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'nic_profile_ansible'"
  register: result
  ignore_errors: true

- name: List NIC Profiles with limit
  nutanix.ncp.ntnx_host_nic_to_nic_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC HostNicToNicProfile info v4 API.
    - It can be a single HostNicToNicProfile if external ID is provided.
    - List of multiple HostNicToNicProfile if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "capability_config": {
          "capability_type": "SRIOV"
      },
      "description": "SR-IOV NIC profile created by Ansible",
      "ext_id": "68e4c68e-1acf-4c05-7792-e062119acb68",
      "host_nic_references": [
          {
              "associated_vm_nic_references": null,
              "compliance_status": "SUCCESS",
              "ext_id": "c1f27ed6-e6dd-4c34-9fda-1acdb1234567",
              "num_v_fs": 8
          }
      ],
      "links": null,
      "metadata": null,
      "name": "nic_profile_ansible",
      "nic_family": "MELLANOX_CX6",
      "tenant_id": null
    }

changed:
  description: Always False for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Status or error message describing the module outcome.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching NIC profiles info"

error:
  description: Error details when an error occurs.
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the NIC Profile.
  type: str
  returned: When external ID is provided
  sample: "68e4c68e-1acf-4c05-7792-e062119acb68"

total_available_results:
  description: The total number of available NIC Profiles in Prism Central.
  type: int
  returned: When all NIC Profiles are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_nic_profiles_api_instance,
)
from ..module_utils.v4.network.helpers import get_nic_profile  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
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


def get_nic_profile_using_ext_id(module, nic_profiles, result):
    ext_id = module.params.get("ext_id")
    resp = get_nic_profile(module, nic_profiles, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_nic_profiles(module, nic_profiles, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating NIC profiles info spec", **result)

    try:
        resp = nic_profiles.list_nic_profiles(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching NIC profiles info",
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
    nic_profiles = get_nic_profiles_api_instance(module)
    if module.params.get("ext_id"):
        get_nic_profile_using_ext_id(module, nic_profiles, result)
    else:
        get_nic_profiles(module, nic_profiles, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
