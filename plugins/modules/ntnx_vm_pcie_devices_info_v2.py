#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_pcie_devices_info_v2
short_description: Fetch information about PCIe devices attached to a Nutanix AHV VM
version_added: 2.5.0
description:
  - This module allows you to fetch information about PcieDevice in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific PcieDevice.
  - If C(ext_id) is not provided, list multiple PcieDevice optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get configuration details for the provided PCIe device) -
      Required Roles: Account Owner, Administrator, Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin,
      Project Manager, Storage Admin, Super Admin, User, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin,
      Self-Service Admin (deprecated)
    - >-
      B(List PCIe devices attached to a VM) -
      Required Roles: Account Owner, Administrator, Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin,
      Project Manager, Storage Admin, Super Admin, User, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin,
      Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the PCIe device attached to the VM.
      - When provided, the module fetches only that specific PCIe device.
    type: str
    required: false
  vm_ext_id:
    description:
      - The external ID (UUID) of the parent VM whose PCIe devices are to be fetched.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get a specific PCIe device attached to a VM
  nutanix.ncp.ntnx_vm_pcie_devices_info_v2:
    vm_ext_id: "c4d28fba-7adb-46b4-5495-01d795d8260b"
    ext_id: "0e6d0dcc-a7e4-47a5-54eb-d58396649a49"
  register: result
  ignore_errors: true

- name: List all PCIe devices attached to a VM
  nutanix.ncp.ntnx_vm_pcie_devices_info_v2:
    vm_ext_id: "c4d28fba-7adb-46b4-5495-01d795d8260b"
  register: result
  ignore_errors: true

- name: List PCIe devices attached to a VM with pagination
  nutanix.ncp.ntnx_vm_pcie_devices_info_v2:
    vm_ext_id: "c4d28fba-7adb-46b4-5495-01d795d8260b"
    page: 0
    limit: 10
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC PcieDevice info v4 API.
    - It can be a single PcieDevice if external ID is provided.
    - List of multiple PcieDevice if external ID is not provided (with optional pagination via C(page) / C(limit)).
  returned: always
  type: dict
  sample:
    {
      "assigned_device_info": null,
      "backing_info": {
        "device_ext_id": "348d4ecb-9ec9-55e6-ad06-5ec88eee87c0"
      },
      "ext_id": "0e6d0dcc-a7e4-47a5-54eb-d58396649a49",
      "links": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM PCIe devices info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - The external ID of the PCIe device when fetching a specific PCIe device.
  type: str
  returned: when external ID is provided
  sample: "0e6d0dcc-a7e4-47a5-54eb-d58396649a49"

vm_ext_id:
  description:
    - The external ID of the parent VM.
  type: str
  returned: always
  sample: "c4d28fba-7adb-46b4-5495-01d795d8260b"

total_available_results:
  description:
    - The total number of available PCIe devices attached to the VM.
  type: int
  returned: when all PCIe devices attached to the VM are fetched
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_pcie_device  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        vm_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_pcie_device_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id
    pcie = get_pcie_device(module, api_instance, ext_id, vm_ext_id)
    result["response"] = strip_internal_attributes(pcie.to_dict())


def get_pcie_devices(module, api_instance, result):
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VM PCIe devices info spec", **result)
    # Only page / limit are supported by list_pcie_devices_by_vm_id; drop any
    # extras that the BaseInfoModule may still expose (filter / orderby / select).
    for extra in ("_filter", "_orderby", "_select"):
        kwargs.pop(extra, None)

    try:
        resp = api_instance.list_pcie_devices_by_vm_id(vmExtId=vm_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM PCIe devices info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "vm_ext_id": None,
    }
    api_instance = get_vm_api_instance(module)
    if module.params.get("ext_id"):
        get_pcie_device_using_ext_id(module, api_instance, result)
    else:
        get_pcie_devices(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
