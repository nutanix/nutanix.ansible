module_content = '''#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_objects
short_description: object module which suports object CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete, Power-on, Power-off Nutanix object''s'
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
      - Specify state of Virtual Machine
      - If C(state) is set to C(present) the object is created.
      - >-
        If C(state) is set to C(absent) and the object exists in the cluster, object
        with specified name is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: This is the wait description.
    type: bool
    required: false
    default: True
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
from ..module_utils.prism.objects import Object  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
    #TODO here should be additional arguments
    )

    return module_args


def create_object(module, result):
    object = Object(module)
    spec, error = object.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating object Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp, status = object.create(spec)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed creating object", **result)

    object_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["object_uuid"] = object_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp, tmp = object.read(object_uuid)
        result["response"] = resp


def delete_object(module, result):
    object_uuid = module.params["object_uuid"]
    if not object_uuid:
        result["error"] = "Missing parameter object_uuid in playbook"
        module.fail_json(msg="Failed deleting object", **result)

    object = Object(module)
    resp, status = object.delete(object_uuid)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed deleting object", **result)

    result["changed"] = True
    result["response"] = resp
    result["object_uuid"] = object_uuid
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
        module.fail_json(msg="Failed creating object", **result)


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
        "object_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_object(module, result)
    elif state == "absent":
        delete_object(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

'''

object_content = """# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from copy import deepcopy

from .prism import Prism


class Object(Prism):
    def __init__(self, module):
        resource_type = "/objects"
        super(Object, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            #TODO here should be methods to build spec for each attribute {attribute: method }
        }

    def get_spec(self):
        spec = self._get_default_spec()
        for ansible_param, ansible_value in self.module.params.items():
            build_spec_method = self.build_spec_methods.get(ansible_param)
            if build_spec_method and ansible_value:
                spec, error = build_spec_method(spec, ansible_value)
                if error:
                    return None, error
        return spec, None

    def _get_default_spec(self):
        return deepcopy(
            {
                #TODO here should be default main spec
            }
        )
"""


def create_module(name):
    with open("plugins/modules/ntnx_{0}s.py".format(name), "wb") as f:
        f.write(
            module_content.replace("object", name.lower()).replace(
                "Object", name.capitalize()
            )
        )

    with open("plugins/module_utils/prism/{0}s.py".format(name), "wb") as f:
        f.write(
            object_content.replace("object", name.lower()).replace(
                "Object", name.capitalize()
            )
        )


def main():
    import sys

    args = sys.argv[1:]

    if "--help" in args:
        print(
            """
        Description:  Script to create module template with base files and functionality
        Usage: create_module.py <module_name>
            module_name    Use for naming, by default "Object"
        """
        )
    else:

        create_module(args[0] if len(args) else "object")


if __name__ == "__main__":
    main()
