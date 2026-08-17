#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_nfected_file_v2
short_description: Manage infected files on Nutanix Files file servers
version_added: 2.5.0
description:
  - This module allows you to manage infected files detected by the antivirus
    (ICAP) scanner on a Nutanix Files file server via the v4 API.
  - Use C(state=present) with C(ext_id) and a valid C(action) to run a fix
    action on an infected file (quarantine, unquarantine, rescan or reset).
  - Use C(state=absent) with C(ext_id) to remove the infected file record.
  - The infected file entry itself is created by the ICAP scan pipeline when a
    file is flagged; this module does not create infected files.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Fix an infected file) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Delete an infected file) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is provided then the
        operation will run a fix C(action) on the infected file.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the
        infected file record will be deleted.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  file_server_ext_id:
    description:
      - The external ID of the parent Nutanix Files file server that owns the
        infected file.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the infected file.
      - Required for fix (state=present) and delete (state=absent) operations.
    type: str
    required: true
  action:
    description:
      - The security action to apply to the infected file when
        C(state=present).
      - C(QUARANTINE) marks the file as quarantined so SMB clients are denied
        access.
      - C(UNQUARANTINE) manually clears an infected file back to accessible
        state (useful for false positives).
      - C(RESCAN) requests the ICAP daemon to scan the file again.
      - C(RESET) removes the antivirus metadata so the file will be rescanned
        on next access.
      - Required when C(state=present).
    type: str
    choices:
      - QUARANTINE
      - UNQUARANTINE
      - RESCAN
      - RESET
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Nutanix (@nutanix)
"""

EXAMPLES = r"""
- name: Quarantine an infected file
  nutanix.ncp.ntnx_files_nfected_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "d1e6f2fa-5c8a-4d2f-9a3b-1a2b3c4d5e6f"
    ext_id: "b7a4c8e6-1234-5678-9abc-def012345678"
    action: QUARANTINE
  register: result

- name: Unquarantine an infected file (false positive)
  nutanix.ncp.ntnx_files_nfected_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "d1e6f2fa-5c8a-4d2f-9a3b-1a2b3c4d5e6f"
    ext_id: "b7a4c8e6-1234-5678-9abc-def012345678"
    action: UNQUARANTINE
  register: result

- name: Trigger a rescan of an infected file
  nutanix.ncp.ntnx_files_nfected_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "d1e6f2fa-5c8a-4d2f-9a3b-1a2b3c4d5e6f"
    ext_id: "b7a4c8e6-1234-5678-9abc-def012345678"
    action: RESCAN
  register: result

- name: Reset antivirus metadata for an infected file
  nutanix.ncp.ntnx_files_nfected_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "d1e6f2fa-5c8a-4d2f-9a3b-1a2b3c4d5e6f"
    ext_id: "b7a4c8e6-1234-5678-9abc-def012345678"
    action: RESET
  register: result

- name: Delete an infected file record
  nutanix.ncp.ntnx_files_nfected_file_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "d1e6f2fa-5c8a-4d2f-9a3b-1a2b3c4d5e6f"
    ext_id: "b7a4c8e6-1234-5678-9abc-def012345678"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for running a fix action or deleting an infected file.
    - If the operation is fix and C(wait) is true, it will return the refreshed
      infected file details.
    - If the operation is fix and C(wait) is false, it will return the task
      details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "b7a4c8e6-1234-5678-9abc-def012345678",
      "is_quarantined": true,
      "links": null,
      "mount_target_ext_id": "aa11bb22-cc33-dd44-ee55-ff6677889900",
      "partner_server": "icap-01.example.com",
      "path": "/share/malware/eicar.txt",
      "scan_time": "2026-07-21T05:12:33.123456+00:00",
      "tenant_id": null,
      "threat_description": "EICAR-Test-File"
    }

task_ext_id:
  description:
    - The external ID of the async Ergon task created by the fix or delete
      operation.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the infected file the operation was performed on.
  returned: always
  type: str
  sample: "b7a4c8e6-1234-5678-9abc-def012345678"

file_server_ext_id:
  description:
    - The external ID of the parent file server.
  returned: always
  type: str
  sample: "d1e6f2fa-5c8a-4d2f-9a3b-1a2b3c4d5e6f"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
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
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation).
  type: str
  sample: "Api Exception raised while running fix action on infected file"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        action=dict(
            type="str",
            required=False,
            choices=["QUARANTINE", "UNQUARANTINE", "RESCAN", "RESET"],
            obj=files_sdk.InfectedFileActionType,
        ),
    )
    return module_args


def fix_infected_file(module, result, api_instance):
    """Run a fix (security) action on an infected file."""
    validate_required_params(module, ["file_server_ext_id", "ext_id", "action"])

    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["file_server_ext_id"] = file_server_ext_id
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = files_sdk.InfectedFileFixSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating fix infected file spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current = get_infected_file(module, api_instance, file_server_ext_id, ext_id)
    etag = get_etag(data=current)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.fix_infected_file(
            fileServerExtId=file_server_ext_id,
            extId=ext_id,
            body=spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while running fix action on infected file",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        refreshed = get_infected_file(module, api_instance, file_server_ext_id, ext_id)
        if refreshed is None:
            raise_api_exception(
                module=module,
                exception=Exception("Failed to refresh infected file after fix action"),
                msg="Failed to refresh infected file after fix action",
            )
        result["response"] = strip_internal_attributes(refreshed.to_dict())
    result["changed"] = True


def delete_infected_file(module, result, api_instance):
    """Delete an infected file record from the file server."""
    validate_required_params(module, ["file_server_ext_id", "ext_id"])

    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["file_server_ext_id"] = file_server_ext_id
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Infected file with ext_id:{0} on file server ext_id:{1} will be deleted.".format(
                ext_id, file_server_ext_id
            )
        )
        return

    current = get_infected_file(module, api_instance, file_server_ext_id, ext_id)
    etag = get_etag(data=current)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.delete_infected_file_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting infected file",
        )

    task_ext_id = resp.data.ext_id if resp and resp.data else None
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    elif resp and resp.data:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("action",)),
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
        "file_server_ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }

    api_instance = get_infected_files_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        fix_infected_file(module, result, api_instance)
    else:
        delete_infected_file(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
