#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_projects
short_description: module for create, update and delete pc projects
version_added: 1.4.0
description: "module for create, update and delete pc projects"
options:
    wait:
        description: Wait for the operations to complete.
        type: bool
        required: false
        default: True
    name:
        description: project name
        required: false
        type: str
    project_uuid:
        description:
            - This field can be used for update and delete of project
            - if C(project_uuid) and C(state)==present will update the project
            - if C(project_uuid) and C(state)==absent will delete the project
        type: str
        required: false
    desc:
        description: A description for project.
        required: false
        type: str
    resource_limits:
        description: resource limit quotas for project.
        required: false
        type: list
        elements: dict
        suboptions:
            resource_type:
                description: Type of resource limit
                required: true
                type: str
                choices:
                    - VCPUS
                    - STORAGE
                    - MEMORY
            limit:
                description:
                    - limit value for given C(resource_type)
                    - for C(resource_type) as VCPUS, unit is counts
                    - for C(resource_type) as MEMORY or STORAGE, unit is bytes
                required: true
                type: int
    default_subnet_reference:
        description: default subnet reference
        type: dict
        required: false
        suboptions:
            name:
                description:
                    - subnet name
                    - Mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - subnet UUID
                    - Mutually exclusive with C(name)
                type: str
    subnet_reference_list:
        description: list of subnets to be added in project
        type: list
        elements: dict
        required: false
        suboptions:
            name:
                description:
                    - subnet name
                    - Mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - subnet UUID
                    - Mutually exclusive with C(name)
                type: str
    user_uuid_list:
        description:
            - list of uuid of users to be added in project
            - this won't add role to the users, for same use ntnx_acps modules
        required: false
        type: list
        elements: str
    external_user_group_uuid_list:
        description:
            - list of uuid of user groups to be added in project
            - this won't add role to the users, for same use ntnx_acps modules
        required: false
        type: list
        elements: str
    cluster_uuid_list:
        description:
            - list of uuid of cluster to be added in project
        required: false
        type: list
        elements: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: Create Project with all specs
  ntnx_projects:
    name: "test-ansible-project-1"
    desc: desc-123
    subnet_reference_list:
      - name: "{{ network.dhcp.name }}"
      - uuid: "{{ static.uuid }}"
    default_subnet_reference:
      name: "{{ network.dhcp.name }}"
    user_uuid_list:
      - "{{ users[0] }}"
      - "{{ users[1] }}"
    external_user_group_uuid_list:
      - "{{ user_groups[0] }}"
    resource_limits:
      - resource_type: STORAGE
        limit: 2046
  register: result

- name: Delete created project
  ntnx_projects:
    state: absent
    project_uuid: "<uuid>"
    wait: true
  register: result
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The project kind metadata
  returned: always
  type: dict
  sample: {
                "categories": {},
                "categories_mapping": {},
                "creation_time": "2022-07-18T06:44:52Z",
                "kind": "project",
                "last_update_time": "2022-07-18T06:44:54Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "project_reference": {
                    "kind": "project",
                    "name": "test_project12-3523111",
                    "uuid": "df78c7800-4232-4ba8-a125-a2478f9383a9"
                },
                "spec_hash": "00000000000000000000000000000000000000000000000000",
                "spec_version": 0,
                "uuid": "df78c7800-4232-4ba8-a125-a2478f9383a9"
            }
spec:
  description: An intentful representation of a project spec
  returned: always
  type: dict
  sample: {
                "description": "check123233221",
                "name": "test_project12-3523111",
                "resources": {
                    "resource_domain": {
                        "resources": [
                            {
                                "limit": 10000000,
                                "resource_type": "STORAGE"
                            }
                        ]
                    }
                }
            }
status:
  description: An intentful representation of a project status
  returned: always
  type: dict
  sample:  {
                "description": "check123233221",
                "execution_context": {
                    "task_uuid": [
                        "6a094910-b033-4c9e-9cb7-757861934614"
                    ]
                },
                "name": "test_project12-3523111",
                "resources": {
                    "account_reference_list": [],
                    "cluster_reference_list": [],
                    "environment_reference_list": [],
                    "external_network_list": [],
                    "external_user_group_reference_list": [],
                    "is_default": false,
                    "resource_domain": {
                        "resources": [
                            {
                                "limit": 10000000,
                                "resource_type": "STORAGE",
                                "units": "BYTES",
                                "value": 0
                            }
                        ]
                    },
                    "subnet_reference_list": [],
                    "tunnel_reference_list": [],
                    "user_reference_list": [],
                    "vpc_reference_list": []
                },
                "state": "COMPLETE"
            }
project_uuid:
  description: The created project's uuid
  returned: always
  type: str
  sample: "df78c7800-4232-4ba8-a125-a2478f9383a9"
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.projects import Projects  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    resource_limit = dict(
        resource_type=dict(
            type="str", required=True, choices=["VCPUS", "MEMORY", "STORAGE"]
        ),
        limit=dict(type="int", required=True),
    )
    module_args = dict(
        name=dict(type="str", required=False),
        project_uuid=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        resource_limits=dict(
            type="list", elements="dict", options=resource_limit, required=False
        ),
        default_subnet_reference=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        subnet_reference_list=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        cluster_uuid_list=dict(type="list", elements="str", required=False),
        user_uuid_list=dict(type="list", elements="str", required=False),
        external_user_group_uuid_list=dict(type="list", elements="str", required=False),
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
        module.exit_json(msg="Nothing to update.")

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
        resp = task.wait_for_completion(task_uuid)
        result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("project_uuid", "name"), True),
            ("state", "absent", ("project_uuid",)),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "project_uuid": None}
    if module.params["state"] == "present":
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
