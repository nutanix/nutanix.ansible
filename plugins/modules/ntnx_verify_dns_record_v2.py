#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_verify_dns_record_v2
short_description: Verify DNS records of a Nutanix Files file server on the DNS server
version_added: 2.7.0
description:
    - Verify DNS records of a Nutanix Files file server on the DNS server.
    - Triggers the C(verify-dns-records) action on the given file server.
    - Optionally accepts a preferred name server, a DNS action type and DNS server credentials.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Verify DNS records for file server.) -
      Required Roles: Prism Admin, Super Admin, File Server Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will trigger the verify-dns-records action on the file server.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the file server whose DNS records must be verified.
        type: str
        required: true
    preferred_name_server:
        description:
            - Preferred name server (FQDN) to use for the DNS verification.
            - Must be a fully qualified domain name (e.g. C(ns1.example.com)).
        type: str
    action:
        description:
            - DNS action type. Applicable only to the revise DNS API but accepted here so the same
              spec object (DnsRecordSpec) can be re-used by the SDK.
            - C(ADD) adds DNS entries to the DNS server, C(REMOVE) removes DNS entries from the DNS server.
        type: str
        choices:
            - ADD
            - REMOVE
    credential:
        description:
            - Credentials for the DNS server used to verify the DNS records.
        type: dict
        suboptions:
            username:
                description:
                    - Name of the DNS server user (max 256 chars).
                type: str
            password:
                description:
                    - Password of the DNS server user.
                type: str
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
- name: Verify DNS records of a file server (no additional parameters)
  nutanix.ncp.ntnx_verify_dns_record_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
  register: result
  ignore_errors: true

- name: Verify DNS records of a file server with all optional parameters
  nutanix.ncp.ntnx_verify_dns_record_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    preferred_name_server: "ns1.example.com"
    action: "ADD"
    credential:
      username: "dns_admin"
      password: "dns_secret"
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
    description:
        - Response for verifying DNS records of a file server on the DNS server.
        - File server DNS verification task details when C(wait) is true.
        - Task submission details when C(wait) is false.
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
            "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
            "rel": "files:config:file-server"
            }
        ],
        "error_messages": null,
        "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
        "is_cancelable": false,
        "last_updated_time": "2026-07-21T06:26:51.524581+00:00",
        "legacy_error_message": null,
        "operation": "VerifyDnsRecords",
        "operation_description": "Verify DNS records",
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
    returned: When there is an error
    type: str
    sample: "Api Exception raised while verifying DNS records of file server"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str
    sample: "Failed generating spec for verify DNS records"

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
    description: The external ID of the file server whose DNS records were verified
    returned: always
    type: str
    sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
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
)

SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    credential_spec = dict(
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        preferred_name_server=dict(type="str"),
        action=dict(type="str", choices=["ADD", "REMOVE"]),
        credential=dict(
            type="dict",
            options=credential_spec,
            no_log=False,
        ),
    )

    return module_args


def verify_dns_records(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = files_sdk.DnsRecordSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for verify DNS records", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    kwargs = {}
    if (
        module.params.get("preferred_name_server")
        or module.params.get("action")
        or module.params.get("credential")
    ):
        kwargs["body"] = spec

    resp = None
    try:
        resp = api_instance.verify_dns_records(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while verifying DNS records of file server",
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
    api_instance = get_dns_api_instance(module)
    verify_dns_records(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
