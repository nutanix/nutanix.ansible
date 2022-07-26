#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_users
short_description: users module which supports pc users management CRUD operations
version_added: 1.4.0
description: "Create, Update, Delete users"
options:
    state:
        description:
        - Specify state
        - If C(state) is set to C(present) then the operation will be  create the item.
        - if C(state) is set to C(present) and C(user_uuid) is given then it will update that user.
        - >-
            If C(state) is set to C(absent) and if the item exists, then
            item is removed.
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
    username:
        description: user name
        required: false
        type: str
    user_uuid:
        description: user uuid
        type: str
        required: false
    categories:
        description:
            - Categories for the user. This allows setting up multiple values from a single key.
            - this will override existing categories with mentioned during update
            - mutually_exclusive with C(remove_categories)
        required: false
        type: dict
    remove_categories:
        description:
            - set this flag to remove dettach all categories attached to user
            - mutually_exclusive with C(categories)
        type: bool
        required: false
        default: false
    identity_provider_uuid:
        type: str
        description: The uuid of the identity provider.
    directory_service_uuid:
        type: str
        description: The UUID of the directory service.
    principal_name:
        type: str
        description: The UserPrincipalName of the user from the directory service.
    project:
        type: dict
        description: project that belogs to
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
- name: create local user
  ntnx_users:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    principal_name: "{{principal_name}}"
    directory_service_uuid:  "{{directory_service_uuid}}"
    project:
      uuid: "{{project_uuid}}"
    categories:
      Environment:
        - "Dev"
      AppType:
        - "Default"
  register: result

- name: create idp user
  ntnx_users:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    identity_provider_uuid: "{{identity_provider_uuid}}"
    username: "{{username}}"
  register: result
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The user kind metadata
  returned: always
  type: dict
  sample: {
                "categories": {
                    "AppFamily": "Backup"
                },
                "categories_mapping": {
                    "AppFamily": [
                        "Backup"
                    ]
                },
                "creation_time": "2022-06-09T10:13:38Z",
                "kind": "user",
                "last_update_time": "2022-06-09T10:37:14Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "spec_hash": "00000000000000000000000000000000000000000000000000",
                "spec_version": 14,
                "uuid": "00000000-0000-0000-0000-000000000000"
            }
spec:
  description: An intentful representation of a user spec
  returned: always
  type: dict
  sample: {
                "resources": {
                    "directory_service_user": {
                        "directory_service_reference": {
                            "kind": "directory_service",
                            "uuid": "00000000-0000-0000-0000-000000000000"
                        },
                        "user_principal_name": "test_custom@qa.nucalm.io"
                    }
                }
            }
status:
  description: An intentful representation of a user status
  returned: always
  type: dict
  sample: {
                "execution_context": {
                    "task_uuid": [
                        "00000000-0000-0000-0000-000000000000"
                    ]
                },
                "name": "test_custom@qa.nucalm.io",
                "resources": {
                    "access_control_policy_reference_list": [],
                    "directory_service_user": {
                        "default_user_principal_name": "test_custom@qa.nucalm.io",
                        "directory_service_reference": {
                            "kind": "directory_service",
                            "name": "qanucalm",
                            "uuid": "00000000-0000-0000-0000-000000000000"
                        },
                        "user_principal_name": "test_custom@qa.nucalm.io"
                    },
                    "display_name": null,
                    "projects_reference_list": [
                        {
                            "kind": "project",
                            "name": "default",
                            "uuid": "00000000-0000-0000-0000-000000000000"
                        }
                    ],
                    "resource_usage_summary": {
                        "resource_domain": {
                            "resources": []
                        }
                    },
                    "user_type": "DIRECTORY_SERVICE"
                },
                "state": "COMPLETE"
            }

user_uuid:
  description: The created user uuid
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.users import Users  # noqa: E402


def get_module_spec():

    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    module_args = dict(
        user_uuid=dict(type="str"),
        principal_name=dict(type="str"),
        username=dict(type="str"),
        directory_service_uuid=dict(type="str"),
        identity_provider_uuid=dict(type="str"),
        project=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        remove_categories=dict(type="bool", default=False),
        categories=dict(type="dict", required=False),
    )
    return module_args


def create_user(module, result):
    user = Users(module)
    spec, error = user.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating create user Spec", **result)
    if module.check_mode:
        result["response"] = spec
        return

    # create user
    resp = user.create(spec)
    user_uuid = resp["metadata"]["uuid"]
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["user_uuid"] = user_uuid
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        # get the user
        resp = user.read(user_uuid)

    result["response"] = resp


def delete_user(module, result):
    uuid = module.params["user_uuid"]
    if not uuid:
        result["error"] = "Missing parameter user_uuid"
        module.fail_json(msg="Failed deleting user", **result)

    user = Users(module)
    resp = user.delete(uuid)
    result["response"] = resp
    result["changed"] = True
    task_uuid = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)


def run_module():
    # mutually_exclusive_list have params which are not allowed together
    mutually_exclusive_list = [
        ("categories", "remove_categories"),
        ("identity_provider_uuid", "directory_service_uuid"),
        ("username", "principal_name"),
    ]
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("user_uuid",)),
        ],
        required_together=[
            ("username", "identity_provider_uuid"),
            ("principal_name", "directory_service_uuid"),
        ],
        mutually_exclusive=mutually_exclusive_list,
    )
    utils.remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "user_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_user(module, result)
    else:
        delete_user(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
