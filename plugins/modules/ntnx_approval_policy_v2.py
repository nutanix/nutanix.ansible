#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_approval_policy_v2
short_description: Create and update Approval Policies in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create and update Approval Policies in Nutanix Prism Central.
  - Approval Policies define the multi-party authorization flow for Secure Snap
    protected operations (for example, updating or deleting protection policies
    that are associated with the approval policy).
  - Also supports associating (or replacing) the list of secured policies that
    an approval policy governs, using the C(associate_policies) action flag.
  - The Nutanix v4 Approval Policies API does not currently expose a delete
    operation, so C(state=absent) is not supported by this module.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation. The required roles depend on the
      operation being performed.
    - >-
      B(Create an Approval Policy) -
      Required Roles: Prism Admin, Security Admin, Super Admin
    - >-
      B(Update an Approval Policy) -
      Required Roles: Prism Admin, Security Admin, Super Admin
    - >-
      B(Associate secured policies with an Approval Policy) -
      Required Roles: Prism Admin, Security Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create approval policy.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update approval policy.
      - C(absent) is accepted by the argument spec but the Nutanix Approval
        Policies v4 API does not currently expose a delete endpoint, so
        C(state=absent) will fail with a descriptive error.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the Approval Policy.
      - Required for update and associate-policies operations.
    type: str
    required: false
  name:
    description:
      - Name of the Approval Policy.
      - Required for create operation.
      - Minimum 4 characters, maximum 199 characters.
    type: str
    required: false
  description:
    description:
      - Description of the Approval Policy.
      - Maximum 499 characters.
    type: str
    required: false
  approver_groups:
    description:
      - List of approver groups that grant approval for actions guarded by this policy.
      - Required for create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      name:
        description:
          - Name of the approver group.
        type: str
        required: true
      expiry_hours:
        description:
          - Time in hours for which an approval request from this group is
            valid before it expires.
        type: int
        required: false
      approvers:
        description:
          - List of IAM users who are approvers in this group.
          - At least one approver is required per approver group.
        type: list
        elements: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External ID of the IAM user acting as an approver.
            type: str
            required: false
          username:
            description:
              - Username of the IAM user acting as an approver.
            type: str
            required: false
          user_type:
            description:
              - IAM user type of the approver.
            type: str
            required: false
            choices:
              - LOCAL
              - LDAP
              - SAML
              - EXTERNAL
              - SERVICE_ACCOUNT
          email_id:
            description:
              - Email address of the IAM user acting as an approver.
              - Used for approval notifications.
            type: str
            required: false
          display_name:
            description:
              - Display name of the IAM user acting as an approver.
            type: str
            required: false
          first_name:
            description:
              - First name of the IAM user acting as an approver.
            type: str
            required: false
          last_name:
            description:
              - Last name of the IAM user acting as an approver.
            type: str
            required: false
          idp_id:
            description:
              - Identity Provider ID of the approver.
            type: str
            required: false
  secured_policies:
    description:
      - List of secured policies governed by this approval policy.
      - Setting this list is equivalent to invoking the
        associate-policies action on the approval policy.
      - This is a read-only field for pure create/update calls; use
        C(associate_policies=true) to replace the associated list on an
        existing approval policy.
    type: list
    elements: dict
    required: false
    suboptions:
      policy_ext_id:
        description:
          - External identifier of the secured policy (for example, a
            protection policy) that is protected by the approval policy.
        type: str
        required: true
      policy_type:
        description:
          - Type of the secured policy.
        type: str
        required: false
        choices:
          - PROTECTION_POLICY
  associate_policies:
    description:
      - When C(true) and C(ext_id) is provided, calls the
        associate-policies action on the approval policy to replace the
        list of secured policies with the ones supplied in
        C(secured_policies) instead of doing a full PUT update.
    type: bool
    required: false
    default: false
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
- name: Create an approval policy with a single approver group
  nutanix.ncp.ntnx_approval_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "ansible_approval_policy"
    description: "Approval policy created by Ansible"
    approver_groups:
      - name: "primary_approvers"
        expiry_hours: 48
        approvers:
          - ext_id: "0005b0f1-6c1e-4d10-9c5a-1234567890ab"
            username: "approver_user_one"
            user_type: "LOCAL"
            email_id: "approver1@example.com"
            display_name: "Approver One"
          - ext_id: "0005b0f1-6c1e-4d10-9c5a-1234567890cd"
            username: "approver_user_two"
            user_type: "LOCAL"
            email_id: "approver2@example.com"
            display_name: "Approver Two"
          - ext_id: "0005b0f1-6c1e-4d10-9c5a-1234567890ef"
            username: "approver_user_three"
            user_type: "LOCAL"
            email_id: "approver3@example.com"
            display_name: "Approver Three"
  register: create_result

- name: Update an existing approval policy (change description and expiry)
  nutanix.ncp.ntnx_approval_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "{{ create_result.ext_id }}"
    name: "ansible_approval_policy_updated"
    description: "Approval policy updated by Ansible"
    approver_groups:
      - name: "primary_approvers"
        expiry_hours: 24
        approvers:
          - ext_id: "0005b0f1-6c1e-4d10-9c5a-1234567890ab"
            username: "approver_user_one"
            user_type: "LOCAL"
          - ext_id: "0005b0f1-6c1e-4d10-9c5a-1234567890cd"
            username: "approver_user_two"
            user_type: "LOCAL"
          - ext_id: "0005b0f1-6c1e-4d10-9c5a-1234567890ef"
            username: "approver_user_three"
            user_type: "LOCAL"
  register: update_result

- name: Associate secured policies with an approval policy
  nutanix.ncp.ntnx_approval_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "{{ create_result.ext_id }}"
    associate_policies: true
    secured_policies:
      - policy_ext_id: "1e2f3d4c-5b6a-7890-abcd-ef1234567890"
        policy_type: "PROTECTION_POLICY"
  register: associate_result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating or associating secured policies with an
      approval policy.
    - If C(wait) is true, it will return the approval policy details.
    - If C(wait) is false, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "approver_groups": [
        {
          "approvers": [
            {
              "display_name": "Approver One",
              "email_id": "approver1@example.com",
              "ext_id": "0005b0f1-6c1e-4d10-9c5a-1234567890ab",
              "first_name": "Approver",
              "last_name": "One",
              "username": "approver_user_one"
            }
          ],
          "expiry_hours": 48,
          "name": "primary_approvers"
        }
      ],
      "description": "Approval policy created by Ansible",
      "ext_id": "8f7e6d5c-4b3a-2109-fedc-ba0987654321",
      "is_update_pending": false,
      "last_updated_by": "admin",
      "last_update_time": "2026-07-20T15:00:00.000Z",
      "links": null,
      "name": "ansible_approval_policy",
      "secured_policies": [],
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task created for the operation.
  returned: always
  type: str
  sample: "ZXJnb24=:1a2b3c4d-5e6f-7890-abcd-ef1234567890"

ext_id:
  description:
    - The external ID of the Approval Policy.
  returned: always
  type: str
  sample: "8f7e6d5c-4b3a-2109-fedc-ba0987654321"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - Indicates the task was skipped because the current spec already
      matches the desired spec.
  returned: When update is skipped due to idempotency
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
  sample: "Nothing to change."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

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
    strip_read_only_fields,
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

    approver_spec = dict(
        ext_id=dict(type="str"),
        username=dict(type="str"),
        user_type=dict(
            type="str",
            choices=["LOCAL", "LDAP", "SAML", "EXTERNAL", "SERVICE_ACCOUNT"],
            obj=security_sdk.UserType,
        ),
        email_id=dict(type="str"),
        display_name=dict(type="str"),
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
            options=approver_spec,
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
        associate_policies=dict(type="bool", default=False),
    )

    return module_args


def _strip_output(spec_dict):
    """Return a copy of the spec dict without server-populated / audit fields
    so it can be compared for idempotency.
    """
    dropped = strip_internal_attributes(spec_dict)
    for key in ("last_updated_by", "last_update_time", "is_update_pending"):
        dropped.pop(key, None)
    return dropped


def check_for_idempotency(old_spec_dict, update_spec_dict):
    return _strip_output(old_spec_dict) == _strip_output(update_spec_dict)


def create_approval_policy(module, api_instance, result):
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


def associate_secured_policies(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = security_sdk.AssociatePoliciesSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating associate secured policies spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.associate_policies(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating secured policies with approval policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_approval_policy(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def update_approval_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.params.get("associate_policies"):
        associate_secured_policies(module, api_instance, result)
        return

    current_spec = get_approval_policy(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating approval policy", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=current_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update approval policy spec", **result)

    if check_for_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. Refer docs to check for fields which can be updated",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    strip_read_only_fields(
        update_spec, fields=["last_updated_by", "last_update_time", "is_update_pending"]
    )

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


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_security_py_client"),
            exception=SDK_IMP_ERROR,
        )

    if module.params.get("associate_policies") and not module.params.get("ext_id"):
        module.fail_json(
            msg="associate_policies=True requires ext_id of an existing approval policy."
        )

    remove_param_with_none_value(module.params)

    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_approval_policies_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_approval_policy(module, api_instance, result)
        else:
            create_approval_policy(module, api_instance, result)
    else:
        module.fail_json(
            msg=(
                "The Nutanix Approval Policies v4 API does not support the "
                "delete operation. state=absent is not implemented for this "
                "entity."
            ),
            **result,
        )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
