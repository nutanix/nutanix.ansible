#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_consistency_rules_v2
short_description: Create, Update, or Delete a Consistency Rule in a Nutanix Protection Policy
version_added: "2.7.0"
description:
    - Create, Update, or Delete a Consistency Rule inside a Protection Policy in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Create a Consistency Rule) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Project Manager, Super Admin
    - >-
      B(Update a Consistency Rule) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Project Manager, Super Admin
    - >-
      B(Delete a Consistency Rule) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
    state:
        description:
            - If C(state) is set to C(present) and C(ext_id) is not provided then
              the operation will create a Consistency Rule.
            - If C(state) is set to C(present) and C(ext_id) is provided then
              the operation will update a Consistency Rule.
            - If C(state) is set to C(absent) and C(ext_id) is provided then
              the operation will delete a Consistency Rule.
        type: str
        required: false
        choices:
            - present
            - absent
        default: present
    protection_policy_ext_id:
        description:
            - The External ID of the parent Protection Policy under which the
              Consistency Rule resides.
            - Required for all Create, Update, and Delete operations.
        type: str
        required: true
    ext_id:
        description:
            - The External ID of the Consistency Rule.
            - Required for update and delete operations.
        type: str
        required: false
    name:
        description:
            - Name of the consistency rule.
        type: str
        required: false
    category_ids:
        description:
            - Specifies the list of External IDs of categories that must form the
              consistency rule. This consistently protects any VM or volume group
              associated with this category. The number of entities attached to
              these categories should not exceed 32, and should reside in the same
              cluster.
        type: list
        elements: str
        required: false
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        default: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create a Consistency Rule under a Protection Policy
  nutanix.ncp.ntnx_consistency_rules_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    protection_policy_ext_id: "0985aafc-8cb8-4e22-b863-3ff5f91c911e"
    name: "example-consistency-rule"
    category_ids:
      - "0d2c792d-8687-4e99-95f7-3c7cc401fe1a"
  register: result

- name: Update a Consistency Rule
  nutanix.ncp.ntnx_consistency_rules_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    protection_policy_ext_id: "0985aafc-8cb8-4e22-b863-3ff5f91c911e"
    ext_id: "{{ result.ext_id }}"
    name: "example-consistency-rule-updated"
    category_ids:
      - "0d2c792d-8687-4e99-95f7-3c7cc401fe1a"
  register: updated

- name: Delete a Consistency Rule
  nutanix.ncp.ntnx_consistency_rules_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    protection_policy_ext_id: "0985aafc-8cb8-4e22-b863-3ff5f91c911e"
    ext_id: "{{ result.ext_id }}"
  register: deleted
"""

RETURN = r"""
response:
    description:
        - Response for Consistency Rule operations.
        - Consistency Rule details if C(wait) is true.
        - Task details if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "tenant_id": "fd4a402d-b2c7-41dd-9fdf-62b9a1d7fe18",
            "ext_id": "84196575-327d-4ba5-9c78-9dff781217f4",
            "links": [
                {
                    "href": "string",
                    "rel": "string"
                }
            ],
            "name": "Consistency_Rule_1",
            "category_ids": [
                "0d2c792d-8687-4e99-95f7-3c7cc401fe1a"
            ]
        }
task_ext_id:
    description:
        - The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
ext_id:
    description:
        - The external ID of the Consistency Rule.
    returned: always
    type: str
    sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
skipped:
    description: This indicates whether the task was skipped
    returned: always
    type: bool
    sample: false
error:
    description: This indicates the error message if any error occurred
    returned: When an error occurs
    type: str
failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent or check mode
    type: str
    sample: "Api Exception raised while creating consistency rule"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_consistency_rules_api_instance,
    get_etag,
)
from ..module_utils.v4.data_policies.helpers import get_consistency_rule  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_datapolicies_py_client as data_policies_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as data_policies_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        protection_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        category_ids=dict(type="list", elements="str", required=False),
    )
    return module_args


def create_consistency_rule(module, result, api_instance):
    validate_required_params(module, ["name", "category_ids"])
    protection_policy_ext_id = module.params.get("protection_policy_ext_id")
    sg = SpecGenerator(module)
    default_spec = data_policies_sdk.ConsistencyRule()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create consistency rule spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.create_consistency_rule(
            protectionPolicyExtId=protection_policy_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating consistency rule",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_data = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_data.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_data, rel=TASK_CONSTANTS.RelEntityType.CONSISTENCY_RULE
        )
        if ext_id:
            result["ext_id"] = ext_id
            fetched = get_consistency_rule(
                module, api_instance, protection_policy_ext_id, ext_id
            )
            result["response"] = strip_internal_attributes(fetched.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Consistency Rule"
                ),
                msg="Failed to get entity ext_id from task for Consistency Rule",
            )
    result["changed"] = True


def check_consistency_rule_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    return old_spec_dict == update_spec_dict


def update_consistency_rule(module, result, api_instance):
    protection_policy_ext_id = module.params.get("protection_policy_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_consistency_rule(
        module, api_instance, protection_policy_ext_id, ext_id
    )
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating consistency rule", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update consistency rule spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_consistency_rule_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    strip_read_only_fields(update_spec, fields=["links", "tenant_id"])

    kwargs = {"if_match": etag}
    try:
        resp = api_instance.update_consistency_rule_by_id(
            protectionPolicyExtId=protection_policy_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating consistency rule",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        fetched = get_consistency_rule(
            module, api_instance, protection_policy_ext_id, ext_id
        )
        result["response"] = strip_internal_attributes(fetched.to_dict())
    result["changed"] = True


def delete_consistency_rule(module, result, api_instance):
    protection_policy_ext_id = module.params.get("protection_policy_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Consistency Rule with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    try:
        resp = api_instance.delete_consistency_rule_by_id(
            protectionPolicyExtId=protection_policy_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting consistency rule",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, raise_error=True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
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
            msg=missing_required_lib("ntnx_datapolicies_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_consistency_rules_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_consistency_rule(module, result, api_instance)
        else:
            create_consistency_rule(module, result, api_instance)
    else:
        delete_consistency_rule(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
