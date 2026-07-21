#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_test_connection_antivirus_server_v2
short_description: Test the connection to an antivirus server registered with a Nutanix Files file server
version_added: 2.7.0
description:
    - Trigger a synchronous connectivity probe from a Nutanix Files file server
      to a previously configured antivirus (ICAP) server.
    - The probe validates that the file server can reach the specified antivirus
      server and updates the C(connection_status) of that antivirus server in
      the Files metadata store.
    - This module does not modify the antivirus server configuration itself; it
      only reports the outcome of the test-connection call.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Test antivirus server connection) -
      Required Roles: File Server Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported because this module executes a
              one-shot connectivity check action.
        type: str
        choices:
            - present
        default: present
    file_server_ext_id:
        description:
            - External identifier of the Nutanix Files file server that owns
              the target antivirus server.
        type: str
        required: true
    ext_id:
        description:
            - External identifier of the antivirus server whose connectivity
              is to be tested.
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
- name: Test connection to antivirus server
  nutanix.ncp.ntnx_test_connection_antivirus_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for testing the antivirus server connection.
        - Task details when C(wait) is true.
        - Task reference details when C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2026-07-21T09:12:44.512983+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T09:12:39.108211+00:00",
            "entities_affected": [
                {
                    "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
                    "rel": "files:config:anti-virus-server"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T09:12:44.512983+00:00",
            "legacy_error_message": null,
            "operation": "TestConnectionAntivirusServer",
            "operation_description": "Test antivirus server connection",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T09:12:39.130522+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: Indicates whether the module made any change on the cluster.
    returned: always
    type: bool
    sample: true

msg:
    description: Human readable message describing the outcome or an error.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while testing antivirus server connection"

error:
    description:
        - Error details captured when an API failure occurs while executing
          the test-connection action.
    returned: when an error occurs
    type: str
    sample: "Not Found"

failed:
    description: Indicates whether the module failed to complete the action.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external identifier of the asynchronous task backing the action.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external identifier of the antivirus server that was tested.
    returned: always
    type: str
    sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_antivirus_servers_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )

    return module_args


def test_connection_antivirus_server(module, result, api_instance):
    """
    Trigger the antivirus server connectivity probe via the Files v4 API.

    The action is stateful on the cluster side (it updates the
    ``connection_status`` for the antivirus server), so ``changed`` is set to
    ``True`` whenever the request is actually sent. In ``check_mode`` we skip
    the API call and return the pending action description instead.

    Args:
        module (AnsibleModule): Ansible module wrapper used for check mode,
            parameter access, and error reporting.
        result (dict): Mutable result dict populated in place with the API
            response, task ext_id, and status flags.
        api_instance: ``AntivirusServersApi`` receiver used to invoke the
            test-connection endpoint.

    Returns:
        None: Populates ``result`` in place; on failure the module exits via
        :func:`raise_api_exception`.
    """
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Connection test for antivirus server with ext_id: {0} on file server "
            "with ext_id: {1} will be triggered.".format(ext_id, file_server_ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.test_connection_antivirus_server(
            fileServerExtId=file_server_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while testing antivirus server connection",
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

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_antivirus_servers_api_instance(module)
    test_connection_antivirus_server(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
