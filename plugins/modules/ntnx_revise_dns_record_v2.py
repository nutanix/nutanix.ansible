#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_revise_dns_record_v2
short_description: Revise DNS records on the DNS server for a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to revise (add or remove) DNS records of a Nutanix
    Files file server on the DNS server through Nutanix Prism Central.
  - It invokes the file server C($actions/revise-dns-records) action.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Revise DNS records of a Files file server) -
    Required Roles: File Server Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported for this action module. If C(state) is
        anything other than C(present) the module will fail.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external identifier of the file server on which the DNS records
        should be revised.
      - Required for the revise DNS records action.
    type: str
    required: true
  preferred_name_server:
    description:
      - Preferred name server for the file server.
      - Optional. When not provided, the file server default preferred name
        server is used by the platform.
    type: str
    required: false
  action:
    description:
      - Type of revise action to perform on the DNS server.
      - C(ADD) will add the file server DNS records on the DNS server.
      - C(REMOVE) will remove the file server DNS records from the DNS server.
    type: str
    choices:
      - ADD
      - REMOVE
    required: false
  credential:
    description:
      - Credential used to authenticate with the DNS server when adding or
        removing records that require administrative rights (for example
        Active Directory integrated DNS zones).
    type: dict
    required: false
    suboptions:
      username:
        description:
          - Name of the user with permission to update DNS records on the
            DNS server.
        type: str
        required: true
      password:
        description:
          - Password of the user with permission to update DNS records on the
            DNS server.
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
- name: Revise DNS records - add file server records on the DNS server
  nutanix.ncp.ntnx_revise_dns_record_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "b1c9c4a2-1cbb-4c9d-8f92-2f01f76fed44"
    preferred_name_server: "10.44.76.10"
    action: ADD
    credential:
      username: "administrator@example.com"
      password: "SuperSecret123"
  register: result
  ignore_errors: true

- name: Revise DNS records - remove file server records from the DNS server
  nutanix.ncp.ntnx_revise_dns_record_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "b1c9c4a2-1cbb-4c9d-8f92-2f01f76fed44"
    preferred_name_server: "10.44.76.10"
    action: REMOVE
    credential:
      username: "administrator@example.com"
      password: "SuperSecret123"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for revising DNS records on the DNS server for a file server.
    - Task details if C(wait) is true.
    - Task reference (initial response) if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T09:20:12.421589+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T09:20:06.187333+00:00",
      "entities_affected": [
        {
          "ext_id": "b1c9c4a2-1cbb-4c9d-8f92-2f01f76fed44",
          "rel": "files:config:file-server"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T09:20:12.421589+00:00",
      "legacy_error_message": null,
      "operation": "kFileServerReviseDnsRecords",
      "operation_description": "Revise DNS records of a file server",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-21T09:20:06.198221+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external identifier of the task created for the revise DNS records action.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description:
    - The external identifier of the file server on which the DNS records were revised.
  returned: always
  type: str
  sample: "b1c9c4a2-1cbb-4c9d-8f92-2f01f76fed44"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description:
    - Contextual message describing the outcome of the action or any error encountered.
  returned: When there is an error or informational message
  type: str
  sample: "Api Exception raised while revising DNS records for file server"

error:
  description:
    - Error details if the API call fails.
  returned: When an error occurs
  type: str
  sample: "Failed to get etag for file server"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_dns_api_instance,
    get_etag,
    get_file_servers_api_instance,
)
from ..module_utils.v4.files.helpers import get_file_server  # noqa: E402
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
            no_log=False,
            options=credential_spec,
            obj=files_sdk.Credential,
        ),
    )

    return module_args


def revise_dns_records(module, api_instance, file_servers_api, result):
    """Revise DNS records for a file server via the DnsApi action endpoint."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = files_sdk.DnsRecordSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for revise DNS records", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    file_server = get_file_server(module, file_servers_api, ext_id)
    etag = get_etag(file_server)
    if not etag:
        module.fail_json(msg="Failed to get etag for file server", **result)
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.revise_dns_records(extId=ext_id, body=spec, **kwargs)
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
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_dns_api_instance(module)
    file_servers_api = get_file_servers_api_instance(module)
    revise_dns_records(module, api_instance, file_servers_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
