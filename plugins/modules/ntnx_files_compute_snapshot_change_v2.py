#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_compute_snapshot_change_v2
short_description: Compute mount target snapshot changed contents in Nutanix Files
version_added: 2.5.0
description:
  - This module allows you to trigger the "compute snapshot change" action for a mount target in
    Nutanix Files (Change File Tracking / CFT diff between two mount target snapshots).
  - When C(state) is C(present) and C(ext_id) is not provided, the module calls the
    C(POST /files/v4.0/.../mount-targets/{mountTargetExtId}/$actions/compute-snapshot-change)
    API to start a compute-snapshot-change action on the given mount target and returns
    the resulting SnapshotChangedContent resource (created from the two snapshots).
  - When C(state) is C(present) and C(ext_id) is provided, the module is idempotent and returns
    the existing SnapshotChangedContent resource without triggering the action again.
  - When C(state) is C(absent), the module is a no-op because the Files v4 API does not
    expose a delete operation for a SnapshotChangedContent (it is cleaned up by the platform).
  - This module uses PC v4 APIs based SDKs (I(ntnx_files_py_client)).
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Compute snapshot change on a mount target) -
      Required Roles: Prism Admin, Super Admin, File Server Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided, the module triggers a
        new compute-snapshot-change action.
      - If C(state) is set to C(present) and C(ext_id) is provided, the module fetches the
        existing SnapshotChangedContent (idempotent, C(changed=false)).
      - If C(state) is set to C(absent), the module is a no-op because the Files v4 API does
        not support deleting a SnapshotChangedContent resource.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the SnapshotChangedContent resource.
      - When provided, the module fetches this resource (idempotent behaviour).
      - This value is not required for a fresh compute-snapshot-change action.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external ID of the file server that hosts the mount target.
      - Required for all operations.
    type: str
    required: true
  mount_target_ext_id:
    description:
      - The external ID of the mount target on which to compute the snapshot change.
      - Required for all operations.
    type: str
    required: true
  snapshot_ext_id:
    description:
      - External ID of the current mount target snapshot to compare.
      - Required when triggering a new compute-snapshot-change action (C(state=present) and
        no C(ext_id)).
    type: str
    required: false
  base_snapshot_ext_id:
    description:
      - External ID of the base mount target snapshot to compare against.
      - When omitted, the API treats the request as a "full" diff (all files in
        C(snapshot_ext_id)); when provided, the API returns only files that changed between
        C(base_snapshot_ext_id) and C(snapshot_ext_id).
    type: str
    required: false
  should_show_relative_path:
    description:
      - When true, the API returns paths relative to the share root instead of absolute paths.
      - Defaults to the SDK default (false) when not provided.
    type: bool
    required: false
  should_use_dfs_namespace:
    description:
      - When true, the API returns paths in the DFS namespace form.
      - Defaults to the SDK default (true) when not provided.
    type: bool
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Compute snapshot change between two snapshots of a mount target
  nutanix.ncp.ntnx_files_compute_snapshot_change_v2:
    state: present
    file_server_ext_id: "6c6f6f6b-1234-4321-9abc-abcdef012345"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    snapshot_ext_id: "3e2d5fbb-0000-0000-0000-000000000002"
    base_snapshot_ext_id: "3e2d5fbb-0000-0000-0000-000000000001"
    should_show_relative_path: true
    should_use_dfs_namespace: false
  register: result
  ignore_errors: true

- name: Idempotent fetch of an existing snapshot changed content by ext_id
  nutanix.ncp.ntnx_files_compute_snapshot_change_v2:
    state: present
    file_server_ext_id: "6c6f6f6b-1234-4321-9abc-abcdef012345"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true

- name: State absent is a no-op because the API does not support delete
  nutanix.ncp.ntnx_files_compute_snapshot_change_v2:
    state: absent
    file_server_ext_id: "6c6f6f6b-1234-4321-9abc-abcdef012345"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the compute-snapshot-change action.
    - If the operation triggered a new action and C(wait) is true, this returns the
      SnapshotChangedContent details fetched after the action completes.
    - If the operation triggered a new action and C(wait) is false, this returns the task
      response payload from the SDK.
    - If C(ext_id) was provided (idempotent case), this returns the existing
      SnapshotChangedContent details.
  returned: always
  type: dict
  sample:
    {
      "base_snapshot_ext_id": "3e2d5fbb-0000-0000-0000-000000000001",
      "changed_contents": [
          {
              "access_time": null,
              "change_time": "2026-07-21T05:00:00Z",
              "creation_time": "2026-07-21T05:00:00Z",
              "inode_number": 42,
              "object_type": "FILE",
              "old_path": null,
              "operation_type": "CREATED",
              "path": "/share/dir1/file1.txt",
              "size_bytes": 1024
          }
      ],
      "ext_id": "48f78959-14a6-4c47-b5db-920460c4b668",
      "has_more_content": false,
      "links": null,
      "snapshot_ext_id": "3e2d5fbb-0000-0000-0000-000000000002",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the compute-snapshot-change task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the SnapshotChangedContent resource produced (or looked up) by
      the module.
  returned: always
  type: str
  sample: "48f78959-14a6-4c47-b5db-920460c4b668"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - This indicates whether the operation was skipped (idempotent no-op).
    - Set to true when C(ext_id) is provided (state=present) or when C(state=absent) since
      the API does not support delete.
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Status/info message emitted by the module.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: >-
    Compute snapshot change with ext_id '48f78959-14a6-4c47-b5db-920460c4b668' already exists.
    Skipping creation.
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_snapshot_changed_contents_api_instance,
)
from ..module_utils.v4.files.helpers import get_snapshot_changed_content  # noqa: E402
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

_SNAPSHOT_CHANGED_CONTENT_REL = "files:config:snapshot-changed-content"


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        mount_target_ext_id=dict(type="str", required=True),
        snapshot_ext_id=dict(type="str"),
        base_snapshot_ext_id=dict(type="str"),
        should_show_relative_path=dict(type="bool"),
        should_use_dfs_namespace=dict(type="bool"),
    )
    return module_args


def _build_compute_snapshot_change_spec(module, result):
    """Build a ComputeSnapshotChangeSpec SDK object from module params."""
    sg = SpecGenerator(module)
    default_spec = files_sdk.ComputeSnapshotChangeSpec()
    spec_attrs = {
        "snapshot_ext_id": module.params.get("snapshot_ext_id"),
        "base_snapshot_ext_id": module.params.get("base_snapshot_ext_id"),
        "should_show_relative_path": module.params.get("should_show_relative_path"),
        "should_use_dfs_namespace": module.params.get("should_use_dfs_namespace"),
    }
    spec, err = sg.generate_spec(obj=default_spec, attr=spec_attrs)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating compute snapshot change spec", **result)
    return spec


def create_ComputeSnapshotChange(module, result, api_instance):
    """Trigger a new compute-snapshot-change action on the given mount target."""
    validate_required_params(
        module, ["file_server_ext_id", "mount_target_ext_id", "snapshot_ext_id"]
    )

    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")

    spec = _build_compute_snapshot_change_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Compute snapshot change spec generated for mount target "
            "'{0}' on file server '{1}' (check mode)."
        ).format(mount_target_ext_id, file_server_ext_id)
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
            msg=(
                "Api Exception raised while triggering compute snapshot change "
                "on mount target '{0}' of file server '{1}'"
            ).format(mount_target_ext_id, file_server_ext_id),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=_SNAPSHOT_CHANGED_CONTENT_REL
        )
        if not ext_id:
            ext_id = get_entity_ext_id_from_task(task_status)
        if ext_id:
            result["ext_id"] = ext_id
            entity = get_snapshot_changed_content(
                module,
                api_instance,
                file_server_ext_id,
                mount_target_ext_id,
                ext_id,
            )
            if entity is not None:
                result["response"] = strip_internal_attributes(entity.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for compute snapshot change"
                ),
                msg="Failed to get entity ext_id from task for compute snapshot change",
            )
    result["changed"] = True


def update_ComputeSnapshotChange(module, result, api_instance):
    """
    "Update" for this action-type module is idempotent: when an ext_id is supplied and
    the resource exists, the module simply returns the existing SnapshotChangedContent
    without triggering the compute-snapshot-change action again, because the underlying
    Files v4 API does not expose an update operation for this resource.
    """
    validate_required_params(
        module, ["file_server_ext_id", "mount_target_ext_id", "ext_id"]
    )

    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")
    ext_id = module.params.get("ext_id")

    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Snapshot changed content with ext_id '{0}' would be fetched (check mode). "
            "The Files v4 API does not support updating a SnapshotChangedContent."
        ).format(ext_id)
        return

    entity = get_snapshot_changed_content(
        module,
        api_instance,
        file_server_ext_id,
        mount_target_ext_id,
        ext_id,
    )
    if entity is not None:
        result["response"] = strip_internal_attributes(entity.to_dict())
    result["skipped"] = True
    result["changed"] = False
    result["msg"] = (
        "Compute snapshot change with ext_id '{0}' already exists. "
        "Skipping creation."
    ).format(ext_id)


def delete_ComputeSnapshotChange(module, result, api_instance):
    """
    Delete is a no-op: the Files v4 API does not expose a delete endpoint for a
    SnapshotChangedContent. The module reports the operation as skipped so that
    playbooks using ``state=absent`` do not fail unexpectedly.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Snapshot changed content with ext_id '{0}' would NOT be deleted; the Files v4 "
            "API does not support delete for this resource (check mode)."
        ).format(ext_id)
        return

    result["skipped"] = True
    result["changed"] = False
    result["msg"] = (
        "Delete is not supported by the Files v4 API for a compute snapshot change "
        "resource. Skipping delete for ext_id '{0}'."
    ).format(ext_id)


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
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
            update_ComputeSnapshotChange(module, result, api_instance)
        else:
            create_ComputeSnapshotChange(module, result, api_instance)
    else:
        delete_ComputeSnapshotChange(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
