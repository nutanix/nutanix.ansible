#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.roles import Roles  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    module_args = dict(
        name=dict(type="str", required=False),
        role_uuid=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        permissions=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        )
    )
    return module_args


def create_role(module, result):
    roles = Roles(module)
    name = module.params["name"]
    if roles.get_uuid(name):
        module.fail_json(msg="Role with given name already exists", **result)

    spec, err = roles.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create Roles Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = roles.create(data=spec)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    role_uuid = resp["metadata"]["uuid"]
    result["role_uuid"] = role_uuid
    result["changed"] = True

    if module.params.get("wait"):
        tasks = Task(module)
        tasks.wait_for_completion(task_uuid)
        resp = roles.read(uuid=role_uuid)
    result["response"] = resp


def update_role(module, result):
    roles = Roles(module)
    role_uuid = module.params.get("role_uuid")
    result["role_uuid"] = role_uuid

    resp = roles.read(uuid=role_uuid)
    utils.strip_extra_attrs_from_status(resp["status"], resp["spec"])
    resp["spec"] = resp.pop("status")

    update_spec, error = roles.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating Role update spec", **result)

    # check for idempotency
    if resp == update_spec:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    if module.check_mode:
        result["response"] = update_spec
        return

    resp = roles.update(data=update_spec, uuid=role_uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["changed"] = True

    if module.params.get("wait"):
        tasks = Task(module)
        tasks.wait_for_completion(task_uuid)
        resp = roles.read(uuid=role_uuid)

    result["response"] = resp


def delete_role(module, result):
    roles = Roles(module)
    role_uuid = module.params["role_uuid"]
    resp = roles.delete(uuid=role_uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["changed"] = True

    if module.params.get("wait"):
        tasks = Task(module)
        resp = tasks.wait_for_completion(task_uuid)
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "role_uuid"), True),
            ("state", "absent", ("role_uuid",))
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "role_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        if module.params.get("role_uuid"):
            update_role(module, result)
        else:
            create_role(module, result)
    elif state == "absent":
        delete_role(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
