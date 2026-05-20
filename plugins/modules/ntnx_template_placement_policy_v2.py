#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_template_placement_policy_v2
short_description: Manage template placement policies in Nutanix Prism Central
description:
    - This module allows you to create, update, and delete template placement policies in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
version_added: "2.6.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a template placement policy) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Update a template placement policy) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Delete a template placement policy) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - The unique identifier of the template placement policy.
            - This parameter is required for update and delete operations.
        required: false
        type: str
    name:
        description:
            - The name of the template placement policy.
        required: false
        type: str
    description:
        description:
            - The description of the template placement policy.
        required: false
        type: str
    placement_type:
        description:
            - The placement type of the template placement policy.
        required: false
        choices:
            - SOFT
        type: str
    content_filter:
        description:
            - The filter for selecting templates for the template placement policy.
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
    cluster_filter:
        description:
            - The filter for selecting clusters for the template placement policy.
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
author:
 - Abhinav Bansal (@abhinavbansal29)
 - George Ghawali (@george-ghawali)
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2

"""

EXAMPLES = r"""
- name: Create a template placement policy
  nutanix.ncp.ntnx_template_placement_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: my_template_policy
    description: My template placement policy
    placement_type: SOFT
    content_filter:
      type: CATEGORIES_MATCH_ALL
      category_ext_ids:
        - "category-ext-id-1"
    cluster_filter:
      type: CATEGORIES_MATCH_ANY
      category_ext_ids:
        - "category-ext-id-2"
    state: present
    wait: true

- name: Update a template placement policy
  nutanix.ncp.ntnx_template_placement_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "605a0cf9-d04e-3be7-911b-1e6f193f6eb9"
    name: my_template_policy_updated
    description: Updated description
    state: present
    wait: true

- name: Delete a template placement policy
  nutanix.ncp.ntnx_template_placement_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "605a0cf9-d04e-3be7-911b-1e6f193f6eb9"
    state: absent
    wait: true
"""


RETURN = r"""
response:
    description:
        - The response from the template placement policy operation.
        - It will be task response if C(wait) is false.
    type: dict
    returned: always
    sample: {
            "cluster_filter": {
                "category_ext_ids": [
                    "605a0cf9-d04e-3be7-911b-1e6f193f6ebe"
                ],
                "type": "CATEGORIES_MATCH_ANY"
            },
            "content_filter": {
                "category_ext_ids": [
                    "98b9dc89-be08-3c56-b554-692b8b676fd1"
                ],
                "type": "CATEGORIES_MATCH_ALL"
            },
            "create_time": "2024-03-25T23:03:17.610346+00:00",
            "description": "policy-description",
            "ext_id": "54fe0ed5-02d8-4588-b10b-3b9736bf3d06",
            "name": "policy-name",
            "placement_type": "SOFT",
            "tenant_id": null
        }
task_ext_id:
    description:
        - The external ID of the task associated with the template placement policy operation.
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
    description: Indicates whether the template placement policy was changed.
    type: bool
    returned: always
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent or check mode (in delete operation)
    type: str
    sample: "Failed generating create Template Placement Policy Spec"
error:
    description: The error message if an error occurred during the template placement policy operation.
    type: str
    returned: when an error occurs
skipped:
    description: Indicates whether the template placement policy operation was skipped.
    type: bool
    returned: when the operation is skipped
failed:
    description: Indicates whether the operation failed.
    type: bool
    returned: on failure
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
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
    get_template_placement_policy_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_template_placement_policy  # noqa: E402

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
    Returns the module specification for template placement policy.
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
        placement_type=dict(type="str", choices=["SOFT"], required=False),
        content_filter=dict(
            type="dict",
            required=False,
            options=entity_filter,
            obj=vmm_sdk.CategoriesFilter,
        ),
        cluster_filter=dict(
            type="dict",
            required=False,
            options=entity_filter,
            obj=vmm_sdk.CategoriesFilter,
        ),
    )
    return module_args


def create_policy(module, api_instance, result):
    """
    Create a new template placement policy.
    Args:
        module: Ansible module
        api_instance: TemplatePlacementPoliciesApi instance
        result: Result dict to populate
    """
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.TemplatePlacementPolicy()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create Template Placement Policy Spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_template_placement_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Template Placement Policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        ext_id = get_entity_ext_id_from_task(
            task, rel=Tasks.RelEntityType.TEMPLATE_PLACEMENT_POLICY
        )
        if ext_id:
            result["ext_id"] = ext_id
            policy = get_template_placement_policy(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(policy.to_dict())

    result["changed"] = True


def update_policy(module, api_instance, result):
    """
    Update an existing template placement policy.
    Args:
        module: Ansible module
        api_instance: TemplatePlacementPoliciesApi instance
        result: Result dict to populate
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_template_placement_policy(module, api_instance, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Template Placement Policy update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if current_spec == update_spec:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "unable to fetch etag for updating Template Placement Policy", **result
        )

    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.update_template_placement_policy_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Template Placement Policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        updated_policy = get_template_placement_policy(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(updated_policy.to_dict())

    result["changed"] = True


def delete_policy(module, api_instance, result):
    """
    Delete a template placement policy.
    Args:
        module: Ansible module
        api_instance: TemplatePlacementPoliciesApi instance
        result: Result dict to populate
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Policy with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_template_placement_policy(module, api_instance, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "unable to fetch etag for deleting Template Placement Policy", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = api_instance.delete_template_placement_policy_by_id(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Template Placement Policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
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

    api_instance = get_template_placement_policy_api_instance(module)

    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_policy(module, api_instance, result)
        else:
            create_policy(module, api_instance, result)
    else:
        delete_policy(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
