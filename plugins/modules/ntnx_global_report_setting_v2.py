#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_global_report_setting_v2
short_description: Update the global report setting for a user in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to update the global report setting for a user in Nutanix Prism Central.
  - C(GlobalReportSetting) is a per-user singleton that is always present for a given user.
  - The Nutanix v4 API only exposes Get and Update (PUT) for this resource, so this module supports
    C(state=present) only and always issues an idempotent update against the setting owned by the
    supplied C(user_ext_id).
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Update the Global Report Setting) -
      Required Roles: NCM Admin, Operations Management Admin, Prism Admin, Project Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=opsmgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) the module will update the global report setting
        owned by C(user_ext_id) using the supplied fields.
      - C(state=absent) is not supported for this resource because the underlying v4 API does
        not expose a delete operation for the per-user global report setting.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the global report setting itself.
      - Optional; when supplied the module will confirm the fetched setting matches and use it
        for logging in the response.
      - The v4 API does not use this value to route the request — the setting is identified by
        C(user_ext_id).
    type: str
    required: false
  user_ext_id:
    description:
      - External ID (UUID) of the user whose global report setting is being updated.
      - This maps to the C(userExtId) path parameter on the underlying v4 API.
      - Required for all operations.
    type: str
    required: true
  name:
    description:
      - Name of the global report setting.
      - Must be between 1 and 64 characters.
      - Required for update operation.
    type: str
    required: false
  retention_config:
    description:
      - Defines how long generated reports should be retained.
      - Only one of C(retention_period_seconds) and C(retention_count) should be specified.
    type: dict
    required: false
    suboptions:
      retention_period_seconds:
        description:
          - Retention period in seconds for the generated reports.
        type: int
        required: false
      retention_count:
        description:
          - Number of most-recent reports to retain per report configuration.
        type: int
        required: false
  notification_policy:
    description:
      - Notification policy applied when generated reports are emailed to recipients.
    type: dict
    required: false
    suboptions:
      recipients:
        description:
          - List of recipients that should receive the report email.
          - Required inside C(notification_policy) whenever it is supplied.
        type: list
        elements: dict
        required: false
        suboptions:
          email_address:
            description:
              - Email address of the recipient.
            type: str
            required: true
          recipient_name:
            description:
              - Display name for the recipient. Maximum 64 characters.
            type: str
            required: false
      recipient_formats:
        description:
          - Formats in which the report is attached to the notification email.
        type: list
        elements: str
        required: false
        choices:
          - PDF
          - CSV
      email_subject:
        description:
          - Subject of the notification email. Maximum 100 characters.
        type: str
        required: false
      email_body:
        description:
          - Body of the notification email. Maximum 1000 characters.
        type: str
        required: false
  report_customization:
    description:
      - Report-level customizations (branding, styling, logo).
    type: dict
    required: false
    suboptions:
      header_html:
        description:
          - Custom header HTML applied to the report.
        type: str
        required: false
      footer_html:
        description:
          - Custom footer HTML applied to the report.
        type: str
        required: false
      css_style_sheet:
        description:
          - Global cascading style sheet applied to the report.
        type: str
        required: false
      logo_image_ext_id:
        description:
          - External ID of an uploaded C(ReportArtifact) that should be used as the report logo.
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
- name: Update global report setting for a user
  nutanix.ncp.ntnx_global_report_setting_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    user_ext_id: "00000000-0000-0000-0000-000000000000"
    name: "global_report_setting_ansible"
    retention_config:
      retention_count: 5
    notification_policy:
      recipients:
        - email_address: "reports@example.com"
          recipient_name: "Reports Owner"
      recipient_formats:
        - PDF
        - CSV
      email_subject: "Your Nutanix reports"
      email_body: "Please find the attached reports."
    report_customization:
      header_html: "<h1>Nutanix reports</h1>"
      footer_html: "<p>Copyright Nutanix</p>"
      css_style_sheet: "body { font-family: Arial; }"
  register: result
  ignore_errors: true

- name: Reset the global report setting to a minimal configuration
  nutanix.ncp.ntnx_global_report_setting_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    user_ext_id: "00000000-0000-0000-0000-000000000000"
    name: "global_report_setting_reset"
    retention_config:
      retention_period_seconds: 604800
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating the global report setting.
    - If the operation is update and C(wait) is true, the module will re-fetch and return the
      updated global report setting details.
    - If C(wait) is false, the module will return the task response captured immediately after
      the update was submitted.
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

task_ext_id:
  description:
    - The external ID of the task.
    - The Update API for GlobalReportSetting is synchronous, so this field is typically null.
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the global report setting.
  returned: always
  type: str
  sample: "b1b5b0c4-c8a2-4b58-9f22-2a4b7e8b9a10"

user_ext_id:
  description:
    - External ID of the user whose global report setting was updated.
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency.
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
  description:
    - Human-readable status message.
    - Populated when the module is idempotent, when C(state=absent) is requested (which is
      unsupported), or when an error occurs.
  returned: When there is an error, module is idempotent, or an unsupported state is requested
  type: str
  sample: "GlobalReportSetting with name 'global_report_setting_ansible' already matches the desired state. Skipping update."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.opsmgmt.api_client import (  # noqa: E402
    get_etag,
    get_global_report_setting_api_instance,
)
from ..module_utils.v4.opsmgmt.helpers import get_global_report_setting  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_opsmgmt_py_client as ncm_operation_base_platform_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as ncm_operation_base_platform_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Attributes populated by the platform that must not be included in the update body.
_READ_ONLY_FIELDS = ("links", "tenant_id")


def get_module_spec():
    """
    Build and return the Ansible argument spec for the CRUD module.

    Field mapping and validation constraints mirror the v4 SDK model
    :class:`ntnx_opsmgmt_py_client.GlobalReportSetting` and its nested models
    (``RetentionConfig``, ``NotificationPolicy``, ``ReportCustomization``).
    ``name`` is the only strictly required attribute per the SDK, but is
    marked optional here because it is only required for the update path and
    is validated at runtime via :func:`validate_required_params`.
    """
    recipient_spec = dict(
        email_address=dict(type="str", required=True),
        recipient_name=dict(type="str", required=False),
    )

    notification_policy_spec = dict(
        recipients=dict(
            type="list",
            elements="dict",
            options=recipient_spec,
            required=False,
            obj=ncm_operation_base_platform_sdk.ConfigRecipient,
        ),
        recipient_formats=dict(
            type="list",
            elements="str",
            required=False,
            choices=["PDF", "CSV"],
        ),
        email_subject=dict(type="str", required=False),
        email_body=dict(type="str", required=False),
    )

    retention_config_spec = dict(
        retention_period_seconds=dict(type="int", required=False),
        retention_count=dict(type="int", required=False),
    )

    report_customization_spec = dict(
        header_html=dict(type="str", required=False),
        footer_html=dict(type="str", required=False),
        css_style_sheet=dict(type="str", required=False),
        logo_image_ext_id=dict(type="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        user_ext_id=dict(type="str", required=True),
        name=dict(type="str", required=False),
        retention_config=dict(
            type="dict",
            options=retention_config_spec,
            required=False,
            obj=ncm_operation_base_platform_sdk.RetentionConfig,
        ),
        notification_policy=dict(
            type="dict",
            options=notification_policy_spec,
            required=False,
            obj=ncm_operation_base_platform_sdk.ConfigNotificationPolicy,
        ),
        report_customization=dict(
            type="dict",
            options=report_customization_spec,
            required=False,
            obj=ncm_operation_base_platform_sdk.ConfigReportCustomization,
        ),
    )
    return module_args


def _check_for_idempotency(old_spec_dict, update_spec_dict):
    """
    Return True when the current and desired specs describe the same setting.

    Internal / server-only attributes are stripped from both sides before the
    comparison so fields such as ``$reserved`` and read-only bookkeeping do
    not create false diffs. Used by :func:`update_global_report_setting` to
    short-circuit the update call when nothing would actually change.
    """
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    for field in _READ_ONLY_FIELDS:
        old_spec_dict.pop(field, None)
        update_spec_dict.pop(field, None)
    return old_spec_dict == update_spec_dict


def update_global_report_setting(module, api_instance, result):
    """
    Update the per-user global report setting.

    Fetches the existing setting for ``user_ext_id``, applies the fields
    supplied by the caller on top of that spec, and issues the SDK Update
    (PUT) call. The current ETag is passed as ``if_match`` to satisfy the
    API's optimistic concurrency requirement. On check mode the module
    returns the fully-populated spec without contacting the server; on real
    runs it re-fetches the setting after the update so callers see the
    canonical server-side state.
    """
    validate_required_params(module, ["user_ext_id", "name"])
    user_ext_id = module.params.get("user_ext_id")
    result["user_ext_id"] = user_ext_id

    current_resp = get_global_report_setting(module, api_instance, user_ext_id)
    old_spec = current_resp.data
    etag = get_etag(data=old_spec)
    if not etag:
        module.fail_json(
            msg=(
                "Unable to fetch etag for updating global report setting "
                "for user ext_id: {0}".format(user_ext_id)
            ),
            **result,
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update global report setting spec", **result
        )

    if update_spec.ext_id:
        result["ext_id"] = update_spec.ext_id

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if _check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(old_spec.to_dict())
        module.exit_json(
            msg=(
                "GlobalReportSetting with name '{0}' already matches the "
                "desired state. Skipping update.".format(module.params.get("name"))
            ),
            **result,
        )

    strip_read_only_fields(update_spec, _READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_global_report_setting(
            userExtId=user_ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating global report setting",
        )

    # The Update API is synchronous and returns the updated entity directly.
    if resp is not None and getattr(resp, "data", None) is not None:
        data = resp.data
        result["response"] = strip_internal_attributes(data.to_dict())
        if getattr(data, "ext_id", None):
            result["ext_id"] = data.ext_id

    # Re-fetch to guarantee the caller sees the canonical server state.
    if module.params.get("wait"):
        refreshed = get_global_report_setting(module, api_instance, user_ext_id)
        result["response"] = strip_internal_attributes(refreshed.data.to_dict())
        if getattr(refreshed.data, "ext_id", None):
            result["ext_id"] = refreshed.data.ext_id

    result["changed"] = True


def run_module():
    """
    Ansible module entry-point.

    Builds the CRUD module, validates SDK availability, dispatches on
    ``state``, and returns the aggregate result. Only ``state=present`` is
    supported for GlobalReportSetting; ``state=absent`` fails with a clear
    message because the underlying v4 API has no delete operation.
    """
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_opsmgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "user_ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }
    api_instance = get_global_report_setting_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        update_global_report_setting(module, api_instance, result)
    else:
        module.fail_json(
            msg=(
                "state=absent is not supported for GlobalReportSetting; the "
                "v4 API only exposes Get and Update. Use state=present with "
                "the desired values to modify the setting."
            ),
            **result,
        )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
