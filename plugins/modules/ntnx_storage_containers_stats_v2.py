#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_storage_containers_stats_v2
short_description: Retrieve stats about Nutanix storage continer from PC
version_added: 2.0.0
description:
    - Get Stats for a Storage Container
options:
  ext_id:
    description:
      - The external ID of the storage continer.
    type: str
    required: true
  start_time:
    description:
        - The start time of the period for which stats should be reported.
        - The value should be in extended ISO-8601 format.
        - sample input time is 2024-07-31T12:41:56.955Z
    type: str
    required: true
  end_time:
    description:
        - The end time of the period for which stats should be reported.
        - The value should be in extended ISO-8601 format.
        - sample input time is 2025-07-31T12:41:56.955Z
    type: str
    required: true
  sampling_interval:
    description:
        - The sampling interval in seconds at which statistical data should be collected.
          For example, if you want performance statistics every 30 seconds, then provide the value as 30.
    type: int
    required: false
  stat_type:
    description:
        - The type of stats.
    type: str
    required: false
    choices:
        - SUM
        - AVG
        - MIN
        - MAX
        - COUNT
        - LAST
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Prem Karat (@premkarat)
 - Alaa Bishtawi (@alaabishtawi)
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch storage container stats during time interval
  nutanix.ncp.ntnx_storage_containers_stats_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
    start_time: 2024-07-31T12:41:56.955Z
    end_time: 2025-07-31T12:41:56.955Z
  register: result

- name: Fetch storage container stats with all attributes
  nutanix.ncp.ntnx_storage_containers_stats_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
    start_time: 2024-07-31T12:41:56.955Z
    end_time: 2025-07-31T12:41:56.955Z
    sampling_interval: 30
    stat_type: "SUM"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching storage container stats.
    type: dict
    returned: always
    sample:
            {
                    "container_ext_id": "547c01c4-19c2-4293-8a9c-43441c18d0c7",
                    "controller_avg_io_latencyu_secs": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 947
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 1061
                        }
                    ],
                    "controller_avg_read_io_latencyu_secs": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 797
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 832
                        }
                    ],
                    "controller_avg_write_io_latencyu_secs": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 2175
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 3182
                        }
                    ],
                    "controller_io_bandwidthk_bps": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 53450
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 51019
                        }
                    ],
                    "controller_num_iops": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 1247
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 1203
                        }
                    ],
                    "controller_num_read_iops": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 1110
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 1086
                        }
                    ],
                    "controller_num_write_iops": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 136
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 117
                        }
                    ],
                    "controller_read_io_bandwidthk_bps": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 52171
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 49956
                        }
                    ],
                    "controller_read_io_ratio_ppm": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 890744
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 902745
                        }
                    ],
                    "controller_write_io_bandwidthk_bps": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 1278
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 1062
                        }
                    ],
                    "controller_write_io_ratio_ppm": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 109255
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 97254
                        }
                    ],
                    "data_reduction_clone_saving_ratio_ppm": null,
                    "data_reduction_compression_saving_ratio_ppm": null,
                    "data_reduction_dedup_saving_ratio_ppm": null,
                    "data_reduction_erasure_coding_saving_ratio_ppm": null,
                    "data_reduction_overall_post_reduction_bytes": null,
                    "data_reduction_overall_pre_reduction_bytes": null,
                    "data_reduction_saved_bytes": null,
                    "data_reduction_saving_ratio_ppm": null,
                    "data_reduction_snapshot_saving_ratio_ppm": null,
                    "data_reduction_thin_provision_saving_ratio_ppm": null,
                    "data_reduction_total_saving_ratio_ppm": null,
                    "data_reduction_zero_write_savings_bytes": null,
                    "ext_id": null,
                    "health": null,
                    "links": null,
                    "storage_actual_physical_usage_bytes": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 139663605760
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 139659902976
                        }
                    ],
                    "storage_capacity_bytes": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 4138110191211
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 4138122024555
                        }
                    ],
                    "storage_free_bytes": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 3998446585451
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 3998462121579
                        }
                    ],
                    "storage_replication_factor": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 1
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 1
                        }
                    ],
                    "storage_reserved_capacity_bytes": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 0
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 0
                        }
                    ],
                    "storage_tier_das_sata_usage_bytes": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 0
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 0
                        }
                    ],
                    "storage_tier_ssd_usage_bytes": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 139663605760
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 139659902976
                        }
                    ],
                    "storage_usage_bytes": [
                        {
                            "timestamp": "2024-07-31T11:29:00+00:00",
                            "value": 139663605760
                        },
                        {
                            "timestamp": "2024-07-31T11:28:30+00:00",
                            "value": 139659902976
                        }
                    ]
        }
error:
    description: The error message if an error occurs.
    type: str
    returned: when an error occurs
ext_id:
    description:
        - The external ID of the storage container .
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_storage_containers_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

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
            choices=[
                "SUM",
                "AVG",
                "MIN",
                "MAX",
                "COUNT",
                "LAST",
            ],
        ),
    )

    return module_args


def get_storage_container_stats(module, result):
    storage_container = get_storage_containers_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")
    sampling_interval = module.params.get("sampling_interval")
    stat_type = module.params.get("stat_type")
    resp = None
    try:
        resp = storage_container.get_storage_container_stats(
            extId=ext_id,
            _startTime=start_time,
            _endTime=end_time,
            _samplingInterval=sampling_interval,
            _statType=stat_type,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching storage containers stats",
        )
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        module.fail_json(msg="Failed fetching storage container stats", **result)


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
    }
    get_storage_container_stats(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
