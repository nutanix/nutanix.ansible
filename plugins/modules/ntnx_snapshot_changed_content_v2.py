#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snapshot_changed_content_v2
short_description: Compute changed content between two mount target snapshots in Nutanix Files
version_added: 2.7.0
description:
  - This module triggers the C(compute-snapshot-change) action on a Nutanix Files
    mount target to compute the changed file system entries between two mount target
    snapshots.
  - The API asynchronously enumerates files/directories that were added, modified,
    meta-modified, deleted or renamed between the base snapshot and the target
    snapshot and stores the diff as one or more C(SnapshotChangedContent) buckets
    on the file server.
  - When C(base_snapshot_ext_id) is omitted the action computes a full-backup style
    diff where every entry is reported with C(ADD) as the operation type.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Compute Snapshot Change) -
      Required Roles: Files Admin, Prism Admin, Super Admin, Backup Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present) the module will trigger the compute
        snapshot change action on the given file server / mount target.
      - Update and delete are not supported by the Nutanix Files SnapshotChangedContent
        API, therefore C(absent) is not a valid state for this entity.
    type: str
    required: false
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external ID of a SnapshotChangedContent bucket.
      - This module does not support update, therefore providing C(ext_id) here
        will cause the module to fail with an explicit message. Use
        M(nutanix.ncp.ntnx_snapshot_changed_contents_info_v2) to fetch an
        existing bucket by C(ext_id).
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server that owns the mount target
        whose snapshots must be diffed.
      - Required for the compute operation.
    type: str
    required: false
  mount_target_ext_id:
    description:
      - The external identifier of the mount target (share) whose snapshots
        must be diffed.
      - Required for the compute operation.
    type: str
    required: false
  snapshot_ext_id:
    description:
      - External identifier of the current (target) snapshot associated with
        the changed files metadata.
      - Required for the compute operation.
    type: str
    required: false
  base_snapshot_ext_id:
    description:
      - External identifier of the base snapshot (older snapshot) used as the
        reference for the diff computation.
      - When omitted the API computes a full backup diff and every path is
        reported with operation type C(ADD).
      - Must not be identical to C(snapshot_ext_id) and must be older than it.
    type: str
    required: false
  should_show_relative_path:
    description:
      - When true, paths in the response are reported relative to the mount
        target root instead of using their absolute paths.
    type: bool
    required: false
  should_use_dfs_namespace:
    description:
      - When true, paths in the response use the DFS namespace of the mount
        target instead of raw share paths. Defaults to true in the SDK.
    type: bool
    required: false
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
- name: Compute snapshot changed content between two mount target snapshots
  nutanix.ncp.ntnx_snapshot_changed_content_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "d8a37c9e-2b6a-4a17-b76f-33d6f11f61aa"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    snapshot_ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
    base_snapshot_ext_id: "6c2c2a6c-7bd5-4e73-b74e-9fbc51c4f2e6"
    should_show_relative_path: true
    should_use_dfs_namespace: false
  register: result
  ignore_errors: true

- name: Compute full snapshot changed content (no base snapshot => full backup diff)
  nutanix.ncp.ntnx_snapshot_changed_content_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "d8a37c9e-2b6a-4a17-b76f-33d6f11f61aa"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    snapshot_ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for computing the snapshot changed content on a mount target.
    - If C(wait) is true, the response contains the terminal task details
      returned by the file server after the compute-snapshot-change task
      completes.
    - If C(wait) is false, the response contains the initial task reference
      returned by the SDK.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
          "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T07:32:12.123456+00:00",
      "completion_details": [
          {
              "name": "snapshotChangedContentExtId",
              "value": "3f8fd0f2-2e91-4b1e-9d21-2b0d5c56b6b1"
          }
      ],
      "created_time": "2026-07-21T07:32:04.987654+00:00",
      "entities_affected": [
          {
              "ext_id": "d8a37c9e-2b6a-4a17-b76f-33d6f11f61aa",
              "rel": "files:config:file-server"
          },
          {
              "ext_id": "9c1e537d-6777-4c22-5d41-ddd0c3337aa9",
              "rel": "files:config:mount-target"
          },
          {
              "ext_id": "3f8fd0f2-2e91-4b1e-9d21-2b0d5c56b6b1",
              "rel": "files:config:snapshot-changed-content"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:6f1f7f4c-6a1e-4a3c-8b8b-1a4a2b0f0e12",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T07:32:12.123456+00:00",
      "legacy_error_message": null,
      "operation": "ComputeSnapshotChange",
      "operation_description": "Compute mount target snapshot change",
      "progress_percentage": 100,
      "started_time": "2026-07-21T07:32:04.987654+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the compute-snapshot-change task returned by the API.
  returned: always
  type: str
  sample: "ZXJnb24=:6f1f7f4c-6a1e-4a3c-8b8b-1a4a2b0f0e12"

ext_id:
  description:
    - The external ID of the SnapshotChangedContent bucket produced by the
      compute-snapshot-change action.
    - Extracted from the terminal task's C(entities_affected) when C(wait)
      is true; may be null if the task did not report a bucket entity.
  returned: always
  type: str
  sample: "3f8fd0f2-2e91-4b1e-9d21-2b0d5c56b6b1"

changed:
  description: This indicates whether the task resulted in any changes on the file server.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the operation was skipped by the module.
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the module task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Contextual status/error message emitted by the module.
  returned: when the module fails, is idempotent, or is running in check mode
  type: str
  sample: "Api Exception raised while computing snapshot changed content"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_snapshot_changed_contents_api_instance,
)
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

SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Ergon task rel string for the SnapshotChangedContent bucket entity produced
# by the compute-snapshot-change action.
_SNAPSHOT_CHANGED_CONTENT_REL = "files:config:snapshot-changed-content"


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str"),
        mount_target_ext_id=dict(type="str"),
        snapshot_ext_id=dict(type="str"),
        base_snapshot_ext_id=dict(type="str"),
        should_show_relative_path=dict(type="bool"),
        should_use_dfs_namespace=dict(type="bool"),
    )
    return module_args


def create_SnapshotChangedContent(module, result, api_instance):
    """
    Trigger the compute-snapshot-change action on a mount target and record the
    resulting task / entity in the module result dict.
    """
    validate_required_params(
        module,
        ["file_server_ext_id", "mount_target_ext_id", "snapshot_ext_id"],
    )

    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")

    sg = SpecGenerator(module)
    default_spec = files_sdk.ComputeSnapshotChangeSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating compute snapshot change spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.compute_snapshot_change(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            body=spec,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while computing snapshot changed content",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        ext_id = get_entity_ext_id_from_task(task, rel=_SNAPSHOT_CHANGED_CONTENT_REL)
        if ext_id:
            result["ext_id"] = ext_id
        else:
            # The bucket ext_id may also be reported via completion_details for
            # some file server versions; if we cannot locate it, leave ext_id
            # as None (do not fail — the task itself succeeded) but surface a
            # message to help the operator use the info module directly.
            result["msg"] = (
                "Compute snapshot change task succeeded but no "
                "snapshot-changed-content ext_id was reported in "
                "entities_affected. Use ntnx_snapshot_changed_contents_info_v2 "
                "to list buckets for this mount target."
            )
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            (
                "state",
                "present",
                (
                    "file_server_ext_id",
                    "mount_target_ext_id",
                    "snapshot_ext_id",
                ),
            ),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_files_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_snapshot_changed_contents_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            module.fail_json(
                msg=(
                    "SnapshotChangedContent does not support update. To fetch "
                    "an existing bucket by ext_id use "
                    "ntnx_snapshot_changed_contents_info_v2."
                ),
                **result,
            )
        create_SnapshotChangedContent(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
