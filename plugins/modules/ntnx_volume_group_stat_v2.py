#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_stat_v2
short_description: Fetch time-series statistics for a Nutanix Volume Group from PC
version_added: 2.7.0
description:
  - This module allows you to fetch time-series performance, utilization, and
    capacity statistics for a specific Volume Group in Nutanix Prism Central.
  - Requires the external ID of the Volume Group along with the reporting time
    window (C(start_time), C(end_time)).
  - Optionally accepts C(sampling_interval) and C(stat_type) to control
    granularity and down-sampling of the returned data points.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get statistics for a Volume Group) -
    Required Roles: Backup Admin, Prism Admin, Prism Viewer, Project Admin, Project Manager, Self-Service Admin (Deprecated),
    Storage Admin, Storage Viewer, Super Admin, Tenant Admin, Tenant Consumer
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  ext_id:
    description:
      - The external identifier of the Volume Group whose stats are to be
        fetched.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - For example, start time of 2022-04-23T01:23:45.678+09:00 would consider all stats starting at 1:23:45.678 on the 23rd of April 2022.
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - Must be greater than or equal to C(start_time).
      - For example, end time of 2022-04-23T01:23:45.678+09:00 would consider all stats ending at 1:23:45.678 on the 23rd of April 2022.
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
      - The operator to use while performing down-sampling on stats data. Allowed values are SUM, MIN, MAX, AVG, COUNT and LAST.
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
      - A URL query parameter that allows clients to request a specific set of properties for each entity or complex type.
      - Expression specified with the $select must conform to the OData V4.01 URL conventions.
      - If a $select expression consists of a single select item that is an asterisk (i.e., *),
        then all properties on the matching resource will be returned.
      - If both $select and $apply query parameters are present, $select will be applied on entities within the groups.
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
- name: Fetch Volume Group stats for the last 5 minutes
  nutanix.ncp.ntnx_volume_group_stat_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "792cd764-37b5-4da3-7ef1-ea3f618c1648"
    start_time: "2026-04-19T06:00:00.000Z"
    end_time: "2026-04-19T06:05:00.000Z"
  register: result

- name: Fetch Volume Group stats with all attributes (interval, stat_type, select)
  nutanix.ncp.ntnx_volume_group_stat_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "792cd764-37b5-4da3-7ef1-ea3f618c1648"
    start_time: "2026-04-19T06:00:00.000Z"
    end_time: "2026-04-19T07:00:00.000Z"
    sampling_interval: 120
    stat_type: "AVG"
    select: "*"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for fetching Volume Group time-series statistics.
    - Contains arrays of TimeValuePair samples for I/O, bandwidth, latency and
      capacity metrics.
  type: dict
  returned: always
  sample:
    {
      "controller_avg_io_latency_usecs": [
        {
          "timestamp": "2026-04-19T06:00:00+00:00",
          "value": 947
        },
        {
          "timestamp": "2026-04-19T06:00:30+00:00",
          "value": 1061
        }
      ],
      "controller_avg_read_io_latency_usecs": [
        {
          "timestamp": "2026-04-19T06:00:00+00:00",
          "value": 797
        }
      ],
      "controller_avg_write_io_latency_usecs": [
        {
          "timestamp": "2026-04-19T06:00:00+00:00",
          "value": 2175
        }
      ],
      "controller_io_bandwidth_k_bps": [
        {
          "timestamp": "2026-04-19T06:00:00+00:00",
          "value": 53450
        }
      ],
      "controller_num_iops": [
        {
          "timestamp": "2026-04-19T06:00:00+00:00",
          "value": 1247
        }
      ],
      "controller_num_read_iops": [
        {
          "timestamp": "2026-04-19T06:00:00+00:00",
          "value": 1110
        }
      ],
      "controller_num_write_iops": [
        {
          "timestamp": "2026-04-19T06:00:00+00:00",
          "value": 136
        }
      ],
      "controller_read_io_bandwidth_k_bps": [
        {
          "timestamp": "2026-04-19T06:00:00+00:00",
          "value": 52171
        }
      ],
      "controller_user_bytes": [
        {
          "timestamp": "2026-04-19T06:00:00+00:00",
          "value": 139663605760
        }
      ],
      "controller_write_io_bandwidth_k_bps": [
        {
          "timestamp": "2026-04-19T06:00:00+00:00",
          "value": 1278
        }
      ],
      "ext_id": null,
      "hydration_remaining_bytes": null,
      "links": null,
      "tenant_id": null,
      "volume_group_ext_id": "792cd764-37b5-4da3-7ef1-ea3f618c1648"
    }
changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false
ext_id:
  description:
    - The external ID of the Volume Group whose stats were fetched.
  type: str
  returned: always
  sample: "792cd764-37b5-4da3-7ef1-ea3f618c1648"
msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or informational message.
  type: str
  sample: "Api Exception raised while fetching volume group stats"
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import get_vg_api_instance  # noqa: E402


def get_module_spec():
    module_args = dict(
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


def get_volume_group_stats(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")
    sampling_interval = module.params.get("sampling_interval")
    stat_type = module.params.get("stat_type")
    select = module.params.get("select")
    kwargs = {}
    if sampling_interval:
        kwargs["_samplingInterval"] = sampling_interval
    if stat_type:
        kwargs["_statType"] = stat_type
    if select:
        kwargs["_select"] = select
    kwargs["_startTime"] = start_time
    kwargs["_endTime"] = end_time
    kwargs["extId"] = ext_id
    resp = None
    try:
        resp = list_entities(api_instance.get_volume_group_stats, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching volume group stats",
        )
    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


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
    }
    api_instance = get_vg_api_instance(module)
    get_volume_group_stats(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
