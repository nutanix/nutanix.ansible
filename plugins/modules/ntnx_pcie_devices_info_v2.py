#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_pcie_devices_info_v2
short_description: Fetch PCIe devices information from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module fetches the PCIe devices information from Nutanix Prism Central.
  - If C(ext_id) is provided, the matching PCIe device is fetched using its external ID.
  - If C(ext_id) is not provided, a list of multiple PCIe devices is fetched with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs.
notes:
  - This module talks to Prism Central (PC), not to FCVM/Foundation.
  - The PCIe devices are discovered from the AHV hosts of the registered clusters.
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List PCIe devices) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the PCIe device.
      - If provided, only the PCIe device with the given external ID is returned.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all PCIe devices
  nutanix.ncp.ntnx_pcie_devices_info_v2:
  register: result
  ignore_errors: true

- name: Fetch a specific PCIe device using external ID
  nutanix.ncp.ntnx_pcie_devices_info_v2:
    ext_id: "5c3f4f9e-1c8b-4c0e-9a2d-7f6b2c1a9d3e"
  register: result
  ignore_errors: true

- name: List PCIe devices with a filter
  nutanix.ncp.ntnx_pcie_devices_info_v2:
    filter: "clusterExtId eq '000647b8-ddb3-6bbb-0000-000000028f57'"
  register: result
  ignore_errors: true

- name: List PCIe devices with a limit
  nutanix.ncp.ntnx_pcie_devices_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PCIe devices info v4 API. The host is Prism Central (PC).
    - It can be a single PCIe device if external ID is provided.
    - It can be a list of multiple PCIe devices if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_id": "00065b6f-ec68-302b-185b-ac1f6b6f97e2",
      "configuration": {
          "class_id": 2,
          "device_id": 5409,
          "prog_i_face": 0,
          "sub_class_id": 0,
          "sub_system_id": 5409,
          "sub_system_vendor_id": 5593,
          "vendor_id": 32902
      },
      "description": "Intel Corporation I350 Gigabit Network Connection (Super Micro Computer Inc X10DRW-i)",
      "ext_id": "17081fa3-3e5c-58d2-aca5-b1312414d8d9",
      "host_ext_id": "06aaf34c-9a27-4125-9557-04f87c7971eb",
      "links": null,
      "maxPartitions": 0,
      "owner_vm_ext_id": null,
      "state": "HOST_USED",
      "tenant_id": null,
      "type": "NETWORK_CONTROLLER"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the PCIe device.
  returned: when external ID is provided
  type: str
  sample: "17081fa3-3e5c-58d2-aca5-b1312414d8d9"

total_available_results:
  description: The total number of available PCIe devices in PC.
  returned: when all PCIe devices are fetched
  type: int
  sample: 4

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching PCIe devices info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  returned: when an error occurs
  type: str

failed:
  description: This field typically holds information about if the task have failed.
  returned: when something fails
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_pcie_devices_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_pcie_device_using_ext_id(module, pcie_devices, result):
    ext_id = module.params.get("ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating PCIe devices info spec", **result)

    kwargs["_filter"] = "extId eq '{0}'".format(ext_id)

    try:
        resp = pcie_devices.list_pcie_devices(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching PCIe device info using ext_id",
        )

    result["ext_id"] = ext_id
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        result["response"] = {}
        result["msg"] = "PCIe device with ext_id '{0}' not found".format(ext_id)
        return
    result["response"] = resp[0]


def get_pcie_devices(module, pcie_devices, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating PCIe devices info spec", **result)

    try:
        resp = pcie_devices.list_pcie_devices(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching PCIe devices info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

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
    result = {"changed": False, "response": None, "failed": False}
    pcie_devices = get_pcie_devices_api_instance(module)
    if module.params.get("ext_id"):
        get_pcie_device_using_ext_id(module, pcie_devices, result)
    else:
        get_pcie_devices(module, pcie_devices, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
