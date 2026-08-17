#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_antivirus_server_stats_info_v2
short_description: Fetch antivirus server statistics info in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to fetch information about AntivirusServerStat in Nutanix Prism Central.
  - The Nutanix Files v4 statistics API exposes antivirus server statistics as a read only,
    get-by-id style entity, so C(ext_id) and C(file_server_ext_id) are always required and the
    module always fetches the statistics of that single antivirus server.
  - Listing / filtering is not supported by the underlying stats endpoint.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get antivirus server statistics) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - The external identifier of the file server that hosts the antivirus server.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the antivirus server whose statistics are requested.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - Sample input time is 2024-07-31T12:41:56.955Z
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - Sample input time is 2025-07-31T12:41:56.955Z
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
      - The type of down sampling operation that should be performed on the requested statistics.
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
      - A URL query parameter that allows clients to request a specific set of properties for each entity.
      - Comma separated list of one or more of
        C(cleanedFileCount), C(disconnectCount), C(latencyMs), C(quarantinedFileCount),
        C(scannedFileCount), C(threatCount), C(throughputBps).
      - Use C(*) to select all properties.
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
 - Nutanix (@nutanix)
"""

EXAMPLES = r"""
- name: Fetch antivirus server stats using external ID
  nutanix.ncp.ntnx_files_antivirus_server_stats_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    file_server_ext_id: "b2c3d4e5-6f78-4a90-b1c2-d3e4f5a6b7c8"
    ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
  register: result

- name: Fetch antivirus server stats with all attributes
  nutanix.ncp.ntnx_files_antivirus_server_stats_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    file_server_ext_id: "b2c3d4e5-6f78-4a90-b1c2-d3e4f5a6b7c8"
    ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
    sampling_interval: 30
    stat_type: "AVG"
    select: "scannedFileCount,threatCount"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC AntivirusServerStat info v4 API.
    - It returns the statistics of the antivirus server identified by C(ext_id).
  returned: always
  type: dict
  sample:
    {
        "cleaned_file_count": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 0
            }
        ],
        "disconnect_count": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 0
            }
        ],
        "ext_id": "18f78959-14a6-4c47-b5db-920460c4b668",
        "latency_ms": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 12
            }
        ],
        "links": null,
        "quarantined_file_count": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 0
            }
        ],
        "scanned_file_count": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 145
            }
        ],
        "tenant_id": null,
        "threat_count": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 0
            }
        ],
        "throughput_bps": [
            {
                "timestamp": "2024-07-31T11:29:00+00:00",
                "value": 10485760
            }
        ]
    }
changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false
ext_id:
  description: External ID of the antivirus server whose statistics were fetched.
  type: str
  returned: always
  sample: "18f78959-14a6-4c47-b5db-920460c4b668"
error:
  description: This field holds the error message if an error occurs.
  type: str
  returned: when an error occurs
failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching antivirus server stats"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import get_analytics_api_instance  # noqa: E402
from ..module_utils.v4.files.helpers import get_antivirus_server_stats  # noqa: E402
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
        select=dict(type="str"),
    )

    return module_args


def get_antivirus_server_stats_with_ext_id(module, result):
    api_instance = get_analytics_api_instance(module)
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    resp = get_antivirus_server_stats(module, api_instance, file_server_ext_id, ext_id)

    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = None


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
    get_antivirus_server_stats_with_ext_id(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
