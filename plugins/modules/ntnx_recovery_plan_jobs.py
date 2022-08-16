#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from re import T
from zoneinfo import available_timezones

from plugins.module_utils import entity

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

# TO-DO: Add floating IP assignment spec
def get_module_spec():
    entity_spec = dict(
        uuid = dict(type="str", required=False),
        name = dict(type="str", required=False)
    )
    availability_zone = dict(
        url = dict(type="str", required=True),
        cluster = dict(type="str", required=False)
    )
    module_args = dict(
        name = dict(type="str", required=False),
        recovery_plan = dict(type="dict", options=entity_spec, mutually_exclusive=[("name", "uuid")], required=False),
        failing_from_zone = dict(type="dict", options=availability_zone, required=False),
        recovery_zone = dict(type="dict", options=availability_zone, required=False),
        action = dict(type="str", options=["VALIDATE", "MIGRATE", "FAILOVER", "TEST_FAILOVER", "LIVE_MIGRATE", "CLEANUP", "RERUN"], required=False),
        recovery_reference_time = dict(type="str", required=False),
        ignore_validation_failures = dict(type="bool", required=False)
    )
    return module_args

def create_job(module, result):
    # creating job will also execute it 
    pass

def delete_job(module, result):
    pass

def perform_action_on_job(module, result):
    # for cleanup and reruns of recovery jobs
    pass

def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("recovery_plan_uuid",)),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "recovery_plan_uuid": None}
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
