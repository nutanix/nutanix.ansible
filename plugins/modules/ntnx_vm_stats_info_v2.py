#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_stats_info_v2
short_description: Fetch ESXi VM stats info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ESXi VM stats in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch stats of the specific ESXi VM.
  - If C(ext_id) is provided along with C(disk_ext_id), fetch stats for the specified VM disk.
  - If C(ext_id) is provided along with C(nic_ext_id), fetch stats for the specified VM NIC.
  - If C(ext_id) is not provided, list stats for multiple ESXi VMs optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
options:
  ext_id:
    description:
      - The external ID of the ESXi VM whose stats are being retrieved.
      - When omitted the module lists stats for all ESXi VMs.
    type: str
  disk_ext_id:
    description:
      - The external ID of the VM disk when retrieving stats for a specific disk.
      - Requires C(ext_id) to be set (the parent VM external ID).
      - Mutually exclusive with C(nic_ext_id).
    type: str
  nic_ext_id:
    description:
      - The external ID of the VM NIC when retrieving stats for a specific NIC.
      - Requires C(ext_id) to be set (the parent VM external ID).
      - Mutually exclusive with C(disk_ext_id).
    type: str
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value must be in extended ISO-8601 format (e.g. C(2024-07-31T12:41:56.955Z)).
      - Required for every stats fetch operation.
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value must be in extended ISO-8601 format (e.g. C(2025-07-31T12:41:56.955Z)).
      - Required for every stats fetch operation.
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval (in seconds) at which statistical data should be collected.
      - For example, C(30) will bucket stats into 30 second windows.
    type: int
    required: false
  stat_type:
    description:
      - The down-sampling operator to use when aggregating stats within each C(sampling_interval).
    type: str
    required: false
    choices:
      - SUM
      - AVG
      - MIN
      - MAX
      - COUNT
      - LAST
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing
    the operation.
  - >-
    B(List ESXi VM stats / Get ESXi VM stats by ext_id) -
    Required Permission: View_ESXi_Virtual_Machine_Stats
  - >-
    B(Get ESXi VM disk stats by ext_id) -
    Required Permission: View_ESXi_Virtual_Machine_Disk_Stats
  - >-
    B(Get ESXi VM NIC stats by ext_id) -
    Required Permission: View_ESXi_Virtual_Machine_NIC_Stats
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
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
- name: List ESXi VM stats for all VMs during a time window
  nutanix.ncp.ntnx_vm_stats_info_v2:
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
  register: result

- name: List ESXi VM stats with sampling interval and stat type
  nutanix.ncp.ntnx_vm_stats_info_v2:
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
    sampling_interval: 30
    stat_type: AVG
    limit: 5
  register: result

- name: Fetch ESXi VM stats for a specific VM
  nutanix.ncp.ntnx_vm_stats_info_v2:
    ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
    sampling_interval: 30
    stat_type: SUM
  register: result

- name: Fetch ESXi VM disk stats for a specific VM disk
  nutanix.ncp.ntnx_vm_stats_info_v2:
    ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
    disk_ext_id: "839feff9-bac0-4a70-9523-82ea9e431517"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
    sampling_interval: 30
    stat_type: AVG
  register: result

- name: Fetch ESXi VM NIC stats for a specific VM NIC
  nutanix.ncp.ntnx_vm_stats_info_v2:
    ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
    nic_ext_id: "1eb11972-dce6-40b9-8d1f-b878ef8410be"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
    sampling_interval: 30
    stat_type: LAST
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ESXi VM stats v4 API.
    - It can be stats for a single ESXi VM, a single VM disk, or a single VM NIC
      when external IDs are supplied.
    - When only C(ext_id) is provided it returns the stats for the specified VM.
    - When neither C(ext_id) nor child IDs are provided it returns a list of ESXi
      VM stats optionally filtered / paginated.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "522670d7-e92d-45c5-9139-76ccff6813c2",
      "links": null,
      "tenant_id": null,
      "stats": {
        "hypervisor_cpu_usage_ppm": [
          {"timestamp": "2024-07-31T11:29:00+00:00", "value": 32100},
          {"timestamp": "2024-07-31T11:28:30+00:00", "value": 31980}
        ],
        "memory_usage_ppm": [
          {"timestamp": "2024-07-31T11:29:00+00:00", "value": 452330},
          {"timestamp": "2024-07-31T11:28:30+00:00", "value": 451102}
        ],
        "controller_num_iops": [
          {"timestamp": "2024-07-31T11:29:00+00:00", "value": 12},
          {"timestamp": "2024-07-31T11:28:30+00:00", "value": 11}
        ]
      }
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message emitted by the module.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching ESXi VM stats"

error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - The external ID of the entity whose stats were fetched.
    - For a VM stats fetch this is the VM external ID.
    - For a disk / NIC stats fetch this is the disk / NIC external ID.
  type: str
  returned: when external ID is provided
  sample: "522670d7-e92d-45c5-9139-76ccff6813c2"

vm_ext_id:
  description: External ID of the parent VM for disk / NIC stats fetch.
  type: str
  returned: when C(disk_ext_id) or C(nic_ext_id) is provided
  sample: "522670d7-e92d-45c5-9139-76ccff6813c2"

total_available_results:
  description: The total number of available ESXi VM stats records in PC.
  type: int
  returned: when listing ESXi VM stats
  sample: 12
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_esxi_stats_api_instance  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        disk_ext_id=dict(type="str"),
        nic_ext_id=dict(type="str"),
        start_time=dict(type="str", required=True),
        end_time=dict(type="str", required=True),
        sampling_interval=dict(type="int"),
        stat_type=dict(
            type="str",
            choices=[
                "SUM",
                "AVG",
                "MIN",
                "MAX",
                "COUNT",
                "LAST",
            ],
        ),
    )

    return module_args


def _build_stats_query(module):
    """Build the shared stats query dict (start/end/interval/type/select)."""
    query = {
        "_startTime": module.params.get("start_time"),
        "_endTime": module.params.get("end_time"),
    }
    sampling_interval = module.params.get("sampling_interval")
    if sampling_interval is not None:
        query["_samplingInterval"] = sampling_interval
    stat_type = module.params.get("stat_type")
    if stat_type is not None:
        query["_statType"] = stat_type
    select = module.params.get("select")
    if select is not None:
        query["_select"] = select
    return query


def get_vm_disk_stats(module, api_instance, result):
    vm_ext_id = module.params.get("ext_id")
    disk_ext_id = module.params.get("disk_ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = disk_ext_id
    query = _build_stats_query(module)
    try:
        resp = api_instance.get_disk_stats_by_id(
            vmExtId=vm_ext_id, extId=disk_ext_id, **query
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ESXi VM disk stats",
        )
    if getattr(resp, "data", None) is None:
        module.fail_json(msg="Failed fetching ESXi VM disk stats", **result)
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_vm_nic_stats(module, api_instance, result):
    vm_ext_id = module.params.get("ext_id")
    nic_ext_id = module.params.get("nic_ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = nic_ext_id
    query = _build_stats_query(module)
    try:
        resp = api_instance.get_nic_stats_by_id(
            vmExtId=vm_ext_id, extId=nic_ext_id, **query
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ESXi VM NIC stats",
        )
    if getattr(resp, "data", None) is None:
        module.fail_json(msg="Failed fetching ESXi VM NIC stats", **result)
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_vm_stats_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    query = _build_stats_query(module)
    try:
        resp = api_instance.get_vm_stats_by_id(extId=ext_id, **query)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ESXi VM stats",
        )
    if getattr(resp, "data", None) is None:
        module.fail_json(msg="Failed fetching ESXi VM stats", **result)
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def list_vm_stats(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating ESXi VM stats info spec", **result)

    kwargs.update(_build_stats_query(module))

    try:
        resp = api_instance.list_vm_stats(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing ESXi VM stats",
        )

    total_available_results = getattr(
        getattr(resp, "metadata", None), "total_available_results", None
    )
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
            ("disk_ext_id", "nic_ext_id"),
            ("filter", "ext_id"),
        ],
        required_by={
            "disk_ext_id": ("ext_id",),
            "nic_ext_id": ("ext_id",),
        },
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_esxi_stats_api_instance(module)
    if module.params.get("disk_ext_id"):
        get_vm_disk_stats(module, api_instance, result)
    elif module.params.get("nic_ext_id"):
        get_vm_nic_stats(module, api_instance, result)
    elif module.params.get("ext_id"):
        get_vm_stats_by_ext_id(module, api_instance, result)
    else:
        list_vm_stats(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
