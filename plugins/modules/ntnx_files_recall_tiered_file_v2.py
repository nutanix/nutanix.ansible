#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_recall_tiered_file_v2
short_description: Recall one or more tiered files on a Nutanix file server
version_added: 2.7.0
description:
    - This module allows you to recall one or more previously tiered files back to a Nutanix file server.
    - Recall moves file data that was tiered to an object store back to the primary file server.
    - This is an asynchronous action; the API returns a task and the data is moved by the tiering engine.
    - This module uses PC v4 APIs based SDKs.
notes:
    - This module requires the tiering feature to be configured on the target file server.
    - Either C(file_paths) or C(i_node_numbers) must be provided, but not both.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is present, the module will recall the tiered files.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the file server on which the tiered files should be recalled.
        type: str
        required: true
    is_single_dir_tree:
        description:
            - Indicates whether the provided file paths belong to a single directory tree.
            - When set to true, the recall is optimized for files that live under a single directory tree.
        type: bool
        required: false
    mount_target_ext_id:
        description:
            - The external identifier of the mount target (share) that owns the files to be recalled.
        type: str
        required: false
    file_paths:
        description:
            - List of file paths (relative to the share) to recall.
            - Mutually exclusive with C(i_node_numbers).
            - Either C(file_paths) or C(i_node_numbers) is required.
        type: list
        elements: str
        required: false
    i_node_numbers:
        description:
            - List of inode numbers identifying the files to recall.
            - Mutually exclusive with C(file_paths).
            - Either C(file_paths) or C(i_node_numbers) is required.
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
- name: Recall tiered files using file paths
  nutanix.ncp.ntnx_files_recall_tiered_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "5f1d0b7a-7f0f-4a0d-9c9a-3f2b1c0d5e6f"
    mount_target_ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    is_single_dir_tree: false
    file_paths:
      - "/dir1/tiered_file1.dat"
      - "/dir1/tiered_file2.dat"
  register: result

- name: Recall tiered files using inode numbers
  nutanix.ncp.ntnx_files_recall_tiered_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "5f1d0b7a-7f0f-4a0d-9c9a-3f2b1c0d5e6f"
    mount_target_ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    i_node_numbers:
      - "1234567"
      - "1234568"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for recalling tiered files on the file server.
        - Task details if C(wait) is true.
        - Task reference if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-21T06:26:51.524581+00:00",
            "created_time": "2026-07-21T06:26:47.167906+00:00",
            "entities_affected": [
                {
                    "ext_id": "5f1d0b7a-7f0f-4a0d-9c9a-3f2b1c0d5e6f",
                    "name": "file_server",
                    "rel": "files:config:file-server"
                }
            ],
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "operation": "RecallTieredFiles",
            "operation_description": "Recall one or more files",
            "progress_percentage": 100,
            "started_time": "2026-07-21T06:26:47.185754+00:00",
            "status": "SUCCEEDED"
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while recalling tiered files"

error:
    description: This field typically holds information about if the task has errors that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Failed generating spec for recalling tiered files"

failed:
    description: This field typically holds information about if the task has failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the file server on which the tiered files were recalled.
    returned: always
    type: str
    sample: "5f1d0b7a-7f0f-4a0d-9c9a-3f2b1c0d5e6f"
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
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        is_single_dir_tree=dict(type="bool"),
        mount_target_ext_id=dict(type="str"),
        file_paths=dict(type="list", elements="str"),
        i_node_numbers=dict(type="list", elements="str"),
    )
    return module_args


def recall_tiered_files(module, result, tier_api):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = files_sdk.RecallTieredFilesSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for recalling tiered files", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = tier_api.recall_tiered_files(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while recalling tiered files",
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
        mutually_exclusive=[
            ("file_paths", "i_node_numbers"),
        ],
        required_one_of=[
            ("file_paths", "i_node_numbers"),
        ],
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
    api_instance = get_tier_api_instance(module)
    recall_tiered_files(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
