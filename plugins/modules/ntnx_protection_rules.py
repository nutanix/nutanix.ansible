#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from re import T

__metaclass__ = type

DOCUMENTATION = r"""
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.protection_rules import ProtectionRule


def get_module_spec():
    snapshot_retention_policy = dict(
        num_snapshots = dict(type="int", required=True),
        rollup_retention_policy = dict(
            snapshot_interval_type = dict(type="str", required=True),
            multiple = dict(type="str", choices=["HOUR", "DAY", "WEEK", "MONTH", "YEAR"], required=True)
        )
    )

    availability_zone = dict(
        availability_zone_url = dict(type="str", required=True),
        cluster_uuid = dict(type="str", required=True),
    ),
    
    schedule = dict(
        source = dict(type="dict", options=availability_zone, required=False),
        destination = dict(type="dict", options=availability_zone, required=False),
        protection_type = dict(type="str", choices=["SYNC", "ASYNC"], required=True),
        auto_suspend_timeout = dict(type="int", required=True),
        rpo = dict(type="int", required=False),
        rpo_unit = dict(type="str", choices=["MINUTE", "HOUR", "DAY", "WEEK"], required=False),
        snapshot_type = dict(type="str", choice=["CRASH_CONSISTENT", "APPLICATION_CONSISTENT"], required=True),
        local_retention_policy = dict(type="dict", options = snapshot_retention_policy, required=False),
        remote_retention_policy = dict(type="dict", options = snapshot_retention_policy, required=True),
    )

    module_args = dict(
        name = dict(type="str", required=False),
        desc = dict(type="str", required=False),
        start_time = dict(type="str", required=False),
        schedules = dict(type="list", elements="dict", options = schedule, required=True),
        protected_categories = dict(type="dict", required=True),
        primay_site = dict(type="dict", options=availability_zone, required=False),
    )
    return module_args


def create_protection_rule(module, result):
    protection_rule = ProtectionRule(module)
    name = module.params["name"]
    if protection_rule.get_uuid(name):
        module.fail_json(msg="Protection Rule with given name already exists", **result)

    spec, error = protection_rule.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating create protection rule spec", **result)
    if module.check_mode:
        result["response"] = spec
        return

    resp = protection_rule.create(spec)
    uuid = resp["metadata"]["uuid"]
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["protection_rule_uuid"] = uuid
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = protection_rule.read(uuid)

    result["response"] = resp
    pass

def update_protection_rule(module, result):
    pass


def delete_protection_rule(module, result):
    pass


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("protection_rule_uuid", "name"), True),
            ("state", "absent", ("protection_rule_uuid",)),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "protection_rule_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("protection_rule_uuid"):
            update_protection_rule(module, result)
        else:
            create_protection_rule(module, result)
    else:
        delete_protection_rule(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
