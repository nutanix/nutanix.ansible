#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

__metaclass__ = type

DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.spec.entity_reference import EntityReference
from ..module_utils.prism.projects import Projects  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402

def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = deepcopy(EntityReference.entity_by_spec)
    resource_limit = dict(
        resource_type = dict(type="str", required=True),
        limit = dict(type="str", required=True)
    )
    # To-Do: 
    # 1. Write get logic for external networks
    # 2. Tunnels and accounts API not in api doc
    # 3. ACPs create using users
    module_args = dict(
        name = dict(type="str", required=False),
        project_uuid = dict(type="str", required=False),
        desc = dict(type="str", required=False),
        is_default = dict(type="bool", required=False),
        remove_categories=dict(type="bool", required=False, default=False),
        categories=dict(type="dict", required=False),
        resource_limits = dict(type="list", elememts="dict", options=resource_limit, required=False),
        default_subnet_reference = dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        subnet_reference_list = dict(type="list", elements="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        external_network_list = dict(type="list", elements="dict", options=EntityReference.get_entity_reference_by_uuid_module_spec("subnet")),
        vpc_reference_list = dict(type="list", elements="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        default_environment_reference = dict(type="dict", options=EntityReference.get_entity_reference_by_uuid_module_spec("environment")),
        environment_reference_list = dict(type="list", elements="dict", options=EntityReference.get_entity_reference_by_uuid_module_spec("environment")),
        user_reference_list = dict(type="list", elements="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        external_user_group_reference_list = dict(type="list", elements="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        account_reference_list = dict(type="list", elements="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        tunnel_reference_list = dict(type="list", elements="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
    )
    return module_args

def create_project(module, result):
    projects = Projects(module)
    name = module.params["name"]
    if projects.get_uuid(name):
        module.fail_json(msg="Project with given name already exists", **result)

    spec, error = projects.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating create project spec", **result)
    if module.check_mode:
        result["response"] = spec
        return

    resp = projects.create(spec)
    project_uuid = resp["metadata"]["uuid"]
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["project_uuid"] = project_uuid
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = projects.read(project_uuid)

    result["response"] = resp

def update_project(module, result):
    uuid = module.params["project_uuid"]
    if not uuid:
        result["error"] = "Missing parameter project_uuid in playbook"
        module.fail_json(msg="Failed updating project", **result)
    result["project_uuid"] = uuid

    projects = Projects(module)
    resp = projects.read(uuid)
    utils.strip_extra_attrs_from_status(resp["status"], resp["spec"])
    resp["spec"] = resp.pop("status")

    update_spec, error = projects.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating project update spec", **result)

    # check for idempotency
    if resp == update_spec:
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to update."
        )

    if module.check_mode:
        result["response"] = update_spec
        return

    resp = projects.update(update_spec, uuid=uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = projects.read(uuid)

    result["changed"] = True
    result["response"] = resp

def delete_project(module, result):
    uuid = module.params["project_uuid"]
    if not uuid:
        result["error"] = "Missing parameter project_uuid"
        module.fail_json(msg="Failed deleting Project", **result)

    projects = Projects(module)
    resp = projects.delete(uuid)
    result["response"] = resp
    result["changed"] = True
    task_uuid = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)

def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[("categories", "remove_categories")],
        required_if=[
            ("state", "present", ("project_uuid", "name"), True),
            ("state", "absent", ("project_uuid",))
        ]
    )
    utils.remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "project_uuid": None
    }
    if module.params["state"]=="present":
        if module.params.get("project_uuid"):
            update_project(module, result)
        else:
            create_project(module, result)
    else:
        delete_project(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
