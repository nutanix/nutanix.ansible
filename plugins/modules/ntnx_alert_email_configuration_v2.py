#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_alert_email_configuration_v2
short_description: Update alert email configuration in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Updates alert email configuration.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update Alert Email Config) -
      Required Roles: Account Owner, Administrator, Files Admin, Monitoring Admin, Prism Admin, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will update the alert email configuration.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    default_nutanix_email:
        description:
            - The default Nutanix email ID to which alert emails are sent.
        type: str
    is_enabled:
        description:
            - Indicates whether alert emails are enabled or not.
        type: bool
    has_default_nutanix_email:
        description:
            - Indicates whether alert emails are enabled or not on default Nutanix email ID.
        type: bool
    is_email_digest_enabled:
        description:
            - Indicates whether alert email digest is enabled or not.
        type: bool
    is_empty_alert_email_digest_skipped:
        description:
            - Send alert email digest only if there are one or more alerts.
        type: bool
    email_config_rules:
        description:
            - Rules for email configuration.
        type: list
        elements: dict
        suboptions:
            cluster_uuids:
                description:
                    - Cluster UUIDs to which this rule applies.
                type: list
                elements: str
            impact_types:
                description:
                    - The impact this alert or event will have on the system. For example,
                      availability, performance, or capacity.
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
            has_global_email_contact_list:
                description:
                    - Indicates whether to include a global email contact list.
                type: bool
            match_phrases:
                description:
                    - List of phrases to match the alert.
                type: list
                elements: str
            recipients:
                description:
                    - List of recipients who will receive emails.
                type: list
                elements: str
            severities:
                description:
                    - Severity of an alert.
                type: list
                elements: str
                choices:
                    - INFO
                    - WARNING
                    - CRITICAL
            is_enabled:
                description:
                    - Indicates whether the configuration rule is enabled or not.
                type: bool
    email_contact_list:
        description:
            - List of email contacts.
        type: list
        elements: str
    email_template:
        description:
            - Email template.
        type: dict
        suboptions:
            body_suffix:
                description:
                    - Suffix for the email body.
                type: str
            subject_prefix:
                description:
                    - Prefix for the email subject.
                type: str
    alert_email_digest_send_time:
        description:
            - Time in HH:mm format when the alert email digest is sent daily.
        type: str
    alert_email_digest_send_timezone:
        description:
            - Timezone for the time at which the alert email digest is sent daily.
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
- name: Update alert email configuration
  nutanix.ncp.ntnx_alert_email_configuration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    is_enabled: true
    has_default_nutanix_email: false
    is_email_digest_enabled: true
    email_contact_list:
      - alerts@example.com
    email_template:
      subject_prefix: "URGENT: Immediate Action Required"
      body_suffix: "Sent from example.com"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for updating alert email configuration.
        - If C(wait) is false, the response will be the initial task details.
        - If C(wait) is true, the response will be the email configuration details after the update operation.
    type: dict
    returned: always
    sample:
        {
        "alert_email_digest_send_time": "09:00",
        "alert_email_digest_send_timezone": "UTC",
        "default_nutanix_email": "nos-alerts@nutanix.com",
        "email_config_rules": [
            {
                "cluster_uuids": null,
                "has_global_email_contact_list": true,
                "impact_types": [
                    "AVAILABILITY",
                    "CAPACITY"
                ],
                "is_enabled": true,
                "match_phrases": [
                    "Storage"
                ],
                "recipients": [
                    "storage-oncall@example.com"
                ],
                "severities": [
                    "CRITICAL",
                    "WARNING"
                ]
            }
        ],
        "email_contact_list": [
            "sre-team@example.com",
            "platform-oncall@example.com"
        ],
        "email_template": {
            "body_suffix": "Please contact SRE if you have any questions.",
            "subject_prefix": "[Nutanix Alerts]"
        },
        "ext_id": null,
        "has_default_nutanix_email": false,
        "is_email_digest_enabled": true,
        "is_empty_alert_email_digest_skipped": true,
        "is_enabled": true,
        "links": null,
        "tenant_id": null,
        "tunnel_details": {
            "connection_status": {
                "last_changed_time": null,
                "last_checked_time": "1970-01-01T00:00:00+00:00",
                "last_successful_transmission_time": "2026-07-20T15:13:31.191422+00:00",
                "message": null,
                "status": "SUCCESS"
            },
            "http_proxy": null,
            "service_center": {
                "ip_address": "nsc02.nutanix.net",
                "name": null,
                "port": 0,
                "username": null
            },
            "transport_status": {
                "last_changed_time": null,
                "last_checked_time": "2026-07-20T15:14:24.673147+00:00",
                "last_successful_transmission_time": "2026-07-20T15:14:24.673145+00:00",
                "message": null,
                "status": "SUCCESS"
            }
        }
    }
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
    get_alert_email_configuration_api_instance,
    get_etag,
)
from ..module_utils.v4.monitoring.helpers import (  # noqa: E402
    get_alert_email_configuration,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    strip_users_empty_attributes,
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
    "tunnel_details",
)

IMPACT_TYPE_CHOICES = [
    "AVAILABILITY",
    "CAPACITY",
    "CONFIGURATION",
    "PERFORMANCE",
    "SYSTEM_INDICATOR",
    "CPU_CAPACITY",
    "MEMORY_CAPACITY",
    "STORAGE_CAPACITY",
]
SEVERITY_CHOICES = ["INFO", "WARNING", "CRITICAL"]


def get_module_spec():
    email_config_rule_spec = dict(
        cluster_uuids=dict(type="list", elements="str"),
        impact_types=dict(
            type="list",
            elements="str",
            choices=IMPACT_TYPE_CHOICES,
        ),
        has_global_email_contact_list=dict(type="bool"),
        match_phrases=dict(type="list", elements="str"),
        recipients=dict(type="list", elements="str"),
        severities=dict(
            type="list",
            elements="str",
            choices=SEVERITY_CHOICES,
        ),
        is_enabled=dict(type="bool"),
    )
    email_template_spec = dict(
        body_suffix=dict(type="str"),
        subject_prefix=dict(type="str"),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        default_nutanix_email=dict(type="str"),
        is_enabled=dict(type="bool"),
        has_default_nutanix_email=dict(type="bool"),
        is_email_digest_enabled=dict(type="bool"),
        is_empty_alert_email_digest_skipped=dict(type="bool"),
        email_config_rules=dict(
            type="list",
            elements="dict",
            options=email_config_rule_spec,
            obj=sdk.EmailConfigurationRule,
        ),
        email_contact_list=dict(type="list", elements="str"),
        email_template=dict(
            type="dict",
            options=email_template_spec,
            obj=sdk.EmailTemplate,
        ),
        alert_email_digest_send_time=dict(type="str"),
        alert_email_digest_send_timezone=dict(type="str"),
    )
    return module_args


def check_alert_email_configuration_idempotency(current_spec, update_spec):
    current = strip_internal_attributes(current_spec.to_dict())
    updated = strip_internal_attributes(update_spec.to_dict())
    for field in _READ_ONLY_FIELDS:
        current.pop(field, None)
        updated.pop(field, None)
    return current == updated


def update_alert_email_configuration(module, result, api_instance):
    current_spec = get_alert_email_configuration(module, api_instance)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        module.fail_json(
            msg="Failed to get etag value from the current alert email configuration",
            **result,
        )

    strip_users_empty_attributes(current_spec)

    sg = SpecGenerator(module)
    default_spec = copy.deepcopy(current_spec)
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for updating alert email configuration",
            **result,
        )

    strip_read_only_fields(update_spec, fields=_READ_ONLY_FIELDS)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_alert_email_configuration_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    kwargs = {"if_match": etag_value}
    try:
        resp = api_instance.update_alert_email_configuration(body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating alert email configuration",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        fetched = get_alert_email_configuration(module, api_instance)
        result["response"] = strip_internal_attributes(fetched.to_dict())
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
    api_instance = get_alert_email_configuration_api_instance(module)
    update_alert_email_configuration(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
