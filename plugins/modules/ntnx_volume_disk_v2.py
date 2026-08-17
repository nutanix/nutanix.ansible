#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_disk_v2
short_description: Create, Update, Delete Volume Disks in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete Volume Disks associated with a Volume Group in Nutanix Prism Central.
  - A Volume Disk is a virtual disk attached to a Volume Group, backed by a vDisk file on the Distributed Storage Fabric (DSF).
  - This module uses the Nutanix PC v4 storage APIs based SDK (C(ntnx_storage_py_client)).
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create a Volume Disk) -
    Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin,
    Project Manager, Storage Admin, Super Admin, Self-Service Admin (deprecated)
  - >-
    B(Update a Volume Disk) -
    Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin,
    Project Manager, Storage Admin, Super Admin, Self-Service Admin (deprecated)
  - >-
    B(Delete a Volume Disk) -
    Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin,
    Project Manager, Storage Admin, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create a Volume Disk.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update the Volume Disk.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete the Volume Disk.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external identifier of the Volume Disk.
      - Required for update and delete operations.
    type: str
    required: false
  volume_group_ext_id:
    description:
      - The external identifier of the Volume Group that owns the Volume Disk.
    type: str
    required: true
  index:
    description:
      - Index of the disk in the Volume Group.
      - This field is immutable after creation and controls the SCSI/NVMe target ordering.
    type: int
    required: false
  disk_size_bytes:
    description:
      - Size of the Volume Disk in bytes.
      - Required when creating a new disk backed by a Storage Container.
    type: int
    required: false
  description:
    description:
      - Optional description of the Volume Disk.
    type: str
    required: false
  disk_data_source_reference:
    description:
      - Reference to the source entity used to seed the Volume Disk's data.
      - When omitted the disk is created empty on the specified Storage Container.
    type: dict
    required: false
    suboptions:
      ext_id:
        description:
          - The external identifier of the source entity.
        type: str
        required: false
      name:
        description:
          - The name of the source entity.
        type: str
        required: false
      entity_type:
        description:
          - Type of the source entity.
        type: str
        required: false
        choices:
          - STORAGE_CONTAINER
          - VOLUME_DISK
          - VM_DISK
          - DISK_RECOVERY_POINT
  disk_storage_features:
    description:
      - Storage optimization features which must be enabled on the Volume Disk.
      - If omitted, the disk honors the parent Volume Group's storage features setting.
    type: dict
    required: false
    suboptions:
      flash_mode:
        description:
          - Flash Mode configuration for the Volume Disk.
          - When enabled the disk stays on the SSD tier and avoids down-migration.
        type: dict
        required: true
        suboptions:
          is_enabled:
            description:
              - Whether Flash Mode is enabled for the disk.
            type: bool
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
- name: Create Volume Disk with all attributes
  nutanix.ncp.ntnx_volume_disk_v2:
    state: present
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34"
    index: 1
    disk_size_bytes: 21474836480
    description: "ansible-created-volume-disk"
    disk_storage_features:
      flash_mode:
        is_enabled: true
    disk_data_source_reference:
      entity_type: "STORAGE_CONTAINER"
      ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b33"
  register: result

- name: Update Volume Disk description
  nutanix.ncp.ntnx_volume_disk_v2:
    state: present
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34"
    ext_id: "4e00e28d-4d93-4587-a8f0-4502d72224c8"
    description: "ansible-updated-volume-disk"
    disk_storage_features:
      flash_mode:
        is_enabled: false
  register: result

- name: Delete Volume Disk
  nutanix.ncp.ntnx_volume_disk_v2:
    state: absent
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34"
    ext_id: "4e00e28d-4d93-4587-a8f0-4502d72224c8"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a Volume Disk.
    - If the operation is create or update and C(wait) is true, it will return the Volume Disk details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "created_time": null,
      "description": "ansible-created-volume-disk",
      "disk_data_source_reference": null,
      "disk_size_bytes": 21474836480,
      "disk_storage_features": {
        "flash_mode": {
          "is_enabled": true
        }
      },
      "ext_id": "4e00e28d-4d93-4587-a8f0-4502d72224c8",
      "index": 1,
      "links": null,
      "storage_container_id": "10eb150f-e8b8-4d69-a828-6f23771d3723",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external identifier of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external identifier of the Volume Disk.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

volume_group_ext_id:
  description:
    - The external identifier of the parent Volume Group.
  returned: always
  type: str
  sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency
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
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Volume Disk with ext_id:4e00e28d-4d93-4587-a8f0-4502d72224c8 will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_etag,
    get_vg_api_instance,
)
from ..module_utils.v4.storage.helpers import get_volume_disk  # noqa: E402
from ..module_utils.v4.storage.spec.volume_disk import (  # noqa: E402
    VolumeDiskSpecs as vd_specs,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_storage_py_client as storage_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as storage_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

VOLUME_DISK_TASK_REL = "volumes:config:volume-group:disk"

VOLUME_DISK_READ_ONLY_FIELDS = (
    "created_time",
    "storage_container_id",
    "links",
    "tenant_id",
)


def get_module_spec():
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        index=dict(type="int"),
        disk_size_bytes=dict(type="int"),
        description=dict(type="str"),
        disk_storage_features=dict(
            type="dict",
            options=vd_specs.get_disk_storage_features_spec(),
            obj=storage_sdk.DiskStorageFeatures,
        ),
        disk_data_source_reference=dict(
            type="dict",
            options=vd_specs.get_disk_data_source_reference_spec(),
            obj=storage_sdk.EntityReference,
        ),
    )
    return module_args


def _idempotent_snapshot(spec_dict):
    """Return a comparable snapshot of a Volume Disk spec.

    We strip internal-only markers and read-only fields (populated by the
    server) so equality reflects user-controlled configuration only.
    """
    snapshot = deepcopy(spec_dict)
    strip_internal_attributes(snapshot)
    for field in VOLUME_DISK_READ_ONLY_FIELDS:
        snapshot.pop(field, None)
    return snapshot


def create_volume_disk(module, result, api_instance):
    validate_required_params(module, ["volume_group_ext_id"])
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    default_spec = storage_sdk.VolumeDisk()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create Volume Disk spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_volume_disk(
            volumeGroupExtId=volume_group_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Volume Disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(task_status, rel=VOLUME_DISK_TASK_REL)
        if ext_id:
            result["ext_id"] = ext_id
            disk = get_volume_disk(module, api_instance, volume_group_ext_id, ext_id)
            result["response"] = strip_internal_attributes(disk.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Volume Disk"
                ),
                msg="Failed to get entity ext_id from task for Volume Disk",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """Return True when the update leaves the Volume Disk unchanged."""
    return _idempotent_snapshot(old_spec_dict) == _idempotent_snapshot(update_spec_dict)


def update_volume_disk(module, result, api_instance):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")

    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id

    old_spec = get_volume_disk(module, api_instance, volume_group_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating Volume Disk", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update Volume Disk spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. No update required for Volume Disk with ext_id: {0}".format(
                ext_id
            ),
            **result,
        )

    strip_read_only_fields(update_spec, fields=VOLUME_DISK_READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_volume_disk(
            volumeGroupExtId=volume_group_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Volume Disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        disk = get_volume_disk(module, api_instance, volume_group_ext_id, ext_id)
        result["response"] = strip_internal_attributes(disk.to_dict())
    result["changed"] = True


def delete_volume_disk(module, result, api_instance):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id

    if module.check_mode:
        result["msg"] = "Volume Disk with ext_id:{0} will be deleted.".format(ext_id)
        return

    disk = get_volume_disk(module, api_instance, volume_group_ext_id, ext_id)
    etag = get_etag(data=disk)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.delete_volume_disk(
            volumeGroupExtId=volume_group_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Volume Disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

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
            msg=missing_required_lib("ntnx_storage_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "volume_group_ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }
    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_volume_disk(module, result, api_instance)
        else:
            create_volume_disk(module, result, api_instance)
    else:
        delete_volume_disk(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
