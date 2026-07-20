#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_disk_stats_info_v2
short_description: Fetch info (stats) about a Nutanix ESXi VM disk from Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about DiskStat in Nutanix Prism Central.
  - If C(ext_id) (the VM disk external ID) is provided, fetch stats for the specific
    ESXi VM disk identified by C(vm_ext_id) + C(ext_id).
  - This entity has no list API in the v4 VMM ESXi stats SDK (there is no C(ListDiskStats)),
    so both C(vm_ext_id) and C(ext_id) are required and the module always returns a single
    C(DiskStat) result.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get Stats for an ESXi VM Disk) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, Virtual Machine Admin, Virtual Machine Viewer.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  vm_ext_id:
    description:
      - The external ID of the VM that owns the disk whose stats are to be fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the VM disk whose stats are to be fetched.
    type: str
    required: true
  start_time:
    description:
      - Start time of the reporting window in extended ISO-8601 format
        (e.g. C(2024-07-31T12:41:56.955Z)).
    type: str
    required: true
  end_time:
    description:
      - End time of the reporting window in extended ISO-8601 format
        (e.g. C(2025-07-31T12:41:56.955Z)).
    type: str
    required: true
  sampling_interval:
    description:
      - Sampling interval in seconds at which statistical data should be collected.
    type: int
    required: false
  stat_type:
    description:
      - Aggregation type applied to each stat over C(sampling_interval).
    type: str
    required: false
    choices:
      - SUM
      - AVG
      - MIN
      - MAX
      - COUNT
      - LAST
  select:
    description:
      - OData C($select) expression that limits the response to a specific set of stat fields.
    type: str
    required: false
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch ESXi VM disk stats using ext_id
  nutanix.ncp.ntnx_vm_disk_stats_info_v2:
    vm_ext_id: "cf1b8f42-8f36-4b3a-9db7-9c1c8f3c8be1"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
  register: disk_stats

- name: Fetch ESXi VM disk stats with all optional parameters
  nutanix.ncp.ntnx_vm_disk_stats_info_v2:
    vm_ext_id: "cf1b8f42-8f36-4b3a-9db7-9c1c8f3c8be1"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
    sampling_interval: 30
    stat_type: "AVG"
    select: "*"
  register: disk_stats_full
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC DiskStat info v4 API.
    - Always a single DiskStat entity because the underlying SDK does not
      expose a C(ListDiskStats) operation - external IDs must always be
      provided.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "vm_ext_id": "cf1b8f42-8f36-4b3a-9db7-9c1c8f3c8be1",
      "links": null,
      "tenant_id": null,
      "stats": [
        {
          "timestamp": "2024-07-31T12:41:00+00:00",
          "controller_num_iops": 12,
          "controller_num_read_iops": 8,
          "controller_num_write_iops": 4,
          "controller_avg_io_latency_micros": 947,
          "controller_avg_read_io_latency_micros": 797,
          "controller_avg_write_io_latency_micros": 2175,
          "controller_io_bandwidth_kbps": 53450,
          "controller_read_io_bandwidth_kbps": 52171,
          "controller_write_io_bandwidth_kbps": 1278,
          "controller_total_io_size_kb": 640,
          "controller_total_read_io_size_kb": 512,
          "controller_num_io": 12,
          "controller_num_read_io": 8,
          "controller_num_write_io": 4,
          "controller_num_seq_io": 6,
          "controller_random_io_ppm": 500000,
          "controller_read_io_ppm": 666666,
          "controller_write_io_ppm": 333333,
          "controller_seq_io_ppm": 500000,
          "controller_avg_read_io_size_kb": 64,
          "controller_avg_write_io_size_kb": 32,
          "controller_total_io_time_micros": 11364,
          "controller_total_read_io_time_micros": 6376,
          "controller_timespan_micros": 30000000,
          "controller_user_bytes": 655360
        }
      ]
    }
ext_id:
  description: External ID of the VM disk whose stats were fetched.
  returned: when external ID is provided
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
vm_ext_id:
  description: External ID of the VM that owns the disk.
  returned: when VM external ID is provided
  type: str
  sample: "cf1b8f42-8f36-4b3a-9db7-9c1c8f3c8be1"
changed:
  description: Always false for info modules.
  returned: always
  type: bool
  sample: false
failed:
  description: Whether the fetch failed.
  returned: always
  type: bool
  sample: false
error:
  description: Error details, when an error occurs.
  returned: when an error occurs
  type: str
msg:
  description: Human-readable status/error message.
  returned: when there is an error or the API returns an empty response
  type: str
  sample: "Api Exception raised while fetching ESXi VM disk stats info"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import get_esxi_stats_api_instance  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        start_time=dict(type="str", required=True),
        end_time=dict(type="str", required=True),
        sampling_interval=dict(type="int", required=False),
        stat_type=dict(
            type="str",
            required=False,
            choices=["SUM", "AVG", "MIN", "MAX", "COUNT", "LAST"],
        ),
        select=dict(type="str", required=False),
    )
    return module_args


def get_vm_disk_stats_using_ext_id(module, api_instance, result):
    """Fetch stats for a single VM disk via GetDiskStatsById."""
    validate_required_params(module, ["vm_ext_id", "ext_id", "start_time", "end_time"])

    vm_ext_id = module.params.get("vm_ext_id")
    ext_id = module.params.get("ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    query, _err = sg.get_stats_spec()
    select = module.params.get("select")
    if select is not None:
        query["_select"] = select

    resp = None
    try:
        resp = api_instance.get_disk_stats_by_id(
            vmExtId=vm_ext_id,
            extId=ext_id,
            **query,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching ESXi VM disk stats info for "
                "vm_ext_id={0} ext_id={1}".format(vm_ext_id, ext_id)
            ),
        )

    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        module.fail_json(
            msg=(
                "Empty response fetching ESXi VM disk stats info for "
                "vm_ext_id={0} ext_id={1}".format(vm_ext_id, ext_id)
            ),
            **result,
        )


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)

    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "ext_id": None,
        "vm_ext_id": None,
        "error": None,
    }
    api_instance = get_esxi_stats_api_instance(module)
    get_vm_disk_stats_using_ext_id(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
