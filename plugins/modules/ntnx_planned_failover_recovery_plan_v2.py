#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_planned_failover_recovery_plan_v2
short_description: Perform a planned failover on a Nutanix Recovery Plan
version_added: 2.7.0
description:
    - Trigger a planned failover on a Recovery Plan identified by its external ID.
    - >-
      A planned failover gracefully migrates the entities protected by the
      Recovery Plan (VMs and Volume Groups) from the source cluster to the
      recovery cluster with zero data loss. Optionally, VMs can be
      live-migrated when synchronous replication is configured.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Planned Failover on a Recovery Plan) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will trigger a planned failover.
            - Any other value will fail (this is an action module and does not support absent).
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the Recovery Plan on which the planned
              failover action must be executed.
        type: str
        required: true
    name:
        description:
            - A user-defined name for the resulting Recovery Plan Job.
            - If omitted, the platform generates a name automatically.
        type: str
    should_ignore_warnings:
        description:
            - Continue the failover even if validation warnings are detected.
            - >-
              For example, when the IP address of some VMs cannot be preserved
              after recovery, setting this to C(true) allows the failover to
              proceed. When C(false) (default) any validation warning aborts
              the action - the user must then either resolve the warnings and
              retry, or re-issue the request with this flag set.
        type: bool
    should_live_migrate_vms:
        description:
            - Orchestrate a Cross Cluster Live Migration (CCLM) for the
              protected VMs during the failover.
            - When C(true), running VMs are migrated between clusters with no
              downtime; this requires that the entities are stretch-protected
              with synchronous replication.
            - When C(false) or omitted, the classic power-off / recover flow
              is used.
        type: bool
    failover_directions:
        description:
            - The failover topology - one entry per source/target cluster
              pair involved in the Recovery Plan.
            - Each entry describes which source cluster (managed by which
              Prism Central) the entities are failing over from, and which
              target cluster (managed by which Prism Central) they should be
              recovered on.
        type: list
        elements: dict
        suboptions:
            source_domain_manager_ext_id:
                description:
                    - External identifier of the Prism Central instance
                      managing the source cluster.
                type: str
            source_cluster:
                description:
                    - Reference to the source Prism Element cluster from
                      which the entities are failing over.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the source cluster.
                        type: str
            target_domain_manager_ext_id:
                description:
                    - External identifier of the Prism Central instance
                      managing the target (recovery) cluster.
                    - In a single-PC / local availability zone setup this
                      may be the same value as
                      C(source_domain_manager_ext_id).
                type: str
            target_cluster:
                description:
                    - Reference to the target Prism Element cluster where
                      the entities will be recovered.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the target cluster.
                        type: str
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
- name: Perform a planned failover on a Recovery Plan
  nutanix.ncp.ntnx_planned_failover_recovery_plan_v2:
    ext_id: "6f4ffcee-1dc4-4982-9401-aa1f65dd7177"
    name: "planned_failover_job_ansible"
    should_ignore_warnings: false
    should_live_migrate_vms: false
    failover_directions:
      - source_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        source_cluster:
          ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
        target_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        target_cluster:
          ext_id: "00062411-a2b3-4dd8-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true

- name: Perform a planned failover with live migration (CCLM)
  nutanix.ncp.ntnx_planned_failover_recovery_plan_v2:
    ext_id: "6f4ffcee-1dc4-4982-9401-aa1f65dd7177"
    should_live_migrate_vms: true
    should_ignore_warnings: true
    failover_directions:
      - source_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        source_cluster:
          ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
        target_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        target_cluster:
          ext_id: "00062411-a2b3-4dd8-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for the planned failover Recovery Plan action.
        - Recovery Plan Job task details when C(wait) is true.
        - Immediate task submission details when C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-21T09:45:12.421810+00:00",
            "completion_details": [
                {
                    "name": "recoveryPlanJobExtId",
                    "value": "7c8e4d5b-9a1c-4f21-9e70-bad0b3b7e001"
                }
            ],
            "created_time": "2026-07-21T09:44:36.129803+00:00",
            "entities_affected": [
                {
                    "ext_id": "6f4ffcee-1dc4-4982-9401-aa1f65dd7177",
                    "rel": "dataprotection:config:recovery-plan"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T09:45:12.421810+00:00",
            "legacy_error_message": null,
            "operation": "PlannedFailoverRecoveryPlan",
            "operation_description": "Planned Failover Recovery Plan",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T09:44:36.145110+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }
changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true
msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while triggering planned failover on recovery plan"
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Failed generating planned failover spec"
failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false
task_ext_id:
    description: The external ID of the task tracking the planned failover.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"
ext_id:
    description: The external ID of the Recovery Plan on which the planned failover was executed.
    returned: always
    type: str
    sample: "6f4ffcee-1dc4-4982-9401-aa1f65dd7177"
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
)

SDK_IMP_ERROR = None
try:
    import ntnx_dataprotection_py_client as data_protection_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_protection_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    entity_reference_sub_spec = dict(
        ext_id=dict(type="str"),
    )

    failover_directions_sub_spec = dict(
        source_domain_manager_ext_id=dict(type="str"),
        source_cluster=dict(
            type="dict",
            options=entity_reference_sub_spec,
            obj=data_protection_sdk.DataprotectionConfigEntityReference,
        ),
        target_domain_manager_ext_id=dict(type="str"),
        target_cluster=dict(
            type="dict",
            options=entity_reference_sub_spec,
            obj=data_protection_sdk.DataprotectionConfigEntityReference,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        name=dict(type="str"),
        should_ignore_warnings=dict(type="bool"),
        should_live_migrate_vms=dict(type="bool"),
        failover_directions=dict(
            type="list",
            elements="dict",
            options=failover_directions_sub_spec,
            obj=data_protection_sdk.FailoverDirection,
        ),
    )

    return module_args


def planned_failover_recovery_plan(module, result, api_instance):
    """Trigger a planned failover on a Recovery Plan.

    The module argument spec uses ``should_live_migrate_vms`` while the SDK
    struct exposes ``should_live_migrate_v_ms`` (auto-generated pluralisation
    for ``shouldLiveMigrateVMs``). Because ``SpecGenerator`` matches only
    attributes present on the SDK spec, we set that field manually after the
    initial spec generation.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = data_protection_sdk.PlannedFailoverSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating planned failover spec", **result)

    should_live_migrate_vms = module.params.get("should_live_migrate_vms")
    if should_live_migrate_vms is not None:
        spec.should_live_migrate_v_ms = should_live_migrate_vms

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.planned_failover_recovery_plan(
            recoveryPlanExtId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while triggering planned failover on recovery plan",
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
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_recovery_plan_actions_api_instance(module)
    planned_failover_recovery_plan(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
