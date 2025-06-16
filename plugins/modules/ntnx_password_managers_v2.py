#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_password_managers_v2
short_description: Update password of system user in Nutanix Clusters
version_added: 2.2.1
description:
    - This module allows you to update the password of a system user in Nutanix Clusters.
    - It uses the Nutanix Clusters Management API to change the password of a specified system user.
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - External ID of the system user password needs to be updated.
        type: str
        required: true
    current_password:
        description:
            - Current password of the system user.
        type: str
        no_log: true
        required: false
    new_password:
        description:
            - New password to be set for the system user.
        type: str
        no_log: true
        required: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Update password
  nutanix.ncp.ntnx_password_managers_v2:
    ext_id: "0a1b2c3d-4e5f-6789-abcd-ef0123456789"
    current_password: "Random.password123"
    new_password: "NewPassword.456"
    state: present
  register: update_password
"""

RETURN = r"""
response:
    description: The response from the API after updating the password.
    returned: always
    type: dict
    sample: {
            "cluster_ext_ids": null,
            "completed_time": "2025-06-16T08:44:55.003449+00:00",
            "completion_details": null,
            "created_time": "2025-06-16T08:44:51.663947+00:00",
            "entities_affected": [
                {
                    "ext_id": "4f8c3c0a-35e4-4756-8c5e-9626e286fba3",
                    "name": "PC admin user password",
                    "rel": "security:config:system-user-passwords"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:2adea6af-8842-47e4-7ea5-57b69f97aa2b",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2025-06-16T08:44:55.003448+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 1,
            "operation": "ChangePassword",
            "operation_description": "Update system user password",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2025-06-16T08:44:52.971399+00:00",
            "status": "SUCCEEDED",
            "sub_steps": [
                {
                    "name": "Initiating change password main task"
                },
                {
                    "name": "Password change successful for user: admin on cluster with UUID: 9e0ea08a-131e-446c-80f7-5c3f30cac3a8"
                },
                {
                    "name": "Successfully published password manager stats. (Status Code: 200)"
                }
            ],
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:4325f855-9be9-4c68-42ff-e4c897151f11",
                    "href": "https://10.96.29.97:9440/api/prism/v4.0/config/tasks/ZXJnb24=:4325f855-9be9-4c68-42ff-e4c897151f11",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }
ext_id:
    description: The external ID of the system user whose password was updated.
    returned: always
    type: str
    sample: "0a1b2c3d-4e5f-6789-abcd-ef0123456789"
task_ext_id:
    description: The external ID of the task that was created to update the password.
    returned: always
    type: str
    sample: "ZXJnb24=:4325f855-9be9-4c68-42ff-e4c897151f11"
changed:
    description: Indicates whether the password was successfully updated.
    returned: always
    type: bool
    sample: true
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""


import traceback  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_password_manager_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
from ansible.module_utils.basic import missing_required_lib  # noqa: E402

try:
    import ntnx_clustermgmt_py_client as clustermgmt_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        current_password=dict(type="str", no_log=True, required=False),
        new_password=dict(type="str", no_log=True, required=True),
    )
    return module_args


def update_password(module, password_manager_api, result):
    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.ChangePasswordSpec()
    spec, err = sg.generate_spec(default_spec)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for updating password of system user", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = password_manager_api.change_system_user_password_by_id(
            extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while updating password of system user",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    password_manager_api = get_password_manager_api_instance(module)
    update_password(module, password_manager_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
