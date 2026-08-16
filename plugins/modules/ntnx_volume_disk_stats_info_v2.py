#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_disk_stats_info_v2
short_description: Fetch statistics for a Volume Disk of a Volume Group in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about VolumeDiskStat in Nutanix Prism Central.
  - VolumeDiskStat is the time-series performance data (IOPS, bandwidth, latency)
    of a Volume Disk that belongs to a Volume Group.
  - Because the statistics are always scoped to a specific disk of a specific
    Volume Group, both C(volume_group_ext_id) and C(ext_id) are required.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Get statistics for a Volume Disk) -
      Required Roles: CSI System, Disaster Recovery Admin, Disaster Recovery Viewer,
      Kubernetes Data Services System, Prism Admin, Prism Viewer, Project Manager,
      Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  volume_group_ext_id:
    description:
      - The external identifier (UUID) of the Volume Group that owns the disk.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier (UUID) of the Volume Disk to fetch statistics for.
    type: str
    required: true
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - Sample input time is C(2025-07-31T12:41:56.955Z).
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format.
      - Sample input time is C(2025-07-31T13:41:56.955Z).
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval in seconds at which statistical data should be collected.
      - For example, to obtain performance statistics every 30 seconds, set to C(30).
      - When omitted, the platform picks a default interval so that at most
        100 samples are returned (minimum interval is 30 seconds).
    type: int
    required: false
  stat_type:
    description:
      - The down-sampling operator to apply on the raw statistical data.
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
      - An OData V4.01 conformant C($select) query parameter that lets the client
        request a specific subset of properties per entity.
      - Use C(*) to return all properties (equivalent to omitting the parameter).
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
- name: Fetch volume disk stats for a fixed window
  nutanix.ncp.ntnx_volume_disk_stats_info_v2:
    volume_group_ext_id: "530567f3-abda-4913-b5d0-0ab6758ec165"
    ext_id: "4e00e28d-4d93-4587-a8f0-4502d72224c8"
    start_time: "2025-07-31T12:41:56.955Z"
    end_time: "2025-07-31T13:41:56.955Z"
  register: result

- name: Fetch volume disk stats with sampling interval, stat_type and $select
  nutanix.ncp.ntnx_volume_disk_stats_info_v2:
    volume_group_ext_id: "530567f3-abda-4913-b5d0-0ab6758ec165"
    ext_id: "4e00e28d-4d93-4587-a8f0-4502d72224c8"
    start_time: "2025-07-31T12:41:56.955Z"
    end_time: "2025-07-31T13:41:56.955Z"
    sampling_interval: 30
    stat_type: "AVG"
    select: "*"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VolumeDiskStat info v4 API.
    - It contains the time-series statistics for the requested Volume Disk.
  returned: always
  type: dict
  sample:
    {
      "controller_avg_io_latency_usecs": [
        {"timestamp": "2025-07-31T12:41:56.955000+00:00", "value": 0}
      ],
      "controller_avg_read_io_latency_usecs": [
        {"timestamp": "2025-07-31T12:41:56.955000+00:00", "value": 0}
      ],
      "controller_avg_write_io_latency_usecs": [
        {"timestamp": "2025-07-31T12:41:56.955000+00:00", "value": 0}
      ],
      "controller_io_bandwidth_k_bps": [
        {"timestamp": "2025-07-31T12:41:56.955000+00:00", "value": 0}
      ],
      "controller_num_iops": [
        {"timestamp": "2025-07-31T12:41:56.955000+00:00", "value": 0}
      ],
      "controller_num_read_iops": [
        {"timestamp": "2025-07-31T12:41:56.955000+00:00", "value": 0}
      ],
      "controller_num_write_iops": [
        {"timestamp": "2025-07-31T12:41:56.955000+00:00", "value": 0}
      ],
      "controller_read_io_bandwidth_k_bps": [
        {"timestamp": "2025-07-31T12:41:56.955000+00:00", "value": 0}
      ],
      "controller_user_bytes": [
        {"timestamp": "2025-07-31T12:41:56.955000+00:00", "value": 0}
      ],
      "controller_write_io_bandwidth_k_bps": [
        {"timestamp": "2025-07-31T12:41:56.955000+00:00", "value": 0}
      ],
      "ext_id": "4e00e28d-4d93-4587-a8f0-4502d72224c8",
      "links": null,
      "tenant_id": null,
      "volume_disk_ext_id": "4e00e28d-4d93-4587-a8f0-4502d72224c8"
    }
volume_group_ext_id:
  description: The external ID of the Volume Group whose disk stats were fetched.
  returned: always
  type: str
  sample: "530567f3-abda-4913-b5d0-0ab6758ec165"
ext_id:
  description: The external ID of the Volume Disk whose stats were fetched.
  returned: always
  type: str
  sample: "4e00e28d-4d93-4587-a8f0-4502d72224c8"
changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false
failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
error:
  description: The error message if any error occurred while fetching the volume disk stats.
  returned: when an error occurs
  type: str
msg:
  description: The status/error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching volume disk stats"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import get_vg_api_instance  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
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


def get_volume_disk_stats(module, api_instance, result):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_stats_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating volume disk stats spec", **result)

    if module.params.get("select") is not None:
        kwargs["_select"] = module.params.get("select")

    resp = None
    try:
        resp = api_instance.get_volume_disk_stats(
            volumeGroupExtId=volume_group_ext_id,
            extId=ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching volume disk stats",
        )

    if getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        module.fail_json(msg="Failed fetching volume disk stats", **result)


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
        "failed": False,
        "ext_id": None,
        "volume_group_ext_id": None,
    }
    api_instance = get_vg_api_instance(module)
    get_volume_disk_stats(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
