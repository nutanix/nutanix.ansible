#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_console_token_v2
short_description: Generate a VNC console token for an AHV VM
version_added: 2.7.0
description:
    - Generate a short-lived VNC console token (JWT) for a given AHV VM in
      Nutanix Prism Central.
    - The generated token is returned via the underlying asynchronous task
      completion details and is intended to be used together with the
      WebSocket URI (C(WsUri)) to establish a secure VNC session against
      the target VM.
    - This module wraps the Nutanix VMM v4
      C(POST /api/vmm/v4.x/ahv/config/vms/{extId}/$actions/generate-console-token)
      action endpoint.
    - This module uses PC v4 APIs based SDKs.
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will generate a new VM
              console token for the provided VM.
            - Only C(present) is supported for this action module.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The globally unique identifier (UUID) of the AHV VM for which
              the console token should be generated.
            - This is the external ID of the target User VM (UVM) — CVMs
              are not supported by this API.
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
- name: Generate VM console token
  nutanix.ncp.ntnx_vm_console_token_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
    description:
        - Response for generating the VM console token.
        - Task details when C(wait) is true (the completed task carries the
          console token / WebSocket URI in its completion details).
        - Task reference details when C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-20T17:36:20.123456+00:00",
            "completion_details": [
                {
                    "name": "VmConsoleToken",
                    "value": "eyJhbGciOiJSUzI1NiJ9.<truncated-jwt>"
                },
                {
                    "name": "WsUri",
                    "value": "wss://10.44.76.28:9440/console/launch/ac5aff0c-6c68-4948-9088-b903e2be0ce7"
                }
            ],
            "created_time": "2026-07-20T17:36:17.000000+00:00",
            "entities_affected": [
                {
                    "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
                    "rel": "vmm:ahv:config:vm"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:1a1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e5e",
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T17:36:20.123456+00:00",
            "legacy_error_message": null,
            "operation": "GenerateVmConsoleToken",
            "operation_description": "Generate VM console token",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T17:36:17.500000+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while generating VM console token"

error:
    description:
        - This field typically holds information about if the task have
          errors that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Not Found"

failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the async task that generates the console token.
    returned: always
    type: str
    sample: "ZXJnb24=:1a1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e5e"

ext_id:
    description: The external ID of the AHV VM the token was generated for.
    returned: always
    type: str
    sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client  # noqa: F401,E402  pylint: disable=unused-import
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: F401,E402  pylint: disable=unused-import
        mock_sdk as ntnx_vmm_py_client,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
    )

    return module_args


def generate_vm_console_token(module, result, api_instance):
    """
    Trigger the async VMM v4 GenerateConsoleTokenById action for the given VM.

    Args:
        module: Ansible module.
        result: shared result dict (mutated in place).
        api_instance: VmApi instance from ntnx_vmm_py_client SDK.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["response"] = {
            "ext_id": ext_id,
            "operation": "GenerateVmConsoleToken",
        }
        return

    resp = None
    try:
        resp = api_instance.generate_console_token_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while generating VM console token",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_vm_api_instance(module)
    generate_vm_console_token(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
