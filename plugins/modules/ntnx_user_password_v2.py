#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_password_v2
short_description: Change or reset a user password in Nutanix Prism Central.
version_added: 2.7.0
description:
    - This module performs password management actions for local users in
      Nutanix Prism Central using the v4 IAM APIs.
    - It supports two mutually exclusive operations.
    - When C(ext_id) is provided, the module performs an administrative
      B(reset) of that user's password (equivalent to the SDK
      C(UsersApi.reset_user_password) call). The B(new_password) field is
      required for this operation. The caller must have admin permissions.
    - When C(username) is provided (along with C(old_password) and
      C(new_password)), the module performs a self-serve password B(change)
      (equivalent to the SDK C(UsersApi.change_user_password) call). A user
      can only change their own password using this API - even administrators
      receive a 403 FORBIDDEN if they attempt to change the password of a
      different user.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation. The required roles depend on the
      operation being performed.
    - >-
      B(Reset user password) -
      Required Roles: Nutanix Central Admin, Prism Admin, Super Admin.
      Requires the C(Reset_User_Password) operation permission on the C(user)
      entity type (maps to legacy operations C(Prism:Reset_Password) and
      C(Prism:Reset_User_Password)).
    - >-
      B(Change user password) -
      Self-service only - a user can change only their own password. Admin
      users cannot use this API to change another user's password.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported because this is an action module.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - External identifier of the user whose password should be reset.
            - When set, the module performs an admin-driven password B(reset)
              action.
            - Mutually exclusive with C(username) and C(old_password).
        required: false
        type: str
    username:
        description:
            - Username (email-form identifier) of the user whose password
              should be changed.
            - When set, the module performs a self-serve password B(change)
              action - only the owning user can invoke this.
            - Required together with C(old_password).
            - Mutually exclusive with C(ext_id).
        required: false
        type: str
    old_password:
        description:
            - Current (old) password of the user, required to authorise a
              self-serve password change.
            - Required together with C(username).
            - Ignored for the reset operation (which does not need the old
              password).
        required: false
        type: str
    new_password:
        description:
            - The new password to set for the user.
            - Required for both the change and reset operations.
        required: true
        type: str
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
- name: Reset a local user's password (admin action)
  nutanix.ncp.ntnx_user_password_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "27892065-1d1b-5d66-ab17-a26038088b17"
    new_password: "N3wStr0ng!Password123"
  register: reset_result

- name: Change your own password (self-serve, needs current password)
  nutanix.ncp.ntnx_user_password_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ target_username }}"
    nutanix_password: "{{ target_current_password }}"
    validate_certs: false
    username: "{{ target_username }}"
    old_password: "{{ target_current_password }}"
    new_password: "N3wStr0ng!Password123"
  register: change_result
"""

RETURN = r"""
response:
    description:
        - Response of the user password action.
        - Contains the C(message) returned by the underlying API on success.
    returned: always
    type: dict
    sample:
        {
            "message": "User Password reset successful."
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error or in check mode operation
    type: str
    sample: "Api Exception raised while resetting user password"

error:
    description:
        - This field typically holds information about if the task have
          errors that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Forbidden"

failed:
    description: This field typically holds information about if the task has failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description:
        - The external ID of the task.
        - The password change/reset actions do not create a long running task
          in PC, so this field is C(None).
    returned: always
    type: str
    sample: null

ext_id:
    description:
        - The external identifier of the user whose password was reset.
        - Only populated when the reset operation was invoked (C(ext_id) was
          supplied).
    returned: always
    type: str
    sample: "27892065-1d1b-5d66-ab17-a26038088b17"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import get_user_api_instance  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as iam_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as iam_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str"),
        username=dict(type="str"),
        old_password=dict(type="str", no_log=True),
        new_password=dict(type="str", required=True, no_log=True),
    )
    return module_args


def reset_user_password(module, users_api, result):
    ext_id = module.params.get("ext_id")
    new_password = module.params.get("new_password")
    result["ext_id"] = ext_id

    validate_required_params(module, ["ext_id", "new_password"])

    spec = iam_sdk.PasswordResetRequest(new_password=new_password)

    if module.check_mode:
        result["response"] = {
            "message": (
                "Password for user with ext_id '{0}' will be reset.".format(ext_id)
            )
        }
        return

    resp = None
    try:
        resp = users_api.reset_user_password(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while resetting user password",
        )

    if resp is not None and getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    else:
        result["response"] = {
            "message": "Password reset successful for user '{0}'.".format(ext_id)
        }
    result["changed"] = True


def change_user_password(module, users_api, result):
    username = module.params.get("username")
    old_password = module.params.get("old_password")
    new_password = module.params.get("new_password")

    validate_required_params(module, ["username", "old_password", "new_password"])

    spec = iam_sdk.PasswordChangeRequest(
        username=username,
        old_password=old_password,
        new_password=new_password,
    )

    if module.check_mode:
        result["response"] = {
            "message": ("Password for user '{0}' will be changed.".format(username))
        }
        return

    resp = None
    try:
        resp = users_api.change_user_password(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while changing user password",
        )

    if resp is not None and getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    else:
        result["response"] = {
            "message": "Password change successful for user '{0}'.".format(username)
        }
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ("ext_id", "username"),
            ("ext_id", "old_password"),
        ],
        required_one_of=[("ext_id", "username")],
        required_together=[("username", "old_password")],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    users_api = get_user_api_instance(module)

    if module.params.get("ext_id"):
        reset_user_password(module, users_api, result)
    else:
        change_user_password(module, users_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
