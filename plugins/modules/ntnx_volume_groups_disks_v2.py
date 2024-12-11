#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_disks_v2
short_description: Manage Nutanix volume group disks
description:
    - This module allows you to create and delete volume group disks in Nutanix.
version_added: "2.0.0"
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then module will create vDisk.
            - if C(state) is set to C(absent) then module will delete vDisk.
        choices:
            - present
            - absent
        type: str
        default: present
    wait:
        description: Wait for the operation to complete.
        type: bool
        required: false
        default: true
    ext_id:
        description:
            - The external ID of the disk.
            - Required for C(state)=absent for delete.
        type: str
        required: false
    volume_group_ext_id:
        description:
            - Volume Group external ID.
        type: str
        required: true
    index:
        description:
            - Index of the disk in a Volume Group.
            - This field is optional and immutable.
        type: int
    disk_size_bytes:
        description:
            - Size of the disk in bytes.
            - This field is mandatory during Volume Group creation if a new disk is being created on the storage container.
        type: int
    description:
        description:
            - Volume Disk description. This is an optional field.
        type: str
    disk_data_source_reference:
        description:
            - Reference for creation of disk.
        type: dict
        suboptions:
            ext_id:
                description:
                    - External ID of the entity.
                type: str
            entity_type:
                description:
                    - Type of the entity.
                type: str
                choices:
                    - STORAGE_CONTAINER
                    - VM_DISK
                    - VOLUME_DISK
                    - DISK_RECOVERY_POINT
    disk_storage_features:
        description:
            - Storage optimization features which must be enabled on the Volume Disks.
            - This is an optional field.
            - If omitted, the disks will honor the Volume Group specific storage features setting.
        type: dict
        suboptions:
            flash_mode:
                description:
                    - Once configured, this field will avoid down migration of data from the hot tier \
                        unless the overrides field is specified for the virtual disks.
                type: dict
                required: true
                suboptions:
                    is_enabled:
                      description: Indicates whether the flash mode is enabled or not. This is an optional field.
                      type: bool
                      required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
- name: Create disk with all attributes
  ntnx_volume_groups_disks_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: "present"
    volume_group_ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34
    index: 1
    disk_size_bytes: 21474836480
    description: "ansible-created-disk"
    disk_storage_features:
      flash_mode:
        is_enabled: true
    disk_data_source_reference:
      entity_type: "STORAGE_CONTAINER"
      ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b33
  register: result
  ignore_errors: true

- name: Create disk with vdisk ref
  check_mode: true
  ntnx_volume_groups_disks_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: "present"
    volume_group_ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34
    index: 1
    description: "ansible-created-disk"
    disk_storage_features:
      flash_mode:
        is_enabled: true
    disk_data_source_reference:
      entity_type: "VM_DISK"
      ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b37
  register: result
  ignore_errors: true


- name: Create disk from volume group disk
  ntnx_volume_groups_disks_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: "present"
    volume_group_ext_id: "{{ vg1_uuid }}"
    index: 2
    description: "ansible-created-disk-updated"
    disk_storage_features:
      flash_mode:
        is_enabled: true
    disk_data_source_reference:
      entity_type: "VOLUME_DISK"
      ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b32
  register: result
  ignore_errors: true

- name: Delete a volume group disk
  ntnx_volume_groups_disks_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
    ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
    state: absent
"""

RETURN = r"""
response:
    description:
        - Disk details after creation if C(wait) is true.
        - Task details if C(wait) is false.
    type: dict
    returned: always
    sample: {
            "created_time": null,
            "description": null,
            "disk_data_source_reference": null,
            "disk_size_bytes": 21474836480,
            "disk_storage_features": {
                "flash_mode": {
                    "is_enabled": true
                }
            },
            "ext_id": "4e00e28d-4d93-4587-a8f0-4502d72224c8",
            "index": 0,
            "links": null,
            "storage_container_id": "10eb150f-e8b8-4d69-a828-6f23771d3723",
            "tenant_id": null
        }
volume_group_ext_id:
    description: Volume Group external ID.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
ext_id:
    description: Disk external ID.
    type: str
    returned: When c(wait) if true
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
task_ext_id:
    description: The task external ID.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
error:
    description: The error message if any.
    type: str
    returned: when error occurs
    sample: "Failed to create volume group disk"
changed:
    description: Indicates whether the resource has changed.
    type: bool
    returned: always
    sample: true
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
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


def get_module_spec():
    disk_data_source_reference = dict(
        ext_id=dict(type="str"),
        entity_type=dict(
            type="str",
            choices=[
                "STORAGE_CONTAINER",
                "VOLUME_DISK",
                "VM_DISK",
                "DISK_RECOVERY_POINT",
            ],
        ),
    )
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        index=dict(type="int"),
        disk_size_bytes=dict(type="int"),
        description=dict(type="str"),
        disk_storage_features=dict(
            type="dict",
            options=vg_specs.get_storage_features_spec(),
            obj=volumes_sdk.DiskStorageFeatures,
        ),
        disk_data_source_reference=dict(
            type="dict",
            options=disk_data_source_reference,
            obj=volumes_sdk.EntityReference,
        ),
    )

    return module_args


def get_volume_group_disk(module, api_instance, ext_id, volume_group_ext_id):
    try:
        return api_instance.get_volume_disk_by_id(
            extId=ext_id, volumeGroupExtId=volume_group_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume group disk info using ext_id",
        )


def create_disk(module, result):
    vgs = get_vg_api_instance(module)
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.VolumeDisk()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create volume group disk spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = vgs.create_volume_disk(body=spec, volumeGroupExtId=volume_group_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating volume group disk",
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
            resp = get_volume_group_disk(module, vgs, ext_id, volume_group_ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_disk(module, result):
    ext_id = module.params.get("ext_id")
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id

    vgs = get_vg_api_instance(module)
    vg = get_volume_group_disk(module, vgs, ext_id, volume_group_ext_id)
    etag = get_etag(vg)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vgs.delete_volume_disk_by_id(
            extId=ext_id, volumeGroupExtId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting volume group disk",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_volumes_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            # Update disk if not supported for pc.2024.1
            pass
        else:
            create_disk(module, result)
    else:
        delete_disk(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
