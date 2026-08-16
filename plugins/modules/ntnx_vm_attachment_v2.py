#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_attachment_v2
short_description: Attach and detach an AHV VM to a Volume Group in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to attach an AHV VM to a Volume Group as a hypervisor attachment.
  - It also allows you to detach the AHV VM from a Volume Group.
  - VmAttachment presents the Volume Group directly on the VM's virtual SCSI bus (bypassing
    the iSCSI network path) using the Nutanix Storage v4 API.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Attach an AHV VM to a Volume Group) -
    Required Roles: Backup Admin, Prism Admin, Project Manager, Storage Admin,
    Super Admin, Virtual Machine Admin, Self-Service Admin (deprecated)
  - >-
    B(Detach an AHV VM from a Volume Group) -
    Required Roles: Backup Admin, Prism Admin, Project Manager, Storage Admin,
    Super Admin, Virtual Machine Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  state:
    description:
      - If C(state) is set to C(present), attach the VM to the Volume Group.
      - If C(state) is set to C(absent), detach the VM from the Volume Group.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  volume_group_ext_id:
    description:
      - The external identifier of the Volume Group.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the VM being attached to (or detached from) the Volume Group.
    type: str
    required: true
  index:
    description:
      - The index on the SCSI bus to attach the VM to the Volume Group.
      - Optional. Only meaningful for attach (C(state=present)).
    type: int
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Attach a VM to a Volume Group
  nutanix.ncp.ntnx_vm_attachment_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    volume_group_ext_id: "d4a91ba0-2af7-4b40-91a4-4b40deadbeef"
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    index: 1
  register: attach_result

- name: Detach the VM from the Volume Group
  nutanix.ncp.ntnx_vm_attachment_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    volume_group_ext_id: "d4a91ba0-2af7-4b40-91a4-4b40deadbeef"
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
  register: detach_result
"""

RETURN = r"""
response:
  description:
    - Response for attaching or detaching a VM to/from a Volume Group.
    - Task details when C(wait) is true.
    - Spec (dict) when C(check_mode) is true.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-05-20T05:19:00.229645+00:00",
      "completion_details": null,
      "created_time": "2026-05-20T05:19:00.095273+00:00",
      "entities_affected": [
        {
          "ext_id": "aea43b5c-ae4d-4b60-934b-f8f581275dec",
          "rel": "storage:config:vms"
        },
        {
          "ext_id": "11ac5593-c9cf-403d-641c-3bf76eff2193",
          "rel": "storage:config:volume-group"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:e7b6ff28-e5f1-4316-82e8-96368cc851d7",
      "is_cancelable": false,
      "last_updated_time": "2026-05-20T05:19:00.229642+00:00",
      "legacy_error_message": null,
      "operation": "VolumeGroupAttachExternal",
      "operation_description": "Volume group attach to VM",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-05-20T05:19:00.122260+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }
ext_id:
  description: External ID of the VM being attached/detached.
  type: str
  returned: always
  sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
volume_group_ext_id:
  description: External ID of the Volume Group involved in the operation.
  type: str
  returned: always
  sample: "d4a91ba0-2af7-4b40-91a4-4b40deadbeef"
task_ext_id:
  description: The external ID of the task associated with the attach/detach operation.
  type: str
  returned: always
  sample: "ZXJnb24=:e7b6ff28-e5f1-4316-82e8-96368cc851d7"
msg:
  description: Status/error message.
  type: str
  returned: contextual
  sample: "Api Exception raised while attaching VM to Volume Group"
error:
  description: The error message if any.
  type: str
  returned: when an error occurs
  sample: "Api Exception raised while attaching VM to Volume Group"
changed:
  description: This indicates whether the task resulted in any changes.
  type: bool
  returned: always
  sample: true
failed:
  description: This indicates whether the task failed.
  type: bool
  returned: always
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_etag,
    get_vg_api_instance,
)
from ..module_utils.v4.storage.helpers import get_volume_group  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
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


def get_module_spec():
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        index=dict(type="int", required=False),
    )
    return module_args


def _build_vm_attachment_spec(module, result, operation):
    """Build the VmAttachment body for the storage v4 SDK attach/detach calls."""
    sg = SpecGenerator(module)
    default_spec = storage_sdk.VmAttachment()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating {0} VM to Volume Group spec".format(operation),
            **result,
        )
    return spec


def attach_vm(module, result, api_instance):
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
    if not etag:
        module.fail_json(
            msg="Failed to fetch etag for Volume Group '{0}' before attaching VM".format(
                volume_group_ext_id
            ),
            **result,
        )
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.attach_vm(extId=volume_group_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while attaching VM to Volume Group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def detach_vm(module, result, api_instance):
    validate_required_params(module, ["volume_group_ext_id", "ext_id"])
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id
    result["ext_id"] = module.params.get("ext_id")

    spec = _build_vm_attachment_spec(module, result, operation="detach")

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vg = get_volume_group(module, api_instance, volume_group_ext_id)
    etag = get_etag(vg)
    if not etag:
        module.fail_json(
            msg="Failed to fetch etag for Volume Group '{0}' before detaching VM".format(
                volume_group_ext_id
            ),
            **result,
        )
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.detach_vm(extId=volume_group_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while detaching VM from Volume Group",
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
    }
    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        attach_vm(module, result, api_instance)
    else:
        detach_vm(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
