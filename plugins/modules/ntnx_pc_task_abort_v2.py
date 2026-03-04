#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_pc_task_abort_v2
short_description: Aborts a task in Prism Central
version_added: 2.3.0
description:
  - This module allows you to abort a task in Prism Central.
  - This module uses PC v4 APIs based SDKs
options:
  task_ext_id:
    description:
      - The external ID of the task.
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
- name: Abort a task
  nutanix.ncp.ntnx_pc_task_abort_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    task_ext_id: "ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description: Task response for aborting the task
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
    description: Task external ID.
    returned: always
    type: str
    sample: "ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "Api Exception raised while aborting task"

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import get_tasks_api_instance  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        task_ext_id=dict(type="str", required=True),
    )
    return module_args


def abort_task(module, result):
    """
    This method will abort a task.
    Args:
        module (object): Ansible module object
        result (dict): Result object
    """
    task_ext_id = module.params.get("task_ext_id")
    result["task_ext_id"] = task_ext_id
    task_api = get_tasks_api_instance(module)

    if module.check_mode:
        result["msg"] = "Task with task_ext_id:{0} will be aborted.".format(task_ext_id)
        return

    resp = None
    try:
        resp = task_api.cancel_task(taskExtId=task_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while aborting task",
        )
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        support_proxy=True,
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "task_ext_id": None,
    }
    abort_task(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
