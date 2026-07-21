#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpc_ns_stats_info_v2
short_description: Fetch VPC North-South statistics in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about VpcNsStat in Nutanix Prism Central.
  - Retrieve VPC North-South traffic statistics for a specific external subnet
    attached to a given VPC over a specified time interval.
  - This module invokes the get VPC North-South stats V4 API for a given
    (vpc_ext_id, ext_id) pair and returns the corresponding stats time series.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get VPC North-South statistics) -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Super Admin,
      VPC Admin, VPC Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  vpc_ext_id:
    description:
      - The external ID (UUID) of the VPC for which North-South statistics should be fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external ID (UUID) of the external subnet attached to the VPC
        for which North-South statistics should be fetched.
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
        For example, if you want performance statistics every 30 seconds, then provide the value as 30.
    type: int
    required: false
  stat_type:
    description:
      - The down-sampling operator to use while aggregating stats data.
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
- name: Fetch VPC North-South stats for an external subnet
  nutanix.ncp.ntnx_vpc_ns_stats_info_v2:
    vpc_ext_id: "a4f3f04f-1222-8544-7896-28b62bcc3e3e"
    ext_id: "9306c8d3-1111-2222-3333-ef2dfbd2c7ba"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
  register: result
  ignore_errors: true

- name: Fetch VPC North-South stats with all attributes
  nutanix.ncp.ntnx_vpc_ns_stats_info_v2:
    vpc_ext_id: "a4f3f04f-1222-8544-7896-28b62bcc3e3e"
    ext_id: "9306c8d3-1111-2222-3333-ef2dfbd2c7ba"
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
    - The response from the Nutanix PC VpcNsStat info v4 API.
    - Contains the VPC North-South statistics time series for the given
      (vpc_ext_id, ext_id) pair over the requested time interval.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "9306c8d3-1111-2222-3333-ef2dfbd2c7ba",
      "links": null,
      "north_south_egress_bytes_abs": [],
      "north_south_egress_bytes_per_sec": [],
      "north_south_egress_packets_abs": [],
      "north_south_egress_packets_per_sec": [],
      "north_south_ingress_bytes_abs": [],
      "north_south_ingress_bytes_per_sec": [],
      "north_south_ingress_packets_abs": [],
      "north_south_ingress_packets_per_sec": [],
      "stat_type": "AVG",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VPC North-South stats"

error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - The external ID of the external subnet whose VPC North-South stats were fetched.
  type: str
  returned: always
  sample: "9306c8d3-1111-2222-3333-ef2dfbd2c7ba"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_vpc_ns_stats_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        vpc_ext_id=dict(type="str", required=True),
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
    )

    return module_args


def get_vpc_ns_stats(module, api_instance, result):
    vpc_ext_id = module.params.get("vpc_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")
    sampling_interval = module.params.get("sampling_interval")
    stat_type = module.params.get("stat_type")
    resp = None
    try:
        resp = api_instance.get_vpc_ns_stats(
            vpcExtId=vpc_ext_id,
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
            msg="Api Exception raised while fetching VPC North-South stats",
        )

    if getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        module.fail_json(msg="Failed fetching VPC North-South stats", **result)


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
    api_instance = get_vpc_ns_stats_api_instance(module)
    get_vpc_ns_stats(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
