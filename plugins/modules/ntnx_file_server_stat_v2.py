#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_file_server_stat_v2
short_description: Fetch statistics for a Nutanix File Server from Prism Central
version_added: 2.7.0
description:
  - Fetch time-series performance and capacity statistics for a specific
    Nutanix File Server managed by Prism Central.
  - The Nutanix Files v4 stats APIs only expose read operations for File Server
    statistics; there is no create, update, or delete API for this entity.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get File Server statistics) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin.
options:
  ext_id:
    description:
      - The external identifier of the File Server whose statistics are to be
        fetched.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format,
        e.g. C(2024-07-31T12:41:56.955Z).
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format,
        e.g. C(2025-07-31T12:41:56.955Z).
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval in seconds at which statistical data should be
        collected. For example, provide C(30) to get data points every 30
        seconds.
    type: int
    required: false
  stat_type:
    description:
      - The down-sampling operator to apply when aggregating the raw stats
        into the requested sampling interval.
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
      - Comma-separated list of specific stat properties to return.
      - Follows the OData V4.01 C($select) query convention.
      - >-
        Valid property names include C(avCleanedFileCount), C(avLatencyMs),
        C(avQuarantinedFileCount), C(avScannedFileCount), C(avThreatCount),
        C(avThroughputBps), C(averageIops), C(averageLatencyUs),
        C(averageThroughputBps), C(datasetSpaceUsedBytes),
        C(icapDaemonQueueLength), C(metadataIops), C(metadataLatencyUs),
        C(numberOfConnections), C(numberOfFiles), C(readIops),
        C(readLatencyUs), C(readThroughputBps), C(snapshotUsedBytes),
        C(totalTieredBytes), C(writeIops), C(writeLatencyUs),
        C(writeThroughputBps). Use C(*) to return all properties.
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
- name: Fetch File Server stats for a given time window
  nutanix.ncp.ntnx_file_server_stat_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6ca5de7e-a9a8-4318-4a62-68b8d5833af7"
    start_time: "2026-07-20T00:00:00.000Z"
    end_time: "2026-07-21T00:00:00.000Z"
  register: fs_stats

- name: Fetch File Server stats with sampling interval and stat_type
  nutanix.ncp.ntnx_file_server_stat_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6ca5de7e-a9a8-4318-4a62-68b8d5833af7"
    start_time: "2026-07-20T00:00:00.000Z"
    end_time: "2026-07-21T00:00:00.000Z"
    sampling_interval: 300
    stat_type: "AVG"
    select: "averageIops,averageLatencyUs,averageThroughputBps"
  register: fs_stats
"""

RETURN = r"""
response:
  description:
    - The full API response for the File Server statistics query.
    - Time-series stats are returned as lists of C({value, timestamp}) pairs.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "6ca5de7e-a9a8-4318-4a62-68b8d5833af7",
      "links": null,
      "tenant_id": null,
      "average_iops": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 3}
      ],
      "average_latency_us": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 812}
      ],
      "average_throughput_bps": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 4096}
      ],
      "read_iops": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 2}
      ],
      "read_latency_us": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 750}
      ],
      "read_throughput_bps": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 3072}
      ],
      "write_iops": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 1}
      ],
      "write_latency_us": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 900}
      ],
      "write_throughput_bps": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 1024}
      ],
      "metadata_iops": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 0}
      ],
      "metadata_latency_us": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 0}
      ],
      "number_of_connections": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 1}
      ],
      "number_of_files": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 25}
      ],
      "snapshot_used_bytes": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 0}
      ],
      "dataset_space_used_bytes": [
          {"timestamp": "2026-07-20T00:00:00+00:00", "value": 10485760}
      ],
      "total_tiered_bytes": null,
      "av_scanned_file_count": null,
      "av_threat_count": null,
      "av_cleaned_file_count": null,
      "av_quarantined_file_count": null,
      "av_latency_ms": null,
      "av_throughput_bps": null,
      "icap_daemon_queue_length": null
    }
ext_id:
  description: External identifier of the File Server whose stats were fetched.
  returned: always
  type: str
  sample: "6ca5de7e-a9a8-4318-4a62-68b8d5833af7"
changed:
  description: Whether the task resulted in any change. Always C(false).
  returned: always
  type: bool
  sample: false
failed:
  description: Whether the task failed.
  returned: always
  type: bool
  sample: false
msg:
  description: Optional status/error message.
  returned: When there is an error or nothing to return
  type: str
  sample: "Api Exception raised while fetching file server stats for ext_id: 6ca5de7e-a9a8-4318-4a62-68b8d5833af7"
error:
  description: The error message if an error occurs.
  returned: When an error occurs
  type: str
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import get_analytics_api_instance  # noqa: E402
from ..module_utils.v4.files.helpers import (  # noqa: E402
    get_file_server_stats as fetch_file_server_stats,
)
from ..module_utils.v4.utils import (  # noqa: E402
    strip_internal_attributes,
    validate_required_params,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
        start_time=dict(type="str", required=True),
        end_time=dict(type="str", required=True),
        sampling_interval=dict(type="int"),
        stat_type=dict(
            type="str",
            choices=["SUM", "AVG", "MIN", "MAX", "COUNT", "LAST"],
        ),
        select=dict(type="str"),
    )

    return module_args


def get_file_server_stat(module, api_instance, result):
    """Populate ``result`` with the File Server stats response."""
    validate_required_params(module, ["ext_id", "start_time", "end_time"])

    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    kwargs = {
        "_startTime": module.params.get("start_time"),
        "_endTime": module.params.get("end_time"),
    }
    if module.params.get("sampling_interval") is not None:
        kwargs["_samplingInterval"] = module.params.get("sampling_interval")
    if module.params.get("stat_type") is not None:
        kwargs["_statType"] = module.params.get("stat_type")
    if module.params.get("select") is not None:
        kwargs["_select"] = module.params.get("select")

    resp = fetch_file_server_stats(module, api_instance, ext_id, **kwargs)

    if getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        module.fail_json(
            msg="Failed to fetch file server stats for ext_id: {0}".format(ext_id),
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
        "response": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_analytics_api_instance(module)
    get_file_server_stat(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
