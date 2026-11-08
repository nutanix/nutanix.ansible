#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_nvmf_clients_v2
short_description: Attach and detach NVMe-TCP clients to Nutanix Volume Groups
version_added: 2.7.0
description:
  - This module allows you to attach and detach NVMe-TCP clients to or from a Volume Group.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Attach an NVMe-TCP client to the given Volume Group) -
    Required Roles: Prism Admin, Project Admin, Project Manager,
    Self-Service Admin (Deprecated), Storage Admin, Super Admin
  - >-
    B(Detach a NVMe-TCP client from the given Volume Group) -
    Required Roles: Prism Admin, Project Admin, Project Manager,
    Self-Service Admin (Deprecated), Storage Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  state:
    description:
      - If C(state) is set to C(present), the module will attach an NVMe-TCP client to the Volume Group.
      - If C(state) is set to C(absent), the module will detach an NVMe-TCP client from the Volume Group.
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
  volume_group_ext_id:
    description:
      - The external identifier of a Volume Group.
    type: str
    required: true
  nvmf_initiator_name:
    description:
      - NVMe-TCP client qualified name.
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
- name: Attach NVMe-TCP client to Volume Group
  nutanix.ncp.ntnx_volume_groups_nvmf_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    nvmf_initiator_name: "nqn.2025-12.org.nvmexpress:uuid:59d5de78-a964-5746-8c6e-677c4c7a79df"
  register: result
  ignore_errors: true

- name: Detach NVMe-TCP client from Volume Group
  nutanix.ncp.ntnx_volume_groups_nvmf_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    nvmf_initiator_name: "nqn.2025-12.org.nvmexpress:uuid:59d5de78-a964-5746-8c6e-677c4c7a79df"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for attaching or detaching an NVMe-TCP client.
    - If C(wait) is true, it will contain the final task payload after completion.
    - If C(wait) is false, it will contain the initial task details.
  type: dict
  returned: always
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
          "rel": "volumes:config:nvmf-client"
        },
        {
          "ext_id": "11ac5593-c9cf-403d-641c-3bf76eff2193",
          "rel": "volumes:config:volume-group"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:e7b6ff28-e5f1-4316-82e8-96368cc851d7",
      "is_cancelable": false,
      "last_updated_time": "2026-05-20T05:19:00.229642+00:00",
      "legacy_error_message": null,
      "operation": "VolumeGroupAttachExternal",
      "operation_description": "Volume group attach to NVMe-TCP Client",
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
  description: NVMe-TCP client external ID.
  type: str
  returned: always
  sample: "aea43b5c-ae4d-4b60-934b-f8f581275dec"

volume_group_ext_id:
  description: Volume Group external ID.
  type: str
  returned: always
  sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"

task_ext_id:
  description: The task external ID.
  type: str
  returned: always
  sample: "ZXJnb24=:e7b6ff28-e5f1-4316-82e8-96368cc851d7"

changed:
  description: Indicates whether the resource has changed.
  type: bool
  returned: always
  sample: true

failed:
  description: Indicates whether the task failed.
  type: bool
  returned: always
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or in check mode operation
  type: str
  sample: "NVMe-TCP client with ext_id:aea43b5c-ae4d-4b60-934b-f8f581275dec will be detached."

error:
  description: The error message if any.
  type: str
  returned: when an error occurs
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
        nvmf_initiator_name=dict(type="str", required=False),
    )
    return module_args


def attach_nvmf_client(module, result, api_instance):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.NvmfClient()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating attach NVMe-TCP client to volume group spec",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.attach_nvmf_client(
            body=spec, extId=volume_group_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while attaching NVMe-TCP client to volume group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.NVMF_CLIENT
        )
        if ext_id:
            result["ext_id"] = ext_id
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for the Volume Group NVMe-TCP client"
                ),
                msg="Failed to get entity ext_id from task for the Volume Group NVMe-TCP client",
            )
    result["changed"] = True


def detach_nvmf_client(module, result, api_instance):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    nvmf_initiator_name = module.params.get("nvmf_initiator_name")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.NvmfClient()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating detach NVMe-TCP client from volume group spec",
            **result,
        )

    if module.check_mode:
        result["msg"] = (
            "NVMe-TCP client with initiator name:{0} will be detached.".format(
                nvmf_initiator_name
            )
        )
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.detach_nvmf_client(
            body=spec, extId=volume_group_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while detaching NVMe-TCP client from volume group",
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
            msg=missing_required_lib("ntnx_volumes_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
    }
    state = module.params.get("state")
    api_instance = get_vg_api_instance(module)
    if state == "present":
        attach_nvmf_client(module, result, api_instance)
    else:
        detach_nvmf_client(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
