#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_virus_scan_policy_v2
short_description: Create, Update and Delete virus scan policies for a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to create, update and delete virus scan policies on a Nutanix Files file server.
  - A virus scan policy defines how files stored on an SMB share are inspected by external ICAP antivirus servers,
    including whether files are scanned on read/write, size thresholds, excluded extensions and the action taken
    when a scan fails.
  - Policies can be created at the file server (global) level or scoped to an individual mount target (share).
  - This module uses the Nutanix Files v4 APIs based SDK.
notes:
    - >-
      Antivirus integration on Nutanix Files is supported only over SMB and requires one or more reachable ICAP
      antivirus servers to be configured on the file server before scans can be performed.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create virus scan policy.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update virus scan policy.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete virus scan policy.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the virus scan policy.
      - Required for update and delete operations.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external ID of the file server that owns the virus scan policy.
      - Required for all operations.
    type: str
    required: true
  scan_timeout_interval_secs:
    description:
      - Time interval, in seconds, allowed for the antivirus scan of a single file to complete.
      - If the scan does not finish within this interval the request times out and the fallback action is taken.
      - Allowed range is 0 to 240.
    type: int
    required: false
  is_scan_on_write_enabled:
    description:
      - Whether files should be scanned for viruses when they are written or updated on the share.
    type: bool
    required: false
    default: true
  is_scan_on_read_enabled:
    description:
      - Whether files should be scanned for viruses when they are opened for read from the share.
    type: bool
    required: false
    default: true
  max_file_size_threshold_bytes:
    description:
      - Maximum file size, in bytes, that is allowed to be scanned by the antivirus servers.
      - Files larger than this threshold are skipped from scanning.
    type: int
    required: false
  is_file_access_blocked:
    description:
      - Whether client file access should be blocked for this policy when the antivirus scan fails or times out.
      - When set to C(true) access is denied on scan failure; when set to C(false) access is allowed.
    type: bool
    required: false
    default: false
  is_anti_virus_enabled:
    description:
      - Whether the antivirus server integration is enabled for this virus scan policy.
    type: bool
    required: false
    default: true
  excluded_file_extensions:
    description:
      - List of file extensions (without the leading dot, e.g. C(txt), C(iso)) that will be excluded from the
        antivirus scan.
    type: list
    elements: str
    required: false
  mount_target_reference:
    description:
      - External ID of the mount target (SMB share) that this policy applies to.
      - Set to C(null) or omit to make this a global (file-server wide) policy.
    type: str
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
- name: Create global virus scan policy
  nutanix.ncp.ntnx_virus_scan_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "b6b74a04-5b9c-4a5f-9e2e-3b1d5f6d1a11"
    scan_timeout_interval_secs: 60
    is_scan_on_write_enabled: true
    is_scan_on_read_enabled: true
    max_file_size_threshold_bytes: 10485760
    is_file_access_blocked: false
    is_anti_virus_enabled: true
    excluded_file_extensions:
      - iso
      - tmp
  register: result

- name: Update virus scan policy
  nutanix.ncp.ntnx_virus_scan_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "b6b74a04-5b9c-4a5f-9e2e-3b1d5f6d1a11"
    ext_id: "5e17ff0d-3a55-4c78-95bb-83a5b6b6bda1"
    scan_timeout_interval_secs: 120
    is_scan_on_write_enabled: true
    is_scan_on_read_enabled: false
    max_file_size_threshold_bytes: 20971520
    is_file_access_blocked: true
    is_anti_virus_enabled: true
    excluded_file_extensions:
      - iso
      - tmp
      - log
  register: result

- name: Delete virus scan policy
  nutanix.ncp.ntnx_virus_scan_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "b6b74a04-5b9c-4a5f-9e2e-3b1d5f6d1a11"
    ext_id: "5e17ff0d-3a55-4c78-95bb-83a5b6b6bda1"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a virus scan policy.
    - If the operation is create or update and C(wait) is true, it returns the virus scan policy details.
    - If the operation is create or update and C(wait) is false, it returns the submitted task details.
    - If the operation is delete, it returns the task details.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "5e17ff0d-3a55-4c78-95bb-83a5b6b6bda1",
      "excluded_file_extensions": ["iso", "tmp"],
      "is_anti_virus_enabled": true,
      "is_file_access_blocked": false,
      "is_scan_on_read_enabled": true,
      "is_scan_on_write_enabled": true,
      "links": null,
      "max_file_size_threshold_bytes": 10485760,
      "mount_target_reference": null,
      "scan_timeout_interval_secs": 60,
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
    - The external ID of the virus scan policy.
  returned: always
  type: str
  sample: "5e17ff0d-3a55-4c78-95bb-83a5b6b6bda1"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
  returned: always
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
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating virus scan policy"
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
    get_virus_scan_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_virus_scan_policy  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
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
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        scan_timeout_interval_secs=dict(type="int"),
        is_scan_on_write_enabled=dict(type="bool", default=True),
        is_scan_on_read_enabled=dict(type="bool", default=True),
        max_file_size_threshold_bytes=dict(type="int"),
        is_file_access_blocked=dict(type="bool", default=False),
        is_anti_virus_enabled=dict(type="bool", default=True),
        excluded_file_extensions=dict(type="list", elements="str"),
        mount_target_reference=dict(type="str"),
    )
    return module_args


def _fetch_virus_scan_policy(module, api_instance, file_server_ext_id, ext_id):
    """Return the persisted virus scan policy for the given IDs."""
    return get_virus_scan_policy(module, api_instance, file_server_ext_id, ext_id)


def create_virus_scan_policy(module, result, api_instance):
    """Create a virus scan policy on the target file server."""
    file_server_ext_id = module.params.get("file_server_ext_id")
    sg = SpecGenerator(module)
    default_spec = files_sdk.VirusScanPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create virus scan policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_virus_scan_policy(
            fileServerExtId=file_server_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating virus scan policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_resp, rel=TASK_CONSTANTS.RelEntityType.VIRUS_SCAN_POLICY
        )
        if not ext_id:
            ext_id = get_entity_ext_id_from_task(task_resp)
        if ext_id:
            result["ext_id"] = ext_id
            fetched = _fetch_virus_scan_policy(
                module, api_instance, file_server_ext_id, ext_id
            )
            result["response"] = strip_internal_attributes(fetched.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Virus Scan Policy"
                ),
                msg="Failed to get entity ext_id from task for Virus Scan Policy",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """Return True when the target virus scan policy already matches the desired spec."""
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    return old_spec_dict == update_spec_dict


def update_virus_scan_policy(module, result, api_instance):
    """Update an existing virus scan policy, honoring etag and idempotency."""
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current = None
    try:
        current = api_instance.get_virus_scan_policy_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virus scan policy for update",
        )

    old_spec = current.data
    etag = get_etag(data=current)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating virus scan policy", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update virus scan policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = None
    try:
        resp = api_instance.update_virus_scan_policy_by_id(
            fileServerExtId=file_server_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating virus scan policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        fetched = _fetch_virus_scan_policy(
            module, api_instance, file_server_ext_id, ext_id
        )
        result["response"] = strip_internal_attributes(fetched.to_dict())
    result["changed"] = True


def delete_virus_scan_policy(module, result, api_instance):
    """Delete a virus scan policy by external ID."""
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Virus scan policy with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.delete_virus_scan_policy_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting virus scan policy",
        )

    task_ext_id = resp.data.ext_id
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
    api_instance = get_virus_scan_policies_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_virus_scan_policy(module, result, api_instance)
        else:
            create_virus_scan_policy(module, result, api_instance)
    else:
        delete_virus_scan_policy(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
