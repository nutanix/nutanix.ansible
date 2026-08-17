#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_synchronous_replication_v2
short_description: Pause synchronous replication of a Volume Group
version_added: 2.7.0
description:
    - Pauses the synchronous replication of a protected Volume Group identified by
      its external ID.
    - Pausing the replication temporarily halts the zero-RPO mirroring of writes
      from the source Volume Group to the recovery-site Volume Group without
      destroying any data or configuration on either Prism Element.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Pause synchronous replication of a Volume Group) -
      Required Roles: Backup Admin, Prism Admin, Project Manager, Storage Admin,
      Super Admin, Self-Service Admin (deprecated).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present) the module pauses synchronous replication
              on the referenced Volume Group.
            - Any other value is not supported for this action module.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the Volume Group whose synchronous
              replication must be paused.
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
- name: Pause synchronous replication for a Volume Group
  nutanix.ncp.ntnx_volume_group_synchronous_replication_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for the pause synchronous replication action.
        - Task details when C(wait) is true.
        - The initial task submission payload when C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-20T15:26:51.524581+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T15:26:47.167906+00:00",
            "entities_affected": [
                {
                    "ext_id": "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b",
                    "rel": "storage:config:volume-group"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T15:26:51.524581+00:00",
            "legacy_error_message": null,
            "operation": "PauseVolumeGroupSynchronousReplication",
            "operation_description": "Pause Volume Group Synchronous Replication",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T15:26:47.185754+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: Indicates whether the task resulted in any change on the cluster.
    returned: always
    type: bool
    sample: true

ext_id:
    description: The external identifier of the Volume Group on which the action was requested.
    returned: always
    type: str
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"

task_ext_id:
    description: The external identifier of the asynchronous task tracking the pause action.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

msg:
    description: Optional status/error message emitted by the module.
    returned: When there is an error or in check_mode.
    type: str
    sample: "Api Exception raised while pausing synchronous replication for Volume Group"

error:
    description: Additional error details, if any, populated when an API call fails.
    returned: when an error occurs
    type: str
    sample: "Failed to get etag for Volume Group"

failed:
    description: Whether the module invocation failed.
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_etag,
    get_volume_group_api_instance,
)
from ..module_utils.v4.storage.helpers import get_volume_group  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_storage_py_client as storage_sdk  # noqa: F401, E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as storage_sdk  # noqa: F401, E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def pause_volume_group_synchronous_replication(module, result, api_instance):
    """
    Invoke the storage v4 SDK to pause synchronous replication on the Volume
    Group identified by ``module.params['ext_id']``.

    The Volume Group is fetched first so its ETag can be sent via ``If-Match``
    (mirrors the update/delete pattern used by ``ntnx_volume_groups_v2``).
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Synchronous replication for Volume Group with ext_id: {0} "
            "will be paused.".format(ext_id)
        )
        return

    volume_group = get_volume_group(module, api_instance, ext_id)
    etag = get_etag(volume_group)
    if not etag:
        module.fail_json(
            msg="Failed to get etag for Volume Group with ext_id: {0}".format(ext_id),
            **result,
        )

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.pause_volume_group_synchronous_replication(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while pausing synchronous replication "
                "for Volume Group with ext_id: {0}".format(ext_id)
            ),
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
            msg=missing_required_lib("ntnx_storage_py_client"),
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

    api_instance = get_volume_group_api_instance(module)
    pause_volume_group_synchronous_replication(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
