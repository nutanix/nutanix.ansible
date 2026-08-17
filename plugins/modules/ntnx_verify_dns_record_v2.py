#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_verify_dns_record_v2
short_description: Verify DNS records of a Nutanix Files file server
version_added: 2.7.0
description:
    - Verify the DNS records of a Nutanix Files file server on its DNS server.
    - This is a validation-only action; it does not create, modify, or delete DNS records.
    - It triggers a lookup of the expected A, AAAA, and PTR records for the file server
      and updates the internal DNS entries verification state.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Verify DNS records of a file server) -
      Required Roles: Files Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will verify the DNS records of the file server.
            - Only C(present) is supported for this action module.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the file server whose DNS records need to be verified.
        type: str
        required: true
    preferred_name_server:
        description:
            - Preferred name server used for the DNS verification.
            - When omitted, the file server's default DNS servers are used.
        type: str
        required: false
    action:
        description:
            - Type of DNS action to perform on the DNS records to verify.
            - C(ADD) verifies that the expected DNS records are present on the DNS server.
            - C(REMOVE) verifies that the expected DNS records are absent from the DNS server.
        type: str
        choices:
            - ADD
            - REMOVE
        required: false
    credential:
        description:
            - User credential used by the DNS verification workflow.
            - Required by the API gateway when a credentialed DNS server is used
              (e.g. Active Directory integrated DNS).
        type: dict
        required: false
        suboptions:
            username:
                description:
                    - Name of the user used to authenticate against the DNS server.
                type: str
                required: true
            password:
                description:
                    - Password of the user used to authenticate against the DNS server.
                    - This field is never logged.
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
- name: Verify DNS records of a file server with default settings
  nutanix.ncp.ntnx_verify_dns_record_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b1cbe1cb-fc4a-4d1a-9c74-1c1ee1cbf1cb"
  register: result
  ignore_errors: true

- name: Verify DNS records of a file server with all attributes
  nutanix.ncp.ntnx_verify_dns_record_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b1cbe1cb-fc4a-4d1a-9c74-1c1ee1cbf1cb"
    preferred_name_server: "dns1.example.com"
    action: "ADD"
    credential:
      username: "administrator@example.com"
      password: "P@ssw0rd!"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for verifying DNS records of a Nutanix Files file server.
        - Task details when C(wait) is true.
        - Initial task submission details when C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-21T09:34:11.524581+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T09:34:07.167906+00:00",
            "entities_affected": [
                {
                    "ext_id": "b1cbe1cb-fc4a-4d1a-9c74-1c1ee1cbf1cb",
                    "rel": "files:config:file-server"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T09:34:11.524581+00:00",
            "legacy_error_message": null,
            "operation": "VerifyDnsRecords",
            "operation_description": "Verify DNS records of file server",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T09:34:07.185754+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
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
    sample: "Api Exception raised while verifying DNS records for file server"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Failed generating spec for verifying DNS records"

failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the Ergon task that runs the DNS record verification.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the file server whose DNS records were verified.
    returned: always
    type: str
    sample: "b1cbe1cb-fc4a-4d1a-9c74-1c1ee1cbf1cb"
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
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        preferred_name_server=dict(type="str", required=False),
        action=dict(type="str", required=False, choices=["ADD", "REMOVE"]),
        credential=dict(
            type="dict",
            required=False,
            options=credential_spec,
            obj=files_sdk.Credential,
            no_log=False,
        ),
    )

    return module_args


def verify_dns_records(module, dns_api, result):
    """
    Trigger DNS record verification for a Nutanix Files file server.

    The v4 verify-dns-records API accepts an optional DnsRecordSpec body
    containing an optional preferred name server, DNS action type, and
    user credential. It creates an Ergon task that performs A/AAAA/PTR
    lookups and updates the file server's DNS verification state.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["ext_id"])

    sg = SpecGenerator(module)
    default_spec = files_sdk.DnsRecordSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for verifying DNS records", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = dns_api.verify_dns_records(extId=ext_id, body=spec)
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
    dns_api = get_dns_api_instance(module)
    verify_dns_records(module, dns_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
