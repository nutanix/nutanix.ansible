#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_network_mappings_info_v2
short_description: Fetch Recovery Plan Network Mappings info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about NetworkMapping in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific NetworkMapping.
  - If C(ext_id) is not provided, list multiple NetworkMapping optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs (ntnx_datapolicies_py_client).
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Network Mapping by ext_id) -
      Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - >-
      B(List Network Mappings) -
      Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  ext_id:
    description:
      - The external ID of the network mapping.
      - When provided, a single network mapping is fetched.
    type: str
    required: false
  recovery_plan_ext_id:
    description:
      - External identifier of the parent recovery plan whose network
        mappings must be fetched.
      - Required for both get-by-id and list operations.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch a specific network mapping by ext_id
  nutanix.ncp.ntnx_network_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "b0e1a7b2-8c31-4a41-9f2c-3f2f0f76de11"
    ext_id: "1cadd9f5-52fa-4ad9-9dcb-11ab8b6c3d7f"
  register: nm_info

- name: List all network mappings under a recovery plan
  nutanix.ncp.ntnx_network_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "b0e1a7b2-8c31-4a41-9f2c-3f2f0f76de11"
  register: nm_list

- name: List network mappings with limit
  nutanix.ncp.ntnx_network_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "b0e1a7b2-8c31-4a41-9f2c-3f2f0f76de11"
    limit: 1
  register: nm_limited
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC NetworkMapping info v4 API.
    - It can be a single NetworkMapping if external ID is provided.
    - List of multiple NetworkMapping if external ID is not provided, with
      optional pagination, filter, order-by and select query parameters.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "1cadd9f5-52fa-4ad9-9dcb-11ab8b6c3d7f",
      "is_ip_mapping_enabled": false,
      "links": null,
      "primary_network": {
        "ip_config": null,
        "subnet_ext_id": "5a6f8f2c-3f2b-4a1c-9c14-2d17b3e6b555",
        "subnet_name": null,
        "vpc": null
      },
      "primary_test_network": null,
      "recovery_network": {
        "ip_config": null,
        "subnet_ext_id": "6b7e9d3c-4a1f-5b12-8e15-3d17b3e6c666",
        "subnet_name": null,
        "vpc": null
      },
      "recovery_test_network": null,
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
  sample: "Api Exception raised while fetching network mappings info"

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
  description: External ID of the network mapping
  type: str
  returned: when external ID is provided
  sample: "1cadd9f5-52fa-4ad9-9dcb-11ab8b6c3d7f"

total_available_results:
  description: The total number of network mappings available under the recovery plan.
  type: int
  returned: when all network mappings are fetched (list operation)
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_recovery_plans_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_network_mapping  # noqa: E402
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
        recovery_plan_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_network_mapping_using_ext_id(module, api_instance, result):
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_network_mapping(module, api_instance, recovery_plan_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_network_mappings(module, api_instance, result):
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating network mappings info spec", **result)

    try:
        resp = api_instance.list_network_mappings(
            recoveryPlanExtId=recovery_plan_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network mappings info",
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
    api_instance = get_recovery_plans_api_instance(module)
    if module.params.get("ext_id"):
        get_network_mapping_using_ext_id(module, api_instance, result)
    else:
        list_network_mappings(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
