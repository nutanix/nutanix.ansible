#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_alert_email_configuration_info_v2
short_description: Fetch alert email configuration in Nutanix Prism Central
version_added: 2.7.0
description:
  - Fetches the configuration that is used to send alert emails.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(View Alert Email Config) -
      Required Roles: Account Owner, Administrator, Files Admin, Files Viewer, Monitoring Admin,
      Monitoring Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get alert email configuration
  nutanix.ncp.ntnx_alert_email_configuration_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
"""

RETURN = r"""
response:
  description:
    - The alert email configuration.
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

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

failed:
  description: This indicates whether the task have failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_alert_email_configuration_api_instance,
)
from ..module_utils.v4.monitoring.helpers import (  # noqa: E402
    get_alert_email_configuration,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict()

    return module_args


def get_alert_email_configuration_info(module, api_instance, result):
    resp = get_alert_email_configuration(module, api_instance)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_alert_email_configuration_api_instance(module)
    get_alert_email_configuration_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
