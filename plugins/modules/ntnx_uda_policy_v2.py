#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_uda_policy_v2
short_description: Create, Update, Delete User-Defined Alert (UDA) policies in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete User-Defined Alert policies in Nutanix Prism Central.
  - User-Defined Alert (UDA) policies let administrators define custom static-threshold conditions
    on individual entities (VM, node, cluster) that generate alerts when the specified conditions are met.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a User-Defined Alert policy) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Update a User-Defined Alert policy) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Delete a User-Defined Alert policy) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be
        create User-Defined Alert policy.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be
        update User-Defined Alert policy.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be
        delete User-Defined Alert policy.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the User-Defined Alert policy.
      - Required for update and delete operations.
    type: str
    required: false
  title:
    description:
      - Title of the User-Defined Alert policy.
      - Required for create operation.
      - Minimum 1, maximum 150 characters.
    type: str
    required: false
  description:
    description:
      - Description of the User-Defined Alert policy.
      - Maximum 500 characters.
    type: str
    required: false
  is_enabled:
    description:
      - Enable or disable the User-Defined Alert policy. Defaults to C(false) at the API level.
    type: bool
    required: false
  is_auto_resolved:
    description:
      - Whether the auto-resolve feature is enabled for this policy. Defaults to C(true) at the API level.
    type: bool
    required: false
  is_expected_to_error_on_conflict:
    description:
      - When C(true) the create/update operation is rejected by the API with a conflict error
        (MONITORING_SERVICE_CONFLICTING_USER_DEFINED_POLICY_ERROR / MON-21602) if conflicting
        policies already exist. Defaults to C(true) at the API level.
    type: bool
    required: false
  policies_to_override:
    description:
      - List of external IDs of existing User-Defined Alert policies that should be overridden by this policy.
    type: list
    elements: str
    required: false
  trigger_wait_period:
    description:
      - Waiting duration (in seconds) before triggering the alert once the condition is met.
      - The API default is 600 seconds when not provided.
    type: int
    required: false
  entity_type:
    description:
      - Entity type associated with the User-Defined Alert policy.
      - Allowed values are C(VM), C(node) and C(cluster).
      - Required for create operation.
      - Minimum 1, maximum 10 characters.
    type: str
    required: false
  filters:
    description:
      - Filter criteria for narrowing down the entities on which the User-Defined Alert
        policy should be evaluated.
      - Provide either C(entity_filters) or C(group_filters), never both.
    type: dict
    required: false
    suboptions:
      entity_filters:
        description:
          - List of specific entity UUIDs to which the User-Defined Alert policy applies.
        type: list
        elements: dict
        required: false
        suboptions:
          ext_id:
            description:
              - Entity UUID on which the User-Defined Alert policy should be set up.
            type: str
            required: true
      group_filters:
        description:
          - List of group references (category or cluster) that scope the User-Defined
            Alert policy to a set of entities.
        type: list
        elements: dict
        required: false
        suboptions:
          ext_id:
            description:
              - UUID of the group (category or cluster) to which the policy applies.
            type: str
            required: true
          type:
            description:
              - Group entity type.
            type: str
            required: true
            choices:
              - CATEGORY
              - CLUSTER
  trigger_conditions:
    description:
      - Trigger conditions for the policy.
      - If there are multiple trigger conditions, all of them will be considered during the operation.
      - Required for create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      condition_type:
        description:
          - Type of the trigger condition.
        type: str
        required: true
        choices:
          - STATIC_THRESHOLD
      severity_level:
        description:
          - Severity level associated with the trigger condition.
        type: str
        required: false
        choices:
          - CRITICAL
          - WARNING
      condition:
        description:
          - Conditions to be met to trigger the alert.
        type: dict
        required: false
        suboptions:
          metric_name:
            description:
              - Metric key. See the Prism Central user-created metrics reference for allowed values -
                U(https://portal.nutanix.com/page/documents/details?targetId=Prism-Central-Guide-vpc_2022_9:mul-alerts-user-created-metrics-r.html).
            type: str
            required: false
          operator:
            description:
              - Comparison operator applied to the metric value against C(threshold_value).
            type: str
            required: false
            choices:
              - EQUAL_TO
              - GREATER_THAN
              - GREATER_THAN_OR_EQUAL_TO
              - LESS_THAN
              - LESS_THAN_OR_EQUAL_TO
          threshold_value:
            description:
              - Threshold value against which the metric is compared.
              - Exactly one of C(int_value) or C(double_value) must be provided.
            type: dict
            required: false
            suboptions:
              int_value:
                description:
                  - Integer threshold value.
                type: int
                required: false
              double_value:
                description:
                  - Double / floating-point threshold value.
                type: float
                required: false
  impact_types:
    description:
      - Impact types associated with the resulting alert(s).
    type: list
    elements: str
    required: false
    choices:
      - AVAILABILITY
      - CAPACITY
      - CONFIGURATION
      - CPU_CAPACITY
      - MEMORY_CAPACITY
      - PERFORMANCE
      - STORAGE_CAPACITY
      - SYSTEM_INDICATOR
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
- name: Create User-Defined Alert policy for VM CPU usage
  nutanix.ncp.ntnx_uda_policy_v2:
    state: present
    title: "vm_high_cpu_uda_policy"
    description: "Trigger critical alert when VM CPU usage exceeds 90%"
    is_enabled: true
    is_auto_resolved: true
    is_expected_to_error_on_conflict: false
    entity_type: "VM"
    trigger_wait_period: 600
    impact_types:
      - PERFORMANCE
      - CPU_CAPACITY
    filters:
      entity_filters:
        - ext_id: "6f0f1af4-7f9c-4b13-9c22-2b4f0f6e0a11"
    trigger_conditions:
      - condition_type: STATIC_THRESHOLD
        severity_level: CRITICAL
        condition:
          metric_name: "hypervisor_cpu_usage_ppm"
          operator: GREATER_THAN
          threshold_value:
            int_value: 900000
  register: create_result

- name: Update User-Defined Alert policy - change threshold and severity
  nutanix.ncp.ntnx_uda_policy_v2:
    state: present
    ext_id: "{{ create_result.ext_id }}"
    title: "vm_high_cpu_uda_policy"
    description: "Trigger warning alert when VM CPU usage exceeds 80%"
    is_enabled: true
    is_auto_resolved: true
    entity_type: "VM"
    trigger_wait_period: 900
    impact_types:
      - PERFORMANCE
    filters:
      entity_filters:
        - ext_id: "6f0f1af4-7f9c-4b13-9c22-2b4f0f6e0a11"
    trigger_conditions:
      - condition_type: STATIC_THRESHOLD
        severity_level: WARNING
        condition:
          metric_name: "hypervisor_cpu_usage_ppm"
          operator: GREATER_THAN
          threshold_value:
            int_value: 800000

- name: Delete User-Defined Alert policy
  nutanix.ncp.ntnx_uda_policy_v2:
    state: absent
    ext_id: "{{ create_result.ext_id }}"
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting the User-Defined Alert policy.
    - If the operation is create or update and C(wait) is true, it returns the policy details.
    - If the operation is create or update and C(wait) is false, it returns the task details.
    - If the operation is delete, it returns the task details.
  returned: always
  type: dict
  sample:
    {
      "created_by": "admin",
      "description": "Trigger critical alert when cluster CPU usage exceeds 90%",
      "entity_type": "cluster",
      "ext_id": "cca36a51-c14c-4afe-958b-1903c7ae9deb",
      "filters": [
          {"ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2", "type": "CLUSTER"}
      ],
      "impact_types": ["PERFORMANCE", "CPU_CAPACITY"],
      "is_auto_resolved": true,
      "is_enabled": true,
      "is_expected_to_error_on_conflict": null,
      "last_updated_time": "2026-07-20T15:30:27.250063+00:00",
      "links": null,
      "policies_to_override": null,
      "policyId": "Ab7a54f9e-a749-4435-8a29-2ab9fa4c24ca",
      "related_policies": null,
      "tenant_id": null,
      "title": "vm_high_cpu_uda_policy_ansible",
      "trigger_conditions": [
          {
              "condition": {
                  "metric_name": "hypervisor_cpu_usage_ppm",
                  "operator": "GREATER_THAN",
                  "threshold_value": {"int_value": 900000}
              },
              "condition_type": "STATIC_THRESHOLD",
              "severity_level": "CRITICAL"
          }
      ],
      "trigger_wait_period": 600
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the User-Defined Alert policy.
  returned: always
  type: str
  sample: "cf3d9d0d-27e4-4c66-9a52-9d19ce6d7b02"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (e.g. idempotency match).
  returned: When applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Status or error message.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "UdaPolicy with ext_id:<id> will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_etag,
    get_user_defined_policies_api_instance,
)
from ..module_utils.v4.monitoring.helpers import get_uda_policy  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_monitoring_py_client as monitoring_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as monitoring_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

READ_ONLY_FIELDS = (
    "ext_id",
    "links",
    "tenant_id",
    "created_by",
    "last_updated_time",
    "related_policies",
)


def _strip_read_only_attributes(spec):
    """Zero-out server-populated / read-only fields before submitting an update."""
    for field in READ_ONLY_FIELDS:
        if hasattr(spec, field):
            try:
                setattr(spec, field, None)
            except (ValueError, AttributeError):
                pass


def get_module_spec():

    threshold_value_spec = dict(
        int_value=dict(type="int", required=False),
        double_value=dict(type="float", required=False),
    )

    condition_spec = dict(
        metric_name=dict(type="str", required=False),
        operator=dict(
            type="str",
            required=False,
            choices=[
                "EQUAL_TO",
                "GREATER_THAN",
                "GREATER_THAN_OR_EQUAL_TO",
                "LESS_THAN",
                "LESS_THAN_OR_EQUAL_TO",
            ],
            obj=monitoring_sdk.ComparisonOperator,
        ),
        threshold_value=dict(
            type="dict",
            required=False,
            options=threshold_value_spec,
            mutually_exclusive=[("int_value", "double_value")],
        ),
    )

    trigger_condition_spec = dict(
        condition_type=dict(
            type="str",
            required=True,
            choices=["STATIC_THRESHOLD"],
            obj=monitoring_sdk.ConditionType,
        ),
        severity_level=dict(
            type="str",
            required=False,
            choices=["CRITICAL", "WARNING"],
            obj=monitoring_sdk.PolicySeverityLevel,
        ),
        condition=dict(
            type="dict",
            required=False,
            options=condition_spec,
            obj=monitoring_sdk.Condition,
        ),
    )

    entity_filter_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    group_filter_spec = dict(
        ext_id=dict(type="str", required=True),
        type=dict(
            type="str",
            required=True,
            choices=["CATEGORY", "CLUSTER"],
            obj=monitoring_sdk.GroupEntityType,
        ),
    )

    filters_spec = dict(
        entity_filters=dict(
            type="list",
            elements="dict",
            required=False,
            options=entity_filter_spec,
        ),
        group_filters=dict(
            type="list",
            elements="dict",
            required=False,
            options=group_filter_spec,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        title=dict(type="str"),
        description=dict(type="str"),
        is_enabled=dict(type="bool"),
        is_auto_resolved=dict(type="bool"),
        is_expected_to_error_on_conflict=dict(type="bool"),
        policies_to_override=dict(type="list", elements="str"),
        trigger_wait_period=dict(type="int"),
        entity_type=dict(type="str"),
        filters=dict(
            type="dict",
            options=filters_spec,
            mutually_exclusive=[("entity_filters", "group_filters")],
            required_one_of=[("entity_filters", "group_filters")],
        ),
        trigger_conditions=dict(
            type="list",
            elements="dict",
            options=trigger_condition_spec,
            obj=monitoring_sdk.TriggerCondition,
        ),
        impact_types=dict(
            type="list",
            elements="str",
            choices=[
                "AVAILABILITY",
                "CAPACITY",
                "CONFIGURATION",
                "CPU_CAPACITY",
                "MEMORY_CAPACITY",
                "PERFORMANCE",
                "STORAGE_CAPACITY",
                "SYSTEM_INDICATOR",
            ],
            obj=monitoring_sdk.ImpactType,
        ),
    )
    return module_args


def _build_threshold_value(threshold_value):
    """Convert Ansible threshold_value dict into an SDK IntValue/DoubleValue instance."""
    if not threshold_value:
        return None
    if threshold_value.get("int_value") is not None:
        return monitoring_sdk.IntValue(int_value=threshold_value["int_value"])
    if threshold_value.get("double_value") is not None:
        return monitoring_sdk.DoubleValue(double_value=threshold_value["double_value"])
    return None


def _build_filters(filters_param):
    """Convert Ansible filters dict into the SDK filters list (entity or group)."""
    if not filters_param:
        return None
    entity_filters = filters_param.get("entity_filters")
    group_filters = filters_param.get("group_filters")
    if entity_filters:
        return [
            monitoring_sdk.EntityFilter(ext_id=item.get("ext_id"))
            for item in entity_filters
            if item and item.get("ext_id") is not None
        ]
    if group_filters:
        return [
            monitoring_sdk.GroupFilter(
                ext_id=item.get("ext_id"),
                type=item.get("type"),
            )
            for item in group_filters
            if item and item.get("ext_id") is not None
        ]
    return None


def _apply_manual_fields(module, spec):
    """Populate SDK fields that the generic spec generator cannot handle
    (nested OneOf polymorphic fields: filters / threshold_value)."""
    if "filters" in module.params:
        spec.filters = _build_filters(module.params.get("filters"))

    trigger_conditions = module.params.get("trigger_conditions")
    if trigger_conditions and getattr(spec, "trigger_conditions", None):
        for idx, tc_input in enumerate(trigger_conditions):
            if idx >= len(spec.trigger_conditions):
                break
            condition_input = tc_input.get("condition") if tc_input else None
            if condition_input is None:
                continue
            if "threshold_value" in condition_input:
                sdk_threshold = _build_threshold_value(
                    condition_input.get("threshold_value")
                )
                if spec.trigger_conditions[idx].condition is None:
                    spec.trigger_conditions[idx].condition = monitoring_sdk.Condition()
                spec.trigger_conditions[idx].condition.threshold_value = sdk_threshold


def _spec_to_comparable(spec_dict):
    """Return a comparable representation of a policy spec dict for idempotency.

    Drops server-populated read-only fields as well as write-only flags that
    the API does not echo back on read (e.g. is_expected_to_error_on_conflict)
    so that a re-apply of an unchanged playbook is idempotent.
    """
    data = strip_internal_attributes(deepcopy(spec_dict))
    for key in READ_ONLY_FIELDS + ("is_expected_to_error_on_conflict", "policyId"):
        data.pop(key, None)
    # Normalize "empty list" to None so an empty list from the playbook matches
    # a server-side null on fields that are optional collections.
    for key in ("policies_to_override", "impact_types"):
        if key in data and data[key] == []:
            data[key] = None
    return data


def check_for_idempotency(old_spec_dict, update_spec_dict):
    return _spec_to_comparable(old_spec_dict) == _spec_to_comparable(update_spec_dict)


def create_uda_policy(module, api_instance, result):
    validate_required_params(module, ["title", "entity_type", "trigger_conditions"])

    sg = SpecGenerator(module)
    default_spec = monitoring_sdk.UserDefinedPolicy(
        title=module.params.get("title"),
        entity_type=module.params.get("entity_type"),
        trigger_conditions=[],
    )
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create User-Defined Alert policy spec", **result
        )

    _apply_manual_fields(module, spec)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.create_uda_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating User-Defined Alert policy",
        )

    ext_id = getattr(getattr(resp, "data", None), "ext_id", None)
    if ext_id:
        result["ext_id"] = ext_id
        entity = get_uda_policy(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(entity.data.to_dict())
    else:
        raise_api_exception(
            module=module,
            exception=Exception(
                "Failed to obtain external ID from create User-Defined Alert policy response"
            ),
            msg="Failed to obtain external ID from create User-Defined Alert policy response",
        )
    result["changed"] = True


def update_uda_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["title", "entity_type", "trigger_conditions"])

    current = get_uda_policy(module, api_instance, ext_id)
    etag = get_etag(data=current)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for updating User-Defined Alert policy",
            **result,
        )

    old_spec = current.data
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update User-Defined Alert policy spec", **result
        )

    _apply_manual_fields(module, update_spec)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(old_spec.to_dict())
        module.exit_json(
            msg="Nothing to change.",
            **result,
        )

    _strip_read_only_attributes(update_spec)

    try:
        api_instance.update_uda_policy_by_id(
            extId=ext_id, body=update_spec, if_match=etag
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating User-Defined Alert policy",
        )

    entity = get_uda_policy(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(entity.data.to_dict())
    result["changed"] = True


def delete_uda_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "UdaPolicy with ext_id:{0} will be deleted.".format(ext_id)
        return

    try:
        resp = api_instance.delete_uda_policy_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting User-Defined Alert policy",
        )

    if resp is not None and getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    else:
        result["response"] = {
            "message": "User-Defined Alert policy deleted successfully."
        }
    result["msg"] = "UdaPolicy with ext_id:{0} deleted successfully.".format(ext_id)
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("title", "ext_id"), True),
        ],
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
        "ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }
    api_instance = get_user_defined_policies_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_uda_policy(module, api_instance, result)
        else:
            create_uda_policy(module, api_instance, result)
    else:
        delete_uda_policy(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
