#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_worm_compliance_v2
short_description: Enable WORM compliance on a Nutanix Files mount target (share)
version_added: 2.7.0
description:
    - Enable Write Once Read Many (WORM) compliance on a WORM-enabled mount target (share) of a file server.
    - Enabling WORM compliance is an irreversible action; once enabled it cannot be disabled on the share.
    - The mount target must already be WORM-enabled before compliance can be enabled on it.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Enable WORM compliance) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is present, the module will enable WORM compliance on the mount target.
            - If C(state) is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    file_server_ext_id:
        description:
            - The external identifier of the file server that the mount target belongs to.
        type: str
        required: true
    ext_id:
        description:
            - The external identifier of the mount target (share) on which WORM compliance will be enabled.
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
- name: Enable WORM compliance on a mount target
  nutanix.ncp.ntnx_files_worm_compliance_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "b2fb8f36-6b3a-4e1a-9b0e-3c2f7d1a9c4e"
    ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for enabling WORM compliance on the mount target.
        - Task details if C(wait) is true.
        - Task details if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-21T06:26:51.524581+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T06:26:47.167906+00:00",
            "entities_affected": [
                {
                    "ext_id": "9c1e537d-6777-4c22-5d41-ddd0c3337aa9",
                    "name": "worm_share_ansible",
                    "rel": "files:config:mount-target"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T06:26:51.524581+00:00",
            "legacy_error_message": null,
            "operation": "EnableWormCompliance",
            "operation_description": "Enable WORM compliance",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T06:26:47.185754+00:00",
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
    returned: When there is an error or in check mode
    type: str
    sample: "Api Exception raised while enabling WORM compliance for mount target"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str
    sample: "Api Exception raised while fetching mount target info using ext_id"

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
    description: The external ID of the mount target on which WORM compliance was enabled
    returned: always
    type: str
    sample: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_mount_target_api_instance,
)
from ..module_utils.v4.files.helpers import get_mount_target  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )

    return module_args


def enable_worm_compliance(module, result, mount_targets):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "WORM compliance will be enabled on the mount target with ext_id:{0} "
            "of the file server with ext_id:{1}.".format(ext_id, file_server_ext_id)
        )
        return

    mount_target = get_mount_target(module, mount_targets, file_server_ext_id, ext_id)
    etag = get_etag(mount_target)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = mount_targets.enable_worm_compliance(
            fileServerExtId=file_server_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while enabling WORM compliance for mount target",
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

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    mount_targets = get_mount_target_api_instance(module)
    enable_worm_compliance(module, result, mount_targets)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
