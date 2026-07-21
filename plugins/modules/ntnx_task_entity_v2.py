#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_task_entity_v2
short_description: Cancel an ongoing task in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module performs actions on a Nutanix Prism Central TaskEntity.
  - Currently the only supported action is cancelling an ongoing task via the
    Prism v4 Tasks API (POST /api/prism/v4.3/config/tasks/{taskExtId}/$actions/cancel).
  - Cancellation is issued only if the task is cancellable (C(is_cancelable=true))
    and it may be delayed until the platform reaches a safe abort point.
  - Cancellation requests are idempotent from the server's point of view; issuing the
    same request multiple times will not fail.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Cancel a task) -
      Required Roles: Intelligent Ops Admin, NCM Admin, Prism Admin, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  state:
    description:
      - Only C(present) is supported. Setting C(state=present) will trigger the cancel action
        on the task identified by C(task_ext_id).
      - This module does not support C(state=absent) because the underlying Prism v4 Tasks
        API only exposes a cancel action for a task and does not support deletion of task
        records.
    type: str
    required: false
    choices:
      - present
    default: present
  task_ext_id:
    description:
      - The external ID of the task to cancel.
      - It consists of a base64-encoded service prefix and a UUID separated by C(:).
        For example C(ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1).
      - The C(legacy) prefix can be used with a task UUID provided by previous API families.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Cancel an ongoing task
  nutanix.ncp.ntnx_task_entity_v2:
    state: present
    task_ext_id: "ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the cancel task action.
    - It contains the C(AppMessage) returned by the Prism v4 Tasks cancel API
      including the cancellation status message, code, severity, and locale.
  returned: always
  type: dict
  sample:
    {
      "arguments_map": null,
      "code": "TSKS-20901",
      "error_group": "TASK_CANCELLATION_SUCCESS",
      "locale": "en_US",
      "message": "Task cancellation issued successfully as requested",
      "severity": "INFO"
    }

task_ext_id:
  description:
    - The external ID of the task that was targeted by the cancel action.
  returned: always
  type: str
  sample: "ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1"

ext_id:
  description:
    - Alias for C(task_ext_id) to match the return contract of other v2 modules.
  returned: always
  type: str
  sample: "ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
  returned: when the operation is skipped (currently unused; cancellation is idempotent server-side)
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
  description: This indicates the message returned by the module.
  returned: When there is an error or in check mode
  type: str
  sample: "Api Exception raised while cancelling task with ext_id:ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import get_tasks_api_instance  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Re-exported so downstream helpers that share this file can reach the SDK
# through a single import (and so pylint sees the fallback import as used).
PRISM_SDK = prism_sdk


def get_module_spec():
    module_args = dict(
        state=dict(type="str", choices=["present"], default="present"),
        task_ext_id=dict(type="str", required=True),
    )
    return module_args


def cancel_task_entity(module, result, api_instance):
    """Cancel an ongoing task identified by C(task_ext_id)."""
    validate_required_params(module, ["task_ext_id"])
    task_ext_id = module.params.get("task_ext_id")
    result["task_ext_id"] = task_ext_id
    result["ext_id"] = task_ext_id

    if module.check_mode:
        result["msg"] = "Task with task_ext_id:{0} will be cancelled.".format(
            task_ext_id
        )
        return

    try:
        resp = api_instance.cancel_task(taskExtId=task_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while cancelling task with ext_id:{0}".format(
                task_ext_id
            ),
        )
        return

    if resp is not None and getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    else:
        result["response"] = None
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "task_ext_id": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_tasks_api_instance(module)
    cancel_task_entity(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
