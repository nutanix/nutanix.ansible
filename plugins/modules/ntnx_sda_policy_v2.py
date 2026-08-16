#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_sda_policy_v2
short_description: Update cluster specific configuration of a System-Defined Alert Policy in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to update the cluster-specific configuration of a System-Defined Alert
    (SDA) Policy in Nutanix Prism Central.
  - System-Defined Alert Policies are built-in policies shipped by Nutanix and cannot be created or
    deleted. Only their cluster-specific configuration can be modified.
  - Because create and delete operations are not supported for SDA policies, this module only
    performs an update when C(state=present), C(sda_policy_ext_id) and C(cluster_ext_id) are
    provided. C(state=absent) is not supported and will fail with a descriptive message.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing
      the operation. The required roles depend on the operation being performed.
    - >-
      B(Update a cluster-specific configuration of a System-Defined Alert Policy) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  state:
    description:
      - If C(state) is set to C(present) and both C(sda_policy_ext_id) and C(cluster_ext_id) are
        provided then the operation will be update cluster configuration of the SDA policy.
      - System-Defined Alert Policies do not support create/delete, so C(state=absent) is
        rejected.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - Alias of C(cluster_ext_id).
      - The external ID of the ClusterConfig which for System-Defined Alert Policies is the
        Prism Element cluster UUID on which the policy is applied.
      - Kept for parity with other v4 CRUD modules; providing C(ext_id) or C(cluster_ext_id) is
        equivalent.
    type: str
    required: false
  sda_policy_ext_id:
    description:
      - The external ID of the System-Defined Alert Policy whose per-cluster configuration is
        being updated.
      - Required for update operation.
    type: str
    required: false
  cluster_ext_id:
    description:
      - Prism Element cluster UUID on which the SDA policy configuration is applied.
      - Required for update operation.
    type: str
    required: false
  is_enabled:
    description:
      - Indicates whether the SDA policy is enabled on the target cluster.
    type: bool
    required: false
  schedule_interval_seconds:
    description:
      - Interval in seconds for periodically executing the SDA policy on the target cluster.
      - This is not applicable for policies whose sub-type is C(NOT_SCHEDULED) or
        C(EVENT_DRIVEN); those types always ignore this field on the server side.
    type: int
    required: false
  configurable_parameters:
    description:
      - Values of the SDA parameters that are configurable by a user for this cluster.
      - Each parameter is a name/value pair whose value type must match the parameter's schema
        (integer / float / boolean / string).
    type: list
    elements: dict
    required: false
    suboptions:
      name:
        description:
          - Unique identifier name of the parameter.
        type: str
        required: true
      display_name:
        description:
          - Human friendly name of the parameter.
        type: str
        required: false
      unit:
        description:
          - Unit associated with the parameter (for example C(GB), C(PERCENT), C(SECONDS)).
        type: str
        required: false
      param_value:
        description:
          - Value for the parameter. Exactly one of the sub-keys
            C(int_value), C(float_value), C(bool_value) or C(string_value) must be set
            and it must match the parameter's underlying type.
        type: dict
        required: false
        suboptions:
          int_value:
            description:
              - Integer valued parameter.
            type: dict
            required: false
            suboptions:
              default_int_value:
                description:
                  - Default value for the parameter.
                type: int
                required: false
              current_int_value:
                description:
                  - Current value for the parameter.
                type: int
                required: false
          float_value:
            description:
              - Float valued parameter.
            type: dict
            required: false
            suboptions:
              default_float_value:
                description:
                  - Default value for the parameter.
                type: float
                required: false
              current_float_value:
                description:
                  - Current value for the parameter.
                type: float
                required: false
          bool_value:
            description:
              - Boolean valued parameter.
            type: dict
            required: false
            suboptions:
              default_bool_value:
                description:
                  - Default value for the parameter.
                type: bool
                required: false
              current_bool_value:
                description:
                  - Current value for the parameter.
                type: bool
                required: false
          string_value:
            description:
              - String valued parameter.
            type: dict
            required: false
            suboptions:
              default_str_value:
                description:
                  - Default value for the parameter.
                type: str
                required: false
              current_str_value:
                description:
                  - Current value for the parameter.
                type: str
                required: false
  alert_config:
    description:
      - Alert specific properties associated with the policy on the target cluster.
    type: dict
    required: false
    suboptions:
      auto_resolve:
        description:
          - Auto-resolve state for alerts generated by this policy on the cluster.
        type: str
        required: false
        choices:
          - ENABLED
          - DISABLED
          - NOT_SUPPORTED
      critical_severity:
        description:
          - Configuration for the critical severity level of the policy.
        type: dict
        required: false
        suboptions:
          state:
            description:
              - Whether the critical severity is enabled, disabled or unsupported.
            type: str
            required: false
            choices:
              - ENABLED
              - DISABLED
              - NOT_SUPPORTED
          threshold_parameters:
            description:
              - Threshold parameters that must be met to raise a critical alert.
            type: list
            elements: dict
            required: false
            suboptions:
              name:
                description:
                  - Unique identifier name of the threshold parameter.
                type: str
                required: true
              display_name:
                description:
                  - Human friendly name of the threshold parameter.
                type: str
                required: false
              unit:
                description:
                  - Unit associated with the threshold parameter.
                type: str
                required: false
              param_value:
                description:
                  - Value for the threshold parameter. Exactly one of the sub-keys
                    C(int_value), C(float_value), C(bool_value) or C(string_value) must be set.
                type: dict
                required: false
                suboptions:
                  int_value:
                    description:
                      - Integer valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_int_value:
                        description:
                          - Default value for the threshold parameter.
                        type: int
                        required: false
                      current_int_value:
                        description:
                          - Current value for the threshold parameter.
                        type: int
                        required: false
                  float_value:
                    description:
                      - Float valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_float_value:
                        description:
                          - Default value for the threshold parameter.
                        type: float
                        required: false
                      current_float_value:
                        description:
                          - Current value for the threshold parameter.
                        type: float
                        required: false
                  bool_value:
                    description:
                      - Boolean valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_bool_value:
                        description:
                          - Default value for the threshold parameter.
                        type: bool
                        required: false
                      current_bool_value:
                        description:
                          - Current value for the threshold parameter.
                        type: bool
                        required: false
                  string_value:
                    description:
                      - String valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_str_value:
                        description:
                          - Default value for the threshold parameter.
                        type: str
                        required: false
                      current_str_value:
                        description:
                          - Current value for the threshold parameter.
                        type: str
                        required: false
      warning_severity:
        description:
          - Configuration for the warning severity level of the policy.
        type: dict
        required: false
        suboptions:
          state:
            description:
              - Whether the warning severity is enabled, disabled or unsupported.
            type: str
            required: false
            choices:
              - ENABLED
              - DISABLED
              - NOT_SUPPORTED
          threshold_parameters:
            description:
              - Threshold parameters that must be met to raise a warning alert.
            type: list
            elements: dict
            required: false
            suboptions:
              name:
                description:
                  - Unique identifier name of the threshold parameter.
                type: str
                required: true
              display_name:
                description:
                  - Human friendly name of the threshold parameter.
                type: str
                required: false
              unit:
                description:
                  - Unit associated with the threshold parameter.
                type: str
                required: false
              param_value:
                description:
                  - Value for the threshold parameter. Exactly one of the sub-keys
                    C(int_value), C(float_value), C(bool_value) or C(string_value) must be set.
                type: dict
                required: false
                suboptions:
                  int_value:
                    description:
                      - Integer valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_int_value:
                        description:
                          - Default value for the threshold parameter.
                        type: int
                        required: false
                      current_int_value:
                        description:
                          - Current value for the threshold parameter.
                        type: int
                        required: false
                  float_value:
                    description:
                      - Float valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_float_value:
                        description:
                          - Default value for the threshold parameter.
                        type: float
                        required: false
                      current_float_value:
                        description:
                          - Current value for the threshold parameter.
                        type: float
                        required: false
                  bool_value:
                    description:
                      - Boolean valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_bool_value:
                        description:
                          - Default value for the threshold parameter.
                        type: bool
                        required: false
                      current_bool_value:
                        description:
                          - Current value for the threshold parameter.
                        type: bool
                        required: false
                  string_value:
                    description:
                      - String valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_str_value:
                        description:
                          - Default value for the threshold parameter.
                        type: str
                        required: false
                      current_str_value:
                        description:
                          - Current value for the threshold parameter.
                        type: str
                        required: false
      info_severity:
        description:
          - Configuration for the info severity level of the policy.
        type: dict
        required: false
        suboptions:
          state:
            description:
              - Whether the info severity is enabled, disabled or unsupported.
            type: str
            required: false
            choices:
              - ENABLED
              - DISABLED
              - NOT_SUPPORTED
          threshold_parameters:
            description:
              - Threshold parameters that must be met to raise an info alert.
            type: list
            elements: dict
            required: false
            suboptions:
              name:
                description:
                  - Unique identifier name of the threshold parameter.
                type: str
                required: true
              display_name:
                description:
                  - Human friendly name of the threshold parameter.
                type: str
                required: false
              unit:
                description:
                  - Unit associated with the threshold parameter.
                type: str
                required: false
              param_value:
                description:
                  - Value for the threshold parameter. Exactly one of the sub-keys
                    C(int_value), C(float_value), C(bool_value) or C(string_value) must be set.
                type: dict
                required: false
                suboptions:
                  int_value:
                    description:
                      - Integer valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_int_value:
                        description:
                          - Default value for the threshold parameter.
                        type: int
                        required: false
                      current_int_value:
                        description:
                          - Current value for the threshold parameter.
                        type: int
                        required: false
                  float_value:
                    description:
                      - Float valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_float_value:
                        description:
                          - Default value for the threshold parameter.
                        type: float
                        required: false
                      current_float_value:
                        description:
                          - Current value for the threshold parameter.
                        type: float
                        required: false
                  bool_value:
                    description:
                      - Boolean valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_bool_value:
                        description:
                          - Default value for the threshold parameter.
                        type: bool
                        required: false
                      current_bool_value:
                        description:
                          - Current value for the threshold parameter.
                        type: bool
                        required: false
                  string_value:
                    description:
                      - String valued threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_str_value:
                        description:
                          - Default value for the threshold parameter.
                        type: str
                        required: false
                      current_str_value:
                        description:
                          - Current value for the threshold parameter.
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
- name: Enable an SDA policy and set severity thresholds on a cluster
  nutanix.ncp.ntnx_sda_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    sda_policy_ext_id: "3f47bbcd-6912-5b0f-bee6-8b45a0d1b1de"
    cluster_ext_id: "00062e83-7dd7-51d9-2ebe-ac1f6b7a7ba0"
    is_enabled: true
    schedule_interval_seconds: 300
    alert_config:
      auto_resolve: ENABLED
      critical_severity:
        state: ENABLED
      warning_severity:
        state: ENABLED
      info_severity:
        state: DISABLED
  register: result
  ignore_errors: true

- name: Update SDA policy threshold value on a cluster
  nutanix.ncp.ntnx_sda_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    sda_policy_ext_id: "3f47bbcd-6912-5b0f-bee6-8b45a0d1b1de"
    ext_id: "00062e83-7dd7-51d9-2ebe-ac1f6b7a7ba0"
    is_enabled: true
    alert_config:
      warning_severity:
        state: ENABLED
        threshold_parameters:
          - name: "warning_threshold_percentage"
            param_value:
              int_value:
                current_int_value: 80
"""

RETURN = r"""
response:
  description:
    - Response for updating the cluster-specific configuration of an SDA policy.
    - If C(wait) is true the module returns the updated ClusterConfig object.
    - If C(wait) is false the module returns the async task reference.
  returned: always
  type: dict
  sample:
    {
      "alert_config": {
          "auto_resolve": "ENABLED",
          "critical_severity": {"state": "ENABLED", "threshold_parameters": null},
          "info_severity": {"state": "DISABLED", "threshold_parameters": null},
          "warning_severity": {"state": "ENABLED", "threshold_parameters": null}
      },
      "configurable_parameters": null,
      "ext_id": "00062e83-7dd7-51d9-2ebe-ac1f6b7a7ba0",
      "is_enabled": true,
      "last_modified_by_user": "admin",
      "last_modified_time": "2026-07-20T14:22:15.371000+00:00",
      "links": null,
      "schedule_interval_seconds": 300,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the async task tracking the update.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the ClusterConfig (cluster UUID) that was updated.
  returned: always
  type: str
  sample: "00062e83-7dd7-51d9-2ebe-ac1f6b7a7ba0"

sda_policy_ext_id:
  description:
    - The external ID of the System-Defined Alert Policy that was updated.
  returned: when provided
  type: str
  sample: "3f47bbcd-6912-5b0f-bee6-8b45a0d1b1de"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (idempotency, check-mode delete).
  returned: always
  type: bool
  sample: false

error:
  description: This field holds the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Status/error message.
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "SDA policy cluster configuration is already in the desired state. Nothing to change."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_etag,
    get_system_defined_policies_api_instance,
)
from ..module_utils.v4.monitoring.helpers import (  # noqa: E402
    get_cluster_config_with_etag,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
)

SDK_IMP_ERROR = None
try:
    import ntnx_monitoring_py_client as monitoring_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as monitoring_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


# Fields on the ClusterConfig response that must not be sent back on an update
# request body. `last_modified_by_user` / `last_modified_time` are populated by
# the server, and `ext_id`, `links`, `tenant_id` are read-only identifiers /
# HATEOAS fields.
CLUSTER_CONFIG_READ_ONLY_FIELDS = [
    "last_modified_by_user",
    "last_modified_time",
    "ext_id",
    "links",
    "tenant_id",
]

# The monitoring service rejects update bodies that include a
# SeverityConfig with `state=NOT_SUPPORTED`. Those severities are
# intrinsically read-only on the policy definition, so we drop them from
# the AlertConfig before sending the update.
_NOT_SUPPORTED_STATE = "NOT_SUPPORTED"


def _int_param_value_spec():
    return dict(
        default_int_value=dict(type="int", required=False),
        current_int_value=dict(type="int", required=False),
    )


def _float_param_value_spec():
    return dict(
        default_float_value=dict(type="float", required=False),
        current_float_value=dict(type="float", required=False),
    )


def _bool_param_value_spec():
    return dict(
        default_bool_value=dict(type="bool", required=False),
        current_bool_value=dict(type="bool", required=False),
    )


def _string_param_value_spec():
    return dict(
        default_str_value=dict(type="str", required=False),
        current_str_value=dict(type="str", required=False),
    )


def _param_value_spec():
    return dict(
        int_value=dict(
            type="dict",
            options=_int_param_value_spec(),
            required=False,
            obj=monitoring_sdk.IntConfigurableParamValue,
        ),
        float_value=dict(
            type="dict",
            options=_float_param_value_spec(),
            required=False,
            obj=monitoring_sdk.FloatConfigurableParamValue,
        ),
        bool_value=dict(
            type="dict",
            options=_bool_param_value_spec(),
            required=False,
            obj=monitoring_sdk.BooleanConfigurableParamValue,
        ),
        string_value=dict(
            type="dict",
            options=_string_param_value_spec(),
            required=False,
            obj=monitoring_sdk.StringConfigurableParamValue,
        ),
    )


def _param_value_obj_map():
    return dict(
        int_value=monitoring_sdk.IntConfigurableParamValue,
        float_value=monitoring_sdk.FloatConfigurableParamValue,
        bool_value=monitoring_sdk.BooleanConfigurableParamValue,
        string_value=monitoring_sdk.StringConfigurableParamValue,
    )


def _configurable_parameter_spec():
    return dict(
        name=dict(type="str", required=True),
        display_name=dict(type="str", required=False),
        unit=dict(type="str", required=False),
        param_value=dict(
            type="dict",
            options=_param_value_spec(),
            required=False,
            obj=_param_value_obj_map(),
        ),
    )


def _severity_config_spec():
    return dict(
        state=dict(
            type="str",
            required=False,
            choices=["ENABLED", "DISABLED", "NOT_SUPPORTED"],
            obj=monitoring_sdk.PropertyState,
        ),
        threshold_parameters=dict(
            type="list",
            elements="dict",
            options=_configurable_parameter_spec(),
            required=False,
            obj=monitoring_sdk.AlertPolicyConfigurableParameter,
        ),
    )


def get_module_spec():

    alert_config_spec = dict(
        auto_resolve=dict(
            type="str",
            required=False,
            choices=["ENABLED", "DISABLED", "NOT_SUPPORTED"],
            obj=monitoring_sdk.AutoResolveState,
        ),
        critical_severity=dict(
            type="dict",
            options=_severity_config_spec(),
            required=False,
            obj=monitoring_sdk.SeverityConfig,
        ),
        warning_severity=dict(
            type="dict",
            options=_severity_config_spec(),
            required=False,
            obj=monitoring_sdk.SeverityConfig,
        ),
        info_severity=dict(
            type="dict",
            options=_severity_config_spec(),
            required=False,
            obj=monitoring_sdk.SeverityConfig,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        sda_policy_ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
        is_enabled=dict(type="bool"),
        schedule_interval_seconds=dict(type="int"),
        configurable_parameters=dict(
            type="list",
            elements="dict",
            options=_configurable_parameter_spec(),
            obj=monitoring_sdk.AlertPolicyConfigurableParameter,
        ),
        alert_config=dict(
            type="dict",
            options=alert_config_spec,
            obj=monitoring_sdk.AlertConfig,
        ),
    )
    return module_args


def _resolve_cluster_ext_id(module):
    """Return the ClusterConfig ext_id (Prism Element cluster UUID)."""
    return module.params.get("cluster_ext_id") or module.params.get("ext_id")


def _normalize_config_dict(data):
    """Return a comparable dict for idempotency: strip server / HATEOAS fields."""
    data = strip_internal_attributes(deepcopy(data))
    for field in ("last_modified_by_user", "last_modified_time", "links", "tenant_id"):
        data.pop(field, None)
    return data


def _drop_unsupported_severities(spec):
    """Remove any severity_config on the update spec whose ``state`` is
    ``NOT_SUPPORTED`` because the monitoring API rejects those on update.
    """
    alert_config = getattr(spec, "alert_config", None)
    if alert_config is None:
        return
    for attr in ("critical_severity", "warning_severity", "info_severity"):
        severity = getattr(alert_config, attr, None)
        if severity is None:
            continue
        state = getattr(severity, "state", None)
        state_str = getattr(state, "value", state)
        if state_str == _NOT_SUPPORTED_STATE:
            setattr(alert_config, attr, None)


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """Return True when the desired update matches the current server state."""
    return _normalize_config_dict(old_spec_dict) == _normalize_config_dict(
        update_spec_dict
    )


def update_sda_policy(module, result, api_instance):
    sda_policy_ext_id = module.params.get("sda_policy_ext_id")
    cluster_ext_id = _resolve_cluster_ext_id(module)

    if not sda_policy_ext_id:
        module.fail_json(
            msg="'sda_policy_ext_id' is required to update SDA policy cluster configuration.",
            **result,
        )
    if not cluster_ext_id:
        module.fail_json(
            msg="'cluster_ext_id' (or 'ext_id') is required to update SDA policy cluster configuration.",
            **result,
        )

    result["ext_id"] = cluster_ext_id
    result["sda_policy_ext_id"] = sda_policy_ext_id

    raw_resp, old_spec = get_cluster_config_with_etag(
        module, api_instance, sda_policy_ext_id, cluster_ext_id
    )
    etag = get_etag(data=raw_resp)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for updating SDA policy cluster configuration.",
            **result,
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update spec for SDA policy cluster configuration.",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(old_spec.to_dict())
        module.exit_json(
            msg=(
                "SDA policy cluster configuration is already in the desired state."
                " Nothing to change."
            ),
            **result,
        )

    strip_read_only_fields(update_spec, CLUSTER_CONFIG_READ_ONLY_FIELDS)
    _drop_unsupported_severities(update_spec)

    resp = None
    try:
        resp = api_instance.update_cluster_config_by_id(
            systemDefinedPolicyExtId=sda_policy_ext_id,
            extId=cluster_ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating SDA policy cluster configuration",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        refreshed_resp, refreshed = get_cluster_config_with_etag(
            module, api_instance, sda_policy_ext_id, cluster_ext_id
        )
        del refreshed_resp
        result["response"] = strip_internal_attributes(refreshed.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ("ext_id", "cluster_ext_id"),
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
        "sda_policy_ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }

    state = module.params.get("state")
    if state == "absent":
        module.fail_json(
            msg=(
                "System-Defined Alert Policies cannot be deleted."
                " 'state=absent' is not supported by ntnx_sda_policy_v2."
            ),
            **result,
        )

    api_instance = get_system_defined_policies_api_instance(module)
    update_sda_policy(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
