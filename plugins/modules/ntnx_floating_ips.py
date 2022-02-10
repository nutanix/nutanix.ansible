#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_floating_ips
short_description: floating_ips module which suports floating_ip CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete floating_ips'
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
      - Specify state of floating_ip
      - If C(state) is set to C(present) then floating_ip is created.
      - >-
        If C(state) is set to C(absent) and if the floating_ip exists, then
        floating_ip is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for floating_ip CRUD operation to complete.
    type: bool
    required: false
    default: True
  name:
    description: floating_ip Name
    required: False
    type: str
  floating_ip_uuid:
    description: floating_ip UUID
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
from ..module_utils.prism.floating_ips import FloatingIP  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    module_args = dict(
        external_subnet=dict(type="dict",
                             options=entity_by_spec,
                             mutually_exclusive=mutually_exclusive,
                             required=True),
        vm=dict(type="dict",
                options=entity_by_spec,
                mutually_exclusive=mutually_exclusive),
        vpc=dict(type="dict",
                 options=entity_by_spec,
                 mutually_exclusive=mutually_exclusive),
        private_ip=dict(type="str")
    )

    return module_args


def create_floating_ip(module, result):
    floating_ip = FloatingIP(module)
    spec, error = floating_ip.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating floating_ip spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp, status = floating_ip.create(spec)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed creating floating_ip", **result)

    floating_ip_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["floating_ip_uuid"] = floating_ip_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp, tmp = floating_ip.read(floating_ip_uuid)
        result["response"] = resp


def delete_floating_ip(module, result):
    floating_ip_uuid = module.params["floating_ip_uuid"]
    if not floating_ip_uuid:
        result["error"] = "Missing parameter floating_ip_uuid in playbook"
        module.fail_json(msg="Failed deleting floating_ip", **result)

    floating_ip = FloatingIP(module)
    resp, status = floating_ip.delete(floating_ip_uuid)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed deleting floating_ip", **result)

    result["changed"] = True
    result["response"] = resp
    result["floating_ip_uuid"] = floating_ip_uuid
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
        module.fail_json(msg="Failed creating floating_ip", **result)


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[("vm", "vpc")]
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "floating_ip_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_floating_ip(module, result)
    elif state == "absent":
        delete_floating_ip(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
