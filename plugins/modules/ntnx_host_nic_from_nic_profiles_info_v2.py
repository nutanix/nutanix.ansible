#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_host_nic_from_nic_profiles_info_v2
short_description: Fetch Host NIC from NIC Profiles info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about HostNicFromNicProfile in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific HostNicFromNicProfile.
  - If C(ext_id) is not provided, list multiple HostNicFromNicProfile optionally filtered / paginated.
  - The HostNicFromNicProfile view is exposed through the NIC Profile API, so this
    module wraps C(get_nic_profile_by_id) (singular) and C(list_nic_profiles) (plural),
    surfacing the C(host_nic_references) list from each NIC Profile.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Get NIC Profile by ext_id) -
    Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Super Admin, Virtual Machine Admin
  - >-
    B(List NIC Profiles) -
    Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Super Admin, Virtual Machine Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the NIC Profile whose Host NIC associations should be fetched.
      - Mutually exclusive with C(filter).
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
- name: Get HostNicFromNicProfile info using ext_id of the NIC Profile
  nutanix.ncp.ntnx_host_nic_from_nic_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "d1f6a2f0-1b1d-4b6b-8c1e-1a2b3c4d5e6f"
  register: result
  ignore_errors: true

- name: List all HostNicFromNicProfile entries (all NIC Profiles)
  nutanix.ncp.ntnx_host_nic_from_nic_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List HostNicFromNicProfile with a filter on NIC Profile name
  nutanix.ncp.ntnx_host_nic_from_nic_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'nic_profile_ansible'"
  register: result
  ignore_errors: true

- name: List HostNicFromNicProfile with a limit
  nutanix.ncp.ntnx_host_nic_from_nic_profiles_info_v2:
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
    - The response from the Nutanix PC HostNicFromNicProfile info v4 API.
    - It can be a single HostNicFromNicProfile if external ID is provided.
    - List of multiple HostNicFromNicProfile if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "capability_config": {
          "config_type": "SR_IOV",
          "num_v_fs": 4
      },
      "description": "SR-IOV NIC profile for ansible tests",
      "ext_id": "d1f6a2f0-1b1d-4b6b-8c1e-1a2b3c4d5e6f",
      "host_nic_references": [
          {
              "associated_vm_nic_references": null,
              "compliance_status": "COMPLIANT",
              "ext_id": "a4b5c6d7-e8f9-4a0b-8c1d-2e3f4a5b6c7d",
              "num_v_fs": 4
          }
      ],
      "links": null,
      "metadata": null,
      "name": "nic_profile_ansible",
      "nic_family": "MELLANOX_CONNECTX_6",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching HostNicFromNicProfile info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the NIC Profile whose HostNicFromNicProfile info was fetched
  type: str
  returned: when external ID is provided
  sample: "d1f6a2f0-1b1d-4b6b-8c1e-1a2b3c4d5e6f"

total_available_results:
  description: The total number of available NIC Profiles in PC when listing.
  type: int
  returned: when all HostNicFromNicProfile entries are fetched
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


def get_host_nic_from_nic_profile_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_nic_profile(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_host_nic_from_nic_profiles(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating HostNicFromNicProfile info spec", **result
        )

    try:
        resp = api_instance.list_nic_profiles(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching HostNicFromNicProfile info",
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
    api_instance = get_nic_profiles_api_instance(module)
    if module.params.get("ext_id"):
        get_host_nic_from_nic_profile_using_ext_id(module, api_instance, result)
    else:
        list_host_nic_from_nic_profiles(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
