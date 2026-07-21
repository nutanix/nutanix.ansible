#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_start_condition_conflicts_info_v2
short_description: Fetch VM startup policy start condition conflicts info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about VmStartupPolicyStartConditionConflict in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VmStartupPolicyStartConditionConflict.
  - If C(ext_id) is not provided, list multiple VmStartupPolicyStartConditionConflict of the specified VM startup policy
    optionally paginated using C(page) and C(limit).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get VM startup policy start condition conflict by ext_id) -
    Required Roles: Prism Admin, Prism Viewer, Project Admin, Self-Service Admin, Super Admin
  - >-
    B(List VM startup policy start condition conflicts) -
    Required Roles: Prism Admin, Prism Viewer, Project Admin, Self-Service Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  vm_startup_policy_ext_id:
    description:
      - The external ID of the parent VM startup policy that owns the start condition conflict.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the start condition conflict of a VM startup policy.
      - When provided, a single conflict is fetched using the get-by-id API.
      - When omitted, the list API is used to return all start condition conflicts of the specified
        VM startup policy.
    type: str
    required: false
  page:
    description:
      - Zero-based page number of the result set for the list operation.
      - Only used when C(ext_id) is not provided.
    type: int
    required: false
  limit:
    description:
      - Maximum number of records to return in the result set for the list operation.
      - Must be a positive integer between 1 and 100 as enforced by the API.
      - Only used when C(ext_id) is not provided.
    type: int
    required: false
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all start condition conflicts of a VM startup policy
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflicts_info_v2:
    vm_startup_policy_ext_id: "d1d1c1b1-1111-1111-1111-000000000001"
  register: all_conflicts

- name: List start condition conflicts with pagination
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflicts_info_v2:
    vm_startup_policy_ext_id: "d1d1c1b1-1111-1111-1111-000000000001"
    page: 0
    limit: 5
  register: page_of_conflicts

- name: Fetch a specific start condition conflict by ext_id
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflicts_info_v2:
    vm_startup_policy_ext_id: "d1d1c1b1-1111-1111-1111-000000000001"
    ext_id: "f2f2f2f2-2222-2222-2222-000000000002"
  register: single_conflict
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmStartupPolicyStartConditionConflict info v4 API.
    - It can be a single VmStartupPolicyStartConditionConflict if external ID is provided.
    - List of multiple VmStartupPolicyStartConditionConflict if external ID is not provided with optional page or limit.
  returned: always
  type: dict
  sample:
    {
      "conflicting_policy": {
          "ext_id": "e5e5e5e5-3333-3333-3333-000000000003",
          "name": "policyB"
      },
      "conflicting_start_condition": {
          "delay_duration_secs": 60,
          "power_state_criteria": "POWER_ON"
      },
      "dependee_category": {
          "ext_id": "aaaa1111-2222-3333-4444-555555555555"
      },
      "dependee_vms_associated_categories": [
          {"ext_id": "aaaa1111-2222-3333-4444-555555555555"}
      ],
      "dependent_category": {
          "ext_id": "bbbb1111-2222-3333-4444-555555555555"
      },
      "dependent_vms_associated_categories": [
          {"ext_id": "bbbb1111-2222-3333-4444-555555555555"}
      ],
      "ext_id": "f2f2f2f2-2222-2222-2222-000000000002",
      "links": null,
      "start_condition": {
          "delay_duration_secs": 300,
          "power_state_criteria": "GUEST_BOOTUP"
      },
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the start condition conflict.
  returned: when external ID is provided
  type: str
  sample: "f2f2f2f2-2222-2222-2222-000000000002"

vm_startup_policy_ext_id:
  description: External ID of the parent VM startup policy.
  returned: always
  type: str
  sample: "d1d1c1b1-1111-1111-1111-000000000001"

total_available_results:
  description: The total number of available start condition conflicts for the parent VM startup policy.
  returned: when the list operation succeeds
  type: int
  sample: 3

msg:
  description: Human readable message describing errors or edge cases.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM startup policy start condition conflicts info"

error:
  description: Details about any error that occurred during the task execution.
  returned: when an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_startup_policies_api_instance,
)
from ..module_utils.v4.vmm.helpers import (  # noqa: E402
    get_vm_startup_policy_start_condition_conflict,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        vm_startup_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
        page=dict(type="int", required=False),
        limit=dict(type="int", required=False),
    )

    return module_args


def get_start_condition_conflict_by_ext_id(module, api_instance, result):
    vm_startup_policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_vm_startup_policy_start_condition_conflict(
        module, api_instance, vm_startup_policy_ext_id, ext_id
    )
    result["ext_id"] = ext_id
    result["vm_startup_policy_ext_id"] = vm_startup_policy_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_start_condition_conflicts(module, api_instance, result):
    vm_startup_policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    result["vm_startup_policy_ext_id"] = vm_startup_policy_ext_id

    kwargs = {}
    if module.params.get("page") is not None:
        kwargs["_page"] = module.params.get("page")
    if module.params.get("limit") is not None:
        kwargs["_limit"] = module.params.get("limit")

    try:
        resp = api_instance.list_vm_startup_policy_start_condition_conflicts(
            vmStartupPolicyExtId=vm_startup_policy_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching VM startup policy "
                "start condition conflicts info"
            ),
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        skip_info_args=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_vm_startup_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_start_condition_conflict_by_ext_id(module, api_instance, result)
    else:
        list_start_condition_conflicts(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
