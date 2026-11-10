#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_defined_policies_v2
short_description: Create, Update, Delete User-Defined Alert policies
version_added: "2.7.0"
description:
    - Create, Update, Delete User-Defined Alert policies.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a User-Defined Alert policy) -
      Required Roles: Monitoring Admin, Prism Admin, Project Manager, Super Admin
    - >-
      B(Update a User-Defined Alert policy) -
      Required Roles: Files Admin, Monitoring Admin, Prism Admin, Project Manager, Super Admin
    - >-
      B(Delete a User-Defined Alert policy) -
      Required Roles: Monitoring Admin, Prism Admin, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  state:
    description:
        - State of the User-Defined Alert policy.
        - If C(state) is C(present) and C(ext_id) is not provided, create a policy.
        - If C(state) is C(present) and C(ext_id) is provided, update the policy.
        - If C(state) is C(absent), delete the policy with the given external ID.
    type: str
    choices:
        - present
        - absent
  ext_id:
    description:
        - Entity UUID.
        - Required for updating or deleting a User-Defined Alert policy.
    type: str
  title:
    description:
        - Title of the policy.
    type: str
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
              int_value:
                description:
                  - Denotes a value of type integer.
                type: dict
                suboptions:
                  int_value:
                    description:
                      - Denotes a value of type integer.
                    type: int
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
- name: Create a User-Defined Alert policy
  nutanix.ncp.ntnx_user_defined_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    title: "VM CPU Usage"
    description: "CPU resources utilization by a VM"
    entity_type: "vm"
    is_enabled: true
    is_auto_resolved: true
    impact_types:
      - PERFORMANCE
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

- name: Update a User-Defined Alert policy
  nutanix.ncp.ntnx_user_defined_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "{{ result.ext_id }}"
    title: "VM CPU Usage Updated"
    description: "Updated CPU resources utilization by a VM"
    entity_type: "vm"
    is_enabled: false
    trigger_conditions:
      - condition_type: STATIC_THRESHOLD
        severity_level: WARNING
        condition:
          metric_name: hypervisor_cpu_usage_ppm
          operator: GREATER_THAN_OR_EQUAL_TO
          threshold_value:
            double_value:
              double_value: 800000.0
  register: result

- name: Delete a User-Defined Alert policy
  nutanix.ncp.ntnx_user_defined_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "{{ result.ext_id }}"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for User-Defined Alert policy operations.
    - Policy details for create and update.
    - Empty when delete succeeds with no response body.
  returned: always
  type: dict
  sample:
    {
      "created_by": "admin",
      "description": "Sample UDA for docs",
      "entity_type": "vm",
      "ext_id": "8101e53a-ccfa-4c36-81e7-c818a0f6873f",
      "is_auto_resolved": true,
      "is_enabled": true,
      "title": "ansible-sample-92174",
      "trigger_conditions": [
        {
          "condition": {
            "metric_name": "hypervisor_cpu_usage_ppm",
            "operator": "GREATER_THAN",
            "threshold_value": {"int_value": 80}
          },
          "condition_type": "STATIC_THRESHOLD",
          "severity_level": "CRITICAL"
        }
      ],
      "trigger_wait_period": 600
    }
ext_id:
  description:
    - The external ID of the User-Defined Alert policy.
  returned: always
  type: str
  sample: "701bcb62-de3c-4f24-aec9-dd9de450d3ac"
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
skipped:
  description: This indicates whether the task was skipped
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
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Nothing to change."
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
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_monitoring_py_client as sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

READ_ONLY_FIELDS = (
    "created_by",
    "last_updated_time",
    "policy_id",
    "links",
    "tenant_id",
)


def get_module_spec():
    entity_filter_spec = dict(
        ext_id=dict(type="str", required=True),
    )
    group_filter_spec = dict(
        ext_id=dict(type="str", required=True),
        type=dict(type="str", required=True, choices=["CATEGORY", "CLUSTER"]),
    )
    double_value_spec = dict(
        double_value=dict(type="float"),
    )
    int_value_spec = dict(
        int_value=dict(type="int"),
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
        ext_id=dict(type="str"),
        title=dict(type="str"),
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
        entity_type=dict(type="str"),
    )
    return module_args


def _prepare_filters_for_generator(module):
    """Expand filters oneOf wrapper into the SDK list field for SpecGenerator."""
    filters = module.params.get("filters")
    if not filters:
        return
    if filters.get("entity_filter") is not None:
        flavour = "entity_filter"
    elif filters.get("group_filter") is not None:
        flavour = "group_filter"
    else:
        module.params.pop("filters", None)
        return
    flavour_schema = module.argument_spec_with_extra_keys["filters"]["options"][flavour]
    module.params["filters"] = filters[flavour]
    module.argument_spec_with_extra_keys["filters"] = flavour_schema


def check_uda_policy_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(deepcopy(old_spec))
    update_spec = strip_internal_attributes(deepcopy(update_spec))
    for field in READ_ONLY_FIELDS:
        old_spec.pop(field, None)
        update_spec.pop(field, None)
    return old_spec == update_spec


def create_uda_policy(module, api_instance, result):
    validate_required_params(module, ["title", "trigger_conditions", "entity_type"])
    _prepare_filters_for_generator(module)

    sg = SpecGenerator(module)
    default_spec = sdk.UserDefinedPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create User-Defined Alert policy spec", **result
        )

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

    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def update_uda_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_uda_policy(module, api_instance, ext_id)

    _prepare_filters_for_generator(module)
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update User-Defined Alert policy spec", **result
        )

    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_uda_policy_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating User-Defined Alert policy", **result
        )
    kwargs = {"if_match": etag}

    try:
        api_instance.update_uda_policy_by_id(extId=ext_id, body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating User-Defined Alert policy",
        )

    resp = get_uda_policy(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_uda_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "User-Defined Alert policy with ext_id:{0} will be deleted.".format(ext_id)
        )
        return

    try:
        resp = api_instance.delete_uda_policy_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting User-Defined Alert policy",
        )

    result["changed"] = True
    if resp is not None and getattr(resp, "data", None) is not None:
        data = resp.data
        if hasattr(data, "to_dict"):
            result["response"] = strip_internal_attributes(data.to_dict())
        else:
            result["response"] = data
    else:
        result["msg"] = (
            "User-Defined Alert policy with ext_id:{0} deleted successfully.".format(
                ext_id
            )
        )


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
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
        "ext_id": None,
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
