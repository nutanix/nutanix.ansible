#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
module: ntnx_pc_tasks_info_v2
short_description: Get PC task details
version_added: 2.3.0
description:
    - Fetch specific PC task info using external ID
    - Fetch list of PC task info if external ID is not provided with optional filters.
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - A globally unique identifier for a task.
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get Task status using task ext_id
  nutanix.ncp.ntnx_pc_tasks_info_v2:
    ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
  register: result

- name: Get all the tasks
  nutanix.ncp.ntnx_pc_tasks_info_v2:
  register: result
  ignore_errors: true

- name: Get task details using filters
  nutanix.ncp.ntnx_pc_tasks_info_v2:
    filter: "operation eq 'kImageCreate'"
  register: result
  ignore_errors: true

- name: Get task details using limit
  nutanix.ncp.ntnx_pc_tasks_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for fetching PC task info.
        - One PC task info if external ID is provided.
        - List of multiple PC tasks info if external ID is not provided.
    type: dict
    returned: always
    sample:
        {
            "app_name": null,
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
            "ext_id": "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8",
            "is_background_task": false,
            "is_cancelable": true,
            "last_updated_time": "2025-08-20T11:25:59.187166+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 1,
            "operation": "kImageCreate",
            "operation_description": "Create Image",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "resource_links": null,
            "root_task": null,
            "started_time": "2025-08-20T11:25:55.661704+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:0d18cb98-3362-412e-87ef-0566c65a4223",
                    "href": "https://10.44.76.129:9440/api/prism/v4.1/config/tasks/ZXJnb24=:0d18cb98-3362-412e-87ef-0566c65a4223",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }
ext_id:
    description: External ID of the task
    type: str
    returned: when external ID is provided
    sample: "ZXJnb24=:cda893b8-2aee-34bf-817d-d2ee6026790b"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

total_available_results:
    description:
        - The total number of available PC tasks
    type: int
    returned: when all pc tasks are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_pc_task  # noqa: E402
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
        ext_id=dict(type="str"),
    )
    return module_args


def get_task_details_with_ext_id(module, tasks_api, result):
    ext_id = module.params.get("ext_id")
    resp = get_pc_task(module, tasks_api, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_tasks_details(module, tasks_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating list tasks info Spec", **result)
    try:
        resp = tasks_api.list_tasks(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching tasks info",
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
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    tasks_api = get_tasks_api_instance(module)
    if module.params.get("ext_id"):
        get_task_details_with_ext_id(module, tasks_api, result)
    else:
        get_tasks_details(module, tasks_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
