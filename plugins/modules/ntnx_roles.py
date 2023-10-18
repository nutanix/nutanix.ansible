#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_roles
short_description: module which supports role CRUD operations
version_added: 1.4.0
description: "Create, Update, Delete Nutanix roles"
options:
    state:
        description:
            - when C(state)=present and role uuid is not given then it will create new role
            - when C(state)=present and role uuid given then it will update the role
            - when C(state)=absent, it will delete the role
    name:
        description:
            - name of the role
            - allowed to update
            - required for creating role
        required: false
        type: str
    role_uuid:
        description:
            - uuid of the role
            - only required while updating or deleting
        required: false
        type: str
    desc:
        description:
            - description of role
            - allowed to update
        required: false
        type: str
    permissions:
        description:
            - list of details of permission to be added in role
            - required while creating new role
            - allowed to update
            - more than or equal to one permission is always required, empty list is not considered
            - during update, if used, it will override the permission list of role
        required: false
        type: list
        elements: dict
        suboptions:
            uuid:
                type: str
                description:
                    - permission uuid.
                    - Mutually exclusive with C(name).
            name:
                description:
                    - permission name.
                    - Mutually exclusive with C(uuid).
                type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""

- name: Create roles with permissions
  ntnx_roles:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: present
    name: test-ansible-role-1
    desc: test-ansible-role-1-desc
    permissions:
      - name: "<permision-1-name>"
      - uuid: "<permission-2-uuid>"
      - uuid: "<permission-3-uuid>"
    wait: true
  register: result

- name: delete role
  ntnx_roles:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: absent
    role_uuid: "<role-uuid>"
  register: result
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The role kind metadata from creation of new role
  returned: always
  type: dict
  sample:  {
                "categories": {},
                "categories_mapping": {},
                "creation_time": "2022-07-26T08:25:00Z",
                "entity_version": "",
                "kind": "role",
                "last_update_time": "2022-07-26T08:25:01Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "spec_hash": "00000000000000000000000000000000000000000000000000",
                "spec_version": 0,
                "uuid": "5d7bv3ab-d825-4cfd-879c-ec7a86a82cfd"
            }
spec:
  description: An intentful representation of a role spec from creation of new role
  returned: always
  type: dict
  sample: {
                "description": "check123",
                "name": "test-ansible",
                "resources": {
                    "permission_reference_list": [
                        {
                            "kind": "permission",
                            "uuid": "190951de-26f1-4caf-760d-df81c3c2jn3j2"
                        },
                        {
                            "kind": "permission",
                            "uuid": "fcf661c5-2253-44a9-7ddd-e10c23424324"
                        }
                    ]
                }
            }
status:
  description: An intentful representation of a role status from creation of role
  returned: always
  type: dict
  sample: {
                "description": "check123",
                "execution_context": {
                    "task_uuid": [
                        "asdasdsd-3e01-42e3-9276-d75571273f89"
                    ]
                },
                "is_system_defined": false,
                "name": "test-ansible",
                "resources": {
                    "permission_reference_list": [
                        {
                            "kind": "permission",
                            "name": "perm1",
                            "uuid": "190951de-26f1-4caf-760d-df81c3c2jn3j2"
                        },
                        {
                            "kind": "permission",
                            "name": "perm2",
                            "uuid": "fcf661c5-2253-44a9-7ddd-e10c23424324"
                        }
                    ]
                },
                "state": "COMPLETE"
            }
role_uuid:
  description: The created role uuid
  returned: always
  type: str
  sample: "5d7bv3ab-d825-4cfd-879c-ec7a86a82cfd"
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.roles import Role  # noqa: E402
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
        ),
    )
    return module_args


def create_role(module, result):
    roles = Role(module)
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


def check_roles_idempotency(old_spec, update_spec):

    if old_spec["spec"]["name"] != update_spec["spec"]["name"]:
        return False

    if old_spec["spec"].get("description") != update_spec["spec"].get("description"):
        return False

    # check permission uuids
    old_permissions = utils.extract_uuids_from_references_list(
        old_spec["spec"]["resources"].get("permission_reference_list", [])
    )
    new_permissions = utils.extract_uuids_from_references_list(
        update_spec["spec"]["resources"].get("permission_reference_list", [])
    )
    if old_permissions != new_permissions:
        return False

    return True


def update_role(module, result):
    roles = Role(module)
    role_uuid = module.params.get("role_uuid")
    result["role_uuid"] = role_uuid

    resp = roles.read(uuid=role_uuid)
    utils.strip_extra_attrs(resp["status"], resp["spec"])
    resp["spec"] = resp.pop("status")

    update_spec, error = roles.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating Role update spec", **result)

    # check for idempotency
    if check_roles_idempotency(resp, update_spec):
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
    roles = Role(module)
    role_uuid = module.params["role_uuid"]

    if module.check_mode:
        result["role_uuid"] = role_uuid
        result["response"] = "Role with uuid:{0} will be deleted.".format(role_uuid)
        return

    resp = roles.delete(uuid=role_uuid)
    result["role_uuid"] = role_uuid
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
            ("state", "absent", ("role_uuid",)),
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
