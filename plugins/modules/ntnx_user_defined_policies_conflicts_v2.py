#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_defined_policies_conflicts_v2
short_description: Find conflicting User-Defined Alert policies
version_added: "2.7.0"
description:
    - Find existing policies with conflicting criteria for a User-Defined Alert Policy.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(View User Defined Alert Policy) -
      Required Roles: Files Admin, Files Viewer, Monitoring Admin, Monitoring Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  state:
    description:
        - State of the module.
        - If C(state) is C(present), the module will find conflicting
          User-Defined Alert policies.
        - If C(state) is C(absent), the module will fail.
    type: str
    choices:
        - present
    default: present
  title:
    description:
        - Title of the policy.
    type: str
    required: true
  description:
    description:
        - Description of the policy.
    type: str
  is_enabled:
    description:
        - Enable/Disable flag for the policy.
    type: bool
  is_auto_resolved:
    description:
        - Indicates whether the auto-resolve feature is enabled for this policy.
    type: bool
  filters:
    description:
        - Filter criteria for narrowing down the entities on which
          User-Defined Alert policies can be set up.
        - Provide exactly one of C(entity_filter) or C(group_filter).
    type: dict
    suboptions:
      entity_filter:
        description:
          - Entity UUID on which the User-Defined Alert policy should be set up.
        type: list
        elements: dict
        suboptions:
          ext_id:
            description:
              - Entity UUID on which the User-Defined Alert policy should be set up.
            type: str
            required: true
      group_filter:
        description:
          - Group of entities on which the User-Defined Alert policy should be set up.
        type: list
        elements: dict
        suboptions:
          ext_id:
            description:
              - Entity UUID of the group entity type on which the User-Defined
                Alert policy should be set up.
            type: str
            required: true
          type:
            description:
              - The allowed entity types that can be used to filter the set of
                entities on which User-Defined Alert policy is set.
            type: str
            required: true
            choices:
              - CATEGORY
              - CLUSTER
  trigger_conditions:
    description:
        - Trigger conditions for the policy. If there are multiple trigger
          conditions, all of them will be considered during the operation.
    type: list
    elements: dict
    required: true
    suboptions:
      condition_type:
        description:
          - "Type of condition. Example type: StaticThreshold."
        type: str
        required: true
        choices:
          - STATIC_THRESHOLD
      severity_level:
        description:
          - "Threshold level to be associated with the alert. Example levels:
            INFO, WARNING, CRITICAL."
        type: str
        required: true
        choices:
          - WARNING
          - CRITICAL
      condition:
        description:
          - Conditions to be met to trigger the alert. Conditions are expressed
            in FIQL.
        type: dict
        required: true
        suboptions:
          metric_name:
            description:
              - The metric key. Allowed values of the metrics list can be found
                at
                https://portal.nutanix.com/page/documents/details?targetId=Prism-Central-Guide-vpc_2022_9:mul-alerts-user-created-metrics-r.html.
            type: str
            required: true
          operator:
            description:
              - The comparison operator used for the condition evaluation.
            type: str
            required: true
            choices:
              - EQUAL_TO
              - GREATER_THAN
              - GREATER_THAN_OR_EQUAL_TO
              - LESS_THAN
              - LESS_THAN_OR_EQUAL_TO
          threshold_value:
            description:
              - The threshold value that was used for the condition evaluation.
            type: dict
            required: true
            suboptions:
              double_value:
                description:
                  - Denotes a value of type double.
                type: dict
                suboptions:
                  double_value:
                    description:
                      - Denotes a value of type double.
                    type: float
                    required: true
              int_value:
                description:
                  - Denotes a value of type integer.
                type: dict
                suboptions:
                  int_value:
                    description:
                      - Denotes a value of type integer.
                    type: int
                    required: true
  impact_types:
    description:
        - Impact types for the associated resulting alert.
    type: list
    elements: str
    choices:
      - AVAILABILITY
      - CAPACITY
      - CONFIGURATION
      - PERFORMANCE
      - SYSTEM_INDICATOR
      - CPU_CAPACITY
      - MEMORY_CAPACITY
      - STORAGE_CAPACITY
  is_expected_to_error_on_conflict:
    description:
        - Error when conflicting alert policies are found.
    type: bool
  policies_to_override:
    description:
        - List of IDs of the alert policies that should be overridden.
    type: list
    elements: str
  trigger_wait_period:
    description:
        - Waiting duration in seconds before triggering the alert, when the
          specified condition is met. It is set to 600s by default.
    type: int
  related_policies:
    description:
        - List of alert policies that are related to the entities of the
          current policy.
    type: list
    elements: dict
    suboptions:
      entity_uuid:
        description:
          - UUID of the entity the User-Defined Alert policy is associated
            with.
        type: str
        required: true
      policy_ids:
        description:
          - Policy IDs associated with the specified entity.
        type: list
        elements: str
        required: true
  entity_type:
    description:
        - Entity type associated with the User-Defined Alert policy. Allowed
          values are VM, node and cluster.
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
- name: Find conflicting User-Defined Alert policies
  nutanix.ncp.ntnx_user_defined_policies_conflicts_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    title: "VM CPU Usage"
    description: "CPU resources utilization by a VM"
    entity_type: "vm"
    is_enabled: true
    trigger_conditions:
      - condition_type: STATIC_THRESHOLD
        severity_level: CRITICAL
        condition:
          metric_name: hypervisor_cpu_usage_ppm
          operator: GREATER_THAN
          threshold_value:
            double_value:
              double_value: 900000.0
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for fetching conflicting User-Defined Alert policies.
  returned: always
  type: list
  sample:
    [
      {
        "ext_id": "c4eff3f4-5ad5-4f72-88d1-11e75c7d2ad9"
      }
    ]
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false
error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str
failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error or in check mode operation
  type: str
  sample: "Conflicting User-Defined Alert policies will be fetched."
total_available_results:
  description: The total number of available User-Defined Alert policies in PC.
  type: int
  returned: when all User-Defined Alert policies are fetched
  sample: 5
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_user_defined_policies_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_monitoring_py_client as sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    entity_filter_spec = dict(
        ext_id=dict(type="str", required=True),
    )
    group_filter_spec = dict(
        ext_id=dict(type="str", required=True),
        type=dict(type="str", required=True, choices=["CATEGORY", "CLUSTER"]),
    )
    double_value_spec = dict(
        double_value=dict(type="float", required=True),
    )
    int_value_spec = dict(
        int_value=dict(type="int", required=True),
    )
    threshold_value_spec = dict(
        double_value=dict(type="dict", options=double_value_spec),
        int_value=dict(type="dict", options=int_value_spec),
    )
    condition_spec = dict(
        metric_name=dict(type="str", required=True),
        operator=dict(
            type="str",
            required=True,
            choices=[
                "EQUAL_TO",
                "GREATER_THAN",
                "GREATER_THAN_OR_EQUAL_TO",
                "LESS_THAN",
                "LESS_THAN_OR_EQUAL_TO",
            ],
        ),
        threshold_value=dict(
            type="dict",
            required=True,
            options=threshold_value_spec,
            obj={
                "double_value": sdk.DoubleValue,
                "int_value": sdk.IntValue,
            },
            mutually_exclusive=[("double_value", "int_value")],
        ),
    )
    trigger_condition_spec = dict(
        condition_type=dict(type="str", required=True, choices=["STATIC_THRESHOLD"]),
        severity_level=dict(type="str", required=True, choices=["WARNING", "CRITICAL"]),
        condition=dict(
            type="dict",
            required=True,
            options=condition_spec,
            obj=sdk.Condition,
        ),
    )
    module_args = dict(
        state=dict(type="str", choices=["present"], default="present"),
        title=dict(type="str", required=True),
        description=dict(type="str"),
        is_enabled=dict(type="bool"),
        is_auto_resolved=dict(type="bool"),
        filters=dict(
            type="dict",
            options=dict(
                entity_filter=dict(
                    type="list",
                    elements="dict",
                    options=entity_filter_spec,
                    obj=sdk.EntityFilter,
                ),
                group_filter=dict(
                    type="list",
                    elements="dict",
                    options=group_filter_spec,
                    obj=sdk.GroupFilter,
                ),
            ),
            mutually_exclusive=[("entity_filter", "group_filter")],
        ),
        trigger_conditions=dict(
            type="list",
            elements="dict",
            options=trigger_condition_spec,
            obj=sdk.TriggerCondition,
            required=True,
        ),
        impact_types=dict(
            type="list",
            elements="str",
            choices=[
                "AVAILABILITY",
                "CAPACITY",
                "CONFIGURATION",
                "PERFORMANCE",
                "SYSTEM_INDICATOR",
                "CPU_CAPACITY",
                "MEMORY_CAPACITY",
                "STORAGE_CAPACITY",
            ],
        ),
        is_expected_to_error_on_conflict=dict(type="bool"),
        policies_to_override=dict(type="list", elements="str"),
        trigger_wait_period=dict(type="int"),
        related_policies=dict(
            type="list",
            elements="dict",
            options=dict(
                entity_uuid=dict(type="str", required=True),
                policy_ids=dict(type="list", elements="str", required=True),
            ),
            obj=sdk.RelatedPolicy,
        ),
        entity_type=dict(type="str", required=True),
    )
    return module_args


def find_conflicting_uda_policies(module, api_instance, result):
    validate_required_params(module, ["title", "trigger_conditions", "entity_type"])

    sg = SpecGenerator(module)
    default_spec = sdk.UserDefinedPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating find conflicting User-Defined Alert policy spec",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Conflicting User-Defined Alert policies will be fetched."
        return

    try:
        resp = api_instance.find_conflicting_uda_policies(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while finding conflicting "
                "User-Defined Alert policies"
            ),
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_monitoring_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    api_instance = get_user_defined_policies_api_instance(module)
    find_conflicting_uda_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
