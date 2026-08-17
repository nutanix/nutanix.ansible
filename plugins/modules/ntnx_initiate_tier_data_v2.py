#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_initiate_tier_data_v2
short_description: Initiate tiering of files on a Nutanix file server
version_added: 2.7.0
description:
    - Initiate a manual tiering data action on a Nutanix Files file server.
    - Trigger tiering either for the whole file server, a whole mount target, or a specific set of files.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Initiate tiering data on a file server) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported; the action always triggers tiering.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the file server on which tiering will be initiated.
        type: str
        required: true
    duration_seconds:
        description:
            - Duration (in seconds) for which the manual tiering action should run.
            - If not provided tiering will run until the memory has reached the threshold capacity value.
            - When provided the SDK enforces a minimum of 3600 seconds.
        type: int
        required: false
    files_spec:
        description:
            - Optional selector describing which files should be tiered.
            - If omitted the whole file server (subject to the tiering configuration) is considered.
        type: dict
        required: false
        suboptions:
            is_single_dir_tree:
                description:
                    - Set to true if all listed files belong to the same Volume Group (single directory tree).
                type: bool
                required: false
                default: false
            mount_target_ext_id:
                description:
                    - External identifier of the mount target (share/export) that contains the files.
                type: str
                required: false
            file_paths:
                description:
                    - List of absolute file paths (relative to the mount target root) to be tiered.
                type: list
                elements: str
                required: false
            i_node_numbers:
                description:
                    - List of inode numbers of files to be tiered.
                type: list
                elements: str
                required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: Initiate tiering for a whole file server
  nutanix.ncp.ntnx_initiate_tier_data_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    duration_seconds: 3600
  register: result
  ignore_errors: true

- name: Initiate tiering for specific files on a mount target
  nutanix.ncp.ntnx_initiate_tier_data_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    duration_seconds: 1800
    files_spec:
      is_single_dir_tree: false
      mount_target_ext_id: "d9c3f0f3-5f4a-42c1-9c66-1b23f4e5a111"
      file_paths:
        - "/archive/2024/report1.pdf"
        - "/archive/2024/report2.pdf"
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
    description:
        - Response for initiating the tier-data action.
        - Task details of the tiering action.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-21T05:14:11.123456+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T05:14:05.001234+00:00",
            "entities_affected": [
                {
                    "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
                    "rel": "files:config:file-server"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T05:14:11.123456+00:00",
            "legacy_error_message": null,
            "operation": "TierData",
            "operation_description": "Initiate tiering data",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T05:14:05.101234+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while initiating tier data on file server"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str
    sample: "Failed generating spec for initiating tier data"

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the file server on which tier data was initiated
    returned: always
    type: str
    sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import get_tier_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    files_spec = dict(
        is_single_dir_tree=dict(type="bool", required=False, default=False),
        mount_target_ext_id=dict(type="str", required=False),
        file_paths=dict(type="list", elements="str", required=False),
        i_node_numbers=dict(type="list", elements="str", required=False),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        duration_seconds=dict(type="int", required=False),
        files_spec=dict(
            type="dict",
            options=files_spec,
            required=False,
            obj=files_sdk.FilesSpec,
        ),
    )
    return module_args


def initiate_tier_data(module, tier_api, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["ext_id"])

    sg = SpecGenerator(module)
    default_spec = files_sdk.TierDataSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for initiating tier data", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = tier_api.tier_data(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while initiating tier data on file server",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_files_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    tier_api = get_tier_api_instance(module)
    initiate_tier_data(module, tier_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
