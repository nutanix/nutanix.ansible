#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from email.policy import default

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_image_placement_policy
short_description: image placement policy module which supports Create, update and delete operations
version_added: 1.0.0
description: "Create, Update, Delete image placement policy"
options:
    state:
        description:
        - Specify state
        - If C(state) is set to C(present) then the operation will be  create the item.
        - if C(state) is set to C(present) and C(policy_uuid) is given then it will update that image placement policy.
        - if C(state) is set to C(present) then C(image_uuid) or one of C(name), C(image_categories), C(cluster_categories) needs to be set.
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
    name:
        description: 
            - policy name
            - allowed in update
        required: false
        type: str
    policy_uuid:
        description: 
            - image placement policy of existig uuid
            - required only when updating or deleting
        type: str
        required: false
    desc:
        description: 
            - A description for policy
            - allowed in update
        required: false
        type: str
    placement_type:
        description:
            - placement type of the policy.
            - allowed in update
        type: str
        required: false
        choices:
            - hard
            - soft
        default: soft
    image_categories:
        description:
            - categories for images which needs to be affected by this policy
            - allowed in update
            - this field cannot be empty
        type: dict
        required: false
    cluster_categories:
        description:
            - categories for clusters which needs to be affected by this policy
            - allowed in update
            - this field cannot be empty
        type: dict
        required: false
    categories:
        description:
            - Categories for the policy. This allows setting up multiple values from a single key.
            - In update, it will override he existing categories attached to policy
            - Mutually exclusive with C(remove_categories)
        required: false
        type: dict
    remove_categories:
        description:
            - When set will remove all categories attached to the policy.
            - Mutually exclusive ith C(categories)
            - It doesnot remove C(image_categories) or C(cluster_categories)
        required: false
        type: bool
        default: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)    
"""

EXAMPLES = r"""
- name: Create image placement policy with minimal spec
  ntnx_image_placement_policy:
    state: "present"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    name: "test_policy_1"
    image_categories: 
      AppFamily:
        - Backup
    cluster_categories:
      AppTier:
        - Default
  register: result

- name: Create image placement policy with all specs and hard type
  ntnx_image_placement_policy:
    state: "present"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    name: "test_policy_2"
    desc: "test_policy_2_desc"
    placement_type: hard
    categories:
      Environment:
        - "Dev"
      AppType:
        - "Default"
    image_categories: 
      AppFamily:
        - Backup
        - Networking
    cluster_categories:
      AppTier:
        - Default
  register: result

- name: Update image placement policy 
  ntnx_image_placement_policy:
    state: "present"
    policy_uuid: "<policy-uuid>"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    name: "test_policy_2-uodated"
    desc: "test_policy_2_desc-updated"
    placement_type: hard
    categories:
      Environment:
        - "Dev"
    image_categories: 
      AppFamily:
        - Backup
    cluster_categories:
      AppTier:
        - Default
  register: result

- name: Remove all categories attached to policy
  ntnx_image_placement_policy:
    state: "present"
    policy_uuid: "<policy-uuid>"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    remove_categories: True
  register: result

- name: Delete image placement policy
  ntnx_image_placement_policy:
    state: "absent"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    state: absent
    policy_uuid: "<policy-uuid>"
  register: result
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The image placement policy type kind metadata
  returned: always
  type: dict
  sample: {
                "categories": {},
                "categories_mapping": {},
                "creation_time": "2022-06-16T08:03:59Z",
                "kind": "image_placement_policy",
                "last_update_time": "2022-06-16T08:04:01Z",
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
  description: An intentful representation of a image placement policy spec
  returned: always
  type: dict
  sample: {
                "description": "check123233",
                "name": "test_policy_1",
                "resources": {
                    "cluster_entity_filter": {
                        "params": {
                            "AppFamily": [
                                "Networking"
                            ]
                        },
                        "type": "CATEGORIES_MATCH_ANY"
                    },
                    "image_entity_filter": {
                        "params": {
                            "AppFamily": [
                                "Backup",
                                "Databases"
                            ]
                        },
                        "type": "CATEGORIES_MATCH_ANY"
                    },
                    "placement_type": "AT_LEAST"
                }
            }
status:
  description: An intentful representation of a image placement policy status
  returned: always
  type: dict
  sample: {
                "description": "check123233",
                "execution_context": {
                    "task_uuid": [
                        "00000000-0000-0000-0000-000000000000"
                    ]
                },
                "name": "test_policy_1",
                "resources": {
                    "cluster_entity_filter": {
                        "params": {
                            "AppFamily": [
                                "Networking"
                            ]
                        },
                        "type": "CATEGORIES_MATCH_ANY"
                    },
                    "image_entity_filter": {
                        "params": {
                            "AppFamily": [
                                "Backup",
                                "Databases"
                            ]
                        },
                        "type": "CATEGORIES_MATCH_ANY"
                    },
                    "placement_type": "AT_LEAST"
                },
                "state": "COMPLETE"
            }
policy_uuid:
  description: The created image placement policy uuid
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.image_placement_policy import ImagePlacementPolicy


def get_module_spec():
    module_args = dict(
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        remove_categories=dict(type="bool", required=False, default=False),
        placement_type=dict(
            type="str", choices=["hard", "soft"], default="soft", required=False
        ),
        image_categories=dict(type="dict", required=False),
        cluster_categories=dict(type="dict", required=False),
        categories=dict(type="dict", required=False),
        policy_uuid=dict(type="str", required=False),
    )
    return module_args


def create_policy(module, result):
    policy_obj = ImagePlacementPolicy(module)
    spec, error = policy_obj.get_spec()
    if error:
        result["error"] = error
        module.fail_json(
            msg="Failed generating create Image Placement Policies Spec", **result
        )
    if module.check_mode:
        result["response"] = spec
        return

    # create image placement policies
    resp = policy_obj.create(spec)
    policy_uuid = resp["metadata"]["uuid"]
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["policy_uuid"] = policy_uuid
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = policy_obj.read(policy_uuid)

    result["response"] = resp


def update_policy(module, result):
    policy_obj = ImagePlacementPolicy(module)
    policy_uuid = module.params.get("policy_uuid")
    if not policy_uuid:
        result["error"] = "Missing parameter policy_uuid in task"
        module.fail_json(msg="Failed updating image placement policy", **result)

    # read the current state of policy
    resp = policy_obj.read(policy_uuid)
    utils.strip_extra_attrs_from_status(resp["status"], resp["spec"])
    resp["spec"] = resp.pop("status")

    # new spec for updating policy
    update_spec, error = policy_obj.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(
            msg="Failed generating Image Placement Policy update spec", **result
        )

    # check for idempotency using update spec and current spec
    if resp == update_spec:
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. Refer docs to check for fields which can be updated"
        )

    result["policy_uuid"] = policy_uuid
    if module.check_mode:
        result["response"] = update_spec
        return

    # update policy
    resp = policy_obj.update(update_spec, uuid=policy_uuid)
    policy_uuid = resp["metadata"]["uuid"]
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["policy_uuid"] = policy_uuid

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = policy_obj.read(policy_uuid)

    result["changed"] = True
    result["response"] = resp


def delete_policy(module, result):
    policy_uuid = module.params["policy_uuid"]
    if not policy_uuid:
        result["error"] = "Missing parameter policy_uuid in task"
        module.fail_json(msg="Failed deleting Image placement policy", **result)

    policy_obj = ImagePlacementPolicy(module)
    resp = policy_obj.delete(policy_uuid)
    result["response"] = resp
    result["changed"] = True
    task_uuid = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)


def run_module():
    required_one_of_list = [
        ("policy_uuid", "name"),
        ("policy_uuid", "image_categories"),
        ("policy_uuid", "cluster_categories"),
    ]
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_one_of=required_one_of_list,
        mutually_exclusive=[
            ("categories", "remove_categories"),
        ],
        required_if=[("state", "absent", ("policy_uuid",))],
    )
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "policy_uuid": None,
    }
    utils.remove_param_with_none_value(module.params)
    state = module.params["state"]
    if state == "present":
        if module.params.get("policy_uuid"):
            update_policy(module, result)
        else:
            create_policy(module, result)
    elif state == "absent":
        delete_policy(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
