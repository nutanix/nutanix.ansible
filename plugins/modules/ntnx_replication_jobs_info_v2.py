#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_replication_jobs_info_v2
short_description: Fetch Nutanix Files Smart DR ReplicationJob info in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to fetch information about ReplicationJob in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ReplicationJob.
  - If C(ext_id) is not provided, list multiple ReplicationJob optionally filtered / paginated.
  - A ReplicationJob represents a single execution instance of a Nutanix Files Smart DR
    (share-level) replication policy between a source and a target mount target.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation. The required roles depend on the operation being performed.
  - >-
    B(Get replication job by ext_id) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(List replication jobs) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external identifier of the replication job.
      - When provided, only that replication job is returned.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get a specific replication job using ext_id
  nutanix.ncp.ntnx_replication_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "8f4c6b52-1234-5678-9abc-def012345678"
  register: result
  ignore_errors: true

- name: List all replication jobs
  nutanix.ncp.ntnx_replication_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List replication jobs with filter on status
  nutanix.ncp.ntnx_replication_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "status eq Files.Config.JobStatus'SUCCEEDED'"
  register: result
  ignore_errors: true

- name: List replication jobs with limit
  nutanix.ncp.ntnx_replication_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 5
  register: result
  ignore_errors: true

- name: List replication jobs ordered by startTime descending
  nutanix.ncp.ntnx_replication_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    orderby: "startTime desc"
    limit: 10
  register: result
  ignore_errors: true

- name: Select specific fields for replication jobs
  nutanix.ncp.ntnx_replication_jobs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    select: "extId,status,policyExtId,startTime,endTime"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ReplicationJob info v4 API.
    - It can be a single ReplicationJob if external ID is provided.
    - List of multiple ReplicationJob if external ID is not provided with optional filter, limit, orderby or select.
  returned: always
  type: dict
  sample:
    {
      "average_throughput_bps": 0,
      "bytes_transferred": 0,
      "end_time": "2026-07-21T05:32:41.123456+00:00",
      "estimated_bytes": 0,
      "ext_id": "8f4c6b52-1234-5678-9abc-def012345678",
      "is_delete_propagation_enabled": false,
      "links": null,
      "number_of_estimated_files": 0,
      "number_of_files_failed": 0,
      "number_of_files_transferred": 0,
      "policy_ext_id": "6ac1e2c1-1111-2222-3333-abcdef012345",
      "progress_percentage": 100,
      "replication_summary": "SCHEDULE_MET",
      "source_file_server_ext_id": "0005f8a3-1111-1111-1111-1111abcdef01",
      "source_mount_target_ext_id": "aa11bb22-1111-2222-3333-4444abcdef01",
      "source_mount_target_path": "\\\\source-fs\\share1",
      "start_time": "2026-07-21T05:31:41.123456+00:00",
      "status": "SUCCEEDED",
      "status_message": null,
      "target_file_server_ext_id": "0005f8a3-2222-2222-2222-2222abcdef01",
      "target_mount_target_ext_id": "bb22cc33-2222-3333-4444-5555abcdef02",
      "target_mount_target_path": "\\\\target-fs\\share1",
      "tenant_id": null
    }
changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false
ext_id:
  description: External ID of the replication job (only when C(ext_id) input is provided).
  returned: when external ID is provided
  type: str
  sample: "8f4c6b52-1234-5678-9abc-def012345678"
total_available_results:
  description: The total number of available replication jobs known to PC.
  returned: when listing all replication jobs
  type: int
  sample: 12
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching replication jobs info"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  returned: when an error occurs
  type: str
failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
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
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching replication jobs info",
        )

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
