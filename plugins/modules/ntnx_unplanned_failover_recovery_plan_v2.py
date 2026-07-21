#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_unplanned_failover_recovery_plan_v2
short_description: Trigger an unplanned failover on a Nutanix Recovery Plan
version_added: 2.5.0
description:
    - Perform an unplanned failover on an existing Recovery Plan in Nutanix Prism Central.
    - Restores the protected entities (VMs/Volume Groups) from their latest available
      recovery points on the target disaster recovery location.
    - This is an asynchronous action; the API returns a task reference that is polled
      to completion when C(wait) is true (the default).
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Unplanned Failover Recovery Plan) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is set to C(present) the module will trigger the unplanned
              failover on the recovery plan referenced by C(ext_id).
            - Only C(present) is supported for this action module.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the recovery plan on which the unplanned
              failover should be performed.
        type: str
        required: true
    name:
        description:
            - Human-readable name for the recovery plan job that will be created for
              this unplanned failover.
            - Required by the API when triggering the unplanned failover.
        type: str
        required: false
    recovery_reference_time:
        description:
            - Point in time from which to restore the entities during the
              C(UNPLANNED_FAILOVER) operation.
            - Only ISO-8601 formatted timestamps are supported (for example,
              C(2024-01-02T03:04:05Z)).
            - When specified, VMs and volume groups are restored from the latest
              recovery points created on or before the given timestamp. If not
              specified, the latest recovery points before the start of the recovery
              plan job are used.
        type: str
        required: false
    should_ignore_warnings:
        description:
            - If set to C(true), non-critical validation warnings raised while
              triggering the unplanned failover are ignored and the action proceeds.
        type: bool
        required: false
    is_instant_restore:
        description:
            - When set to C(true), an instant restore is attempted for the recovery
              points instead of a full restore.
        type: bool
        required: false
    failover_directions:
        description:
            - Failover direction(s) mapping source disaster recovery locations to
              target disaster recovery locations for the unplanned failover.
            - Required by the API when triggering the unplanned failover.
        type: list
        elements: dict
        required: false
        suboptions:
            source_domain_manager_ext_id:
                description:
                    - External identifier of the source domain manager (Prism Central).
                type: str
                required: false
            source_cluster:
                description:
                    - Reference to the source cluster participating in the failover.
                type: dict
                required: false
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the source cluster.
                        type: str
                        required: false
            target_domain_manager_ext_id:
                description:
                    - External identifier of the target domain manager (Prism Central).
                type: str
                required: false
            target_cluster:
                description:
                    - Reference to the target cluster participating in the failover.
                type: dict
                required: false
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the target cluster.
                        type: str
                        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - George Ghawali (@george-ghawali)
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Trigger an unplanned failover with only the required fields
  nutanix.ncp.ntnx_unplanned_failover_recovery_plan_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6f4ffcee-1dc4-4982-9401-aa1f65dd7177"
    name: "rpj_unplanned_failover_ansible"
    failover_directions:
      - source_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        source_cluster:
          ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
        target_domain_manager_ext_id: "97da301d-0a8b-4334-94cd-16a83563218e"
        target_cluster:
          ext_id: "00062899-58d4-9d37-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true

- name: Trigger an unplanned failover with all supported attributes
  nutanix.ncp.ntnx_unplanned_failover_recovery_plan_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6f4ffcee-1dc4-4982-9401-aa1f65dd7177"
    name: "rpj_unplanned_failover_ansible"
    recovery_reference_time: "2024-01-02T03:04:05Z"
    should_ignore_warnings: true
    is_instant_restore: false
    failover_directions:
      - source_domain_manager_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
        source_cluster:
          ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
        target_domain_manager_ext_id: "97da301d-0a8b-4334-94cd-16a83563218e"
        target_cluster:
          ext_id: "00062899-58d4-9d37-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for triggering the unplanned failover on a recovery plan.
        - When C(wait) is C(true) (default) it contains the full task details after
          completion, otherwise it contains the initial task reference returned by
          the create action.
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
skipped:
    description: This indicates whether the task was skipped (for example in check mode).
    returned: when applicable
    type: bool
    sample: false
error:
    description: Error details if the task failed.
    returned: When an error occurs
    type: str
    sample: null
failed:
    description: This indicates whether the task failed.
    returned: always
    type: bool
    sample: false
msg:
    description: Human-readable status message, populated on errors or informational paths.
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
        ext_id=dict(type="str"),
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

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        name=dict(type="str"),
        recovery_reference_time=dict(type="str"),
        should_ignore_warnings=dict(type="bool"),
        is_instant_restore=dict(type="bool"),
        failover_directions=dict(
            type="list",
            elements="dict",
            options=failover_direction_spec,
            obj=data_protection_sdk.FailoverDirection,
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
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_recovery_plan_actions_api_instance(module)
    unplanned_failover_recovery_plan(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
