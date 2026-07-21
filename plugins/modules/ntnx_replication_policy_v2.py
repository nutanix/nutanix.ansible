#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_replication_policy_v2
short_description: Create, Update, Delete Nutanix Files replication policies
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete Nutanix Files
    replication policies (Smart DR, Data Sync, VDI Sync) in Prism Central.
  - Replication policies govern how, when and where Nutanix Files share
    data is replicated to a target file server.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Create / Update / Delete a Replication Policy) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is C(present) and C(ext_id) is not provided the module
        will create a replication policy.
      - If C(state) is C(present) and C(ext_id) is provided the module will
        update the replication policy.
      - If C(state) is C(absent) and C(ext_id) is provided the module will
        delete the replication policy.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - External ID of the replication policy.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the replication policy.
      - Required for create operation.
      - Minimum 1 char, maximum 64 chars.
    type: str
    required: false
  description:
    description:
      - Replication policy description.
      - Maximum 180 chars.
    type: str
    required: false
  type:
    description:
      - Replication policy type.
      - Required for create operation.
      - C(SMART_DR) is asynchronous share-level disaster recovery.
      - C(DATA_SYNC) is file-level synchronization between file servers.
      - C(VDI_SYNC) is bi-directional VDI user profile synchronization.
    type: str
    required: false
    choices:
      - SMART_DR
      - DATA_SYNC
      - VDI_SYNC
  replication_configurations:
    description:
      - Replication configuration list.
      - Represents combination of file server entities involved in the
        replication policy, schedules, policy status and replication summary.
      - For C(SMART_DR) the system supports a single replication configuration
        object per replication policy.
      - For C(DATA_SYNC) or C(VDI_SYNC) between 1 and 10 configurations are
        allowed. In C(VDI_SYNC) the primary file server of the first entry is
        the preferred file server for replication.
      - Required for create of forward (non C(is_reverse)) policies.
    type: list
    elements: dict
    required: false
    suboptions:
      primary_file_server_ext_id:
        description:
          - External ID of the primary file server.
        type: str
        required: false
      secondary_file_server_ext_id:
        description:
          - External ID of the secondary file server.
        type: str
        required: false
      primary_domain_manager_ext_id:
        description:
          - External ID of the primary Prism Central (domain manager) that
            manages the primary file server.
        type: str
        required: false
      secondary_domain_manager_ext_id:
        description:
          - External ID of the secondary Prism Central (domain manager) that
            manages the secondary file server.
        type: str
        required: false
      replication_entities:
        description:
          - List of shares / mount targets that participate in the replication.
          - Required for C(DATA_SYNC) and C(VDI_SYNC); optional for
            C(SMART_DR) where mount targets can be auto-included via
            C(should_include_new_mount_targets).
        type: list
        elements: dict
        required: false
        suboptions:
          primary_file_server_mount_target_ext_id:
            description:
              - External ID of the primary file server mount target (share).
            type: str
            required: false
          primary_file_server_mount_target_path:
            description:
              - Path inside the primary file server mount target to replicate.
            type: str
            required: false
          secondary_file_server_mount_target_ext_id:
            description:
              - External ID of the secondary file server mount target.
            type: str
            required: false
          secondary_file_server_mount_target_path:
            description:
              - Path inside the secondary file server mount target.
            type: str
            required: false
          exclude_dir_patterns:
            description:
              - List of directory patterns to exclude from the replication.
            type: list
            elements: str
            required: false
      schedule:
        description:
          - Replication schedule that controls RPO cadence.
        type: dict
        required: false
        suboptions:
          frequency:
            description:
              - Frequency multiplier for the selected C(schedule_interval).
                Together with the interval this defines the RPO.
            type: int
            required: false
          start_time:
            description:
              - ISO-8601 time at which the policy becomes active. If not set
                the policy is applied immediately.
            type: str
            required: false
          schedule_interval:
            description:
              - Selects the interval unit. Exactly one of C(daily),
                C(weekly), C(monthly) may be provided.
            type: dict
            required: false
            suboptions:
              daily:
                description:
                  - Daily schedule interval.
                type: dict
                required: false
                suboptions:
                  frequency:
                    description:
                      - Frequency (multiplier of days).
                    type: int
                    required: false
              weekly:
                description:
                  - Weekly schedule interval.
                type: dict
                required: false
                suboptions:
                  days_of_week:
                    description:
                      - Days of the week (0-6) on which to replicate.
                    type: list
                    elements: int
                    required: false
              monthly:
                description:
                  - Monthly schedule interval.
                type: dict
                required: false
                suboptions:
                  days_of_month:
                    description:
                      - Days of the month (1-31) on which to replicate.
                    type: list
                    elements: int
                    required: false
      should_cancel_ongoing_replication_jobs:
        description:
          - If C(true), any ongoing replication job for this configuration
            will be cancelled on update.
        type: bool
        required: false
  should_include_new_mount_targets:
    description:
      - Whether new mount targets on the file server should be auto-included
        in the replication policy. Applicable for C(SMART_DR). Defaults to
        C(true) on the server side.
    type: bool
    required: false
  should_keep_deleted_files:
    description:
      - Flag to maintain files/folders on the target that are deleted on the
        source. Applicable for C(DATA_SYNC).
    type: bool
    required: false
  exclude_file_patterns:
    description:
      - File patterns to exclude from replication (e.g. C(["*.tmp", "*.log"])).
      - Applicable for C(DATA_SYNC).
    type: list
    elements: str
    required: false
  change_user_session_ownership_spec:
    description:
      - VDI user session ownership change spec. Applicable for C(VDI_SYNC)
        updates that move a user session from one owner file server to
        another.
    type: dict
    required: false
    suboptions:
      current_owner_file_server_ext_id:
        description:
          - External ID of the current owner file server.
        type: str
        required: false
      new_owner_file_server_ext_id:
        description:
          - External ID of the new owner file server.
        type: str
        required: false
  is_reverse:
    description:
      - Reverse the data replication direction during a planned failover or
        to resume replication from the secondary site. Applicable only for
        C(SMART_DR). When C(true) no C(replication_entities) need to be
        specified.
    type: bool
    required: false
    default: false
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
- name: Create Smart DR replication policy with daily schedule
  nutanix.ncp.ntnx_replication_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "smartdr_policy_ansible"
    description: "Smart DR replication policy created by Ansible"
    type: "SMART_DR"
    should_include_new_mount_targets: true
    replication_configurations:
      - primary_file_server_ext_id: "a4b02ea9-6a56-4c1b-9d0b-6bdf7bf67e11"
        secondary_file_server_ext_id: "b7d84e21-3a45-47dc-a1c8-4bcf6a24fa19"
        primary_domain_manager_ext_id: "1c2d3e4f-1234-4c1b-9d0b-6bdf7bf67e11"
        secondary_domain_manager_ext_id: "2b3c4d5e-5678-4c1b-9d0b-6bdf7bf67e11"
        schedule:
          frequency: 1
          schedule_interval:
            daily:
              frequency: 1
  register: result
  ignore_errors: true

- name: Create Data Sync replication policy with excludes and weekly schedule
  nutanix.ncp.ntnx_replication_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "datasync_policy_ansible"
    description: "Data Sync policy created by Ansible"
    type: "DATA_SYNC"
    should_keep_deleted_files: true
    exclude_file_patterns:
      - "*.tmp"
      - "*.log"
    replication_configurations:
      - primary_file_server_ext_id: "a4b02ea9-6a56-4c1b-9d0b-6bdf7bf67e11"
        secondary_file_server_ext_id: "b7d84e21-3a45-47dc-a1c8-4bcf6a24fa19"
        replication_entities:
          - primary_file_server_mount_target_ext_id: "aaaa1111-6a56-4c1b-9d0b-6bdf7bf67e11"
            primary_file_server_mount_target_path: "/data"
            secondary_file_server_mount_target_ext_id: "bbbb2222-3a45-47dc-a1c8-4bcf6a24fa19"
            secondary_file_server_mount_target_path: "/data"
            exclude_dir_patterns:
              - "tmp"
              - "logs"
        schedule:
          frequency: 1
          schedule_interval:
            weekly:
              days_of_week: [1, 3, 5]
  register: result
  ignore_errors: true

- name: Update replication policy description and schedule
  nutanix.ncp.ntnx_replication_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "smartdr_policy_ansible"
    description: "Updated Smart DR policy description"
    type: "SMART_DR"
    replication_configurations:
      - primary_file_server_ext_id: "a4b02ea9-6a56-4c1b-9d0b-6bdf7bf67e11"
        secondary_file_server_ext_id: "b7d84e21-3a45-47dc-a1c8-4bcf6a24fa19"
        schedule:
          frequency: 2
          schedule_interval:
            daily:
              frequency: 1
  register: result
  ignore_errors: true

- name: Delete replication policy
  nutanix.ncp.ntnx_replication_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a replication policy.
    - If the operation is create or update and C(wait) is C(true) it will
      return the replication policy details.
    - If the operation is create or update and C(wait) is C(false) it will
      return the task details.
    - If the operation is delete it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "change_user_session_ownership_spec": null,
      "description": "Smart DR replication policy created by Ansible",
      "exclude_file_patterns": null,
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "is_reverse": false,
      "links": null,
      "name": "smartdr_policy_ansible",
      "replication_configurations": [
          {
              "primary_domain_manager_ext_id": "1c2d3e4f-1234-4c1b-9d0b-6bdf7bf67e11",
              "primary_file_server_ext_id": "a4b02ea9-6a56-4c1b-9d0b-6bdf7bf67e11",
              "replication_entities": null,
              "replication_summary": null,
              "schedule": {
                  "frequency": 1,
                  "schedule_interval": {
                      "frequency": 1
                  },
                  "start_time": null
              },
              "secondary_domain_manager_ext_id": "2b3c4d5e-5678-4c1b-9d0b-6bdf7bf67e11",
              "secondary_file_server_ext_id": "b7d84e21-3a45-47dc-a1c8-4bcf6a24fa19",
              "should_cancel_ongoing_replication_jobs": null,
              "status": "ENABLED"
          }
      ],
      "should_include_new_mount_targets": true,
      "should_keep_deleted_files": null,
      "status": "ENABLED",
      "tenant_id": null,
      "type": "SMART_DR"
    }

task_ext_id:
  description:
    - The external ID of the task tracking the operation.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the replication policy.
  returned: always
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

changed:
  description: Whether the module made any change on the cluster.
  returned: always
  type: bool
  sample: true

skipped:
  description: Whether the operation was skipped (e.g. idempotent update).
  returned: always
  type: bool
  sample: false

error:
  description: Error message when an error occurs.
  returned: When an error occurs
  type: str

failed:
  description: Whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description:
    - Message describing the outcome (idempotent skip, check-mode delete, or
      the specific error path).
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating replication policy"
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
    get_replication_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_replication_policy  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
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


# Read-only fields that must be stripped from the spec before sending it back
# on an update PUT request. ``status`` and ``replication_summary`` on the
# nested replication_configurations are also server-populated.
READ_ONLY_FIELDS = ["status"]
READ_ONLY_CONFIG_FIELDS = ["status", "replication_summary"]


def get_module_spec():

    ownership_spec = dict(
        current_owner_file_server_ext_id=dict(type="str", required=False),
        new_owner_file_server_ext_id=dict(type="str", required=False),
    )

    replication_entity_spec = dict(
        primary_file_server_mount_target_ext_id=dict(type="str", required=False),
        primary_file_server_mount_target_path=dict(type="str", required=False),
        secondary_file_server_mount_target_ext_id=dict(type="str", required=False),
        secondary_file_server_mount_target_path=dict(type="str", required=False),
        exclude_dir_patterns=dict(type="list", elements="str", required=False),
    )

    daily_schedule_spec = dict(
        frequency=dict(type="int", required=False),
    )
    weekly_schedule_spec = dict(
        days_of_week=dict(type="list", elements="int", required=False),
    )
    monthly_schedule_spec = dict(
        days_of_month=dict(type="list", elements="int", required=False),
    )

    schedule_interval_spec = dict(
        daily=dict(
            type="dict",
            options=daily_schedule_spec,
            required=False,
            obj=files_sdk.DailySchedule,
        ),
        weekly=dict(
            type="dict",
            options=weekly_schedule_spec,
            required=False,
            obj=files_sdk.WeeklySchedule,
        ),
        monthly=dict(
            type="dict",
            options=monthly_schedule_spec,
            required=False,
            obj=files_sdk.MonthlySchedule,
        ),
    )

    schedule_spec = dict(
        frequency=dict(type="int", required=False),
        start_time=dict(type="str", required=False),
        schedule_interval=dict(
            type="dict",
            options=schedule_interval_spec,
            required=False,
            mutually_exclusive=[("daily", "weekly", "monthly")],
            obj={
                "daily": files_sdk.DailySchedule,
                "weekly": files_sdk.WeeklySchedule,
                "monthly": files_sdk.MonthlySchedule,
            },
        ),
    )

    replication_config_spec = dict(
        primary_file_server_ext_id=dict(type="str", required=False),
        secondary_file_server_ext_id=dict(type="str", required=False),
        primary_domain_manager_ext_id=dict(type="str", required=False),
        secondary_domain_manager_ext_id=dict(type="str", required=False),
        replication_entities=dict(
            type="list",
            elements="dict",
            options=replication_entity_spec,
            required=False,
            obj=files_sdk.ReplicationEntity,
        ),
        schedule=dict(
            type="dict",
            options=schedule_spec,
            required=False,
            obj=files_sdk.ReplicationSchedule,
        ),
        should_cancel_ongoing_replication_jobs=dict(type="bool", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        type=dict(
            type="str",
            choices=["SMART_DR", "DATA_SYNC", "VDI_SYNC"],
            obj=files_sdk.ReplicationPolicyType,
        ),
        replication_configurations=dict(
            type="list",
            elements="dict",
            options=replication_config_spec,
            required=False,
            obj=files_sdk.ReplicationConfiguration,
        ),
        should_include_new_mount_targets=dict(type="bool", required=False),
        should_keep_deleted_files=dict(type="bool", required=False),
        exclude_file_patterns=dict(type="list", elements="str", required=False),
        change_user_session_ownership_spec=dict(
            type="dict",
            options=ownership_spec,
            required=False,
            obj=files_sdk.OwnershipSpec,
        ),
        is_reverse=dict(type="bool", required=False, default=False),
    )
    return module_args


def create_replication_policy(module, api_instance, result):
    """Create a new replication policy on the cluster."""
    validate_required_params(module, ["name", "type"])

    sg = SpecGenerator(module)
    default_spec = files_sdk.ReplicationPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating replication policy spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_replication_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating replication policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task, rel=TASK_CONSTANTS.RelEntityType.FILES_REPLICATION_POLICY
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_replication_policy(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Replication Policy"
                ),
                msg="Failed to get entity ext_id from task for Replication Policy",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """Return True when the new update spec is identical to what already exists."""
    old = strip_internal_attributes(deepcopy(old_spec_dict))
    new = strip_internal_attributes(deepcopy(update_spec_dict))
    for field in READ_ONLY_FIELDS:
        old.pop(field, None)
        new.pop(field, None)
    for configs in (
        old.get("replication_configurations") or [],
        new.get("replication_configurations") or [],
    ):
        for cfg in configs:
            for field in READ_ONLY_CONFIG_FIELDS:
                cfg.pop(field, None)
    return old == new


def _strip_config_read_only_fields(spec):
    """Remove server-populated fields from replication_configurations before update."""
    if not getattr(spec, "replication_configurations", None):
        return
    for cfg in spec.replication_configurations:
        strip_read_only_fields(cfg, READ_ONLY_CONFIG_FIELDS)


def update_replication_policy(module, api_instance, result):
    """Update an existing replication policy identified by C(ext_id)."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_replication_policy(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating replication policy", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update replication policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change.",
            skipped=True,
            ext_id=ext_id,
            response=strip_internal_attributes(old_spec.to_dict()),
        )

    strip_read_only_fields(update_spec, READ_ONLY_FIELDS)
    _strip_config_read_only_fields(update_spec)

    resp = None
    try:
        resp = api_instance.update_replication_policy_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating replication policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_replication_policy(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_replication_policy(module, api_instance, result):
    """Delete an existing replication policy by C(ext_id)."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Replication policy with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.delete_replication_policy_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting replication policy",
        )

    task_ext_id = resp.data.ext_id if resp and resp.data else None
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
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
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
        "failed": False,
    }
    api_instance = get_replication_policies_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_replication_policy(module, api_instance, result)
        else:
            create_replication_policy(module, api_instance, result)
    else:
        delete_replication_policy(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
