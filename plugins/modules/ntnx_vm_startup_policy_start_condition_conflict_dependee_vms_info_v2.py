#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_start_condition_conflict_dependee_vms_info_v2
short_description: List dependee VMs of a start-condition conflict of a VM startup policy
version_added: 2.7.0
description:
  - This module allows you to fetch information about VmStartupPolicyStartConditionConflictDependeeVm in Nutanix Prism Central.
  - Lists the dependee VMs of a specific start-condition conflict of a given VM startup policy.
  - A dependee VM is a VM that must be started first and meet its startup conditions before dependent VMs are allowed to power on.
  - Both C(vm_startup_policy_ext_id) and C(start_condition_conflict_ext_id) are required to identify the conflict scope.
  - Optional C(page) and C(limit) can be used to paginate the result set.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List dependee VMs of a start-condition conflict of a VM startup policy) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
    Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  vm_startup_policy_ext_id:
    description:
      - The external ID of the VM startup policy that owns the start-condition conflict.
    type: str
    required: true
  start_condition_conflict_ext_id:
    description:
      - The external ID of the start-condition conflict of the VM startup policy.
    type: str
    required: true
  page:
    description:
      - A URL query parameter that specifies the page number of the result set.
      - It must be a positive integer between 0 and the maximum number of pages that are available for that resource.
      - Any number out of this range might lead to no results.
    type: int
    required: false
  limit:
    description:
      - A URL query parameter that specifies the total number of records returned in the result set.
      - Must be a positive integer between 1 and 100.
      - Any number out of this range will lead to a validation error.
      - If the limit is not provided, a default value of 50 records will be returned in the result set.
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
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all dependee VMs of a start-condition conflict of a VM startup policy
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflict_dependee_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "0b0f9c7e-2b6f-4d61-8d3d-7b8c9e0a1b2c"
    start_condition_conflict_ext_id: "aa11bb22-cc33-dd44-ee55-ff6677889900"
  register: result
  ignore_errors: true

- name: List dependee VMs with pagination
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflict_dependee_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "0b0f9c7e-2b6f-4d61-8d3d-7b8c9e0a1b2c"
    start_condition_conflict_ext_id: "aa11bb22-cc33-dd44-ee55-ff6677889900"
    page: 0
    limit: 10
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmStartupPolicyStartConditionConflictDependeeVm info v4 API.
    - A list of VM references that participate as dependee VMs in the given start-condition conflict.
    - Empty list when no dependee VMs exist for the given policy / conflict.
  returned: always
  type: list
  elements: dict
  sample:
    - ext_id: "b7cd0f79-6dc5-4a53-9d97-2f4d1a5b3c11"
    - ext_id: "9f0e8420-7f2c-42c3-a34a-6b0dcef91d21"

total_available_results:
  description: The total number of dependee VMs available in the given start-condition conflict scope.
  type: int
  returned: always
  sample: 2

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM startup policy start-condition conflict dependee VMs info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
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
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_startup_policies_api_instance,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_startup_policy_ext_id=dict(type="str", required=True),
        start_condition_conflict_ext_id=dict(type="str", required=True),
        page=dict(type="int", required=False),
        limit=dict(type="int", required=False),
    )
    return module_args


def list_dependee_vms(module, api_instance, result):
    """List dependee VMs of a start-condition conflict of a VM startup policy."""
    vm_startup_policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    start_condition_conflict_ext_id = module.params.get(
        "start_condition_conflict_ext_id"
    )

    kwargs = {}
    page = module.params.get("page")
    limit = module.params.get("limit")
    if page is not None:
        kwargs["_page"] = page
    if limit is not None:
        kwargs["_limit"] = limit

    try:
        resp = (
            api_instance.list_vm_startup_policy_start_condition_conflict_dependee_vms(
                vmStartupPolicyExtId=vm_startup_policy_ext_id,
                startConditionConflictExtId=start_condition_conflict_ext_id,
                **kwargs,
            )
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching VM startup policy "
                "start-condition conflict dependee VMs info"
            ),
        )

    total_available_results = 0
    if getattr(resp, "metadata", None) is not None:
        total_available_results = (
            getattr(resp.metadata, "total_available_results", 0) or 0
        )
    result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    api_instance = get_vm_startup_policies_api_instance(module)
    list_dependee_vms(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
