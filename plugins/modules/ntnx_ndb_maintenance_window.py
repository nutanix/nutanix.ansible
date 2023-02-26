#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ndb_maintenance_window
short_description: write
version_added: 1.8.0
description: 'write'
options:
    name:
        description:
            - write
        type: str
    uuid:
        description:
            - write
        type: str
    desc:
        description:
            - write
        type: str
    schedule:
        description:
            - write
        type: dict
        suboptions:
            recurrence:
                description:
                    - write
                type: str
                choices: ["weekly", "monthly"]
            duration:
                description:
                    - write
                type: int
            start_time:
                description:
                    - write
                type: str
            timezone:
                description:
                    - write
                type: str
            week_of_month:
                description:
                    - write
                type: str
            day_of_week:
                description:
                    - write
                type: str

extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
"""

EXAMPLES = r"""
"""
RETURN = r"""
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
