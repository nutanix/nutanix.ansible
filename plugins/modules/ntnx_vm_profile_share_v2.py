#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_profile_share_v2
short_description: Share or unshare a VM profile with a project in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Share a VM profile with a project or unshare a VM profile from a project in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Share Virtual Machine Profile With Project) -
      Required Roles: Super Admin
    - >-
      B(Unshare Virtual Machine Profile From Project) -
      Required Roles: Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - Specify state.
            - If C(state) is set to C(present), the VM profile is shared with the project.
            - If C(state) is set to C(absent), the VM profile is unshared from the project.
        type: str
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - The external ID (UUID) of the VM profile.
        type: str
        required: true
    project_ext_id:
        description:
            - The external ID (UUID) of the project to share the VM profile with or to unshare the VM profile from.
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
- name: Share a VM profile with a project
  nutanix.ncp.ntnx_vm_profile_share_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11"
    project_ext_id: "26ff200c-e24c-47f7-809b-00a571fe7ecc"
  register: result

- name: Unshare a VM profile from a project
  nutanix.ncp.ntnx_vm_profile_share_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11"
    project_ext_id: "26ff200c-e24c-47f7-809b-00a571fe7ecc"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for sharing or unsharing a VM profile.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    type: dict
    returned: always
    sample:
        {
            "completed_time": "2027-01-12T05:31:44.875612+00:00",
            "created_time": "2027-01-12T05:31:44.382175+00:00",
            "entities_affected": [
                {
                    "ext_id": "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11",
                    "name": "ai.xlarge.h100.8gpu",
                    "rel": "vmm:ahv:config:vm-profile"
                }
            ],
            "ext_id": "ZXJnb24=:f1e19e35-8c51-53f5-a699-70dd11f8724d",
            "operation": "ShareVmProfileWithProject",
            "progress_percentage": 100,
            "status": "SUCCEEDED"
        }
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: when the VM profile is shared or unshared
    sample: "ZXJnb24=:f1e19e35-8c51-53f5-a699-70dd11f8724d"
ext_id:
    description: The external ID of the VM profile.
    type: str
    returned: always
    sample: "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error
    sample: "Api Exception raised while sharing VM profile with project"
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
from ..module_utils.v4.vmm.api_client import get_vm_profile_api_instance  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present", "absent"]),
        ext_id=dict(type="str", required=True),
        project_ext_id=dict(type="str", required=True),
    )
    return module_args


def share_vm_profile(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.ShareVmProfileWithProjectParams()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating share VM profile spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.share_vm_profile_with_project(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while sharing VM profile with project",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def unshare_vm_profile(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.UnshareVmProfileFromProjectParams()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating unshare VM profile spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.unshare_vm_profile_from_project(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while unsharing VM profile from project",
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
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False, "ext_id": None}

    api_instance = get_vm_profile_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        share_vm_profile(module, result, api_instance)
    else:
        unshare_vm_profile(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
