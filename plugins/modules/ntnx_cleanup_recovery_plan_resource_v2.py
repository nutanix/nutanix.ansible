#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cleanup_recovery_plan_resource_v2
short_description: Cleanup resources on the last Recovery Plan execution
version_added: 2.5.0
description:
  - This module allows you to trigger cleanup of resources that were created
    (recovered VMs, volume groups, subnets, etc.) as part of the last execution
    of a Recovery Plan on the target Prism Central.
  - Use this after a Test Failover or a partial / failed failover to remove
    leftover recovered entities from the target Availability Zone.
  - The action is idempotent from the API perspective - if there are no
    leftover resources to clean up, the underlying task simply completes
    without changes.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to
    the user performing the operation.
  - >-
    B(Cleanup Recovery Plan resources) -
    Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported for this action module. Providing any
        other value will cause the module to fail.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external identifier of the recovery plan whose last-execution
        resources need to be cleaned up.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Cleanup resources from the last execution of a Recovery Plan
  nutanix.ncp.ntnx_cleanup_recovery_plan_resource_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for the cleanup recovery plan resources action.
    - When C(wait) is true, this is the completed task details.
    - When C(wait) is false, this is the created task reference.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": null,
      "completed_time": "2026-07-21T10:18:39.599580+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T10:17:47.283752+00:00",
      "entities_affected": [
        {
          "ext_id": "1ca2963d-77b6-453a-ae23-2c19e7a954a3",
          "rel": "dataprotection:config:recovery-plan"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:c3f6cc70-fda6-4133-a97c-58802d58186a",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T10:18:39.599579+00:00",
      "legacy_error_message": null,
      "operation": "CleanupRecoveryPlanResources",
      "operation_description": "Cleanup Recovery Plan Resources",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-21T10:17:47.300538+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task that performed the cleanup.
  returned: always
  type: str
  sample: "ZXJnb24=:c3f6cc70-fda6-4133-a97c-58802d58186a"

ext_id:
  description:
    - The external ID of the recovery plan the action was invoked on.
  returned: always
  type: str
  sample: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"

changed:
  description: Indicates whether the action resulted in any changes.
  returned: always
  type: bool
  sample: true

error:
  description: The error message if an error occurred.
  returned: when an error occurs
  type: str
  sample: null

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Status or error message returned by the module.
  returned: When there is an error or check_mode is used
  type: str
  sample: "Api Exception raised while cleaning up recovery plan resources"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_plan_actions_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_dataprotection_py_client as data_protection_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_protection_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Preserve a reference to the SDK module so importers / linters see the
# import as used - the actual API surface used by this module is exposed
# through get_recovery_plan_actions_api_instance above.
RecoveryPlanActionsApi = getattr(data_protection_sdk, "RecoveryPlanActionsApi", None)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def cleanup_recovery_plan_resources(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Cleanup of resources for recovery plan with ext_id:{0} will be triggered.".format(
                ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.cleanup_recovery_plan_resources(recoveryPlanExtId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while cleaning up recovery plan resources",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_dataprotection_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_recovery_plan_actions_api_instance(module)
    cleanup_recovery_plan_resources(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
