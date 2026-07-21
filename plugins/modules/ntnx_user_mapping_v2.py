#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_mapping_v2
short_description: Upload user mappings for a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to upload the NFS/SMB user-mapping configuration
    for a Nutanix Files file server in Nutanix Prism Central.
  - The user-mapping file describes how Active Directory (Windows) users and
    groups are mapped to NFS UIDs/GIDs (Unix), which is required for
    multiprotocol shares that must present a consistent identity to SMB and
    NFS clients.
  - Only the upload (POST) action is exposed by this module. To read the
    current user-mapping configuration back from the file server, use
    M(nutanix.ncp.ntnx_user_mappings_info_v2).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Upload user mappings for a file server) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is set to C(present), the module will upload the user
        mappings file to the given file server.
      - Only C(present) is supported because the underlying API only exposes
        an upload action.
    type: str
    choices:
      - present
    default: present
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server on which to install the
        user mappings.
    type: str
    required: true
  path:
    description:
      - Absolute path on the Ansible controller of the user mappings file to
        upload.
      - The file typically contains the AD-to-NFS user/group mapping
        definitions (for example a mapping file exported from an existing
        Files file server).
    type: str
    required: true
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
- name: Upload user mappings for a file server
  nutanix.ncp.ntnx_user_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "0005d0f6-1c3f-4e15-1155-ac1f6b6d0e3c"
    path: "/tmp/user_mappings.json"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for uploading user mappings on a Nutanix Files file server.
    - Task details when C(wait) is true; otherwise the raw task reference
      returned by the SDK.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T09:12:41.121412+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T09:12:35.921955+00:00",
      "entities_affected": [
        {
          "ext_id": "0005d0f6-1c3f-4e15-1155-ac1f6b6d0e3c",
          "name": "fs-ansible",
          "rel": "files:config:file-server"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:9c8b9e94-3a41-42d1-b41b-3f5d8c26f3e2",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T09:12:41.121412+00:00",
      "legacy_error_message": null,
      "operation": "UploadUserMappings",
      "operation_description": "Upload user mappings",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-21T09:12:35.945112+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the upload user mappings task.
  returned: always
  type: str
  sample: "ZXJnb24=:9c8b9e94-3a41-42d1-b41b-3f5d8c26f3e2"

ext_id:
  description:
    - The external ID of the file server on which the user mappings were
      uploaded.
  returned: always
  type: str
  sample: "0005d0f6-1c3f-4e15-1155-ac1f6b6d0e3c"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, in check mode, or on validation failure.
  type: str
  sample: "Api Exception raised while uploading user mappings for file server"

error:
  description:
    - This field typically holds information about if the task have errors
      that occurred during the task execution.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

PATHLIB_IMP_ERROR = None
try:
    import pathlib  # noqa: E402
except ImportError:
    pathlib = None
    PATHLIB_IMP_ERROR = traceback.format_exc()

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_user_mappings_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        file_server_ext_id=dict(type="str", required=True),
        path=dict(type="str", required=True),
    )
    return module_args


def upload_user_mappings(module, api_instance, result):
    """
    Upload the NFS/SMB user mappings file to a Nutanix Files file server.

    Args:
        module (object): Ansible module object
        api_instance (object): UserMappingsApi instance
        result (dict): Result object to populate for the caller
    """
    validate_required_params(module, ["file_server_ext_id", "path"])

    file_server_ext_id = module.params.get("file_server_ext_id")
    raw_path = module.params.get("path")
    result["ext_id"] = file_server_ext_id

    if not pathlib:
        module.fail_json(
            msg=missing_required_lib("pathlib"), exception=PATHLIB_IMP_ERROR, **result
        )

    upload_path = pathlib.Path(raw_path)
    if not upload_path.is_file():
        module.fail_json(
            msg=(
                "Path to the user mappings file '{0}' is invalid or does not "
                "exist on the Ansible controller".format(raw_path)
            ),
            **result  # fmt: skip
        )

    if module.check_mode:
        result["msg"] = (
            "User mappings from '{0}' will be uploaded to file server with "
            "ext_id:{1}.".format(str(upload_path), file_server_ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.upload_user_mappings(
            fileServerExtId=file_server_ext_id, path=upload_path
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while uploading user mappings for file server",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_user_mappings_api_instance(module)
    upload_user_mappings(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
