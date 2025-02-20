#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_promote_protected_resources_v2
short_description: Module to promote a protected resource in Nutanix Prism Central.
description:
  - This module can be used to promote a protected resource in Nutanix Prism Central.
  - Supported only for protected resources that have synchronous protection policies.
options:
  ext_id:
    description:
      - The external identifier of a protected VM or volume group.
    type: str
    required: true
  wait:
    description:
      - Wait for the task to complete.
    type: bool
    required: false
    default: True
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Promote VM
  nutanix.ncp.ntnx_promote_protected_resources_v2:
    nutanix_host: "{{ availability_zone_pc_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description: Task response for promoting a protected resource.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
          "00062aa9-5634-d950-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2025-01-14T08:03:14.995979+00:00",
      "completion_details": [
          {
              "name": "promotedVmExtId",
              "value": "655ea7b5-22f6-4989-9820-4992f8165bc1"
          }
      ],
      "created_time": "2025-01-14T08:03:03.027768+00:00",
      "entities_affected": null,
      "error_messages": null,
      "ext_id": "ZXJnb24=:3db0a14c-53d4-4b3e-8c86-7417ee9cae43",
      "is_background_task": false,
      "is_cancelable": true,
      "last_updated_time": "2025-01-14T08:03:14.995978+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 0,
      "number_of_subtasks": 0,
      "operation": "VmPromote",
      "operation_description": "Promote Virtual Machine",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2025-01-14T08:03:03.089069+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external identifier of the protected resource.
  returned: always
  type: str
  sample: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"

task_ext_id:
  description: The external identifier of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:af298405-1d59-4c28-9b78-f8f94a5adf2d"
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_protected_resource_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def promote_protected_resource(module, result):
    protected_resource = get_protected_resource_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    resp = None
    try:
        resp = protected_resource.promote_protected_resource(extId=ext_id)

    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while promoting protected resource",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    promote_protected_resource(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
