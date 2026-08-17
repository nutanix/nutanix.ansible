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
  - This module allows you to re-enforce a VM-Host Affinity Policy in Nutanix Prism Central.
  - The re-enforce operation re-evaluates the policy's compliance for every VM associated with it
    and attempts to migrate VMs so that they comply with the configured host affinity rules.
  - This is an asynchronous action; if C(wait) is true (default) the module waits for the
    underlying task to complete before returning.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Re-enforce a VM-Host Affinity Policy) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported for this action module.
      - Setting C(state) to C(present) re-enforces the VM-Host Affinity Policy identified by C(ext_id).
    type: str
    required: false
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the VM-Host Affinity Policy to re-enforce.
    type: str
    required: true
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
- name: Re-enforce a VM-Host Affinity Policy
  nutanix.ncp.ntnx_re_enforce_vm_host_affinity_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for re-enforcing a VM-Host Affinity Policy.
    - If C(wait) is true, returns the details of the completed task.
    - If C(wait) is false, returns the initial task submission details.
  returned: always
  type: dict
  sample:
    {
        "cluster_ext_ids": null,
        "completed_time": "2026-07-20T18:45:12.101234+00:00",
        "completion_details": null,
        "created_time": "2026-07-20T18:45:03.001122+00:00",
        "entities_affected": [
            {
                "ext_id": "e2f16b41-0e8e-4a3f-9d33-84a7c95dfae1",
                "rel": "vmm:ahv:config:vm-host-affinity-policy"
            }
        ],
        "error_messages": null,
        "ext_id": "ZXJnb24=:9c1de6c4-0f0d-5aa1-b1c6-3b8f1e0e2f27",
        "is_cancelable": false,
        "last_updated_time": "2026-07-20T18:45:12.101234+00:00",
        "legacy_error_message": null,
        "operation": "ReEnforceVmHostAffinityPolicy",
        "operation_description": "Re-enforce VM-Host Affinity Policy",
        "owned_by": {
            "ext_id": "00000000-0000-0000-0000-000000000000",
            "name": "admin"
        },
        "parent_task": null,
        "progress_percentage": 100,
        "started_time": "2026-07-20T18:45:03.135566+00:00",
        "status": "SUCCEEDED",
        "sub_steps": null,
        "sub_tasks": null,
        "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task submitted for re-enforcing the VM-Host Affinity Policy.
  returned: always
  type: str
  sample: "ZXJnb24=:9c1de6c4-0f0d-5aa1-b1c6-3b8f1e0e2f27"

ext_id:
  description:
    - The external ID of the VM-Host Affinity Policy that was re-enforced.
  returned: always
  type: str
  sample: "e2f16b41-0e8e-4a3f-9d33-84a7c95dfae1"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

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
  sample: false

msg:
  description: Status/error message from the module.
  returned: When there is an error or when running in check mode
  type: str
  sample: "VM-Host Affinity Policy with ext_id 'e2f16b41-0e8e-4a3f-9d33-84a7c95dfae1' will be re-enforced."
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
    import ntnx_vmm_py_client as virtual_machine_management_sdk  # noqa: E402, F401  # pylint: disable=unused-import
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402, F401  # pylint: disable=unused-import
        mock_sdk as virtual_machine_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def re_enforce_vm_host_affinity_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    validate_required_params(module, ["ext_id"])
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "VM-Host Affinity Policy with ext_id '{0}' will be re-enforced.".format(
                ext_id
            )
        )
        return

    policy = get_vm_host_affinity_policy(module, api_instance, ext_id)
    etag = get_etag(policy)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.re_enforce_vm_host_affinity_policy_by_id(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while re-enforcing VM-Host Affinity Policy "
                "with ext_id: {0}".format(ext_id)
            ),
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
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
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
    re_enforce_vm_host_affinity_policy(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
