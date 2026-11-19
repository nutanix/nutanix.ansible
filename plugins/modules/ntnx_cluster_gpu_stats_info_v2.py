#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_gpu_stats_info_v2
short_description: Fetch GPU stats info
version_added: "2.7.0"
description:
  - This module allows you to fetch GPU statistics for a host in a cluster.
  - Requires cluster, host and GPU external IDs along with start and end time.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View GPU Stats) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster.
    type: str
    required: true
  host_ext_id:
    description:
      - The external ID (UUID) of the host.
    type: str
    required: true
  ext_id:
    description:
      - The external ID (UUID) of the GPU.
    type: str
    required: true
  start_time:
    description:
      - The start time for stats query in ISO-8601 format.
    type: str
    required: true
  end_time:
    description:
      - The end time for stats query in ISO-8601 format.
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval in seconds.
    type: int
    required: false
  stat_type:
    description:
      - The stat type.
    type: str
    required: false
  select:
    description:
      - Select clause for query.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch GPU stats
  nutanix.ncp.ntnx_cluster_gpu_stats_info_v2:
    cluster_ext_id: "0005b3f7-1234-4321-abcd-0123456789ab"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    ext_id: "d6e2eec2-8d68-4b9c-a3f5-cfc9f9b7a821"
    start_time: "2024-01-01T00:00:00.000Z"
    end_time: "2024-01-01T01:00:00.000Z"
    sampling_interval: 30
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC GPU stats info v4 API.
    - GPU statistics details.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "d6e2eec2-8d68-4b9c-a3f5-cfc9f9b7a821",
        "gpu_usage_ppm": [
            {
                "timestamp": "2024-01-01T00:00:00.000Z",
                "value": 12345
            }
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
  sample: "Api Exception raised while fetching GPU stats"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs
failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
ext_id:
  description: External ID of the GPU.
  type: str
  returned: When external ID is provided
  sample: "d6e2eec2-8d68-4b9c-a3f5-cfc9f9b7a821"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_pcie_devices_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        host_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        start_time=dict(type="str", required=True),
        end_time=dict(type="str", required=True),
        sampling_interval=dict(type="int"),
        stat_type=dict(type="str"),
        select=dict(type="str"),
    )
    return module_args


def get_gpu_stats(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")
    ext_id = module.params.get("ext_id")
    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")
    sampling_interval = module.params.get("sampling_interval")
    stat_type = module.params.get("stat_type")
    select = module.params.get("select")
    kwargs = {}
    if sampling_interval is not None:
        kwargs["_samplingInterval"] = sampling_interval
    if stat_type:
        kwargs["_statType"] = stat_type
    if select:
        kwargs["_select"] = select
    try:
        resp = api_instance.get_gpu_stats(
            clusterExtId=cluster_ext_id,
            hostExtId=host_ext_id,
            extId=ext_id,
            _startTime=start_time,
            _endTime=end_time,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching GPU stats",
        )
    result["ext_id"] = ext_id
    result["response"] = (
        strip_internal_attributes(resp.data.to_dict()) if resp.data else {}
    )


def run_module():
    module = BaseInfoModule(argument_spec=get_module_spec(), supports_check_mode=False)
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "failed": False}
    api_instance = get_pcie_devices_api_instance(module)
    get_gpu_stats(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
