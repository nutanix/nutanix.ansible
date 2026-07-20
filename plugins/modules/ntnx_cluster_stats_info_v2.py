#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_stats_info_v2
short_description: Fetch information about ClusterStat in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about ClusterStat in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ClusterStat.
  - The Nutanix v4 API only exposes a per-cluster stats endpoint
    (C(GET /api/clustermgmt/v4.2/stats/clusters/{extId})); it does NOT expose a "list all
    cluster stats" operation, so C(ext_id) is always required.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get cluster statistics) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin, Storage Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the cluster whose statistics should be fetched.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which statistics should be reported.
      - Value must be in extended ISO-8601 format, e.g. C(2026-04-23T01:23:45.678+00:00) or
        C(2026-04-23T01:23:45Z).
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which statistics should be reported.
      - Value must be in extended ISO-8601 format, e.g. C(2026-04-23T13:23:45.678+00:00) or
        C(2026-04-23T13:23:45Z).
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval in seconds at which statistical data should be collected.
      - For example, C(30) returns performance statistics every 30 seconds.
    type: int
    required: false
  stat_type:
    description:
      - The down-sampling / aggregation operator applied over the requested time window.
      - Corresponds to the C($statType) OData query parameter on the underlying stats endpoint.
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
      - A comma-separated list of statistic properties to return, corresponding to the
        C($select) OData query parameter on the underlying stats endpoint.
      - Use C('*') to request all properties on the matching resource.
    type: str
    required: false
  read_timeout:
    description:
      - Read timeout in milliseconds for API calls.
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
- name: Fetch cluster statistics for a specific cluster
  nutanix.ncp.ntnx_cluster_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-20T00:00:00Z"
    sampling_interval: 30
    stat_type: "AVG"
    select: "hypervisorCpuUsagePpm,aggregateHypervisorMemoryUsagePpm"
  register: result
  ignore_errors: true

- name: Fetch all cluster statistic properties using select wildcard
  nutanix.ncp.ntnx_cluster_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-20T00:00:00Z"
    stat_type: "LAST"
    select: "*"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ClusterStat info v4 API.
    - It contains a single ClusterStat entity because the underlying API is per-cluster and
      the Nutanix v4 stats API does not support listing stats for multiple clusters in a
      single call, so C(ext_id) is required.
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

changed:
  description: This indicates whether the task resulted in any changes. Always C(false) for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching cluster stats using ext_id"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task has failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the cluster whose statistics were fetched.
  type: str
  returned: always
  sample: "0006361b-6855-3644-7458-2268f8ffb2bd"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cluster_stats  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

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
            choices=["SUM", "MIN", "MAX", "AVG", "COUNT", "LAST"],
        ),
        select=dict(type="str", required=False),
    )
    return module_args


def _build_stats_kwargs(module):
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


def get_cluster_stat_by_ext_id(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    kwargs = _build_stats_kwargs(module)
    resp = get_cluster_stats(module, api_instance, ext_id, kwargs)
    result["ext_id"] = ext_id
    data = getattr(resp, "data", None)
    if data is None:
        result["response"] = {}
        return
    result["response"] = strip_internal_attributes(data.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False, "error": None}
    api_instance = get_clusters_api_instance(module)
    get_cluster_stat_by_ext_id(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
