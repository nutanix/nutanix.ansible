#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_disk_hydration_v2
short_description: Enable or disable hydration for a VM disk in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to enable or disable background hydration
    (storage migration) on a Nutanix AHV VM disk in Nutanix Prism Central.
  - Enable hydration triggers a background migration of the VM disk data
    from an external repository (for example an NFS-backed Instant
    Recovery target) to the local storage container, so the VM can be
    served from Nutanix ADSF once the migration completes.
  - Disable hydration pauses/stops the background storage migration for
    the specified VM disk. The hydration can later be resumed by calling
    this module again with C(state=present).
  - If C(state) is C(present), hydration is enabled for the VM disk.
  - If C(state) is C(absent), hydration is disabled for the VM disk.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Enable hydration for a VM disk) -
    Required Roles: Backup Admin, Cluster Admin, Consumer, Developer, Disaster Recovery Admin, Operator, Prism Admin, Project Admin, Project Manager,
    Super Admin, Virtual Machine Admin, Virtual Machine Operator, Self-Service Admin (deprecated)
  - >-
    B(Disable hydration for a VM disk) -
    Required Roles: Backup Admin, Cluster Admin, Consumer, Developer, Disaster Recovery Admin, Operator, Prism Admin, Project Admin, Project Manager,
    Super Admin, Virtual Machine Admin, Virtual Machine Operator, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - If C(state) is set to C(present), hydration is enabled on the
        specified VM disk.
      - If C(state) is set to C(absent), hydration is disabled on the
        specified VM disk.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  vm_ext_id:
    description:
      - The external ID of the VM the disk belongs to.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the VM disk on which hydration will be
        enabled or disabled.
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
- name: Enable hydration for a VM disk
  nutanix.ncp.ntnx_vm_disk_hydration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    ext_id: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"
  register: enable_result
  ignore_errors: true

- name: Disable hydration for a VM disk
  nutanix.ncp.ntnx_vm_disk_hydration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    ext_id: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"
  register: disable_result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for enabling or disabling hydration for a VM disk.
    - Task details when C(wait) is true (default).
    - Contains the task/response payload returned by the SDK when
      C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T05:31:04.812371+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T05:31:03.129843+00:00",
      "entities_affected": [
        {
          "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
          "rel": "vmm:ahv:config:vm"
        },
        {
          "ext_id": "0f34a2a7-6068-48ba-859d-1ced14d7f5da",
          "rel": "vmm:ahv:config:vm:disk"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T05:31:04.812371+00:00",
      "legacy_error_message": null,
      "operation": "EnableVmDiskHydration",
      "operation_description": "Enable hydration for a VM disk",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-21T05:31:03.194103+00:00",
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
  description: The message associated with the task if any.
  returned: When there is an error, or when in check mode.
  type: str
  sample: "Api Exception raised while enabling hydration for VM disk"

error:
  description: The error message if any error occurred during the operation.
  returned: When an error occurs
  type: str
  sample: "Failed to fetch etag for VM disk hydration operation"

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

task_ext_id:
  description: The external ID of the task associated with the operation.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the VM disk on which hydration was enabled or disabled.
  returned: always
  type: str
  sample: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"

vm_ext_id:
  description: The external ID of the VM that owns the disk.
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
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    # pylint: disable=unused-import
    import ntnx_vmm_py_client as virtual_machine_management_sdk  # noqa: E402, F401
except ImportError:
    # pylint: disable=unused-import
    from ..module_utils.v4.sdk_mock import (  # noqa: E402, F401
        mock_sdk as virtual_machine_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def _get_if_match_kwargs(module, api_instance, vm_ext_id):
    """Fetch the parent VM and return an if_match kwargs dict.

    Hydration endpoints are AHV VM $action endpoints — the SDK
    accepts an optional If-Match header populated from the parent
    VM's ETag. We fetch the VM once and pass its ETag along for
    optimistic concurrency; if the SDK returns no ETag we simply
    skip the header (see ENG-859716 which makes ETag optional on
    $action endpoints).
    """
    vm = get_vm(module, api_instance, vm_ext_id)
    etag = get_etag(vm)
    if etag:
        return {"if_match": etag}
    return {}


def enable_vm_disk_hydration(module, result, api_instance):
    """Enable hydration on the specified VM disk."""
    vm_ext_id = module.params.get("vm_ext_id")
    ext_id = module.params.get("ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Hydration will be enabled for VM disk with ext_id:{0} on VM ext_id:{1}."
        ).format(ext_id, vm_ext_id)
        return

    kwargs = _get_if_match_kwargs(module, api_instance, vm_ext_id)

    resp = None
    try:
        resp = api_instance.enable_vm_disk_hydration(
            vmExtId=vm_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while enabling hydration for VM disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def disable_vm_disk_hydration(module, result, api_instance):
    """Disable hydration on the specified VM disk."""
    vm_ext_id = module.params.get("vm_ext_id")
    ext_id = module.params.get("ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Hydration will be disabled for VM disk with ext_id:{0} on VM ext_id:{1}."
        ).format(ext_id, vm_ext_id)
        return

    kwargs = _get_if_match_kwargs(module, api_instance, vm_ext_id)

    resp = None
    try:
        resp = api_instance.disable_vm_disk_hydration(
            vmExtId=vm_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disabling hydration for VM disk",
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
        "vm_ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }
    api_instance = get_vm_api_instance(module)

    state = module.params.get("state")
    if state == "present":
        enable_vm_disk_hydration(module, result, api_instance)
    else:
        disable_vm_disk_hydration(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
