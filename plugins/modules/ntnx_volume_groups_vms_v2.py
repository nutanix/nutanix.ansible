#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_vms_v2
short_description: Attach/Detach volume group to AHV VMs in Nutanix PC
description:
    - Attach/Detach volume group to AHV VMs in Nutanix PC
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then module will attach VG to VM.
            - If C(state) is set to C(present) then module will detach VG from VM.
        choices:
            - present
            - absent
        type: str
        default: present
    wait:
        description: Wait for the operation to complete.
        type: bool
        required: false
        default: True
    ext_id:
        description:
            - The external ID of the VM
            - Its required for delete.
        type: str
        required: true
    volume_group_ext_id:
        description:
            - The external ID of the volume group.
        type: str
        required: true
    index:
        description:
            - The index on the SCSI bus to attach the VM to the Volume Group.
            - This is an optional field.
        type: int
        required: false

extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
"""

EXAMPLES = r"""
- name: Attach VM to VG
  nutanix.ncp.ntnx_volume_groups_vms_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: present
    volume_group_ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35
    ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4asda
    index: 1
  register: result

- name: Detach VM from VG
  ntnx_volume_groups_vms_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: absent
    volume_group_ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35
    ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b
  register: result
"""

RETURN = r"""
response:
    description:
       - Task details
    type: dict
    returned: always
    sample:  {
            "cluster_ext_ids": [
                "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2024-05-20T05:19:00.229645+00:00",
            "completion_details": null,
            "created_time": "2024-05-20T05:19:00.095273+00:00",
            "entities_affected": [
                {
                    "ext_id": "aea43b5c-ae4d-4b60-934b-f8f581275dec",
                    "rel": "volumes:config:vms"
                },
                {
                    "ext_id": "11ac5593-c9cf-403d-641c-3bf76eff2193",
                    "rel": "volumes:config:volume-group"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:e7b6ff28-e5f1-4316-82e8-96368cc851d7",
            "is_cancelable": false,
            "last_updated_time": "2024-05-20T05:19:00.229642+00:00",
            "legacy_error_message": null,
            "operation": "VolumeGroupAttachExternal",
            "operation_description": "Volume group attach to VM",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2024-05-20T05:19:00.122260+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }
ext_id:
    description: VM external ID.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
volume_group_ext_id:
    description: Volume group external ID.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
task_ext_id:
    description: The task external ID.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Failed generating attach VM to volume group spec"
error:
    description: The error message if any.
    type: str
    returned: when error occurs
    sample: "Api Exception raised while attaching VM to volume group"
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
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
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
        index=dict(type="int"),
    )

    return module_args


def attach_vm(module, result):
    vgs = get_vg_api_instance(module)
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id
    result["ext_id"] = module.params.get("ext_id")

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.VmAttachment()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating attach VM to volume group spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vg = get_volume_group(module, vgs, volume_group_ext_id)
    etag = get_etag(vg)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vgs.attach_vm(body=spec, extId=volume_group_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while attaching VM to volume group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def detach_vm(module, result):
    vgs = get_vg_api_instance(module)
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id
    result["ext_id"] = module.params.get("ext_id")

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.VmAttachment()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating detach VM to volume group spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vg = get_volume_group(module, vgs, volume_group_ext_id)
    etag = get_etag(vg)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vgs.detach_vm(body=spec, extId=volume_group_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while detaching VM to volume group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
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
        attach_vm(module, result)
    else:
        detach_vm(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
