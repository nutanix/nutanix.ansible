#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
module: ntnx_object_stores_stats_info_v2
short_description: Get Object Store statistics
version_added: 2.6.0
description:
    - Fetch statistics of an object store for a given time window
    - This module uses PC v4 APIs based GA SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get the stats of an Object store) -
      Required Roles: Objects Admin, Objects Editor, Objects Viewer, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=objects)"
options:
    ext_id:
        description: External ID of the object store to fetch statistics for
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
"""

EXAMPLES = r"""
- name: Fetch object store statistics for the last hour
  nutanix.ncp.ntnx_object_stores_stats_info_v2:
    ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    start_time: "2025-05-04T10:30:10.000+00:00"
    end_time: "2025-05-04T11:30:10.000+00:00"
    sampling_interval: 300
    stat_type: "SUM"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching object store statistics
    type: dict
    returned: always
    sample:
        {
            "bucket_count": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 1
                }
            ],
            "delete_requests_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "ext_id": null,
            "get_bucket_operations_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "get_object_ttfb_msecs": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "get_request_throughput_bytes_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "get_requests_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "head_requests_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "inbound_bytes_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "links": null,
            "list_multipart_uploads_operations_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "multipart_upload_start_operations_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "nfs_read_requests_per_second": null,
            "nfs_read_throughput_bytes_per_second": null,
            "nfs_write_requests_per_second": null,
            "nfs_write_throughput_bytes_per_second": null,
            "object_count": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 138
                }
            ],
            "object_operations_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "outbound_bytes_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "post_requests_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "put_request_throughput_bytes_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "put_requests_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "select_object_content_operations_per_second": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 0.0
                }
            ],
            "storage_usage_bytes": [
                {
                    "timestamp": "2026-06-11T12:40:00+00:00",
                    "value": 2859830
                }
            ],
            "tenant_id": null
        }

ext_id:
    description: External ID of the object store
    returned: always
    type: str
    sample: "cda893b8-2aee-34bf-817d-d2ee6026790b"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching object store stats info"

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.objects.api_client import (  # noqa: E402
    get_objects_stats_api_instance,
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
            choices=["SUM", "MIN", "MAX", "AVG", "COUNT", "LAST"],
        ),
        select=dict(type="str"),
    )
    return module_args


def get_object_store_stats(module, stats_api, result):
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

    try:
        resp = stats_api.get_objectstore_stats_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store stats info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    stats_api = get_objects_stats_api_instance(module)
    get_object_store_stats(module, stats_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
