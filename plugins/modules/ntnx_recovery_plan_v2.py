#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_plan_v2
short_description: Trigger action operations on a Nutanix Recovery Plan
version_added: 2.7.0
description:
  - This module allows you to trigger Recovery Plan action operations in Nutanix Prism Central.
  - Supported actions are planned failover, test failover, unplanned failover, validate, and cleanup.
  - The Recovery Plan itself must already exist. This module only performs action operations
    against an existing Recovery Plan identified by its external ID.
  - Failover actions must be initiated on the target/destination Prism Central.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the action being performed.
    - >-
      B(Planned Failover / Test Failover / Unplanned Failover Recovery Plan) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin
    - >-
      B(Validate Recovery Plan) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin
    - >-
      B(Cleanup Recovery Plan Resources) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
    state:
        description:
            - State of the module.
            - If state is present, the selected action will be performed on the recovery plan.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the Recovery Plan to perform the action on.
        type: str
        required: true
    action:
        description:
            - The action to perform on the Recovery Plan.
            - C(PLANNED_FAILOVER) triggers a planned failover using the C(planned_failover_recovery_plan) SDK API.
            - C(TEST_FAILOVER) triggers a test failover using the C(test_failover_recovery_plan) SDK API.
            - C(UNPLANNED_FAILOVER) triggers an unplanned failover using the C(unplanned_failover_recovery_plan) SDK API.
            - C(VALIDATE) triggers a Recovery Plan validation using the C(validate_recovery_plan) SDK API.
            - C(CLEANUP) triggers cleanup of resources from the last Recovery Plan execution using the C(cleanup_recovery_plan_resources) SDK API.
        type: str
        required: true
        choices:
            - PLANNED_FAILOVER
            - TEST_FAILOVER
            - UNPLANNED_FAILOVER
            - VALIDATE
            - CLEANUP
    name:
        description:
            - Name of the Recovery Plan Job that will be created for the action.
            - Used only for C(PLANNED_FAILOVER), C(TEST_FAILOVER), C(UNPLANNED_FAILOVER) and C(VALIDATE) actions.
        type: str
        required: false
    failover_directions:
        description:
            - Failover directions describing the source and target disaster recovery locations for the action.
            - Required for C(PLANNED_FAILOVER), C(TEST_FAILOVER), C(UNPLANNED_FAILOVER) and C(VALIDATE) actions.
        type: list
        elements: dict
        required: false
        suboptions:
            source_domain_manager_ext_id:
                description:
                    - External identifier of the source domain manager (source Prism Central).
                type: str
                required: false
            source_cluster:
                description:
                    - Reference to the source cluster from which the entities will fail over.
                type: dict
                required: false
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the cluster entity reference.
                        type: str
                        required: false
                    name:
                        description:
                            - Name of the cluster entity reference.
                        type: str
                        required: false
            target_domain_manager_ext_id:
                description:
                    - External identifier of the target domain manager (target Prism Central).
                type: str
                required: false
            target_cluster:
                description:
                    - Reference to the target cluster to which the entities will fail over.
                type: dict
                required: false
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the cluster entity reference.
                        type: str
                        required: false
                    name:
                        description:
                            - Name of the cluster entity reference.
                        type: str
                        required: false
    should_ignore_warnings:
        description:
            - Indicates whether to continue the recovery plan action despite validation warnings.
            - Applies to C(PLANNED_FAILOVER), C(TEST_FAILOVER) and C(UNPLANNED_FAILOVER) actions.
        type: bool
        required: false
    should_live_migrate_vms:
        description:
            - Indicates whether to live-migrate VMs during the planned failover instead of shutting them down.
            - Applies to C(PLANNED_FAILOVER) only.
        type: bool
        required: false
    is_instant_restore:
        description:
            - Indicates whether to perform an instant restore.
            - Applies to C(TEST_FAILOVER) and C(UNPLANNED_FAILOVER) actions.
        type: bool
        required: false
    recovery_reference_time:
        description:
            - Point in time from which to restore the entities during an C(UNPLANNED_FAILOVER) operation.
            - ISO-8601 formatted timestamp, for example C(2023-01-02T03:04:05Z).
            - When specified, VMs and Volume Groups are restored from the latest recovery points on or before this time.
            - Applies to C(UNPLANNED_FAILOVER) only.
        type: str
        required: false
    post_failover_behaviour:
        description:
            - Post-failover behaviour applied after the action completes.
            - Applies to C(PLANNED_FAILOVER) and C(UNPLANNED_FAILOVER) actions.
        type: dict
        required: false
        suboptions:
            should_pause_protection:
                description:
                    - Whether to pause protection on the entities after failover completes.
                type: bool
                required: false
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
- name: Validate a Recovery Plan
  nutanix.ncp.ntnx_recovery_plan_v2:
    ext_id: "0f79d2a1-6f9b-4b8c-9d1a-3b7cd82bf5c1"
    action: VALIDATE
    name: "recovery_plan_validate_job"
    failover_directions:
      - source_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        source_cluster:
          ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
        target_domain_manager_ext_id: "b7d2f8ee-8f61-46c8-9812-3fb0f9a8a3d0"
        target_cluster:
          ext_id: "0006178c-2f5c-9c1c-1f47-ac1f6b6f97e3"
  register: validate_result
  ignore_errors: true

- name: Trigger a Test Failover of a Recovery Plan
  nutanix.ncp.ntnx_recovery_plan_v2:
    ext_id: "0f79d2a1-6f9b-4b8c-9d1a-3b7cd82bf5c1"
    action: TEST_FAILOVER
    name: "recovery_plan_test_failover_job"
    should_ignore_warnings: true
    is_instant_restore: false
    failover_directions:
      - source_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        source_cluster:
          ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
        target_domain_manager_ext_id: "b7d2f8ee-8f61-46c8-9812-3fb0f9a8a3d0"
        target_cluster:
          ext_id: "0006178c-2f5c-9c1c-1f47-ac1f6b6f97e3"
  register: test_failover_result
  ignore_errors: true

- name: Trigger a Planned Failover of a Recovery Plan
  nutanix.ncp.ntnx_recovery_plan_v2:
    ext_id: "0f79d2a1-6f9b-4b8c-9d1a-3b7cd82bf5c1"
    action: PLANNED_FAILOVER
    name: "recovery_plan_planned_failover_job"
    should_ignore_warnings: false
    should_live_migrate_vms: true
    post_failover_behaviour:
      should_pause_protection: false
    failover_directions:
      - source_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        source_cluster:
          ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
        target_domain_manager_ext_id: "b7d2f8ee-8f61-46c8-9812-3fb0f9a8a3d0"
        target_cluster:
          ext_id: "0006178c-2f5c-9c1c-1f47-ac1f6b6f97e3"
  register: planned_failover_result
  ignore_errors: true

- name: Trigger an Unplanned Failover of a Recovery Plan
  nutanix.ncp.ntnx_recovery_plan_v2:
    ext_id: "0f79d2a1-6f9b-4b8c-9d1a-3b7cd82bf5c1"
    action: UNPLANNED_FAILOVER
    name: "recovery_plan_unplanned_failover_job"
    should_ignore_warnings: true
    is_instant_restore: true
    recovery_reference_time: "2024-01-02T03:04:05Z"
    post_failover_behaviour:
      should_pause_protection: true
    failover_directions:
      - source_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        source_cluster:
          ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
        target_domain_manager_ext_id: "b7d2f8ee-8f61-46c8-9812-3fb0f9a8a3d0"
        target_cluster:
          ext_id: "0006178c-2f5c-9c1c-1f47-ac1f6b6f97e3"
  register: unplanned_failover_result
  ignore_errors: true

- name: Cleanup resources from the last Recovery Plan execution
  nutanix.ncp.ntnx_recovery_plan_v2:
    ext_id: "0f79d2a1-6f9b-4b8c-9d1a-3b7cd82bf5c1"
    action: CLEANUP
  register: cleanup_result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for the requested Recovery Plan action.
        - Task details if C(wait) is true.
        - Initial task-reference response if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2024-11-04T12:00:41.599580+00:00",
            "completion_details": [
                {
                    "name": "recoveryPlanJobExtId",
                    "value": "5f3d92c1-8a5b-4c1a-9d1e-42feab61bd15"
                }
            ],
            "created_time": "2024-11-04T11:59:47.283752+00:00",
            "entities_affected": [
                {
                    "ext_id": "0f79d2a1-6f9b-4b8c-9d1a-3b7cd82bf5c1",
                    "rel": "dataprotection:config:recovery-plan"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:c3f6cc70-fda6-4133-a97c-58802d58186a",
            "is_cancelable": false,
            "last_updated_time": "2024-11-04T12:00:41.599579+00:00",
            "legacy_error_message": null,
            "operation": "RecoveryPlanTestFailover",
            "operation_description": "Test Failover Recovery Plan",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2024-11-04T11:59:47.300538+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while triggering Recovery Plan action"

error:
    description: This field typically holds information about if the task has errors that occurred during the task execution
    returned: when an error occurs
    type: str
    sample: "Failed generating spec for Recovery Plan action"

failed:
    description: This field typically holds information about if the task has failed
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task
    returned: always
    type: str
    sample: "ZXJnb24=:c3f6cc70-fda6-4133-a97c-58802d58186a"

ext_id:
    description: The external ID of the Recovery Plan on which the action was performed
    returned: always
    type: str
    sample: "0f79d2a1-6f9b-4b8c-9d1a-3b7cd82bf5c1"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_plan_actions_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_dataprotection_py_client as data_protection_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_protection_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Some SDK builds of 4.3.x do not expose the PostFailoverBehaviourSpec class or
# the corresponding `post_failover_behaviour` field on the failover-spec
# classes. Resolve the class defensively so the module can still be imported
# on those older builds; SpecGenerator will simply skip the field when the
# underlying SDK spec object does not have that attribute.
_POST_FAILOVER_BEHAVIOUR_SPEC = getattr(
    data_protection_sdk, "PostFailoverBehaviourSpec", None
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

ACTION_PLANNED_FAILOVER = "PLANNED_FAILOVER"
ACTION_TEST_FAILOVER = "TEST_FAILOVER"
ACTION_UNPLANNED_FAILOVER = "UNPLANNED_FAILOVER"
ACTION_VALIDATE = "VALIDATE"
ACTION_CLEANUP = "CLEANUP"

ACTION_CHOICES = [
    ACTION_PLANNED_FAILOVER,
    ACTION_TEST_FAILOVER,
    ACTION_UNPLANNED_FAILOVER,
    ACTION_VALIDATE,
    ACTION_CLEANUP,
]


def get_module_spec():
    entity_reference_spec = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
    )

    failover_direction_spec = dict(
        source_domain_manager_ext_id=dict(type="str"),
        source_cluster=dict(
            type="dict",
            options=entity_reference_spec,
            obj=data_protection_sdk.DataprotectionConfigEntityReference,
        ),
        target_domain_manager_ext_id=dict(type="str"),
        target_cluster=dict(
            type="dict",
            options=entity_reference_spec,
            obj=data_protection_sdk.DataprotectionConfigEntityReference,
        ),
    )

    post_failover_behaviour_spec = dict(
        should_pause_protection=dict(type="bool"),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        action=dict(type="str", required=True, choices=ACTION_CHOICES),
        name=dict(type="str"),
        failover_directions=dict(
            type="list",
            elements="dict",
            options=failover_direction_spec,
            obj=data_protection_sdk.FailoverDirection,
        ),
        should_ignore_warnings=dict(type="bool"),
        should_live_migrate_vms=dict(type="bool"),
        is_instant_restore=dict(type="bool"),
        recovery_reference_time=dict(type="str"),
        post_failover_behaviour=dict(
            type="dict",
            options=post_failover_behaviour_spec,
            obj=_POST_FAILOVER_BEHAVIOUR_SPEC,
        ),
    )
    return module_args


def _build_action_spec(module, result, action):
    """Build the SDK request body for the requested Recovery Plan action.

    Only VALIDATE uses `BaseRecoveryPlanActionSpec`; the failover actions each
    have their own dedicated spec class that includes their specific fields
    (e.g. `should_live_migrate_v_ms` for planned failover).
    """

    if action == ACTION_PLANNED_FAILOVER:
        default_spec = data_protection_sdk.PlannedFailoverSpec()
    elif action == ACTION_TEST_FAILOVER:
        default_spec = data_protection_sdk.TestFailoverSpec()
    elif action == ACTION_UNPLANNED_FAILOVER:
        default_spec = data_protection_sdk.UnplannedFailoverSpec()
    else:
        default_spec = data_protection_sdk.BaseRecoveryPlanActionSpec()

    sg = SpecGenerator(module)
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for Recovery Plan action", **result
        )

    # The SDK spec attribute is `should_live_migrate_v_ms` (snake_case of
    # `shouldLiveMigrateVMs`) while the module param uses the more idiomatic
    # `should_live_migrate_vms`. Copy the value across when running the
    # planned-failover action.
    if action == ACTION_PLANNED_FAILOVER:
        should_live_migrate_vms = module.params.get("should_live_migrate_vms")
        if should_live_migrate_vms is not None and hasattr(
            spec, "should_live_migrate_v_ms"
        ):
            spec.should_live_migrate_v_ms = should_live_migrate_vms

    return spec


def planned_failover_recovery_plan(module, api_instance, result):
    validate_required_params(module, ["failover_directions"])
    spec = _build_action_spec(module, result, ACTION_PLANNED_FAILOVER)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    ext_id = module.params.get("ext_id")
    try:
        resp = api_instance.planned_failover_recovery_plan(
            recoveryPlanExtId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while triggering Planned Failover on Recovery Plan",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def test_failover_recovery_plan(module, api_instance, result):
    validate_required_params(module, ["failover_directions"])
    spec = _build_action_spec(module, result, ACTION_TEST_FAILOVER)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    ext_id = module.params.get("ext_id")
    try:
        resp = api_instance.test_failover_recovery_plan(
            recoveryPlanExtId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while triggering Test Failover on Recovery Plan",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def unplanned_failover_recovery_plan(module, api_instance, result):
    validate_required_params(module, ["failover_directions"])
    spec = _build_action_spec(module, result, ACTION_UNPLANNED_FAILOVER)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    ext_id = module.params.get("ext_id")
    try:
        resp = api_instance.unplanned_failover_recovery_plan(
            recoveryPlanExtId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while triggering Unplanned Failover on Recovery Plan",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def validate_recovery_plan(module, api_instance, result):
    validate_required_params(module, ["failover_directions"])
    spec = _build_action_spec(module, result, ACTION_VALIDATE)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    ext_id = module.params.get("ext_id")
    try:
        resp = api_instance.validate_recovery_plan(recoveryPlanExtId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while triggering Validate on Recovery Plan",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def cleanup_recovery_plan_resources(module, api_instance, result):
    ext_id = module.params.get("ext_id")

    if module.check_mode:
        result["response"] = {
            "ext_id": ext_id,
            "action": ACTION_CLEANUP,
        }
        result["msg"] = (
            "Recovery Plan resources cleanup will be triggered for "
            "ext_id: {0}".format(ext_id)
        )
        return

    try:
        resp = api_instance.cleanup_recovery_plan_resources(recoveryPlanExtId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while triggering Cleanup on Recovery Plan resources",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


ACTION_DISPATCH = {
    ACTION_PLANNED_FAILOVER: planned_failover_recovery_plan,
    ACTION_TEST_FAILOVER: test_failover_recovery_plan,
    ACTION_UNPLANNED_FAILOVER: unplanned_failover_recovery_plan,
    ACTION_VALIDATE: validate_recovery_plan,
    ACTION_CLEANUP: cleanup_recovery_plan_resources,
}


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_dataprotection_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": module.params.get("ext_id"),
        "task_ext_id": None,
    }

    api_instance = get_recovery_plan_actions_api_instance(module)
    action = module.params.get("action")
    handler = ACTION_DISPATCH.get(action)
    if handler is None:
        module.fail_json(
            msg="Unsupported Recovery Plan action: {0}".format(action), **result
        )
    handler(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
