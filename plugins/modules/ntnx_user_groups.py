#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_groups
short_description: user_groups module which supports pc user_groups management CRUD operations
version_added: 1.4.0
description: "Create, Update, Delete user_groups"
options:
    state:
        description:
        - Specify state
        - If C(state) is set to C(present) then the operation will be  create the item.
        - if C(state) is set to C(present) and C(user_group_uuid) is given then it will update that user_group.
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
    user_groupname:
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
    identity_provider:
        type: dict
        description: An Identity Provider user_group.
        suboptions:
            name:
                type: str
                description: The user_groupname from the identity provider. Name Id for SAML Identity Provider.
            uuid:
                type: str
                description: The uuid from the identity provider. Name Id for SAML Identity Provider.
    directory_service:
        type: dict
        description: A Directory Service user_group.
        suboptions:
            name:
                type: str
                description: The user_groupPrincipalName of the user_group from the directory service.
            uuid:
                type: str
                description: The user_groupPrincipal UUID of the user_group from the directory service.
    principal_name:
        type: str
        description: The user_groupPrincipalName of the user_group from the directory service.
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""

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
                "categories": {
                    "AppFamily": "Backup"
                },
                "categories_mapping": {
                    "AppFamily": [
                        "Backup"
                    ]
                },
                "creation_time": "2022-06-09T10:13:38Z",
                "kind": "user_group",
                "last_update_time": "2022-06-09T10:37:14Z",
                "owner_reference": {
                    "kind": "user_group",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "spec_hash": "00000000000000000000000000000000000000000000000000",
                "spec_version": 14,
                "uuid": "00000000-0000-0000-0000-000000000000"
            }
spec:
  description: An intentful representation of a user_group spec
  returned: always
  type: dict
  sample: {
  #TODO
  }
status:
  description: An intentful representation of a user_group status
  returned: always
  type: dict
  sample: {
  #TODO
  }
user_group_uuid:
  description: The created user_group uuid
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.user_groups import UserGroups  # noqa: E402


def get_module_spec():
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    module_args = dict(
        user_group_uuid=dict(type="str"),
        name=dict(type="str"),
        remove_categories=dict(type="bool", default=False),
        categories=dict(type="dict", required=False),
    )
    return module_args


def create_user_group(module, result):
    user_group = UserGroups(module)
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

    user_group = UserGroups(module)
    resp = user_group.delete(uuid)
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
