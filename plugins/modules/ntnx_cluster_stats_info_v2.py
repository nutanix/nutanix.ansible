#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_stats_info_v2
short_description: Retrieve ClusterStat information from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ClusterStat in Nutanix Prism Central.
  - Fetches performance statistics for a specific cluster identified by C(ext_id).
  - The Nutanix v4 ClusterStat API only supports single-cluster lookup, so C(ext_id) is required.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(View Cluster Stats) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin,
    Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the cluster.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - >-
        For example, start time of C(2022-04-23T01:23:45.678+09:00) would consider
        all stats starting at 1:23:45.678 on the 23rd of April 2022.
      - Details around ISO-8601 format can be found at U(https://www.iso.org/standard/70907.html)
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - >-
        For example, end time of C(2022-04-23T13:23:45.678+09:00) would consider
        all stats till 13:23:45.678 on the 23rd of April 2022.
      - Details around ISO-8601 format can be found at U(https://www.iso.org/standard/70907.html)
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
      - C(SUM) - Aggregation with sum of all values.
      - C(MIN) - Aggregation containing lowest of all values.
      - C(MAX) - Aggregation containing highest of all values.
      - C(AVG) - Aggregation indicating mean or average of all values.
      - C(COUNT) - Aggregation containing total count of values.
      - C(LAST) - Aggregation containing only the last recorded value.
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
      - A URL query parameter that allows clients to request a specific set of properties for each entity or complex type.
      - >-
        Expression specified with the C($select) must conform to the OData V4.01 URL conventions.
      - >-
        If a C($select) expression consists of a single select item that is an asterisk (i.e., *),
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
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch cluster stats info during a time interval
  nutanix.ncp.ntnx_cluster_stats_info_v2:
    ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-20T00:00:00Z"
  register: result

- name: Fetch cluster stats info with all attributes
  nutanix.ncp.ntnx_cluster_stats_info_v2:
    ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-20T00:00:00Z"
    sampling_interval: 30
    stat_type: "AVG"
    select: "hypervisorCpuUsagePpm,aggregateHypervisorMemoryUsagePpm"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ClusterStat info v4 API.
    - Returns the single ClusterStat identified by external ID (with its time-series metrics).
  returned: always
  type: dict
  sample:
    {
      "controller_avg_io_latency_usecs": [
        {"timestamp": "2026-07-19T00:00:30+00:00", "value": 1200}
      ],
      "hypervisor_cpu_usage_ppm": [
        {"timestamp": "2026-07-19T00:00:30+00:00", "value": 152340}
      ],
      "ext_id": "0006361b-6855-3644-7458-2268f8ffb2bd",
      "links": null,
      "tenant_id": null
    }

ext_id:
  description: External ID of the cluster whose statistics were fetched.
  type: str
  returned: always
  sample: "0006361b-6855-3644-7458-2268f8ffb2bd"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

failed:
  description: This field typically holds information about if the task has failed.
  returned: always
  type: bool
  sample: false

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching cluster stats using ext_id"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cluster_stats  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

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
            choices=["SUM", "MIN", "MAX", "AVG", "COUNT", "LAST"],
        ),
        select=dict(type="str"),
    )
    return module_args


def get_cluster_stat_by_ext_id(module, result, api_instance):
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

    resp = get_cluster_stats(module, api_instance, ext_id, **kwargs)
    if resp:
        result["response"] = strip_internal_attributes(resp.to_dict())
    else:
        module.fail_json(
            msg="Failed fetching cluster stats for ext_id: {0}".format(ext_id),
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
        "error": None,
        "response": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_clusters_api_instance(module)
    get_cluster_stat_by_ext_id(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
