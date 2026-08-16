#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_start_condition_conflict_v2
short_description: Manage VM startup policy start condition conflicts in Nutanix Prism Central (read-only entity)
version_added: 2.7.0
description:
  - This module represents the C(VmStartupPolicyStartConditionConflict) entity
    surfaced by Prism Central v4 VMM APIs.
  - A B(start condition conflict) is a derived, read-only resource that Prism
    Central computes when two or more VM startup policies enforce
    contradictory start conditions (delay timers or power-state criteria)
    against overlapping category memberships. See
    M(nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflicts_info_v2)
    for read/list access.
  - The upstream v4 VMM SDK (C(ntnx_vmm_py_client.VmStartupPoliciesApi))
    does NOT expose any Create, Update or Delete endpoints for start
    condition conflicts - the platform derives them automatically from the
    parent VM startup policies. This module therefore intentionally does
    NOT perform any mutating API calls; it fails cleanly to make that
    contract explicit to playbook authors.
  - To alter which start condition conflicts exist on the cluster, adjust
    the parent VM startup policies (their groups, categories or start
    conditions) via the VM startup policy management modules; the
    conflicts will be re-computed by Prism Central.
  - This module uses PC v4 APIs based SDKs
notes:
    - This module talks to Prism Central v4 VMM APIs (C(vmm) namespace,
      C(VmStartupPoliciesApi) receiver).
    - >-
      B(Read a Start Condition Conflict) -
      Use M(nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflicts_info_v2)
      with I(vm_startup_policy_ext_id) and (optionally) I(ext_id).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided the
        module reports a clear failure because the SDK does not support
        creating start condition conflicts directly.
      - If C(state) is set to C(present) and C(ext_id) is provided the
        module reports a clear failure because the SDK does not support
        updating start condition conflicts directly.
      - If C(state) is set to C(absent) the module reports a clear failure
        because the SDK does not support deleting start condition
        conflicts directly.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the VM startup policy start condition conflict.
      - Accepted here for parity with other v2 CRUD modules; the SDK does
        not support update or delete on this resource.
    type: str
    required: false
  vm_startup_policy_ext_id:
    description:
      - The external ID of the parent VM startup policy.
      - Start condition conflicts are always scoped to a parent VM startup
        policy so this value identifies the parent when interacting with
        the entity.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Attempt to create a start condition conflict (fails - not supported by SDK)
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflict_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vm_startup_policy_ext_id: "9b7c5c2e-9c9e-4f2d-a9c1-1e2f3a4b5c6d"
  register: result
  ignore_errors: true

- name: Attempt to update a start condition conflict (fails - not supported by SDK)
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflict_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vm_startup_policy_ext_id: "9b7c5c2e-9c9e-4f2d-a9c1-1e2f3a4b5c6d"
    ext_id: "aa11bb22-cc33-dd44-ee55-ff6677889900"
  register: result
  ignore_errors: true

- name: Attempt to delete a start condition conflict (fails - not supported by SDK)
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflict_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    vm_startup_policy_ext_id: "9b7c5c2e-9c9e-4f2d-a9c1-1e2f3a4b5c6d"
    ext_id: "aa11bb22-cc33-dd44-ee55-ff6677889900"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Structured response for the requested operation.
    - Because the upstream SDK does not expose Create, Update or Delete
      for a start condition conflict, the module always fails and this
      field carries the state that would have been sent had a mutating
      operation been supported.
  returned: always
  type: dict
  sample:
    {
      "ext_id": null,
      "vm_startup_policy_ext_id": "9b7c5c2e-9c9e-4f2d-a9c1-1e2f3a4b5c6d",
      "state": "present"
    }

task_ext_id:
  description:
    - The external ID of the async task.
    - Always C(null) for this module because no mutating API is invoked.
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the VM startup policy start condition conflict.
  returned: always
  type: str
  sample: "aa11bb22-cc33-dd44-ee55-ff6677889900"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

skipped:
  description: This indicates whether the task was skipped.
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
  sample: true

msg:
  description:
    - This indicates the message returned by the module.
    - For this read-only entity the message explains that Create, Update
      and Delete are not supported by the SDK, and points the user to
      M(nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflicts_info_v2).
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: >-
    VmStartupPolicyStartConditionConflict is a read-only, derived entity in the
    Nutanix Prism Central v4 VMM API. Use
    ntnx_vm_startup_policy_start_condition_conflicts_info_v2 to fetch details.
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_startup_policies_api_instance,
)

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as virtual_machine_management_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as virtual_machine_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Reference the SDK's StartConditionConflict model so the import above is
# consumed. This entity is read-only so no SDK objects need constructing,
# but keeping a reference here means the module fails cleanly at import
# time if the SDK layout ever changes.
SDK_START_CONDITION_CONFLICT_MODEL = getattr(
    virtual_machine_management_sdk, "StartConditionConflict", None
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


READ_ONLY_MSG = (
    "VmStartupPolicyStartConditionConflict is a read-only, derived entity in the "
    "Nutanix Prism Central v4 VMM API. The SDK does not expose Create, Update or "
    "Delete endpoints for start condition conflicts - Prism Central re-computes "
    "them automatically from the parent VM startup policies. Use "
    "ntnx_vm_startup_policy_start_condition_conflicts_info_v2 to read them, and "
    "adjust the parent VM startup policies to influence which conflicts exist."
)


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        vm_startup_policy_ext_id=dict(type="str"),
    )
    return module_args


def _build_context_payload(module):
    """Return a small dict describing the invocation for RETURN.response."""
    return {
        "ext_id": module.params.get("ext_id"),
        "vm_startup_policy_ext_id": module.params.get("vm_startup_policy_ext_id"),
        "state": module.params.get("state"),
    }


def create_VmStartupPolicyStartConditionConflict(module, result, api_instance):
    """Create is intentionally unsupported: no matching SDK endpoint exists."""
    result["response"] = _build_context_payload(module)
    result["failed"] = True
    module.fail_json(msg=READ_ONLY_MSG, **result)


def update_VmStartupPolicyStartConditionConflict(module, result, api_instance):
    """Update is intentionally unsupported: no matching SDK endpoint exists.

    We deliberately do NOT attempt to fetch the parent/child pair from the API
    first - a fetch that fails (for example on a non-existent ext_id) would
    obscure the real contract of this module: the SDK does not expose an
    update endpoint for start condition conflicts, so we must always fail
    with the same read-only message regardless of whether the referenced
    entity happens to exist on the target Prism Central.
    """
    result["ext_id"] = module.params.get("ext_id")
    result["response"] = _build_context_payload(module)
    result["failed"] = True
    module.fail_json(msg=READ_ONLY_MSG, **result)


def delete_VmStartupPolicyStartConditionConflict(module, result, api_instance):
    """Delete is intentionally unsupported: no matching SDK endpoint exists.

    Same rationale as C(update_VmStartupPolicyStartConditionConflict): we
    never call the API here because there is no matching Delete SDK
    endpoint, and issuing a probe Get would only muddle the deterministic
    read-only error message this stub is required to surface.
    """
    result["ext_id"] = module.params.get("ext_id")
    result["response"] = _build_context_payload(module)
    result["failed"] = True
    module.fail_json(msg=READ_ONLY_MSG, **result)


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id", "vm_startup_policy_ext_id")),
        ],
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
    api_instance = get_vm_startup_policies_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_VmStartupPolicyStartConditionConflict(module, result, api_instance)
        else:
            create_VmStartupPolicyStartConditionConflict(module, result, api_instance)
    else:
        delete_VmStartupPolicyStartConditionConflict(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
