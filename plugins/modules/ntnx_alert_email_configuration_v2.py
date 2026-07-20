#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_alert_email_configuration_v2
short_description: Update the alert email configuration in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to update the alert email configuration in Nutanix Prism Central.
  - The alert email configuration is a singleton entity per Prism Central instance.
  - Only the update operation is supported by the underlying v4 SDK API
    (there is no create or delete for this configuration).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update the alert email configuration) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  state:
    description:
      - If C(state) is set to C(present) the operation will be update the alert email configuration.
      - The alert email configuration is a singleton entity; therefore C(state=absent) is not supported
        by the underlying v4 API and this module will fail the task if it is used.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the alert email configuration.
      - The alert email configuration is a singleton entity, hence C(ext_id) is optional.
      - When provided, it is used for logging and for updating the specific instance.
    type: str
    required: false
  is_enabled:
    description:
      - Indicates whether the alert email configuration is enabled or not.
      - When C(true) alert emails are sent for the generated alerts.
    type: bool
    required: false
  default_nutanix_email:
    description:
      - The default Nutanix email ID to which alert emails are sent (for example C(nos-alerts@nutanix.com)).
    type: str
    required: false
  has_default_nutanix_email:
    description:
      - Indicates whether the default Nutanix email is set for sending the alert emails or not.
    type: bool
    required: false
  is_email_digest_enabled:
    description:
      - Indicates whether the email digest (a periodic summary email of alerts) is enabled or not.
    type: bool
    required: false
  is_empty_alert_email_digest_skipped:
    description:
      - Indicates whether the empty alert email digest is skipped or not.
      - When C(true) no digest email is sent when there are no alerts to summarize.
    type: bool
    required: false
  email_contact_list:
    description:
      - The global list of email addresses (recipients) to which alert emails are sent.
    type: list
    elements: str
    required: false
  alert_email_digest_send_time:
    description:
      - The time of the day (in C(HH:mm) 24-hour format) at which the alert email digest is sent.
    type: str
    required: false
  alert_email_digest_send_timezone:
    description:
      - The timezone used for the alert email digest send time (for example C(UTC) or C(America/Los_Angeles)).
    type: str
    required: false
  email_template:
    description:
      - The email template used for the alert emails.
    type: dict
    required: false
    suboptions:
      subject_prefix:
        description:
          - Prefix for the email subject line.
        type: str
        required: false
      body_suffix:
        description:
          - Suffix appended to the email body content.
        type: str
        required: false
  email_config_rules:
    description:
      - The list of email configuration rules used to send targeted alert emails
        to specific recipients based on filter criteria (cluster, severity, impact type, etc.).
    type: list
    elements: dict
    required: false
    suboptions:
      is_enabled:
        description:
          - Indicates whether this email configuration rule is enabled or not.
        type: bool
        required: false
      has_global_email_contact_list:
        description:
          - Indicates whether the global email contact list is applied for this rule
            in addition to the rule-specific recipients.
        type: bool
        required: false
      cluster_uuids:
        description:
          - The list of cluster UUIDs to which this rule applies.
        type: list
        elements: str
        required: false
      impact_types:
        description:
          - The list of impact types for which alert emails should be sent for this rule.
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
        required: false
      severities:
        description:
          - The list of severities for which alert emails should be sent for this rule.
        type: list
        elements: str
        choices:
          - CRITICAL
          - WARNING
          - INFO
        required: false
      match_phrases:
        description:
          - The list of match phrases used to filter alerts for this rule.
          - Only alerts whose title contains one of these phrases will trigger emails for this rule.
        type: list
        elements: str
        required: false
      recipients:
        description:
          - The list of email addresses (recipients) to which alert emails for this rule are sent.
        type: list
        elements: str
        required: false
  tunnel_details:
    description:
      - Remote tunnel details associated with the alert email configuration.
      - Used when alert emails are relayed through a Nutanix service center via a remote tunnel.
    type: dict
    required: false
    suboptions:
      http_proxy:
        description:
          - HTTP proxy used to establish the remote tunnel.
        type: dict
        required: false
        suboptions:
          name:
            description:
              - Proxy name.
            type: str
            required: false
          port:
            description:
              - Proxy port.
            type: int
            required: false
          username:
            description:
              - Username used to authenticate with the proxy.
            type: str
            required: false
          password:
            description:
              - Password used to authenticate with the proxy.
              - This value is treated as sensitive and is not logged.
            type: str
            required: false
          proxy_types:
            description:
              - List of proxy types supported by this proxy.
            type: list
            elements: str
            choices:
              - HTTP
              - HTTPS
              - SOCKS
            required: false
          address_value:
            description:
              - The IPv4 / IPv6 address or FQDN of the proxy host.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address of the proxy host.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the IPv4 address.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description:
                  - IPv6 address of the proxy host.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the IPv6 address.
                    type: int
                    required: false
                    default: 128
              fqdn:
                description:
                  - Fully qualified domain name of the proxy host.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The FQDN value.
                    type: str
                    required: true
      service_center:
        description:
          - Service center to which the remote tunnel is connected at Nutanix's end.
        type: dict
        required: false
        suboptions:
          name:
            description:
              - Name of the service center.
            type: str
            required: false
          ip_address:
            description:
              - IP address of the service center.
            type: str
            required: false
          username:
            description:
              - Username used to authenticate with the service center.
            type: str
            required: false
          port:
            description:
              - Port used to connect to the service center.
            type: int
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
- name: Update alert email configuration (enable email + digest, set global contact list)
  nutanix.ncp.ntnx_alert_email_configuration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    is_enabled: true
    default_nutanix_email: "nos-alerts@nutanix.com"
    has_default_nutanix_email: true
    is_email_digest_enabled: true
    is_empty_alert_email_digest_skipped: true
    email_contact_list:
      - "sre-team@example.com"
      - "platform-oncall@example.com"
    alert_email_digest_send_time: "09:00"
    alert_email_digest_send_timezone: "UTC"
    email_template:
      subject_prefix: "[Nutanix Alerts]"
      body_suffix: "Please contact SRE if you have any questions."
    email_config_rules:
      - is_enabled: true
        has_global_email_contact_list: true
        cluster_uuids:
          - "0005f7f7-a5e6-1234-0000-000000012345"
        impact_types:
          - AVAILABILITY
          - CAPACITY
        severities:
          - CRITICAL
          - WARNING
        match_phrases:
          - "Storage"
        recipients:
          - "storage-oncall@example.com"
  register: result
  ignore_errors: true

- name: Disable alert email digest and clear the global contact list
  nutanix.ncp.ntnx_alert_email_configuration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    is_email_digest_enabled: false
    email_contact_list: []
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating the alert email configuration.
    - Contains the full alert email configuration as returned by the API after the update.
  returned: always
  type: dict
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

task_ext_id:
  description:
    - The external ID of the task.
    - Since the AlertEmailConfiguration update is a synchronous API and does not create a task,
      this value is typically C(None).
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the alert email configuration.
    - The alert email configuration is a singleton and typically does not carry an external ID.
  returned: always
  type: str
  sample: null

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (e.g. due to idempotency).
  returned: always
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
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent, or check mode is used.
  type: str
  sample: "Api Exception raised while updating alert email configuration"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

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
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_monitoring_py_client as monitoring_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as monitoring_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )

    ip_address_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=monitoring_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=monitoring_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            required=False,
            obj=monitoring_sdk.FQDN,
        ),
    )

    http_proxy_spec = dict(
        name=dict(type="str", required=False),
        port=dict(type="int", required=False),
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
        proxy_types=dict(
            type="list",
            elements="str",
            choices=["HTTP", "HTTPS", "SOCKS"],
            required=False,
        ),
        address_value=dict(
            type="dict",
            options=ip_address_or_fqdn_spec,
            required=False,
            obj=monitoring_sdk.IPAddressOrFQDN,
        ),
    )

    service_center_spec = dict(
        name=dict(type="str", required=False),
        ip_address=dict(type="str", required=False),
        username=dict(type="str", required=False),
        port=dict(type="int", required=False),
    )

    tunnel_details_spec = dict(
        http_proxy=dict(
            type="dict",
            options=http_proxy_spec,
            required=False,
            obj=monitoring_sdk.HttpProxy,
        ),
        service_center=dict(
            type="dict",
            options=service_center_spec,
            required=False,
            obj=monitoring_sdk.ServiceCenter,
        ),
    )

    email_template_spec = dict(
        subject_prefix=dict(type="str", required=False),
        body_suffix=dict(type="str", required=False),
    )

    email_config_rule_spec = dict(
        is_enabled=dict(type="bool", required=False),
        has_global_email_contact_list=dict(type="bool", required=False),
        cluster_uuids=dict(type="list", elements="str", required=False),
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
            required=False,
        ),
        severities=dict(
            type="list",
            elements="str",
            choices=["CRITICAL", "WARNING", "INFO"],
            required=False,
        ),
        match_phrases=dict(type="list", elements="str", required=False),
        recipients=dict(type="list", elements="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        is_enabled=dict(type="bool", required=False),
        default_nutanix_email=dict(type="str", required=False),
        has_default_nutanix_email=dict(type="bool", required=False),
        is_email_digest_enabled=dict(type="bool", required=False),
        is_empty_alert_email_digest_skipped=dict(type="bool", required=False),
        email_contact_list=dict(type="list", elements="str", required=False),
        alert_email_digest_send_time=dict(type="str", required=False),
        alert_email_digest_send_timezone=dict(type="str", required=False),
        email_template=dict(
            type="dict",
            options=email_template_spec,
            required=False,
            obj=monitoring_sdk.EmailTemplate,
        ),
        email_config_rules=dict(
            type="list",
            elements="dict",
            options=email_config_rule_spec,
            required=False,
            obj=monitoring_sdk.EmailConfigurationRule,
        ),
        tunnel_details=dict(
            type="dict",
            options=tunnel_details_spec,
            required=False,
            obj=monitoring_sdk.RemoteTunnelDetails,
        ),
    )
    return module_args


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """Compare old vs new spec dicts to determine if an update is needed."""
    old = strip_internal_attributes(deepcopy(old_spec_dict))
    new = strip_internal_attributes(deepcopy(update_spec_dict))
    return old == new


def update_AlertEmailConfiguration(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    if ext_id:
        result["ext_id"] = ext_id

    old_spec = get_alert_email_configuration(module, api_instance)
    etag = get_etag(data=old_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update alert email configuration spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(old_spec.to_dict())
        module.exit_json(
            msg="Nothing to change. Alert email configuration is already up to date.",
            **result,
        )

    # Blank server-populated read-only fields on the tunnel details before
    # sending the update body. If the user did not supply ``tunnel_details``
    # at all, drop the whole block — the server-provided value can contain
    # e.g. an FQDN in ``service_center.ip_address`` that fails the update
    # schema validation.
    if module.params.get("tunnel_details") is None:
        try:
            update_spec.tunnel_details = None
        except AttributeError:
            pass
    elif getattr(update_spec, "tunnel_details", None) is not None:
        try:
            update_spec.tunnel_details.connection_status = None
            update_spec.tunnel_details.transport_status = None
        except AttributeError:
            pass

    try:
        api_instance.update_alert_email_configuration(body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating alert email configuration",
        )

    # Refetch the config to return the authoritative post-update state; the
    # update API's ``data`` field is a discriminated union (list of app
    # messages, error response, or empty) rather than the entity itself.
    new_spec = get_alert_email_configuration(module, api_instance)
    result["response"] = strip_internal_attributes(new_spec.to_dict())
    result["changed"] = True


def delete_AlertEmailConfiguration(module, result, api_instance):
    module.fail_json(
        msg=(
            "state=absent is not supported for alert email configuration: "
            "the underlying v4 API does not expose a delete operation for this singleton resource."
        ),
        **result,
    )


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
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }
    api_instance = get_alert_email_configuration_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        update_AlertEmailConfiguration(module, result, api_instance)
    else:
        delete_AlertEmailConfiguration(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
