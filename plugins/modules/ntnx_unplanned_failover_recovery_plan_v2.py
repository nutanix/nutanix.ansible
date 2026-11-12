#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_unplanned_failover_recovery_plan_v2
short_description: Trigger an unplanned failover on a Nutanix Recovery Plan
version_added: 2.7.0
description:
    - Trigger an unplanned failover on a Recovery Plan identified by its external ID.
    - Restore the entity from the recovery points on the target domain manager.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Planned Failover on a Recovery Plan) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Project Manager, Self-Service Admin (Deprecated), Super Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will trigger an unplanned failover.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the Recovery Plan on which the unplanned
              failover action must be executed.
        type: str
        required: true
    name:
        description:
            - Name of the Recovery Plan Job.
        type: str
        required: true
    should_ignore_warnings:
        description:
            - Indicates whether to continue the recovery plan action despite validation warnings.
            - For example, if the IP of some virtual machines (VMs) cannot be preserved after recovery,
              the Recovery Plan action can still be initiated by passing shouldIgnoreWarnings as true.
            - This value allows the recovery operations to continue despite the validation warnings.
            - Alternatively, the user can choose to resolve the validation warnings and trigger another failover action on recovery plan.
        type: bool
        default: false
    recovery_reference_time:
        description:
            - Point in time from which to restore the entities during an UNPLANNED_FAILOVER operation.
            - Only ISO-8601 formatted timestamps are supported. For example, 2023-01-02T03:04:05Z.
            - When specified, virtual machines (VMs) and volume groups are restored from the latest recovery points
              created on or before the specified timestamp. If not specified, virtual machines (VMs) and volume groups are
              restored from the latest recovery points created on or before the start of the Recovery plan job.
        type: str
    failover_directions:
        description:
            - List of failover directions from source disaster recovery location to target disaster recovery location.
            - For example, when failing over virtual machines (VMs) and volume groups from clusters C1, C2 registered to domain manager PC1 on source location
              to cluster C3 registered to domain manager PC1 on target location, there must be one direction between source location (PC1, C1)
              to target location (PC1, C3) and another mapping between source location (PC1, C2) and target location (PC1, C3).
            - Domain manager is a required parameter while describing disaster recovery location in failover directions.
            - When creating a Recovery Plan Job across two domain managers, the source clusters are not required.
            - Failover direction contains clusters only when failing over between primary and secondary clusters registered to the same domain manager.
        type: list
        elements: dict
        required: true
        suboptions:
            source_domain_manager_ext_id:
                description:
                    - External identifier of the Prism Central instance
                      managing the source cluster.
                type: str
                required: true
            source_cluster:
                description:
                    - External reference of the source cluster.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the source cluster.
                        type: str
                        required: true
            target_domain_manager_ext_id:
                description:
                    - External identifier of the target domain manager.
                type: str
                required: true
            target_cluster:
                description:
                    - External reference of the target cluster.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the target cluster.
                        type: str
                        required: true
    post_failover_behaviour:
        description:
            - Defines the overall set of behaviors that should be applied after a failover.
        type: dict
        suboptions:
            should_pause_protection:
                description:
                    - Defines whether to pause protection of the recovered workloads after a failover.
                type: bool
                default: false
    is_instant_restore:
                description:
                    - Indicates whether this is an instant restore task.
                type: bool
                default: false
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
- name: Trigger an unplanned failover on a Recovery Plan
  nutanix.ncp.ntnx_unplanned_failover_recovery_plan_v2:
    ext_id: "6f4ffcee-1dc4-4982-9401-aa1f65dd7177"
    name: "unplanned_failover_job_ansible"
    should_ignore_warnings: false
    recovery_reference_time: "2023-01-02T03:04:05Z"
    failover_directions:
      - source_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        source_cluster:
          ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
        target_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        target_cluster:
          ext_id: "00062411-a2b3-4dd8-185b-ac1f6b6f97e2"
    post_failover_behaviour:
      should_pause_protection: false
    is_instant_restore: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for triggering the unplanned failover on a recovery plan.
        - When C(wait) is C(true) (default) it contains the full task details after
          completion, otherwise if C(wait) is C(false) it contains the initial task reference returned after the unplanned failover action.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2024-01-02T03:15:22.123456+00:00",
            "completion_details": [
                {
                    "name": "recoveryPlanJobExtId",
                    "value": "f5d3b1a2-92e7-4c9d-a1b8-abcdef123456"
                }
            ],
            "created_time": "2024-01-02T03:10:14.101010+00:00",
            "entities_affected": [
                {
                    "ext_id": "6f4ffcee-1dc4-4982-9401-aa1f65dd7177",
                    "rel": "dataprotection:config:recovery-plan"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:c3f6cc70-fda6-4133-a97c-58802d58186a",
            "is_cancelable": false,
            "last_updated_time": "2024-01-02T03:15:22.123457+00:00",
            "legacy_error_message": null,
            "operation": "UnplannedFailoverRecoveryPlan",
            "operation_description": "Unplanned Failover Recovery Plan",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2024-01-02T03:10:14.109999+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }
task_ext_id:
    description:
        - The external ID of the task tracking the unplanned failover.
    returned: always
    type: str
    sample: "ZXJnb24=:c3f6cc70-fda6-4133-a97c-58802d58186a"
ext_id:
    description:
        - The external ID of the recovery plan on which the unplanned failover
          was triggered.
    returned: always
    type: str
    sample: "6f4ffcee-1dc4-4982-9401-aa1f65dd7177"
changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true
error:
    description: Error details if the task failed.
    returned: When an error occurs
    type: str
failed:
    description: This indicates whether the task failed.
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error or an informational status
    type: str
    sample: "Api Exception raised while triggering unplanned failover on recovery plan"
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    entity_reference_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    failover_direction_spec = dict(
        source_domain_manager_ext_id=dict(type="str", required=True),
        source_cluster=dict(
            type="dict",
            options=entity_reference_spec,
            obj=data_protection_sdk.DataprotectionConfigEntityReference,
        ),
        target_domain_manager_ext_id=dict(type="str", required=True),
        target_cluster=dict(
            type="dict",
            options=entity_reference_spec,
            obj=data_protection_sdk.DataprotectionConfigEntityReference,
        ),
    )

    post_failover_behaviour_spec = dict(
        should_pause_protection=dict(type="bool", default=False),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        name=dict(type="str", required=True),
        recovery_reference_time=dict(type="str"),
        should_ignore_warnings=dict(type="bool", default=False),
        is_instant_restore=dict(type="bool", default=False),
        failover_directions=dict(
            type="list",
            elements="dict",
            options=failover_direction_spec,
            obj=data_protection_sdk.FailoverDirection,
            required=True,
        ),
        post_failover_behaviour=dict(
            type="dict",
            options=post_failover_behaviour_spec,
            obj=data_protection_sdk.PostFailoverBehaviourSpec,
        ),
    )
    return module_args


def unplanned_failover_recovery_plan(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["ext_id", "name", "failover_directions"])

    sg = SpecGenerator(module)
    default_spec = data_protection_sdk.UnplannedFailoverSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating unplanned failover recovery plan spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Unplanned failover would be triggered on recovery plan with "
            "ext_id: {0} (check mode).".format(ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.unplanned_failover_recovery_plan(
            recoveryPlanExtId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while triggering unplanned failover on recovery plan",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


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
        "failed": False,
        "response": None,
    }
    api_instance = get_recovery_plan_actions_api_instance(module)
    unplanned_failover_recovery_plan(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
