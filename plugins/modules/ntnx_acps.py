#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_acps
short_description: acp module which suports acp CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete acp'
options:
  nutanix_host:
    description:
      - PC hostname or IP address
    type: str
    required: true
  nutanix_port:
    description:
      - PC port
    type: str
    default: 9440
    required: false
  nutanix_username:
    description:
      - PC username
    type: str
    required: true
  nutanix_password:
    description:
      - PC password;
    required: true
    type: str
  validate_certs:
    description:
      - Set value to C(False) to skip validation for self signed certificates
      - This is not recommended for production setup
    type: bool
    default: true
  state:
    description:
      - Specify state of acp
      - If C(state) is set to C(present) then acp is created.
      - >-
        If C(state) is set to C(absent) and if the acp exists, then
        acp is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for acp CRUD operation to complete.
    type: bool
    required: false
    default: True
  name:
    description: acp Name
    required: False
    type: str
  acp_uuid:
    description: acp UUID
    type: str

  # Step 4: here should be additional arguments documentation

"""

EXAMPLES = r"""
# Step 5
"""

RETURN = r"""
# Step 6
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.acps import ACP  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    rhs_spec = dict(
        collection=dict(type="str"),
        categories=dict(type="dict"),
        uuids=dict(type="list"),
    )

    filter_spec = dict(
        lhs=dict(type="str"),
        operator=dict(type="str"),
        rhs=dict(type="dict", options=rhs_spec),
    )

    module_args = dict(
        user=dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        user_group=dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        role=dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        scope_filter=dict(type="dict", options=filter_spec),
        entity_filter=dict(type="dict", options=filter_spec),
    )

    return module_args


def create_acp(module, result):
    acp = ACP(module)
    spec, error = acp.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating acp spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = acp.create(spec)
    acp_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["acp_uuid"] = acp_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = acp.read(acp_uuid)
        result["response"] = resp


def delete_acp(module, result):
    acp_uuid = module.params["acp_uuid"]
    if not acp_uuid:
        result["error"] = "Missing parameter acp_uuid in playbook"
        module.fail_json(msg="Failed deleting acp", **result)

    acp = ACP(module)
    resp = acp.delete(acp_uuid)
    result["changed"] = True
    result["response"] = resp
    result["acp_uuid"] = acp_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid)
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "acp_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_acp(module, result)
    elif state == "absent":
        delete_acp(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

