#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_images
short_description: images module which supports pc images management CRUD operations
version_added: 1.0.0
description: "Create, Update, Delete images"
options:
    state:
        description:
        - Specify state
        - If C(state) is set to C(present) then the operation will be  create the item.
        - if C(state) is set to C(present) and C(image_uuid) is given then it will update that image.
        - if C(state) is set to C(present) then C(image_uuid), C(source_uri) and C(source_path) are mutually exclusive.
        - if C(state) is set to C(present) then C(image_uuid) or C(name) needs to be set.
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
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.image_placement_policy import ImagePlacementPolicy


def get_module_spec():
    module_args = dict(
        name = dict(type="str", required=False),
        desc = dict(type="str", required=False),
        placement_type = dict(type="str", choices=["hard", "soft"], default="soft", required=False),
        image_categories = dict(type="dict", required=False),
        cluster_categories = dict(type="dict", required=False),
        categories=dict(type="dict", required=False),
        policy_uuid=dict(type="str", required=False)
    )
    return module_args

def create_policy(module, result):
    policy_obj = ImagePlacementPolicy(module)
    spec, error = policy_obj.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating create Image Placement Policies Spec", **result)
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
        module.fail_json(msg="Failed generating Image Placement Policy update spec", **result)
    
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
        ("policy_uuid","name"),
        ("policy_uuid","image_categories"),
        ("policy_uuid","cluster_categories")
    ]
    module = BaseModule(
        argument_spec = get_module_spec(),
        supports_check_mode = True,
        required_one_of = required_one_of_list,
        required_if = [
            ("state", "absent",("policy_uuid",))
        ]
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
