#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy


from ..module_utils.prism.idempotence_identifiers import IdempotenceIdenitifiers
from ..module_utils.prism.projects_internal import ProjectsInternal

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
        description:
            - project name
            - cannot update once project is created
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
    default_subnet:
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
    subnets:
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
    users:
        description:
            - list of uuid of users to be added in project
            - this won't add role to the users, for same use ntnx_acps modules
        required: false
        type: list
        elements: str
    external_user_groups:
        description:
            - list of uuid of user groups to be added in project
            - this won't add role to the users, for same use ntnx_acps modules
        required: false
        type: list
        elements: str
    clusters:
        description:
            - list of uuid of cluster to be added in project
            - Adding clusters is supported for PC versions >= pc.2022.1
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
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    name: "test-ansible-project-1"
    desc: desc-123
    subnets:
      - name: "{{ network.dhcp.name }}"
      - uuid: "{{ static.uuid }}"
    default_subnet:
      name: "{{ network.dhcp.name }}"
    users:
      - "{{ users[0] }}"
      - "{{ users[1] }}"
    external_user_groups:
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

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.projects import Project  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.utils import (  # noqa: E402
    extract_uuids_from_references_list,
    remove_param_with_none_value,
    strip_extra_attrs,
)


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    saml_user_group_spec = dict(
        idp_uuid=dict(type="str", required=True),
        group_name=dict(type="str", required=True),
    )

    resource_limit = dict(
        resource_type=dict(
            type="str", required=True, choices=["VCPUS", "MEMORY", "STORAGE"]
        ),
        limit=dict(type="int", required=True),
    )

    user = dict(
        uuid=dict(type="str"),
        principal_name=dict(type="str"),
        username=dict(type="str"),
        directory_service_uuid=dict(type="str"),
        identity_provider_uuid=dict(type="str"),
    )
    user_mutually_exclusive = [
        ("principal_name", "uuid"),
        ("username", "uuid"),
        ("directory_service_uuid", "uuid"),
        ("identity_provider_uuid", "uuid"),
    ]

    user_group = dict(
        uuid=dict(type="str"),
        distinguished_name=dict(type="str"),
        idp=dict(type="dict", options=saml_user_group_spec),
    )
    user_group_mutually_exclusive = [
        ("distinguished_name", "uuid"),
        ("idp", "uuid"),
    ]

    role_mapping = dict(
        user=dict(
            type="dict",
            options=user,
            mutually_exclusive=user_mutually_exclusive,
            required=False,
        ),
        user_group=dict(
            type="dict",
            options=user_group,
            mutually_exclusive=user_group_mutually_exclusive,
            required=False,
        ),
        role=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
    )

    module_args = dict(
        name=dict(type="str", required=False),
        project_uuid=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        resource_limits=dict(
            type="list", elements="dict", options=resource_limit, required=False
        ),
        default_subnet=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        subnets=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        accounts=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        clusters=dict(type="list", elements="str", required=False),
        users=dict(type="list", elements="str", required=False),
        external_user_groups=dict(type="list", elements="str", required=False),
        collaboration=dict(type="bool", required=False),
        role_mappings=dict(
            type="list",
            elements="dict",
            options=role_mapping,
            mutually_exclusive=[("user", "user_group")],
            required=False,
        ),
    )
    return module_args


def create_project(module, result):

    projects = None
    if module.params.get("role_mappings"):

        # generate new uuid for project
        ii = IdempotenceIdenitifiers(module)
        uuids = ii.get_idempotent_uuids()
        projects = ProjectsInternal(module, uuid=uuids[0])

    else:
        projects = Project(module)

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
        task_status = task.wait_for_completion(task_uuid, raise_error=False)
        resp = projects.read(project_uuid)
        if task_status.get("status", "") == "FAILED":
            if task_status.get("error_detail"):
                module.fail_json(
                    msg=task_status["error_detail"],
                    status_code=task_status.get("error_code"),
                    error="Error creating project",
                    response=task_status,
                )
            else:
                module.fail_json(
                    msg=resp["status"]["message_list"],
                    error="Error creating project. Project is in {0} state".format(
                        resp["status"]["state"]
                    ),
                    response=resp,
                )

    result["response"] = resp


def check_project_idempotency(old_spec, update_spec):
    """
    Check every individual entities for similarity
    """
    old_spec = deepcopy(old_spec)
    update_spec = deepcopy(update_spec)

    # If creation of new users and user list is required
    if update_spec["spec"].get("users_list") or update_spec["spec"].get(
        "user_groups_list"
    ):
        return False

    # We compare role mapping between new acps and old acps to check idempotency
    # Only clusters(checked further), role to users/usergroups mapping or new acp creation should trigger update
    if update_spec["spec"].get("access_control_policy_list"):
        old_role_user_user_group_map = {}
        updated_role_user_user_group_map = {}

        for acp in update_spec["spec"].get("access_control_policy_list", {}):

            # Update should be done for this operations
            if acp["operation"] == "DELETE" or acp["operation"] == "ADD":
                return False

            users = []
            user_groups = []
            for user in acp["acp"]["resources"]["user_reference_list"]:
                users.append(user["uuid"])
            for ug in acp["acp"]["resources"]["user_group_reference_list"]:
                user_groups.append(ug["uuid"])

            # sort to maintain similar order while comparing
            users.sort()
            user_groups.sort()
            updated_role_user_user_group_map[
                acp["acp"]["resources"]["role_reference"]["uuid"]
            ] = {"users": users, "user_groups": user_groups}

        for acp in old_spec["spec"].get("access_control_policy_list", {}):

            users = []
            user_groups = []
            for user in acp["acp"]["resources"]["user_reference_list"]:
                users.append(user["uuid"])
            for ug in acp["acp"]["resources"]["user_group_reference_list"]:
                user_groups.append(ug["uuid"])

            # sort to maintain similar order while comparing
            users.sort()
            user_groups.sort()
            old_role_user_user_group_map[
                acp["acp"]["resources"]["role_reference"]["uuid"]
            ] = {"users": users, "user_groups": user_groups}

        if old_role_user_user_group_map != updated_role_user_user_group_map:
            return False

    if old_spec["spec"].get("project_detail"):
        old_spec = old_spec["spec"]["project_detail"]
    else:
        old_spec = old_spec["spec"]

    if update_spec["spec"].get("project_detail"):
        update_spec = update_spec["spec"]["project_detail"]
    else:
        update_spec = update_spec["spec"]

    if old_spec["name"] != update_spec["name"]:
        return False

    if old_spec.get("description") != update_spec.get("description"):
        return False

    # check quota
    if old_spec["resources"].get("resource_domain") != update_spec["resources"].get(
        "resource_domain"
    ):
        return False

    # check default subnet reference
    if old_spec["resources"].get("default_subnet_reference", {}).get(
        "uuid"
    ) != update_spec["resources"].get("default_subnet_reference", {}).get("uuid"):
        return False

    # check cluster
    old_clusters = extract_uuids_from_references_list(
        old_spec["resources"].get("cluster_reference_list", [])
    )
    new_clusters = extract_uuids_from_references_list(
        update_spec["resources"].get("cluster_reference_list", [])
    )
    if old_clusters != new_clusters:
        return False

    # check subnets
    old_subnets = extract_uuids_from_references_list(
        old_spec["resources"].get("subnet_reference_list", [])
    )
    new_subnets = extract_uuids_from_references_list(
        update_spec["resources"].get("subnet_reference_list", [])
    )
    if old_subnets != new_subnets:
        return False

    # check users
    old_users = extract_uuids_from_references_list(
        old_spec["resources"].get("user_reference_list", [])
    )
    new_users = extract_uuids_from_references_list(
        update_spec["resources"].get("user_reference_list", [])
    )
    if old_users != new_users:
        return False

    # check user groups
    old_usergroups = extract_uuids_from_references_list(
        old_spec["resources"].get("external_user_group_reference_list", [])
    )
    new_usergroups = extract_uuids_from_references_list(
        update_spec["resources"].get("external_user_group_reference_list", [])
    )
    if old_usergroups != new_usergroups:
        return False

    return True


def update_project(module, result):
    uuid = module.params["project_uuid"]
    if not uuid:
        result["error"] = "Missing parameter project_uuid in playbook"
        module.fail_json(msg="Failed updating project", **result)
    result["project_uuid"] = uuid

    projects = None
    if module.params.get("role_mappings"):
        projects = ProjectsInternal(module, uuid)
    else:
        projects = Project(module)

    resp = projects.read(uuid)

    # handle cases for projects_internal based status and spec differences
    if isinstance(projects, ProjectsInternal):
        resp["status"]["project_detail"] = resp["status"].pop("project_status")
        resp["status"]["access_control_policy_list"] = resp["spec"][
            "access_control_policy_list"
        ]

    strip_extra_attrs(resp["status"], resp["spec"])
    resp["spec"] = resp.pop("status")

    update_spec, error = projects.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating project update spec", **result)

    if module.check_mode:
        result["response"] = update_spec
        return

    # check for idempotency
    if check_project_idempotency(resp, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to update.")

    resp = projects.update(update_spec, uuid=uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        task = Task(module)
        task_status = task.wait_for_completion(task_uuid)
        resp = projects.read(uuid)
        if task_status.get("status", "") == "FAILED":
            if task_status.get("error_detail"):
                module.fail_json(
                    msg=task_status["error_detail"],
                    status_code=task_status.get("error_code"),
                    error="Error creating project",
                    response=task_status,
                )
            else:
                module.fail_json(
                    msg=resp["status"]["message_list"],
                    error="Error creating project. Project is in {0} state".format(
                        resp["status"]["state"]
                    ),
                    response=resp,
                )

    result["changed"] = True
    result["response"] = resp


def delete_project(module, result):
    uuid = module.params["project_uuid"]
    if not uuid:
        result["error"] = "Missing parameter project_uuid"
        module.fail_json(msg="Failed deleting Project", **result)

    projects = Project(module)
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
        mutually_exclusive=[
            ("users", "role_mappings"),
            ("external_user_groups", "role_mappings"),
        ],
        required_if=[
            ("state", "present", ("project_uuid", "name"), True),
            ("state", "absent", ("project_uuid",)),
        ],
        required_together=[("role_mappings", "collaboration")],
    )
    remove_param_with_none_value(module.params)
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
