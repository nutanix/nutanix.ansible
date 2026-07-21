#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_state_v2
short_description: Update the active state of a user in Nutanix Prism Central
version_added: 2.7.0
description:
    - This module allows you to change the active state (C(ACTIVE)/C(INACTIVE)) of a user in Nutanix Prism Central.
    - It wraps the IAM v4 C(UpdateUserState) action endpoint (POST /api/iam/v4.1.b2/authn/users/{extId}/$actions/change-state).
    - The endpoint is idempotent - setting the state to the current value is a no-op on the server.
    - Internal (predefined) users cannot be disabled through this endpoint.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update active state of user) -
      Required Roles: Nutanix Central Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will update the active state of the user.
            - The C(status) option controls whether the user becomes C(ACTIVE) or C(INACTIVE).
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier (UUID) of the user whose active state is to be updated.
        type: str
        required: true
    status:
        description:
            - The new active state to apply to the user.
            - C(ACTIVE) enables the user, C(INACTIVE) disables the user.
        type: str
        choices:
            - ACTIVE
            - INACTIVE
        required: true
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
- name: Deactivate a user
  nutanix.ncp.ntnx_user_state_v2:
    ext_id: "27892065-1d1b-5d66-ab17-a26038088b17"
    status: INACTIVE
  register: result

- name: Re-activate a user
  nutanix.ncp.ntnx_user_state_v2:
    ext_id: "27892065-1d1b-5d66-ab17-a26038088b17"
    status: ACTIVE
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for updating the active state of a user.
        - Contains the C(UserStateUpdateResponse) returned by the C(change-state) action API.
    returned: always
    type: dict
    sample:
        {
            "message": "User State update successful."
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
    sample: "Api Exception raised while updating user state"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Failed generating spec for update user state"

failed:
    description: This field typically holds information about if the task has failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task, if the action is asynchronous.
    returned: when the API returns a task
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external identifier (UUID) of the user whose state was updated.
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
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as identity_and_access_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as identity_and_access_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", choices=["present"], default="present"),
        ext_id=dict(type="str", required=True),
        status=dict(
            type="str",
            choices=["ACTIVE", "INACTIVE"],
            required=True,
            obj=identity_and_access_management_sdk.UserStatusType,
        ),
    )
    return module_args


def update_user_state(module, users_api, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = identity_and_access_management_sdk.UserStateUpdate()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for update user state", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = users_api.update_user_state(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating user state",
        )

    task_ext_id = getattr(getattr(resp, "data", None), "ext_id", None)
    if task_ext_id:
        result["task_ext_id"] = task_ext_id
        if module.params.get("wait"):
            task = wait_for_completion(module, task_ext_id)
            result["response"] = strip_internal_attributes(task.to_dict())
        else:
            result["response"] = strip_internal_attributes(resp.data.to_dict())
    else:
        # Synchronous response - typically a UserStateUpdateResponse with a `message`.
        response_body = getattr(resp, "data", None)
        if response_body is not None and hasattr(response_body, "to_dict"):
            result["response"] = strip_internal_attributes(response_body.to_dict())
        else:
            result["response"] = None

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    users_api = get_user_api_instance(module)
    update_user_state(module, users_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
