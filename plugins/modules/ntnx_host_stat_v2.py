#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_host_stat_v2
short_description: Retrieve host statistics from Nutanix Prism Central
version_added: 2.7.0
description:
  - Get stats for a host registered to Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(View Host Stats) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Manager,
    Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster the host belongs to.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the host.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - For example C(2026-07-19T00:00:00Z).
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - For example C(2026-07-20T00:00:00Z).
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval in seconds at which statistical data should be collected.
      - For example, if you want performance statistics every 30 seconds, then provide the value as 30.
    type: int
  stat_type:
    description:
      - The operator to use while performing down-sampling on stats data.
      - Allowed values are SUM, MIN, MAX, AVG, COUNT and LAST.
    type: str
    choices:
      - SUM
      - MIN
      - MAX
      - AVG
      - COUNT
      - LAST
  select:
    description:
      - A URL query parameter that allows clients to request a specific set of properties
        for each entity or complex type.
      - Expression specified with the C($select) must conform to the OData V4.01 URL conventions.
      - If a C($select) expression consists of a single select item that is an asterisk (i.e., C(*)),
        then all properties on the matching resource will be returned.
    type: str
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
- name: Fetch host stats during time interval
  nutanix.ncp.ntnx_host_stat_v2:
    cluster_ext_id: "0006c9d0-abcd-1234-5678-0242ac110002"
    ext_id: "d7f28e12-cafe-babe-0000-1a2b3c4d5e6f"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-20T00:00:00Z"
  register: result

- name: Fetch host stats with all attributes
  nutanix.ncp.ntnx_host_stat_v2:
    cluster_ext_id: "0006c9d0-abcd-1234-5678-0242ac110002"
    ext_id: "d7f28e12-cafe-babe-0000-1a2b3c4d5e6f"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-20T00:00:00Z"
    sampling_interval: 30
    stat_type: "AVG"
    select: "controllerNumIops,hypervisorCpuUsagePpm,overallMemoryUsagePpm"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for fetching host statistics.
  returned: always
  type: dict
  sample:
    {
      "controller_num_iops": [
          {"timestamp": "2026-07-19T00:00:00+00:00", "value": 128},
          {"timestamp": "2026-07-19T00:00:30+00:00", "value": 141}
      ],
      "hypervisor_cpu_usage_ppm": [
          {"timestamp": "2026-07-19T00:00:00+00:00", "value": 132456},
          {"timestamp": "2026-07-19T00:00:30+00:00", "value": 138245}
      ],
      "overall_memory_usage_ppm": [
          {"timestamp": "2026-07-19T00:00:00+00:00", "value": 654321},
          {"timestamp": "2026-07-19T00:00:30+00:00", "value": 657982}
      ],
      "ext_id": "d7f28e12-cafe-babe-0000-1a2b3c4d5e6f",
      "links": null,
      "tenant_id": null
    }

cluster_ext_id:
  description: The external ID of the cluster the host belongs to.
  returned: always
  type: str
  sample: "0006c9d0-abcd-1234-5678-0242ac110002"

ext_id:
  description: The external ID of the host.
  returned: always
  type: str
  sample: "d7f28e12-cafe-babe-0000-1a2b3c4d5e6f"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching host stats"

error:
  description: The error message if an error occurs.
  returned: when an error occurs
  type: str

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        start_time=dict(type="str", required=True),
        end_time=dict(type="str", required=True),
        sampling_interval=dict(type="int"),
        stat_type=dict(
            type="str",
            choices=["SUM", "MIN", "MAX", "AVG", "COUNT", "LAST"],
        ),
        select=dict(type="str"),
    )

    return module_args


def get_host_stats(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["cluster_ext_id"] = cluster_ext_id
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

    resp = None
    try:
        resp = api_instance.get_host_stats(
            clusterExtId=cluster_ext_id,
            extId=ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching host stats",
        )

    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        module.fail_json(msg="Failed fetching host stats", **result)


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
        "cluster_ext_id": None,
        "failed": False,
    }
    api_instance = get_clusters_api_instance(module)
    get_host_stats(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
