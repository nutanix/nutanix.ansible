#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vm_host_affinity_policy_re_enforce_v2
short_description: Re-enforce VM-host affinity policy in Nutanix Prism Central
description:
    - This module allows you to re-enforce an existing VM-host affinity policy in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs.
version_added: "2.6.0"
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
options:
    state:
        description:
            - Specify state.
            - If C(state) is set to C(present), VM-host affinity policy re-enforce operation is triggered.
            - No other choices are supported for this module.
        choices:
            - present
        type: str
        default: present
    ext_id:
        description:
            - The external ID of the VM-host affinity policy to re-enforce.
        required: true
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Re-enforce the VM-host affinity policy) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
"""

EXAMPLES = r"""
- name: Re-enforce VM-host affinity policy
  nutanix.ncp.ntnx_vm_host_affinity_policy_re_enforce_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"
    wait: true
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the VM-host affinity policy re-enforce operation.
        - It will be task response if C(wait) is false.
    type: dict
    returned: always
    sample:
        {
            "app_name": null,
            "batch_summary": null,
            "cluster_ext_ids": null,
            "completed_time": "2026-06-18T07:06:20.750802+00:00",
            "completion_details": null,
            "created_time": "2026-06-18T07:06:19.975722+00:00",
            "entities_affected": [
                {
                    "ext_id": "3714b301-a75c-4384-715b-f096c5520cfd",
                    "name": "ansible_AFFwugpxMuBW_host_affinity_test_functional",
                    "rel": "vmm:ahv:policies:vm-host-affinity-policy"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:916a732d-1ca6-5750-9869-196fbd781205",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-06-18T07:06:20.750801+00:00",
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
            "resource_links": null,
            "root_task": null,
            "started_time": "2026-06-18T07:06:19.985487+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }
task_ext_id:
    description: The external ID of the task associated with the operation.
    type: str
    returned: when a task is created
    sample: "98b9dc89-be08-3c56-b554-692b8b676fd2"
ext_id:
    description: The external ID of the VM-host affinity policy.
    type: str
    returned: always
    sample: "98b9dc89-be08-3c56-b554-692b8b676fd2"
changed:
    description: Indicates whether the resource was changed.
    type: bool
    returned: always
    sample: true
error:
    description: The error message if an error occurred.
    type: str
    returned: when an error occurs
msg:
    description: A message describing the result.
    type: str
    returned: on error or check mode
    sample: "VM-host affinity policy with ext_id:98b9dc89-be08-3c56-b554-692b8b676fd2 will be re-enforced."
failed:
    description: Indicates whether the operation failed.
    type: bool
    returned: always
    sample: false
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
    get_etag,
    get_vm_host_affinity_policies_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_vm_host_affinity_policy  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def re_enforce_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "VM-host affinity policy with ext_id:{0} will be re-enforced.".format(
                ext_id
            )
        )
        return

    current_spec = get_vm_host_affinity_policy(module, api_instance, ext_id=ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for re-enforcing VM host affinity policy",
            **result,
        )
    kwargs = {"if_match": etag}

    try:
        resp = api_instance.re_enforce_vm_host_affinity_policy_by_id(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while re-enforcing VM-host affinity policy",
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

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_vm_host_affinity_policies_api_instance(module)
    re_enforce_policy(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
