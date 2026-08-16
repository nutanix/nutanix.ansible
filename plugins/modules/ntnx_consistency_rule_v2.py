#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_consistency_rule_v2
short_description: Create, Update, Delete a Consistency Rule of a Protection Policy in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete a Consistency Rule under a Protection Policy in Nutanix Prism Central.
  - A Consistency Rule groups entities (identified by categories) so their recovery points are captured at the same instant.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create a Consistency Rule) -
    Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin
  - >-
    B(Update a Consistency Rule) -
    Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin
  - >-
    B(Delete a Consistency Rule) -
    Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create a consistency rule.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update the consistency rule.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the consistency rule.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  protection_policy_ext_id:
    description:
      - The external identifier of the parent Protection Policy that owns this Consistency Rule.
      - Required for all operations (create, update, delete).
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the Consistency Rule.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the Consistency Rule.
      - Required for create operation.
      - Minimum 1 character, maximum 256 characters.
    type: str
    required: false
  category_ids:
    description:
      - List of Nutanix Category external identifiers whose members are grouped together for consistent snapshots.
      - Required for create operation.
    type: list
    elements: str
    required: false
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
- name: Create a consistency rule under a protection policy
  nutanix.ncp.ntnx_consistency_rule_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    protection_policy_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    name: "consistency_rule_ansible"
    category_ids:
      - "22222222-2222-2222-2222-222222222222"
  register: result
  ignore_errors: true

- name: Update a consistency rule
  nutanix.ncp.ntnx_consistency_rule_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    protection_policy_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    ext_id: "5c9a2d54-1f18-4f0e-b2b4-3a5cee0031b7"
    name: "consistency_rule_ansible_updated"
    category_ids:
      - "33333333-3333-3333-3333-333333333333"
  register: result
  ignore_errors: true

- name: Delete a consistency rule
  nutanix.ncp.ntnx_consistency_rule_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    protection_policy_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    ext_id: "5c9a2d54-1f18-4f0e-b2b4-3a5cee0031b7"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a consistency rule.
    - If the operation is create or update and C(wait) is true, it will return the consistency rule details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "category_ids": ["22222222-2222-2222-2222-222222222222"],
      "ext_id": "5c9a2d54-1f18-4f0e-b2b4-3a5cee0031b7",
      "links": null,
      "name": "consistency_rule_ansible",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the consistency rule.
  returned: always
  type: str
  sample: "5c9a2d54-1f18-4f0e-b2b4-3a5cee0031b7"

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
  returned: When there is an error, module is idempotent or check mode (in delete operation)
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
    get_etag,
    get_protection_policies_api_instance,
)
from ..module_utils.v4.data_policies.helpers import (  # noqa: E402
    get_consistency_rule,
    get_consistency_rule_by_name,
)
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_datapolicies_py_client as data_policies_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_policies_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        protection_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        name=dict(type="str"),
        category_ids=dict(type="list", elements="str"),
    )
    return module_args


def create_consistency_rule(module, api_instance, result):
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

    resp = None
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
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        # The Consistency Rule create task returns the parent Protection
        # Policy in `entities_affected`; the rule's own ext_id is not
        # exposed there. Fall back to looking up the rule by its (unique)
        # name under the protection policy after the task succeeds.
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.CONSISTENCY_RULE
        )
        if not ext_id:
            entity = get_consistency_rule_by_name(
                module,
                api_instance,
                protection_policy_ext_id,
                module.params.get("name"),
            )
            if entity is not None:
                ext_id = getattr(entity, "ext_id", None)
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_consistency_rule(
                module, api_instance, protection_policy_ext_id, ext_id
            )
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to resolve ext_id of the newly created Consistency Rule"
                ),
                msg="Failed to resolve ext_id of the newly created Consistency Rule",
            )
    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):
    if old_spec != update_spec:
        return False
    return True


def update_consistency_rule(module, api_instance, result):
    protection_policy_ext_id = module.params.get("protection_policy_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_consistency_rule(
        module, api_instance, protection_policy_ext_id, ext_id
    )
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating consistency rule", **result
        )
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update consistency rule spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    old_spec_dict = strip_internal_attributes(old_spec.to_dict())
    update_spec_dict = strip_internal_attributes(update_spec.to_dict())
    if check_for_idempotency(old_spec_dict, update_spec_dict):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    kwargs = {"if_match": etag}
    resp = None
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
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        resp = get_consistency_rule(
            module, api_instance, protection_policy_ext_id, ext_id
        )
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_consistency_rule(module, api_instance, result):
    protection_policy_ext_id = module.params.get("protection_policy_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Consistency rule with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
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
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_datapolicies_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    api_instance = get_protection_policies_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_consistency_rule(module, api_instance, result)
        else:
            create_consistency_rule(module, api_instance, result)
    else:
        delete_consistency_rule(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
