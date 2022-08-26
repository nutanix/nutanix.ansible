#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
allowed_actions_on_recovery_plan_job = ["CLEANUP"]

DOCUMENTATION = r"""
module: ntnx_recovery_plan_jobs
short_description: Create/Run recovery plan jobs related to recovery plan
version_added: 1.5.0
description: Create/Run recovery plan jobs related to recovery plan
options:
  name:
    description: Recovery Plan Job name.
    type: str
    required: false
  job_uuid:
    description:
      - recovery_plan_job uuid
      - only required for running cleanup for Test Failover jobs
    type: str
    required: false
  recovery_plan:
    description: The reference to a recovery_plan
    type: dict
    required: false
    suboptions:
      name:
        description:
          - recovery plan name
          - mutually exclusive with C(uuid)
        type: str
        required: false
      uuid:
        description:
          - recovery plan UUID
          - mutually exclusive with C(name)
        type: str
        required: false
  failed_site:
    description: Availability Zones that have failed.
    type: dict
    required: false
    suboptions:
      url:
        description: URL of the Availability Zone.
        type: str
        required: true
      cluster:
        description: >-
          cluster references. This is applicable only in scenario where failed
          and recovery clusters both are managed by the same Availability Zone.
        type: str
        required: false
  recovery_site:
    description: Availability Zones wherein entities need to be recovered.
    type: dict
    required: false
    suboptions:
      url:
        description: URL of the Availability Zone.
        type: str
        required: true
      cluster:
        description: >-
          cluster references. This is applicable only in scenario where failed
          and recovery clusters both are managed by the same Availability Zone.
        type: str
        required: false
  action:
    description: >-
      Type of action performed by the Recovery Plan Job. VALIDATE - Performs the
      validation of the Recovery Plan. The validation includes checks for the
      presence of entities, networks, categories etc. referenced in the Recovery
      Plan. MIGRATE - VM would be powered off on the sourece before migrating it
      to the recovery Availability Zone. FAILOVER - Restore the entity from the
      recovery points on the recovery Availability Zone. TEST_FAILOVER - Same as
      FAILOVER but on a test network. LIVE_MIGRATE - Migrate without powering
      off the VM. CLEANUP - for cleaning entities created usnig test failover
    type: str
    required: true
    choices:
      - VALIDATE
      - MIGRATE
      - FAILOVER
      - TEST_FAILOVER
      - LIVE_MIGRATE
      - CLEANUP
  recovery_reference_time:
    description: >-
      Time with respect to which Recovery Plan Job has to be executed. This time
      will be used as reference time with respect to which latest snapshot will
      have to be restored in case of failover. For example, if failover is
      required to be done using snapshot created on or before yesterday '2:00'
      PM, then recovery_reference_time will be set to this time.
    type: str
    required: false
  ignore_validation_failures:
    description: >-
      Whether to ignore the validation failures(e.g. Network mapping is missing
      for some networks on failed Availability Zone, Virtual network missing.)
      for the Recovery Plan actions MIGRATE, FAILOVER, TEST_FAILOVER and execute
      the Recovery Plan.
    type: bool
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Pradeepsingh Bhati (@bhati-pradeep)
"""


EXAMPLES = r"""
- name: Run Test Failover without ignoring validation failures
  ntnx_recovery_plan_jobs:
    nutanix_host: "{{recovery_site_ip}}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
    state: "present"
    name: test-failover-with-errors
    recovery_plan:
      name: "{{recovery_plan.response.status.name}}"
    failed_site:
      url: "{{primary_az_url}}"
    recovery_site:
      url: "{{dr.recovery_az_url}}"
    action: TEST_FAILOVER
  ignore_errors: true
  no_log: true

  register: result

- name: Run Test Failover ignoring validation failures
  ntnx_recovery_plan_jobs:
    nutanix_host: "{{recovery_site_ip}}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
    state: "present"
    name: test-failover
    recovery_plan:
      uuid: "{{recovery_plan.plan_uuid}}"
    failed_site:
      url: "{{primary_az_url}}"
    recovery_site:
      url: "{{recovery_az_url}}"
    action: TEST_FAILOVER
    ignore_validation_failures: true

  register: test_failover_job

- name: Run Cleanup
  ntnx_recovery_plan_jobs:
    job_uuid: "{{test_failover_job.job_uuid}}"
    nutanix_host: "{{recovery_site_ip}}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: "{{ validate_certs }}"
    state: "present"
    action: CLEANUP
  register: result

"""

RETURN = r"""
"""
import time  # noqa: E402

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.recovery_plan_jobs import RecoveryPlanJob  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402


# TO-DO: Add floating IP assignment spec
def get_module_spec():
    entity_spec = dict(
        uuid=dict(type="str", required=False), name=dict(type="str", required=False)
    )
    availability_zone = dict(
        url=dict(type="str", required=True), cluster=dict(type="str", required=False)
    )
    module_args = dict(
        name=dict(type="str", required=False),
        job_uuid=dict(type="str", required=False),
        recovery_plan=dict(
            type="dict",
            options=entity_spec,
            mutually_exclusive=[("name", "uuid")],
            required=False,
        ),
        failed_site=dict(type="dict", options=availability_zone, required=False),
        recovery_site=dict(type="dict", options=availability_zone, required=False),
        action=dict(
            type="str",
            choices=[
                "VALIDATE",
                "MIGRATE",
                "FAILOVER",
                "TEST_FAILOVER",
                "LIVE_MIGRATE",
                "CLEANUP",
            ],
            required=True,
        ),
        recovery_reference_time=dict(type="str", required=False),
        ignore_validation_failures=dict(type="bool", required=False),
    )
    return module_args


def get_recovery_plan_job_uuid(module, task_uuid):
    """
    This function extracts recovery plan job uuid from task status.
    It polls for 10 mins untill the recovery plan job uuid comes up in task response.
    """
    task = Task(module)
    timeout = time.time() + 600
    while True:
        time.sleep(5)
        response = task.read(task_uuid, raise_error=False)

        # check for recovery plan job uuid
        for ref in response["entity_reference_list"]:
            if ref["kind"] == "recovery_plan_job":
                return ref["uuid"], None

        if time.time() > timeout:
            return (
                None,
                "Failed to get recovery plan job uuid. Reason: Timeout.",
            )


def create_job(module, result):
    recovery_plan_job = RecoveryPlanJob(module)

    spec, error = recovery_plan_job.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating recovery plan job spec", **result)
    if module.check_mode:
        result["response"] = spec
        return

    resp = recovery_plan_job.create(spec)
    task_uuid = resp["task_uuid"]

    job_uuid, err = get_recovery_plan_job_uuid(module, task_uuid)
    if err:
        result["error"] = error
        module.fail_json(msg="Failed creating recovery plan job", **result)

    result["job_uuid"] = job_uuid
    resp = recovery_plan_job.read(job_uuid)
    resp["response"] = resp
    resp["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid, raise_error=False)

        # get job status
        job_uuid, err = get_recovery_plan_job_uuid(module, task_uuid)
        if err:
            result["error"] = error
            module.fail_json(msg="Failed creating recovery plan job", **result)
        job_status = recovery_plan_job.read(job_uuid)

        # get overall task status
        task_status = task.read(task_uuid)
        if task_status["status"] == "FAILED":
            result["error"] = job_status
            module.fail_json(msg="Recovery plan job failed", **result)
        result["response"] = job_status
        result["changed"] = True


def perform_action_on_job(module, result):
    job_uuid = module.params.get("job_uuid")
    if not job_uuid:
        err_msg = "job_uuid is a required field for 'CLEANUP' and 'RERUN' action"
        module.fail_json(msg=err_msg, **result)

    action = module.params["action"]

    if action not in allowed_actions_on_recovery_plan_job:
        err_msg = (
            "Only 'CLEANUP' action can be performed on existing recovery plan jobs"
        )
        module.fail_json(msg=err_msg, **result)

    if module.check_mode:
        result["response"] = {}
        return

    recovery_plan_job = RecoveryPlanJob(module)
    resp = recovery_plan_job.perform_action_on_existing_job(job_uuid, action)
    task_uuid = resp["task_uuid"]
    job_uuid, error = get_recovery_plan_job_uuid(module, task_uuid)
    if error:
        result["error"] = error
        module.fail_json(
            msg="Failed performing action on existing recovery plan job", **result
        )

    result["job_uuid"] = job_uuid
    resp = recovery_plan_job.read(job_uuid)
    resp["response"] = resp
    resp["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid, raise_error=False)

        # get job status
        job_uuid, err = get_recovery_plan_job_uuid(module, task_uuid)
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed performing action on existing recovery plan job", **result
            )

        job_status = recovery_plan_job.read(job_uuid)

        # get overall task status
        task_status = task.read(task_uuid)
        if task_status["status"] == "FAILED":
            result["error"] = job_status
            module.fail_json(msg="Recovery plan job failed", **result)
        result["response"] = job_status
        result["changed"] = True


def run_module():
    # mutually_exclusive_list have params which are not allowed together
    # we only need recovery plan job's uuid for cleanup and rerun actions
    # hence blocking other fields when recovery plan job uuid is given
    mutually_exclusive_list = [
        ("job_uuid", "recovery_plan"),
        ("job_uuid", "recovery_reference_time"),
        ("job_uuid", "failed_site"),
        ("job_uuid", "recovery_site"),
        ("job_uuid", "name"),
        ("job_uuid", "ignore_validation_failures"),
    ]
    required_if_list = [
        ("state", "present", ("name", "job_uuid"), True),
        ("state", "present", ("recovery_plan", "job_uuid"), True),
        ("state", "present", ("failed_site", "job_uuid"), True),
        ("state", "present", ("recovery_site", "job_uuid"), True),
    ]
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=mutually_exclusive_list,
        required_if=required_if_list,
    )
    utils.remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "job_uuid": None,
    }
    if module.params["action"] in allowed_actions_on_recovery_plan_job:
        perform_action_on_job(module, result)
    else:
        create_job(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
