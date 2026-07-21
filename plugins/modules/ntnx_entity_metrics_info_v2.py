#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_entity_metrics_info_v2
short_description: Fetch AIOps EntityMetricsV4 info from Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about EntityMetricsV4 in Nutanix Prism Central.
  - Backs the v4 AIOps StatsApi C(getEntityMetricsV4) API
    (C(GET /api/aiops/v4.2.b1/stats/sources/{sourceExtId}/entities/{extId})).
  - Both C(source_ext_id) and C(ext_id) are required — the underlying API only
    supports fetching metrics for a specific entity type of a specific source.
  - Returned data is a paginated list of entities with attribute values and
    time-series metric samples for the requested time window.
  - This module uses PC v4 APIs based SDKs (ntnx_aiops_py_client).
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get EntityMetricsV4 for an entity type) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, Intelligent Ops Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  source_ext_id:
    description:
      - The UUID of the AIOps data source (e.g. C(nutanix), C(nutanix_vcenter)).
    type: str
    required: true
  ext_id:
    description:
      - The UUID of the entity type whose metrics/attributes to fetch
        (e.g. C(vm), C(cluster), C(node), C(disk)).
    type: str
    required: true
  start_time:
    description:
      - Start time of the reporting window in extended ISO-8601 format.
      - Example C(2026-07-21T09:00:00.000Z).
    type: str
    required: true
  end_time:
    description:
      - End time of the reporting window in extended ISO-8601 format.
      - Example C(2026-07-21T10:00:00.000Z).
    type: str
    required: true
  sampling_interval:
    description:
      - Sampling interval in seconds at which statistical data is aggregated.
    type: int
    required: false
  stat_type:
    description:
      - Downsampling operator used when aggregating stats over
        C(sampling_interval).
    type: str
    required: false
    choices:
      - SUM
      - MIN
      - MAX
      - AVG
      - COUNT
      - LAST
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get VM metrics info for the last hour (paginated)
  nutanix.ncp.ntnx_entity_metrics_info_v2:
    source_ext_id: "nutanix"
    ext_id: "vm"
    start_time: "2026-07-21T08:00:00.000Z"
    end_time: "2026-07-21T09:00:00.000Z"
    limit: 5
  register: vm_metrics_info

- name: Get cluster metrics info with 60s SUM downsampling
  nutanix.ncp.ntnx_entity_metrics_info_v2:
    source_ext_id: "nutanix"
    ext_id: "cluster"
    start_time: "2026-07-21T08:00:00.000Z"
    end_time: "2026-07-21T09:00:00.000Z"
    sampling_interval: 60
    stat_type: "SUM"
  register: cluster_metrics_info

- name: Get first 3 sorted VM metric entries
  nutanix.ncp.ntnx_entity_metrics_info_v2:
    source_ext_id: "nutanix"
    ext_id: "vm"
    start_time: "2026-07-21T08:00:00.000Z"
    end_time: "2026-07-21T09:00:00.000Z"
    limit: 3
    orderby: "extId asc"
  register: sorted_vm_metrics
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC EntityMetricsV4 info v4 API.
    - A list of EntityMetricsV4 entries (attribute values + time-series metric
      samples) for the entity type identified by C(ext_id) within the given
      source. The list is paginated using C(page) / C(limit).
  returned: always
  type: list
  elements: dict
  sample:
    - entity_type: "cluster"
      ext_id: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
      links: null
      parents: null
      source: "nutanix"
      tenant_id: null
      metrics:
          - name: "extId"
            time_series:
                sampling_interval_secs: null
                values:
                    - timestamp: "2026-06-30T16:42:01+00:00"
                      value:
                          str_value: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"

changed:
  description: This indicates whether the task resulted in any changes.
    Info modules always return false.
  returned: always
  type: bool
  sample: false

total_available_results:
  description: Total available results across all pages of the query.
  returned: always
  type: int
  sample: 12

source_ext_id:
  description: AIOps data source UUID used for the request.
  returned: always
  type: str
  sample: "db293e8a-5770-c3c7-4213-85dbbc1d3679"

ext_id:
  description: Entity type UUID used for the request.
  returned: always
  type: str
  sample: "06b2d4b9-1b5c-9eaa-8c20-a1c270f95b3c"

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching AIOps entity metrics info"

error:
  description: This field holds information about any errors that occurred during execution.
  type: str
  returned: when an error occurs

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import get_stats_api_instance  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        source_ext_id=dict(type="str", required=True),
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


def get_entity_metrics_info(module, api_instance, result):
    validate_required_params(
        module, ["source_ext_id", "ext_id", "start_time", "end_time"]
    )

    source_ext_id = module.params.get("source_ext_id")
    ext_id = module.params.get("ext_id")
    result["source_ext_id"] = source_ext_id
    result["ext_id"] = ext_id

    kwargs = dict(
        sourceExtId=source_ext_id,
        extId=ext_id,
        _startTime=module.params.get("start_time"),
        _endTime=module.params.get("end_time"),
    )

    optional_kwargs = {
        "_page": module.params.get("page"),
        "_limit": module.params.get("limit"),
        "_samplingInterval": module.params.get("sampling_interval"),
        "_statType": module.params.get("stat_type"),
        "_filter": module.params.get("filter"),
        "_orderby": module.params.get("orderby"),
    }
    for key, value in optional_kwargs.items():
        if value is not None:
            kwargs[key] = value

    try:
        resp = api_instance.get_entity_metrics_v4(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching AIOps entity metrics info",
        )

    total_available_results = 0
    if getattr(resp, "metadata", None) is not None:
        total_available_results = (
            getattr(resp.metadata, "total_available_results", 0) or 0
        )
    result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "source_ext_id": None,
        "ext_id": None,
        "total_available_results": 0,
        "failed": False,
    }
    api_instance = get_stats_api_instance(module)
    get_entity_metrics_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
