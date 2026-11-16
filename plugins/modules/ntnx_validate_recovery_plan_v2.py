#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_validate_recovery_plan_v2
short_description: Validate a Nutanix Recovery Plan
version_added: 2.7.0
description:
    - Performs the validation of the Recovery Plan identified by its external ID.
    - The validation includes checks for the presence of entities, networks, categories, etc. referenced in the recovery plan.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Validate Recovery Plan Config) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Project Manager, Self-Service Admin (Deprecated), Super Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will validate the Recovery Plan.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the Recovery Plan on which the validate action must be executed.
        type: str
        required: true
    name:
        description:
            - Name of the Recovery Plan Job.
        type: str
        required: true
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
                    - External identifier of the source domain manager.
                type: str
                required: true
            source_cluster:
                description:
                    - External reference of the source cluster.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the entity.
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
                            - External identifier of the entity.
                        type: str
                        required: true
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
  nutanix.ncp.ntnx_validate_recovery_plan_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "6f4ffcee-1dc4-4982-9401-aa1f65dd7177"
    name: "validate_job_ansible"
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
        - Response for validating the Recovery Plan.
        - If C(wait) is C(true) (default) it contains the full task details after
          completion, otherwise if C(wait) is C(false) it contains the initial task reference returned after the validate action.
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
            "operation": "ValidateRecoveryPlan",
            "operation_description": "Validate Recovery Plan",
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
    sample: "Api Exception raised while validating recovery plan"
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    returned: when an error occurs
    type: str
failed:
    description: This indicates whether the task failed.
    returned: always
    type: bool
    sample: false
task_ext_id:
    description: The external ID of the task tracking the validate action.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"
ext_id:
    description: The external ID of the Recovery Plan on which the validate was executed.
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
    validate_required_params,
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
        ext_id=dict(type="str", required=True),
    )

    failover_directions_sub_spec = dict(
        source_domain_manager_ext_id=dict(type="str", required=True),
        source_cluster=dict(
            type="dict",
            options=entity_reference_sub_spec,
            obj=data_protection_sdk.DataprotectionConfigEntityReference,
        ),
        target_domain_manager_ext_id=dict(type="str", required=True),
        target_cluster=dict(
            type="dict",
            options=entity_reference_sub_spec,
            obj=data_protection_sdk.DataprotectionConfigEntityReference,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        name=dict(type="str", required=True),
        failover_directions=dict(
            type="list",
            elements="dict",
            options=failover_directions_sub_spec,
            obj=data_protection_sdk.FailoverDirection,
            required=True,
        ),
    )

    return module_args


def validate_recovery_plan(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["ext_id", "name", "failover_directions"])
    sg = SpecGenerator(module)
    default_spec = data_protection_sdk.BaseRecoveryPlanActionSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating validate recovery plan spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.validate_recovery_plan(recoveryPlanExtId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while validating recovery plan",
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
    validate_recovery_plan(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
