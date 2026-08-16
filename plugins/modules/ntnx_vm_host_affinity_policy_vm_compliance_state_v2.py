#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_host_affinity_policy_vm_compliance_state_v2
short_description: Manage VM-host affinity policy VM compliance state view in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to work with the VM compliance states associated with a VM-host affinity policy in Nutanix Prism Central.
  - The Nutanix v4 VMM API does not expose Create, Update or Delete operations for individual VM compliance state entries;
    compliance is computed automatically by the AHV placement engine based on the parent VM-host affinity policy.
  - When C(state) is C(present) and only C(vm_host_affinity_policy_ext_id) is provided, the module returns the full list of
    compliance state entries currently associated with the policy.
  - When C(state) is C(present) and both C(vm_host_affinity_policy_ext_id) and C(ext_id) are provided, the module returns the
    single compliance state entry that matches C(ext_id) (looked up by paginating the list endpoint).
  - When C(state) is C(absent) the module fails with a clear message because compliance state entries cannot be deleted.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List/Get VM host affinity policy VM compliance states) -
      Required Roles: Super Admin, Prism Admin, Prism Viewer, Virtual Machine Admin, Virtual Machine Viewer, Internal Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - If C(state) is C(present), fetch the compliance state entries for the policy identified by
        C(vm_host_affinity_policy_ext_id) (optionally filtered by C(ext_id)).
      - If C(state) is C(absent), the module fails because compliance state entries cannot be deleted.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  vm_host_affinity_policy_ext_id:
    description:
      - The external ID (UUID) of the parent VM-host affinity policy whose compliance state entries must be fetched.
      - Required for every invocation.
    type: str
    required: true
  ext_id:
    description:
      - The external ID (UUID) of a single VM compliance state entry to fetch from the parent policy.
      - When provided, the module returns just that entry (looked up by iterating the list endpoint).
      - When omitted, the module returns all compliance state entries for the policy.
    type: str
    required: false
  page:
    description:
      - Zero-based page number of the paginated list of compliance state entries to fetch.
      - Only honored when C(ext_id) is not supplied.
    type: int
    required: false
  limit:
    description:
      - Maximum number of compliance state entries to return per page.
      - Must be a positive integer between 1 and 100.
      - Only honored when C(ext_id) is not supplied.
    type: int
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch all VM compliance state entries for a VM-host affinity policy
  nutanix.ncp.ntnx_vm_host_affinity_policy_vm_compliance_state_v2:
    state: present
    vm_host_affinity_policy_ext_id: "d4b6b8a6-9d1b-4a72-8fcc-8a1c93e01234"
  register: result
  ignore_errors: true

- name: Fetch a specific VM compliance state entry by ext_id
  nutanix.ncp.ntnx_vm_host_affinity_policy_vm_compliance_state_v2:
    state: present
    vm_host_affinity_policy_ext_id: "d4b6b8a6-9d1b-4a72-8fcc-8a1c93e01234"
    ext_id: "6c6d0a01-e4f2-4c05-a1b3-8f9e88d5c111"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the fetch operation on VM host affinity policy VM compliance state.
    - When C(ext_id) is provided, the sanitized dict of the matching compliance state entry.
    - When C(ext_id) is not provided, the sanitized list of compliance state entries for the policy.
  returned: always
  type: dict
  sample:
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

task_ext_id:
  description:
    - The external ID of the task.
    - Always C(None) for this module because the underlying API is a synchronous read; kept for parity with other v2 modules.
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the fetched compliance state entry, when C(ext_id) was supplied on input.
  returned: always
  type: str
  sample: "6c6d0a01-e4f2-4c05-a1b3-8f9e88d5c111"

changed:
  description: This indicates whether the task resulted in any changes. Always C(false) because this module only reads state.
  returned: always
  type: bool
  sample: false

skipped:
  description:
    - This indicates whether the task was skipped.
    - Set to C(true) when C(check_mode) is enabled or when no matching entry is found.
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Status or error message describing the outcome of the fetch operation.
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Fetched 3 VM compliance state entries for VM-host affinity policy."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_host_affinity_policies_api_instance,
)
from ..module_utils.v4.vmm.helpers import (  # noqa: E402
    get_vm_host_affinity_policy_vm_compliance_state,
    list_vm_host_affinity_policy_vm_compliance_states,
)

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as virtual_machine_management_sdk  # noqa: E402,F401  # pylint: disable=unused-import
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402,F401  # pylint: disable=unused-import
        mock_sdk as virtual_machine_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        vm_host_affinity_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        page=dict(type="int"),
        limit=dict(type="int"),
    )
    return module_args


def create_VmHostAffinityPolicyVmComplianceState(module, result, api_instance):
    """
    "Create" semantics for a read-only entity: fetch and return compliance
    state entries for the referenced VM-host affinity policy.

    - With only ``vm_host_affinity_policy_ext_id``: return the full list of
      compliance state entries for the policy (optionally paginated).
    - With ``vm_host_affinity_policy_ext_id`` and ``ext_id``: return the
      single matching compliance state entry.
    """
    validate_required_params(module, ["vm_host_affinity_policy_ext_id"])
    vm_host_affinity_policy_ext_id = module.params.get("vm_host_affinity_policy_ext_id")
    ext_id = module.params.get("ext_id")
    page = module.params.get("page")
    limit = module.params.get("limit")

    if module.check_mode:
        result["skipped"] = True
        result["msg"] = (
            "Check mode: would fetch VM compliance state entries for "
            "VM-host affinity policy ext_id={0}".format(vm_host_affinity_policy_ext_id)
        )
        return

    if ext_id:
        entry = get_vm_host_affinity_policy_vm_compliance_state(
            module, api_instance, vm_host_affinity_policy_ext_id, ext_id
        )
        if not entry:
            result["skipped"] = True
            result["msg"] = (
                "No VM compliance state entry found with ext_id '{0}' under "
                "VM-host affinity policy '{1}'.".format(
                    ext_id, vm_host_affinity_policy_ext_id
                )
            )
            result["response"] = None
            return
        result["ext_id"] = ext_id
        result["response"] = strip_internal_attributes(entry.to_dict())
        result["msg"] = (
            "Fetched VM compliance state entry '{0}' for VM-host affinity "
            "policy '{1}'.".format(ext_id, vm_host_affinity_policy_ext_id)
        )
        return

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

    entries = strip_internal_attributes(resp.to_dict()).get("data")
    if not entries:
        entries = []
    result["response"] = entries
    result["msg"] = (
        "Fetched {0} VM compliance state entries for VM-host affinity policy "
        "'{1}'.".format(len(entries), vm_host_affinity_policy_ext_id)
    )


def update_VmHostAffinityPolicyVmComplianceState(module, result, api_instance):
    """
    Update is not supported by the SDK for compliance state entries — they are
    read-only aggregates derived from the parent policy. Falling back to a
    fetch preserves idempotent behavior for existing playbooks that provide
    ``ext_id`` alongside ``state: present``.
    """
    create_VmHostAffinityPolicyVmComplianceState(module, result, api_instance)


def delete_VmHostAffinityPolicyVmComplianceState(module, result, api_instance):
    """
    Delete is not supported for VM compliance state entries: they are
    read-only outputs computed by the placement engine. Fail with a clear
    message so operators know to remove the parent policy instead.
    """
    vm_host_affinity_policy_ext_id = module.params.get("vm_host_affinity_policy_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    result["failed"] = True
    result["msg"] = (
        "state=absent is not supported for VM host affinity policy VM "
        "compliance state entries: they are derived read-only data. Delete "
        "the parent VM-host affinity policy '{0}' instead.".format(
            vm_host_affinity_policy_ext_id
        )
    )
    module.fail_json(**result)


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }
    api_instance = get_vm_host_affinity_policies_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_VmHostAffinityPolicyVmComplianceState(module, result, api_instance)
        else:
            create_VmHostAffinityPolicyVmComplianceState(module, result, api_instance)
    else:
        delete_VmHostAffinityPolicyVmComplianceState(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
