#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_pc_task_abort_v2
short_description: Deploys a Prism Central using the provided details
version_added: 2.3.0

    
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""

"""

RETURN = r"""
response:
    description: Task response for aborting the task
    returned: always
    type: dict
    sample:

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

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_tasks_api_instance,
)
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
    task_api = get_tasks_api_instance(module)

    if module.check_mode:
        result["msg"] = "Task with ext_id:{0} will be aborted.".format(task_ext_id)
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
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    abort_task(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
