#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_revert_volume_group_v2
short_description: Revert a Volume Group to a Volume Group recovery point in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to revert an existing Volume Group in Nutanix Prism Central
    to the state captured in a previously created Volume Group recovery point.
  - The Volume Group is identified by its external ID and the recovery point is
    identified by the Volume Group recovery point external ID that lives inside a
    top-level recovery point.
  - This module uses PC v4 APIs based SDKs.
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  state:
    description:
      - The state of the operation.
      - Only C(present) is supported for the revert action.
    type: str
    required: false
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external identifier of the Volume Group to be reverted.
    type: str
    required: true
  volume_group_recovery_point_ext_id:
    description:
      - The external identifier of the Volume Group recovery point that the
        Volume Group should be reverted to.
      - This must be the ext_id of the Volume Group recovery point (nested under
        a top-level recovery point), not the ext_id of the top-level recovery point.
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
  nutanix.ncp.ntnx_revert_volume_group_v2:
    ext_id: "530567f3-abda-4913-b5d0-0ab6758ec165"
    volume_group_recovery_point_ext_id: "b2f6c1de-2e59-4a1c-9d5c-2c7a10a37c7a"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for the revert Volume Group operation.
    - Task details if C(wait) is true (task waits until the revert completes).
    - Task submission details if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-20T06:26:51.524581+00:00",
      "completion_details": null,
      "created_time": "2026-07-20T06:26:47.167906+00:00",
      "entities_affected": [
        {
          "ext_id": "530567f3-abda-4913-b5d0-0ab6758ec165",
          "rel": "volumes:config:volume-group"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T06:26:51.524581+00:00",
      "legacy_error_message": null,
      "operation": "RevertVolumeGroup",
      "operation_description": "Revert Volume Group",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-20T06:26:47.185754+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task that performed the revert.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description:
    - The external ID of the Volume Group that was reverted.
  returned: always
  type: str
  sample: "530567f3-abda-4913-b5d0-0ab6758ec165"

changed:
  description:
    - This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - This indicates whether the operation was skipped (e.g. in check mode).
  returned: when applicable
  type: str
  sample: "Volume Group with ext_id:530567f3-abda-4913-b5d0-0ab6758ec165 will be reverted to recovery point b2f6c1de-2e59-4a1c-9d5c-2c7a10a37c7a."

error:
  description:
    - The error message if any error occurred while performing the revert.
  returned: When an error occurs
  type: str
  sample: "Failed to get etag for Volume Group"

failed:
  description:
    - This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description:
    - Status or informational message.
    - Populated on error, in check mode, or when the module short-circuits.
  returned: when applicable
  type: str
  sample: "Api Exception raised while reverting Volume Group"
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
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        volume_group_recovery_point_ext_id=dict(type="str", required=True),
    )
    return module_args


def revert_volume_group(module, result, api_instance):
    """Revert the target Volume Group to the given Volume Group recovery point."""
    validate_required_params(module, ["ext_id", "volume_group_recovery_point_ext_id"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.RevertSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for revert Volume Group", **result)

    if module.check_mode:
        recovery_point_ext_id = module.params.get("volume_group_recovery_point_ext_id")
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["skipped"] = (
            "Volume Group with ext_id:{0} will be reverted to recovery " "point {1}."
        ).format(ext_id, recovery_point_ext_id)
        result["msg"] = result["skipped"]
        return

    vg = get_volume_group(module, api_instance, ext_id)
    etag = get_etag(vg)
    if not etag:
        module.fail_json(
            msg="Failed to get etag for Volume Group with ext_id:{0}".format(ext_id),
            **result,
        )
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.revert_volume_group(extId=ext_id, body=spec, **kwargs)
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
        entity_ext_id = get_entity_ext_id_from_task(
            task, rel=TASK_CONSTANTS.RelEntityType.VOLUME_GROUP
        )
        if entity_ext_id:
            result["ext_id"] = entity_ext_id
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Volume Group"
                ),
                msg="Failed to get entity ext_id from task for Volume Group",
            )
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
        "failed": False,
    }

    api_instance = get_vg_api_instance(module)
    revert_volume_group(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
