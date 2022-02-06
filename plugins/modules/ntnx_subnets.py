#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_subnets
short_description: subnets module which suports subnet CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete subnets'
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
      - Specify state of subnet
      - If C(state) is set to C(present) then subnet is created.
      - >-
        If C(state) is set to C(absent) and if the subnet exists, then
        subnet is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for subnet CRUD operation to complete.
    type: bool
    required: false
    default: True
  name:
    description: subnet Name
    required: False
    type: str
  subnet_uuid:
    description: subnet UUID
    type: str

  #TODO here should be additional arguments documentation

"""

EXAMPLES = r"""
# TODO
"""

RETURN = r"""
# TODO
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.subnets import Subnet  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    module_args = dict(
        # TODO: Ansible module spec and spec validation
    )

    return module_args


def create_subnet(module, result):
    subnet = Subnet(module)
    spec, error = subnet.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating subnet spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp, status = subnet.create(spec)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed creating subnet", **result)

    subnet_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["subnet_uuid"] = subnet_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp, tmp = subnet.read(subnet_uuid)
        result["response"] = resp


def delete_subnet(module, result):
    subnet_uuid = module.params["subnet_uuid"]
    if not subnet_uuid:
        result["error"] = "Missing parameter subnet_uuid in playbook"
        module.fail_json(msg="Failed deleting subnet", **result)

    subnet = Subnet(module)
    resp, status = subnet.delete(subnet_uuid)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed deleting subnet", **result)

    result["changed"] = True
    result["response"] = resp
    result["subnet_uuid"] = subnet_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp, status = task.wait_for_completion(task_uuid)
    result["response"] = resp
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed creating subnet", **result)


def run_module():
    module = BaseModule(argument_spec=get_module_spec(), supports_check_mode=True)
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "subnet_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_subnet(module, result)
    elif state == "absent":
        delete_subnet(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
