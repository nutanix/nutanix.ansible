#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

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
from ..module_utils.prism.recovery_plans import RecoveryPlan  # noqa: E402

# TO-DO: Add floating IP assignment spec
def get_module_spec():
    
    vm_spec = dict(
        uuid = dict(type="str", required=False),
        name = dict(type="str", required=False),
        enable_script_exec = dict(type="bool", required=False)
    )
    entity_by_spec = dict(
        uuid = dict(type="str", required=False),
        name = dict(type="str", required=False),
    )
    category = dict(
        key = dict(type="str", required=False),
        value = dict(type="str", required=False),
        enable_script_exec = dict(type="bool", required=False)
    )
    stage = dict(
        vms = dict(type="list", elements="dict", options=vm_spec, mutually_exclusive=[("name", "uuid")], required=False),
        categories = dict(type="list", elements="dict", options=category, required=False),
        delay = dict(type="int", required=False)
    )
    availability_zone = dict(
        url = dict(type="str", required=True),
        cluster = dict(type="str", required=False)
    )
    custom_ip_config = dict(
        vm = dict(type="dict", options=entity_by_spec, mutually_exclusive=[("name", "uuid")], required=True),
        ip = dict(type="str", required=True),
    )
    network=dict(
        name=dict(type="str", required=True),
        gateway_ip=dict(type="str", required=False),
        prefix=dict(type="int", required=False),
        external_connectivity_state=dict(type="bool", required=False),
        custom_ip_conifg = dict(type="list", elements="dict", options=custom_ip_config, required=False)
    )
    site_network=dict(
        test=dict(type="dict", option=network, required=False),
        prod=dict(type="dict", option=network, required=False),
    )

    # TO-DO: Test Custom IP mappings and add spec according to them
    network_mapping = dict(
        primary = dict(type="dict", options=site_network, required=True),
        recovery = dict(type="dict", options=site_network, required=True),
    )
    module_args = dict(
        plan_uuid = dict(type="str", required=False),
        name = dict(type="str", required=False),
        desc = dict(type="str", required=False),
        stages = dict(type="list", elements="dict", options=stage, required=False),
        primary_location = dict(type="dict", options=availability_zone, required=False),
        recovery_location = dict(type="dict", options=availability_zone, required=False),
        network_mappings = dict(type="list", elements="dict", options=network_mapping, required=False),
        network_type = dict(type="str", choices=["STRETCH", "NON_STRETCH"], required=True)
    )
    return module_args


def create_recovery_plan(module, result):
    recovery_plan = RecoveryPlan(module)
    name = module.params["name"]
    if recovery_plan.get_uuid(name):
        module.fail_json(msg="Recovery Plan with given name already exists", **result)

    spec, error = recovery_plan.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating create recovery plan spec", **result)
    if module.check_mode:
        result["response"] = spec
        return

    resp = recovery_plan.create(spec)
    uuid = resp["metadata"]["uuid"]
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["plan_uuid"] = uuid
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = recovery_plan.read(uuid)

    result["response"] = resp

def check_recovery_plan_idempotency(old_spec, update_spec):
    # order of elements in availability_zone_list and stages are also significant hence they can be directly compared while comparing first level of fields
    # while each element of network_mappings have to checked as order of mappings is not significant in this case
    old_ntw_mappings = old_spec["spec"]["resources"]["parameters"]["network_mapping_list"]
    update_ntw_mappings = update_spec["spec"]["resources"]["parameters"]["network_mapping_list"]

    if len(old_ntw_mappings) != len(update_ntw_mappings):
        return False
    for mapping in update_ntw_mappings:
        if mapping not in old_ntw_mappings:
            return False
    
    # check first level of fields
    if old_spec != update_spec:
        return False
    
    return True
    

def update_recovery_plan(module, result):
    recovery_plan = RecoveryPlan(module)
    plan_uuid = module.params.get("plan_uuid")
    result["plan_uuid"] = plan_uuid

    resp = recovery_plan.read(uuid=plan_uuid)
    utils.strip_extra_attrs(resp["status"], resp["spec"])
    resp["spec"] = resp.pop("status")
    # remove stage_uuid of all stages
    for stage in resp["spec"]["resources"]["stage_list"]:
        stage.pop("stage_uuid")

    update_spec, error = recovery_plan.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating recovery plan update spec", **result)

    # check for idempotency
    if check_recovery_plan_idempotency(resp, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    if module.check_mode:
        result["response"] = update_spec
        return

    resp = recovery_plan.update(data=update_spec, uuid=plan_uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["changed"] = True

    if module.params.get("wait"):
        tasks = Task(module)
        tasks.wait_for_completion(task_uuid)
        resp = recovery_plan.read(uuid=plan_uuid)

    result["response"] = resp


def delete_recovery_plan(module, result):
    recovery_plan = RecoveryPlan(module)
    plan_uuid = module.params["plan_uuid"]
    resp = recovery_plan.delete(uuid=plan_uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["changed"] = True

    if module.params.get("wait"):
        tasks = Task(module)
        resp = tasks.wait_for_completion(task_uuid)
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("plan_uuid", "name"), True),
            ("state", "absent", ("plan_uuid",)),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "plan_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("plan_uuid"):
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
