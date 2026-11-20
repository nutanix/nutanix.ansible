#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_revert_v2
short_description: Revert a Volume Group
version_added: "2.7.0"
description:
    - Reverts a Volume Group identified by its External ID.
    - This API performs an in-place restore from a specified Volume Group recovery point.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Revert a Volume Group) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Self-Service Admin (deprecated), Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will revert the Volume Group to a recovery point.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The External ID of the Volume Group to revert.
        type: str
        required: true
    volume_group_recovery_point_ext_id:
        description:
            - The external identifier of the Volume Group recovery point.
            - This is a mandatory field.
        type: str
        required: true
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
- name: Revert a Volume Group to a recovery point
  nutanix.ncp.ntnx_volume_groups_revert_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "9341e04e-45dd-4ffa-8775-f5b4218a85c7"
    volume_group_recovery_point_ext_id: "3acdebac-e5ac-0add-f1e2-ebccb1bddcbb"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for reverting a Volume Group.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: dict
    sample: {
        "app_name": null,
        "cluster_ext_ids": null,
        "completed_time": "2026-11-17T11:45:00.000000+00:00",
        "completion_details": null,
        "created_time": "2026-11-17T11:44:59.000000+00:00",
        "entities_affected": null,
        "error_messages": null,
        "ext_id": "ZXJnb24=:c44331ab-8260-46ab-896f-af114d0985bf",
        "is_background_task": false,
        "is_cancelable": false,
        "last_updated_time": "2026-11-17T11:45:00.000000+00:00",
        "legacy_error_message": null,
        "number_of_entities_affected": 0,
        "number_of_subtasks": 0,
        "operation": "RevertVolumeGroup",
        "operation_description": "Revert Volume Group",
        "owned_by": {"ext_id": "00000000-0000-0000-0000-000000000000", "name": "admin"},
        "parent_task": null,
        "progress_percentage": 100,
        "project_ext_id": "00000000-0000-0000-0000-000000000000",
        "resource_links": null,
        "root_task": null,
        "started_time": "2026-11-17T11:44:59.000000+00:00",
        "status": "SUCCEEDED",
        "sub_steps": null,
        "sub_tasks": null,
        "warnings": null
    }
task_ext_id:
    description:
        - The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
ext_id:
    description:
        - The External ID of the Volume Group.
    returned: always
    type: str
    sample: "9341e04e-45dd-4ffa-8775-f5b4218a85c7"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
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
    returned: When there is an error
    type: str
    sample: "Api Exception raised while reverting Volume Group"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import get_vg_api_instance  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client as volumes_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as volumes_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        volume_group_recovery_point_ext_id=dict(type="str", required=True),
    )
    return module_args


def revert_volume_group(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.RevertSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating revert Volume Group spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.revert_volume_group(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while reverting Volume Group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_volumes_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_vg_api_instance(module)
    revert_volume_group(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
