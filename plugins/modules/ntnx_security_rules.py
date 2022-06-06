#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_rules
short_description: security_rules module which suports security_rules CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete security_rules'
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
      - Specify state of security_rules
      - If C(state) is set to C(present) then security_rules is created.
      - >-
        If C(state) is set to C(absent) and if the security_rules exists, then
        security_rules is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for security_rules CRUD operation to complete.
    type: bool
    required: false
    default: True
  name:
    description: security_rules Name
    required: False
    type: str
  security_rules_uuid:
    description: security_rules UUID
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
from ..module_utils.prism.security_rules import SecurityRules  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    module_args = dict(
    # Step 1: Ansible module spec and spec validation
    )

    return module_args


def create_security_rules(module, result):
    security_rules = SecurityRules(module)
    spec, error = security_rules.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating security_rules spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = security_rules.create(spec)
    security_rules_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["security_rules_uuid"] = security_rules_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = security_rules.read(security_rules_uuid)
        result["response"] = resp


def delete_security_rules(module, result):
    security_rules_uuid = module.params["security_rules_uuid"]
    if not security_rules_uuid:
        result["error"] = "Missing parameter security_rules_uuid in playbook"
        module.fail_json(msg="Failed deleting security_rules", **result)

    security_rules = SecurityRules(module)
    resp = security_rules.delete(security_rules_uuid)
    result["changed"] = True
    result["response"] = resp
    result["security_rules_uuid"] = security_rules_uuid
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
        "security_rules_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_security_rules(module, result)
    elif state == "absent":
        delete_security_rules(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

