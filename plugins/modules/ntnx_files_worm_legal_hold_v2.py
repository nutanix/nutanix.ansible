#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_worm_legal_hold_v2
short_description: Enable or disable WORM legal hold on a Nutanix Files mount target
version_added: 2.7.0
description:
  - This module allows you to enable or disable WORM (Write Once Read Many) legal hold on a Nutanix Files mount target.
  - If C(state) is C(present), WORM legal hold is enabled on the mount target.
  - If C(state) is C(absent), WORM legal hold is disabled on the mount target.
  - WORM legal hold is applicable only for WORM compliant mount targets.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Enable WORM legal hold) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Disable WORM legal hold) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present), WORM legal hold will be enabled on the mount target.
      - If C(state) is set to C(absent), WORM legal hold will be disabled on the mount target.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  file_server_ext_id:
    description:
      - The external identifier of the file server that owns the mount target.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the mount target on which WORM legal hold is enabled or disabled.
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
- name: Enable WORM legal hold on a mount target
  nutanix.ncp.ntnx_files_worm_legal_hold_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "d1e2f3a4-b5c6-4d7e-8f90-1a2b3c4d5e6f"
    ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
  register: result
  ignore_errors: true

- name: Disable WORM legal hold on a mount target
  nutanix.ncp.ntnx_files_worm_legal_hold_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "d1e2f3a4-b5c6-4d7e-8f90-1a2b3c4d5e6f"
    ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for enabling or disabling WORM legal hold on the mount target.
    - Task details when C(wait) is true.
    - Task details when C(wait) is false.
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
              "ext_id": "9c1e537d-6777-4c22-5d41-ddd0c3337aa9",
              "name": "mount_target_ansible",
              "rel": "files:config:mount-target"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T06:26:51.524581+00:00",
      "legacy_error_message": null,
      "operation": "EnableWormLegalHold",
      "operation_description": "Enable WORM legal hold",
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

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description:
    - The external ID of the mount target on which the operation was performed.
  returned: always
  type: str
  sample: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency
  returned: when the operation was skipped
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or in check mode
  type: str
  sample: "WORM legal hold is already enabled on mount target with ext_id: 9c1e537d-6777-4c22-5d41-ddd0c3337aa9. Skipping enable operation."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

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

SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: E402,F401  # pylint: disable=unused-import
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402,F401  # pylint: disable=unused-import
        mock_sdk as files_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )

    return module_args


def _is_legal_hold_enabled(mount_target):
    """Return the current WORM legal hold state of a mount target."""
    worm_spec = getattr(mount_target, "worm_spec", None)
    if worm_spec is None:
        return False
    return bool(getattr(worm_spec, "is_legal_hold_enabled", False))


def enable_worm_legal_hold(module, result, mount_targets_api):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "WORM legal hold will be enabled on mount target with ext_id: {0}".format(
                ext_id
            )
        )
        return

    mount_target = get_mount_target(
        module, mount_targets_api, file_server_ext_id, ext_id
    )
    if _is_legal_hold_enabled(mount_target):
        result["skipped"] = True
        result["msg"] = (
            "WORM legal hold is already enabled on mount target with ext_id: "
            "{0}. Skipping enable operation.".format(ext_id)
        )
        module.exit_json(**result)

    etag = get_etag(mount_target)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for enabling WORM legal hold on mount target "
            "with ext_id: {0}".format(ext_id),
            **result,
        )
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = mount_targets_api.enable_worm_legal_hold(
            fileServerExtId=file_server_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while enabling WORM legal hold on mount target",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def disable_worm_legal_hold(module, result, mount_targets_api):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "WORM legal hold will be disabled on mount target with ext_id: {0}".format(
                ext_id
            )
        )
        return

    mount_target = get_mount_target(
        module, mount_targets_api, file_server_ext_id, ext_id
    )
    if not _is_legal_hold_enabled(mount_target):
        result["skipped"] = True
        result["msg"] = (
            "WORM legal hold is already disabled on mount target with ext_id: "
            "{0}. Skipping disable operation.".format(ext_id)
        )
        module.exit_json(**result)

    etag = get_etag(mount_target)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for disabling WORM legal hold on mount target "
            "with ext_id: {0}".format(ext_id),
            **result,
        )
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = mount_targets_api.disable_worm_legal_hold(
            fileServerExtId=file_server_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disabling WORM legal hold on mount target",
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
            msg=missing_required_lib("ntnx_files_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }
    mount_targets_api = get_mount_target_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        enable_worm_legal_hold(module, result, mount_targets_api)
    else:
        disable_worm_legal_hold(module, result, mount_targets_api)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
