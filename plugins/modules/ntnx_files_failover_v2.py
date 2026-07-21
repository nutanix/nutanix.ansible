#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_failover_v2
short_description: Perform data replication failover between Nutanix File Servers
version_added: 2.7.0
description:
    - Perform data replication failover between a primary and a secondary Nutanix File Server.
    - Failover switches client file access from the primary file server to the secondary
      file server for a given replication policy.
    - Supports planned failover, unplanned failover and failback flows through the C(type) parameter.
    - Optionally synchronizes DNS records and Active Directory configuration during the failover.
    - This module uses PC v4 APIs based SDKs.
options:
    state:
        description:
            - State of the module.
            - If C(state) is set to C(present), the module will perform the failover action.
        type: str
        choices:
            - present
        default: present
    primary_file_server_ext_id:
        description:
            - The external identifier of the primary file server for the replication.
            - Must be a valid UUID.
        type: str
        required: true
    secondary_file_server_ext_id:
        description:
            - The external identifier of the secondary file server for the replication.
            - Must be a valid UUID.
        type: str
        required: true
    type:
        description:
            - Type of failover to perform.
            - C(PLANNED) performs a graceful failover, completing a final synchronization
              from the primary before switching workloads to the secondary.
            - C(UNPLANNED) performs a forced failover when the primary is unavailable,
              using the last replicated checkpoint.
            - C(FAILBACK) reverses the failover to return workloads to the original
              primary file server.
        type: str
        choices:
            - PLANNED
            - UNPLANNED
            - FAILBACK
    active_directory:
        description:
            - Configuration to access the file server active directory server during failover.
        type: dict
        required: false
        suboptions:
            credential:
                description:
                    - Credentials used to authenticate to the active directory server.
                type: dict
                required: false
                suboptions:
                    username:
                        description:
                            - Username for the active directory server.
                        type: str
                        required: false
                    password:
                        description:
                            - Password for the active directory server.
                        type: str
                        required: false
            preferred_domain_controller:
                description:
                    - Preferred domain controller for the active directory server.
                type: str
                required: false
    dns:
        description:
            - DNS record specification used to update DNS entries during the failover.
        type: dict
        required: false
        suboptions:
            preferred_name_server:
                description:
                    - IP address or FQDN of the preferred DNS name server used to update
                      DNS records during the failover.
                type: str
                required: false
            action:
                description:
                    - The DNS record action to perform.
                type: str
                required: false
                choices:
                    - ADD
                    - REMOVE
            credential:
                description:
                    - Credentials used to authenticate to the DNS server when it requires
                      authenticated updates.
                type: dict
                required: false
                suboptions:
                    username:
                        description:
                            - Username for the DNS server.
                        type: str
                        required: false
                    password:
                        description:
                            - Password for the DNS server.
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
- name: Perform a planned data replication failover between two file servers
  nutanix.ncp.ntnx_files_failover_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    primary_file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    secondary_file_server_ext_id: "5b2e4e93-2222-3333-7777-a015d302eec2"
    type: PLANNED
  register: result
  ignore_errors: true

- name: Perform an unplanned failover with DNS updates and AD credentials
  nutanix.ncp.ntnx_files_failover_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    primary_file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    secondary_file_server_ext_id: "5b2e4e93-2222-3333-7777-a015d302eec2"
    type: UNPLANNED
    active_directory:
      credential:
        username: "ad_user@example.com"
        password: "AdPassword123!"
      preferred_domain_controller: "dc1.example.com"
    dns:
      preferred_name_server: "10.10.10.10"
      action: ADD
      credential:
        username: "dns_user"
        password: "DnsPassword123!"
  register: result
  ignore_errors: true

- name: Perform a failback to the original file server
  nutanix.ncp.ntnx_files_failover_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    primary_file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    secondary_file_server_ext_id: "5b2e4e93-2222-3333-7777-a015d302eec2"
    type: FAILBACK
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for performing data replication failover.
        - Task details if C(wait) is true, contains task completion state and entities affected.
        - Task reference if C(wait) is false.
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
                    "ext_id": "9c1e537d-6777-4c22-5d41-ddd0c3337aa9",
                    "rel": "files:config:file-server"
                },
                {
                    "ext_id": "5b2e4e93-2222-3333-7777-a015d302eec2",
                    "rel": "files:config:file-server"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T06:26:51.524581+00:00",
            "legacy_error_message": null,
            "operation": "Failover",
            "operation_description": "Perform data replication failover",
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
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while performing files failover"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Failed generating files failover spec"

failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the primary file server for the failover operation.
    returned: always
    type: str
    sample: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_replication_policies_api_instance,
)
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
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
    )

    active_directory_spec = dict(
        credential=dict(
            type="dict",
            options=credential_spec,
            obj=files_sdk.Credential,
        ),
        preferred_domain_controller=dict(type="str"),
    )

    dns_spec = dict(
        preferred_name_server=dict(type="str"),
        action=dict(type="str", choices=["ADD", "REMOVE"], obj=files_sdk.DnsActionType),
        credential=dict(
            type="dict",
            options=credential_spec,
            obj=files_sdk.Credential,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        primary_file_server_ext_id=dict(type="str", required=True),
        secondary_file_server_ext_id=dict(type="str", required=True),
        type=dict(
            type="str",
            choices=["PLANNED", "UNPLANNED", "FAILBACK"],
            obj=files_sdk.FailoverType,
        ),
        active_directory=dict(
            type="dict",
            options=active_directory_spec,
            obj=files_sdk.ADServerSpec,
        ),
        dns=dict(
            type="dict",
            options=dns_spec,
            obj=files_sdk.DnsRecordSpec,
        ),
    )

    return module_args


def perform_files_failover(module, api_instance, result):
    validate_required_params(
        module,
        ["primary_file_server_ext_id", "secondary_file_server_ext_id"],
    )

    result["ext_id"] = module.params.get("primary_file_server_ext_id")

    sg = SpecGenerator(module)
    default_spec = files_sdk.FailoverSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating files failover spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.failover(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing files failover",
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
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_replication_policies_api_instance(module)
    perform_files_failover(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
