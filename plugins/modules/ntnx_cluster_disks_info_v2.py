#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_disks_info_v2
short_description: Fetch Disk info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about Disk in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Disk.
  - If C(ext_id) is not provided, list multiple Disk optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get Disk by ext_id) -
    Required Roles: Cluster Admin, Consumer, Developer, Operator, Prism Admin,
    Prism Viewer, Super Admin
  - >-
    B(List Disks) -
    Required Roles: Cluster Admin, Consumer, Developer, Operator, Prism Admin,
    Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the Disk.
      - If provided, fetch details of the specific Disk.
      - If not provided, list all Disks (with optional filter / limit / order).
    type: str
    required: false
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
- name: Get Disk using ext_id
  nutanix.ncp.ntnx_cluster_disks_info_v2:
    ext_id: "62cd8f7a-9f0f-4a26-b1ab-2f0a72c48d0e"
  register: result
  ignore_errors: true

- name: List all Disks in Prism Central
  nutanix.ncp.ntnx_cluster_disks_info_v2:
  register: result
  ignore_errors: true

- name: List Disks with filter on storage tier
  nutanix.ncp.ntnx_cluster_disks_info_v2:
    filter: "storageTier eq Clustermgmt.Config.StorageTier'SSD_SATA'"
  register: result
  ignore_errors: true

- name: List first 2 Disks ordered by mountPath
  nutanix.ncp.ntnx_cluster_disks_info_v2:
    limit: 2
    orderby: "mountPath asc"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Disk info v4 API.
    - It can be a single Disk if external ID is provided.
    - List of multiple Disk if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_id": "000653ea-e2f2-ee30-0000-000000019bcd",
      "cluster_name": "auto_cluster_prod_f6b78dc0aa70",
      "cvm_ip_address": {
        "ipv4": {"prefix_length": 32, "value": "10.46.137.52"},
        "ipv6": null
      },
      "disk_advance_config": {
        "has_boot_partitions_only": false,
        "is_boot_disk": true,
        "is_data_migrated": false,
        "is_diagnostic_info_available": false,
        "is_error_found_in_log": false,
        "is_marked_for_removal": false,
        "is_mounted": true,
        "is_online": true,
        "is_password_protected": null,
        "is_planned_outage": false,
        "is_self_encrypting_drive": false,
        "is_self_managed_nvme": false,
        "is_spdk_managed": false,
        "is_suspected_unhealthy": false,
        "is_under_diagnosis": false,
        "is_unhealthy": false
      },
      "disk_size_bytes": 621396250716,
      "ext_id": "9f08041d-f8d1-4f44-bf7f-2afb036628ae",
      "firmware_version": "304Q",
      "host_name": "Beerus-4",
      "links": [
        {
          "href": "https://10.44.76.28:9440/api/clustermgmt/v4.2/config/disks/9f08041d-f8d1-4f44-bf7f-2afb036628ae",
          "rel": "disk"
        }
      ],
      "location": 1,
      "model": "SAMSUNG MZ7KM960HMJP-00005",
      "mount_path": "/home/nutanix/data/stargate-storage/disks/S3F3NX0KB08851",
      "node_ext_id": "4ef8c07f-ec03-40dc-b277-e81c306899b0",
      "node_ip_address": {
        "ipv4": {"prefix_length": 32, "value": "10.46.137.48"},
        "ipv6": null
      },
      "nvme_pcie_path": null,
      "physical_capacity_bytes": 960197124096,
      "serial_number": "S3F3NX0KB08851",
      "service_vm_id": "000653ea-e2f2-ee30-0000-000000019bcd::3",
      "status": "NORMAL",
      "storage_pool_ext_id": "c5c0459e-a94f-4d32-8caf-363a58422905",
      "storage_tier": "SSD_SATA",
      "target_firmware_version": "304Q",
      "tenant_id": null,
      "vendor": "Not Available"
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
  sample: "Api Exception raised while fetching Disks info"

error:
  description: The error message if an error occurs.
  type: str
  returned: When an error occurs

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the Disk (when requested via C(ext_id)).
  type: str
  returned: When external ID is provided
  sample: "9f08041d-f8d1-4f44-bf7f-2afb036628ae"

total_available_results:
  description: The total number of available Disks in PC.
  type: int
  returned: When all Disks are fetched
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_disks_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_disk  # noqa: E402
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


def get_disk_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_disk(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_disks(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Disks info spec", **result)

    try:
        resp = api_instance.list_disks(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Disks info",
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
    result = {"changed": False, "error": None, "response": None, "failed": False}
    api_instance = get_disks_api_instance(module)
    if module.params.get("ext_id"):
        get_disk_using_ext_id(module, api_instance, result)
    else:
        get_disks(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
