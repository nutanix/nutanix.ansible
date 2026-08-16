#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vdi_user_session_v2
short_description: Update VDI synchronization user session in Nutanix Files
version_added: 2.7.0
description:
  - This module allows you to update the owner file server for a VDI synchronization
    user session belonging to a VDI-sync replication policy in Nutanix Files.
  - VDI user sessions are read-mostly resources managed by the Files control plane;
    the Files v4 API only exposes an Update endpoint for this entity, so the module
    supports M(nutanix.ncp.ntnx_vdi_user_session_v2) with I(state=present) and a
    resolved I(ext_id) only. Attempting to run this module with I(state=absent) or
    without I(ext_id) is intentionally rejected because the underlying API neither
    creates nor deletes VDI user sessions.
  - This module uses Prism Central v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation. The required roles depend on the operation being performed.
  - >-
    B(Update VDI user session owner file server) -
    Required Roles: Prism Admin, Super Admin, File Server Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - When I(state=present) and I(ext_id) is provided the module updates the VDI
        user session by switching its owner file server to
        I(owner_file_server_ext_id).
      - I(state=absent) is rejected because the Files v4 API does not expose a
        delete operation for VDI user sessions.
      - Providing I(state=present) without I(ext_id) is rejected because the
        Files v4 API does not expose a create operation for VDI user sessions.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external identifier of the VDI synchronization user session to update.
      - Required for the update operation.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server that hosts the VDI-sync
        replication policy.
      - Required for the update operation.
    type: str
    required: true
  replication_policy_ext_id:
    description:
      - The external identifier of the VDI-sync replication policy that owns the
        VDI user session.
      - Required for the update operation.
    type: str
    required: true
  owner_file_server_ext_id:
    description:
      - File server external identifier that will become the owner file server for
        the specified VDI user session. The value must be a valid UUID that refers
        to a Nutanix file server participating in the referenced VDI-sync
        replication policy.
      - Required for the update operation.
    type: str
    required: false
  user_name:
    description:
      - Domain and username of the VDI user (for example V(EXAMPLE\\alice)).
      - The Files control plane translates the value to the user SID; this field
        is treated as read-only by the API and is only echoed back in the response
        of the update call for correlation.
      - Maximum 256 characters.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Update VDI user session owner file server
  nutanix.ncp.ntnx_vdi_user_session_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "b1c9d6a2-1234-4c22-8d41-000000000001"
    replication_policy_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "e5d3f0a1-4444-4222-8d41-000000000010"
    owner_file_server_ext_id: "5f7b26f9-aaaa-4c22-8d41-000000000002"
    user_name: "EXAMPLE\\alice"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating a VDI synchronization user session.
    - If C(wait) is true the response holds the completed task detail for the
      Update VDI User Session action.
    - If C(wait) is false the response holds the initial task reference returned
      by the API.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": null,
      "completed_time": "2026-05-06T11:52:14.000123+00:00",
      "completion_details": null,
      "created_time": "2026-05-06T11:52:12.000123+00:00",
      "entities_affected": [
          {
              "ext_id": "e5d3f0a1-4444-4222-8d41-000000000010",
              "name": null,
              "rel": "files:config:vdi-user-session"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:6d3d9c30-1111-4c22-8d41-000000000099",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-05-06T11:52:14.000123+00:00",
      "legacy_error_message": null,
      "number_of_subtasks": 0,
      "operation": "kFilesVdiUserSessionUpdate",
      "operation_description": "Update VDI synchronization user session owner file server",
      "owned_by": null,
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2026-05-06T11:52:12.000456+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task that performed the update.
  returned: always
  type: str
  sample: "ZXJnb24=:6d3d9c30-1111-4c22-8d41-000000000099"

ext_id:
  description:
    - The external ID of the VDI synchronization user session.
  returned: always
  type: str
  sample: "e5d3f0a1-4444-4222-8d41-000000000010"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - This indicates whether the task was skipped, for example when the update
      body would not change any field on the current VDI user session.
  returned: When the update is a no-op
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description:
    - Status or error message describing the outcome of the operation.
    - Populated on validation errors (missing required parameters, unsupported
      state), idempotency short-circuits, and API failures.
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: >-
    VDI user session with ext_id 'e5d3f0a1-4444-4222-8d41-000000000010' is
    already owned by file server '5f7b26f9-aaaa-4c22-8d41-000000000002'.
    Nothing to change.
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_replication_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_vdi_user_session  # noqa: E402
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
    module_args = dict(
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        replication_policy_ext_id=dict(type="str", required=True),
        owner_file_server_ext_id=dict(type="str"),
        user_name=dict(type="str"),
    )
    return module_args


def _check_for_idempotency(old_spec_dict, update_spec_dict):
    """Compare the sanitized old and updated VDI user session dicts.

    The only user-mutable attribute on this entity is
    ``owner_file_server_ext_id``. All other fields (``user_name``,
    ``current_session``, ``ext_id``, ``links``, ``tenant_id``) are read-only
    and echoed unchanged. Comparing sanitized dicts is therefore a reliable
    idempotency signal.
    """
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    return old_spec_dict == update_spec_dict


def update_vdi_user_session(module, api_instance, result):
    validate_required_params(module, ["ext_id", "owner_file_server_ext_id"])

    file_server_ext_id = module.params.get("file_server_ext_id")
    replication_policy_ext_id = module.params.get("replication_policy_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec_wrapper = get_vdi_user_session(
        module,
        api_instance,
        file_server_ext_id,
        replication_policy_ext_id,
        ext_id,
    )
    old_spec = old_spec_wrapper.data
    # Fall back to a freshly built VdiUserSession spec if the SDK ever returns
    # a bare wrapper without ``data`` (defensive; the get-by-id call above
    # normally raises for a missing entity).
    if old_spec is None:
        old_spec = files_sdk.VdiUserSession(
            owner_file_server_ext_id=module.params.get("owner_file_server_ext_id"),
            user_name=module.params.get("user_name"),
        )

    etag = get_etag(data=old_spec_wrapper)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating VDI user session", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update VDI user session spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if _check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(old_spec.to_dict())
        module.exit_json(
            msg=(
                "VDI user session with ext_id '{0}' is already owned by file "
                "server '{1}'. Nothing to change.".format(
                    ext_id, module.params.get("owner_file_server_ext_id")
                )
            ),
            **result,
        )

    resp = None
    try:
        resp = api_instance.update_vdi_user_session_by_id(
            fileServerExtId=file_server_ext_id,
            replicationPolicyExtId=replication_policy_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating VDI user session",
        )

    task_ext_id = resp.data.ext_id
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
        required_if=[
            ("state", "present", ("ext_id",)),
            ("state", "absent", ("ext_id",)),
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
    state = module.params.get("state")
    if state == "absent":
        module.fail_json(
            msg=(
                "Deleting a VDI user session is not supported by the Nutanix "
                "Files v4 API. Only state=present with an ext_id is supported "
                "for this module."
            ),
            **result,
        )

    api_instance = get_replication_policies_api_instance(module)
    update_vdi_user_session(module, api_instance, result)

    # Ensure task_ext_id is always present on the result envelope even when the
    # underlying wait_for_completion path did not populate it (e.g. wait=False
    # for a check-mode preview).
    result.setdefault("task_ext_id", None)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
