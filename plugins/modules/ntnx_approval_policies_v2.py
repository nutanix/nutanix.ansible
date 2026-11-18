#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_approval_policies_v2
short_description: Create or Update an approval policy
version_added: "2.7.0"
description:
    - Create or Update an approval policy for secure snapshots in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Create Approval Policy) -
      Required Roles: Prism Admin, Secure Policy Admin, Super Admin
    - >-
      B(Update Approval Policy) -
      Required Roles: Prism Admin, Secure Policy Admin, Secure Policy Editor, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present) and C(ext_id) is not provided, the module will create an approval policy.
            - If C(state) is C(present) and C(ext_id) is provided, the module will update the approval policy.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - External ID of the approval policy.
            - Required for update.
        type: str
        required: false
    name:
        description:
            - Name of the approval policy.
        type: str
        required: false
    description:
        description:
            - Description of the approval policy.
        type: str
        required: false
    approver_groups:
        description:
            - List of approver sets.
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
                    - Number of hours until approval request expires.
                type: int
                required: true
            approvers:
                description:
                    - List of approvers.
                type: list
                elements: dict
                required: true
                suboptions:
                    username:
                        description:
                            - Identifier of the user.
                        type: str
                        required: true
                    user_type:
                        description:
                            - Type of the user.
                        type: str
                        choices:
                            - LOCAL
                            - SAML
                            - LDAP
                            - EXTERNAL
                            - SERVICE_ACCOUNT
                        required: true
                    idp_id:
                        description:
                            - Identifier of the IDP for the user.
                        type: str
                        required: false
                    display_name:
                        description:
                            - Display name of the user. For LDAP and SAML users, this is set from AD config.
                        type: str
                        required: false
                    first_name:
                        description:
                            - First name of the user.
                        type: str
                        required: false
                    middle_initial:
                        description:
                            - Middle name of the user.
                        type: str
                        required: false
                    last_name:
                        description:
                            - Last name of the user.
                        type: str
                        required: false
                    email_id:
                        description:
                            - Email ID of the user.
                        type: str
                        required: false
                    locale:
                        description:
                            - Default locale of the user.
                        type: str
                        required: false
                    region:
                        description:
                            - Default region of the user.
                        type: str
                        required: false
                    password:
                        description:
                            - Password of the user.
                        type: str
                        required: false
                    is_force_reset_password_enabled:
                        description:
                            - Flag to force the user to reset password.
                        type: bool
                        required: false
                    additional_attributes:
                        description:
                            - Indicates additional attributes of the user.
                        type: list
                        elements: dict
                        required: false
                        suboptions:
                            name:
                                description:
                                    - The key of the key-value pair.
                                type: str
                                required: false
                            value:
                                description:
                                    - The value associated with the key for this key-value pair.
                                type: str
                                required: false
                    description:
                        description:
                            - Description of the user.
                        type: str
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
- name: Create an approval policy
  nutanix.ncp.ntnx_approval_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: "Platinum Approval Policy"
    description: "This policy is for platinum snapshots"
    approver_groups:
      - name: "Platinum Approvers"
        expiry_hours: 44
        approvers:
          - username: "admin"
            user_type: LOCAL
          - username: "approver2"
            user_type: LOCAL
          - username: "approver3"
            user_type: LOCAL
  register: result

- name: Update an approval policy
  nutanix.ncp.ntnx_approval_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "f19af988-ea11-46ca-8958-e8158d87383b"
    name: "Platinum Approval Policy Updated"
    description: "Updated description"
    approver_groups:
      - name: "Platinum Approvers"
        expiry_hours: 48
        approvers:
          - username: "admin"
            user_type: LOCAL
          - username: "approver2"
            user_type: LOCAL
          - username: "approver3"
            user_type: LOCAL
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for creating or updating an approval policy.
        - If C(wait) is true and the operation is Create or Update, it will contain the approval policy details.
        - If C(wait) is false, it will contain the task details.
    type: dict
    returned: always
    sample:
        {
            "approver_groups": [
                {
                    "approvers": [
                        {
                            "username": "admin",
                            "user_type": "LOCAL"
                        }
                    ],
                    "expiry_hours": 44,
                    "name": "Platinum Approvers"
                }
            ],
            "description": "This policy is for platinum snapshots",
            "ext_id": "f19af988-ea11-46ca-8958-e8158d87383b",
            "is_update_pending": false,
            "last_update_time": null,
            "last_updated_by": null,
            "links": null,
            "name": "Platinum Approval Policy",
            "secured_policies": null,
            "tenant_id": null
        }
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
skipped:
    description: This indicates whether the task was skipped
    type: bool
    returned: when module is idempotent
    sample: false
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
ext_id:
    description: The external ID of the approval policy.
    type: str
    returned: always
    sample: "f19af988-ea11-46ca-8958-e8158d87383b"
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent or check mode
    type: str
    sample: "Nothing to change."
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
"""

import copy  # noqa: E402
import traceback  # noqa: E402
import uuid  # noqa: E402
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
from ..module_utils.v4.security.helpers import (  # noqa: E402
    get_approval_policy_by_ext_id,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_users_empty_attributes,
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
    additional_attributes_spec = dict(
        name=dict(type="str"),
        value=dict(type="str"),
    )
    approver_spec = dict(
        username=dict(type="str", required=True),
        user_type=dict(
            type="str",
            required=True,
            choices=["LOCAL", "SAML", "LDAP", "EXTERNAL", "SERVICE_ACCOUNT"],
        ),
        idp_id=dict(type="str"),
        display_name=dict(type="str"),
        first_name=dict(type="str"),
        middle_initial=dict(type="str"),
        last_name=dict(type="str"),
        email_id=dict(type="str"),
        locale=dict(type="str"),
        region=dict(type="str"),
        password=dict(type="str", no_log=True),
        is_force_reset_password_enabled=dict(type="bool"),
        additional_attributes=dict(
            type="list",
            elements="dict",
            options=additional_attributes_spec,
            obj=security_sdk.KVPair,
        ),
        description=dict(type="str"),
    )
    approver_group_spec = dict(
        name=dict(type="str", required=True),
        expiry_hours=dict(type="int", required=True),
        approvers=dict(
            type="list",
            elements="dict",
            required=True,
            options=approver_spec,
            obj=security_sdk.User,
        ),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        approver_groups=dict(
            type="list",
            elements="dict",
            options=approver_group_spec,
            obj=security_sdk.ApproverGroup,
        ),
    )
    return module_args


def create_approval_policy(module, result, api_instance):
    validate_required_params(module, ["name", "approver_groups"])
    sg = SpecGenerator(module)
    default_spec = security_sdk.ApprovalPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create approval policy Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Approval policy will be created."
        return

    resp = None
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
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Approval Policy"
                ),
                msg="Failed to get entity ext_id from task for Approval Policy",
            )
        resp = get_approval_policy_by_ext_id(module, api_instance, ext_id)
        result["ext_id"] = ext_id
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def check_approval_policy_idempotency(old_spec, update_spec):
    old_dict = strip_internal_attributes(old_spec.to_dict())
    update_dict = strip_internal_attributes(update_spec.to_dict())
    for field in (
        "last_updated_by",
        "last_update_time",
        "is_update_pending",
        "secured_policies",
        "ext_id",
        "links",
        "tenant_id",
    ):
        old_dict.pop(field, None)
        update_dict.pop(field, None)
    return old_dict == update_dict


def update_approval_policy(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_approval_policy_by_ext_id(module, api_instance, ext_id)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        module.fail_json(
            msg="Unable to fetch etag for updating approval policy", **result
        )

    strip_users_empty_attributes(current_spec)

    sg = SpecGenerator(module)
    default_spec = copy.deepcopy(current_spec)
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update approval policy Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        result["msg"] = "Approval policy will be updated."
        return

    if check_approval_policy_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    kwargs = {"if_match": etag_value, "NTNX-Request-Id": str(uuid.uuid4())}
    resp = None
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
        resp = get_approval_policy_by_ext_id(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    if SDK_IMP_ERROR:
        module = BaseModuleV4(
            argument_spec=get_module_spec(),
            supports_check_mode=True,
        )
        module.fail_json(
            msg=missing_required_lib("ntnx_security_py_client"),
            exception=SDK_IMP_ERROR,
        )

    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
    }
    api_instance = get_approval_policies_api_instance(module)
    if module.params.get("ext_id"):
        update_approval_policy(module, result, api_instance)
    else:
        create_approval_policy(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
