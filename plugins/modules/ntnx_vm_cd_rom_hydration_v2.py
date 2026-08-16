#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_cd_rom_hydration_v2
short_description: Enable or disable hydration for a Nutanix AHV VM CD-ROM
version_added: 2.7.0
description:
    - Enable or disable background hydration of a Nutanix AHV VM CD-ROM.
    - Hydration is the process of transferring CD-ROM/ISO data that currently
      resides on an external repository (for example the Managed Storage
      Tier used by Instant Recovery / Early Recovery workflows) into the
      cluster's local storage container.
    - If I(state) is C(present) the module calls the enable-hydration
      endpoint on the specified CD-ROM.
    - If I(state) is C(absent) the module calls the disable-hydration
      endpoint on the specified CD-ROM.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned
      to the user performing the operation. The required roles depend on
      the operation being performed.
    - >-
      B(Enable hydration for a VM CD-ROM) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - >-
      B(Disable hydration for a VM CD-ROM) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - Desired hydration state of the CD-ROM.
            - If C(state) is set to C(present) the module enables hydration
              for the CD-ROM by calling the enable-hydration action.
            - If C(state) is set to C(absent) the module disables hydration
              for the CD-ROM by calling the disable-hydration action.
        type: str
        choices:
            - present
            - absent
        default: present
    vm_ext_id:
        description:
            - A globally unique identifier of the AHV VM that owns the
              CD-ROM (UUID).
        type: str
        required: true
    ext_id:
        description:
            - A globally unique identifier of the CD-ROM (UUID) attached to
              the VM referenced by I(vm_ext_id).
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
- name: Enable hydration for a VM CD-ROM
  nutanix.ncp.ntnx_vm_cd_rom_hydration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    ext_id: "7439fc19-1733-42c8-aa86-01b08fe84a06"
  register: enable_result
  ignore_errors: true

- name: Disable hydration for a VM CD-ROM
  nutanix.ncp.ntnx_vm_cd_rom_hydration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    ext_id: "7439fc19-1733-42c8-aa86-01b08fe84a06"
  register: disable_result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for enabling or disabling hydration for a VM CD-ROM.
        - Contains the task details returned by the v4 API.
        - When C(wait) is C(true) this is the completed task object; when
          C(wait) is C(false) it is the task reference returned by the API.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-21T05:24:07.561731+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T05:24:06.695534+00:00",
            "entities_affected": [
                {
                    "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
                    "rel": "vmm:ahv:config:vm"
                },
                {
                    "ext_id": "7439fc19-1733-42c8-aa86-01b08fe84a06",
                    "rel": "vmm:ahv:config:vm:cdrom"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:d0eba95b-5ac1-5564-9be7-7137a82214ab",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T05:24:07.561730+00:00",
            "legacy_error_message": null,
            "operation": "EnableVmCdRomHydration",
            "operation_description": "Enable hydration for a VM CD-ROM",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T05:24:06.706222+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
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
    sample: "Api Exception raised while enabling hydration for VM CD-ROM"

error:
    description:
        - This field typically holds information about if the task have errors
          that occurred during the task execution.
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
    sample: "ZXJnb24=:d0eba95b-5ac1-5564-9be7-7137a82214ab"

ext_id:
    description: The external ID of the CD-ROM
    returned: always
    type: str
    sample: "7439fc19-1733-42c8-aa86-01b08fe84a06"

vm_ext_id:
    description: The external ID of the VM
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(
            type="str",
            choices=["present", "absent"],
            default="present",
        ),
        vm_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def _get_vm_etag(module, api_instance, vm_ext_id, result):
    """Fetch the VM and return its etag; fail the module if it cannot be resolved."""
    vm = get_vm(module, api_instance, vm_ext_id)
    etag = get_etag(vm)
    if not etag:
        module.fail_json(msg="Failed to get etag for VM", **result)
    return etag


def _wait_and_capture_task(module, task_ext_id, action_description, result):
    """Wait for a task and mirror its outcome back through the result dict.

    The upstream `wait_for_completion` helper calls ``module.fail_json``
    directly when the task reports ``FAILED``. That path discards the
    caller's ``result`` dict, which means identifying context (``ext_id``,
    ``vm_ext_id``, ``task_ext_id``) is lost from the module output. Passing
    ``raise_error=False`` lets us surface those fields alongside the task
    error before failing the module ourselves.
    """
    task = wait_for_completion(module, task_ext_id, raise_error=False)
    task_dict = strip_internal_attributes(task.to_dict())
    result["response"] = task_dict
    if task_dict.get("status") == "FAILED":
        result["failed"] = True
        result["error"] = task_dict.get("error_messages")
        module.fail_json(
            msg="Task Failed while {0}".format(action_description),
            **result,
        )


def enable_vm_cd_rom_hydration(module, api_instance, result):
    vm_ext_id = module.params.get("vm_ext_id")
    ext_id = module.params.get("ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    if module.check_mode:
        result["response"] = (
            "Hydration will be enabled for CD-ROM with ext_id: {0} on VM with"
            " ext_id: {1}".format(ext_id, vm_ext_id)
        )
        return

    etag = _get_vm_etag(module, api_instance, vm_ext_id, result)
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.enable_vm_cd_rom_hydration(
            vmExtId=vm_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while enabling hydration for VM CD-ROM",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        _wait_and_capture_task(
            module,
            task_ext_id,
            "enabling hydration for VM CD-ROM",
            result,
        )
    result["changed"] = True


def disable_vm_cd_rom_hydration(module, api_instance, result):
    vm_ext_id = module.params.get("vm_ext_id")
    ext_id = module.params.get("ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    if module.check_mode:
        result["response"] = (
            "Hydration will be disabled for CD-ROM with ext_id: {0} on VM with"
            " ext_id: {1}".format(ext_id, vm_ext_id)
        )
        return

    etag = _get_vm_etag(module, api_instance, vm_ext_id, result)
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.disable_vm_cd_rom_hydration(
            vmExtId=vm_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disabling hydration for VM CD-ROM",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        _wait_and_capture_task(
            module,
            task_ext_id,
            "disabling hydration for VM CD-ROM",
            result,
        )
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
        "failed": False,
        "ext_id": None,
        "vm_ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_vm_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        enable_vm_cd_rom_hydration(module, api_instance, result)
    else:
        disable_vm_cd_rom_hydration(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
