#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_owner_v2
short_description: Assign owner of an ESXi VM in Nutanix Prism Central
version_added: 2.7.0
description:
    - Assign the owner of an ESXi virtual machine using the VM external ID.
    - Uses the Nutanix Prism Central v4 VMM API
      C(POST /api/vmm/v4.2/esxi/config/vms/{extId}/$actions/assign-owner).
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation. The required roles depend on the operation
      being performed.
    - >-
      B(Assign Owner of an ESXi VM) -
      Required Roles: Super Admin, Prism Admin, Project Manager,
      Self-Service Admin (deprecated), Internal Super Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will assign the given owner
              to the ESXi VM referenced by C(ext_id).
            - Only C(present) is supported for this action module.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The globally unique identifier (UUID) of the ESXi VM whose owner is
              being assigned.
        type: str
        required: true
    owner:
        description:
            - Owner reference to assign to the ESXi VM.
            - Required for the assign-owner operation.
        type: dict
        required: true
        suboptions:
            ext_id:
                description:
                    - The external ID (UUID) of the user or entity that will be
                      set as the owner of the VM.
                type: str
                required: true
            entity_type:
                description:
                    - The type of the entity referenced by C(owner.ext_id).
                    - The Nutanix v4 ESXi VMM API currently allows C(USER).
                type: str
                required: false
                choices:
                    - USER
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
- name: Assign owner to an ESXi VM
  nutanix.ncp.ntnx_vm_owner_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    owner:
      ext_id: "00000000-0000-0000-0000-000000000000"
      entity_type: "USER"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for assigning owner to an ESXi VM.
        - Task details if C(wait) is true (task waits to completion).
        - Task submission response if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-21T05:12:47.185754+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T05:12:40.167906+00:00",
            "entities_affected": [
                {
                    "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
                    "rel": "vmm:esxi:config:vm"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T05:12:47.185754+00:00",
            "legacy_error_message": null,
            "operation": "AssignVmOwner",
            "operation_description": "Assign VM Owner",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T05:12:40.185754+00:00",
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
    description: Status/error message returned by the module.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while assigning owner to ESXi VM"

error:
    description:
        - This field typically holds information about the error that occurred
          during execution.
    returned: when an error occurs
    type: str
    sample: "Failed to get etag for ESXi VM"

failed:
    description: This field indicates whether the task failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task tracking the assign-owner operation.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the ESXi VM whose owner was assigned.
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
    validate_required_params,
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
    """Return the argument spec for the ``ntnx_vm_owner_v2`` action module."""
    owner_spec = dict(
        ext_id=dict(type="str", required=True),
        entity_type=dict(type="str", required=False, choices=["USER"]),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        owner=dict(
            type="dict",
            options=owner_spec,
            required=True,
            obj=vmm_sdk.EsxiConfigOwnerReference,
        ),
    )

    return module_args


def assign_vm_owner(module, api_instance, result):
    """Assign the owner of an ESXi VM using the v4 VMM API."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["ext_id", "owner"])

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.EsxiConfigOwnershipInfo()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for assigning VM owner", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vm = get_esxi_vm(module, api_instance, ext_id)
    etag = get_etag(vm)
    if not etag:
        result["error"] = "Failed to get etag for ESXi VM"
        module.fail_json(msg="Failed to get etag for ESXi VM", **result)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.assign_vm_owner(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while assigning owner to ESXi VM",
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
    api_instance = get_esxi_vm_api_instance(module)
    assign_vm_owner(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
