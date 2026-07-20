#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_disk_stat_v2
short_description: Fetch disk stats from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch performance statistics for a physical disk in a Nutanix cluster.
  - The stats are returned as time-series values covering the requested time window.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get Stats for a Disk) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external identifier of the disk whose stats should be fetched.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - Example input C(2024-07-31T12:41:56.955Z).
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - Example input C(2025-07-31T12:41:56.955Z).
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval in seconds at which statistical data should be collected.
      - For example, if you want performance statistics every 30 seconds, then provide the value as 30.
    type: int
    required: false
  stat_type:
    description:
      - The type of down-sampling operator to apply to the stats data.
      - See Nutanix SDK C(DownSamplingOperator) enum for details.
    type: str
    required: false
    choices:
      - SUM
      - MIN
      - MAX
      - AVG
      - COUNT
      - LAST
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
- name: Fetch disk stats during time interval
  nutanix.ncp.ntnx_disk_stat_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6f0a0f0b-4b39-4d05-89be-fefdaea6a3c1"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
  register: result

- name: Fetch disk stats with all attributes
  nutanix.ncp.ntnx_disk_stat_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6f0a0f0b-4b39-4d05-89be-fefdaea6a3c1"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
    sampling_interval: 30
    stat_type: "AVG"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC DiskStat get-stats v4 API.
    - Contains time-series values for the requested disk metrics.
  returned: always
  type: dict
  sample:
    {
      "disk_avg_io_latency_microsec": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 369},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 506}
      ],
      "disk_base_io_bandwidthkbps": null,
      "disk_base_io_latency_microsec": null,
      "disk_base_num_iops": null,
      "disk_base_read_io_avg_latency_microsec": null,
      "disk_base_read_io_bandwidthkbps": null,
      "disk_base_read_iops": null,
      "disk_base_write_io_avg_latency_microsec": null,
      "disk_base_write_io_bandwidthkbps": null,
      "disk_base_write_iops": null,
      "disk_capacity_bytes": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 604114121598},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 604114121598}
      ],
      "disk_free_bytes": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 152043597477},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 152062940837}
      ],
      "disk_io_bandwidthkbps": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 1224},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 1202}
      ],
      "disk_num_iops": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 21},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 17}
      ],
      "disk_peak_io_bandwidthkbps": null,
      "disk_peak_io_latency_microsec": null,
      "disk_peak_num_iops": null,
      "disk_peak_read_io_avg_latency_microsec": null,
      "disk_peak_read_io_bandwidthkbps": null,
      "disk_peak_read_iops": null,
      "disk_peak_write_io_avg_latency_microsec": null,
      "disk_peak_write_io_bandwidthkbps": null,
      "disk_peak_write_iops": null,
      "disk_read_io_avg_latency_microsec": null,
      "disk_read_io_bandwidthkbps": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 89},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 96}
      ],
      "disk_read_io_ppm": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 413145},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 427745}
      ],
      "disk_read_iops": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 8},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 7}
      ],
      "disk_usage_bytes": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 452070524121},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 452051180761}
      ],
      "disk_usage_ppm": [
        {"timestamp": "2026-07-20T13:13:30+00:00", "value": 748358},
        {"timestamp": "2026-07-20T13:13:00+00:00", "value": 748346}
      ],
      "disk_write_io_avg_latency_microsec": null,
      "disk_write_io_bandwidthkbps": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 1135},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 1105}
      ],
      "disk_write_io_ppm": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 586854},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 572254}
      ],
      "disk_write_iops": [
        {"timestamp": "2026-07-20T13:12:00+00:00", "value": 12},
        {"timestamp": "2026-07-20T13:11:30+00:00", "value": 9}
      ],
      "ext_id": null,
      "links": null,
      "tenant_id": null
    }

ext_id:
  description:
    - The external ID of the disk whose stats were fetched.
  returned: always
  type: str
  sample: "4542a93c-f79a-43fc-a515-ec8c066000a0"

changed:
  description: This indicates whether the task resulted in any changes. Always false for stats fetches.
  returned: always
  type: bool
  sample: false

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching disk stats"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_disks_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
        start_time=dict(type="str", required=True),
        end_time=dict(type="str", required=True),
        sampling_interval=dict(type="int", required=False),
        stat_type=dict(
            type="str",
            required=False,
            choices=["SUM", "MIN", "MAX", "AVG", "COUNT", "LAST"],
        ),
    )

    return module_args


def get_disk_stats(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["ext_id", "start_time", "end_time"])
    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")
    sampling_interval = module.params.get("sampling_interval")
    stat_type = module.params.get("stat_type")
    resp = None
    try:
        resp = api_instance.get_disk_stats(
            extId=ext_id,
            _startTime=start_time,
            _endTime=end_time,
            _samplingInterval=sampling_interval,
            _statType=stat_type,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching disk stats",
        )
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        module.fail_json(
            msg="Failed fetching disk stats for ext_id: {0}".format(ext_id), **result
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
        "error": None,
        "response": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_disks_api_instance(module)
    get_disk_stats(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
