#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_task_jobs_info_v2
short_description: Fetch task job(s) associated with a Prism Central task
version_added: 2.5.0
description:
  - This module allows you to fetch information about TaskJob in Nutanix Prism Central.
  - A TaskJob represents a single action inside a parent batch task; each
    TaskJob reports its own status, entities affected and error messages.
  - If C(ext_id) is provided, fetch details of the specific TaskJob.
  - If C(ext_id) is not provided, list multiple TaskJob optionally paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to
    the user performing the operation.
  - >-
    B(Get task job by ext_id) -
    Required Roles: Account Owner, Administrator, Backup Admin, CSI System,
    Intelligent Ops Admin, Kubernetes Data Services System, Monitoring Admin,
    NCM Admin, NCM Connector, NCM Viewer, Prism Admin, Prism Viewer, Super Admin,
    Self-Service Admin (deprecated)
  - >-
    B(List task jobs) -
    Required Roles: Account Owner, Administrator, Backup Admin, CSI System,
    Intelligent Ops Admin, Kubernetes Data Services System, Monitoring Admin,
    NCM Admin, NCM Connector, NCM Viewer, Prism Admin, Prism Viewer, Super Admin,
    Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  task_ext_id:
    description:
      - The external ID of the parent task whose jobs are to be fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of a specific task job.
      - When provided, the module fetches the details of that single job.
      - When omitted, the module lists all jobs of the parent task.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch all jobs for a task
  nutanix.ncp.ntnx_task_jobs_info_v2:
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
  register: result
  ignore_errors: true

- name: Fetch a single task job by ext_id
  nutanix.ncp.ntnx_task_jobs_info_v2:
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    ext_id: "0d18cb98-3362-412e-87ef-0566c65a4223"
  register: result
  ignore_errors: true

- name: List task jobs with pagination
  nutanix.ncp.ntnx_task_jobs_info_v2:
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    page: 0
    limit: 1
  register: result
  ignore_errors: true

- name: List task jobs and select only status and name
  nutanix.ncp.ntnx_task_jobs_info_v2:
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    select: "status,name"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC TaskJob info v4 API.
    - Single TaskJob when I(ext_id) is provided.
    - List of TaskJob objects when I(ext_id) is not provided (optionally paginated).
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00063a1c-a953-2048-0000-000000028f57"
      ],
      "completed_time": "2025-08-20T11:25:59.187167+00:00",
      "completion_details": null,
      "created_time": "2025-08-20T11:25:55.634964+00:00",
      "entities_affected": [
        {
          "ext_id": "c13300a6-d246-4d1f-9d0c-64b5dd31c393",
          "name": "ansible-image-LHAIPsToXnDF1",
          "rel": "vmm:content:image"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0d18cb98-3362-412e-87ef-0566c65a4223",
      "links": null,
      "name": "kImageCreate",
      "status": "SUCCEEDED",
      "tenant_id": null,
      "warnings": null
    }

task_ext_id:
  description: External ID of the parent task the jobs belong to.
  type: str
  returned: always
  sample: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"

ext_id:
  description: External ID of the task job when a specific one was requested.
  type: str
  returned: when I(ext_id) is provided
  sample: "ZXJnb24=:0d18cb98-3362-412e-87ef-0566c65a4223"

changed:
  description: Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Status or error message emitted by the module.
  returned: when there is an error
  type: str
  sample: "Api Exception raised while fetching task jobs info"

error:
  description: Error details when the underlying API call fails.
  type: str
  returned: when an error occurs

failed:
  description: True on failure, False otherwise.
  returned: always
  type: bool
  sample: false

total_available_results:
  description:
    - Total number of task jobs associated with the parent task.
    - Only present when listing jobs (no I(ext_id) provided).
  type: int
  returned: when all task jobs are fetched
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_task_job  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import get_tasks_api_instance  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        task_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def get_task_job_with_ext_id(module, tasks_api, result):
    task_ext_id = module.params.get("task_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_task_job(module, tasks_api, task_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_task_jobs(module, tasks_api, result):
    task_ext_id = module.params.get("task_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating list task jobs info spec", **result)

    # The list_task_jobs SDK method does not support filter/orderby.
    kwargs.pop("_filter", None)
    kwargs.pop("_orderby", None)

    try:
        resp = tasks_api.list_task_jobs(taskExtId=task_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching task jobs info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "task_ext_id": module.params.get("task_ext_id"),
    }
    tasks_api = get_tasks_api_instance(module)
    if module.params.get("ext_id"):
        get_task_job_with_ext_id(module, tasks_api, result)
    else:
        get_task_jobs(module, tasks_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
