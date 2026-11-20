#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_load_balancer_session_stats_info_v2
short_description: Fetch load balancer session listener and target statistics from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about LoadBalancerSessionStat in Nutanix Prism Central.
  - Retrieves per-session listener and target traffic statistics (bytes, packets, requests)
    over the requested time interval for a given load balancer session external ID.
  - The Networking v4 API only exposes a get-by-ID stats endpoint for load balancer
    sessions, therefore this module requires C(ext_id), C(start_time) and C(end_time).
  - Optional C(sampling_interval), C(stat_type) and C(select) allow shaping of
    the returned statistics data.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Load Balancer Session statistics) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the load balancer session whose statistics should be fetched.
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
      - MIN
      - MAX
      - AVG
      - COUNT
      - LAST
  select:
    description:
      - A URL query parameter that allows clients to request a specific set of
        properties for each entity or complex type. Expression specified with the
        $select must conform to the OData V4.01 URL conventions.
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
- name: Fetch load balancer session stats over a time window
  nutanix.ncp.ntnx_load_balancer_session_stats_info_v2:
    ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    start_time: "2026-07-20T12:36:56.955Z"
    end_time: "2026-07-20T12:41:56.955Z"
  register: result
  ignore_errors: true

- name: Fetch load balancer session stats with all attributes
  nutanix.ncp.ntnx_load_balancer_session_stats_info_v2:
    ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    start_time: "2026-07-20T12:36:56.955Z"
    end_time: "2026-07-20T12:41:56.955Z"
    sampling_interval: 30
    stat_type: "SUM"
    select: "*"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC LoadBalancerSessionStat info v4 API.
    - Contains listener and target statistics for the requested load balancer session
      over the requested time window.
    - The Networking v4 API only exposes a get-by-ID stats endpoint for load balancer
      sessions, so filter, limit, page and orderby are not supported.
  type: dict
  returned: always
  sample:
    {
      "ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
      "stat_type": "SUM",
      "listener_stats": [
        {
          "virtual_ip_address": "10.44.76.100",
          "num_bytes": ["10240", "11264"],
          "num_packets": ["128", "132"],
          "num_requests": ["42", "46"]
        }
      ],
      "target_stats": [
        {
          "virtual_nic_reference": "6f1c1fbf-2a4c-4c22-9a5b-1a3f2b6b1d21",
          "num_bytes": ["5120"],
          "num_packets": ["64"],
          "num_requests": ["21"]
        }
      ],
      "links": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching load balancer session stats"

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
    - The external ID of the load balancer session whose stats were fetched.
  type: str
  returned: always
  sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_load_balancer_session_stats_api_instance,
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
        sampling_interval=dict(type="int", required=False),
        stat_type=dict(
            type="str",
            required=False,
            choices=[
                "SUM",
                "MIN",
                "MAX",
                "AVG",
                "COUNT",
                "LAST",
            ],
        ),
        select=dict(type="str", required=False),
    )

    return module_args


def get_load_balancer_session_stats(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_stats_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating load balancer session stats info spec", **result
        )

    if module.params.get("select") is not None:
        kwargs["_select"] = module.params.get("select")

    try:
        resp = api_instance.get_load_balancer_session_stats(
            extId=ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching load balancer session stats",
        )

    if getattr(resp, "data", None) is None:
        result["response"] = None
        module.fail_json(
            msg="Failed fetching load balancer session stats",
            **result,
        )

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
        "response": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_load_balancer_session_stats_api_instance(module)
    get_load_balancer_session_stats(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
