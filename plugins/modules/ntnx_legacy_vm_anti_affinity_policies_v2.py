#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_legacy_vm_anti_affinity_policies_v2
short_description: Delete legacy VM-VM anti-affinity policies in Nutanix Prism Central.
version_added: "2.7.0"
description:
    - This module allows you to delete legacy VM-VM anti-affinity policies in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Delete Legacy VM Anti-Affinity Policy) -
      Required Roles: Prism Admin, Project Admin, Project Manager,
      Self-Service Admin (deprecated), Super Admin, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - The External ID of the legacy VM-VM anti-affinity policy.
            - Required for deleting the policy.
        type: str
        required: false
    state:
        description:
            - State of the module.
            - If C(state) is C(absent), the module will delete the legacy VM-VM anti-affinity policy.
            - If C(state) is C(present), the module will fail.
        type: str
        choices:
            - present
            - absent
        default: present
    wait:
        description:
            - Wait for the delete task to complete.
        type: bool
        required: false
        default: true
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
- name: Delete a legacy VM-VM anti-affinity policy
  nutanix.ncp.ntnx_legacy_vm_anti_affinity_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00060a2b-5c99-5a52-ebd2-ac1f6b02d3e0"
    state: absent
    wait: true
  register: result

- name: Delete a legacy VM-VM anti-affinity policy without waiting for task
  nutanix.ncp.ntnx_legacy_vm_anti_affinity_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00060a2b-5c99-5a52-ebd2-ac1f6b02d3e0"
    state: absent
    wait: false
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for deleting the legacy VM-VM anti-affinity policy.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    type: dict
    returned: always
    sample:
        {
            "app_name": null,
            "batch_summary": null,
            "cluster_ext_ids": null,
            "completed_time": "2026-11-17T12:05:41.322065+00:00",
            "completion_details": null,
            "created_time": "2026-11-17T12:05:41.267740+00:00",
            "entities_affected": [
                {
                    "ext_id": "00060a2b-5c99-5a52-ebd2-ac1f6b02d3e0",
                    "name": null,
                    "rel": "vmm:ahv:policies:legacy-vm-anti-affinity-policy"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:350f0fd5-097d-4ece-8f44-6e5bfbe2dc08",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-11-17T12:05:41.322065+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 0,
            "operation": "DeleteLegacyVmAntiAffinityPolicyById",
            "operation_description": "Delete the Legacy VM Anti-Affinity Policy",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "project_ext_id": "00000000-0000-0000-0000-000000000000",
            "resource_links": null,
            "root_task": null,
            "started_time": "2026-11-17T12:05:41.277127+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:350f0fd5-097d-4ece-8f44-6e5bfbe2dc08"
ext_id:
    description: The external ID of the legacy VM-VM anti-affinity policy.
    type: str
    returned: always
    sample: "00060a2b-5c99-5a52-ebd2-ac1f6b02d3e0"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
error:
    description: This indicates the error message if any error occurred
    returned: When an error occurs
    type: str
failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "Api Exception raised while deleting legacy VM-VM anti-affinity policy"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_anti_affinity_policies_api_instance,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def delete_legacy_policy(module, result, api_instance):
    """Delete an existing legacy VM-VM anti-affinity policy."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Legacy VM-VM anti-affinity policy with ext_id:{0} will be deleted.".format(
                ext_id
            )
        )
        return

    try:
        resp = api_instance.delete_legacy_vm_anti_affinity_policy_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting legacy VM-VM anti-affinity policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_vm_anti_affinity_policies_api_instance(module)
    state = module.params.get("state")
    if state == "absent":
        delete_legacy_policy(module, result, api_instance)
    else:
        module.fail_json(
            msg="Create and update operations are not supported for legacy VM-VM anti-affinity policies.",
            **result,
        )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
