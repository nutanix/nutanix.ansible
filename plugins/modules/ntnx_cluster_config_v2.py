#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_config_v2
short_description: Update cluster-specific configuration of a System-Defined Alert Policy in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to update cluster-specific configuration (ClusterConfig)
    associated with a System-Defined Alert (SDA) Policy in Nutanix Prism Central.
  - ClusterConfig captures the overrides for an SDA policy on a specific cluster,
    including enable/disable state, schedule interval, per-severity thresholds and
    auto-resolve behaviour.
  - The Nutanix Monitoring v4 API does not support create or delete for
    ClusterConfig - it is auto-provisioned per cluster whenever an SDA policy
    is present. Only update is supported.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation. The required roles depend on the operation being performed.
  - >-
    B(Update a ClusterConfig for a System-Defined Alert Policy) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update ClusterConfig.
      - The Monitoring v4 API does not support create/delete for ClusterConfig; other combinations will fail with a descriptive error.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The Cluster UUID whose ClusterConfig entry (under the given SDA policy) should be updated.
      - Required for update.
    type: str
    required: false
  system_defined_policy_ext_id:
    description:
      - The unique external ID of the parent System-Defined Alert (SDA) Policy.
      - Required for update.
    type: str
    required: false
  is_enabled:
    description:
      - Indicates whether the SDA policy is enabled or not on the cluster.
    type: bool
    required: false
  schedule_interval_seconds:
    description:
      - Interval in seconds defining how often the health check/policy runs on this cluster.
    type: int
    required: false
  configurable_parameters:
    description:
      - Parameters of the SDA that are configurable by a user.
      - Each entry captures the parameter name and its per-cluster value.
    type: list
    elements: dict
    required: false
    suboptions:
      name:
        description:
          - Unique identifier name for the parameter.
        type: str
        required: false
      display_name:
        description:
          - Display name of the parameter.
        type: str
        required: false
      unit:
        description:
          - Unit for the parameter (e.g., seconds, count, MB).
        type: str
        required: false
      param_value:
        description:
          - The value assigned to the parameter for this cluster.
          - Exactly ONE of C(int_value), C(float_value), C(bool_value) or C(string_value)
            may be provided.
        type: dict
        required: false
        suboptions:
          int_value:
            description:
              - Value when the parameter is an integer.
            type: dict
            required: false
            suboptions:
              default_int_value:
                description:
                  - Captures the default value of the parameter.
                type: int
                required: false
              current_int_value:
                description:
                  - Captures the current value of the parameter for this cluster.
                type: int
                required: false
          float_value:
            description:
              - Value when the parameter is a float.
            type: dict
            required: false
            suboptions:
              default_float_value:
                description:
                  - Captures the default value of the parameter.
                type: float
                required: false
              current_float_value:
                description:
                  - Captures the current value of the parameter for this cluster.
                type: float
                required: false
          bool_value:
            description:
              - Value when the parameter is a boolean.
            type: dict
            required: false
            suboptions:
              default_bool_value:
                description:
                  - Captures the default value of the parameter.
                type: bool
                required: false
              current_bool_value:
                description:
                  - Captures the current value of the parameter for this cluster.
                type: bool
                required: false
          string_value:
            description:
              - Value when the parameter is a string.
            type: dict
            required: false
            suboptions:
              default_str_value:
                description:
                  - Captures the default value of the parameter.
                type: str
                required: false
              current_str_value:
                description:
                  - Captures the current value of the parameter for this cluster.
                type: str
                required: false
  alert_config:
    description:
      - Alert specific properties associated with the policy on this cluster.
    type: dict
    required: false
    suboptions:
      auto_resolve:
        description:
          - Auto resolve state for the alert.
        type: str
        required: false
        choices:
          - DISABLED
          - ENABLED
          - NOT_SUPPORTED
      critical_severity:
        description:
          - Critical severity override configuration.
        type: dict
        required: false
        suboptions:
          state:
            description:
              - Enable/disable state for this severity.
            type: str
            required: false
            choices:
              - DISABLED
              - ENABLED
              - NOT_SUPPORTED
          threshold_parameters:
            description:
              - Alert-related thresholds that correspond to this severity.
            type: list
            elements: dict
            required: false
            suboptions:
              name:
                description:
                  - Unique identifier name for the parameter.
                type: str
                required: false
              display_name:
                description:
                  - Display name of the parameter.
                type: str
                required: false
              unit:
                description:
                  - Unit for the parameter.
                type: str
                required: false
              param_value:
                description:
                  - The value assigned to the parameter for this severity.
                  - Exactly ONE of C(int_value), C(float_value), C(bool_value) or C(string_value)
                    may be provided.
                type: dict
                required: false
                suboptions:
                  int_value:
                    description:
                      - Value when the threshold is an integer.
                    type: dict
                    required: false
                    suboptions:
                      default_int_value:
                        description:
                          - Captures the default value of the parameter.
                        type: int
                        required: false
                      current_int_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
                        type: int
                        required: false
                  float_value:
                    description:
                      - Value when the threshold is a float.
                    type: dict
                    required: false
                    suboptions:
                      default_float_value:
                        description:
                          - Captures the default value of the parameter.
                        type: float
                        required: false
                      current_float_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
                        type: float
                        required: false
                  bool_value:
                    description:
                      - Value when the threshold is a boolean.
                    type: dict
                    required: false
                    suboptions:
                      default_bool_value:
                        description:
                          - Captures the default value of the parameter.
                        type: bool
                        required: false
                      current_bool_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
                        type: bool
                        required: false
                  string_value:
                    description:
                      - Value when the threshold is a string.
                    type: dict
                    required: false
                    suboptions:
                      default_str_value:
                        description:
                          - Captures the default value of the parameter.
                        type: str
                        required: false
                      current_str_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
                        type: str
                        required: false
      warning_severity:
        description:
          - Warning severity override configuration.
        type: dict
        required: false
        suboptions:
          state:
            description:
              - Enable/disable state for this severity.
            type: str
            required: false
            choices:
              - DISABLED
              - ENABLED
              - NOT_SUPPORTED
          threshold_parameters:
            description:
              - Alert-related thresholds that correspond to this severity.
            type: list
            elements: dict
            required: false
            suboptions:
              name:
                description:
                  - Unique identifier name for the parameter.
                type: str
                required: false
              display_name:
                description:
                  - Display name of the parameter.
                type: str
                required: false
              unit:
                description:
                  - Unit for the parameter.
                type: str
                required: false
              param_value:
                description:
                  - Same shape as C(alert_config.critical_severity.threshold_parameters.param_value).
                type: dict
                required: false
                suboptions:
                  int_value:
                    description:
                      - Value when the threshold is an integer.
                    type: dict
                    required: false
                    suboptions:
                      default_int_value:
                        description:
                          - Captures the default value of the parameter.
                        type: int
                        required: false
                      current_int_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
                        type: int
                        required: false
                  float_value:
                    description:
                      - Value when the threshold is a float.
                    type: dict
                    required: false
                    suboptions:
                      default_float_value:
                        description:
                          - Captures the default value of the parameter.
                        type: float
                        required: false
                      current_float_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
                        type: float
                        required: false
                  bool_value:
                    description:
                      - Value when the threshold is a boolean.
                    type: dict
                    required: false
                    suboptions:
                      default_bool_value:
                        description:
                          - Captures the default value of the parameter.
                        type: bool
                        required: false
                      current_bool_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
                        type: bool
                        required: false
                  string_value:
                    description:
                      - Value when the threshold is a string.
                    type: dict
                    required: false
                    suboptions:
                      default_str_value:
                        description:
                          - Captures the default value of the parameter.
                        type: str
                        required: false
                      current_str_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
                        type: str
                        required: false
      info_severity:
        description:
          - Info severity override configuration.
        type: dict
        required: false
        suboptions:
          state:
            description:
              - Enable/disable state for this severity.
            type: str
            required: false
            choices:
              - DISABLED
              - ENABLED
              - NOT_SUPPORTED
          threshold_parameters:
            description:
              - Alert-related thresholds that correspond to this severity.
            type: list
            elements: dict
            required: false
            suboptions:
              name:
                description:
                  - Unique identifier name for the parameter.
                type: str
                required: false
              display_name:
                description:
                  - Display name of the parameter.
                type: str
                required: false
              unit:
                description:
                  - Unit for the parameter.
                type: str
                required: false
              param_value:
                description:
                  - Same shape as C(alert_config.critical_severity.threshold_parameters.param_value).
                type: dict
                required: false
                suboptions:
                  int_value:
                    description:
                      - Value when the threshold is an integer.
                    type: dict
                    required: false
                    suboptions:
                      default_int_value:
                        description:
                          - Captures the default value of the parameter.
                        type: int
                        required: false
                      current_int_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
                        type: int
                        required: false
                  float_value:
                    description:
                      - Value when the threshold is a float.
                    type: dict
                    required: false
                    suboptions:
                      default_float_value:
                        description:
                          - Captures the default value of the parameter.
                        type: float
                        required: false
                      current_float_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
                        type: float
                        required: false
                  bool_value:
                    description:
                      - Value when the threshold is a boolean.
                    type: dict
                    required: false
                    suboptions:
                      default_bool_value:
                        description:
                          - Captures the default value of the parameter.
                        type: bool
                        required: false
                      current_bool_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
                        type: bool
                        required: false
                  string_value:
                    description:
                      - Value when the threshold is a string.
                    type: dict
                    required: false
                    suboptions:
                      default_str_value:
                        description:
                          - Captures the default value of the parameter.
                        type: str
                        required: false
                      current_str_value:
                        description:
                          - Captures the current value of the parameter for this cluster.
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
- name: Update ClusterConfig - toggle isEnabled and adjust schedule interval
  nutanix.ncp.ntnx_cluster_config_v2:
    state: present
    system_defined_policy_ext_id: "6c3f96e8-4d63-4a91-a2b4-4f6ce7de7f22"
    ext_id: "0005f36a-b46f-8d0e-0000-000000000000"
    is_enabled: true
    schedule_interval_seconds: 600
  register: result
  ignore_errors: true

- name: Update ClusterConfig - full spec with alert_config severities
  nutanix.ncp.ntnx_cluster_config_v2:
    state: present
    system_defined_policy_ext_id: "6c3f96e8-4d63-4a91-a2b4-4f6ce7de7f22"
    ext_id: "0005f36a-b46f-8d0e-0000-000000000000"
    is_enabled: true
    schedule_interval_seconds: 300
    configurable_parameters:
      - name: "sample_param"
        display_name: "Sample Param"
        unit: "seconds"
        param_value:
          int_value:
            default_int_value: 60
            current_int_value: 120
    alert_config:
      auto_resolve: ENABLED
      critical_severity:
        state: ENABLED
        threshold_parameters:
          - name: "critical_threshold"
            display_name: "Critical Threshold"
            unit: "%"
            param_value:
              int_value:
                default_int_value: 90
                current_int_value: 95
      warning_severity:
        state: ENABLED
        threshold_parameters:
          - name: "warning_threshold"
            display_name: "Warning Threshold"
            unit: "%"
            param_value:
              int_value:
                default_int_value: 75
                current_int_value: 80
      info_severity:
        state: DISABLED
  register: result
  ignore_errors: true

- name: Delete ClusterConfig (not supported by API — fails gracefully)
  nutanix.ncp.ntnx_cluster_config_v2:
    state: absent
    system_defined_policy_ext_id: "6c3f96e8-4d63-4a91-a2b4-4f6ce7de7f22"
    ext_id: "0005f36a-b46f-8d0e-0000-000000000000"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating a ClusterConfig.
    - If the operation is update and C(wait) is true, it will return the ClusterConfig details.
    - If the operation is update and C(wait) is false, it will return the task details.
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
      "ext_id": "0005f36a-b46f-8d0e-0000-000000000000",
      "is_enabled": true,
      "last_modified_by_user": "admin",
      "last_modified_time": "2026-07-21T10:15:22.123456+00:00",
      "links": null,
      "schedule_interval_seconds": 600,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID (Cluster UUID) of the ClusterConfig.
  returned: always
  type: str
  sample: "0005f36a-b46f-8d0e-0000-000000000000"

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
  sample: "Api Exception raised while updating ClusterConfig"
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
from ..module_utils.v4.monitoring.helpers import get_cluster_config  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_monitoring_py_client as monitoring_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as monitoring_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def _param_value_spec():
    """Argument-spec dict for AlertPolicyConfigurableParameterparam_value oneOf wrapper."""
    return dict(
        int_value=dict(
            type="dict",
            required=False,
            options=dict(
                default_int_value=dict(type="int", required=False),
                current_int_value=dict(type="int", required=False),
            ),
            obj=monitoring_sdk.IntConfigurableParamValue,
        ),
        float_value=dict(
            type="dict",
            required=False,
            options=dict(
                default_float_value=dict(type="float", required=False),
                current_float_value=dict(type="float", required=False),
            ),
            obj=monitoring_sdk.FloatConfigurableParamValue,
        ),
        bool_value=dict(
            type="dict",
            required=False,
            options=dict(
                default_bool_value=dict(type="bool", required=False),
                current_bool_value=dict(type="bool", required=False),
            ),
            obj=monitoring_sdk.BooleanConfigurableParamValue,
        ),
        string_value=dict(
            type="dict",
            required=False,
            options=dict(
                default_str_value=dict(type="str", required=False),
                current_str_value=dict(type="str", required=False),
            ),
            obj=monitoring_sdk.StringConfigurableParamValue,
        ),
    )


def _configurable_parameter_spec():
    """Argument-spec dict for AlertPolicyConfigurableParameter."""
    return dict(
        name=dict(type="str", required=False),
        display_name=dict(type="str", required=False),
        unit=dict(type="str", required=False),
        param_value=dict(
            type="dict",
            required=False,
            options=_param_value_spec(),
            obj={
                "int_value": monitoring_sdk.IntConfigurableParamValue,
                "float_value": monitoring_sdk.FloatConfigurableParamValue,
                "bool_value": monitoring_sdk.BooleanConfigurableParamValue,
                "string_value": monitoring_sdk.StringConfigurableParamValue,
            },
            mutually_exclusive=[
                ("int_value", "float_value", "bool_value", "string_value")
            ],
        ),
    )


def _severity_config_spec():
    """Argument-spec dict for SeverityConfig."""
    return dict(
        state=dict(
            type="str",
            required=False,
            choices=["DISABLED", "ENABLED", "NOT_SUPPORTED"],
            obj=monitoring_sdk.PropertyState,
        ),
        threshold_parameters=dict(
            type="list",
            elements="dict",
            required=False,
            options=_configurable_parameter_spec(),
            obj=monitoring_sdk.AlertPolicyConfigurableParameter,
        ),
    )


def get_module_spec():

    alert_config_spec = dict(
        auto_resolve=dict(
            type="str",
            required=False,
            choices=["DISABLED", "ENABLED", "NOT_SUPPORTED"],
            obj=monitoring_sdk.AutoResolveState,
        ),
        critical_severity=dict(
            type="dict",
            required=False,
            options=_severity_config_spec(),
            obj=monitoring_sdk.SeverityConfig,
        ),
        warning_severity=dict(
            type="dict",
            required=False,
            options=_severity_config_spec(),
            obj=monitoring_sdk.SeverityConfig,
        ),
        info_severity=dict(
            type="dict",
            required=False,
            options=_severity_config_spec(),
            obj=monitoring_sdk.SeverityConfig,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        system_defined_policy_ext_id=dict(type="str", required=False),
        is_enabled=dict(type="bool", required=False),
        schedule_interval_seconds=dict(type="int", required=False),
        configurable_parameters=dict(
            type="list",
            elements="dict",
            required=False,
            options=_configurable_parameter_spec(),
            obj=monitoring_sdk.AlertPolicyConfigurableParameter,
        ),
        alert_config=dict(
            type="dict",
            required=False,
            options=alert_config_spec,
            obj=monitoring_sdk.AlertConfig,
        ),
    )
    return module_args


def _fetch_current_cluster_config(module, api_instance):
    """Fetch the current ClusterConfig object (already unwrapped via .data)."""
    sda_policy_ext_id = module.params.get("system_defined_policy_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_cluster_config(module, api_instance, sda_policy_ext_id, ext_id)
    return resp


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """Compare stripped dicts and return True if they are effectively equal."""
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    # last_modified_* fields are server-populated and MUST NOT drive idempotency
    for key in ("last_modified_by_user", "last_modified_time"):
        old_spec_dict.pop(key, None)
        update_spec_dict.pop(key, None)
    return old_spec_dict == update_spec_dict


def _sanitize_alert_config_for_update(spec):
    """
    The Monitoring v4 API returns ``state: NOT_SUPPORTED`` on severities the
    underlying NCC check does not expose, but rejects that value on write with
    ``MON-30018 invalid argument for key alertConfig/<severity>/state``. The
    same applies to ``auto_resolve``. Detach any such severity before we PUT
    the spec back so we do not re-post a server-populated marker as user
    input.
    """
    ac = getattr(spec, "alert_config", None)
    if ac is None:
        return
    if getattr(ac, "auto_resolve", None) == "NOT_SUPPORTED":
        try:
            ac.auto_resolve = None
        except AttributeError:
            pass
    for sev_attr in ("critical_severity", "warning_severity", "info_severity"):
        sev = getattr(ac, sev_attr, None)
        if sev is None:
            continue
        if getattr(sev, "state", None) == "NOT_SUPPORTED":
            try:
                setattr(ac, sev_attr, None)
            except AttributeError:
                pass


def create_ClusterConfig(module, result, api_instance):
    """Create is not supported by the Monitoring v4 API for ClusterConfig."""
    result["failed"] = True
    module.fail_json(
        msg=(
            "Create is not supported for ClusterConfig by the Monitoring v4 API. "
            "ClusterConfig entries are auto-provisioned for each cluster when a "
            "System-Defined Alert Policy is present. Provide 'ext_id' and "
            "'system_defined_policy_ext_id' to update an existing ClusterConfig."
        ),
        **result,
    )


def update_ClusterConfig(module, result, api_instance):
    validate_required_params(module, ["ext_id", "system_defined_policy_ext_id"])
    sda_policy_ext_id = module.params.get("system_defined_policy_ext_id")
    ext_id = module.params.get("ext_id")

    result["ext_id"] = ext_id

    current = _fetch_current_cluster_config(module, api_instance)
    old_spec = current.data
    etag = get_etag(data=current)
    if not etag:
        return module.fail_json(
            msg=(
                "Unable to fetch etag for updating ClusterConfig with cluster ext_id: "
                "{0} under System-Defined Alert Policy: {1}".format(
                    ext_id, sda_policy_ext_id
                )
            ),
            **result,
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update ClusterConfig spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(old_spec.to_dict())
        module.exit_json(
            msg="Nothing to change. ClusterConfig is already in the desired state.",
            **result,
        )

    strip_read_only_fields(
        update_spec, fields=["last_modified_by_user", "last_modified_time"]
    )
    _sanitize_alert_config_for_update(update_spec)

    resp = None
    try:
        resp = api_instance.update_cluster_config_by_id(
            systemDefinedPolicyExtId=sda_policy_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating ClusterConfig",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        refreshed = _fetch_current_cluster_config(module, api_instance)
        result["response"] = strip_internal_attributes(refreshed.data.to_dict())
    result["changed"] = True


def delete_ClusterConfig(module, result, api_instance):
    """Delete is not supported by the Monitoring v4 API for ClusterConfig."""
    result["failed"] = True
    module.fail_json(
        msg=(
            "Delete is not supported for ClusterConfig by the Monitoring v4 API. "
            "ClusterConfig entries are auto-managed by the platform for each "
            "System-Defined Alert Policy and cannot be removed via API."
        ),
        **result,
    )


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id", "system_defined_policy_ext_id")),
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
    api_instance = get_system_defined_policies_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_ClusterConfig(module, result, api_instance)
        else:
            create_ClusterConfig(module, result, api_instance)
    else:
        delete_ClusterConfig(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
