#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_nic_profiles_info_v2
short_description: Fetch NIC profiles info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch NIC profile info or a specific NIC profile in Nutanix Prism Central.
  - If ext_id is provided, fetch a particular NIC profile info using external ID.
  - If ext_id is not provided, fetch multiple NIC profiles info with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external identifier of the NIC profile.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get NIC profile using ext_id
  nutanix.ncp.ntnx_nic_profiles_info_v2:
    ext_id: "ad2c7c4e-4694-4c95-82f4-eadc761a4d17"
  register: result
  ignore_errors: true

- name: List all NIC profiles
  nutanix.ncp.ntnx_nic_profiles_info_v2:
  register: result
  ignore_errors: true

- name: List NIC profiles with filter
  nutanix.ncp.ntnx_nic_profiles_info_v2:
    filter: "name eq 'nic_profile_sriov'"
  register: result
  ignore_errors: true

- name: List NIC profiles with limit
  nutanix.ncp.ntnx_nic_profiles_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for fetching NIC profile info.
    - Specific NIC profile info if External ID is provided.
    - List of multiple NIC profiles info if External ID is not provided.
  returned: always
  type: dict
  sample:
    {
      "capability_config": {
          "capability_type": "SRIOV"
      },
      "description": "NIC profile updated",
      "ext_id": "f98bdee4-fa0d-4b8b-a68e-f020d5a7fcfb",
      "host_nic_references": null,
      "links": null,
      "metadata": {
          "category_ids": null,
          "owner_reference_id": "00000000-0000-0000-0000-000000000000",
          "owner_user_name": "admin",
          "project_name": null,
          "project_reference_id": null
      },
      "name": "nic_profile_ansible_GSPVxekSKefu_updated",
      "nic_family": "15b3:101d",
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
  sample: "Api Exception raised while fetching NIC profiles info"
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
  description: External ID of the NIC profile
  type: str
  returned: when external ID is provided
  sample: f98bdee4-fa0d-4b8b-a68e-f020d5a7fcfb
total_available_results:
  description: The total number of available NIC profiles in PC.
  type: int
  returned: when all NIC profiles are fetched
  sample: 2
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
        module.fail_json(msg="Failed generating NIC profiles info Spec", **result)

    try:
        resp = nic_profiles.list_nic_profiles(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching NIC profiles info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = None
    if resp.get("metadata"):
        total_available_results = resp.get("metadata", {}).get(
            "total_available_results"
        )
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
    result = {"changed": False, "response": None, "error": None}
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
