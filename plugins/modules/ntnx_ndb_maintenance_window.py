#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ndb_maintenance_window
short_description: module to create, update and delete mainetance window
version_added: 1.8.0
description: 'write'
options:
    name:
        description:
            - name of maintenance window
        type: str
    uuid:
        description:
            - uuid of maintenance window
            - should be used for update or delete
        type: str
    desc:
        description:
            - description of maintenance window
        type: str
    schedule:
        description:
            - schedule of maintenance
        type: dict
        suboptions:
            recurrence:
                description:
                    - type of recurrence
                type: str
                choices: ["weekly", "monthly"]
            duration:
                description:
                    - duration of window in hours
                type: int
            start_time:
                description:
                    - start time of maintenance in formate 'hh:mm:ss'
                type: str
            timezone:
                description:
                    - time zone related to C(start_time)
                    - required with start_time
                type: str
            week_of_month:
                description:
                    - week of month for maitenance
                type: str
            day_of_week:
                description:
                    - day of week for maitenance
                type: str

extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: create window with weekly schedule
  ntnx_ndb_maintenance_window:
    name: "{{window1_name}}"
    desc: "anisble-created-window"
    schedule:
      recurrence: "weekly"
      duration: 2
      start_time: "11:00:00"
      day_of_week: "tuesday"
      timezone: "UTC"
  register: result

- name: create window with monthly schedule
  ntnx_ndb_maintenance_window:
    name: "{{window2_name}}"
    desc: "anisble-created-window"
    schedule:
      recurrence: "monthly"
      duration: 2
      start_time: "11:00:00"
      day_of_week: "tuesday"
      week_of_month: 2
      timezone: "UTC"

  register: result

"""
RETURN = r"""
response:
  description: maintenance window response with associated tasks
  returned: always
  type: dict
  sample: {
        "id": "3c8704e7-e1a7-49f9-9943-a92090f8d098",
        "name": "test-check",
        "description": "",
        "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
        "dateCreated": "2023-02-28 10:50:16",
        "dateModified": "2023-02-28 10:50:16",
        "accessLevel": null,
        "properties": null,
        "tags": null,
        "schedule": {
            "startTime": "10:50:02",
            "recurrence": "MONTHLY",
            "threshold": null,
            "hour": 10,
            "minute": 50,
            "dayOfWeek": "TUESDAY",
            "weekOfMonth": 4,
            "duration": 2,
            "timeZone": "UTC"
        },
        "status": "ACTIVE",
        "nextRunTime": "2023-03-28 10:50:00",
        "entityTaskAssoc": null,
        "timezone": null
    }
uuid:
  description: maintenance window uuid
  returned: always
  type: str
  sample: "be524e70-60ad-4a8c-a0ee-8d72f954d7e6"

"""

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.maintenance_window import MaintenanceWindow  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    schedule = dict(
        recurrence=dict(type="str", choices=["weekly", "monthly"], required=False),
        duration=dict(type="int", required=False),  # in hrs
        start_time=dict(type="str", required=False),  # in 24hrs format in HH:MM:SS
        timezone=dict(type="str", required=False),
        week_of_month=dict(type="str", required=False),
        day_of_week=dict(type="str", required=False),
    )
    module_args = dict(
        uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        schedule=dict(
            type="dict",
            options=schedule,
            required_together=[("start_time", "timezone")],
            required=False,
        ),
    )
    return module_args


def create_window(module, result):
    maintenance_window = MaintenanceWindow(module)

    spec, err = maintenance_window.get_spec()
    if err:
        result["error"] = err
        err_msg = "Failed getting spec for new maintenance window"
        module.fail_json(msg=err_msg, **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = maintenance_window.create(spec)
    result["response"] = resp
    result["uuid"] = resp.get("id")
    result["changed"] = True


def check_idempotency(old_spec, new_spec):

    args = ["name", "description"]
    for arg in args:
        if old_spec.get(arg, "") != new_spec.get(arg, ""):
            return False

    # check for schedule changes
    args = ["recurrence", "dayOfWeek", "weekOfMonth", "duration", "startTime"]
    for arg in args:
        if old_spec.get("schedule", {}).get(arg, "") != new_spec.get(
            "schedule", {}
        ).get(arg, ""):
            return False
    return True


def update_window(module, result):
    _maintenance_window = MaintenanceWindow(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for update", **result)

    maintenance_window = _maintenance_window.read(uuid=uuid)
    default_spec = _maintenance_window.get_default_update_spec(
        override_spec=maintenance_window
    )
    spec, err = _maintenance_window.get_spec(old_spec=default_spec)
    if err:
        result["error"] = err
        err_msg = "Failed getting spec for updating maintenance window"
        module.fail_json(msg=err_msg, **result)

    if module.check_mode:
        result["response"] = spec
        return

    # defining start_time will skip idempotency checks
    if check_idempotency(old_spec=maintenance_window, new_spec=spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = _maintenance_window.update(uuid=uuid, data=spec)
    result["response"] = resp
    result["uuid"] = uuid
    result["changed"] = True


def delete_window(module, result):
    _maintenance_window = MaintenanceWindow(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for delete", **result)

    resp = _maintenance_window.delete(uuid=uuid, data={})
    result["response"] = resp
    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    if module.params.get("state") == "present":
        if module.params.get("uuid"):
            update_window(module, result)
        else:
            create_window(module, result)
    else:
        delete_window(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
