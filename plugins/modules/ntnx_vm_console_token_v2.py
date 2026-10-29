#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_console_token_v2
short_description: Generate VM console token
version_added: "2.7.0"
description:
    - Generates a token to launch a VM console.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Generate VM console token) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Project Admin, Project Manager, Super Admin,
      Virtual Machine Admin, Virtual Machine Operator
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - A globally unique identifier of a VM of type UUID.
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
    ext_id: "d85ef6d4-bd69-4c40-a77e-597a2e62751f"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for generate VM console token.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    type: dict
    returned: always
    sample:
        {
            "ext_id": "ZXJnb24=:1a1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e5e",
            "status": "SUCCEEDED",
            "operation": "GenerateVmConsoleToken",
            "progress_percentage": 100,
            "completion_details": [
                {
                    "name": "VmConsoleToken",
                    "value": "eyJhbGciOiJSUzI1NiJ9.<truncated-jwt>"
                },
                {
                    "name": "WsUri",
                    "value": "wss://10.44.76.28:9440/console/launch/d85ef6d4-bd69-4c40-a77e-597a2e62751f"
                }
            ]
        }
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:1a1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e5e"
ext_id:
    description: The external ID of the VM.
    type: str
    returned: always
    sample: "d85ef6d4-bd69-4c40-a77e-597a2e62751f"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "Console token for VM with ext_id:d85ef6d4-bd69-4c40-a77e-597a2e62751f will be generated."
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
    import ntnx_vmm_py_client  # noqa: E402, F401  # pylint: disable=unused-import
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def generate_vm_console_token(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Console token for VM with ext_id:{0} will be generated.".format(ext_id)
        )
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
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_vm_api_instance(module)
    generate_vm_console_token(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
