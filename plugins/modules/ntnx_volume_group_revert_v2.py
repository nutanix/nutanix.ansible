#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_revert_v2
short_description: Revert a Nutanix Volume Group to a Volume Group recovery point
version_added: 2.7.0
description:
    - Revert an existing Volume Group in Nutanix Prism Central to the state
      captured by a previously created Volume Group recovery point.
    - This is an in-place, task-based restore operation.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Revert a Volume Group) -
      Required Roles: Backup Admin, Prism Admin, Project Manager, Storage Admin, Super Admin,
      Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module reverts the Volume Group from the
              supplied recovery point.
            - Only C(present) is supported for this action module.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the Volume Group that has to be reverted.
        type: str
        required: true
    volume_group_recovery_point_ext_id:
        description:
            - The external identifier of the Volume Group recovery point to which the
              Volume Group should be reverted.
            - This is a mandatory field.
        type: str
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
- name: Revert a Volume Group to a Volume Group recovery point
  nutanix.ncp.ntnx_volume_group_revert_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6aeec7b5-6ab6-4eb6-acf9-cf1e8b14a0b8"
    volume_group_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for reverting the Volume Group from the recovery point.
        - Task details containing the outcome of the revert operation when C(wait) is
          C(true).
        - Task submission details (containing at least C(ext_id)) when C(wait) is
          C(false).
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-20T11:11:35.665908+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T11:11:33.185386+00:00",
            "entities_affected": [
                {
                    "ext_id": "ad96f00a-5331-4a05-b1a9-2f4b66bb1a63",
                    "name": "ansible-rp-revert",
                    "rel": "dataprotection:config:volume-group-recovery-point"
                },
                {
                    "ext_id": "c81e0f94-967d-4d12-5604-1193e3a23087",
                    "name": "ansible-vg-revert",
                    "rel": "volumes:config:volume-group"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:d0341bca-793a-4066-bbab-424b964a89e0",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T11:11:35.665907+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 2,
            "number_of_subtasks": 0,
            "operation": "RevertVolumeGroup",
            "operation_description": "Revert Volume Group",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T11:11:33.196992+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while reverting volume group"

error:
    description:
        - This field typically holds information about any errors that occurred during
          the task execution.
    returned: when an error occurs
    type: str
    sample: "Failed to get etag for Volume Group"

failed:
    description: This field typically holds information about if the task has failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:d0341bca-793a-4066-bbab-424b964a89e0"

ext_id:
    description: The external ID of the Volume Group that was reverted.
    returned: always
    type: str
    sample: "c81e0f94-967d-4d12-5604-1193e3a23087"
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
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_etag,
    get_vg_api_instance,
)
from ..module_utils.v4.volumes.helpers import get_volume_group  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client as volumes_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as volumes_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
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
        module.fail_json(
            msg="Failed generating spec for reverting volume group", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vg = get_volume_group(module, api_instance, ext_id)
    etag = get_etag(vg)
    if not etag:
        module.fail_json(msg="Failed to get etag for Volume Group", **result)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.revert_volume_group(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while reverting volume group",
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
            msg=missing_required_lib("ntnx_volumes_py_client"),
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
    api_instance = get_vg_api_instance(module)
    revert_volume_group(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
