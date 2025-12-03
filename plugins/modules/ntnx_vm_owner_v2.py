#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_owner_v2
short_description: Assign owner to a VM using PC v4 APIs
version_added: 2.4.0
description:
    - Assign owner to a VM
    - This module uses PC v4 APIs based SDKs
options:
    vm_ext_id:
        description:
            - External ID of the VM
        type: str
        required: true
    owner:
        description:
            - Owner field to add owner details
        type: dict
        required: true
        suboptions:
            ext_id:
                description:
                    - External ID of the owner
                type: str
                required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""
EXAMPLES = r"""
- name: Assign owner to a VM
  nutanix.ncp.ntnx_vm_owner_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    owner:
        ext_id: "00000000-0000-0000-0000-000000000000"
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
    description:
        - Response for assigning owner to a VM
        - VM details if C(wait) is true.
        - Task details if C(wait) is false.
    returned: always
    type: dict
    sample:
        

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str
    sample: "Failed to get etag for VM"

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the VM
    returned: always
    type: str
    sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
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
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402

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
        vm_ext_id=dict(type="str", required=True),  # external id of the VM
        owner=dict(
            type="dict",
            required=True,
            suboptions=dict(
                ext_id=dict(type="str", required=True),
            ),
        ),
    )

    return module_args


def assign_owner_to_vm(module, result):
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id
    vms = get_vm_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.AhvConfigOwnershipInfo()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for assign owner to VM", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return
    vm = get_vm(module, vms, vm_ext_id)
    etag = get_etag(vm)
    if not etag:
        module.fail_json(msg="Failed to get etag for VM", **result)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.assign_vm_owner(extId=vm_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while assigning owner to VM",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        vm = get_vm(module, vms, vm_ext_id)
        result["response"] = strip_internal_attributes(vm.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
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
        "task_ext_id": None,
    }
    assign_owner_to_vm(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
