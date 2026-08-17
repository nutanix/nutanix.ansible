#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_stat_v2
short_description: Fetch cluster performance and capacity statistics from Nutanix Prism Central
version_added: 2.5.0
description:
  - This module fetches performance and capacity statistics for a specific cluster in Nutanix Prism Central.
  - The C(ClusterStat) entity in the C(cluster_management) namespace is read-only in the v4 API - the SDK
    only exposes a single Get operation (C(GET /api/clustermgmt/v4.2/stats/clusters/{extId})), there is no
    Create, Update or Delete for cluster statistics. This module therefore only supports C(state=present)
    to fetch stats; setting C(state=absent) is rejected with a descriptive error.
  - Metrics returned include controller latency and IOPS, hypervisor CPU/memory usage, storage capacity
    and savings, IO bandwidth, and power consumption over the requested time window.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get cluster statistics) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin, Storage Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present), the module will fetch cluster statistics for the given C(ext_id).
      - C(state=absent) is not supported for this entity because the v4 API does not expose a delete
        operation for cluster stats; supplying it will cause the module to fail with a descriptive error.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the cluster whose statistics should be fetched.
      - Required for fetching cluster statistics.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which statistics should be reported.
      - Value must be in extended ISO-8601 format, e.g. C(2026-04-23T01:23:45.678+00:00) or
        C(2026-04-23T01:23:45Z).
      - Required when C(state=present).
    type: str
    required: false
  end_time:
    description:
      - The end time of the period for which statistics should be reported.
      - Value must be in extended ISO-8601 format, e.g. C(2026-04-23T13:23:45.678+00:00) or
        C(2026-04-23T13:23:45Z).
      - Required when C(state=present).
    type: str
    required: false
  sampling_interval:
    description:
      - The sampling interval in seconds at which statistical data should be collected.
      - For example, C(30) returns performance statistics every 30 seconds.
      - Optional, controlled by the caller depending on the desired time-resolution.
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
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch cluster statistics with averaged aggregation
  nutanix.ncp.ntnx_cluster_stat_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-20T00:00:00Z"
    sampling_interval: 30
    stat_type: "AVG"
    select: "hypervisorCpuUsagePpm,aggregateHypervisorMemoryUsagePpm,ioBandwidthKbps"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for fetching cluster statistics.
    - Contains the ClusterStats entity with time-series values for the requested metrics.
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

task_ext_id:
  description:
    - The external ID of the task.
    - This field is always C(null) for cluster stats since the underlying API is synchronous
      and does not create a task; it is kept for parity with other v2 modules.
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID (UUID) of the cluster whose statistics were fetched.
  returned: always
  type: str
  sample: "0006361b-6855-3644-7458-2268f8ffb2bd"

changed:
  description: This indicates whether the task resulted in any changes. Always C(false) for stats fetches.
  returned: always
  type: bool
  sample: false

skipped:
  description: This indicates whether the task was skipped.
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while fetching cluster stats using ext_id"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cluster_stats  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    # pylint: disable=unused-import
    # The SDK import is verified here (not used directly) so we can surface a
    # clear "install ntnx_clustermgmt_py_client" error to the user instead of a
    # cryptic ImportError originating deep inside api_client.
    import ntnx_clustermgmt_py_client  # noqa: F401
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        start_time=dict(type="str", required=False),
        end_time=dict(type="str", required=False),
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
    """Build the kwargs dict passed to ClustersApi.get_cluster_stats.

    The SDK accepts a set of OData-style query parameters. We only include
    parameters the user actually specified so we don't override server-side
    defaults with ``None``.
    """
    kwargs = {
        "_startTime": module.params.get("start_time"),
        "_endTime": module.params.get("end_time"),
    }
    sampling_interval = module.params.get("sampling_interval")
    if sampling_interval is not None:
        kwargs["_samplingInterval"] = sampling_interval
    stat_type = module.params.get("stat_type")
    if stat_type is not None:
        kwargs["_statType"] = stat_type
    select = module.params.get("select")
    if select is not None:
        kwargs["_select"] = select
    return kwargs


def fetch_cluster_stat(module, result, api_instance):
    """Fetch statistics for the cluster identified by ``ext_id``."""
    validate_required_params(module, ["ext_id", "start_time", "end_time"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Cluster stats will be fetched for cluster with ext_id:{0}".format(ext_id)
        )
        return

    kwargs = _build_stats_kwargs(module)
    resp = get_cluster_stats(module, api_instance, ext_id, kwargs)
    data = getattr(resp, "data", None)
    if data is None:
        result["response"] = {}
        result["msg"] = (
            "Cluster stats response contained no data for ext_id:{0}".format(ext_id)
        )
        return
    result["response"] = strip_internal_attributes(data.to_dict())


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("start_time", "end_time")),
        ],
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
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }

    state = module.params.get("state")
    if state == "absent":
        module.fail_json(
            msg=(
                "state=absent is not supported for ClusterStat: the Nutanix v4 cluster "
                "management API does not expose a delete operation for cluster stats."
            ),
            **result,
        )

    api_instance = get_clusters_api_instance(module)
    fetch_cluster_stat(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
