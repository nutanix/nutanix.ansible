#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_host_stat_v2
short_description: Retrieve host statistics from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch time-series performance and capacity statistics
    for a specific host within a cluster registered to Nutanix Prism Central.
  - The stats endpoint is read-only, so this module performs no create, update or
    delete operations - it only reports the statistics returned by the underlying
    C(GetHostStats) v4 API.
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
      - The external ID (UUID) of the cluster the host belongs to.
    type: str
    required: true
  ext_id:
    description:
      - The external ID (UUID) of the host whose statistics are being fetched.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value must be in extended ISO-8601 format.
      - For example C(2026-07-19T00:00:00Z).
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value must be in extended ISO-8601 format.
      - For example C(2026-07-20T00:00:00Z).
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval in seconds at which statistical data should be collected.
      - For example, provide C(30) to get one data point every 30 seconds.
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
      - Supply a comma-separated list of C(HostStatsProjection) field names.
      - Provide C(*) to explicitly request all fields.
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
- name: Fetch host stats for a specific host
  nutanix.ncp.ntnx_host_stat_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006c9d0-abcd-1234-5678-0242ac110002"
    ext_id: "d7f28e12-cafe-babe-0000-1a2b3c4d5e6f"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-20T00:00:00Z"
  register: result

- name: Fetch host stats with all optional attributes
  nutanix.ncp.ntnx_host_stat_v2:
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
    select: "controllerNumIops,hypervisorCpuUsagePpm,overallMemoryUsagePpm"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for fetching host statistics.
    - Contains time-series arrays of C(TimeValuePair) objects for each requested metric.
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
  description: The external ID of the host whose statistics were fetched.
  returned: always
  type: str
  sample: "d7f28e12-cafe-babe-0000-1a2b3c4d5e6f"

changed:
  description: Always C(false) - this module only reads statistics.
  returned: always
  type: bool
  sample: false

skipped:
  description: Whether the operation was skipped.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or an informational message
  type: str
  sample: "Api Exception raised while fetching host stats"

error:
  description: The error message if an error occurs.
  returned: When an error occurs
  type: str

failed:
  description: Whether the module failed.
  returned: always
  type: bool
  sample: false

task_ext_id:
  description:
    - The external ID of the task.
    - Always C(null) for this stats module - the underlying API is synchronous and does not create a task.
  returned: always
  type: str
  sample: null
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


def get_HostStat(module, result, api_instance):
    """Fetch host stats for a single host and populate ``result``.

    This is a read-only operation - the SDK's ``get_host_stats`` endpoint has no
    counterpart create/update/delete methods, so ``changed`` is always
    ``False`` and no task is produced by the API.
    """
    validate_required_params(
        module, ["cluster_ext_id", "ext_id", "start_time", "end_time"]
    )

    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")
    sampling_interval = module.params.get("sampling_interval")
    stat_type = module.params.get("stat_type")
    select = module.params.get("select")

    result["cluster_ext_id"] = cluster_ext_id
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Host stats for host ext_id:{0} in cluster ext_id:{1} would be fetched "
            "for the window {2} -> {3}."
        ).format(ext_id, cluster_ext_id, start_time, end_time)
        return

    kwargs = {}
    if sampling_interval is not None:
        kwargs["_samplingInterval"] = sampling_interval
    if stat_type is not None:
        kwargs["_statType"] = stat_type
    if select is not None:
        kwargs["_select"] = select

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
            msg="Api Exception raised while fetching host stats",
        )

    if getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = None
        module.fail_json(
            msg=(
                "Failed to fetch host stats: response contained no data for host "
                "ext_id:{0} in cluster ext_id:{1}."
            ).format(ext_id, cluster_ext_id),
            **result,
        )


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
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
        "error": None,
        "failed": False,
        "skipped": False,
        "cluster_ext_id": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_clusters_api_instance(module)
    get_HostStat(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
