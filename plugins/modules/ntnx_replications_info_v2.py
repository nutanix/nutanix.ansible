#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_replications_info_v2
short_description: Fetch Nutanix Files replication jobs info from Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about Replication in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Replication.
  - If C(ext_id) is not provided, list multiple Replication optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get replication job by ext_id / List replication jobs) -
    Required Roles: Prism Admin, Super Admin, Prism Viewer
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external ID of the replication job.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get replication job details using external ID
  nutanix.ncp.ntnx_replications_info_v2:
    ext_id: "6f6c5e75-bd80-4d5a-9d3f-7a1f7f9a4d90"
  register: result
  ignore_errors: true

- name: List all replication jobs
  nutanix.ncp.ntnx_replications_info_v2:
  register: result
  ignore_errors: true

- name: List replication jobs filtered by status
  nutanix.ncp.ntnx_replications_info_v2:
    filter: "status eq Files.Config.JobStatus'SUCCEEDED'"
  register: result
  ignore_errors: true

- name: List replication jobs with limit and ordering
  nutanix.ncp.ntnx_replications_info_v2:
    limit: 5
    orderby: "startTime desc"
  register: result
  ignore_errors: true

- name: List replication jobs and select specific fields
  nutanix.ncp.ntnx_replications_info_v2:
    select: "extId,status,progressPercentage,startTime,endTime"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Replication info v4 API.
    - It can be a single Replication if external ID is provided.
    - List of multiple Replication if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "average_throughput_bps": 0,
      "bytes_transferred": 0,
      "end_time": "2026-07-21T06:26:51.524581+00:00",
      "estimated_bytes": 0,
      "ext_id": "6f6c5e75-bd80-4d5a-9d3f-7a1f7f9a4d90",
      "is_delete_propagation_enabled": false,
      "links": null,
      "number_of_estimated_files": 0,
      "number_of_files_failed": 0,
      "number_of_files_transferred": 0,
      "policy_ext_id": "9c1e537d-6777-4c22-5d41-ddd0c3337aa9",
      "progress_percentage": 100,
      "replication_summary": null,
      "source_file_server_ext_id": "b39d3fa0-3f2c-4c07-9e10-51e7b3f5b4a1",
      "source_mount_target_ext_id": "1a2b3c4d-3f2c-4c07-9e10-51e7b3f5b4a2",
      "source_mount_target_path": "share_source",
      "start_time": "2026-07-21T06:26:47.185754+00:00",
      "status": "SUCCEEDED",
      "status_message": "Replication completed successfully",
      "target_file_server_ext_id": "c39d3fa0-3f2c-4c07-9e10-51e7b3f5b4a1",
      "target_mount_target_ext_id": "2a2b3c4d-3f2c-4c07-9e10-51e7b3f5b4a2",
      "target_mount_target_path": "share_target",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching replication jobs info"

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
  description: External ID of the replication job.
  type: str
  returned: when external ID is provided
  sample: "6f6c5e75-bd80-4d5a-9d3f-7a1f7f9a4d90"

total_available_results:
  description: The total number of available replication jobs in PC.
  type: int
  returned: when all replication jobs are fetched
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_replication_jobs_api_instance,
)
from ..module_utils.v4.files.helpers import get_replication_job  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_replication_job_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_replication_job(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_replication_jobs(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating replication jobs info spec", **result)

    try:
        resp = api_instance.list_replication_jobs(**kwargs)
    except Exception as exc:
        raise_api_exception(
            module=module,
            exception=exc,
            msg="Api Exception raised while fetching replication jobs info",
        )
        return

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_replication_jobs_api_instance(module)
    if module.params.get("ext_id"):
        get_replication_job_using_ext_id(module, api_instance, result)
    else:
        get_replication_jobs(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
