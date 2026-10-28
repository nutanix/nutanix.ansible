#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_task_entities_info_v2
short_description: Fetch the affected entities (TaskEntity) of a Prism Central task
version_added: "2.7.0"
description:
  - Fetch list of TaskEntity records for a Prism Central task identified by C(task_ext_id).
  - A TaskEntity is an entity (VM, image, subnet, VPC, category, etc.) that a Prism Central
    v4 asynchronous task created, modified, or otherwise affected.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(List entities associated with a task) -
    Required Roles: Account Owner, Administrator, Backup Admin, Consumer, CSI System,
    Intelligent Ops Admin, Kubernetes Data Services System, Monitoring Admin,
    NCM Admin, NCM Connector, NCM Viewer, Prism Admin, Prism Viewer, Project Admin,
    Self-Service Admin (deprecated), Super Admin, Tenant Admin, Tenant Consumer
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  task_ext_id:
    description:
      - External ID of the parent task whose affected entities should be listed.
      - Consists of a prefix and a UUID separated by C(:).
      - The C(legacy) prefix can be used with a task UUID from previous API families.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all entities affected by a task
  nutanix.ncp.ntnx_task_entities_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
  register: result

- name: List all entities affected by a task with fetch_all
  nutanix.ncp.ntnx_task_entities_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    fetch_all: true
  register: result

- name: List task-affected entities with a limit
  nutanix.ncp.ntnx_task_entities_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    limit: 1
  register: result

- name: List task-affected entities filtered by rel
  nutanix.ncp.ntnx_task_entities_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    task_ext_id: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"
    filter: "rel eq 'vmm:content:image'"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for fetching task entities info.
    - Always a list of TaskEntity dicts for the given C(task_ext_id).
    - Empty list when the task has not affected any entities.
  returned: always
  type: list
  elements: dict
  sample:
    - ext_id: "c13300a6-d246-4d1f-9d0c-64b5dd31c393"
      name: "ansible-image-LHAIPsToXnDF1"
      rel: "vmm:content:image"

task_ext_id:
  description: The external ID of the parent task whose affected entities were fetched.
  returned: always
  type: str
  sample: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching task entities info"

total_available_results:
  description: The total number of available TaskEntity records for the parent task.
  returned: when all task entities are fetched
  type: int
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import get_tasks_api_instance  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
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
        resp = list_entities(
            tasks_api.list_task_entities,
            kwargs=kwargs,
            taskExtId=task_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching task entities info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

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
        "failed": False,
        "response": None,
        "task_ext_id": None,
    }
    tasks_api = get_tasks_api_instance(module)
    list_task_entities(module, tasks_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
