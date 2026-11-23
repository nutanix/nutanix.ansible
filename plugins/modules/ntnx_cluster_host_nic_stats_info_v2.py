#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_host_nic_stats_info_v2
short_description: Fetch host NIC stats info in Nutanix Prism Central
version_added: "2.7.0"
description:
  - This module allows you to fetch information about HostNicStats in Nutanix Prism Central.
  - List host NIC stats for a given host and cluster with required start and end time.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(View Host Nic Stats) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin,
    Prism Viewer, Project Manager, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster that owns the host.
    type: str
    required: true
  host_ext_id:
    description:
      - The external ID (UUID) of the host that owns the host NICs.
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
    type: str
    choices:
      - SUM
      - MIN
      - MAX
      - AVG
      - COUNT
      - LAST
  filter:
    description:
      - Filter for host NIC stats list.
    type: str
  orderby:
    description:
      - Ordering for host NIC stats list.
    type: str
  select:
    description:
      - Select fields for host NIC stats list.
    type: str
  page:
    description:
      - Page number for pagination.
    type: int
  limit:
    description:
      - Limit for pagination.
    type: int
  fetch_all:
    description:
      - Fetch all records without pagination.
    type: bool
    default: false
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
- name: List host NIC stats for a host
  nutanix.ncp.ntnx_cluster_host_nic_stats_info_v2:
    cluster_ext_id: "0005b3f7-1234-4321-abcd-0123456789ab"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2024-08-01T12:41:56.955Z"
  register: result
  ignore_errors: true

- name: List host NIC stats with filter
  nutanix.ncp.ntnx_cluster_host_nic_stats_info_v2:
    cluster_ext_id: "0005b3f7-1234-4321-abcd-0123456789ab"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2024-08-01T12:41:56.955Z"
    filter: "extId eq 'd6e2eec2-8d68-4b9c-a3f5-cfc9f9b7a821'"
  register: result
  ignore_errors: true

- name: List host NIC stats with limit
  nutanix.ncp.ntnx_cluster_host_nic_stats_info_v2:
    cluster_ext_id: "0005b3f7-1234-4321-abcd-0123456789ab"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2024-08-01T12:41:56.955Z"
    limit: 1
  register: result
  ignore_errors: true

- name: List host NIC stats with fetch_all
  nutanix.ncp.ntnx_cluster_host_nic_stats_info_v2:
    cluster_ext_id: "0005b3f7-1234-4321-abcd-0123456789ab"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    start_time: "2024-07-31T12:41:56.955Z"
    end_time: "2024-08-01T12:41:56.955Z"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC HostNicStats info v4 API.
    - List of multiple HostNicStats with optional filter, limit, or fetch_all.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "d6e2eec2-8d68-4b9c-a3f5-cfc9f9b7a821",
        "links": null,
        "received_bytes": [
            {"timestamp": "2026-07-20T13:12:00+00:00", "value": 12345}
        ],
        "received_rate_kbps": [
            {"timestamp": "2026-07-20T13:12:00+00:00", "value": 100}
        ],
        "tenant_id": null,
        "transmitted_bytes": [
            {"timestamp": "2026-07-20T13:12:00+00:00", "value": 54321}
        ]
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
  sample: "Api Exception raised while fetching host NIC stats info"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs
failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
total_available_results:
  description: The total number of available host NIC stats matching the query.
  type: int
  returned: When a list call is made.
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        host_ext_id=dict(type="str", required=True),
        start_time=dict(type="str", required=True),
        end_time=dict(type="str", required=True),
        sampling_interval=dict(type="int"),
        stat_type=dict(
            type="str", choices=["SUM", "MIN", "MAX", "AVG", "COUNT", "LAST"]
        ),
        filter=dict(type="str"),
        orderby=dict(type="str"),
        select=dict(type="str"),
        page=dict(type="int"),
        limit=dict(type="int"),
        fetch_all=dict(type="bool", default=False),
    )
    return module_args


def get_host_nic_stats_list(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating host NIC stats info spec", **result)

    # Add required stats params
    kwargs["_startTime"] = module.params.get("start_time")
    kwargs["_endTime"] = module.params.get("end_time")
    if module.params.get("sampling_interval") is not None:
        kwargs["_samplingInterval"] = module.params.get("sampling_interval")
    if module.params.get("stat_type") is not None:
        kwargs["_statType"] = module.params.get("stat_type")

    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")

    try:
        resp = list_entities(
            api_instance.list_host_nic_stats_by_host_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
            hostExtId=host_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching host NIC stats info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    data = resp.get("data") or []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    get_host_nic_stats_list(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
