#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_dns_record_v2
short_description: Revise and verify DNS records for a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to revise (add or remove) and verify DNS records for a
    Nutanix Files file server on the configured DNS server.
  - Reviser and verify are asynchronous operations backed by the Nutanix Files
    v4 DNS API and return a task ext_id.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Revise DNS records) -
    Required Roles: File Server Admin, Prism Admin, Super Admin
  - >-
    B(Verify DNS records) -
    Required Roles: File Server Admin, File Server Viewer, Prism Admin,
    Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported since DNS records are managed through
        action APIs (revise / verify) that operate on the referenced file
        server rather than a separate DNS record entity.
    type: str
    choices:
      - present
    default: present
  file_server_ext_id:
    description:
      - The external identifier of the file server whose DNS records will be
        revised or verified.
    type: str
    required: true
  operation:
    description:
      - The DNS operation to perform against the file server.
      - C(revise) adds or removes DNS records on the DNS server (controlled by
        the C(dns_action) parameter).
      - C(verify) verifies that the DNS records of the file server exist on the
        DNS server.
    type: str
    choices:
      - revise
      - verify
    default: revise
  dns_action:
    description:
      - The DNS action to perform when C(operation=revise).
      - C(ADD) adds DNS entries for the file server to the DNS server.
      - C(REMOVE) removes DNS entries for the file server from the DNS server.
      - Required when C(operation=revise). Ignored when C(operation=verify).
    type: str
    choices:
      - ADD
      - REMOVE
  preferred_name_server:
    description:
      - The preferred name server that should be contacted for the DNS revise
        operation.
      - Applicable only when C(operation=revise).
    type: str
  credential:
    description:
      - Credential used to authenticate against the DNS server.
      - Required when C(operation=revise). Optional when C(operation=verify).
    type: dict
    suboptions:
      username:
        description:
          - Username used to authenticate against the DNS server.
        type: str
        required: true
      password:
        description:
          - Password associated with the C(username) used to authenticate
            against the DNS server.
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
- name: Revise (add) DNS records for a file server
  nutanix.ncp.ntnx_dns_record_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    operation: revise
    dns_action: ADD
    preferred_name_server: "dns.example.com"
    credential:
      username: "administrator@example.com"
      password: "SuperSecret1"
  register: result
  ignore_errors: true

- name: Revise (remove) DNS records for a file server
  nutanix.ncp.ntnx_dns_record_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    operation: revise
    dns_action: REMOVE
    preferred_name_server: "dns.example.com"
    credential:
      username: "administrator@example.com"
      password: "SuperSecret1"
  register: result
  ignore_errors: true

- name: Verify DNS records for a file server (without credentials)
  nutanix.ncp.ntnx_dns_record_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    operation: verify
  register: result
  ignore_errors: true

- name: Verify DNS records for a file server (with credentials)
  nutanix.ncp.ntnx_dns_record_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    operation: verify
    credential:
      username: "administrator@example.com"
      password: "SuperSecret1"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for revising or verifying DNS records for the file server.
    - If C(wait) is true, this is the completed task object.
    - If C(wait) is false, this is the initial task reference returned by
      the DNS action API.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T06:20:11.524581+00:00",
      "created_time": "2026-07-21T06:20:07.167906+00:00",
      "entities_affected": [
        {
          "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
          "rel": "files:config:file-server"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T06:20:11.524581+00:00",
      "legacy_error_message": null,
      "operation": "ReviseDnsRecords",
      "operation_description": "Revise DNS records",
      "progress_percentage": 100,
      "started_time": "2026-07-21T06:20:07.185754+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task started by the DNS operation.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description:
    - The external ID of the file server on which the DNS operation was
      performed.
  returned: always
  type: str
  sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"

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

msg:
  description:
    - Contextual message emitted by the module. Populated on validation
      errors, in check mode, and when an operation is skipped.
  returned: When there is an error, in check mode, or on validation failures
  type: str
  sample: "Api Exception raised while revising DNS records for file server"

error:
  description: Details about any error encountered while running the module.
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

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import get_dns_api_instance  # noqa: E402
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

    credential_spec = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )

    module_args = dict(
        state=dict(type="str", choices=["present"], default="present"),
        file_server_ext_id=dict(type="str", required=True),
        operation=dict(
            type="str",
            choices=["revise", "verify"],
            default="revise",
        ),
        dns_action=dict(
            type="str",
            choices=["ADD", "REMOVE"],
            obj=files_sdk.DnsActionType,
        ),
        preferred_name_server=dict(type="str"),
        credential=dict(
            type="dict",
            options=credential_spec,
            obj=files_sdk.Credential,
        ),
    )
    return module_args


def _build_dns_record_spec(module, result, require_all_revise_fields=True):
    """
    Build a :class:`DnsRecordSpec` populated from the module params.

    When ``require_all_revise_fields`` is True (revise flow), the module
    parameters ``dns_action``, ``preferred_name_server`` and ``credential``
    are validated up front. The verify flow may omit ``credential``.
    """
    if require_all_revise_fields:
        validate_required_params(
            module,
            ["dns_action", "preferred_name_server", "credential"],
        )

    sg = SpecGenerator(module)
    default_spec = files_sdk.DnsRecordSpec()

    attrs = {
        "preferred_name_server": module.params.get("preferred_name_server"),
        "credential": module.params.get("credential"),
    }
    dns_action = module.params.get("dns_action")
    if dns_action is not None:
        attrs["action"] = dns_action

    spec, err = sg.generate_spec(
        obj=default_spec,
        attr=attrs,
        module_args={
            "preferred_name_server": {"type": "str"},
            "action": {"type": "str"},
            "credential": {
                "type": "dict",
                "options": {
                    "username": {"type": "str"},
                    "password": {"type": "str", "no_log": True},
                },
                "obj": files_sdk.Credential,
            },
        },
    )
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating DNS record spec", **result)
    return spec


def revise_dns_records(module, result, api_instance):
    """
    Revise (add / remove) DNS records for the file server referenced by
    ``file_server_ext_id`` using ``DnsApi.revise_dns_records``.
    """
    ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = ext_id

    spec = _build_dns_record_spec(module, result, require_all_revise_fields=True)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.revise_dns_records(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while revising DNS records for file server",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def verify_dns_records(module, result, api_instance):
    """
    Verify DNS records for the file server referenced by
    ``file_server_ext_id`` using ``DnsApi.verify_dns_records``.
    """
    ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = ext_id

    spec = None
    if module.params.get("credential") is not None:
        spec = _build_dns_record_spec(module, result, require_all_revise_fields=False)

    if module.check_mode:
        if spec is not None:
            result["response"] = strip_internal_attributes(spec.to_dict())
        else:
            result["msg"] = (
                "DNS records verification for file server '{0}' will be "
                "triggered.".format(ext_id)
            )
        return

    try:
        if spec is not None:
            resp = api_instance.verify_dns_records(extId=ext_id, body=spec)
        else:
            resp = api_instance.verify_dns_records(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while verifying DNS records for file server",
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
        required_if=[
            (
                "operation",
                "revise",
                ("dns_action", "preferred_name_server", "credential"),
            ),
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
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_dns_api_instance(module)
    operation = module.params.get("operation")

    if operation == "revise":
        revise_dns_records(module, result, api_instance)
    else:
        verify_dns_records(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
