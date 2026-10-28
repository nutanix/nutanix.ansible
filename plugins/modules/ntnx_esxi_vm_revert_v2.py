#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_esxi_vm_revert_v2
short_description: Revert an ESXi VM from a recovery point in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Revert an ESXi VM from a recovery point using VM external ID
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Revert ESXi Virtual Machine) -
      Required Roles: Prism Admin, Project Manager, Self-Service Admin (deprecated), Super Admin, Disaster Recovery Admin, Backup Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will revert an ESXi VM from a recovery point.
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - External ID of the ESXi VM
        type: str
        required: true
    vm_recovery_point_ext_id:
        description:
            - VM recovery point external ID
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
- name: Revert an ESXi VM to a Recovery Point
  nutanix.ncp.ntnx_esxi_vm_revert_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    vm_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
    description:
        - Task details of the revert operation.
        - In check mode, the request spec which would be sent.
    returned: always
    type: dict
    sample:
        {
        "completed_time": "2024-09-04T06:26:51.524581+00:00",
        "created_time": "2024-09-04T06:26:47.167906+00:00",
        "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
        "is_cancelable": false,
        "last_updated_time": "2024-09-04T06:26:51.524581+00:00",
        "operation": "RevertVm",
        "operation_description": "Revert VM",
        "progress_percentage": 100,
        "started_time": "2024-09-04T06:26:47.185754+00:00",
        "status": "SUCCEEDED"
        }

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while reverting ESXi VM"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task
    returned: when a revert task is triggered
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the ESXi VM
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
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_esxi_vm_api_instance,
    get_etag,
)
from ..module_utils.v4.vmm.helpers import get_esxi_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),  # external id of the ESXi VM
        vm_recovery_point_ext_id=dict(type="str", required=True),
    )

    return module_args


def revert_vm_from_recovery_point(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    vms = get_esxi_vm_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.EsxiConfigRevertParams()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for revert ESXi VM", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return
    vm = get_esxi_vm(module, vms, ext_id)
    etag = get_etag(vm)
    if not etag:
        module.fail_json(msg="Failed to get etag for ESXi VM", **result)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.revert_vm(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while reverting ESXi VM",
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
        "failed": False,
        "response": None,
        "ext_id": None,
    }
    revert_vm_from_recovery_point(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
