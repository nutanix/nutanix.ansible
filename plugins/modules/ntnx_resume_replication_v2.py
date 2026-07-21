#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_resume_replication_v2
short_description: Resume mount target level replication after a failover in Nutanix Files
version_added: 2.5.0
description:
  - Resume replication on Nutanix Files mount targets after a failover has been performed.
  - This module invokes the resume replication action on the file server replication policy.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Resume Replication) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module resumes replication.
    type: str
    choices:
      - present
    default: present
  replication_direction:
    description:
      - The direction in which replication should resume between the primary and secondary file servers.
    type: str
    choices:
      - PRIMARY_TO_SECONDARY
      - SECONDARY_TO_PRIMARY
  primary_file_server_ext_id:
    description:
      - The external identifier of the primary file server in the replication pair.
    type: str
  secondary_file_server_ext_id:
    description:
      - The external identifier of the secondary file server in the replication pair.
    type: str
  type:
    description:
      - The type of failover that was originally performed.
      - This is used to determine how replication should resume.
    type: str
    choices:
      - PLANNED
      - UNPLANNED
      - FAILBACK
  active_directory:
    description:
      - Active Directory server details used to re-register SPN records when
        replication resumes.
    type: dict
    suboptions:
      preferred_domain_controller:
        description:
          - The FQDN or IP address of the preferred domain controller to reach
            for AD updates.
        type: str
      credential:
        description:
          - Credentials used to authenticate against Active Directory.
        type: dict
        suboptions:
          username:
            description:
              - The username used to authenticate.
            type: str
          password:
            description:
              - The password used to authenticate.
            type: str
  dns:
    description:
      - DNS record configuration used to update A / PTR records when
        replication resumes.
    type: dict
    suboptions:
      preferred_name_server:
        description:
          - The FQDN or IP address of the preferred name server.
        type: str
      action:
        description:
          - Whether DNS records should be added or removed.
        type: str
        choices:
          - ADD
          - REMOVE
      credential:
        description:
          - Credentials used to authenticate against the DNS server.
        type: dict
        suboptions:
          username:
            description:
              - The username used to authenticate.
            type: str
          password:
            description:
              - The password used to authenticate.
            type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Resume replication after a planned failover from primary to secondary
  nutanix.ncp.ntnx_resume_replication_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    replication_direction: PRIMARY_TO_SECONDARY
    primary_file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    secondary_file_server_ext_id: "8c1e537d-6777-4c22-5d41-ddd0c3337aa8"
    type: PLANNED
    active_directory:
      preferred_domain_controller: "dc.example.local"
      credential:
        username: "ad_admin"
        password: "AdSecret.123"
    dns:
      preferred_name_server: "10.0.0.53"
      action: ADD
      credential:
        username: "dns_admin"
        password: "DnsSecret.123"
  register: result
  ignore_errors: true

- name: Resume replication after an unplanned failover from secondary to primary
  nutanix.ncp.ntnx_resume_replication_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    replication_direction: SECONDARY_TO_PRIMARY
    primary_file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    secondary_file_server_ext_id: "8c1e537d-6777-4c22-5d41-ddd0c3337aa8"
    type: UNPLANNED
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the resume replication action.
    - Task details if C(wait) is true.
    - Initial task reference if C(wait) is false.
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
          "rel": "files:config:replication-policy"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T06:26:51.524581+00:00",
      "legacy_error_message": null,
      "operation": "ResumeReplication",
      "operation_description": "Resume replication",
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
  sample: "Api Exception raised while resuming replication"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  returned: when an error occurs
  type: str
  sample: "Failed generating resume replication spec"

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
  description: The external ID of the replication entity affected by the action.
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

    credential_spec = dict(
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
    )

    active_directory_spec = dict(
        preferred_domain_controller=dict(type="str"),
        credential=dict(
            type="dict",
            options=credential_spec,
            obj=files_sdk.Credential,
        ),
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
        replication_direction=dict(
            type="str",
            choices=["PRIMARY_TO_SECONDARY", "SECONDARY_TO_PRIMARY"],
            obj=files_sdk.ReplicationDirection,
        ),
        primary_file_server_ext_id=dict(type="str"),
        secondary_file_server_ext_id=dict(type="str"),
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


def resume_replication(module, api_instance, result):
    sg = SpecGenerator(module)
    default_spec = files_sdk.ResumeReplicationSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating resume replication spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.resume_replication(body=spec)
    except Exception as exc:
        raise_api_exception(
            module=module,
            exception=exc,
            msg="Api Exception raised while resuming replication",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        entity_ext_id = get_entity_ext_id_from_task(task)
        if entity_ext_id:
            result["ext_id"] = entity_ext_id
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_together=[
            ("primary_file_server_ext_id", "secondary_file_server_ext_id"),
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
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_replication_policies_api_instance(module)
    resume_replication(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
