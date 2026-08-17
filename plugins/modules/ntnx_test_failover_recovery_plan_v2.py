#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_test_failover_recovery_plan_v2
short_description: Perform Test Failover on a Nutanix Recovery Plan
version_added: 2.7.0
description:
    - Performs a Test Failover action on an existing Recovery Plan in Nutanix Prism Central.
    - The test failover action creates a Recovery Plan Job that recovers the protected
      entities (VMs / Volume Groups) in a test environment on the target site without
      impacting the production entities on the primary site.
    - This module MUST be executed against the target/recovery Prism Central endpoint
      where the entities will be recovered.
    - Use C(clean-up-resources) on the same Recovery Plan afterwards to delete the
      resources spun up by the test failover.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Test Failover a Recovery Plan) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
    state:
        description:
            - State of the module.
            - This is an action module; only C(present) is supported.
            - When C(state) is C(present) the Test Failover action is triggered on
              the referenced Recovery Plan.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the Recovery Plan on which to perform the
              Test Failover action.
        type: str
        required: true
    name:
        description:
            - Name to assign to the generated Recovery Plan Job.
            - When omitted the system auto-generates a name in the form
              C(TestFailover-<random>-<timestamp>).
        type: str
        required: false
    should_ignore_warnings:
        description:
            - When set to C(true) the recovery plan action proceeds even if there
              are non-fatal validation warnings (for example the IP address of
              some VMs cannot be preserved after recovery).
            - When C(false) (the default) validation warnings abort the failover
              and the user is expected to fix them first.
        type: bool
        required: false
        default: false
    is_instant_restore:
        description:
            - Indicates whether the Instant Restore capability should be used for
              this test failover so that VMs come up faster on the target site.
        type: bool
        required: false
        default: false
    failover_directions:
        description:
            - List of failover directions describing which source site/cluster
              should be recovered on which target site/cluster.
            - Every direction represents one source-to-target pair.
        type: list
        elements: dict
        required: false
        suboptions:
            source_domain_manager_ext_id:
                description:
                    - External identifier of the source Prism Central (domain manager)
                      from which the entities are being failed over.
                type: str
                required: false
            source_cluster:
                description:
                    - Reference to the source Prism Element cluster.
                    - Omit when the source and target domain managers differ.
                type: dict
                required: false
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the source Prism Element cluster.
                        type: str
                        required: false
            target_domain_manager_ext_id:
                description:
                    - External identifier of the target Prism Central (domain manager)
                      to which the entities are being failed over.
                    - This should match the PC on which this action is executed.
                type: str
                required: false
            target_cluster:
                description:
                    - Reference to the target Prism Element cluster.
                    - Omit when the source and target domain managers differ.
                type: dict
                required: false
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the target Prism Element cluster.
                        type: str
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
- name: Perform Test Failover on a Recovery Plan (different domain managers)
  nutanix.ncp.ntnx_test_failover_recovery_plan_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005c0ef-b0f4-40b6-a5a1-2a5a2a5a2a5a"
    name: "ansible-test-failover-job"
    should_ignore_warnings: true
    is_instant_restore: false
    failover_directions:
      - source_domain_manager_ext_id: "d4d3f6d5-1111-2222-3333-4444d3f6d5c3"
        target_domain_manager_ext_id: "d4d3f6d5-5555-6666-7777-8888d3f6d5c3"
  register: result

- name: Perform Test Failover with explicit source and target clusters
  nutanix.ncp.ntnx_test_failover_recovery_plan_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005c0ef-b0f4-40b6-a5a1-2a5a2a5a2a5a"
    name: "ansible-test-failover-same-pc"
    should_ignore_warnings: false
    is_instant_restore: true
    failover_directions:
      - source_domain_manager_ext_id: "d4d3f6d5-1111-2222-3333-4444d3f6d5c3"
        source_cluster:
          ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
        target_domain_manager_ext_id: "d4d3f6d5-1111-2222-3333-4444d3f6d5c3"
        target_cluster:
          ext_id: "000647b8-ddb3-6bbb-0000-000000028f58"
  register: result
"""
RETURN = r"""
response:
    description:
        - Response for the Test Failover action on the Recovery Plan.
        - Task details if C(wait) is true.
        - Task reference if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-21T06:30:12.123456+00:00",
            "completion_details": [
                {
                    "name": "recoveryPlanJobExtId",
                    "value": "89e6d19f-9b1e-4b5f-9f1e-3b0f0f3b0f0f"
                }
            ],
            "created_time": "2026-07-21T06:29:47.283752+00:00",
            "entities_affected": [
                {
                    "ext_id": "0005c0ef-b0f4-40b6-a5a1-2a5a2a5a2a5a",
                    "rel": "dataprotection:config:recovery-plan"
                },
                {
                    "ext_id": "89e6d19f-9b1e-4b5f-9f1e-3b0f0f3b0f0f",
                    "rel": "dataprotection:config:recovery-plan-job"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T06:30:12.123456+00:00",
            "legacy_error_message": null,
            "operation": "TestFailoverRecoveryPlan",
            "operation_description": "Test Failover Recovery Plan",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T06:29:47.300538+00:00",
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
    sample: "Api Exception raised while performing Test Failover on Recovery Plan"
error:
    description: This field typically holds information about errors that occurred during task execution.
    returned: when an error occurs
    type: str
    sample: null
failed:
    description: This field indicates whether the task failed.
    returned: always
    type: bool
    sample: false
task_ext_id:
    description: The external ID of the task tracking the asynchronous Test Failover operation.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"
ext_id:
    description: The external ID of the Recovery Plan on which the Test Failover was performed.
    returned: always
    type: str
    sample: "0005c0ef-b0f4-40b6-a5a1-2a5a2a5a2a5a"
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    entity_reference_spec = dict(
        ext_id=dict(type="str", required=False),
    )

    failover_direction_spec = dict(
        source_domain_manager_ext_id=dict(type="str", required=False),
        source_cluster=dict(
            type="dict",
            options=entity_reference_spec,
            required=False,
            obj=data_protection_sdk.DataprotectionConfigEntityReference,
        ),
        target_domain_manager_ext_id=dict(type="str", required=False),
        target_cluster=dict(
            type="dict",
            options=entity_reference_spec,
            required=False,
            obj=data_protection_sdk.DataprotectionConfigEntityReference,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        name=dict(type="str", required=False),
        should_ignore_warnings=dict(type="bool", required=False, default=False),
        is_instant_restore=dict(type="bool", required=False, default=False),
        failover_directions=dict(
            type="list",
            elements="dict",
            options=failover_direction_spec,
            required=False,
            obj=data_protection_sdk.FailoverDirection,
        ),
    )
    return module_args


def test_failover_recovery_plan(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = data_protection_sdk.TestFailoverSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Test Failover Recovery Plan spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.test_failover_recovery_plan(
            recoveryPlanExtId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing Test Failover on Recovery Plan",
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
    test_failover_recovery_plan(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
