#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_quota_policy_v2
short_description: Create, Update and Delete quota policies for a Nutanix Files mount target
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete quota policies for a Nutanix Files mount target in Nutanix Prism Central.
  - A quota policy specifies the storage consumption limit for a particular user or group on a mount target (share/export).
  - This module uses PC v4 APIs based SDKs.
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create quota policy.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update quota policy.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete quota policy.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the quota policy.
      - Required for update and delete operations.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server that owns the mount target.
    type: str
    required: true
  mount_target_ext_id:
    description:
      - The external identifier of the mount target (share/export) for which the quota policy is configured.
    type: str
    required: true
  principal_type:
    description:
      - The principal type for which the quota policy is applied.
      - Required for create operation.
    type: str
    required: false
    choices:
      - USER
      - GROUP
  principal_name:
    description:
      - Principal name is the name of the user or group assigned to the principal type.
      - Maximum 256 characters.
      - Required for create operation.
    type: str
    required: false
  size_in_bytes:
    description:
      - Quota size in bytes.
      - Minimum value is 0.
      - Required for create operation.
    type: int
    required: false
  enforcement_type:
    description:
      - The enforcement type for the quota policy.
      - C(SOFT) enforcement only notifies while C(HARD) enforcement blocks writes beyond the quota limit.
      - Required for create operation.
    type: str
    required: false
    choices:
      - SOFT
      - HARD
  notification_recipients:
    description:
      - List of recipient's emails to notify about the quota policy consumption.
    type: list
    elements: str
    required: false
  is_notification_enabled:
    description:
      - Enables email notifications for the user or group specified in the principal type.
      - A notification will only be sent if the user or group is close to the quota provided.
    type: bool
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
- name: Create quota policy for a user
  nutanix.ncp.ntnx_files_quota_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    mount_target_ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
    principal_type: "USER"
    principal_name: "user1@ad.example.com"
    size_in_bytes: 1073741824
    enforcement_type: "SOFT"
    is_notification_enabled: true
    notification_recipients:
      - "admin@ad.example.com"
  register: result
  ignore_errors: true

- name: Update quota policy
  nutanix.ncp.ntnx_files_quota_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    mount_target_ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    principal_type: "USER"
    principal_name: "user1@ad.example.com"
    size_in_bytes: 2147483648
    enforcement_type: "HARD"
    is_notification_enabled: false
  register: result
  ignore_errors: true

- name: Delete quota policy
  nutanix.ncp.ntnx_files_quota_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    mount_target_ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting quota policy.
    - If the operation is create or update and C(wait) is true, it will return the quota policy details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "enforcement_type": "SOFT",
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "is_notification_enabled": true,
      "links": null,
      "notification_recipients": ["admin@ad.example.com"],
      "principal_name": "user1@ad.example.com",
      "principal_type": "USER",
      "size_in_bytes": 1073741824,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the quota policy.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: always
  type: bool
  sample: false

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
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating quota policy"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_quota_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_quota_policy  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
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

# Read-only attributes populated by the platform which must not be sent in an update body.
READ_ONLY_FIELDS = ["ext_id", "links", "tenant_id"]


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        mount_target_ext_id=dict(type="str", required=True),
        principal_type=dict(
            type="str",
            choices=["USER", "GROUP"],
            obj=files_sdk.PrincipalType,
        ),
        principal_name=dict(type="str"),
        size_in_bytes=dict(type="int"),
        enforcement_type=dict(
            type="str",
            choices=["SOFT", "HARD"],
            obj=files_sdk.EnforcementType,
        ),
        notification_recipients=dict(type="list", elements="str"),
        is_notification_enabled=dict(type="bool"),
    )
    return module_args


def create_quota_policy(module, result, quota_policies):
    validate_required_params(
        module,
        ["principal_type", "principal_name", "size_in_bytes", "enforcement_type"],
    )
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")

    sg = SpecGenerator(module)
    default_spec = files_sdk.QuotaPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create quota policy spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = quota_policies.create_quota_policy(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            body=spec,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating quota policy",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.QUOTA_POLICY
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_quota_policy(
                module,
                quota_policies,
                file_server_ext_id,
                mount_target_ext_id,
                ext_id,
            )
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Quota Policy"
                ),
                msg="Failed to get entity ext_id from task for Quota Policy",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    return old_spec_dict == update_spec_dict


def update_quota_policy(module, result, quota_policies):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")

    old_spec = get_quota_policy(
        module, quota_policies, file_server_ext_id, mount_target_ext_id, ext_id
    )
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating quota policy", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update quota policy spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    strip_read_only_fields(update_spec, READ_ONLY_FIELDS)

    resp = None
    try:
        resp = quota_policies.update_quota_policy_by_id(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating quota policy",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_quota_policy(
            module, quota_policies, file_server_ext_id, mount_target_ext_id, ext_id
        )
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_quota_policy(module, result, quota_policies):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")

    if module.check_mode:
        result["msg"] = "Quota policy with ext_id:{0} will be deleted.".format(ext_id)
        return

    old_spec = get_quota_policy(
        module, quota_policies, file_server_ext_id, mount_target_ext_id, ext_id
    )
    etag = get_etag(data=old_spec)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = quota_policies.delete_quota_policy_by_id(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            extId=ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting quota policy",
        )
    task_ext_id = getattr(resp.data, "ext_id", None) if resp else None
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("principal_type", "ext_id"), True),
        ],
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
        "failed": False,
        "ext_id": None,
    }
    quota_policies = get_quota_policies_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_quota_policy(module, result, quota_policies)
        else:
            create_quota_policy(module, result, quota_policies)
    else:
        delete_quota_policy(module, result, quota_policies)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
