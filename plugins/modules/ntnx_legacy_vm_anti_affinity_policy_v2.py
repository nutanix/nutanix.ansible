#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_legacy_vm_anti_affinity_policy_v2
short_description: Delete legacy VM-VM anti-affinity policies in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to manage the lifecycle of a legacy VM-VM anti-affinity policy in Nutanix Prism Central.
  - Legacy VM-VM anti-affinity policies were originally configured on Prism Element using VM groups (via acli or Prism Element APIs).
  - The Prism Central v4 API exposes these legacy policies as read-only entities that can only be deleted to make room for the
    modern category-based VM-VM anti-affinity policies.
  - This module therefore supports the delete operation only. Attempting create (C(state=present) without C(ext_id))
    or update (C(state=present) with C(ext_id)) will fail with a descriptive error, because the underlying v4 SDK does
    not expose create or update endpoints for legacy policies.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Delete a Legacy VM-VM Anti-Affinity Policy) -
      Required Roles: Prism Admin, Super Admin, Cluster Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=virtual_machine_management)"
options:
  state:
    description:
      - If C(state) is set to C(absent) and C(ext_id) is provided then the legacy VM-VM anti-affinity policy will be deleted.
      - C(state=present) is not supported by the underlying v4 API for legacy policies and will fail with a descriptive error.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the legacy VM-VM anti-affinity policy.
      - Required for the delete operation.
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
- name: Delete legacy VM-VM anti-affinity policy
  nutanix.ncp.ntnx_legacy_vm_anti_affinity_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "3f6a1c5c-4b7f-4a5f-8e2e-6a1e5b9c2d3f"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for deleting a legacy VM-VM anti-affinity policy.
    - When C(wait) is C(true), it contains the completed delete task details.
    - When C(wait) is C(false), it contains the task reference returned by the API.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": null,
      "completed_time": "2026-07-21T09:12:45.000000+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T09:12:43.000000+00:00",
      "entities_affected": [
          {
              "ext_id": "3f6a1c5c-4b7f-4a5f-8e2e-6a1e5b9c2d3f",
              "name": null,
              "rel": "vmm:ahv:policies:legacy-vm-anti-affinity-policy"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T09:12:45.000000+00:00",
      "legacy_error_message": null,
      "operation": "DeleteLegacyVmAntiAffinityPolicy",
      "operation_description": "Delete legacy VM-VM anti-affinity policy",
      "owned_by": null,
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2026-07-21T09:12:43.000000+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the asynchronous task returned by the delete API.
  returned: always
  type: str
  sample: "ZXJnb24=:1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"

ext_id:
  description:
    - The external ID of the legacy VM-VM anti-affinity policy that was acted upon.
  returned: always
  type: str
  sample: "3f6a1c5c-4b7f-4a5f-8e2e-6a1e5b9c2d3f"

changed:
  description: Whether the operation resulted in any changes on the target Prism Central.
  returned: always
  type: bool
  sample: true

skipped:
  description: Whether the operation was skipped (for example, when running in check mode).
  returned: always
  type: bool
  sample: false

error:
  description: The error message, if any, when the operation failed.
  returned: When an error occurs
  type: str

failed:
  description: Whether the module invocation failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Contextual status or error message emitted by the module.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Legacy VM-VM anti-affinity policy with ext_id: 3f6a1c5c-4b7f-4a5f-8e2e-6a1e5b9c2d3f will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_anti_affinity_policies_api_instance,
)

# The SDK is not referenced directly in this module (no spec object building is
# required for a delete-only entity), but a guarded import is still kept to
# match the convention used by the other v4 modules in this collection and to
# produce a clean ``missing_required_lib`` failure at run time if the wheel is
# absent. The imports below are intentionally unused at import time.
SDK_IMP_ERROR = None
try:
    # pylint: disable=unused-import
    import ntnx_vmm_py_client as virtual_machine_management_sdk  # noqa: F401,E402
except ImportError:

    # pylint: disable=unused-import
    from ..module_utils.v4.sdk_mock import (  # noqa: F401,E402
        mock_sdk as virtual_machine_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def create_LegacyVmAntiAffinityPolicy(module, result, api_instance):
    """Create is not supported for legacy VM-VM anti-affinity policies.

    The v4 SDK does not expose a create endpoint for legacy policies — they
    are strictly read-only/delete-only carry-overs from PE. Fail loudly with
    a descriptive message so operators are directed to the modern
    category-based VM-VM anti-affinity policy APIs instead.
    """
    module.fail_json(
        msg=(
            "Create is not supported for legacy VM-VM anti-affinity policies. "
            "The Nutanix v4 VMM API only allows listing and deleting legacy "
            "policies. Use the modern VM-VM anti-affinity policy APIs to "
            "create new anti-affinity rules."
        ),
        **result,
    )


def update_LegacyVmAntiAffinityPolicy(module, result, api_instance):
    """Update is not supported for legacy VM-VM anti-affinity policies.

    The v4 SDK does not expose an update endpoint for legacy policies. Fail
    loudly with a descriptive message rather than silently no-op'ing.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    module.fail_json(
        msg=(
            "Update is not supported for legacy VM-VM anti-affinity policies "
            "(ext_id: {0}). The Nutanix v4 VMM API only allows listing and "
            "deleting legacy policies. Delete the legacy policy and re-create "
            "the equivalent rule using the modern VM-VM anti-affinity policy "
            "APIs instead.".format(ext_id)
        ),
        **result,
    )


def delete_LegacyVmAntiAffinityPolicy(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["ext_id"])

    if module.check_mode:
        result["msg"] = (
            "Legacy VM-VM anti-affinity policy with ext_id: "
            "{0} will be deleted.".format(ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.delete_legacy_vm_anti_affinity_policy_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while deleting legacy VM-VM "
                "anti-affinity policy with ext_id: {0}".format(ext_id)
            ),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
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
    }
    api_instance = get_vm_anti_affinity_policies_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_LegacyVmAntiAffinityPolicy(module, result, api_instance)
        else:
            create_LegacyVmAntiAffinityPolicy(module, result, api_instance)
    else:
        delete_LegacyVmAntiAffinityPolicy(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
