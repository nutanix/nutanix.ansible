#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snapshot_schedule_v2
short_description: Create, Update, Delete snapshot schedules for a file server in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete snapshot schedules on a Nutanix file server.
  - Snapshot schedules define the frequency (hourly/daily/weekly/monthly) at which snapshots
    of the file server shares are taken and how many of them are retained.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create a Snapshot Schedule) -
    Required Roles: File Server Admin, Prism Admin, Super Admin
  - >-
    B(Update a Snapshot Schedule) -
    Required Roles: File Server Admin, Prism Admin, Super Admin
  - >-
    B(Delete a Snapshot Schedule) -
    Required Roles: File Server Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create snapshot schedule.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update snapshot schedule.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete snapshot schedule.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the snapshot schedule.
      - Required for update and delete operations.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external ID of the parent file server that owns the snapshot schedule.
      - Required for every operation.
    type: str
    required: true
  type:
    description:
      - Frequency type of the snapshot schedule.
      - Required for create operation.
    type: str
    required: false
    choices:
      - HOURLY
      - DAILY
      - WEEKLY
      - MONTHLY
  max_retention_count:
    description:
      - Maximum number of snapshots to retain for this schedule.
      - When exceeded, the oldest snapshots are deleted automatically.
    type: int
    required: false
  schedule:
    description:
      - Snapshot schedule details. Exactly one of C(daily_schedule), C(weekly_schedule)
        or C(monthly_schedule) must be provided, and it must be consistent with the C(type).
      - For C(HOURLY) and C(DAILY) types use C(daily_schedule.frequency).
      - For C(WEEKLY) type use C(weekly_schedule.days_of_week).
      - For C(MONTHLY) type use C(monthly_schedule.days_of_month).
    type: dict
    required: false
    suboptions:
      daily_schedule:
        description:
          - Daily/Hourly schedule details.
          - Used for schedule C(type) of C(HOURLY) or C(DAILY).
        type: dict
        required: false
        suboptions:
          frequency:
            description:
              - Frequency of snapshots to be taken daily or hourly.
              - For example, a frequency of C(1) with type C(DAILY) means one snapshot per day.
            type: int
            required: true
      weekly_schedule:
        description:
          - Weekly schedule details.
          - Used for schedule C(type) of C(WEEKLY).
        type: dict
        required: false
        suboptions:
          days_of_week:
            description:
              - A list of the days of the week on which snapshots should be taken.
              - The values represent the ordinal day of the week starting at C(1) for Sunday.
            type: list
            elements: int
            required: true
      monthly_schedule:
        description:
          - Monthly schedule details.
          - Used for schedule C(type) of C(MONTHLY).
        type: dict
        required: false
        suboptions:
          days_of_month:
            description:
              - A list of the days of the month (1-31) on which snapshots should be taken.
            type: list
            elements: int
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
- name: Create daily snapshot schedule
  nutanix.ncp.ntnx_snapshot_schedule_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "d1234567-89ab-cdef-0123-456789abcdef"
    type: "DAILY"
    max_retention_count: 7
    schedule:
      daily_schedule:
        frequency: 1
  register: result
  ignore_errors: true

- name: Create weekly snapshot schedule
  nutanix.ncp.ntnx_snapshot_schedule_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "d1234567-89ab-cdef-0123-456789abcdef"
    type: "WEEKLY"
    max_retention_count: 4
    schedule:
      weekly_schedule:
        days_of_week:
          - 1
          - 4
  register: result
  ignore_errors: true

- name: Update snapshot schedule retention count
  nutanix.ncp.ntnx_snapshot_schedule_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "d1234567-89ab-cdef-0123-456789abcdef"
    ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
    type: "DAILY"
    max_retention_count: 14
    schedule:
      daily_schedule:
        frequency: 1
  register: result
  ignore_errors: true

- name: Delete snapshot schedule
  nutanix.ncp.ntnx_snapshot_schedule_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "d1234567-89ab-cdef-0123-456789abcdef"
    ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a snapshot schedule.
    - If the operation is create or update and C(wait) is true, it will return the snapshot schedule details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "48f78959-14a6-4c47-b5db-920460c4b668",
      "type": "DAILY",
      "max_retention_count": 7,
      "schedule": {
          "frequency": 1
      },
      "links": null,
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
    - The external ID of the snapshot schedule.
  returned: always
  type: str
  sample: "48f78959-14a6-4c47-b5db-920460c4b668"

file_server_ext_id:
  description:
    - The external ID of the parent file server.
  returned: always
  type: str
  sample: "d1234567-89ab-cdef-0123-456789abcdef"

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
  sample: "Api Exception raised while creating snapshot schedule"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_snapshot_schedules_api_instance,
)
from ..module_utils.v4.files.helpers import get_snapshot_schedule  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
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

    daily_schedule_spec = dict(
        frequency=dict(type="int", required=True),
    )

    weekly_schedule_spec = dict(
        days_of_week=dict(type="list", elements="int", required=True),
    )

    monthly_schedule_spec = dict(
        days_of_month=dict(type="list", elements="int", required=True),
    )

    schedule_spec = dict(
        daily_schedule=dict(type="dict", options=daily_schedule_spec, required=False),
        weekly_schedule=dict(type="dict", options=weekly_schedule_spec, required=False),
        monthly_schedule=dict(
            type="dict", options=monthly_schedule_spec, required=False
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        type=dict(
            type="str",
            choices=["HOURLY", "DAILY", "WEEKLY", "MONTHLY"],
        ),
        max_retention_count=dict(type="int"),
        schedule=dict(
            type="dict",
            options=schedule_spec,
            mutually_exclusive=[
                ("daily_schedule", "weekly_schedule", "monthly_schedule"),
            ],
            required_one_of=[
                ("daily_schedule", "weekly_schedule", "monthly_schedule"),
            ],
        ),
    )
    return module_args


def _validate_schedule_matches_type(module, schedule_type, schedule_params):
    """
    Validate that the provided schedule sub-block matches the schedule type.
    """
    if not schedule_params:
        return
    daily = schedule_params.get("daily_schedule")
    weekly = schedule_params.get("weekly_schedule")
    monthly = schedule_params.get("monthly_schedule")

    if schedule_type in ("HOURLY", "DAILY") and not daily:
        module.fail_json(
            msg="schedule.daily_schedule is required when type is HOURLY or DAILY"
        )
    if schedule_type == "WEEKLY" and not weekly:
        module.fail_json(msg="schedule.weekly_schedule is required when type is WEEKLY")
    if schedule_type == "MONTHLY" and not monthly:
        module.fail_json(
            msg="schedule.monthly_schedule is required when type is MONTHLY"
        )


def _build_schedule_object(module, schedule_type, schedule_params):
    """
    Build the SDK schedule object based on the schedule type and user params.
    Returns the concrete DailySchedule/WeeklySchedule/MonthlySchedule instance.
    """
    if not schedule_params:
        return None
    if schedule_type in ("HOURLY", "DAILY"):
        daily = schedule_params.get("daily_schedule") or {}
        return files_sdk.DailySchedule(frequency=daily.get("frequency"))
    if schedule_type == "WEEKLY":
        weekly = schedule_params.get("weekly_schedule") or {}
        return files_sdk.WeeklySchedule(days_of_week=weekly.get("days_of_week"))
    if schedule_type == "MONTHLY":
        monthly = schedule_params.get("monthly_schedule") or {}
        return files_sdk.MonthlySchedule(days_of_month=monthly.get("days_of_month"))
    module.fail_json(
        msg="Unsupported snapshot schedule type: {0}".format(schedule_type)
    )
    return None


def _build_spec(module, schedule_type):
    """
    Build a SnapshotSchedule SDK spec from module params.
    """
    spec = files_sdk.SnapshotSchedule()
    spec.type = getattr(files_sdk.SnapshotScheduleType, schedule_type)
    if module.params.get("max_retention_count") is not None:
        spec.max_retention_count = module.params.get("max_retention_count")
    schedule_obj = _build_schedule_object(
        module, schedule_type, module.params.get("schedule")
    )
    if schedule_obj is not None:
        spec.schedule = schedule_obj
    return spec


def create_snapshot_schedule(module, result, api_instance):
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["file_server_ext_id"] = file_server_ext_id

    validate_required_params(module, ["type", "schedule"])

    schedule_type = module.params.get("type")
    _validate_schedule_matches_type(
        module, schedule_type, module.params.get("schedule")
    )

    spec = _build_spec(module, schedule_type)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.create_snapshot_schedule(
            fileServerExtId=file_server_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating snapshot schedule",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        # Snapshot schedule creation returns a task; extract the entity ext_id
        # from the task's entities_affected list (skip the file server entity).
        new_ext_id = _extract_snapshot_schedule_ext_id(task_status, file_server_ext_id)
        if new_ext_id:
            result["ext_id"] = new_ext_id
            entity = get_snapshot_schedule(
                module, api_instance, file_server_ext_id, new_ext_id
            )
            result["response"] = strip_internal_attributes(entity.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Snapshot Schedule"
                ),
                msg="Failed to get entity ext_id from task for Snapshot Schedule",
            )
    result["changed"] = True


def _extract_snapshot_schedule_ext_id(task_data, file_server_ext_id):
    """
    Look through task.entities_affected for the snapshot schedule entity.
    We take the first entity whose ext_id is not the parent file_server_ext_id.
    """
    entities = getattr(task_data, "entities_affected", None) or []
    for entity in entities:
        rel = getattr(entity, "rel", None) or ""
        ext_id = getattr(entity, "ext_id", None)
        if not ext_id:
            continue
        if ext_id == file_server_ext_id:
            continue
        if "snapshot-schedule" in rel.lower() or "snapshotschedule" in rel.lower():
            return ext_id
    # Fallback: return the first non-parent ext_id we see.
    for entity in entities:
        ext_id = getattr(entity, "ext_id", None)
        if ext_id and ext_id != file_server_ext_id:
            return ext_id
    return None


def _spec_dicts_for_idempotency(current, updated):
    current_dict = strip_internal_attributes(deepcopy(current.to_dict()))
    updated_dict = strip_internal_attributes(deepcopy(updated.to_dict()))
    # Server-managed fields to ignore on idempotency comparison.
    for key in ("ext_id", "links", "tenant_id"):
        current_dict.pop(key, None)
        updated_dict.pop(key, None)
    return current_dict, updated_dict


def check_for_idempotency(current_spec, update_spec):
    current_dict, updated_dict = _spec_dicts_for_idempotency(current_spec, update_spec)
    return current_dict == updated_dict


def update_snapshot_schedule(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = ext_id
    result["file_server_ext_id"] = file_server_ext_id

    current = get_snapshot_schedule(module, api_instance, file_server_ext_id, ext_id)
    etag = get_etag(data=current)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating snapshot schedule", **result
        )

    # Determine target schedule type (falls back to current on partial input).
    schedule_type = module.params.get("type") or getattr(current, "type", None)
    if schedule_type is None:
        module.fail_json(
            msg="Unable to determine snapshot schedule type for update", **result
        )
    _validate_schedule_matches_type(
        module, schedule_type, module.params.get("schedule")
    )

    update_spec = deepcopy(current)
    update_spec.type = getattr(files_sdk.SnapshotScheduleType, schedule_type)
    if module.params.get("max_retention_count") is not None:
        update_spec.max_retention_count = module.params.get("max_retention_count")
    schedule_obj = _build_schedule_object(
        module, schedule_type, module.params.get("schedule")
    )
    if schedule_obj is not None:
        update_spec.schedule = schedule_obj

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(current, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    kwargs = {"if_match": etag}
    try:
        resp = api_instance.update_snapshot_schedule_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating snapshot schedule",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
    entity = get_snapshot_schedule(module, api_instance, file_server_ext_id, ext_id)
    result["response"] = strip_internal_attributes(entity.to_dict())
    result["changed"] = True


def delete_snapshot_schedule(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = ext_id
    result["file_server_ext_id"] = file_server_ext_id

    if module.check_mode:
        result["msg"] = "Snapshot schedule with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    current = get_snapshot_schedule(module, api_instance, file_server_ext_id, ext_id)
    etag = get_etag(data=current)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    try:
        resp = api_instance.delete_snapshot_schedule_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting snapshot schedule",
        )
    task_ext_id = getattr(getattr(resp, "data", None), "ext_id", None)
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, raise_error=False)
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
        "file_server_ext_id": None,
        "skipped": False,
    }
    api_instance = get_snapshot_schedules_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_snapshot_schedule(module, result, api_instance)
        else:
            create_snapshot_schedule(module, result, api_instance)
    else:
        delete_snapshot_schedule(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
