#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_pcie_devices_info_v2
short_description: Fetch PCIe devices info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about PcieDevice in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific PcieDevice.
  - If C(ext_id) is not provided, list multiple PcieDevice optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get PCIe device by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, Virtual Machine Admin,
      Virtual Machine Operator, Virtual Machine Viewer, VPC Admin (requires View_Pcie_Device permission).
    - >-
      B(List PCIe devices) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, Virtual Machine Admin,
      Virtual Machine Operator, Virtual Machine Viewer, VPC Admin (requires View_Pcie_Device permission).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the PCIe device.
      - When provided, only the matching PCIe device is returned.
      - The v4.2 SDK does not expose a dedicated get-by-id endpoint; the module
        emulates that by listing PCIe devices with an OData
        C($filter=extId eq '<ext_id>') expression and returning the single
        matching entity.
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
- name: Get a specific PCIe device using ext_id
  nutanix.ncp.ntnx_pcie_devices_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all PCIe devices
  nutanix.ncp.ntnx_pcie_devices_info_v2:
  register: result
  ignore_errors: true

- name: List PCIe devices filtered by cluster ext_id
  nutanix.ncp.ntnx_pcie_devices_info_v2:
    filter: "clusterExtId eq '0005a9f0-6f13-4a5f-0000-000000019cd8'"
  register: result
  ignore_errors: true

- name: List first PCIe device only using limit
  nutanix.ncp.ntnx_pcie_devices_info_v2:
    limit: 1
  register: result
  ignore_errors: true

- name: List PCIe devices with pagination
  nutanix.ncp.ntnx_pcie_devices_info_v2:
    page: 0
    limit: 10
  register: result
  ignore_errors: true

- name: List PCIe devices selecting only a subset of fields
  nutanix.ncp.ntnx_pcie_devices_info_v2:
    select: "extId,clusterExtId,hostExtId,type,state"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC PcieDevice info v4 API.
    - It can be a single PcieDevice if external ID is provided.
    - List of multiple PcieDevice if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "configuration": {
          "class_id": 2,
          "device_id": 4347,
          "prog_i_face": 0,
          "sub_class_id": 0,
          "sub_system_id": 12,
          "sub_system_vendor_id": 32902,
          "vendor_id": 32902
      },
      "description": "Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (Ethernet Server Adapter X520-2)",
      "ext_id": "348d4ecb-9ec9-55e6-ad06-5ec88eee87c0",
      "host_ext_id": "adf0c9e0-4051-4cd2-9f6f-ca9f962e941b",
      "links": null,
      "owner_vm_ext_id": null,
      "state": "HOST_USED",
      "tenant_id": null,
      "type": "NETWORK_CONTROLLER"
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching PCIe devices info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the PCIe device.
  type: str
  returned: When external ID is provided
  sample: "348d4ecb-9ec9-55e6-ad06-5ec88eee87c0"

total_available_results:
  description: The total number of available PCIe devices in PC.
  type: int
  returned: When all PCIe devices are fetched
  sample: 4
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_pcie_devices_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_pcie_device  # noqa: E402
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


def get_pcie_device_using_ext_id(module, api_instance, result):
    """Fetch a single PCIe device using its external ID.

    The v4.2 SDK does not expose a dedicated get-by-id endpoint for PCIe
    devices, so this helper emulates that by calling the list API with an
    OData ``$filter`` on ``extId``. When no PCIe device matches the given
    ``ext_id``, the module fails with a descriptive error so the caller
    knows the device does not exist on the cluster.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_pcie_device(module, api_instance, ext_id)
    if resp is None:
        module.fail_json(
            msg="PCIe device with ext_id '{0}' not found on the cluster.".format(
                ext_id
            ),
            **result,
        )
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_pcie_devices(module, api_instance, result):
    """Fetch the paginated / filtered list of PCIe devices from Prism Central."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating PCIe devices info spec", **result)

    try:
        resp = api_instance.list_pcie_devices(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching PCIe devices info",
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
    result = {"changed": False, "response": None, "ext_id": None, "failed": False}
    api_instance = get_pcie_devices_api_instance(module)
    if module.params.get("ext_id"):
        get_pcie_device_using_ext_id(module, api_instance, result)
    else:
        get_pcie_devices(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
