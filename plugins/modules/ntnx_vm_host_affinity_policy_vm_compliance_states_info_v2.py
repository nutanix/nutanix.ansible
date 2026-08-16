#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_host_affinity_policy_vm_compliance_states_info_v2
short_description: Fetch VM host affinity policy VM compliance states info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about VmHostAffinityPolicyVmComplianceState in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VmHostAffinityPolicyVmComplianceState.
  - If C(ext_id) is not provided, list multiple VmHostAffinityPolicyVmComplianceState optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List VM host affinity policy VM compliance states) -
      Required Roles: Super Admin, Prism Admin, Prism Viewer, Virtual Machine Admin, Virtual Machine Viewer, Internal Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  vm_host_affinity_policy_ext_id:
    description:
      - The external ID (UUID) of the parent VM-host affinity policy whose compliance state entries must be fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external ID (UUID) of a single VM compliance state entry to fetch from the parent policy.
      - When provided, the module returns the single matching entry (looked up by paginating the list endpoint).
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
- name: List all VM compliance state entries for a VM-host affinity policy
  nutanix.ncp.ntnx_vm_host_affinity_policy_vm_compliance_states_info_v2:
    vm_host_affinity_policy_ext_id: "d4b6b8a6-9d1b-4a72-8fcc-8a1c93e01234"
  register: result
  ignore_errors: true

- name: Fetch a specific VM compliance state entry by ext_id
  nutanix.ncp.ntnx_vm_host_affinity_policy_vm_compliance_states_info_v2:
    vm_host_affinity_policy_ext_id: "d4b6b8a6-9d1b-4a72-8fcc-8a1c93e01234"
    ext_id: "6c6d0a01-e4f2-4c05-a1b3-8f9e88d5c111"
  register: result
  ignore_errors: true

- name: List first page of compliance state entries with a page size of 20
  nutanix.ncp.ntnx_vm_host_affinity_policy_vm_compliance_states_info_v2:
    vm_host_affinity_policy_ext_id: "d4b6b8a6-9d1b-4a72-8fcc-8a1c93e01234"
    page: 0
    limit: 20
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmHostAffinityPolicyVmComplianceState info v4 API.
    - It can be a single VmHostAffinityPolicyVmComplianceState if external ID is provided.
    - List of multiple VmHostAffinityPolicyVmComplianceState if external ID is not provided with optional page/limit.
  returned: always
  type: dict
  sample:
    [
      {
        "associated_categories": [
          {
            "ext_id": "b0d29b0f-9f52-4a95-9c1d-2ce6d9fa9421"
          }
        ],
        "cluster": {
          "ext_id": "0005f6ba-1c31-6a12-0000-000000034521"
        },
        "compliance_status": {
          "non_compliance_reason": {
            "minimum_aos_version_required": "6.1"
          }
        },
        "ext_id": "6c6d0a01-e4f2-4c05-a1b3-8f9e88d5c111",
        "host": {
          "ext_id": "f28e7475-f835-42ef-ac35-ecbc48d5421e"
        },
        "links": null,
        "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always C(false) for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM host affinity policy VM compliance states"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the fetched VM compliance state entry when provided on input.
  type: str
  returned: when external ID is provided
  sample: "6c6d0a01-e4f2-4c05-a1b3-8f9e88d5c111"

total_available_results:
  description: The total number of available VM compliance state entries for the referenced policy.
  type: int
  returned: when all compliance state entries are fetched
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_host_affinity_policies_api_instance,
)
from ..module_utils.v4.vmm.helpers import (  # noqa: E402
    get_vm_host_affinity_policy_vm_compliance_state,
    list_vm_host_affinity_policy_vm_compliance_states,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        vm_host_affinity_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )

    return module_args


def get_vm_host_affinity_policy_vm_compliance_state_using_ext_id(
    module, api_instance, result
):
    vm_host_affinity_policy_ext_id = module.params.get("vm_host_affinity_policy_ext_id")
    ext_id = module.params.get("ext_id")
    entry = get_vm_host_affinity_policy_vm_compliance_state(
        module, api_instance, vm_host_affinity_policy_ext_id, ext_id
    )
    result["ext_id"] = ext_id
    if not entry:
        result["msg"] = (
            "No VM compliance state entry found with ext_id '{0}' under "
            "VM-host affinity policy '{1}'.".format(
                ext_id, vm_host_affinity_policy_ext_id
            )
        )
        result["response"] = None
        return
    result["response"] = strip_internal_attributes(entry.to_dict())


def list_vm_host_affinity_policy_vm_compliance_states_info(
    module, api_instance, result
):
    vm_host_affinity_policy_ext_id = module.params.get("vm_host_affinity_policy_ext_id")
    page = module.params.get("page")
    limit = module.params.get("limit")
    resp = list_vm_host_affinity_policy_vm_compliance_states(
        module,
        api_instance,
        vm_host_affinity_policy_ext_id,
        page=page,
        limit=limit,
    )
    total_available_results = getattr(
        getattr(resp, "metadata", None), "total_available_results", None
    )
    if total_available_results is not None:
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
            ("ext_id", "orderby"),
            ("ext_id", "select"),
            ("ext_id", "limit"),
            ("ext_id", "page"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False, "ext_id": None}
    api_instance = get_vm_host_affinity_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_vm_host_affinity_policy_vm_compliance_state_using_ext_id(
            module, api_instance, result
        )
    else:
        list_vm_host_affinity_policy_vm_compliance_states_info(
            module, api_instance, result
        )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
