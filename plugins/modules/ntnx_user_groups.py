#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_groups
short_description: user_groups module which supports pc user_groups management create delete operations
version_added: 1.4.0
description: "Create, Delete user_groups"
options:
    state:
        description:
        - Specify state
        - If C(state) is set to C(present) then the operation will be  create the item.
        - If C(state) is set to C(absent) and if the item exists, then item is removed.
        choices:
        - present
        - absent
        type: str
        default: present
    wait:
        description: Wait for the  CRUD operation to complete.
        type: bool
        required: false
        default: True
    distinguished_name:
        description: user_group name
        required: false
        type: str
    user_group_uuid:
        description: user_group uuid
        type: str
        required: false
    categories:
        description:
            - Categories for the user_group. This allows setting up multiple values from a single key.
            - this will override existing categories with mentioned during update
            - mutually_exclusive with C(remove_categories)
        required: false
        type: dict
    remove_categories:
        description:
            - set this flag to remove dettach all categories attached to user_group
            - mutually_exclusive with C(categories)
        type: bool
        required: false
        default: false
    idp:
        type: dict
        description: An Identity Provider user
        suboptions:
            idp_uuid:
                type: str
                required: true
                description: An Identity Provider user uuid
            group_name:
                type: str
                required: true
                description: group name
    project:
        type: dict
        description: project that belongs to
        suboptions:
            name:
                type: str
                description: project name
            uuid:
                type: str
                description: project uuid
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: create image from local workstation
  ntnx_images:

- name: create user  group
  ntnx_user_groups:
    state: "present"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    distinguished_name: "<distinguished-name>"
    project:
      uuid: "{{project_uuid}}"
    categories:
      Environment:
        - "Dev"
  register: result

- name: create user group with idp
  ntnx_user_groups:
    state: "present"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    idp:
      idp_uuid: "{{idp_uuid}}"
      group_name: "{{group_name}}"
  register: result
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The user_group kind metadata
  returned: always
  type: dict
  sample: {
                "categories": {},
                "categories_mapping": {},
                "kind": "user_group",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "spec_hash": "00000000000000000000000000000000000000000000000000",
                "spec_version": 0,
                "uuid": "00000000-0000-0000-0000-000000000000"

            }
spec:
  description: An intentful representation of a user_group spec
  returned: always
  type: dict
  sample: {
    "resources": {
                        "directory_service_user_group": {
                            "distinguished_name": "<distinguished name>"
                        }
                    }

  }
status:
  description: An intentful representation of a user_group status
  returned: always
  type: dict
  sample: {
"execution_context": {
                    "task_uuid": [
                        "00000000-0000-0000-0000-000000000000"
                    ]
                },
                "resources": {
                    "access_control_policy_reference_list": [],
                    "directory_service_user_group": {
                        "directory_service_reference": {
                            "kind": "directory_service",
                            "name": "ds",
                            "uuid": "00000000-0000-0000-0000-000000000000"
                        },
                        "distinguished_name": "<distinguished name>"
                    },
                    "display_name": "<display_name>",
                    "projects_reference_list": [],
                    "user_group_type": "DIRECTORY_SERVICE"
                },
                "state": "COMPLETE"

  }
user_group_uuid:
  description: The created user_group uuid
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.v3.prism.tasks import Task  # noqa: E402
from ..module_utils.v3.prism.user_groups import UserGroup  # noqa: E402


def get_module_spec():

    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    saml_user_group_spec = dict(
        idp_uuid=dict(type="str", required=True),
        group_name=dict(type="str", required=True),
    )

    module_args = dict(
        user_group_uuid=dict(type="str"),
        distinguished_name=dict(type="str"),
        idp=dict(type="dict", options=saml_user_group_spec),
        project=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        remove_categories=dict(type="bool", default=False),
        categories=dict(type="dict", required=False),
    )
    return module_args


def create_user_group(module, result):
    user_group = UserGroup(module)
    spec, error = user_group.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating create user_group Spec", **result)
    if module.check_mode:
        result["response"] = spec
        return

    # create user_group
    resp = user_group.create(spec)
    user_group_uuid = resp["metadata"]["uuid"]
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["user_group_uuid"] = user_group_uuid
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        # get the user_group
        resp = user_group.read(user_group_uuid)

    result["response"] = resp


def delete_user_group(module, result):
    uuid = module.params["user_group_uuid"]
    if not uuid:
        result["error"] = "Missing parameter user_group_uuid"
        module.fail_json(msg="Failed deleting user_group", **result)

    user_group = UserGroup(module)
    resp = user_group.delete(uuid)
    result["response"] = resp
    result["changed"] = True
    task_uuid = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        task = Task(module)
        resp = task.wait_for_completion(task_uuid)
        result["response"] = resp


def run_module():
    # mutually_exclusive_list have params which are not allowed together
    mutually_exclusive_list = [
        ("categories", "remove_categories"),
        ("distinguished_name", "idp"),
    ]
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("user_group_uuid",)),
        ],
        mutually_exclusive=mutually_exclusive_list,
    )
    utils.remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "user_group_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_user_group(module, result)
    else:
        delete_user_group(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
