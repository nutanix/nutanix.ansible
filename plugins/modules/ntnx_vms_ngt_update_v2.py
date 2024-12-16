#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_ngt_update_v2
short_description: Update Nutanix Guest Tools (NGT) configuration for a VM.
version_added: "2.0.0"
description:
    - This module allows you to update the Nutanix Guest Tools (NGT) configuration for a VM.
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    ext_id:
        description:
            - The external ID of the VM.
        type: str
        required: true
    is_enabled:
        description:
            - To enable or disable NGT for the VM.
        type: bool
        required: false
    capabilities:
        description:
            - The list of NGT capabilities to enable for the VM.
        type: list
        elements: str
        choices:
            - SELF_SERVICE_RESTORE
            - VSS_SNAPSHOT
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""


EXAMPLES = r"""
- name: Update NGT configuration for a VM
  nutanix.ncp.ntnx_vms_ngt_update_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
    capabilities:
      - SELF_SERVICE_RESTORE
      - VSS_SNAPSHOT
"""

RETURNS = r"""
response:
    description:
        - If C(wait) is true, It will show NGT configuration of VM after operation.
        - If C(wait) is false, It will show task status of NGT operation.
    type: dict
    returned: always
    sample: {
            "available_version": "4.1",
            "capabilities": [
                "VSS_SNAPSHOT"
            ],
            "guest_os_version": "linux:64:CentOS Linux-7.3.1611",
            "is_enabled": true,
            "is_installed": true,
            "is_iso_inserted": false,
            "is_reachable": true,
            "is_vm_mobility_drivers_installed": null,
            "is_vss_snapshot_capable": null,
            "version": "4.1"
        }
changed:
    description: Indicates whether the NGT configuration was changed.
    type: bool
    returned: always
    sample: false
error:
    description: The error message, if any.
    type: str
    returned: on error
    sample: "Failed to update NGT configuration."
task_ext_id:

    description: The external ID of the task, if the update operation is asynchronous.
    type: str
    returned: when the update operation is asynchronous
skipped:
    description: Indicates whether the NGT configuration update was skipped due to idempotency.
    type: bool
    returned: when the NGT configuration is already up to date
"""

import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_ngt_status  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        is_enabled=dict(type="bool"),
        capabilities=dict(
            type="list",
            elements="str",
            choices=["SELF_SERVICE_RESTORE", "VSS_SNAPSHOT"],
        ),
    )
    return module_args


def check_idempotency(current_spec, update_spec):
    current_capabilities = getattr(current_spec, "capabilities", [])
    if current_capabilities is None:
        current_capabilities = []
    updated_capabilities = getattr(update_spec, "capabilities", [])
    if updated_capabilities is None:
        updated_capabilities = []
    if (
        sorted(current_capabilities) == sorted(updated_capabilities)
        and current_spec.is_enabled == update_spec.is_enabled
    ):
        return True
    return False


def update_ngt_config(module, result):
    vmm = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    if not ext_id:
        return module.fail_json(msg="vm ext_id is required to update NGT", **result)

    result["ext_id"] = ext_id

    current_spec = get_ngt_status(module, vmm, ext_id)

    spec = deepcopy(current_spec)

    if module.params.get("capabilities") is not None:
        spec.capabilities = module.params.get("capabilities")

    if module.params.get("is_enabled") is not None:
        spec.is_enabled = module.params.get("is_enabled")

    if check_idempotency(current_spec, spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = vmm.update_guest_tools_by_id(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating NGT",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        status = get_ngt_status(module, vmm, ext_id)
        result["response"] = strip_internal_attributes(status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[("state", "present", ("capabilities", "is_enabled"), True)],
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    update_ngt_config(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
