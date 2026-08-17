#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_fix_infected_file_v2
short_description: Manage security actions on infected files in Nutanix Files
version_added: 2.7.0
description:
  - This module allows you to manage the security of an infected file on a Nutanix Files server.
  - When C(state) is C(present), the module invokes the security action (RESCAN, RESET,
    QUARANTINE, UNQUARANTINE) specified via C(action) on the target infected file.
  - When C(state) is C(absent), the module deletes the infected file entry from the file server.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Manage security of an infected file) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Delete an infected file) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present), the security C(action) is applied to the infected file.
      - If C(state) is set to C(absent), the infected file is deleted from the file server.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external identifier of the infected file.
      - Required for both C(state=present) (fix action) and C(state=absent) (delete).
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server that owns the infected file.
      - Required for both C(state=present) (fix action) and C(state=absent) (delete).
    type: str
    required: false
  action:
    description:
      - Security action to perform on the infected file.
      - Required when C(state=present).
      - C(RESCAN) sends the file for AV re-scan through the configured ICAP servers.
      - C(RESET) resets the quarantine/unquarantine bits and removes the quarantined-file entry.
      - C(QUARANTINE) marks the infected file as quarantined so it is blocked to SMB clients.
      - C(UNQUARANTINE) removes the quarantine mark from an infected file.
    type: str
    required: false
    choices:
      - RESCAN
      - RESET
      - QUARANTINE
      - UNQUARANTINE
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
- name: Quarantine an infected file
  nutanix.ncp.ntnx_files_fix_infected_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "b6f6c9c7-6b0a-4d3e-a91d-2eaf2b3ec8b1"
    action: QUARANTINE
  register: result
  ignore_errors: true

- name: Unquarantine an infected file
  nutanix.ncp.ntnx_files_fix_infected_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "b6f6c9c7-6b0a-4d3e-a91d-2eaf2b3ec8b1"
    action: UNQUARANTINE
  register: result
  ignore_errors: true

- name: Rescan an infected file
  nutanix.ncp.ntnx_files_fix_infected_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "b6f6c9c7-6b0a-4d3e-a91d-2eaf2b3ec8b1"
    action: RESCAN
  register: result
  ignore_errors: true

- name: Reset quarantine/unquarantine flags on an infected file
  nutanix.ncp.ntnx_files_fix_infected_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "b6f6c9c7-6b0a-4d3e-a91d-2eaf2b3ec8b1"
    action: RESET
  register: result
  ignore_errors: true

- name: Delete an infected file entry
  nutanix.ncp.ntnx_files_fix_infected_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "b6f6c9c7-6b0a-4d3e-a91d-2eaf2b3ec8b1"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the fix or delete operation on the infected file.
    - When C(wait=true) this returns the task details for the FixInfectedFile / DeleteInfectedFile task.
    - When C(wait=false) this returns the immediate task reference returned by the API.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T08:11:12.104582+00:00",
      "created_time": "2026-07-21T08:11:10.001156+00:00",
      "entities_affected": [
        {
          "ext_id": "b6f6c9c7-6b0a-4d3e-a91d-2eaf2b3ec8b1",
          "rel": "files:config:infected-file"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T08:11:12.104582+00:00",
      "legacy_error_message": null,
      "operation": "FixInfectedFile",
      "operation_description": "Manage security of an infected file",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-21T08:11:10.020123+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task started by the operation.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the infected file that was acted upon.
  returned: always
  type: str
  sample: "b6f6c9c7-6b0a-4d3e-a91d-2eaf2b3ec8b1"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - Indicates whether the operation was skipped because the infected file is already in the requested state.
    - For example, applying C(QUARANTINE) to an already-quarantined file, or C(UNQUARANTINE) to a non-quarantined file.
  returned: when applicable
  type: bool
  sample: false

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
    - Human readable status message returned by the module (idempotency notes, check-mode notes, or error messages).
  returned: When there is an error, module is idempotent, or in check mode
  type: str
  sample: "Infected file with ext_id 'b6f6c9c7-6b0a-4d3e-a91d-2eaf2b3ec8b1' is already quarantined. Skipping QUARANTINE action."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_infected_files_api_instance,
)
from ..module_utils.v4.files.helpers import get_infected_file  # noqa: E402
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
        file_server_ext_id=dict(type="str"),
        action=dict(
            type="str",
            choices=["RESCAN", "RESET", "QUARANTINE", "UNQUARANTINE"],
            obj=files_sdk.InfectedFileActionType,
        ),
    )
    return module_args


def _build_fix_spec(module, result):
    """Build the InfectedFileFixSpec SDK object from module params."""
    sg = SpecGenerator(module)
    default_spec = files_sdk.InfectedFileFixSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating fix infected file spec", **result)
    return spec


def _check_idempotency(module, api_instance, file_server_ext_id, ext_id, action):
    """
    Return (skipped_bool, message). If the requested action is a no-op given the
    current state of the infected file (e.g. QUARANTINE on an already quarantined
    file), skipped_bool is True and the message explains why.
    """
    try:
        current = get_infected_file(module, api_instance, file_server_ext_id, ext_id)
    except Exception:
        return False, None

    is_quarantined = getattr(current, "is_quarantined", None)
    if action == "QUARANTINE" and is_quarantined is True:
        return True, (
            "Infected file with ext_id '{0}' is already quarantined. "
            "Skipping QUARANTINE action.".format(ext_id)
        )
    if action == "UNQUARANTINE" and is_quarantined is False:
        return True, (
            "Infected file with ext_id '{0}' is not quarantined. "
            "Skipping UNQUARANTINE action.".format(ext_id)
        )
    return False, None


def create_FixInfectedFile(module, result, api_instance):
    """
    Fallback create path — the FixInfectedFile action is not a resource-create
    operation and always requires an ext_id. This method exists only to satisfy
    the state-based dispatch contract and fails with a helpful message when
    reached without an ext_id.
    """
    result["failed"] = True
    module.fail_json(
        msg=(
            "'ext_id' and 'file_server_ext_id' are required to perform a fix action "
            "on an infected file. FixInfectedFile is an action on an existing "
            "infected file, not a creation of a new resource."
        ),
        **result,
    )


def update_FixInfectedFile(module, result, api_instance):
    """Perform the fix (security action) on the target infected file."""
    validate_required_params(module, ["ext_id", "file_server_ext_id", "action"])

    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    action = module.params.get("action")

    result["ext_id"] = ext_id

    spec = _build_fix_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Fix action '{0}' will be applied to infected file with "
            "ext_id '{1}' on file server '{2}'.".format(
                action, ext_id, file_server_ext_id
            )
        )
        return

    skipped, msg = _check_idempotency(
        module, api_instance, file_server_ext_id, ext_id, action
    )
    if skipped:
        result["skipped"] = True
        result["changed"] = False
        module.exit_json(msg=msg, **result)

    resp = None
    try:
        resp = api_instance.fix_infected_file(
            fileServerExtId=file_server_ext_id, extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while performing fix action '{0}' on "
                "infected file '{1}' of file server '{2}'".format(
                    action, ext_id, file_server_ext_id
                )
            ),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def delete_FixInfectedFile(module, result, api_instance):
    """Delete the infected file entry from the file server."""
    validate_required_params(module, ["ext_id", "file_server_ext_id"])

    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")

    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Infected file with ext_id '{0}' on file server '{1}' will be "
            "deleted.".format(ext_id, file_server_ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.delete_infected_file_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while deleting infected file '{0}' on "
                "file server '{1}'".format(ext_id, file_server_ext_id)
            ),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id", "file_server_ext_id")),
            ("state", "present", ("ext_id", "file_server_ext_id", "action")),
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
        "task_ext_id": None,
    }
    api_instance = get_infected_files_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_FixInfectedFile(module, result, api_instance)
        else:
            create_FixInfectedFile(module, result, api_instance)
    else:
        delete_FixInfectedFile(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
