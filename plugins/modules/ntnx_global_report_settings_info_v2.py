#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_global_report_settings_info_v2
short_description: Fetch the global report setting for a user in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about GlobalReportSetting in Nutanix Prism Central.
  - GlobalReportSetting is a per-user singleton resource; the Nutanix v4 API only exposes a
    Get-by-user endpoint and does not offer a list, filter, or pagination API.
  - Supply C(user_ext_id) to fetch the setting owned by that user.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get the Global Report Setting) -
      Required Roles: Developer, NCM Admin, Operations Management Admin, Operations Management Viewer, Operator,
      Prism Admin, Project Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=opsmgmt)"
options:
  user_ext_id:
    description:
      - External ID (UUID) of the user whose global report setting should be fetched.
      - Maps to the C(userExtId) path parameter on the underlying v4 API.
      - Required.
    type: str
    required: true
  ext_id:
    description:
      - Optional external ID of the global report setting.
      - Included so the module can echo it back in the response for logging / assertions;
        the v4 API does not accept it as a routing parameter.
    type: str
    required: false
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
- name: Get global report setting for a user
  nutanix.ncp.ntnx_global_report_settings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    user_ext_id: "00000000-0000-0000-0000-000000000000"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC GlobalReportSetting info v4 API.
    - It contains a single GlobalReportSetting dict since C(user_ext_id) uniquely identifies the resource.
    - The v4 API does not expose a list endpoint for this entity, so a list response is not possible.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "b1b5b0c4-c8a2-4b58-9f22-2a4b7e8b9a10",
      "links": null,
      "name": "global_report_setting_ansible",
      "notification_policy": {
          "email_body": "Please find the attached reports.",
          "email_subject": "Your Nutanix reports",
          "recipient_formats": ["PDF", "CSV"],
          "recipients": [
              {
                  "email_address": "reports@example.com",
                  "recipient_name": "Reports Owner"
              }
          ]
      },
      "report_customization": {
          "css_style_sheet": "body { font-family: Arial; }",
          "footer_html": "<p>Copyright Nutanix</p>",
          "header_html": "<h1>Nutanix reports</h1>",
          "logo_image_ext_id": null
      },
      "retention_config": {
          "retention_count": 5,
          "retention_period_seconds": null
      },
      "tenant_id": null
    }

user_ext_id:
  description: User external ID whose global report setting was fetched.
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"

ext_id:
  description: External ID of the fetched global report setting.
  type: str
  returned: when the API returns an ext_id in the response
  sample: "b1b5b0c4-c8a2-4b58-9f22-2a4b7e8b9a10"

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching global report setting for user ext_id"

error:
  description: Error information if any error occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: Whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.opsmgmt.api_client import (  # noqa: E402
    get_global_report_setting_api_instance,
)
from ..module_utils.v4.opsmgmt.helpers import get_global_report_setting  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """
    Build the argument spec for the info module.

    GlobalReportSetting is a per-user singleton, so the only routing key we
    expose is ``user_ext_id``. ``ext_id`` is optional and only echoed back in
    the module response for callers that want to assert on it.
    """
    module_args = dict(
        user_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_global_report_setting_using_user_ext_id(module, api_instance, result):
    """
    Fetch the setting for ``user_ext_id`` and populate ``result``.

    The helper strips SDK internal attributes so callers get a clean dict
    suitable for assertions. When the API returns an ``ext_id`` on the entity
    it is copied to the top-level result for convenience.
    """
    user_ext_id = module.params.get("user_ext_id")
    resp = get_global_report_setting(module, api_instance, user_ext_id)
    data = resp.data
    result["user_ext_id"] = user_ext_id
    if getattr(data, "ext_id", None):
        result["ext_id"] = data.ext_id
    result["response"] = strip_internal_attributes(data.to_dict())


def run_module():
    """
    Ansible info-module entry-point.
    """
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "user_ext_id": None,
    }
    api_instance = get_global_report_setting_api_instance(module)
    get_global_report_setting_using_user_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
