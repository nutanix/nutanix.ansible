#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_configs_by_sda_id_v2
short_description: Update cluster-specific configuration of a System-Defined Alert Policy in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to update the cluster-specific configuration associated with a
    System-Defined Alert (SDA) Policy for a specific cluster in Nutanix Prism Central.
  - A ClusterConfigsBySdaId entry represents the per-cluster overrides of an SDA policy
    (schedule interval, enablement, alert severity thresholds and configurable parameters)
    and it exists implicitly for every cluster registered to Prism Central.
  - The Nutanix Monitoring v4 API does NOT expose a create or delete endpoint for these
    cluster-specific configuration entries; only the update operation is supported.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Update a Cluster Config of an SDA Policy) -
    Required Roles: Prism Admin, Super Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation
        will be update cluster config of the given SDA policy for the given cluster.
      - C(state=present) without C(ext_id) and C(state=absent) are not supported by the
        underlying API and the module will fail with a descriptive error.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - Cluster UUID for which the SDA policy cluster configuration is being updated.
      - Required for update operation.
    type: str
    required: false
  system_defined_policy_ext_id:
    description:
      - Unique ID of the System-Defined Alert Policy whose per-cluster configuration is
        being updated.
      - Required for update operation.
    type: str
    required: false
  is_enabled:
    description:
      - Indicates whether the SDA policy is enabled or not on the target cluster.
    type: bool
    required: false
  schedule_interval_seconds:
    description:
      - The scheduling interval, in seconds, at which this System-Defined Alert Policy
        is evaluated for the target cluster.
    type: int
    required: false
  configurable_parameters:
    description:
      - Parameters of the SDA that are configurable by a user for the target cluster.
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
          - User-visible display name for the parameter.
        type: str
        required: false
      unit:
        description:
          - Unit associated with the parameter value (for example seconds, percent).
        type: str
        required: false
      param_value:
        description:
          - Current value of the configurable parameter.
          - Exactly one of the sub-typed values (integer, boolean, string, float) MUST
            be provided depending on the data type declared by the policy.
        type: dict
        required: false
        suboptions:
          int_value:
            description:
              - Integer value for the configurable parameter.
              - Populate C(current_int_value) with the desired override.
            type: dict
            required: false
            suboptions:
              default_int_value:
                description:
                  - Default integer value of the parameter (read-only, returned by API).
                type: int
                required: false
              current_int_value:
                description:
                  - Current integer value of the parameter.
                type: int
                required: false
          bool_value:
            description:
              - Boolean value for the configurable parameter.
            type: dict
            required: false
            suboptions:
              default_bool_value:
                description:
                  - Default boolean value of the parameter (read-only, returned by API).
                type: bool
                required: false
              current_bool_value:
                description:
                  - Current boolean value of the parameter.
                type: bool
                required: false
          string_value:
            description:
              - String value for the configurable parameter.
            type: dict
            required: false
            suboptions:
              default_str_value:
                description:
                  - Default string value of the parameter (read-only, returned by API).
                type: str
                required: false
              current_str_value:
                description:
                  - Current string value of the parameter.
                type: str
                required: false
          float_value:
            description:
              - Floating-point value for the configurable parameter.
            type: dict
            required: false
            suboptions:
              default_float_value:
                description:
                  - Default float value of the parameter (read-only, returned by API).
                type: float
                required: false
              current_float_value:
                description:
                  - Current float value of the parameter.
                type: float
                required: false
  alert_config:
    description:
      - Alert-specific properties associated with the SDA policy for the target cluster.
    type: dict
    required: false
    suboptions:
      auto_resolve:
        description:
          - Whether auto-resolution is enabled for alerts raised by this policy.
        type: str
        choices:
          - ENABLED
          - DISABLED
          - NOT_SUPPORTED
        required: false
      critical_severity:
        description:
          - Configuration for the CRITICAL severity threshold of this policy.
        type: dict
        required: false
        suboptions:
          state:
            description:
              - Whether this severity level is enabled, disabled, or not supported.
            type: str
            choices:
              - ENABLED
              - DISABLED
              - NOT_SUPPORTED
            required: false
          threshold_parameters:
            description:
              - Threshold parameters associated with the severity level.
              - Each item follows the same schema as C(configurable_parameters).
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
                  - User-visible display name for the parameter.
                type: str
                required: false
              unit:
                description:
                  - Unit associated with the parameter value.
                type: str
                required: false
              param_value:
                description:
                  - Current value of the threshold parameter.
                type: dict
                required: false
                suboptions:
                  int_value:
                    description:
                      - Integer value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_int_value:
                        description:
                          - Default integer value (read-only).
                        type: int
                        required: false
                      current_int_value:
                        description:
                          - Current integer value.
                        type: int
                        required: false
                  bool_value:
                    description:
                      - Boolean value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_bool_value:
                        description:
                          - Default boolean value (read-only).
                        type: bool
                        required: false
                      current_bool_value:
                        description:
                          - Current boolean value.
                        type: bool
                        required: false
                  string_value:
                    description:
                      - String value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_str_value:
                        description:
                          - Default string value (read-only).
                        type: str
                        required: false
                      current_str_value:
                        description:
                          - Current string value.
                        type: str
                        required: false
                  float_value:
                    description:
                      - Float value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_float_value:
                        description:
                          - Default float value (read-only).
                        type: float
                        required: false
                      current_float_value:
                        description:
                          - Current float value.
                        type: float
                        required: false
      warning_severity:
        description:
          - Configuration for the WARNING severity threshold of this policy.
        type: dict
        required: false
        suboptions:
          state:
            description:
              - Whether this severity level is enabled, disabled, or not supported.
            type: str
            choices:
              - ENABLED
              - DISABLED
              - NOT_SUPPORTED
            required: false
          threshold_parameters:
            description:
              - Threshold parameters associated with the WARNING severity level.
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
                  - User-visible display name for the parameter.
                type: str
                required: false
              unit:
                description:
                  - Unit associated with the parameter value.
                type: str
                required: false
              param_value:
                description:
                  - Current value of the threshold parameter.
                type: dict
                required: false
                suboptions:
                  int_value:
                    description:
                      - Integer value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_int_value:
                        description:
                          - Default integer value (read-only).
                        type: int
                        required: false
                      current_int_value:
                        description:
                          - Current integer value.
                        type: int
                        required: false
                  bool_value:
                    description:
                      - Boolean value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_bool_value:
                        description:
                          - Default boolean value (read-only).
                        type: bool
                        required: false
                      current_bool_value:
                        description:
                          - Current boolean value.
                        type: bool
                        required: false
                  string_value:
                    description:
                      - String value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_str_value:
                        description:
                          - Default string value (read-only).
                        type: str
                        required: false
                      current_str_value:
                        description:
                          - Current string value.
                        type: str
                        required: false
                  float_value:
                    description:
                      - Float value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_float_value:
                        description:
                          - Default float value (read-only).
                        type: float
                        required: false
                      current_float_value:
                        description:
                          - Current float value.
                        type: float
                        required: false
      info_severity:
        description:
          - Configuration for the INFO severity threshold of this policy.
        type: dict
        required: false
        suboptions:
          state:
            description:
              - Whether this severity level is enabled, disabled, or not supported.
            type: str
            choices:
              - ENABLED
              - DISABLED
              - NOT_SUPPORTED
            required: false
          threshold_parameters:
            description:
              - Threshold parameters associated with the INFO severity level.
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
                  - User-visible display name for the parameter.
                type: str
                required: false
              unit:
                description:
                  - Unit associated with the parameter value.
                type: str
                required: false
              param_value:
                description:
                  - Current value of the threshold parameter.
                type: dict
                required: false
                suboptions:
                  int_value:
                    description:
                      - Integer value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_int_value:
                        description:
                          - Default integer value (read-only).
                        type: int
                        required: false
                      current_int_value:
                        description:
                          - Current integer value.
                        type: int
                        required: false
                  bool_value:
                    description:
                      - Boolean value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_bool_value:
                        description:
                          - Default boolean value (read-only).
                        type: bool
                        required: false
                      current_bool_value:
                        description:
                          - Current boolean value.
                        type: bool
                        required: false
                  string_value:
                    description:
                      - String value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_str_value:
                        description:
                          - Default string value (read-only).
                        type: str
                        required: false
                      current_str_value:
                        description:
                          - Current string value.
                        type: str
                        required: false
                  float_value:
                    description:
                      - Float value for the threshold parameter.
                    type: dict
                    required: false
                    suboptions:
                      default_float_value:
                        description:
                          - Default float value (read-only).
                        type: float
                        required: false
                      current_float_value:
                        description:
                          - Current float value.
                        type: float
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
- name: Update SDA policy cluster config - enable and change schedule interval
  nutanix.ncp.ntnx_cluster_configs_by_sda_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    system_defined_policy_ext_id: "5a8b7f2c-4ce3-9212-2ca4-e4b4d258bde7"
    ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    is_enabled: true
    schedule_interval_seconds: 600
    alert_config:
      auto_resolve: ENABLED
      critical_severity:
        state: ENABLED
      warning_severity:
        state: ENABLED
      info_severity:
        state: DISABLED
    configurable_parameters:
      - name: threshold_percent
        display_name: "Threshold percent"
        unit: "percent"
        param_value:
          int_value:
            current_int_value: 80
  register: result
  ignore_errors: true

- name: Disable SDA policy on a specific cluster
  nutanix.ncp.ntnx_cluster_configs_by_sda_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    system_defined_policy_ext_id: "5a8b7f2c-4ce3-9212-2ca4-e4b4d258bde7"
    ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    is_enabled: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating cluster-specific configuration of an SDA Policy.
    - If C(wait) is true, it will contain the updated ClusterConfig details.
    - If C(wait) is false, it will contain the task details.
  returned: always
  type: dict
  sample:
    {
        "alert_config": {
            "auto_resolve": "ENABLED",
            "critical_severity": {
                "state": "ENABLED",
                "threshold_parameters": null
            },
            "info_severity": {
                "state": "DISABLED",
                "threshold_parameters": null
            },
            "warning_severity": {
                "state": "ENABLED",
                "threshold_parameters": null
            }
        },
        "configurable_parameters": null,
        "ext_id": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
        "is_enabled": true,
        "last_modified_by_user": "admin",
        "last_modified_time": "2026-07-20T12:30:00Z",
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
    - Cluster UUID of the SDA policy cluster configuration that was updated.
  returned: always
  type: str
  sample: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"

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
  sample: "Api Exception raised while updating cluster config for SDA policy"
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
    get_cluster_config_by_sda_id,
)
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


def get_module_spec():

    int_value_spec = dict(
        default_int_value=dict(type="int", required=False),
        current_int_value=dict(type="int", required=False),
    )

    bool_value_spec = dict(
        default_bool_value=dict(type="bool", required=False),
        current_bool_value=dict(type="bool", required=False),
    )

    string_value_spec = dict(
        default_str_value=dict(type="str", required=False),
        current_str_value=dict(type="str", required=False),
    )

    float_value_spec = dict(
        default_float_value=dict(type="float", required=False),
        current_float_value=dict(type="float", required=False),
    )

    param_value_spec = dict(
        int_value=dict(
            type="dict",
            options=int_value_spec,
            required=False,
            obj=monitoring_sdk.IntConfigurableParamValue,
        ),
        bool_value=dict(
            type="dict",
            options=bool_value_spec,
            required=False,
            obj=monitoring_sdk.BooleanConfigurableParamValue,
        ),
        string_value=dict(
            type="dict",
            options=string_value_spec,
            required=False,
            obj=monitoring_sdk.StringConfigurableParamValue,
        ),
        float_value=dict(
            type="dict",
            options=float_value_spec,
            required=False,
            obj=monitoring_sdk.FloatConfigurableParamValue,
        ),
    )

    configurable_parameter_spec = dict(
        name=dict(type="str", required=False),
        display_name=dict(type="str", required=False),
        unit=dict(type="str", required=False),
        param_value=dict(
            type="dict",
            options=param_value_spec,
            required=False,
            obj=dict(
                int_value=monitoring_sdk.IntConfigurableParamValue,
                bool_value=monitoring_sdk.BooleanConfigurableParamValue,
                string_value=monitoring_sdk.StringConfigurableParamValue,
                float_value=monitoring_sdk.FloatConfigurableParamValue,
            ),
            mutually_exclusive=[
                ("int_value", "bool_value", "string_value", "float_value"),
            ],
        ),
    )

    severity_config_spec = dict(
        state=dict(
            type="str",
            required=False,
            choices=["ENABLED", "DISABLED", "NOT_SUPPORTED"],
            obj=monitoring_sdk.PropertyState,
        ),
        threshold_parameters=dict(
            type="list",
            elements="dict",
            required=False,
            options=configurable_parameter_spec,
            obj=monitoring_sdk.AlertPolicyConfigurableParameter,
        ),
    )

    alert_config_spec = dict(
        auto_resolve=dict(
            type="str",
            required=False,
            choices=["ENABLED", "DISABLED", "NOT_SUPPORTED"],
            obj=monitoring_sdk.AutoResolveState,
        ),
        critical_severity=dict(
            type="dict",
            required=False,
            options=severity_config_spec,
            obj=monitoring_sdk.SeverityConfig,
        ),
        warning_severity=dict(
            type="dict",
            required=False,
            options=severity_config_spec,
            obj=monitoring_sdk.SeverityConfig,
        ),
        info_severity=dict(
            type="dict",
            required=False,
            options=severity_config_spec,
            obj=monitoring_sdk.SeverityConfig,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        system_defined_policy_ext_id=dict(type="str"),
        is_enabled=dict(type="bool"),
        schedule_interval_seconds=dict(type="int"),
        configurable_parameters=dict(
            type="list",
            elements="dict",
            options=configurable_parameter_spec,
            obj=monitoring_sdk.AlertPolicyConfigurableParameter,
        ),
        alert_config=dict(
            type="dict",
            options=alert_config_spec,
            obj=monitoring_sdk.AlertConfig,
        ),
    )
    return module_args


def create_ClusterConfigsBySdaId(module, result, api_instance):
    """Create is not supported for SDA policy cluster configs.

    The Nutanix Monitoring v4 API does not expose a create endpoint for these
    per-cluster entries; they exist implicitly for every cluster that is
    registered to Prism Central. Fail with a descriptive error so that the user
    understands the supported workflow (update via ext_id).
    """
    result["error"] = (
        "Create operation is not supported for ClusterConfigsBySdaId. "
        "The per-cluster configuration of a System-Defined Alert Policy is created "
        "implicitly by Prism Central. Use state=present with 'ext_id' and "
        "'system_defined_policy_ext_id' to update an existing entry."
    )
    module.fail_json(
        msg=(
            "Create operation is not supported for ClusterConfigsBySdaId. "
            "Provide 'ext_id' (cluster UUID) and 'system_defined_policy_ext_id' "
            "to update an existing per-cluster SDA policy configuration."
        ),
        **result,
    )


def _idempotency_check(old_spec_dict, update_spec_dict):
    """Compare the old and desired spec dicts to detect idempotent updates."""
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    for key in ("last_modified_by_user", "last_modified_time", "links", "tenant_id"):
        old_spec_dict.pop(key, None)
        update_spec_dict.pop(key, None)
    return old_spec_dict == update_spec_dict


def _drop_unsupported_severity_configs(alert_config):
    """Null out per-severity configs whose ``state`` is NOT_SUPPORTED.

    The Nutanix Monitoring v4 API rejects PUT requests that include a value
    (even NOT_SUPPORTED) for a severity that the policy does not support. Since
    the update spec is built from the current GET response, we must strip those
    entries before sending the update body.
    """
    if alert_config is None:
        return
    for severity_attr in ("critical_severity", "warning_severity", "info_severity"):
        severity_cfg = getattr(alert_config, severity_attr, None)
        if severity_cfg is None:
            continue
        state = getattr(severity_cfg, "state", None)
        if state == "NOT_SUPPORTED":
            setattr(alert_config, severity_attr, None)


def _sanitize_update_spec(update_spec):
    """Remove fields that cannot be sent in the ClusterConfig update body."""
    strip_read_only_fields(
        update_spec, fields=["last_modified_by_user", "last_modified_time"]
    )
    _drop_unsupported_severity_configs(getattr(update_spec, "alert_config", None))


def update_ClusterConfigsBySdaId(module, result, api_instance):
    validate_required_params(module, ["ext_id", "system_defined_policy_ext_id"])
    ext_id = module.params.get("ext_id")
    system_defined_policy_ext_id = module.params.get("system_defined_policy_ext_id")
    result["ext_id"] = ext_id

    old_spec = get_cluster_config_by_sda_id(
        module, api_instance, system_defined_policy_ext_id, ext_id
    )
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg=(
                "Unable to fetch etag for updating ClusterConfigsBySdaId with "
                "ext_id: {0} under system_defined_policy_ext_id: {1}".format(
                    ext_id, system_defined_policy_ext_id
                )
            ),
            **result,
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update ClusterConfigsBySdaId spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if _idempotency_check(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(old_spec.to_dict())
        module.exit_json(
            msg=(
                "ClusterConfigsBySdaId with ext_id '{0}' for SDA policy '{1}' is "
                "already in the desired state. Skipping update.".format(
                    ext_id, system_defined_policy_ext_id
                )
            ),
            **result,
        )

    _sanitize_update_spec(update_spec)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.update_cluster_config_by_id(
            systemDefinedPolicyExtId=system_defined_policy_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while updating cluster config for SDA policy "
                "ext_id: {0} and cluster ext_id: {1}".format(
                    system_defined_policy_ext_id, ext_id
                )
            ),
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    if task_ext_id:
        result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        latest = get_cluster_config_by_sda_id(
            module, api_instance, system_defined_policy_ext_id, ext_id
        )
        result["response"] = strip_internal_attributes(latest.to_dict())

    result["changed"] = True


def delete_ClusterConfigsBySdaId(module, result, api_instance):
    """Delete is not supported for SDA policy cluster configs.

    The Nutanix Monitoring v4 API does not expose a delete endpoint for these
    per-cluster entries. Fail with a descriptive error so that the user
    understands the supported workflow.
    """
    result["error"] = (
        "Delete operation is not supported for ClusterConfigsBySdaId. "
        "The per-cluster configuration of a System-Defined Alert Policy is managed "
        "by Prism Central and can only be updated. Use state=present with "
        "is_enabled=false to disable evaluation of the SDA policy on a specific cluster."
    )
    module.fail_json(
        msg=(
            "Delete operation is not supported for ClusterConfigsBySdaId. "
            "Use state=present with is_enabled=false to disable the SDA policy on the target cluster."
        ),
        **result,
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
    api_instance = get_system_defined_policies_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_ClusterConfigsBySdaId(module, result, api_instance)
        else:
            create_ClusterConfigsBySdaId(module, result, api_instance)
    else:
        delete_ClusterConfigsBySdaId(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
