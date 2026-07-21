#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpn_connection_stat_v2
short_description: Retrieve VPN connection statistics from Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to fetch time-series statistics (throughput Rx/Tx in Kbps)
    for a specific VPN connection managed by Nutanix Flow Virtual Networking.
  - The statistics are returned over a user provided time window and can be
    downsampled using aggregation operators such as SUM, AVG, MIN, MAX, COUNT or LAST.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Get VPN connection statistics) -
    Required Roles: Super Admin, Prism Admin, Prism Viewer, Network Infra Admin,
    VPC Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the VPN connection whose statistics should be
        retrieved.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - Sample input time is C(2024-07-31T12:41:56.955Z).
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - Sample input time is C(2025-07-31T12:41:56.955Z).
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval in seconds at which statistical data should be
        collected. For example, if you want performance statistics every 30
        seconds, provide the value as 30.
    type: int
    required: false
  stat_type:
    description:
      - The downsampling operator used to aggregate metric values within each
        sampling interval.
      - If not provided, the API defaults to C(AVG).
    type: str
    required: false
    choices:
      - SUM
      - MIN
      - MAX
      - AVG
      - COUNT
      - LAST
  page:
    description:
      - A URL query parameter that specifies the page number of the result set.
        It must be a positive integer between 0 and the maximum number of pages
        available for that resource.
    type: int
    required: false
  limit:
    description:
      - A URL query parameter that specifies the total number of records
        returned in the result set. Must be a positive integer between 1 and 100.
        If not provided, a default of 50 is used by the API.
    type: int
    required: false
  select:
    description:
      - A URL query parameter that allows clients to request a specific set of
        properties for each entity. Expression must conform to OData v4.01
        conventions.
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
"""

EXAMPLES = r"""
- name: Fetch VPN connection stats over a time window
  nutanix.ncp.ntnx_vpn_connection_stat_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "5482651f-f898-4964-9c30-3549033d6d92"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2024-07-31T13:41:56.955Z"
  register: result

- name: Fetch VPN connection stats with all supported parameters
  nutanix.ncp.ntnx_vpn_connection_stat_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "5482651f-f898-4964-9c30-3549033d6d92"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2024-07-31T13:41:56.955Z"
    sampling_interval: 30
    stat_type: AVG
    limit: 50
    page: 0
    select: "throughputRxKbps,throughputTxKbps"
  register: result
"""

RETURN = r"""
response:
  description:
    - The full API response containing the requested VPN connection statistics.
    - Includes throughput Rx and Tx values (in Kbps) as time-series arrays for the
      selected time window.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "5482651f-f898-4964-9c30-3549033d6d92",
      "links": null,
      "stat_type": "AVG",
      "tenant_id": null,
      "throughput_rx_kbps": [
        {
          "timestamp": "2024-07-31T12:42:00+00:00",
          "value": 0
        },
        {
          "timestamp": "2024-07-31T12:42:30+00:00",
          "value": 0
        }
      ],
      "throughput_tx_kbps": [
        {
          "timestamp": "2024-07-31T12:42:00+00:00",
          "value": 0
        },
        {
          "timestamp": "2024-07-31T12:42:30+00:00",
          "value": 0
        }
      ]
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the VPN connection whose statistics were fetched.
  returned: always
  type: str
  sample: "5482651f-f898-4964-9c30-3549033d6d92"

msg:
  description: A status or error message returned by the module.
  returned: When there is an error or informational message
  type: str
  sample: "Api Exception raised while fetching VPN connection stats"

error:
  description: The error details if any error occurs during the operation.
  returned: when an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_vpn_connection_stats_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


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
                "MIN",
                "MAX",
                "AVG",
                "COUNT",
                "LAST",
            ],
        ),
        page=dict(type="int"),
        limit=dict(type="int"),
        select=dict(type="str"),
    )

    return module_args


def get_vpn_connection_stats(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    kwargs = {
        "extId": ext_id,
        "_startTime": module.params.get("start_time"),
        "_endTime": module.params.get("end_time"),
    }

    if module.params.get("sampling_interval") is not None:
        kwargs["_samplingInterval"] = module.params.get("sampling_interval")
    if module.params.get("stat_type") is not None:
        kwargs["_statType"] = module.params.get("stat_type")
    if module.params.get("page") is not None:
        kwargs["_page"] = module.params.get("page")
    if module.params.get("limit") is not None:
        kwargs["_limit"] = module.params.get("limit")
    if module.params.get("select") is not None:
        kwargs["_select"] = module.params.get("select")

    try:
        resp = api_instance.get_vpn_connection_stats(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VPN connection stats",
        )
        return

    if getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = None
        module.fail_json(
            msg="Failed fetching VPN connection stats for ext_id: {0}".format(ext_id),
            **result,
        )


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
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

    if module.check_mode:
        result["ext_id"] = module.params.get("ext_id")
        result["msg"] = (
            "VPN connection stats fetch skipped due to check_mode for ext_id: {0}".format(
                module.params.get("ext_id")
            )
        )
        module.exit_json(**result)

    api_instance = get_vpn_connection_stats_api_instance(module)
    get_vpn_connection_stats(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
