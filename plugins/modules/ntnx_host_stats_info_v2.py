#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_host_stats_info_v2
short_description: Fetch host statistics info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about HostStat in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific HostStat for that host.
  - If C(ext_id) is not provided, list HostStat for every host in the supplied
    C(cluster_ext_id). Server-side filter / limit / orderby / page are NOT supported
    by the underlying C(GetHostStats) v4 API, so those options are intentionally
    absent from this module.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Get Host Stats) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster the host(s) belong to.
    type: str
    required: true
  ext_id:
    description:
      - The external ID (UUID) of the host whose statistics are being fetched.
      - When omitted, the module fetches stats for every host in C(cluster_ext_id).
    type: str
    required: false
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value must be in extended ISO-8601 format.
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value must be in extended ISO-8601 format.
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval in seconds at which statistical data should be collected.
    type: int
    required: false
  stat_type:
    description:
      - The down-sampling operator applied when aggregating stats across the sampling interval.
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
      - OData V4.01 C($select) query parameter used to restrict the returned properties.
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
- name: Fetch stats for a single host using ext_id
  nutanix.ncp.ntnx_host_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006c9d0-abcd-1234-5678-0242ac110002"
    ext_id: "d7f28e12-cafe-babe-0000-1a2b3c4d5e6f"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-20T00:00:00Z"
  register: single_host

- name: Fetch stats for a single host with all optional attributes
  nutanix.ncp.ntnx_host_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006c9d0-abcd-1234-5678-0242ac110002"
    ext_id: "d7f28e12-cafe-babe-0000-1a2b3c4d5e6f"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-20T00:00:00Z"
    sampling_interval: 30
    stat_type: "AVG"
    select: "controllerNumIops,hypervisorCpuUsagePpm"
  register: single_host_full

- name: Fetch stats for every host in a cluster
  nutanix.ncp.ntnx_host_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006c9d0-abcd-1234-5678-0242ac110002"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-20T00:00:00Z"
    sampling_interval: 60
    stat_type: "AVG"
  register: cluster_hosts
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC HostStat info v4 API.
    - It can be a single HostStat if external ID is provided.
    - List of multiple HostStat (one entry per host in the cluster) if external ID is not provided.
    - Filter / limit / orderby / page are NOT supported by the underlying stats endpoint.
  returned: always
  type: dict
  sample:
    {
      "controller_num_iops": [
          {"timestamp": "2026-07-19T00:00:00+00:00", "value": 128}
      ],
      "hypervisor_cpu_usage_ppm": [
          {"timestamp": "2026-07-19T00:00:00+00:00", "value": 132456}
      ],
      "overall_memory_usage_ppm": [
          {"timestamp": "2026-07-19T00:00:00+00:00", "value": 654321}
      ],
      "ext_id": "d7f28e12-cafe-babe-0000-1a2b3c4d5e6f",
      "links": null,
      "tenant_id": null
    }

cluster_ext_id:
  description: The external ID of the cluster the stats were fetched from.
  returned: always
  type: str
  sample: "0006c9d0-abcd-1234-5678-0242ac110002"

ext_id:
  description: External ID of the host.
  returned: when external ID is provided
  type: str
  sample: "d7f28e12-cafe-babe-0000-1a2b3c4d5e6f"

total_available_results:
  description: The number of hosts that stats were fetched for.
  returned: when external ID is not provided
  type: int
  sample: 3

changed:
  description: Always C(false) for this info module.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching host stats info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    # Imported so we can surface a helpful missing-SDK error to the caller;
    # the API instance itself is built via get_clusters_api_instance().
    import ntnx_clustermgmt_py_client  # noqa: F401  pylint: disable=unused-import
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
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
    """Build the kwargs dict for a ``get_host_stats`` call."""
    kwargs = {}
    sampling_interval = module.params.get("sampling_interval")
    stat_type = module.params.get("stat_type")
    select = module.params.get("select")
    if sampling_interval is not None:
        kwargs["_samplingInterval"] = sampling_interval
    if stat_type is not None:
        kwargs["_statType"] = stat_type
    if select is not None:
        kwargs["_select"] = select
    return kwargs


def get_host_stats_using_ext_id(module, api_instance, result):
    """Fetch stats for a single host and populate ``result``."""
    validate_required_params(
        module, ["cluster_ext_id", "ext_id", "start_time", "end_time"]
    )

    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")

    result["cluster_ext_id"] = cluster_ext_id
    result["ext_id"] = ext_id

    kwargs = _build_stats_kwargs(module)

    resp = None
    try:
        resp = api_instance.get_host_stats(
            clusterExtId=cluster_ext_id,
            extId=ext_id,
            _startTime=start_time,
            _endTime=end_time,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching host stats info",
        )

    if getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = None
        module.fail_json(
            msg=(
                "Failed to fetch host stats info: response contained no data for host "
                "ext_id:{0} in cluster ext_id:{1}."
            ).format(ext_id, cluster_ext_id),
            **result,
        )


def get_host_stats_for_cluster(module, api_instance, result):
    """List all hosts in the cluster and fetch stats for each one."""
    validate_required_params(module, ["cluster_ext_id", "start_time", "end_time"])

    cluster_ext_id = module.params.get("cluster_ext_id")
    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")

    result["cluster_ext_id"] = cluster_ext_id

    hosts_resp = None
    try:
        hosts_resp = api_instance.list_hosts_by_cluster_id(clusterExtId=cluster_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while listing hosts in cluster "
                "ext_id:{0} for host stats info"
            ).format(cluster_ext_id),
        )

    hosts_dict = strip_internal_attributes(hosts_resp.to_dict())
    hosts = hosts_dict.get("data") or []

    kwargs = _build_stats_kwargs(module)

    stats_list = []
    for host in hosts:
        host_ext_id = host.get("ext_id")
        if not host_ext_id:
            continue
        try:
            host_stats_resp = api_instance.get_host_stats(
                clusterExtId=cluster_ext_id,
                extId=host_ext_id,
                _startTime=start_time,
                _endTime=end_time,
                **kwargs,
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg=(
                    "Api Exception raised while fetching host stats info for host "
                    "ext_id:{0} in cluster ext_id:{1}"
                ).format(host_ext_id, cluster_ext_id),
            )
        if getattr(host_stats_resp, "data", None) is not None:
            stats_list.append(
                strip_internal_attributes(host_stats_resp.to_dict()).get("data")
            )

    result["total_available_results"] = len(stats_list)
    result["response"] = stats_list


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "cluster_ext_id": None,
    }
    api_instance = get_clusters_api_instance(module)
    if module.params.get("ext_id"):
        get_host_stats_using_ext_id(module, api_instance, result)
    else:
        get_host_stats_for_cluster(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
