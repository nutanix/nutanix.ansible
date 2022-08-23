#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_protection_rules
short_description: 'module for create, update and delete protection rule'
version_added: 1.5.0
description: 'module for create, update and delete protection rule'
options:
  rule_uuid:
    description: protection_rule uuid
    type: str
    required: false
  start_time:
    description:
      - >-
        Time of the day, the policy will be started. This is in "h:m" format.
        The values must be between 00h:00m and 23h:59m. For example user
        specified 18h:00m and the current time is 17h:00m then the first
        snapshot will be captured at 18h:00m. If the current time is 19h:00m
        then the first snapshot will be captured at 18h:00m next day. If not
        set, policy will be applicable immediately.
    type: str
    required: false
  name:
    description: Protection Rule name
    type: str
    required: false
  desc:
    description: A description for the protection rule.
    type: str
    required: false
  protected_categories:
    description: Categories for the protection_rule. This allows assigning one value of a key to any entity. Changes done in this will be reflected in the categories_mapping field.
    type: dict
    required: true
  primary_site:
    description:  it constitutes the primary locations of this Protection Rule.
    type: dict
    required: true
    suboptions:
      availability_zone_url:
        description: This represents the source availability zone where the entity is running.
        type: str
        required: true
      cluster_uuid:
        description: cluster UUID
        type: str
        required: false
  schedules:
    description: write
    type: list
    elements: dict
    required: true
    suboptions:
      source:
        description: write
        type: dict
        required: false
        suboptions:
          availability_zone_url:
            description: This represents the availability zone where the entity needs to be replicated to.
            type: str
            required: true
          cluster_uuid:
            description: cluster UUID
            type: str
            required: false
      destination:
        description: write
        type: dict
        required: false
        suboptions:
          availability_zone_url:
            description: write
            type: str
            required: true
          cluster_uuid:
            description: write
            type: str
            required: false
      protection_type:
        description: write
        type: str
        required: true
        choices:
          - SYNC
          - ASYNC
      auto_suspend_timeout:
        description: Auto suspend timeout in case of connection failure between the sites. If not set, then policy will not be suspended in case of site connection failure.
        type: int
        required: false
      rpo:
        description: write
        type: int
        required: false
      rpo_unit:
        description: write
        type: str
        required: false
        choices:
          - MINUTE
          - HOUR
          - DAY
          - WEEK
      snapshot_type:
        description: Crash consistent or Application Consistent snapshot
        type: str
        required: false
        choices:
          - CRASH_CONSISTENT
          - APPLICATION_CONSISTENT
      local_retention_policy:
        description: write
        type: dict
        required: false
        suboptions:
          num_snapshots:
            description: Number of snapshots need to be retained. This will be set in case of linear snapshot retention.
            type: int
            required: false
          rollup_retention_policy:
            description: write
            type: dict
            required: false
            suboptions:
              multiple:
                description:
                  - >-
                    Multiplier to 'snapshot_interval_type'. For example if
                    'snapshot_interval_type' is "YEARLY" and 'multiple' is 5,
                    then 5 years worth of rollup snapshots will be retained.
                type: int
                required: true
              snapshot_interval_type:
                description: Snapshot interval period.
                type: str
                required: true
                choices:
                  - HOURLY
                  - DAILY
                  - WEEKLY
                  - MONTHLY
                  - YEARLY
      remote_retention_policy:
        description: >-
          This describes the snapshot retention policy for this availability
          zone. This translates into how many snapshots taken as part of this
          protection rule need to be retained on this availability zone.
        type: dict
        required: false
        suboptions:
          num_snapshots:
            description: >-
              Number of snapshots need to be retained. This will be set in case
              of linear snapshot retention.
            type: int
            required: false
          rollup_retention_policy:
            description: Maximum snapshot retention time with rollup schedules.
            type: dict
            required: false
            suboptions:
              multiple:
                description:
                  - >-
                    Multiplier to 'snapshot_interval_type'. For example if
                    'snapshot_interval_type' is "YEARLY" and 'multiple' is 5,
                    then 5 years worth of rollup snapshots will be retained.
                type: int
                required: true
              snapshot_interval_type:
                description: Snapshot interval period.
                type: str
                required: true
                choices:
                  - HOURLY
                  - DAILY
                  - WEEKLY
                  - MONTHLY
                  - YEARLY
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations
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
from ..module_utils.prism.protection_rules import ProtectionRule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402


def get_module_spec():
    rollup_policy = dict(
        multiple=dict(type="int", required=True),
        snapshot_interval_type=dict(
            type="str",
            choices=["HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"],
            required=True,
        ),
    )
    snapshot_retention_policy = dict(
        num_snapshots=dict(type="int", required=False),
        rollup_retention_policy=dict(
            type="dict", options=rollup_policy, required=False
        ),
    )

    availability_zone = dict(
        availability_zone_url=dict(type="str", required=True),
        cluster_uuid=dict(type="str", required=False),
    )

    schedule = dict(
        source=dict(type="dict", options=availability_zone, required=False),
        destination=dict(type="dict", options=availability_zone, required=False),
        protection_type=dict(type="str", choices=["SYNC", "ASYNC"], required=True),
        auto_suspend_timeout=dict(type="int", required=False),
        rpo=dict(type="int", required=False),
        rpo_unit=dict(
            type="str", choices=["MINUTE", "HOUR", "DAY", "WEEK"], required=False
        ),
        snapshot_type=dict(
            type="str",
            choices=["CRASH_CONSISTENT", "APPLICATION_CONSISTENT"],
            required=False,
        ),
        local_retention_policy=dict(
            type="dict",
            options=snapshot_retention_policy,
            mutually_exclusive=[("num_snapshots", "rollup_retention_policy")],
            required=False,
        ),
        remote_retention_policy=dict(
            type="dict",
            options=snapshot_retention_policy,
            mutually_exclusive=[("num_snapshots", "rollup_retention_policy")],
            required=False,
        ),
    )

    module_args = dict(
        rule_uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        start_time=dict(type="str", required=False),
        schedules=dict(type="list", elements="dict", options=schedule, required=True),
        protected_categories=dict(type="dict", required=True),
        primary_site=dict(type="dict", options=availability_zone, required=True),
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
    result["rule_uuid"] = uuid
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = protection_rule.read(uuid)

    result["response"] = resp


def check_rule_idempotency(rule_spec, update_spec):
    # check if primary location is updated
    if rule_spec["spec"]["resources"].get("primary_location_list") != update_spec[
        "spec"
    ]["resources"].get("primary_location_list"):
        return False

    # check if categories have updated
    if rule_spec["spec"]["resources"].get("category_filter") != update_spec["spec"][
        "resources"
    ].get("category_filter"):
        return False

    # check if availibility zones have updated
    if len(rule_spec["spec"]["resources"]["ordered_availability_zone_list"]) != len(
        update_spec["spec"]["resources"]["ordered_availability_zone_list"]
    ):
        return False

    for az in update_spec["spec"]["resources"]["ordered_availability_zone_list"]:
        if az not in rule_spec["spec"]["resources"]["ordered_availability_zone_list"]:
            return False

    # check if schedules have updated
    if len(
        rule_spec["spec"]["resources"]["availability_zone_connectivity_list"]
    ) != len(update_spec["spec"]["resources"]["availability_zone_connectivity_list"]):
        return False

    for schedule in update_spec["spec"]["resources"][
        "availability_zone_connectivity_list"
    ]:
        if (
            schedule
            not in rule_spec["spec"]["resources"]["availability_zone_connectivity_list"]
        ):
            return False

    # check first level of entities if update is required (for fields like name and desc)
    if rule_spec != update_spec:
        return False

    return True


def update_protection_rule(module, result):
    protection_rule = ProtectionRule(module)
    rule_uuid = module.params.get("rule_uuid")
    result["rule_uuid"] = rule_uuid

    resp = protection_rule.read(uuid=rule_uuid)
    utils.strip_extra_attrs(resp["status"], resp["spec"])
    resp["spec"] = resp.pop("status")

    update_spec, error = protection_rule.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating protection rule update spec", **result)

    # check for idempotency
    if check_rule_idempotency(resp, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    if module.check_mode:
        result["response"] = update_spec
        return

    resp = protection_rule.update(data=update_spec, uuid=rule_uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["changed"] = True

    if module.params.get("wait"):
        tasks = Task(module)
        tasks.wait_for_completion(task_uuid)
        resp = protection_rule.read(uuid=rule_uuid)

    result["response"] = resp


def delete_protection_rule(module, result):
    protection_rule = ProtectionRule(module)
    rule_uuid = module.params["rule_uuid"]
    resp = protection_rule.delete(uuid=rule_uuid)
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
            ("state", "present", ("name", "rule_uuid"), True),
            ("state", "absent", ("rule_uuid",)),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "rule_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("rule_uuid"):
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


EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.protection_rules import ProtectionRule
from ..module_utils.prism.tasks import Task  # noqa: E402


def get_module_spec():
    rollup_policy = dict(
        multiple=dict(type="int", required=True),
        snapshot_interval_type=dict(
            type="str",
            choices=["HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"],
            required=True,
        ),
    )
    snapshot_retention_policy = dict(
        num_snapshots=dict(type="int", required=False),
        rollup_retention_policy=dict(
            type="dict", options=rollup_policy, required=False
        ),
    )

    availability_zone = dict(
        availability_zone_url=dict(type="str", required=True),
        cluster_uuid=dict(type="str", required=False),
    )

    schedule = dict(
        source=dict(type="dict", options=availability_zone, required=False),
        destination=dict(type="dict", options=availability_zone, required=False),
        protection_type=dict(type="str", choices=["SYNC", "ASYNC"], required=True),
        auto_suspend_timeout=dict(type="int", required=False),
        rpo=dict(type="int", required=False),
        rpo_unit=dict(
            type="str", choices=["MINUTE", "HOUR", "DAY", "WEEK"], required=False
        ),
        snapshot_type=dict(
            type="str",
            choice=["CRASH_CONSISTENT", "APPLICATION_CONSISTENT"],
            required=False,
        ),
        local_retention_policy=dict(
            type="dict",
            options=snapshot_retention_policy,
            mutually_exclusive=[("num_snapshots", "rollup_retention_policy")],
            required=False,
        ),
        remote_retention_policy=dict(
            type="dict",
            options=snapshot_retention_policy,
            mutually_exclusive=[("num_snapshots", "rollup_retention_policy")],
            required=False,
        ),
    )

    module_args = dict(
        rule_uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        start_time=dict(type="str", required=False),
        schedules=dict(type="list", elements="dict", options=schedule, required=False),
        protected_categories=dict(type="dict", required=False),
        primary_site=dict(type="dict", options=availability_zone, required=False),
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
    result["rule_uuid"] = uuid
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = protection_rule.read(uuid)

    result["response"] = resp


def check_rule_idempotency(rule_spec, update_spec):
    # check if primary location is updated
    if rule_spec["spec"]["resources"].get("primary_location_list") != update_spec[
        "spec"
    ]["resources"].get("primary_location_list"):
        return False

    # check if categories have updated
    if rule_spec["spec"]["resources"].get("category_filter") != update_spec["spec"][
        "resources"
    ].get("category_filter"):
        return False

    # check if availibility zones have updated
    if len(rule_spec["spec"]["resources"]["ordered_availability_zone_list"]) != len(
        update_spec["spec"]["resources"]["ordered_availability_zone_list"]
    ):
        return False

    for az in update_spec["spec"]["resources"]["ordered_availability_zone_list"]:
        if az not in rule_spec["spec"]["resources"]["ordered_availability_zone_list"]:
            return False

    # check if schedules have updated
    if len(
        rule_spec["spec"]["resources"]["availability_zone_connectivity_list"]
    ) != len(update_spec["spec"]["resources"]["availability_zone_connectivity_list"]):
        return False

    for schedule in update_spec["spec"]["resources"][
        "availability_zone_connectivity_list"
    ]:
        if (
            schedule
            not in rule_spec["spec"]["resources"]["availability_zone_connectivity_list"]
        ):
            return False

    # check first level of entities if update is required (for fields like name and desc)
    if rule_spec != update_spec:
        return False

    return True


def update_protection_rule(module, result):
    protection_rule = ProtectionRule(module)
    rule_uuid = module.params.get("rule_uuid")
    result["rule_uuid"] = rule_uuid

    resp = protection_rule.read(uuid=rule_uuid)
    utils.strip_extra_attrs(resp["status"], resp["spec"])
    resp["spec"] = resp.pop("status")

    update_spec, error = protection_rule.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating protection rule update spec", **result)

    # check for idempotency
    if check_rule_idempotency(resp, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    if module.check_mode:
        result["response"] = update_spec
        return

    resp = protection_rule.update(data=update_spec, uuid=rule_uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["changed"] = True

    if module.params.get("wait"):
        tasks = Task(module)
        tasks.wait_for_completion(task_uuid)
        resp = protection_rule.read(uuid=rule_uuid)

    result["response"] = resp


def delete_protection_rule(module, result):
    protection_rule = ProtectionRule(module)
    rule_uuid = module.params["rule_uuid"]
    resp = protection_rule.delete(uuid=rule_uuid)
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
            ("state", "present", ("name", "rule_uuid"), True),
            ("state", "present", ("schedules", "rule_uuid"), True),
            ("state", "present", ("protected_categories", "rule_uuid"), True),
            ("state", "present", ("primary_site", "rule_uuid"), True),
            ("state", "absent", ("rule_uuid",)),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "rule_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("rule_uuid"):
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
