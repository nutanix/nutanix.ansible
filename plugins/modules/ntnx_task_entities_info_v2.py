#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_task_entities_info_v2
short_description: Fetch information about entities affected by a task in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about TaskEntity in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific TaskEntity.
  - If C(ext_id) is not provided, list multiple TaskEntity optionally filtered / paginated.
  - The "TaskEntity" here refers to an entity that was affected by a specific Prism task
    (endpoint C(/api/prism/v4.3/config/tasks/{taskExtId}/affected-entities)).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(List entities affected by a task) -
      Required Roles: Account Owner, Administrator, Backup Admin, CSI System, Intelligent Ops Admin, Kubernetes Data Services System, Monitoring Admin,
      NCM Admin, NCM Connector, NCM Viewer, Prism Admin, Prism Viewer, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  task_ext_id:
    description:
      - The external ID of the parent task whose affected entities are being fetched.
      - Required for all operations.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of a specific affected entity to return.
      - When provided, the module filters the affected-entities list by this ID and
        returns a single entity.
      - When not provided, the module returns the list of affected entities.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all entities affected by a task
  nutanix.ncp.ntnx_task_entities_info_v2:
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
  register: result
  ignore_errors: true

- name: Get a specific affected entity of a task using its ext_id
  nutanix.ncp.ntnx_task_entities_info_v2:
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    ext_id: "c13300a6-d246-4d1f-9d0c-64b5dd31c393"
  register: result
  ignore_errors: true

- name: List entities affected by a task using filter
  nutanix.ncp.ntnx_task_entities_info_v2:
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    filter: "rel eq 'vmm:content:image'"
  register: result
  ignore_errors: true

- name: List entities affected by a task using limit
  nutanix.ncp.ntnx_task_entities_info_v2:
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC TaskEntity info v4 API.
    - It can be a single TaskEntity if external ID is provided.
    - List of multiple TaskEntity if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    [
        {
            "ext_id": "215b3b02-348e-4d05-b6c1-2cfec4778ace",
            "name": "image_rate_limit_policy_ansible_updated",
            "rel": "vmm:images:config:rate-limit-policy"
        }
    ]

task_ext_id:
  description: The external ID of the parent task.
  type: str
  returned: always
  sample: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"

ext_id:
  description: External ID of a specific affected entity, if it was provided.
  type: str
  returned: when external ID is provided
  sample: "c13300a6-d246-4d1f-9d0c-64b5dd31c393"

total_available_results:
  description: The total number of affected entities available for the task.
  type: int
  returned: when listing all affected entities
  sample: 1

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or when a single entity is not found
  type: str
  sample: "Api Exception raised while fetching task entities info"

error:
  description: Information about errors that occurred during the module execution.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the module execution failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import get_tasks_api_instance  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        task_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def _list_task_entities(module, api_instance, kwargs):
    """Call TasksApi.list_task_entities and return the raw response object."""
    task_ext_id = module.params.get("task_ext_id")
    try:
        return api_instance.list_task_entities(taskExtId=task_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching task entities info",
        )


def get_task_entity_by_ext_id(module, api_instance, result):
    """Return a single affected entity by matching on ext_id.

    The Prism v4 Tasks API does not expose a dedicated GetById endpoint for an
    affected entity. Server-side C(_filter) on C(extId) is not honoured by
    the C(list_task_entities) endpoint (it silently returns all rows), so we
    page through the entire affected-entities list and match the requested
    C(ext_id) client-side.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    result["task_ext_id"] = module.params.get("task_ext_id")

    match = None
    page = 0
    while True:
        kwargs = {"_page": page, "_limit": 100}
        resp = _list_task_entities(module, api_instance, kwargs)
        page_data = strip_internal_attributes(resp.to_dict()).get("data") or []
        for entity in page_data:
            if entity.get("ext_id") == ext_id:
                match = entity
                break
        if match is not None or len(page_data) < 100:
            break
        page += 1

    if match is None:
        module.fail_json(
            msg=(
                "Affected entity with ext_id:{0} was not found for task with "
                "task_ext_id:{1}."
            ).format(ext_id, module.params.get("task_ext_id")),
            response=None,
            failed=True,
        )
        return

    result["response"] = match


def list_task_entities(module, api_instance, result):
    """List all entities affected by the task (with optional pagination/filter)."""
    result["task_ext_id"] = module.params.get("task_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating list task entities info spec", **result)

    resp = _list_task_entities(module, api_instance, kwargs)
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
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_tasks_api_instance(module)
    if module.params.get("ext_id"):
        get_task_entity_by_ext_id(module, api_instance, result)
    else:
        list_task_entities(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
