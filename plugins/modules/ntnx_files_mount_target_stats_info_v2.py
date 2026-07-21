#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_mount_target_stats_info_v2
short_description: Fetch mount target statistics info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about MountTargetStat in Nutanix Prism Central.
  - It fetches the statistics of a specific mount target (share/export) identified by C(ext_id)
    belonging to the file server identified by C(file_server_ext_id).
  - The mount target statistics datasource always requires an external ID, so this module always
    fetches a single MountTargetStat entity for the requested reporting time window.
  - This module uses PC v4 APIs based SDKs.
options:
  file_server_ext_id:
    description:
      - The external identifier of the file server that owns the mount target.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the mount target.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - sample input time is 2024-07-31T12:41:56.955Z
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - sample input time is 2025-07-31T12:41:56.955Z
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
      - The type of stats (down-sampling operator) applied while aggregating the data points.
    type: str
    required: false
    choices:
      - SUM
      - AVG
      - MIN
      - MAX
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
- name: Fetch mount target stats using external IDs
  nutanix.ncp.ntnx_files_mount_target_stats_info_v2:
    file_server_ext_id: 5f1e537d-6777-4c22-5d41-ddd0c3337aa9
    ext_id: 9c1e537d-6777-4c22-5d41-ddd0c3337aa9
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
  register: result
  ignore_errors: true

- name: Fetch mount target stats with sampling interval and stat type
  nutanix.ncp.ntnx_files_mount_target_stats_info_v2:
    file_server_ext_id: 5f1e537d-6777-4c22-5d41-ddd0c3337aa9
    ext_id: 9c1e537d-6777-4c22-5d41-ddd0c3337aa9
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
    sampling_interval: 30
    stat_type: "AVG"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC MountTargetStat info v4 API.
    - It is a single MountTargetStat entity for the file server and mount target external IDs provided.
  returned: always
  type: dict
  sample:
    {
        "average_iops": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 12
            }
        ],
        "average_latency_us": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 947
            }
        ],
        "average_throughput_bps": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 53450
            }
        ],
        "dataset_space_used_bytes": null,
        "ext_id": "9c1e537d-6777-4c22-5d41-ddd0c3337aa9",
        "links": null,
        "metadata_iops": null,
        "metadata_latency_us": null,
        "number_of_connections": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 3
            }
        ],
        "number_of_files": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 128
            }
        ],
        "read_iops": null,
        "read_latency_us": null,
        "read_throughput_bps": null,
        "snapshot_used_bytes": null,
        "tenant_id": null,
        "tiering_latency_ms": null,
        "used_bytes": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 139663605760
            }
        ],
        "write_iops": null,
        "write_latency_us": null,
        "write_throughput_bps": null
    }
changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false
ext_id:
  description: The external ID of the mount target.
  type: str
  returned: always
  sample: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching mount target stats for mount target ext_id: 9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs
failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import get_analytics_api_instance  # noqa: E402
from ..module_utils.v4.files.helpers import get_mount_target_stats  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
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


def get_mount_target_stats_with_ext_id(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_mount_target_stats(module, api_instance, file_server_ext_id, ext_id)
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        module.fail_json(msg="Failed fetching mount target stats", **result)


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
    }
    api_instance = get_analytics_api_instance(module)
    get_mount_target_stats_with_ext_id(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
