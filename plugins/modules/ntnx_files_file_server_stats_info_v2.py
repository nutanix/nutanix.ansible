#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_file_server_stats_info_v2
short_description: Fetch File Server statistics info (File Server, Antivirus
    Server, or Mount Target) from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about FileServerStat in
    Nutanix Prism Central.
  - >-
    When only C(ext_id) is provided, the module fetches statistics for the
    File Server identified by C(ext_id).
  - >-
    When C(ext_id) is provided together with C(antivirus_server_ext_id), the
    module fetches statistics for the given Antivirus Server attached to the
    File Server.
  - >-
    When C(ext_id) is provided together with C(mount_target_ext_id), the
    module fetches statistics for the given Mount Target attached to the
    File Server.
  - The Nutanix Files v4 stats APIs only expose read operations; there is no
    list-all API for File Server stats — an entity ext_id is always required.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get statistics for File Server, Antivirus Server, or Mount Target) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin.
options:
  ext_id:
    description:
      - The external identifier of the File Server whose statistics are to be
        fetched.
      - Required for every operation.
    type: str
    required: true
  antivirus_server_ext_id:
    description:
      - The external identifier of an Antivirus Server attached to the File
        Server referenced by C(ext_id).
      - When provided, the module fetches Antivirus Server statistics.
      - Mutually exclusive with C(mount_target_ext_id).
    type: str
    required: false
  mount_target_ext_id:
    description:
      - The external identifier of a Mount Target attached to the File Server
        referenced by C(ext_id).
      - When provided, the module fetches Mount Target statistics.
      - Mutually exclusive with C(antivirus_server_ext_id).
    type: str
    required: false
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
        collected.
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
      - Use C(*) to return all properties.
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
- name: Fetch File Server stats using ext_id
  nutanix.ncp.ntnx_files_file_server_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6ca5de7e-a9a8-4318-4a62-68b8d5833af7"
    start_time: "2026-07-20T00:00:00.000Z"
    end_time: "2026-07-21T00:00:00.000Z"
  register: fs_stats_info

- name: Fetch Antivirus Server stats for a File Server
  nutanix.ncp.ntnx_files_file_server_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6ca5de7e-a9a8-4318-4a62-68b8d5833af7"
    antivirus_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    start_time: "2026-07-20T00:00:00.000Z"
    end_time: "2026-07-21T00:00:00.000Z"
    sampling_interval: 300
    stat_type: "AVG"
  register: av_stats_info

- name: Fetch Mount Target stats for a File Server
  nutanix.ncp.ntnx_files_file_server_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6ca5de7e-a9a8-4318-4a62-68b8d5833af7"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    start_time: "2026-07-20T00:00:00.000Z"
    end_time: "2026-07-21T00:00:00.000Z"
    select: "averageIops,averageLatencyUs"
  register: mt_stats_info
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC FileServerStat info v4 API.
    - >-
      When C(antivirus_server_ext_id) is provided, the response is an
      Antivirus Server stats object.
    - >-
      When C(mount_target_ext_id) is provided, the response is a Mount Target
      stats object.
    - Otherwise, the response is a File Server stats object.
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
      ]
    }
ext_id:
  description:
    - The external identifier of the sub-entity queried (antivirus server or
      mount target). When only File Server stats are queried, this is the
      File Server C(ext_id).
  returned: when a single entity is queried
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
    get_antivirus_server_stats,
    get_file_server_stats,
    get_mount_target_stats,
)
from ..module_utils.v4.utils import (  # noqa: E402
    strip_internal_attributes,
    validate_required_params,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
        antivirus_server_ext_id=dict(type="str"),
        mount_target_ext_id=dict(type="str"),
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


def _build_common_kwargs(module):
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
    return kwargs


def get_stats(module, api_instance, result):
    """Route to the correct stats endpoint based on the module params."""
    validate_required_params(module, ["ext_id", "start_time", "end_time"])

    file_server_ext_id = module.params.get("ext_id")
    antivirus_ext_id = module.params.get("antivirus_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")

    kwargs = _build_common_kwargs(module)

    if antivirus_ext_id:
        result["ext_id"] = antivirus_ext_id
        resp = get_antivirus_server_stats(
            module,
            api_instance,
            file_server_ext_id,
            antivirus_ext_id,
            **kwargs,
        )
        fail_msg = "Failed to fetch antivirus server stats for ext_id: {0}".format(
            antivirus_ext_id
        )
    elif mount_target_ext_id:
        result["ext_id"] = mount_target_ext_id
        resp = get_mount_target_stats(
            module,
            api_instance,
            file_server_ext_id,
            mount_target_ext_id,
            **kwargs,
        )
        fail_msg = "Failed to fetch mount target stats for ext_id: {0}".format(
            mount_target_ext_id
        )
    else:
        result["ext_id"] = file_server_ext_id
        resp = get_file_server_stats(module, api_instance, file_server_ext_id, **kwargs)
        fail_msg = "Failed to fetch file server stats for ext_id: {0}".format(
            file_server_ext_id
        )

    if getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        module.fail_json(msg=fail_msg, **result)


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
        mutually_exclusive=[
            ("antivirus_server_ext_id", "mount_target_ext_id"),
        ],
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_analytics_api_instance(module)
    get_stats(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
