#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_layer2_stretch_stats_info_v2
short_description: Fetch Layer2 Stretch statistics from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Layer2StretchStat in Nutanix Prism Central.
  - Retrieve time-series metrics such as round-trip-time (rtt) and ingress/egress
    throughput for a Layer2 Stretch identified by C(ext_id) over a specified time interval.
  - The Networking v4 API only exposes a get-by-ID stats endpoint for Layer2 Stretches,
    therefore this module requires C(ext_id), C(start_time) and C(end_time).
  - Optional C(sampling_interval), C(stat_type), C(page), C(limit) and C(select) allow
    shaping of the returned statistics data.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(View Layer2 Stretch Stats) -
      Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin,
      Prism Viewer, Super Admin, Tenant Admin, User, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the Layer2 Stretch configuration whose stats to fetch.
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
      - The sampling interval in seconds at which statistical data should be
        collected. For example, if you want performance statistics every 30
        seconds, then provide the value as 30.
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
  page:
    description:
      - A URL query parameter that specifies the page number of the result set.
      - It must be a positive integer between 0 and the maximum number of pages
        that are available for that resource.
      - Any number out of this range might lead to no results.
    type: int
    required: false
  limit:
    description:
      - A URL query parameter that specifies the total number of records
        returned in the result set.
      - Must be a positive integer between 1 and 100.
      - Any number out of this range will lead to a validation error.
      - If the limit is not provided, a default value of 50 records will be
        returned in the result set.
    type: int
    required: false
  select:
    description:
      - A URL query parameter that allows clients to request a specific set of
        properties for each entity or complex type.
      - Expression specified with the C($select) must conform to the
        L(OData V4.01,https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html)
        URL conventions.
      - If a C($select) expression consists of a single select item that is an
        asterisk (i.e., C(*)), then all properties on the matching resource will
        be returned.
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
- name: Fetch Layer2 Stretch stats for a given time interval
  nutanix.ncp.ntnx_layer2_stretch_stats_info_v2:
    ext_id: "b8d1a2ef-3f8b-4e19-9f8c-3f8b4e199f8c"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
  register: result
  ignore_errors: true

- name: Fetch Layer2 Stretch stats with sampling interval and stat type
  nutanix.ncp.ntnx_layer2_stretch_stats_info_v2:
    ext_id: "b8d1a2ef-3f8b-4e19-9f8c-3f8b4e199f8c"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
    sampling_interval: 30
    stat_type: "AVG"
  register: result
  ignore_errors: true

- name: Fetch Layer2 Stretch stats with all attributes
  nutanix.ncp.ntnx_layer2_stretch_stats_info_v2:
    ext_id: "b8d1a2ef-3f8b-4e19-9f8c-3f8b4e199f8c"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2025-07-31T12:41:56.955Z"
    sampling_interval: 30
    stat_type: "SUM"
    page: 0
    limit: 50
    select: "*"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Layer2StretchStat info v4 API.
    - Returns the Layer2 Stretch statistics for the given external ID.
    - Includes time-series arrays for I(rtt), I(throughput_rx_kbps), and
      I(throughput_tx_kbps).
  type: dict
  returned: always
  sample:
    {
      "ext_id": "b8d1a2ef-3f8b-4e19-9f8c-3f8b4e199f8c",
      "links": null,
      "rtt": [],
      "stat_type": "AVG",
      "tenant_id": null,
      "throughput_rx_kbps": [],
      "throughput_tx_kbps": []
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
  sample: "Api Exception raised while fetching Layer2 Stretch stats"

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
    - The external ID of the Layer2 Stretch whose stats were fetched.
  type: str
  returned: always
  sample: "b8d1a2ef-3f8b-4e19-9f8c-3f8b4e199f8c"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_layer2_stretch_stats_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
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


def get_layer2_stretch_stats(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_stats_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Layer2 Stretch stats info spec", **result
        )

    info_kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Layer2 Stretch stats info spec", **result
        )
    kwargs.update(info_kwargs)

    resp = None
    try:
        resp = api_instance.get_layer2_stretch_stats(
            extId=ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Layer2 Stretch stats",
        )

    if getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = None
        module.fail_json(
            msg="Failed fetching Layer2 Stretch stats for ext_id: {0}".format(ext_id),
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
    api_instance = get_layer2_stretch_stats_api_instance(module)
    get_layer2_stretch_stats(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
