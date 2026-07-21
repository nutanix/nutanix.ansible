#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_task_entities_info_v2
short_description: Fetch the affected entities (TaskEntity) of a Prism Central task
version_added: 2.5.0
description:
  - This module allows you to fetch information about TaskEntity in Nutanix Prism Central.
  - A TaskEntity is an entity (VM, image, subnet, VPC, category, etc.) that a Prism Central
    v4 asynchronous task created, modified, or otherwise affected.
  - The list of affected entities is scoped to a single parent task identified by C(task_ext_id).
  - The Nutanix Prism v4 API only exposes a list endpoint for task entities
    (C(GET /api/prism/v4.3/config/tasks/{taskExtId}/affected-entities)); there is no
    dedicated get-by-ID endpoint. This module therefore always returns a list of
    TaskEntity records for the given task, optionally filtered / paginated / projected.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(List entities associated with a task) -
    Required Roles: Account Owner, Administrator, Backup Admin, CSI System,
    Intelligent Ops Admin, Kubernetes Data Services System, Monitoring Admin,
    NCM Admin, NCM Connector, NCM Viewer, Prism Admin, Prism Viewer, Super Admin,
    Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  task_ext_id:
    description:
      - A globally unique identifier for a task.
      - It consists of a prefix and a UUID separated by C(:).
      - The C(legacy) prefix can be used with a task UUID provided by previous API families.
      - Required. The task entities endpoint is always scoped to a specific parent task.
    type: str
    required: true
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

- name: List task-affected entities with a limit
  nutanix.ncp.ntnx_task_entities_info_v2:
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    limit: 1
  register: result
  ignore_errors: true

- name: List task-affected entities filtered by rel (entity type)
  nutanix.ncp.ntnx_task_entities_info_v2:
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    filter: "rel eq 'vmm:content:image'"
  register: result
  ignore_errors: true

- name: Project only ext_id and rel of task-affected entities
  nutanix.ncp.ntnx_task_entities_info_v2:
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    select: "extId,rel"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC TaskEntity info v4 API.
    - Always a list of TaskEntity dicts for the given C(task_ext_id).
    - Each element is an EntityReference with fields such as C(ext_id), C(rel), and C(name).
    - When the task has not affected any entities the list is empty.
  returned: always
  type: list
  elements: dict
  sample:
    - ext_id: "c13300a6-d246-4d1f-9d0c-64b5dd31c393"
      name: "ansible-image-LHAIPsToXnDF1"
      rel: "vmm:content:image"

task_ext_id:
  description:
    - The external ID of the parent task whose affected entities were fetched.
  returned: always
  type: str
  sample: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"

total_available_results:
  description:
    - The total number of TaskEntity records available on the server for the given
      parent task (not just the current page).
  returned: when the list call succeeds
  type: int
  sample: 1

changed:
  description: Always C(false); this is a read-only info module.
  returned: always
  type: bool
  sample: false

failed:
  description: Whether the module failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Status or error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching task entities info"

error:
  description: Error details returned by the SDK, if any.
  returned: When an error occurs
  type: str

status:
  description: HTTP status code returned by the SDK, if any.
  returned: When an error occurs
  type: int
  sample: 400

response_on_error:
  description: Raw error body returned by the SDK, if any.
  returned: When an error occurs
  type: raw
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        task_ext_id=dict(type="str", required=True),
    )
    return module_args


def list_task_entities(module, tasks_api, result):
    """List entities affected by a parent task.

    Args:
        module: Ansible module object.
        tasks_api: TasksApi instance from ntnx_prism_py_client SDK.
        result (dict): Result dict populated in-place.
    """
    task_ext_id = module.params.get("task_ext_id")
    result["task_ext_id"] = task_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating list task entities info spec", **result)

    # The /affected-entities SDK method does not accept _orderby; strip it to avoid
    # a spurious keyword being forwarded via **kwargs.
    kwargs.pop("_orderby", None)

    try:
        resp = tasks_api.list_task_entities(taskExtId=task_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching task entities info",
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
        "task_ext_id": None,
    }
    tasks_api = get_tasks_api_instance(module)
    list_task_entities(module, tasks_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
