#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_plan_job_v2
short_description: Delete a Recovery Plan Job
version_added: 2.7.0
description:
  - This module allows you to delete an existing Recovery Plan Job in Nutanix Prism Central.
  - This module does not support create/update operations for Recovery Plan Jobs, so this
    module supports the delete operation only.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation. The required roles depend on the operation being performed.
    - >-
      B(Delete a Recovery Plan Job) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Project Manager, Self-Service Admin (Deprecated), Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
  state:
    description:
      - The state of the Recovery Plan Job.
      - Only C(absent) is supported, which triggers a delete on the Recovery Plan Job identified by C(ext_id).
    type: str
    required: false
    choices:
      - absent
    default: absent
  ext_id:
    description:
      - The external identifier of the Recovery Plan Job.
      - Required for delete operation.
    type: str
    required: false
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
- name: Delete a Recovery Plan Job
  nutanix.ncp.ntnx_recovery_plan_job_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "0d9d8f39-2e6b-4a19-8d33-6a2bde7ac1f2"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for deleting a Recovery Plan Job.
    - If C(wait) is true, it will return the task details after completion (including status).
    - If C(wait) is false, it will return the task submission details.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": null,
      "completed_time": "2026-07-21T07:12:38.532000+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T07:12:34.101000+00:00",
      "entities_affected": [
        {
          "ext_id": "0d9d8f39-2e6b-4a19-8d33-6a2bde7ac1f2",
          "name": null,
          "rel": "dataprotection:config:recovery-plan-job"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:9b58e37d-2c31-49c5-ba8e-5e8f1c2c1cb1",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T07:12:38.560000+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 0,
      "operation": "Delete",
      "operation_description": "Delete Recovery Plan Job",
      "owned_by": null,
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2026-07-21T07:12:34.130000+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:9b58e37d-2c31-49c5-ba8e-5e8f1c2c1cb1"

ext_id:
  description:
    - The external ID of the Recovery Plan Job.
  returned: always
  type: str
  sample: "0d9d8f39-2e6b-4a19-8d33-6a2bde7ac1f2"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while deleting recovery plan job"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_plan_jobs_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(
            type="str",
            required=False,
            choices=["absent"],
            default="absent",
        ),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def delete_recovery_plan_job(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Recovery plan job with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    try:
        resp = api_instance.delete_recovery_plan_job_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting recovery plan job",
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
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    api_instance = get_recovery_plan_jobs_api_instance(module)
    delete_recovery_plan_job(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
