#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snapshot_schedules_info_v2
short_description: Fetch snapshot schedules info of a file server in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about SnapshotSchedule in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific SnapshotSchedule.
  - If C(ext_id) is not provided, list multiple SnapshotSchedule optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get snapshot schedule by ext_id) -
    Required Roles: File Server Admin, File Server Viewer, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(List snapshot schedules) -
    Required Roles: File Server Admin, File Server Viewer, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external ID of the snapshot schedule.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external ID of the parent file server that owns the snapshot schedule.
    type: str
    required: true
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
- name: Get snapshot schedule using ext_id
  nutanix.ncp.ntnx_snapshot_schedules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d1234567-89ab-cdef-0123-456789abcdef"
    ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true

- name: List all snapshot schedules on a file server
  nutanix.ncp.ntnx_snapshot_schedules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d1234567-89ab-cdef-0123-456789abcdef"
  register: result
  ignore_errors: true

- name: List snapshot schedules with filter
  nutanix.ncp.ntnx_snapshot_schedules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d1234567-89ab-cdef-0123-456789abcdef"
    filter: "type eq Nutanix.Files.Config.SnapshotScheduleType'DAILY'"
  register: result
  ignore_errors: true

- name: List snapshot schedules with limit
  nutanix.ncp.ntnx_snapshot_schedules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d1234567-89ab-cdef-0123-456789abcdef"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC SnapshotSchedule info v4 API.
    - It can be a single SnapshotSchedule if external ID is provided.
    - List of multiple SnapshotSchedule if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "48f78959-14a6-4c47-b5db-920460c4b668",
      "type": "DAILY",
      "max_retention_count": 7,
      "schedule": {
          "frequency": 1
      },
      "links": null,
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
  sample: "Api Exception raised while fetching snapshot schedule info"

error:
  description: This field holds information about any errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field holds information about whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the snapshot schedule.
  type: str
  returned: when external ID is provided
  sample: "48f78959-14a6-4c47-b5db-920460c4b668"

file_server_ext_id:
  description: External ID of the parent file server.
  type: str
  returned: always
  sample: "d1234567-89ab-cdef-0123-456789abcdef"

total_available_results:
  description: The total number of available snapshot schedules on the file server.
  type: int
  returned: when all snapshot schedules are listed
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_snapshot_schedules_api_instance,
)
from ..module_utils.v4.files.helpers import get_snapshot_schedule  # noqa: E402
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
        file_server_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_snapshot_schedule_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    resp = get_snapshot_schedule(module, api_instance, file_server_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["file_server_ext_id"] = file_server_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_snapshot_schedules(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["file_server_ext_id"] = file_server_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating snapshot schedules info spec", **result)

    try:
        resp = api_instance.list_snapshot_schedules(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching snapshot schedules info",
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
    api_instance = get_snapshot_schedules_api_instance(module)
    if module.params.get("ext_id"):
        get_snapshot_schedule_using_ext_id(module, api_instance, result)
    else:
        list_snapshot_schedules(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
