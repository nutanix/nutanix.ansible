#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_find_conflicting_uda_policy_v2
short_description: Find User-Defined Alert policies with conflicting criteria in Nutanix Prism Central
version_added: 2.7.0
description:
    - This module invokes the User-Defined Alert (UDA) policies
      C($actions/find-conflicts) action against Nutanix Prism Central.
    - Given the proposed User-Defined Alert policy body, it returns all
      existing policies that have conflicting criteria — same metric,
      operator, threshold, and overlapping entity/group filters.
    - Typical use is a pre-flight check before calling
      C(ntnx_create_uda_policy) / C(ntnx_update_uda_policy_by_id) so
      callers can detect overlaps early and avoid alert storms.
    - The action is read-only on the server. It does NOT create,
      update, or delete any policy, therefore C(changed) is always
      C(false).
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Find conflicting User-Defined Alert policies) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported since this is a read-only
              lookup action; any other value causes the module to fail.
        type: str
        choices:
            - present
        default: present
    title:
        description:
            - Title of the proposed User-Defined Alert policy that
              should be evaluated for conflicts.
            - Between 1 and 150 characters.
        type: str
        required: true
    description:
        description:
            - Human-readable description of the proposed policy.
        type: str
    is_enabled:
        description:
            - Whether the proposed policy is enabled.
            - Only affects the conflict evaluation payload.
        type: bool
    is_auto_resolved:
        description:
            - Whether the proposed policy is expected to be auto-resolved
              by the alert engine.
        type: bool
    entity_filters:
        description:
            - Explicit list of entity references the proposed policy applies to.
            - Mutually exclusive with I(group_filters).
        type: list
        elements: dict
        suboptions:
            ext_id:
                description:
                    - External ID of the entity the policy targets.
                type: str
                required: true
    group_filters:
        description:
            - Group / category references the proposed policy applies to.
            - Mutually exclusive with I(entity_filters).
        type: list
        elements: dict
        suboptions:
            ext_id:
                description:
                    - External ID of the group entity.
                type: str
                required: true
            type:
                description:
                    - Type of the group entity used for the filter.
                type: str
                choices:
                    - CATEGORY
                    - CLUSTER
                required: true
    trigger_conditions:
        description:
            - Alert trigger conditions of the proposed policy.
            - At least one entry is required by the server (min=1).
        type: list
        elements: dict
        required: true
        suboptions:
            condition_type:
                description:
                    - Type of trigger condition.
                type: str
                choices:
                    - STATIC_THRESHOLD
                required: true
            severity_level:
                description:
                    - Severity level to raise if the condition is met.
                type: str
                choices:
                    - CRITICAL
                    - WARNING
                required: true
            condition:
                description:
                    - Threshold-based condition definition.
                type: dict
                required: true
                suboptions:
                    metric_name:
                        description:
                            - Name of the metric evaluated by the condition.
                            - See the Nutanix documentation for the full list of
                              supported metric identifiers.
                        type: str
                        required: true
                    operator:
                        description:
                            - Comparison operator applied to the metric value.
                        type: str
                        choices:
                            - EQUAL_TO
                            - GREATER_THAN
                            - GREATER_THAN_OR_EQUAL_TO
                            - LESS_THAN
                            - LESS_THAN_OR_EQUAL_TO
                        required: true
                    threshold_value:
                        description:
                            - Threshold value the metric is compared against.
                            - Provide exactly one of C(int_value) or C(double_value).
                        type: dict
                        required: true
                        suboptions:
                            int_value:
                                description:
                                    - Integer threshold value.
                                type: int
                            double_value:
                                description:
                                    - Double / float threshold value.
                                type: float
    impact_types:
        description:
            - Impact categories that describe what the policy monitors.
        type: list
        elements: str
        choices:
            - AVAILABILITY
            - CAPACITY
            - CONFIGURATION
            - CPU_CAPACITY
            - MEMORY_CAPACITY
            - PERFORMANCE
            - STORAGE_CAPACITY
            - SYSTEM_INDICATOR
    is_expected_to_error_on_conflict:
        description:
            - Whether the caller expects the server to return an error on
              conflict; forwarded verbatim into the request body.
        type: bool
    policies_to_override:
        description:
            - List of existing policy external IDs the caller intends to
              override when the create/update is eventually invoked.
        type: list
        elements: str
    trigger_wait_period:
        description:
            - Trigger wait period (in seconds) before an alert fires when
              the condition holds true.
        type: int
    related_policies:
        description:
            - Related policies referenced by the proposed policy.
        type: list
        elements: dict
        suboptions:
            entity_uuid:
                description:
                    - External ID of the entity the related policy targets.
                type: str
            policy_ids:
                description:
                    - External IDs of policies related to the proposed one.
                type: list
                elements: str
    entity_type:
        description:
            - Entity type the proposed policy monitors (e.g. C(cluster),
              C(node), C(vm)).
            - Required by the server-side validator — omitting it produces
              a 400 Bad Request.
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
- name: Find conflicting User-Defined Alert policies for a proposed CPU policy
  nutanix.ncp.ntnx_find_conflicting_uda_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    title: "High CPU Usage Policy - Conflict Check"
    description: "Alert when VM CPU usage crosses 90% for 5 minutes"
    entity_type: "vm"
    is_enabled: true
    is_auto_resolved: true
    impact_types:
      - PERFORMANCE
      - CPU_CAPACITY
    is_expected_to_error_on_conflict: false
    trigger_wait_period: 300
    group_filters:
      - ext_id: "eb8b62cc-1111-2222-3333-1234567890ab"
        type: CATEGORY
    trigger_conditions:
      - condition_type: STATIC_THRESHOLD
        severity_level: CRITICAL
        condition:
          metric_name: "hypervisor_cpu_usage_ppm"
          operator: GREATER_THAN_OR_EQUAL_TO
          threshold_value:
            int_value: 900000
  register: result
  ignore_errors: true

- name: Find conflicting UDA policies using explicit entity filters
  nutanix.ncp.ntnx_find_conflicting_uda_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    title: "Memory Usage Policy - Conflict Check"
    entity_type: "vm"
    entity_filters:
      - ext_id: "8300384a-1111-2222-3333-3d1c42908bee"
    trigger_conditions:
      - condition_type: STATIC_THRESHOLD
        severity_level: WARNING
        condition:
          metric_name: "memory_usage_ppm"
          operator: GREATER_THAN
          threshold_value:
            double_value: 850000.0
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response of the find-conflicts action.
        - When conflicts are found this is a list of conflicting policies,
          each entry contains at minimum the C(ext_id) of an existing
          User-Defined Alert policy that conflicts with the input.
        - When no conflicts are found the list is empty.
    returned: always
    type: list
    elements: dict
    sample:
        - ext_id: "eb8b62cc-3f7a-4b6d-8b7a-1234567890ab"
        - ext_id: "aabb1122-3f7a-4b6d-8b7a-abcdef123456"

changed:
    description: Always C(false) — this action does not mutate any policy.
    returned: always
    type: bool
    sample: false

failed:
    description: Whether the module failed while contacting the API.
    returned: always
    type: bool
    sample: false

error:
    description: Error details, populated when the module failed.
    returned: when an error occurs
    type: str
    sample: "Api Exception raised while finding conflicting User-Defined Alert policies"

msg:
    description: Human-readable status message.
    returned: When there is an error, in check mode, or when the response is empty
    type: str
    sample: "No conflicting User-Defined Alert policies were found for the given input"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_user_defined_policies_api_instance,
)
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


def get_module_spec():
    entity_filter_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    group_filter_spec = dict(
        ext_id=dict(type="str", required=True),
        type=dict(
            type="str",
            choices=["CATEGORY", "CLUSTER"],
            required=True,
        ),
    )

    threshold_value_spec = dict(
        int_value=dict(type="int"),
        double_value=dict(type="float"),
    )

    condition_spec = dict(
        metric_name=dict(type="str", required=True),
        operator=dict(
            type="str",
            choices=[
                "EQUAL_TO",
                "GREATER_THAN",
                "GREATER_THAN_OR_EQUAL_TO",
                "LESS_THAN",
                "LESS_THAN_OR_EQUAL_TO",
            ],
            required=True,
        ),
        threshold_value=dict(
            type="dict",
            required=True,
            options=threshold_value_spec,
            mutually_exclusive=[("int_value", "double_value")],
            required_one_of=[("int_value", "double_value")],
        ),
    )

    trigger_condition_spec = dict(
        condition_type=dict(
            type="str",
            choices=["STATIC_THRESHOLD"],
            required=True,
        ),
        severity_level=dict(
            type="str",
            choices=["CRITICAL", "WARNING"],
            required=True,
        ),
        condition=dict(
            type="dict",
            required=True,
            options=condition_spec,
        ),
    )

    related_policy_spec = dict(
        entity_uuid=dict(type="str"),
        policy_ids=dict(type="list", elements="str"),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        title=dict(type="str", required=True),
        description=dict(type="str"),
        is_enabled=dict(type="bool"),
        is_auto_resolved=dict(type="bool"),
        entity_filters=dict(
            type="list",
            elements="dict",
            options=entity_filter_spec,
        ),
        group_filters=dict(
            type="list",
            elements="dict",
            options=group_filter_spec,
        ),
        trigger_conditions=dict(
            type="list",
            elements="dict",
            required=True,
            options=trigger_condition_spec,
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
        ),
        is_expected_to_error_on_conflict=dict(type="bool"),
        policies_to_override=dict(type="list", elements="str"),
        trigger_wait_period=dict(type="int"),
        related_policies=dict(
            type="list",
            elements="dict",
            options=related_policy_spec,
        ),
        entity_type=dict(type="str", required=True),
    )
    return module_args


def _build_threshold_value(threshold_value):
    """
    Build the SDK ``OneOfmonitoring.v4.common.Conditionthreshold_value``
    payload from an Ansible ``threshold_value`` dict.

    Args:
        threshold_value (dict): The ``threshold_value`` sub-block from
            ``module.params``; exactly one of ``int_value`` /
            ``double_value`` is expected.

    Returns:
        object | None: A concrete SDK value wrapper (IntValue /
        DoubleValue) or ``None`` when the user did not supply the block.
    """
    if not threshold_value:
        return None
    if threshold_value.get("int_value") is not None:
        return monitoring_sdk.IntValue(int_value=threshold_value["int_value"])
    if threshold_value.get("double_value") is not None:
        return monitoring_sdk.DoubleValue(double_value=threshold_value["double_value"])
    return None


def _build_condition(condition):
    """
    Build a ``monitoring.v4.serviceability.Condition`` SDK object from
    the Ansible ``condition`` sub-block.

    Args:
        condition (dict): The ``condition`` sub-dict — must contain
            ``metric_name``, ``operator`` and ``threshold_value``.

    Returns:
        monitoring_sdk.Condition: The populated SDK model.
    """
    return monitoring_sdk.Condition(
        metric_name=condition["metric_name"],
        operator=condition["operator"],
        threshold_value=_build_threshold_value(condition.get("threshold_value")),
    )


def _build_trigger_conditions(trigger_conditions):
    """
    Convert the list of Ansible ``trigger_conditions`` dicts into a list
    of SDK ``TriggerCondition`` objects for the request body.

    Args:
        trigger_conditions (list[dict] | None): The user-supplied list.

    Returns:
        list[monitoring_sdk.TriggerCondition] | None: SDK-ready trigger
        conditions, or ``None`` when the caller supplied nothing.
    """
    if not trigger_conditions:
        return None
    result = []
    for item in trigger_conditions:
        result.append(
            monitoring_sdk.TriggerCondition(
                condition_type=item["condition_type"],
                severity_level=item["severity_level"],
                condition=_build_condition(item["condition"]),
            )
        )
    return result


def _build_related_policies(related_policies):
    """
    Convert the Ansible ``related_policies`` param to a list of SDK
    ``RelatedPolicy`` objects.
    """
    if not related_policies:
        return None
    result = []
    for item in related_policies:
        result.append(
            monitoring_sdk.RelatedPolicy(
                entity_uuid=item.get("entity_uuid"),
                policy_ids=item.get("policy_ids"),
            )
        )
    return result


def _build_filters(module_params):
    """
    Build the ``filters`` OneOf payload for ``UserDefinedPolicy``.

    Callers may supply exactly one of ``entity_filters`` (list of
    ``EntityFilter``) or ``group_filters`` (list of ``GroupFilter``);
    passing both is rejected upstream by ``mutually_exclusive``.

    Args:
        module_params (dict): ``module.params`` — inspected for
            ``entity_filters`` / ``group_filters``.

    Returns:
        list | None: SDK filter list or ``None`` when neither is set.
    """
    entity_filters = module_params.get("entity_filters")
    group_filters = module_params.get("group_filters")
    if entity_filters:
        return [monitoring_sdk.EntityFilter(ext_id=f["ext_id"]) for f in entity_filters]
    if group_filters:
        return [
            monitoring_sdk.GroupFilter(ext_id=f["ext_id"], type=f["type"])
            for f in group_filters
        ]
    return None


def _build_uda_policy_spec(module):
    """
    Build a ``UserDefinedPolicy`` SDK model from module params.

    The model is used as the request body for
    ``find_conflicting_uda_policies``.
    """
    params = module.params
    spec = monitoring_sdk.UserDefinedPolicy(
        title=params.get("title"),
        description=params.get("description"),
        is_enabled=params.get("is_enabled"),
        is_auto_resolved=params.get("is_auto_resolved"),
        filters=_build_filters(params),
        trigger_conditions=_build_trigger_conditions(params.get("trigger_conditions")),
        impact_types=params.get("impact_types"),
        is_expected_to_error_on_conflict=params.get("is_expected_to_error_on_conflict"),
        policies_to_override=params.get("policies_to_override"),
        trigger_wait_period=params.get("trigger_wait_period"),
        related_policies=_build_related_policies(params.get("related_policies")),
        entity_type=params.get("entity_type"),
    )
    return spec


def _extract_response_data(resp):
    """
    Normalize the SDK ``FindConflictingUdaPoliciesApiResponse`` payload
    into a plain Python list.

    The v4 SDK models ``data`` as a ``OneOf`` — it can be a list of
    ``ConflictingPolicy``, an ``ErrorResponse``, or ``None`` when there
    are no conflicts. We always return a list (empty when nothing to
    report) so that Ansible tasks can safely iterate the result.

    Args:
        resp: The SDK response object.

    Returns:
        list[dict]: List of stripped conflict dicts (may be empty).
    """
    data = getattr(resp, "data", None)
    if not data:
        return []
    if isinstance(data, list):
        cleaned = []
        for item in data:
            if hasattr(item, "to_dict"):
                cleaned.append(strip_internal_attributes(item.to_dict()))
            elif isinstance(item, dict):
                cleaned.append(strip_internal_attributes(item))
            else:
                cleaned.append(item)
        return cleaned
    if hasattr(data, "to_dict"):
        return strip_internal_attributes(data.to_dict())
    return data


def find_conflicting_uda_policies(module, api_instance, result):
    """
    Perform the ``$actions/find-conflicts`` call against Prism Central
    and populate ``result`` with the outcome.

    - Validates that all server-required params are present.
    - Builds the ``UserDefinedPolicy`` request body from module params.
    - In check-mode, returns the intended request body without calling
      the API.
    - On success, populates ``result['response']`` with the list of
      conflicting policies and sets ``result['msg']`` when the list is
      empty. ``result['changed']`` is left at C(False) because this
      action is read-only.
    """
    validate_required_params(module, ["title", "entity_type", "trigger_conditions"])

    spec = _build_uda_policy_spec(module)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Check mode: skipping actual find-conflicts API call for "
            "User-Defined Alert policy '{0}'.".format(module.params.get("title"))
        )
        return

    resp = None
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

    conflicts = _extract_response_data(resp)
    result["response"] = conflicts
    if not conflicts:
        result["msg"] = (
            "No conflicting User-Defined Alert policies were found for the "
            "given input."
        )
    else:
        result["msg"] = (
            "Found {0} conflicting User-Defined Alert "
            "policies for the given input.".format(len(conflicts))
        )


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ("entity_filters", "group_filters"),
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
        "failed": False,
    }
    api_instance = get_user_defined_policies_api_instance(module)
    find_conflicting_uda_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
