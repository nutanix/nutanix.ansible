#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_traffic_mirror_stat_v2
short_description: Retrieve traffic mirror session statistics from Nutanix Prism Central
version_added: 2.7.0
description:
  - Fetch statistics for a Nutanix traffic mirror session using its external ID.
  - The API returns time-series values for C(transmit_packet_count) and
    C(transmit_byte_count) collected during the requested time window.
  - Both C(start_time) and C(end_time) are mandatory ISO-8601 timestamps.
  - Optional C(sampling_interval) controls the resolution of the returned series
    and C(stat_type) controls how the values are aggregated
    (SUM, MIN, MAX, AVG, COUNT, LAST).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Traffic mirror session statistics) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, Network Infra Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the traffic mirror session.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - "sample input time is 2024-07-31T12:41:56.955Z"
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - "sample input time is 2025-07-31T12:41:56.955Z"
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval in seconds at which statistical data should be
        collected. For example, if you want performance statistics every 30
        seconds, then provide the value as 30.
    type: int
    required: false
  stat_type:
    description:
      - The down-sampling operator to apply on the returned stats values.
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
      - A URL query parameter that allows clients to request a specific set of
        properties for each entity or complex type. Expression specified with the
        $select must conform to the OData V4.01 URL conventions. If a $select
        expression consists of a single select item that is an asterisk
        (i.e., '*'), then all properties on the matching resource will be
        returned.
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
- name: Fetch traffic mirror session stats for the last 5 minutes
  nutanix.ncp.ntnx_traffic_mirror_stat_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cae2b71d-e46d-4d10-8c8b-1c9c6f2f7501"
    start_time: "2026-07-21T05:00:00.000Z"
    end_time: "2026-07-21T05:05:00.000Z"
  register: result

- name: Fetch traffic mirror session stats with sampling interval and stat type
  nutanix.ncp.ntnx_traffic_mirror_stat_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cae2b71d-e46d-4d10-8c8b-1c9c6f2f7501"
    start_time: "2026-07-21T05:00:00.000Z"
    end_time: "2026-07-21T05:05:00.000Z"
    sampling_interval: 30
    stat_type: "SUM"
  register: result

- name: Fetch traffic mirror session stats and only return transmit_packet_count
  nutanix.ncp.ntnx_traffic_mirror_stat_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cae2b71d-e46d-4d10-8c8b-1c9c6f2f7501"
    start_time: "2026-07-21T05:00:00.000Z"
    end_time: "2026-07-21T05:05:00.000Z"
    sampling_interval: 30
    stat_type: "AVG"
    select: "transmitPacketCount"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for fetching traffic mirror session statistics.
    - Contains time-series arrays for C(transmit_packet_count) and
      C(transmit_byte_count) along with C(stat_type), C(ext_id), C(links)
      and C(tenant_id).
  returned: always
  type: dict
  sample:
    {
      "ext_id": "cae2b71d-e46d-4d10-8c8b-1c9c6f2f7501",
      "links": null,
      "stat_type": "LAST",
      "tenant_id": null,
      "transmit_byte_count": [0],
      "transmit_packet_count": [0]
    }

ext_id:
  description:
    - The external ID of the traffic mirror session.
  returned: always
  type: str
  sample: "cae2b71d-e46d-4d10-8c8b-1c9c6f2f7501"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching traffic mirror session stats"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_traffic_mirror_stats_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

# Suppress the InsecureRequestWarning
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
            choices=[
                "SUM",
                "AVG",
                "MIN",
                "MAX",
                "COUNT",
                "LAST",
            ],
        ),
        select=dict(type="str", required=False),
    )

    return module_args


def get_traffic_mirror_stat(module, api_instance, result):
    """Fetch traffic mirror session stats for the given ext_id.

    Args:
        module: Ansible module instance.
        api_instance: TrafficMirrorStatsApi SDK instance.
        result: mutable result dict updated in place.
    """
    validate_required_params(module, ["ext_id", "start_time", "end_time"])

    ext_id = module.params.get("ext_id")
    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")
    sampling_interval = module.params.get("sampling_interval")
    stat_type = module.params.get("stat_type")
    select = module.params.get("select")

    result["ext_id"] = ext_id

    try:
        resp = api_instance.get_traffic_mirror_stats(
            extId=ext_id,
            _startTime=start_time,
            _endTime=end_time,
            _samplingInterval=sampling_interval,
            _statType=stat_type,
            _select=select,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching traffic mirror session stats",
        )

    if getattr(resp, "data", None) is None:
        result["response"] = None
        module.fail_json(msg="Failed fetching traffic mirror session stats", **result)

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
        "error": None,
        "response": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_traffic_mirror_stats_api_instance(module)
    get_traffic_mirror_stat(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
