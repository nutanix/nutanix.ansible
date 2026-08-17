#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_policy_v2
short_description: Create or Update an approval policy in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create and update approval policies (a.k.a. Policy)
    in Nutanix Prism Central using the PC v4 security management APIs.
  - An approval policy governs sensitive operations on secured entities such as
    Recovery Points and Protection Policies by requiring one or more approvers
    to approve the operation before it is executed.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create an approval policy) -
      Required Roles: Super Admin
    - >-
      B(Update an approval policy) -
      Required Roles: Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create approval policy.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update approval policy.
      - C(state=absent) is currently not supported because the underlying SDK does not expose
        a delete operation for approval policies. When invoked, the module fails fast with a
        descriptive error message so callers do not silently expect a delete.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the approval policy.
      - Required for update operation.
    type: str
    required: false
  name:
    description:
      - Name of the approval policy.
      - Required for create operation.
    type: str
    required: false
  description:
    description:
      - Description of the approval policy.
    type: str
    required: false
  approver_groups:
    description:
      - List of approver groups (approver sets) for the approval policy.
      - Each group defines a set of approvers and an expiry window.
      - Required for create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      name:
        description:
          - Name of the approver set.
        type: str
        required: true
      expiry_hours:
        description:
          - Expiry window (in hours) within which the approvers of the set must approve the request.
          - Typical valid range is C(1) to C(168).
        type: int
        required: false
      approvers:
        description:
          - List of users belonging to this approver set.
          - Every approver must be an existing IAM user in Prism Central.
        type: list
        elements: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External ID of the IAM user acting as approver.
            type: str
            required: false
          username:
            description:
              - Identifier / login name of the approver user.
            type: str
            required: false
          user_type:
            description:
              - Type of the approver user.
            type: str
            required: false
            choices:
              - LOCAL
              - SAML
              - LDAP
              - EXTERNAL
              - SERVICE_ACCOUNT
          display_name:
            description:
              - Display name of the approver.
            type: str
            required: false
          email_id:
            description:
              - Email address of the approver used for notifications.
            type: str
            required: false
          first_name:
            description:
              - First name of the approver.
            type: str
            required: false
          last_name:
            description:
              - Last name of the approver.
            type: str
            required: false
          idp_id:
            description:
              - Identity provider identifier for the approver user (SAML/LDAP flows).
            type: str
            required: false
  secured_policies:
    description:
      - List of policies that are secured by this approval policy.
      - Each entry associates a policy (typically a Protection Policy) with this approval policy.
    type: list
    elements: dict
    required: false
    suboptions:
      policy_ext_id:
        description:
          - External identifier of the policy being secured by this approval policy.
        type: str
        required: true
      policy_type:
        description:
          - Type of the secured policy.
        type: str
        required: false
        choices:
          - PROTECTION_POLICY
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
- name: Create an approval policy
  nutanix.ncp.ntnx_security_policy_v2:
    state: present
    name: "ansible-approval-policy"
    description: "Approval policy created by Ansible"
    approver_groups:
      - name: "admin-approvers"
        expiry_hours: 24
        approvers:
          - ext_id: "00000000-0000-0000-0000-000000000000"
            username: "admin"
    secured_policies:
      - policy_ext_id: "11111111-1111-1111-1111-111111111111"
        policy_type: "PROTECTION_POLICY"
  register: created

- name: Update an approval policy (change description and expiry_hours)
  nutanix.ncp.ntnx_security_policy_v2:
    state: present
    ext_id: "22222222-2222-2222-2222-222222222222"
    name: "ansible-approval-policy-updated"
    description: "Updated approval policy description"
    approver_groups:
      - name: "admin-approvers"
        expiry_hours: 48
        approvers:
          - ext_id: "00000000-0000-0000-0000-000000000000"
            username: "admin"
    secured_policies:
      - policy_ext_id: "11111111-1111-1111-1111-111111111111"
        policy_type: "PROTECTION_POLICY"
  register: updated
"""

RETURN = r"""
response:
  description:
    - Response for creating or updating an approval policy.
    - If the operation is create/update and C(wait) is true, it will return the approval policy details.
    - If C(wait) is false, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "approver_groups": [
        {
          "approvers": [
            {
              "buckets_access_keys": null,
              "created_by": null,
              "created_time": null,
              "creation_type": null,
              "description": null,
              "display_name": null,
              "email_id": null,
              "ext_id": "00000000-0000-0000-0000-000000000000",
              "first_name": null,
              "idp_id": null,
              "is_force_reset_password_enabled": null,
              "last_login_time": null,
              "last_name": null,
              "last_updated_by": null,
              "last_updated_time": null,
              "locale": null,
              "middle_initial": null,
              "password": null,
              "region": null,
              "status": null,
              "tenant_id": null,
              "user_type": null,
              "username": "admin"
            }
          ],
          "expiry_hours": 24,
          "name": "admin-approvers"
        }
      ],
      "description": "Approval policy created by Ansible",
      "ext_id": "22222222-2222-2222-2222-222222222222",
      "is_update_pending": false,
      "last_update_time": "2026-07-20T12:00:00.000Z",
      "last_updated_by": "00000000-0000-0000-0000-000000000000",
      "links": null,
      "name": "ansible-approval-policy",
      "secured_policies": [
        {
          "policy_ext_id": "11111111-1111-1111-1111-111111111111",
          "policy_type": "PROTECTION_POLICY"
        }
      ],
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
    - The external ID of the approval policy.
  returned: always
  type: str
  sample: "22222222-2222-2222-2222-222222222222"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - This indicates whether the task was skipped because the approval policy already
      matches the desired state.
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
  sample: "Api Exception raised while creating approval policy"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_approval_policies_api_instance,
    get_etag,
)
from ..module_utils.v4.security.helpers import get_approval_policy  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_security_py_client as security_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as security_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    user_spec = dict(
        ext_id=dict(type="str"),
        username=dict(type="str"),
        user_type=dict(
            type="str",
            choices=["LOCAL", "SAML", "LDAP", "EXTERNAL", "SERVICE_ACCOUNT"],
            obj=security_sdk.UserType,
        ),
        display_name=dict(type="str"),
        email_id=dict(type="str"),
        first_name=dict(type="str"),
        last_name=dict(type="str"),
        idp_id=dict(type="str"),
    )

    approver_group_spec = dict(
        name=dict(type="str", required=True),
        expiry_hours=dict(type="int"),
        approvers=dict(
            type="list",
            elements="dict",
            options=user_spec,
            obj=security_sdk.User,
        ),
    )

    secured_policy_spec = dict(
        policy_ext_id=dict(type="str", required=True),
        policy_type=dict(
            type="str",
            choices=["PROTECTION_POLICY"],
            obj=security_sdk.PolicyType,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        approver_groups=dict(
            type="list",
            elements="dict",
            options=approver_group_spec,
            obj=security_sdk.ApproverGroup,
        ),
        secured_policies=dict(
            type="list",
            elements="dict",
            options=secured_policy_spec,
            obj=security_sdk.SecuredPolicy,
        ),
    )
    return module_args


def _strip_server_populated_fields(spec):
    """Zero-out fields the platform manages so they are not sent back on update."""

    for field in ("last_updated_by", "last_update_time", "is_update_pending"):
        if hasattr(spec, field):
            setattr(spec, field, None)
    return spec


def create_Policy(module, result, api_instance):
    validate_required_params(module, ["name", "approver_groups"])
    sg = SpecGenerator(module)
    default_spec = security_sdk.ApprovalPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create approval policy spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.create_approval_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating approval policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.APPROVAL_POLICY
        )
        if not ext_id:
            ext_id = get_entity_ext_id_from_task(task_status)
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_approval_policy(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Approval Policy"
                ),
                msg="Failed to get entity ext_id from task for Approval Policy",
            )

    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    for key in ("last_updated_by", "last_update_time", "is_update_pending"):
        old_spec_dict.pop(key, None)
        update_spec_dict.pop(key, None)
    return old_spec_dict == update_spec_dict


def update_Policy(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_approval_policy(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating approval policy", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update approval policy spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    _strip_server_populated_fields(update_spec)

    kwargs = {"if_match": etag}
    try:
        resp = api_instance.update_approval_policy_by_ext_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating approval policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_approval_policy(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_Policy(module, result, api_instance):
    """Delete is not supported by the Approval Policies SDK.

    The v4.1 security SDK exposes only create/get/list/update/associate
    operations for approval policies. Fail fast so callers do not silently
    expect a working delete.
    """

    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    msg = (
        "Delete is not supported for Approval Policy by the current "
        "ntnx_security_py_client SDK. Skipping delete for ext_id: {0}".format(ext_id)
    )
    result["failed"] = True
    result.pop("msg", None)
    module.fail_json(msg=msg, **result)


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_security_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }
    api_instance = get_approval_policies_api_instance(module)

    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_Policy(module, result, api_instance)
        else:
            create_Policy(module, result, api_instance)
    else:
        delete_Policy(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
