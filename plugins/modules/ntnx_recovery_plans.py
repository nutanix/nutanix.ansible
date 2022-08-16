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
    stage = dict(
        vms = dict(type="list", elements="dict", options=entity_spec, mutually_exclusive=[("name", "uuid")], required=False),
        categories = dict(type="dict", required=False),
        delay = dict(type="int", required=False)
    )
    availability_zone = dict(
        url = dict(type="str", required=True),
        cluster = dict(type="str", required=False)
    )
    network=dict(
        name=dict(type="str", required=True),
        gateway_ip=dict(type="str", required=False),
        prefix=dict(type="int", required=False),
        external_connectivity_state=dict(type="bool", required=False)
    )
    site_network=dict(
        test=dict(type="dict", option=network, required=False),
        prod=dict(type="dict", option=network, required=False),
    )
    network_mapping = dict(
        primary_site = dict(type="dict", options=site_network, required=True),
        recovery_site = dict(type="dict", options=site_network, required=True),
        are_networks_stretched = dict(type="bool", required=False)
    )
    module_args = dict(
        name = dict(type="str", required=False),
        desc = dict(type="str", required=False),
        stages = dict(type="list", elements="dict", options=stage, required=False),
        primary_location = dict(type="dict", options=availability_zone, required=False),
        recovery_location = dict(type="dict", options=availability_zone, required=False),
        network_mappings = dict(type="list", elements="dict", options=network_mapping, required=False)
    )
    return module_args


def create_recovery_plan(module, result):
    pass

def update_recovery_plan(module, result):
    pass


def delete_recovery_plan(module, result):
    pass


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("recovery_plan_uuid", "name"), True),
            ("state", "absent", ("recovery_plan_uuid",)),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "recovery_plan_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("protection_rule_uuid"):
            update_recovery_plan(module, result)
        else:
            create_recovery_plan(module, result)
    else:
        delete_recovery_plan(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
