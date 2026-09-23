#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpc_virtual_switch_mappings_info_v2
short_description: Fetch VPC virtual switch mappings info in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module fetches the VPC virtual switch mappings configuration from Nutanix Prism Central.
  - Fetch all mappings with optional filtering and pagination.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get VPC virtual switch mappings) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options: {}
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
- name: List all VPC virtual switch mappings
  nutanix.ncp.ntnx_vpc_virtual_switch_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List VPC virtual switch mappings with filter
  nutanix.ncp.ntnx_vpc_virtual_switch_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "virtualSwitchUuid eq '11111111-1111-1111-1111-111111111111'"
  register: result

- name: List VPC virtual switch mappings with limit
  nutanix.ncp.ntnx_vpc_virtual_switch_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for fetching VPC virtual switch mappings info.
    - It contains the list of VPC virtual switch mappings.
  returned: always
  type: list
  elements: dict
  sample:
    [
      {
        "ext_id": null,
        "virtual_switch_uuid": "11111111-1111-1111-1111-111111111111",
        "cluster_uuids": ["22222222-2222-2222-2222-222222222222"],
        "is_all_traffic_permitted": true,
        "metadata": null,
        "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error.
  type: str

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  returned: When an error occurs.
  type: str

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available VPC virtual switch mappings in PC.
  type: int
  returned: always
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_vpc_virtual_switch_mappings_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict()
    return module_args


def get_vpc_virtual_switch_mappings(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VPC virtual switch mappings info spec",
            **result,
        )

    try:
        resp = api_instance.list_vpc_virtual_switch_mappings(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VPC virtual switch mappings info",
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
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vpc_virtual_switch_mappings_api_instance(module)
    get_vpc_virtual_switch_mappings(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
