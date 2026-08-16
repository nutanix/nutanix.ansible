#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_stat_v2
short_description: Fetch stats for a single ESXi Virtual Machine, its disk or its NIC in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module fetches statistics for a single ESXi Virtual Machine, or for a
    disk / NIC attached to that VM, from the Nutanix Prism Central v4 VMM API.
  - If only C(ext_id) is provided, VM-level stats are fetched
    (C(get_vm_stats_by_id)).
  - If C(disk_ext_id) is also provided, disk stats are fetched
    (C(get_disk_stats_by_id)).
  - If C(nic_ext_id) is also provided, NIC stats are fetched
    (C(get_nic_stats_by_id)).
  - C(disk_ext_id) and C(nic_ext_id) are mutually exclusive.
  - Only ESXi Virtual Machines are supported by this API. A vCenter instance
    must be registered with the cluster; the corresponding endpoints will
    fail for VMs hosted on AHV.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Get ESXi VM Stats / Disk Stats / NIC Stats) -
      Required Roles: Prism Admin, Prism Viewer, Project Manager,
      Self-Service Admin (deprecated), Super Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - External ID of the ESXi Virtual Machine whose stats should be
        retrieved.
      - Required for all three operations.
    type: str
    required: true
  disk_ext_id:
    description:
      - External ID of the ESXi VM disk to retrieve stats for.
      - When set, the module fetches disk-level stats instead of VM-level
        stats.
      - Mutually exclusive with C(nic_ext_id).
    type: str
    required: false
  nic_ext_id:
    description:
      - External ID of the ESXi VM NIC to retrieve stats for.
      - When set, the module fetches NIC-level stats instead of VM-level
        stats.
      - Mutually exclusive with C(disk_ext_id).
    type: str
    required: false
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format, for example
        C(2026-07-21T00:00:00.000Z).
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format, for example
        C(2026-07-21T01:00:00.000Z).
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval, in seconds, at which statistical data should
        be collected. For example, C(30) requests one sample every 30
        seconds.
    type: int
    required: false
  stat_type:
    description:
      - The down-sampling / aggregation operator to apply while returning
        stats.
    type: str
    required: false
    choices:
      - SUM
      - MIN
      - MAX
      - AVG
      - COUNT
      - LAST
  select:
    description:
      - A URL C($select) query parameter that allows clients to request a
        specific set of properties for each entity or complex type.
      - Expression must conform to the OData V4.01 URL conventions.
    type: str
    required: false
  read_timeout:
    description:
      - Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch ESXi VM stats using ext_id
  nutanix.ncp.ntnx_vm_stat_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
  register: vm_stats

- name: Fetch ESXi VM stats with sampling and aggregation
  nutanix.ncp.ntnx_vm_stat_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    sampling_interval: 30
    stat_type: AVG
    select: "stats/hypervisorCpuUsagePpm,stats/hypervisorMemoryUsagePpm"
  register: vm_stats_avg

- name: Fetch ESXi VM disk stats
  nutanix.ncp.ntnx_vm_stat_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    disk_ext_id: "6f7d5cf6-2e42-4b71-9e73-6a4d1e5a9b1c"
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    sampling_interval: 30
    stat_type: AVG
  register: vm_disk_stats

- name: Fetch ESXi VM NIC stats
  nutanix.ncp.ntnx_vm_stat_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    nic_ext_id: "a1c8fce7-1c1e-4c1c-9e19-11cbeeb2f0b1"
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    sampling_interval: 30
    stat_type: SUM
  register: vm_nic_stats
"""

RETURN = r"""
response:
  description:
    - The stats payload returned by the Nutanix PC VmStat v4 API.
    - When C(disk_ext_id) or C(nic_ext_id) is not provided this contains the
      VM-level stats, indexed by C(stats).
    - When C(disk_ext_id) is provided this contains disk-level stats, also
      carrying the C(vm_ext_id) of the parent VM.
    - When C(nic_ext_id) is provided this contains NIC-level stats, also
      carrying the C(vm_ext_id) of the parent VM.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "links": null,
      "tenant_id": null,
      "stats": [
        {
          "timestamp": "2026-07-21T00:00:00+00:00",
          "hypervisor_cpu_usage_ppm": 12345,
          "hypervisor_memory_usage_ppm": 67890,
          "controller_num_iops": 100,
          "controller_avg_io_latency_micros": 950
        }
      ]
    }

ext_id:
  description:
    - External ID of the ESXi Virtual Machine.
  returned: always
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

vm_ext_id:
  description:
    - External ID of the parent ESXi Virtual Machine when disk or NIC stats
      are fetched. It matches C(ext_id) in that case.
  returned: when C(disk_ext_id) or C(nic_ext_id) is provided
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

changed:
  description: This indicates whether the task resulted in any changes. Info
    modules never make changes.
  returned: always
  type: bool
  sample: false

msg:
  description: Status/error message emitted by the module.
  returned: When there is an error or the module has an informative status.
  type: str
  sample: "Api Exception raised while fetching ESXi VM stats using ext_id"

error:
  description: The error message if an error occurred.
  type: str
  returned: When an error occurs

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import get_esxi_stats_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import (  # noqa: E402
    get_esxi_vm_disk_stats,
    get_esxi_vm_nic_stats,
    get_esxi_vm_stats,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
        disk_ext_id=dict(type="str", required=False),
        nic_ext_id=dict(type="str", required=False),
        start_time=dict(type="str", required=True),
        end_time=dict(type="str", required=True),
        sampling_interval=dict(type="int", required=False),
        stat_type=dict(
            type="str",
            required=False,
            choices=["SUM", "MIN", "MAX", "AVG", "COUNT", "LAST"],
        ),
        select=dict(type="str", required=False),
    )

    return module_args


def _serialize(resp):
    """Serialize an SDK response, returning the ``data`` block only."""
    if resp is None or getattr(resp, "data", None) is None:
        return None
    return strip_internal_attributes(resp.to_dict()).get("data")


def get_vm_stat(module, api_instance, result):
    """Fetch VM-level stats via get_vm_stats_by_id."""
    ext_id = module.params.get("ext_id")
    resp = get_esxi_vm_stats(
        module,
        api_instance,
        ext_id=ext_id,
        start_time=module.params.get("start_time"),
        end_time=module.params.get("end_time"),
        sampling_interval=module.params.get("sampling_interval"),
        stat_type=module.params.get("stat_type"),
        select=module.params.get("select"),
    )
    data = _serialize(resp)
    if data is None:
        module.fail_json(msg="Failed fetching ESXi VM stats", **result)
    result["response"] = data


def get_vm_disk_stat(module, api_instance, result):
    """Fetch VM disk stats via get_disk_stats_by_id."""
    ext_id = module.params.get("ext_id")
    disk_ext_id = module.params.get("disk_ext_id")
    result["vm_ext_id"] = ext_id
    resp = get_esxi_vm_disk_stats(
        module,
        api_instance,
        vm_ext_id=ext_id,
        ext_id=disk_ext_id,
        start_time=module.params.get("start_time"),
        end_time=module.params.get("end_time"),
        sampling_interval=module.params.get("sampling_interval"),
        stat_type=module.params.get("stat_type"),
        select=module.params.get("select"),
    )
    data = _serialize(resp)
    if data is None:
        module.fail_json(msg="Failed fetching ESXi VM disk stats", **result)
    result["ext_id"] = disk_ext_id
    result["response"] = data


def get_vm_nic_stat(module, api_instance, result):
    """Fetch VM NIC stats via get_nic_stats_by_id."""
    ext_id = module.params.get("ext_id")
    nic_ext_id = module.params.get("nic_ext_id")
    result["vm_ext_id"] = ext_id
    resp = get_esxi_vm_nic_stats(
        module,
        api_instance,
        vm_ext_id=ext_id,
        ext_id=nic_ext_id,
        start_time=module.params.get("start_time"),
        end_time=module.params.get("end_time"),
        sampling_interval=module.params.get("sampling_interval"),
        stat_type=module.params.get("stat_type"),
        select=module.params.get("select"),
    )
    data = _serialize(resp)
    if data is None:
        module.fail_json(msg="Failed fetching ESXi VM NIC stats", **result)
    result["ext_id"] = nic_ext_id
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
        mutually_exclusive=[("disk_ext_id", "nic_ext_id")],
    )

    remove_param_with_none_value(module.params)
    validate_required_params(module, ["ext_id", "start_time", "end_time"])

    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": module.params.get("ext_id"),
        "failed": False,
    }

    api_instance = get_esxi_stats_api_instance(module)

    if module.params.get("disk_ext_id"):
        get_vm_disk_stat(module, api_instance, result)
    elif module.params.get("nic_ext_id"):
        get_vm_nic_stat(module, api_instance, result)
    else:
        get_vm_stat(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
