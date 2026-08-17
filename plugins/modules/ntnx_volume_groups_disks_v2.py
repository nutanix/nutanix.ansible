#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_disks_v2
short_description: Create, Update, Delete Volume Group Disks in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete Volume Disks
    belonging to a Volume Group in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Creates a new Volume Disk) -
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
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
    state:
        description:
            - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create Volume Disk.
            - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update Volume Disk.
            - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete Volume Disk.
        choices:
            - present
            - absent
        type: str
        required: false
        default: present
    wait:
        description: Wait for the operation to complete.
        type: bool
        required: false
        default: true
    ext_id:
        description:
            - The external ID of the Volume Disk.
            - Required for update and delete operations.
        type: str
        required: false
    volume_group_ext_id:
        description:
            - The external ID of the Volume Group that owns the disk.
        type: str
        required: true
    index:
        description:
            - Index of the disk in a Volume Group.
            - This field is optional and immutable.
        type: int
        required: false
    disk_size_bytes:
        description:
            - Size of the disk in bytes.
            - This field is mandatory during Volume Disk creation if a new disk is being created on the storage container.
        type: int
        required: false
    description:
        description:
            - Volume Disk description.
            - This is an optional field.
        type: str
        required: false
    disk_data_source_reference:
        description:
            - Reference to an entity that acts as the source for creation of the disk.
            - Used to clone from an existing V(VOLUME_DISK), V(VM_DISK) or restore from a V(DISK_RECOVERY_POINT),
              or to create a fresh disk on a V(STORAGE_CONTAINER).
            - This field is optional. If not provided, the disk is created on the default backing storage.
        type: dict
        required: false
        suboptions:
            ext_id:
                description:
                    - The external identifier of the referenced entity.
                type: str
                required: false
            name:
                description:
                    - The name of the referenced entity.
                type: str
                required: false
            entity_type:
                description:
                    - The entity type of the referenced entity.
                type: str
                required: false
                choices:
                    - STORAGE_CONTAINER
                    - VM_DISK
                    - VOLUME_DISK
                    - DISK_RECOVERY_POINT
            uris:
                description:
                    - The URIs for the referenced entity.
                type: list
                elements: str
                required: false
    disk_storage_features:
        description:
            - Storage optimization features which must be enabled on the Volume Disk.
            - This is an optional field.
            - If omitted, the disk will honor the Volume Group specific storage features setting.
        type: dict
        required: false
        suboptions:
            flash_mode:
                description:
                    - Once configured, this field will avoid down-migration of data from the hot tier
                      unless overrides are specified for the virtual disks.
                type: dict
                required: true
                suboptions:
                    is_enabled:
                        description:
                            - Indicates whether flash mode is enabled or not on the disk.
                        type: bool
                        required: true
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
- name: Create Volume Disk on a storage container with all attributes
  nutanix.ncp.ntnx_volume_groups_disks_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34"
    index: 1
    disk_size_bytes: 21474836480
    description: "ansible-created-disk"
    disk_storage_features:
      flash_mode:
        is_enabled: true
    disk_data_source_reference:
      entity_type: "STORAGE_CONTAINER"
      ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b33"
  register: result
  ignore_errors: true

- name: Update a Volume Disk with all mutable attributes
  nutanix.ncp.ntnx_volume_groups_disks_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34"
    ext_id: "4e00e28d-4d93-4587-a8f0-4502d72224c8"
    disk_size_bytes: 42949672960
    description: "ansible-updated-disk"
    disk_storage_features:
      flash_mode:
        is_enabled: false
  register: result
  ignore_errors: true

- name: Delete a Volume Disk
  nutanix.ncp.ntnx_volume_groups_disks_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34"
    ext_id: "4e00e28d-4d93-4587-a8f0-4502d72224c8"
  register: result
  ignore_errors: true
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
      "description": "ansible-created-disk",
      "disk_data_source_reference": null,
      "disk_size_bytes": 21474836480,
      "disk_storage_features": {
          "flash_mode": {
              "is_enabled": true
          }
      },
      "ext_id": "046020bf-e7e0-419e-854c-e971967eca5c",
      "index": 1,
      "links": null,
      "storage_container_id": "44481f83-d0a1-47b3-b9b8-32b5465c622e",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task associated with the operation.
  returned: always
  type: str
  sample: "ZXJnb24=:b6ef13cc-99a7-4905-b12c-c313dbd57df0"

ext_id:
  description:
    - The external ID of the Volume Disk.
  returned: always
  type: str
  sample: "046020bf-e7e0-419e-854c-e971967eca5c"

volume_group_ext_id:
  description:
    - The external ID of the Volume Group that owns the disk.
  returned: always
  type: str
  sample: "d32862d3-5218-4970-61e2-da2a2ce8df50"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency.
  returned: always
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
  description: This indicates the message if any message occurred.
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
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
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
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_etag,
    get_vg_api_instance,
)
from ..module_utils.v4.volumes.spec.volume_group import (  # noqa: E402
    VGSpecs as vg_specs,
)

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client as volumes_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as volumes_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Read-only / immutable fields that must NOT be sent back in a Volume Disk
# update body.
# * ``storage_container_id`` and ``tenant_id`` are populated by the server.
# * ``links`` is server-generated hypermedia metadata.
# * ``index`` is documented as optional AND immutable at create time — the
#   Volumes API rejects any update payload that carries it with error
#   ``VOL-40101: The index of the disk can't be changed``.
# * ``disk_data_source_reference`` is only meaningful for the create-from-source
#   operation; the server persists the resulting ``storage_container_id`` and
#   refuses to accept it back in an update body.
_VOLUME_DISK_READ_ONLY_FIELDS = (
    "storage_container_id",
    "links",
    "tenant_id",
    "index",
    "disk_data_source_reference",
)


def get_module_spec():

    disk_data_source_reference_spec = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        entity_type=dict(
            type="str",
            required=False,
            choices=[
                "STORAGE_CONTAINER",
                "VM_DISK",
                "VOLUME_DISK",
                "DISK_RECOVERY_POINT",
            ],
        ),
        uris=dict(type="list", elements="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        volume_group_ext_id=dict(type="str", required=True),
        index=dict(type="int", required=False),
        disk_size_bytes=dict(type="int", required=False),
        description=dict(type="str", required=False),
        disk_data_source_reference=dict(
            type="dict",
            options=disk_data_source_reference_spec,
            required=False,
            obj=volumes_sdk.EntityReference,
        ),
        disk_storage_features=dict(
            type="dict",
            options=vg_specs.get_storage_features_spec(),
            required=False,
            obj=volumes_sdk.DiskStorageFeatures,
        ),
    )
    return module_args


def get_volume_disk(module, api_instance, ext_id, volume_group_ext_id):
    """Fetch a Volume Disk by ext_id inside a Volume Group."""
    try:
        return api_instance.get_volume_disk_by_id(
            extId=ext_id, volumeGroupExtId=volume_group_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume Disk info using ext_id",
        )


def create_volume_disk(module, api_instance, result):
    validate_required_params(module, ["volume_group_ext_id"])
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.VolumeDisk()
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
            body=spec, volumeGroupExtId=volume_group_ext_id
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
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.VOLUME_GROUP_DISK
        )
        if ext_id:
            result["ext_id"] = ext_id
            disk = get_volume_disk(module, api_instance, ext_id, volume_group_ext_id)
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
    """Return True when the desired spec matches the current disk state."""
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    for field in _VOLUME_DISK_READ_ONLY_FIELDS:
        old_spec_dict.pop(field, None)
        update_spec_dict.pop(field, None)
    return old_spec_dict == update_spec_dict


def update_volume_disk(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id

    old_spec = get_volume_disk(module, api_instance, ext_id, volume_group_ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating Volume Disk", **result
        )

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
            msg="Nothing to change.",
            skipped=True,
            ext_id=ext_id,
            volume_group_ext_id=volume_group_ext_id,
        )

    strip_read_only_fields(update_spec, fields=_VOLUME_DISK_READ_ONLY_FIELDS)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.update_volume_disk_by_id(
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
        disk = get_volume_disk(module, api_instance, ext_id, volume_group_ext_id)
        result["response"] = strip_internal_attributes(disk.to_dict())
    result["changed"] = True


def delete_volume_disk(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id

    if module.check_mode:
        result["msg"] = "Volume Disk with ext_id:{0} will be deleted.".format(ext_id)
        return

    disk = get_volume_disk(module, api_instance, ext_id, volume_group_ext_id)
    etag = get_etag(disk)
    kwargs = {"if_match": etag} if etag else {}
    resp = None
    try:
        resp = api_instance.delete_volume_disk_by_id(
            extId=ext_id, volumeGroupExtId=volume_group_ext_id, **kwargs
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
            msg=missing_required_lib("ntnx_volumes_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
        "volume_group_ext_id": None,
        "skipped": False,
    }

    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_volume_disk(module, api_instance, result)
        else:
            create_volume_disk(module, api_instance, result)
    else:
        delete_volume_disk(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
