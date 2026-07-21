#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_attachments_by_volume_group_id_v2
short_description: Attach or detach an AHV VM as a VmAttachment on a Nutanix Volume Group.
version_added: 2.7.0
description:
  - This module manages VmAttachmentsByVolumeGroupId on a Nutanix Volume Group in Prism Central.
  - A VmAttachment binds an AHV VM directly to a Volume Group so the VG is hot-plugged
    onto the VM SCSI bus (hypervisor-attached storage), bypassing the guest iSCSI path.
  - If C(state) is C(present) then an AHV VM is attached to the given Volume Group using
    the C(AttachVm) API on C(VolumeGroupsApi).
  - If C(state) is C(absent) then the referenced VM is detached from the Volume Group using
    the C(DetachVm) API on C(VolumeGroupsApi).
  - The list-side (C(ListVmAttachmentsByVolumeGroupId)) is exposed by the companion info
    module C(ntnx_volume_group_vm_attachment_info_v2).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Attach an AHV VM to the given Volume Group) -
    Required Roles: Backup Admin, Prism Admin, Project Manager, Storage Admin, Super Admin,
    Virtual Machine Admin, Self-Service Admin (deprecated)
  - >-
    B(Detach an AHV VM from the given Volume Group) -
    Required Roles: Backup Admin, Prism Admin, Project Manager, Storage Admin, Super Admin,
    Virtual Machine Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  state:
    description:
      - Specify the desired state of the VM attachment.
      - If C(state) is set to C(present) the module attaches the VM to the given Volume Group.
      - If C(state) is set to C(absent) the module detaches the VM from the given Volume Group.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  volume_group_ext_id:
    description:
      - The external identifier of the Volume Group that the VM will be attached to or detached from.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the AHV VM to attach to or detach from the Volume Group.
    type: str
    required: true
  index:
    description:
      - The index on the SCSI bus at which the Volume Group should be attached to the VM.
      - This is optional. When omitted, the hypervisor picks the next available index.
      - Ignored when C(state) is C(absent).
    type: int
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
- name: Attach VM to Volume Group at a specific SCSI index
  nutanix.ncp.ntnx_vm_attachments_by_volume_group_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4a5d"
    index: 1
  register: result

- name: Detach VM from Volume Group
  nutanix.ncp.ntnx_vm_attachments_by_volume_group_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4a5d"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response of the attach/detach operation.
    - When C(wait) is C(true) the module returns the final task details.
    - When C(wait) is C(false) the module returns the queued task response.
    - In C(check_mode) the module returns the VmAttachment spec that would be sent.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T06:09:26.134731+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T06:09:25.848056+00:00",
      "entities_affected": [
        {
          "ext_id": "2b18feee-4502-4f73-4fa7-1216446cf8e5",
          "rel": "volumes:config:volume-group"
        },
        {
          "ext_id": "16f04294-2b2b-4b2b-7b34-9cb81195f92c",
          "rel": "vmm:ahv:config:vm"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:8c8c692a-e0c6-4fa2-bbf1-10af383fab63",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T06:09:26.134730+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 2,
      "number_of_subtasks": 1,
      "operation": "VolumeGroupAttachVm",
      "operation_description": "Volume group attach to VM",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-21T06:09:25.848056+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": [
        {
          "ext_id": "ZXJnb24=:6463bfb0-9a70-4055-903a-b941e5ae7101",
          "href": "https://pc.example.com:9440/api/prism/v4.3/config/tasks/ZXJnb24=:6463bfb0-9a70-4055-903a-b941e5ae7101",
          "rel": "subtask"
        }
      ],
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the attach/detach task.
  returned: always
  type: str
  sample: "ZXJnb24=:8c8c692a-e0c6-4fa2-bbf1-10af383fab63"

ext_id:
  description:
    - The external ID of the AHV VM that was attached/detached.
  returned: always
  type: str
  sample: "16f04294-2b2b-4b2b-7b34-9cb81195f92c"

volume_group_ext_id:
  description:
    - The external ID of the Volume Group the operation was performed on.
  returned: always
  type: str
  sample: "2b18feee-4502-4f73-4fa7-1216446cf8e5"

changed:
  description: Indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
  returned: when applicable
  type: bool
  sample: false

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent, or check mode
  type: str
  sample: "Api Exception raised while attaching VM to volume group"
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        index=dict(type="int", required=False),
    )
    return module_args


def _build_vm_attachment_spec(module, result, operation):
    """Build a ``VmAttachment`` request body for the attach/detach action."""
    sg = SpecGenerator(module)
    default_spec = volumes_sdk.VmAttachment()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating {0} VM to volume group spec".format(operation),
            **result,
        )
    return spec


def _finalize_task_response(module, result, resp):
    """Populate result with task info; wait for completion when requested."""
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def create_VmAttachmentsByVolumeGroupId(module, result, api_instance):
    """Attach the requested AHV VM to the Volume Group (state=present)."""
    validate_required_params(module, ["volume_group_ext_id", "ext_id"])

    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id
    result["ext_id"] = module.params.get("ext_id")

    spec = _build_vm_attachment_spec(module, result, operation="attach")

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vg = get_volume_group(module, api_instance, volume_group_ext_id)
    etag = get_etag(vg)
    kwargs = {"if_match": etag}

    try:
        resp = api_instance.attach_vm(body=spec, extId=volume_group_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while attaching VM to volume group",
        )

    _finalize_task_response(module, result, resp)


def delete_VmAttachmentsByVolumeGroupId(module, result, api_instance):
    """Detach the requested AHV VM from the Volume Group (state=absent)."""
    validate_required_params(module, ["volume_group_ext_id", "ext_id"])

    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id
    result["ext_id"] = module.params.get("ext_id")

    spec = _build_vm_attachment_spec(module, result, operation="detach")

    if module.check_mode:
        result["msg"] = (
            "VM with ext_id: {0} will be detached from Volume Group with ext_id: {1}.".format(
                module.params.get("ext_id"), volume_group_ext_id
            )
        )
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vg = get_volume_group(module, api_instance, volume_group_ext_id)
    etag = get_etag(vg)
    kwargs = {"if_match": etag}

    try:
        resp = api_instance.detach_vm(body=spec, extId=volume_group_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while detaching VM from volume group",
        )

    _finalize_task_response(module, result, resp)


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("volume_group_ext_id", "ext_id")),
            ("state", "absent", ("volume_group_ext_id", "ext_id")),
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
        "volume_group_ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        create_VmAttachmentsByVolumeGroupId(module, result, api_instance)
    else:
        delete_VmAttachmentsByVolumeGroupId(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
