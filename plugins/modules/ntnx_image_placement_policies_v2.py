#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_image_placement_policies_v2
short_description: Manage image placement policies in Nutanix Prism Central
description:
    - This module allows you to create, update, and delete image placement policies in Nutanix Prism Central.
    - This module allows you to suspend and resume image placement policies in Nutanix Prism Central.
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    ext_id:
        description:
            - The unique identifier of the image placement policy.
            - This parameter is required for update and delete operations.
        required: false
        type: str
    name:
        description:
            - The name of the image placement policy.
        required: false
        type: str
    description:
        description:
            - The description of the image placement policy.
        required: false
        type: str
    placement_type:
        description:
            - The placement type of the image placement policy.
        required: false
        choices:
            - HARD
            - SOFT
        type: str
    image_entity_filter:
        description:
            - The filter for selecting images for the image placement policy.
        required: false
        type: dict
        suboptions:
            type:
                description:
                    - The type of filter to apply.
                required: true
                choices:
                    - CATEGORIES_MATCH_ALL
                    - CATEGORIES_MATCH_ANY
                type: str
            category_ext_ids:
                description:
                    - The list of category external IDs to match.
                required: true
                type: list
                elements: str
    cluster_entity_filter:
        description:
            - The filter for selecting clusters for the image placement policy.
        required: false
        type: dict
        suboptions:
            type:
                description:
                    - The type of filter to apply.
                required: true
                choices:
                    - CATEGORIES_MATCH_ALL
                    - CATEGORIES_MATCH_ANY
                type: str
            category_ext_ids:
                description:
                    - The list of category external IDs to match.
                required: true
                type: list
                elements: str
    enforcement_state:
        description:
            - The enforcement state of the image placement policy.
            - This parameter is required for suspending and resuming the image placement policy.
        required: false
        choices:
            - ACTIVE
            - SUSPENDED
        type: str
    should_cancel_running_tasks:
        description:
            - Whether to cancel running tasks when suspending the image placement policy.
        required: false
        type: bool
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then the operation will be to create the item.
            - if C(state) is set to C(present) and C(ext_id) is given then it will update that policy.
            - if C(state) is set to C(present) then C(ext_id) or C(name) needs to be set.
            - >-
                If C(state) is set to C(absent) and if the item exists, then
                item is removed.
        choices:
            - present
            - absent
        type: str
        default: present
    wait:
        description: Wait for the CRUD operation to complete.
        type: bool
        required: false
        default: True
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
notes:
    - This module follows two steps update process. Configuration update and enforcement state update.
    - If enforcement state is changed, then task_ext_id will have the task id of enforcement state update.
    - Else it will be create, update config or delete task id as per C(state).
"""

EXAMPLES = r"""
- name: Create an image placement policy
  ntnx_image_placement_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: my_policy
    description: My image placement policy
    placement_type: HARD
    image_entity_filter:
      type: CATEGORIES_MATCH_ALL
      category_ext_ids:
        - category1
        - category2
    cluster_entity_filter:
      type: CATEGORIES_MATCH_ANY
      category_ext_ids:
        - category3
        - category4
    enforcement_state: ACTIVE
    state: present
    wait: true

- name: Delete an image placement policy
  ntnx_image_placement_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: 605a0cf9-d04e-3be7-911b-1e6f193f6eb9
    state: absent
    wait: true
"""


RETURN = r"""
response:
    description:
        - The response from the image placement policy operation.
        - It will be task response if C(wait) is false.
    type: dict
    returned: always
    sample: {
            "cluster_entity_filter": {
                "category_ext_ids": [
                    "605a0cf9-d04e-3be7-911b-1e6f193f6ebe"
                ],
                "type": "CATEGORIES_MATCH_ANY"
            },
            "create_time": "2024-03-25T23:03:17.610346+00:00",
            "description": "new1-description-updated",
            "enforcement_state": "SUSPENDED",
            "ext_id": "54fe0ed5-02d8-4588-b10b-3b9736bf3d06",
            "image_entity_filter": {
                "category_ext_ids": [
                    "98b9dc89-be08-3c56-b554-692b8b676fd1"
                ],
                "type": "CATEGORIES_MATCH_ALL"
            },
            "last_update_time": "2024-03-25T23:44:01.955468+00:00",
            "links": null,
            "name": "new1-updated",
            "owner_ext_id": "00000000-0000-0000-0000-000000000000",
            "placement_type": "SOFT",
            "tenant_id": null
        }
task_ext_id:
    description:
        - The external ID of the task associated with the image placement policy operation.
        - If enforcement state is changed, then task_ext_id will have the task id of enforcement state update.
    type: str
    returned: when a task is created
    sample: "98b9dc89-be08-3c56-b554-692b8b676fd2"
ext_id:
    description:
        - The external ID of the policy
    type: str
    sample: "98b9dc89-be08-3c56-b554-692b8b676fd2"
    returned: always
changed:
    description: Indicates whether the image placement policy was changed.
    type: bool
    returned: always
error:
    description: The error message if an error occurred during the image placement policy operation.
    type: str
    returned: when an error occurs
skipped:
    description: Indicates whether the image placement policy operation was skipped.
    type: bool
    returned: when the operation is skipped
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_etag,
    get_image_placement_policy_api_instance,
)

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """
    Returns the module specification.
    """
    entity_filter = dict(
        type=dict(
            type="str",
            required=True,
            choices=["CATEGORIES_MATCH_ALL", "CATEGORIES_MATCH_ANY"],
        ),
        category_ext_ids=dict(type="list", required=True, elements="str"),
    )
    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        placement_type=dict(type="str", choices=["HARD", "SOFT"], required=False),
        image_entity_filter=dict(
            type="dict", required=False, options=entity_filter, obj=vmm_sdk.Filter
        ),
        cluster_entity_filter=dict(
            type="dict", required=False, options=entity_filter, obj=vmm_sdk.Filter
        ),
        enforcement_state=dict(
            type="str", choices=["ACTIVE", "SUSPENDED"], required=False
        ),
        should_cancel_running_tasks=dict(type="bool", required=False),
    )
    return module_args


def get_policy(module, api_instance, ext_id):
    try:
        return api_instance.get_placement_policy_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching image placement policy info using ext_id",
        )


def create_policy(module, result):
    policies = get_image_placement_policy_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.PlacementPolicy()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create Image Placement Policy Spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = policies.create_placement_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Image Placement Policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        ext_id = get_entity_ext_id_from_task(
            task, rel=Tasks.RelEntityType.IMAGE_PLACEMENT_POLICY
        )
        policy = get_policy(module, policies, ext_id)
        if ext_id:
            result["ext_id"] = ext_id

            # update policy enforcement state if needed
            if check_if_state_update_required(policy, spec):
                task_ext_id = update_policy_state(module, result, policies, ext_id)
                if task_ext_id:
                    wait_for_completion(module, task_ext_id)
                    result["task_ext_id"] = task_ext_id

            policy = get_policy(module, policies, ext_id)
            result["response"] = strip_internal_attributes(policy.to_dict())

    result["changed"] = True


def check_if_config_update_required(current_spec, update_spec):
    if current_spec == update_spec:
        return False

    lhs = current_spec.to_dict()
    rhs = update_spec.to_dict()
    for key in lhs.keys():
        if key != "enforcement_state" and lhs.get(key) != rhs.get(key):
            return True
    return False


def check_if_state_update_required(current_spec, update_spec):
    if current_spec.enforcement_state == update_spec.enforcement_state:
        return False
    return True


def update_policy_config(module, api_instance, update_spec, ext_id):
    resp = None
    try:
        resp = api_instance.update_placement_policy_by_id(
            extId=ext_id, body=update_spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Image Placement Policy",
        )

    task_ext_id = resp.data.ext_id
    return task_ext_id


def update_policy_state(module, result, policies, ext_id):
    desired_state = module.params.get("enforcement_state")

    policy = get_policy(module, policies, ext_id)
    etag = get_etag(data=policy)
    if not etag:
        return module.fail_json(
            "unable to fetch etag for updating Placement Policy enforcement state",
            **result,
        )

    kwargs = {"if_match": etag}
    resp = None
    if desired_state == vmm_sdk.EnforcementState.SUSPENDED:
        should_cancel_running_tasks = module.params.get("should_cancel_running_tasks")
        spec = vmm_sdk.SuspendPlacementPolicyConfig(
            should_cancel_running_tasks=should_cancel_running_tasks
        )
        try:
            resp = policies.suspend_placement_policy(extId=ext_id, body=spec, **kwargs)
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while suspending given Placement Policy",
            )
    else:
        try:
            resp = policies.resume_placement_policy(extId=ext_id, **kwargs)
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while resuming Placement Policy",
            )
    task_ext_id = resp.data.ext_id
    return task_ext_id


def update_policy(module, result):
    policies = get_image_placement_policy_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_policy(module, policies, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Image Placement Policy update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    state_update_required = check_if_state_update_required(current_spec, update_spec)
    config_update_required = check_if_config_update_required(current_spec, update_spec)

    if not (config_update_required or state_update_required):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    previous_task_ext_id = None
    if config_update_required:
        previous_task_ext_id = update_policy_config(
            module, policies, update_spec, ext_id
        )

    if state_update_required:

        if previous_task_ext_id:
            wait_for_completion(module, previous_task_ext_id)

        previous_task_ext_id = update_policy_state(module, result, policies, ext_id)

    if previous_task_ext_id and module.params.get("wait", False):
        wait_for_completion(module, previous_task_ext_id)

    result["ext_id"] = ext_id

    updated_policy = get_policy(module, policies, ext_id)
    result["response"] = strip_internal_attributes(updated_policy.to_dict())
    result["task_ext_id"] = previous_task_ext_id
    result["changed"] = True


def delete_policy(module, result):
    policies = get_image_placement_policy_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_policy(module, policies, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "unable to fetch etag for deleting Image Placement Policy", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = policies.delete_placement_policy_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Image Placement Policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_policy(module, result)
        else:
            create_policy(module, result)
    else:
        delete_policy(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
