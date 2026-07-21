#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_mount_target_snapshot_v2
short_description: Create, Restore, and Delete mount target snapshots in Nutanix Files
version_added: 2.7.0
description:
  - This module allows you to create and delete mount target snapshots in Nutanix Files on Prism Central.
  - It also supports restoring a mount target from an existing snapshot.
  - A mount target snapshot is a point-in-time copy of a mount target (share/export) that belongs to a file server.
  - This module uses PC v4 APIs based SDKs.
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided, the operation will create a mount target snapshot.
      - If C(state) is set to C(present) and C(ext_id) is provided, the operation will restore the mount target from the snapshot.
      - If C(state) is set to C(absent) and C(ext_id) is provided, the operation will delete the mount target snapshot.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the mount target snapshot.
      - Required for restore (C(state=present)) and delete (C(state=absent)) operations.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external ID of the file server that owns the mount target.
    type: str
    required: true
  mount_target_ext_id:
    description:
      - The external ID of the mount target (share/export) to snapshot.
    type: str
    required: true
  name:
    description:
      - Mount target snapshot name.
      - Required for create operation only.
      - Minimum 1 character, maximum 80 characters.
    type: str
    required: false
  type:
    description:
      - Mount target snapshot type.
      - Used for create operation only.
    type: str
    required: false
    choices:
      - SSR_SNAPSHOT
      - USER_SNAPSHOT
      - REPLICATION_SNAPSHOT
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
- name: Create mount target snapshot
  nutanix.ncp.ntnx_files_mount_target_snapshot_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "5f1b7b3e-1234-4c47-b5db-920460c4b668"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    name: "mount_target_snapshot_ansible"
    type: "USER_SNAPSHOT"
  register: result
  ignore_errors: true

- name: Restore mount target from snapshot
  nutanix.ncp.ntnx_files_mount_target_snapshot_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "5f1b7b3e-1234-4c47-b5db-920460c4b668"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true

- name: Delete mount target snapshot
  nutanix.ncp.ntnx_files_mount_target_snapshot_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "5f1b7b3e-1234-4c47-b5db-920460c4b668"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, restoring, or deleting a mount target snapshot.
    - If the operation is create and C(wait) is true, it will return the mount target snapshot details.
    - If the operation is create and C(wait) is false, it will return the task details.
    - If the operation is restore or delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "create_time": "2026-07-21T07:36:00.000000+00:00",
      "ext_id": "48f78959-14a6-4c47-b5db-920460c4b668",
      "links": null,
      "name": "mount_target_snapshot_ansible",
      "reclaimable_space_bytes": 0,
      "tenant_id": null,
      "total_space_bytes": 0,
      "type": "USER_SNAPSHOT"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the mount target snapshot.
  returned: always
  type: str
  sample: "48f78959-14a6-4c47-b5db-920460c4b668"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: when applicable
  type: bool
  sample: false

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
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Mount target snapshot with name 'mount_target_snapshot_ansible' already exists. Skipping creation."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.files.api_client import get_snapshots_api_instance  # noqa: E402
from ..module_utils.v4.files.helpers import get_mount_target_snapshot  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
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


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        mount_target_ext_id=dict(type="str", required=True),
        name=dict(type="str"),
        type=dict(
            type="str",
            choices=["SSR_SNAPSHOT", "USER_SNAPSHOT", "REPLICATION_SNAPSHOT"],
            obj=files_sdk.SnapshotType,
        ),
    )
    return module_args


def get_mount_target_snapshot_by_name(module, api_instance, name):
    """
    This method fetches a mount target snapshot by its name for idempotency.
    Args:
        module: Ansible module
        api_instance: SnapshotsApi instance from ntnx_files_py_client sdk
        name (str): mount target snapshot name
    return:
        snapshot (object): mount target snapshot object if found, else None
    """
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")
    try:
        resp = api_instance.list_mount_target_snapshots(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            _filter="name eq '{0}'".format(name),
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while checking existing mount target snapshots",
        )
    if resp is None or resp.data is None:
        return None
    for snapshot in resp.data:
        if snapshot.name == name:
            return snapshot
    return None


def create_mount_target_snapshot(module, result, api_instance):
    validate_required_params(module, ["name"])
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")
    name = module.params.get("name")

    existing_snapshot = get_mount_target_snapshot_by_name(module, api_instance, name)
    if existing_snapshot:
        result["ext_id"] = existing_snapshot.ext_id
        result["response"] = strip_internal_attributes(existing_snapshot.to_dict())
        result["skipped"] = True
        result["msg"] = (
            "Mount target snapshot with name '{0}' already exists. "
            "Skipping creation.".format(name)
        )
        return

    sg = SpecGenerator(module)
    default_spec = files_sdk.Snapshot()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create mount target snapshot spec", **result
        )

    # Read-only fields are populated by the platform and must not be sent.
    strip_read_only_fields(
        spec, fields=["create_time", "total_space_bytes", "reclaimable_space_bytes"]
    )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_mount_target_snapshot(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            body=spec,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating mount target snapshot",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.MOUNT_TARGET_SNAPSHOT
        )
        if not ext_id:
            ext_id = get_entity_ext_id_from_task(task_status)
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_mount_target_snapshot(
                module,
                api_instance,
                ext_id,
                file_server_ext_id,
                mount_target_ext_id,
            )
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for MountTargetSnapshot"
                ),
                msg="Failed to get entity ext_id from task for MountTargetSnapshot",
            )
    result["changed"] = True


def restore_mount_target(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Mount target with ext_id:{0} will be restored from snapshot with "
            "ext_id:{1}.".format(mount_target_ext_id, ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.restore_mount_target(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            extId=ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while restoring mount target from snapshot",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def delete_mount_target_snapshot(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Mount target snapshot with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.delete_mount_target_snapshot_by_id(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            extId=ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting mount target snapshot",
        )
    task_ext_id = None
    if resp is not None and getattr(resp, "data", None) is not None:
        task_ext_id = resp.data.ext_id
        result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


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
    }
    api_instance = get_snapshots_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            restore_mount_target(module, result, api_instance)
        else:
            create_mount_target_snapshot(module, result, api_instance)
    else:
        delete_mount_target_snapshot(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
