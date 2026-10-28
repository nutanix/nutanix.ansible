#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vm_disk_stats_info_v2
short_description: Fetch stats for a single ESXi VM disk
version_added: "2.7.0"
description:
    - Fetch statistics for a disk attached to an ESXi Virtual Machine in Nutanix
      Prism Central.
    - Only ESXi Virtual Machines are supported. A vCenter instance must be
      registered with the cluster; the endpoints fail for AHV VMs.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Get the stats for the specified VM disk) -
      Required Roles: Backup Admin, Prism Admin, Prism Viewer, Project Manager,
      Self-Service Admin (deprecated), Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    vm_ext_id:
        description:
            - The VM external ID when retrieving the stats for a given VM disk.
        type: str
        required: true
    ext_id:
        description:
            - The external ID of the VM disk when retrieving stats for a given
              VM disk.
        type: str
        required: true
    start_time:
        description:
            - The start time of the period for which stats should be reported.
            - The value should be in extended ISO-8601 format.
            - >-
              For example, start time of C(2022-04-23T01:23:45.678+09:00) would
              consider all stats starting at 1:23:45.678 on the 23rd of April
              2022.
        type: str
        required: true
    end_time:
        description:
            - The end time of the period for which stats should be reported.
            - The value should be in extended ISO-8601 format.
            - >-
              For example, end time of C(2022-04-23T13:23:45.678+09:00) would
              consider all stats till 13:23:45.678 on the 23rd of April 2022.
        type: str
        required: true
    sampling_interval:
        description:
            - The sampling interval in seconds at which statistical data should
              be collected.
            - For example, if you want performance statistics every 30 seconds,
              then provide the value as 30.
        type: int
        required: false
    stat_type:
        description:
            - The operator to use while performing down-sampling on stats data.
            - Allowed values are SUM, MIN, MAX, AVG, COUNT and LAST.
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
            - A URL query parameter that allows clients to request a specific
              set of properties for each entity or complex type.
            - Expression specified with the C($select) must conform to the
              OData V4.01 URL conventions.
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
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch ESXi VM disk stats
  nutanix.ncp.ntnx_vm_disk_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    ext_id: "6f7d5cf6-2e42-4b71-9e73-6a4d1e5a9b1c"
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
  register: vm_disk_stats

- name: Fetch ESXi VM disk stats with sampling and aggregation
  nutanix.ncp.ntnx_vm_disk_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    ext_id: "6f7d5cf6-2e42-4b71-9e73-6a4d1e5a9b1c"
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    sampling_interval: 30
    stat_type: AVG
    select: "stats/controllerNumIops,stats/controllerAvgIoLatencyMicros"
  register: vm_disk_stats_avg
"""

RETURN = r"""
response:
    description: The disk stats payload returned by the API.
    returned: always
    type: dict
    sample:
        {
            "ext_id": "6f7d5cf6-2e42-4b71-9e73-6a4d1e5a9b1c",
            "vm_ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
            "links": null,
            "tenant_id": null,
            "stats": [
                {
                    "timestamp": "2026-07-21T00:00:00+00:00",
                    "controller_num_iops": 100,
                    "controller_avg_io_latency_micros": 950
                }
            ]
        }
ext_id:
    description: The external ID of the ESXi VM disk.
    type: str
    returned: always
    sample: "6f7d5cf6-2e42-4b71-9e73-6a4d1e5a9b1c"
vm_ext_id:
    description: The external ID of the parent ESXi Virtual Machine.
    type: str
    returned: always
    sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error
    sample: "Api Exception raised while fetching ESXi VM disk stats using ext_id"
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402
from ..module_utils.v4.vmm.api_client import get_esxi_stats_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_esxi_vm_disk_stats  # noqa: E402

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
            choices=["SUM", "MIN", "MAX", "AVG", "COUNT", "LAST"],
        ),
        select=dict(type="str", required=False),
    )
    return module_args


def get_vm_disk_stat(module, api_instance, result):
    vm_ext_id = module.params.get("vm_ext_id")
    ext_id = module.params.get("ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id
    resp = get_esxi_vm_disk_stats(
        module,
        api_instance,
        vm_ext_id=vm_ext_id,
        ext_id=ext_id,
        start_time=module.params.get("start_time"),
        end_time=module.params.get("end_time"),
        sampling_interval=module.params.get("sampling_interval"),
        stat_type=module.params.get("stat_type"),
        select=module.params.get("select"),
    )
    if resp is None or getattr(resp, "data", None) is None:
        module.fail_json(msg="Failed fetching ESXi VM disk stats", **result)
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }

    api_instance = get_esxi_stats_api_instance(module)
    get_vm_disk_stat(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
