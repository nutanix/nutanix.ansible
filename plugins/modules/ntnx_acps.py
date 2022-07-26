#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_acps
short_description: acp module which suports acp Create, update and delete operations
version_added: 1.4.0
description: 'Create, Update, Delete acp'
options:
  name:
    description: acp Name
    required: False
    type: str
  acp_uuid:
    description: acp UUID
    type: str
  desc:
    description: The description of the association of a role to a user in a given context
    required: False
    type: str
  user_uuids:
    type: list
    elements: str
    description: The User(s) uuid being assigned a given role.
  user_group_uuids:
    type: list
    elements: str
    description: The User group(s) uuid being assigned a given role.
  filters:
    type: list
    elements: dict
    description: The list of filters, which define the entities.
    suboptions:
        scope_filter:
            type: list
            elements: dict
            description: A list of Scope filter expressions.
            suboptions:
                lhs:
                     type: str
                     description: The left hand side of an expression.
                     choices: ["CATEGORY", "PROJECT", "CLUSTER", "VPC"]
                operator:
                    type: str
                    description: The operator of the filter expression.
                    choices: ["IN", "IN_ALL", "NOT_IN"]
                rhs:
                    type: dict
                    description: The right hand side of an expression.
                    suboptions:
                        collection:
                            type: str
                            description: A representative term for supported groupings of entities. ALL = All the entities of a given kind.
                            choices: ["ALL", "SELF_OWNED"]
                        categories:
                            type: dict
                            description: The category values represented as a dictionary of key -> list of values. e.g.{"env":["env1", "env2"]}
                        uuid_list:
                            type: list
                            elements: str
                            description: The explicit list of UUIDs for the given kind.
        entity_filter:
            type: list
            elements: dict
            description: A list of Entity filter expressions.
            suboptions:
                lhs:
                        type: str
                        description: The left hand side of an expression.
                operator:
                        type: str
                        description: The operator of the filter expression.
                        choices: ["IN", "NOT_IN"]
                rhs:
                    type: dict
                    description: The right hand side of an expression.
                    suboptions:
                        collection:
                            type: str
                            description: A representative term for supported groupings of entities. ALL = All the entities of a given kind.
                            choices: ["ALL", "SELF_OWNED"]
                        categories:
                            type: dict
                            description: The category values represented as a dictionary of key -> list of values. e.g.{"env":["env1", "env2"]}
                        uuid_list:
                            type: list
                            elements: str
                            description: The explicit list of UUIDs for the given kind.
  role:
    type: dict
    description: The reference to a role
    suboptions:
        name:
          description: the name of th role
          required: False
          type: str
        uuid:
          description: the uuid of the role
          required: False
          type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Create min ACP
  ntnx_acps:
    validate_certs: False
    state: present
    nutanix_host: "{{ IP }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    wait: true
    name: MinACP
    role:
      uuid: '{{ role.uuid }}'

- name: Create ACP with user reference
  ntnx_acps:
    validate_certs: False
    state: present
    nutanix_host: "{{ IP }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: acp_with_user_reference
    role:
      uuid: "{{ role.uuid }}"
    user_uuids:
      - "{{ user_uuid }}"

- name: Create ACP with user ad user group reference
  ntnx_acps:
    validate_certs: False
    state: present
    nutanix_host: "{{ IP }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: acp_with_user_and_user_group_reference
    role:
      uuid: "{{ role.uuid }}"
    user_uuids:
      - "{{ user_uuid }}"
    user_group_uuids:
      - "{{ user_group_uuid }}"

- name: Create ACP with all specfactions
  ntnx_acps:
    validate_certs: False
    state: present
    nutanix_host: "{{ IP }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: acp_with_all_specfactions
    role:
      uuid: "{{ role.uuid }}"
    user_uuids:
      - "{{ user_uuid }}"
    user_group_uuids:
      - "{{ user_group_uuid }}"
    filters:
      - scope_filter:
          -
            lhs: PROJECT
            operator: IN
            rhs:
              uuid_list:
                - "{{ project.uuid }}"
        entity_filter:
          -
            lhs: ALL
            operator: IN
            rhs:
              collection: ALL
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: '3.1'
metadata:
  description: Metadata for ACP output
  returned: always
  type: dict
  sample:
    categories: {}
    categories_mapping: {}
    creation_time: '2022-06-15T11:59:38Z'
    kind: access_control_policy
    last_update_time: '2022-06-15T11:59:41Z'
    owner_reference:
      kind: user
      name: admin
      uuid: 00000000000-0000-0000-0000-00000000000
    spec_hash: '00000000000000000000000000000000000000000000000000'
    spec_version: 0
    uuid: 00000000000-0000-0000-0000-00000000000
spec:
  description: An intentful representation of a subnet spec
  returned: always
  type: dict
  sample:
    description: desc,
    name: name,
    resources:
        filter_list:
            context_list:
                entity_filter_expression_list:
                    left_hand_side:
                        entity_type: ALL
                    operator: IN,
                    right_hand_side:
                        collection: ALL
                scope_filter_expression_list:
                    left_hand_side: PROJECT,
                    operator: IN,
                    right_hand_side:
                        uuid_list:
                            00000000000-0000-0000-0000-00000000000
        role_reference:
            kind: role,
            uuid: 00000000000-0000-0000-0000-00000000000
        user_group_reference_list:
            kind: user_group,
            uuid: 00000000000-0000-0000-0000-00000000000
        user_reference_list:
                kind: user,
                uuid: 00000000000-0000-0000-0000-00000000000
status:
  description: An intentful representation of a ACP status
  returned: always
  type: dict
  sample: {
        "description": "desc",
        "execution_context": {
            "task_uuid": "00000000000-0000-0000-0000-00000000000"
        },
        "is_system_defined": false,
        "name": "name",
        "resources": {
            "filter_list": {
                "context_list": {
                    "entity_filter_expression_list": {
                        "left_hand_side": {
                            "entity_type": "ALL"
                        },
                        "operator": "IN",
                        "right_hand_side": {
                            "collection": "ALL"
                        }
                    },
                    "scope_filter_expression_list": {
                        "left_hand_side": "PROJECT,",
                        "operator": "IN,",
                        "right_hand_side": {
                            "uuid_list": "00000000000-0000-0000-0000-00000000000"
                        }
                    }
                }
            },
            "role_reference": {
                "kind": "role,",
                "name": "Project Admin,",
                "uuid": "00000000000-0000-0000-0000-00000000000"
            },
            "user_group_reference_list": {
                "kind": "user_group,",
                "name": "cn=sspadmins,cn=users,dc=qa,dc=nucalm,dc=io,",
                "uuid": "00000000000-0000-0000-0000-00000000000"
            },
            "user_reference_list": {
                "kind": "user,",
                "name": "idpuser1@calmsaastest.com,",
                "uuid": "00000000000-0000-0000-0000-00000000000"
            }
        },
        "state": "COMPLETE"
    }
acp_uuid:
  description: The created acp's uuid
  returned: always
  type: str
  sample: 00000000000-0000-0000-0000-00000000000
task_uuid:
  description: The task uuid for the creation
  returned: always
  type: str
  sample: 00000000000-0000-0000-0000-00000000000
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.acps import ACP  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    rhs_spec = dict(
        collection=dict(type="str", choices=["ALL", "SELF_OWNED"]),
        categories=dict(type="dict"),
        uuid_list=dict(type="list", elements="str"),
    )

    scope_context_spec = dict(
        lhs=dict(type="str", choices=["CATEGORY", "PROJECT", "CLUSTER", "VPC"]),
        operator=dict(type="str", choices=["IN", "IN_ALL", "NOT_IN"]),
        rhs=dict(type="dict", options=rhs_spec),
    )

    entity_context_spec = dict(
        lhs=dict(type="str"),
        operator=dict(type="str", choices=["IN", "NOT_IN"]),
        rhs=dict(type="dict", options=rhs_spec),
    )

    filter_spec = dict(
        scope_filter=dict(type="list", elements="dict", options=scope_context_spec),
        entity_filter=dict(type="list", elements="dict", options=entity_context_spec),
    )

    module_args = dict(
        name=dict(type="str"),
        acp_uuid=dict(type="str"),
        desc=dict(type="str"),
        user_uuids=dict(type="list", elements="str"),
        user_group_uuids=dict(type="list", elements="str"),
        role=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        filters=dict(type="list", elements="dict", options=filter_spec),
    )

    return module_args


def create_acp(module, result):
    acp = ACP(module)
    spec, error = acp.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating acp spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = acp.create(spec)
    acp_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["acp_uuid"] = acp_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = acp.read(acp_uuid)
        result["response"] = resp


def update_acp(module, result):
    acp_uuid = module.params["acp_uuid"]
    state = module.params.get("state")

    acp = ACP(module)
    resp = acp.read(acp_uuid)
    result["response"] = resp
    utils.strip_extra_attrs(resp["status"], resp["spec"])
    resp.pop("status")

    spec, error = acp.get_spec(resp)

    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating ACP spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    if utils.check_for_idempotency(spec, resp, state=state):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change")

    resp = acp.update(spec, acp_uuid)
    acp_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["acp_uuid"] = acp_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = acp.read(acp_uuid)
        result["response"] = resp


def delete_acp(module, result):
    acp_uuid = module.params["acp_uuid"]
    if not acp_uuid:
        result["error"] = "Missing parameter acp_uuid in playbook"
        module.fail_json(msg="Failed deleting acp", **result)

    acp = ACP(module)
    resp = acp.delete(acp_uuid)
    result["changed"] = True
    result["response"] = resp
    result["acp_uuid"] = acp_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid)
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "acp_uuid"), True),
            ("state", "present", ("role", "acp_uuid"), True),
            ("state", "absent", ("acp_uuid",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "acp_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "absent":
        delete_acp(module, result)
    elif module.params.get("acp_uuid"):
        update_acp(module, result)
    else:
        create_acp(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
