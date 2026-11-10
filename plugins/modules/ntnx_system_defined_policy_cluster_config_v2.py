#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_system_defined_policy_cluster_config_v2
short_description: Update System-Defined Alert policy cluster configuration
version_added: "2.7.0"
description:
    - Update cluster-specific configuration associated with a System-Defined Alert Policy.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update System Defined Alert Policy Cluster Configs) -
      Required Roles: Monitoring Admin, Prism Admin, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will update the cluster configuration.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    system_defined_policy_ext_id:
        description:
            - Unique ID of the System-Defined Alert Policy.
        type: str
        required: true
    ext_id:
        description:
            - Cluster UUID.
        type: str
        required: true
    is_enabled:
        description:
            - Indicates whether the SDA policy is enabled or not on the cluster.
        type: bool
    schedule_interval_seconds:
        description:
            - Interval in seconds for periodically executing the SDA policy.
            - This will not be set for policies with the type NOT_SCHEDULED & EVENT_DRIVEN.
        type: int
    configurable_parameters:
        description:
            - Parameters of the SDA that are configurable by a user.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Unique identifier name for the parameter.
                type: str
                required: true
            param_value:
                description:
                    - Captures the parameter value. Currently, it supports 4 data type, that is,
                      string, integer, float, and boolean.
                type: dict
                required: true
                suboptions:
                    int_configurable_param_value:
                        description:
                            - Captures values of the parameter when it's an integer type.
                        type: dict
                        suboptions:
                            current_int_value:
                                description:
                                    - Captures the current value of the parameter.
                                type: int
                                required: true
                    float_configurable_param_value:
                        description:
                            - Captures values of the parameter when it's of type float.
                        type: dict
                        suboptions:
                            current_float_value:
                                description:
                                    - Captures the current value of the parameter.
                                type: float
                                required: true
                    boolean_configurable_param_value:
                        description:
                            - Captures values of the parameter when it's of type boolean.
                        type: dict
                        suboptions:
                            current_bool_value:
                                description:
                                    - Captures the current value of the parameter.
                                type: bool
                                required: true
                    string_configurable_param_value:
                        description:
                            - Captures values of the parameter when it's of type string.
                        type: dict
                        suboptions:
                            current_str_value:
                                description:
                                    - Captures the current value of the parameter.
                                type: str
                                required: true
    alert_config:
        description:
            - Alert specific properties associated with the policy.
        type: dict
        suboptions:
            auto_resolve:
                description:
                    - Indicates the auto-resolve configuration for the alert generated through the
                      policy.
                type: str
                choices:
                    - ENABLED
                    - DISABLED
                    - NOT_SUPPORTED
            critical_severity:
                description:
                    - Captures information about alert of Critical severity.
                type: dict
                suboptions:
                    state:
                        description:
                            - Indicates whether an alert of the specific severity type is configured
                              to be raised or not.
                        type: str
                        choices:
                            - ENABLED
                            - DISABLED
                            - NOT_SUPPORTED
                    threshold_parameters:
                        description:
                            - Captures alert-related thresholds that correspond to a particular
                              severity.
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description:
                                    - Unique identifier name for the parameter.
                                type: str
                                required: true
                            param_value:
                                description:
                                    - Captures the parameter value. Currently, it supports 4 data
                                      type, that is, string, integer, float, and boolean.
                                type: dict
                                required: true
                                suboptions:
                                    int_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's an integer
                                              type.
                                        type: dict
                                        suboptions:
                                            current_int_value:
                                                description:
                                                    - Captures the current value of the parameter.
                                                type: int
                                                required: true
                                    float_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's of type
                                              float.
                                        type: dict
                                        suboptions:
                                            current_float_value:
                                                description:
                                                    - Captures the current value of the parameter.
                                                type: float
                                                required: true
                                    boolean_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's of type
                                              boolean.
                                        type: dict
                                        suboptions:
                                            current_bool_value:
                                                description:
                                                    - Captures the current value of the parameter.
                                                type: bool
                                                required: true
                                    string_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's of type
                                              string.
                                        type: dict
                                        suboptions:
                                            current_str_value:
                                                description:
                                                    - Captures the current value of the parameter.
                                                type: str
                                                required: true
            warning_severity:
                description:
                    - Captures information about alert of Warning severity.
                type: dict
                suboptions:
                    state:
                        description:
                            - Indicates whether an alert of the specific severity type is configured
                              to be raised or not.
                        type: str
                        choices:
                            - ENABLED
                            - DISABLED
                            - NOT_SUPPORTED
                    threshold_parameters:
                        description:
                            - Captures alert-related thresholds that correspond to a particular
                              severity.
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description:
                                    - Unique identifier name for the parameter.
                                type: str
                                required: true
                            param_value:
                                description:
                                    - Captures the parameter value. Currently, it supports 4 data
                                      type, that is, string, integer, float, and boolean.
                                type: dict
                                required: true
                                suboptions:
                                    int_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's an integer
                                              type.
                                        type: dict
                                        suboptions:
                                            current_int_value:
                                                description:
                                                    - Captures the current value of the parameter.
                                                type: int
                                                required: true
                                    float_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's of type
                                              float.
                                        type: dict
                                        suboptions:
                                            current_float_value:
                                                description:
                                                    - Captures the current value of the parameter.
                                                type: float
                                                required: true
                                    boolean_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's of type
                                              boolean.
                                        type: dict
                                        suboptions:
                                            current_bool_value:
                                                description:
                                                    - Captures the current value of the parameter.
                                                type: bool
                                                required: true
                                    string_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's of type
                                              string.
                                        type: dict
                                        suboptions:
                                            current_str_value:
                                                description:
                                                    - Captures the current value of the parameter.
                                                type: str
                                                required: true
            info_severity:
                description:
                    - Captures information about alert of Info severity.
                type: dict
                suboptions:
                    state:
                        description:
                            - Indicates whether an alert of the specific severity type is configured
                              to be raised or not.
                        type: str
                        choices:
                            - ENABLED
                            - DISABLED
                            - NOT_SUPPORTED
                    threshold_parameters:
                        description:
                            - Captures alert-related thresholds that correspond to a particular
                              severity.
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description:
                                    - Unique identifier name for the parameter.
                                type: str
                                required: true
                            param_value:
                                description:
                                    - Captures the parameter value. Currently, it supports 4 data
                                      type, that is, string, integer, float, and boolean.
                                type: dict
                                required: true
                                suboptions:
                                    int_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's an integer
                                              type.
                                        type: dict
                                        suboptions:
                                            current_int_value:
                                                description:
                                                    - Captures the current value of the parameter.
                                                type: int
                                                required: true
                                    float_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's of type
                                              float.
                                        type: dict
                                        suboptions:
                                            current_float_value:
                                                description:
                                                    - Captures the current value of the parameter.
                                                type: float
                                                required: true
                                    boolean_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's of type
                                              boolean.
                                        type: dict
                                        suboptions:
                                            current_bool_value:
                                                description:
                                                    - Captures the current value of the parameter.
                                                type: bool
                                                required: true
                                    string_configurable_param_value:
                                        description:
                                            - Captures values of the parameter when it's of type
                                              string.
                                        type: dict
                                        suboptions:
                                            current_str_value:
                                                description:
                                                    - Captures the current value of the parameter.
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
- name: Update System-Defined policy cluster configuration
  nutanix.ncp.ntnx_system_defined_policy_cluster_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    system_defined_policy_ext_id: "111053"
    ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    is_enabled: true
    schedule_interval_seconds: 3600
    alert_config:
      auto_resolve: ENABLED
      critical_severity:
        state: ENABLED
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for updating System-Defined policy cluster configuration.
        - If C(wait) is True, the response will be the cluster configuration details after the
          update operation is completed.
        - If C(wait) is False, the response will be task details.
    type: dict
    returned: always
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
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:1a1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e5e"
ext_id:
    description: The external ID of the cluster.
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
skipped:
    description: This indicates whether the task was skipped
    type: bool
    returned: When the operation was skipped
    sample: true
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or module is idempotent
    type: str
    sample: "Nothing to change."
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
"""

import copy  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402

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
)

SDK_IMP_ERROR = None
try:
    import ntnx_monitoring_py_client as sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

_READ_ONLY_FIELDS = (
    "ext_id",
    "links",
    "tenant_id",
    "last_modified_by_user",
    "last_modified_time",
)
PROPERTY_STATE_CHOICES = ["ENABLED", "DISABLED", "NOT_SUPPORTED"]
PARAM_VALUE_KEYS = (
    "int_configurable_param_value",
    "float_configurable_param_value",
    "boolean_configurable_param_value",
    "string_configurable_param_value",
)


def _param_value_spec():
    return dict(
        int_configurable_param_value=dict(
            type="dict",
            options=dict(current_int_value=dict(type="int", required=True)),
        ),
        float_configurable_param_value=dict(
            type="dict",
            options=dict(current_float_value=dict(type="float", required=True)),
        ),
        boolean_configurable_param_value=dict(
            type="dict",
            options=dict(current_bool_value=dict(type="bool", required=True)),
        ),
        string_configurable_param_value=dict(
            type="dict",
            options=dict(current_str_value=dict(type="str", required=True)),
        ),
    )


def _configurable_parameter_spec():
    return dict(
        name=dict(type="str", required=True),
        param_value=dict(
            type="dict",
            required=True,
            options=_param_value_spec(),
            obj={
                "int_configurable_param_value": sdk.IntConfigurableParamValue,
                "float_configurable_param_value": sdk.FloatConfigurableParamValue,
                "boolean_configurable_param_value": sdk.BooleanConfigurableParamValue,
                "string_configurable_param_value": sdk.StringConfigurableParamValue,
            },
            mutually_exclusive=[list(PARAM_VALUE_KEYS)],
            required_one_of=[list(PARAM_VALUE_KEYS)],
        ),
    )


def _severity_config_spec():
    return dict(
        state=dict(type="str", choices=PROPERTY_STATE_CHOICES),
        threshold_parameters=dict(
            type="list",
            elements="dict",
            options=_configurable_parameter_spec(),
            obj=sdk.AlertPolicyConfigurableParameter,
        ),
    )


def get_module_spec():
    alert_config_spec = dict(
        auto_resolve=dict(type="str", choices=PROPERTY_STATE_CHOICES),
        critical_severity=dict(
            type="dict",
            options=_severity_config_spec(),
            obj=sdk.SeverityConfig,
        ),
        warning_severity=dict(
            type="dict",
            options=_severity_config_spec(),
            obj=sdk.SeverityConfig,
        ),
        info_severity=dict(
            type="dict",
            options=_severity_config_spec(),
            obj=sdk.SeverityConfig,
        ),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        system_defined_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        is_enabled=dict(type="bool"),
        schedule_interval_seconds=dict(type="int"),
        configurable_parameters=dict(
            type="list",
            elements="dict",
            options=_configurable_parameter_spec(),
            obj=sdk.AlertPolicyConfigurableParameter,
        ),
        alert_config=dict(
            type="dict",
            options=alert_config_spec,
            obj=sdk.AlertConfig,
        ),
    )
    return module_args


def check_cluster_config_idempotency(current_spec, update_spec):
    current = strip_internal_attributes(current_spec.to_dict())
    updated = strip_internal_attributes(update_spec.to_dict())
    for field in _READ_ONLY_FIELDS:
        current.pop(field, None)
        updated.pop(field, None)
    return current == updated


def update_cluster_config(module, result, api_instance):
    policy_ext_id = module.params.get("system_defined_policy_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_cluster_config(module, api_instance, policy_ext_id, ext_id)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        module.fail_json(
            msg="Failed to get etag value from the current cluster configuration",
            **result,
        )

    sg = SpecGenerator(module)
    default_spec = copy.deepcopy(current_spec)
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for updating cluster configuration",
            **result,
        )

    strip_read_only_fields(update_spec, fields=_READ_ONLY_FIELDS)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_cluster_config_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    kwargs = {"if_match": etag_value}
    resp = None
    try:
        resp = api_instance.update_cluster_config_by_id(
            systemDefinedPolicyExtId=policy_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating cluster configuration",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        updated_config = get_cluster_config(module, api_instance, policy_ext_id, ext_id)
        result["response"] = strip_internal_attributes(updated_config.to_dict())
    result["changed"] = True


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
    api_instance = get_system_defined_policies_api_instance(module)
    update_cluster_config(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
