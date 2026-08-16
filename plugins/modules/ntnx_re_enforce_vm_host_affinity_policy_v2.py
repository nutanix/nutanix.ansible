#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_re_enforce_vm_host_affinity_policy_v2
short_description: Re-enforce a VM-Host Affinity Policy in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module re-enforces (re-applies) an existing VM-Host Affinity Policy against all
    the VMs currently associated with the policy in Nutanix Prism Central.
  - Re-enforcement re-evaluates the affinity/anti-affinity rules and, if required, live-migrates
    non-compliant VMs to hosts that satisfy the policy so that the policy compliance status
    moves back to compliant.
  - The referenced VM-Host Affinity Policy is identified by its external ID (C(ext_id)) and
    must already exist. This module does not create, update or delete the policy — it only
    triggers the re-enforce action.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the Nutanix IAM permission
    B(Reenforce_VM_Host_Affinity_Policy). The following roles carry this permission
    by default - Prism Admin, Super Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the VM-Host Affinity Policy to re-enforce.
    type: str
    required: true
  state:
    description:
      - Kept for consistency with other v2 modules; only C(present) is meaningful for
        this action module and it triggers a re-enforce.
    type: str
    choices:
      - present
    default: present
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Re-enforce a VM-Host Affinity Policy
  nutanix.ncp.ntnx_re_enforce_vm_host_affinity_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for the VM-Host Affinity Policy re-enforce action.
    - When C(wait) is true, contains the final Prism task details.
    - When C(wait) is false, contains the task reference returned immediately by the API.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": null,
      "completed_time": "2026-07-21T05:16:05.496138+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T05:16:04.313893+00:00",
      "entities_affected": [
        {
          "ext_id": "d8cf7870-6162-474b-4e62-dfa249096ffe",
          "name": "ansible_reenforce_vmhap_mrJbSeKTuMUl",
          "rel": "vmm:ahv:policies:vm-host-affinity-policy"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:adb28ae9-d8c1-50c8-b12f-8a25832a95eb",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T05:16:05.496137+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 0,
      "operation": "VmHostAffinityPolicyEnforce",
      "operation_description": "Enforce VM-Host Affinity Policy",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2026-07-21T05:16:04.322317+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }
task_ext_id:
  description:
    - The external ID of the Prism task that was created for the re-enforce action.
  returned: always
  type: str
  sample: "ZXJnb24=:adb28ae9-d8c1-50c8-b12f-8a25832a95eb"
ext_id:
  description:
    - The external ID of the VM-Host Affinity Policy that was re-enforced.
  returned: always
  type: str
  sample: "d8cf7870-6162-474b-4e62-dfa249096ffe"
changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true
skipped:
  description:
    - This indicates whether the task was skipped (e.g. in check mode).
  returned: when applicable
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
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or in check mode.
  type: str
  sample: "VM-Host Affinity Policy with ext_id:d8cf7870-6162-474b-4e62-dfa249096ffe will be re-enforced."
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
    get_etag,
    get_vm_host_affinity_policies_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_vm_host_affinity_policy  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402  # pylint: disable=unused-import
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402  # pylint: disable=unused-import
        mock_sdk as vmm_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        state=dict(type="str", choices=["present"], default="present"),
    )
    return module_args


def re_enforce_vm_host_affinity_policy(module, result, api_instance):
    """Trigger the re-enforce action on an existing VM-Host Affinity Policy."""
    validate_required_params(module, ["ext_id"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_policy = get_vm_host_affinity_policy(module, api_instance, ext_id)

    if module.check_mode:
        result["msg"] = (
            "VM-Host Affinity Policy with ext_id:{0} will be re-enforced.".format(
                ext_id
            )
        )
        result["response"] = strip_internal_attributes(current_policy.to_dict())
        return

    etag = get_etag(data=current_policy)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    try:
        resp = api_instance.re_enforce_vm_host_affinity_policy_by_id(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while re-enforcing VM-Host Affinity Policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


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
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
        "failed": False,
    }

    api_instance = get_vm_host_affinity_policies_api_instance(module)
    re_enforce_vm_host_affinity_policy(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
