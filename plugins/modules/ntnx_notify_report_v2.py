#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_notify_report_v2
short_description: Notify recipients with a generated report in Nutanix Prism Central
version_added: 2.7.0
description:
    - Notify a list of recipients by email with a previously generated report.
    - The report identified by C(ext_id) is emailed to the provided C(recipients)
      in each of the requested C(recipient_formats).
    - The API is asynchronous and returns a task reference.
    - The report instance must already exist in Prism Central. Reports can be
      generated using the NCM Intelligent Operations reporting workflow.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Notify recipients with a report) -
      Required Roles: Internal Super Admin, Prism Admin, Intelligent Ops Admin, Report Instance Self Owned
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=opsmgmt)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported; the notification is triggered on invocation.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - External ID (UUID) of the previously generated report instance
              whose contents will be emailed to the recipients.
        type: str
        required: true
    recipient_formats:
        description:
            - List of report formats in which the report will be delivered to
              each recipient.
            - At least one format must be provided.
        type: list
        elements: str
        required: true
        choices:
            - PDF
            - CSV
    recipients:
        description:
            - List of recipients that should receive the report by email.
            - At least one recipient must be provided.
        type: list
        elements: dict
        required: true
        suboptions:
            email_address:
                description:
                    - Email address of the recipient.
                type: str
                required: true
            recipient_name:
                description:
                    - Display name of the recipient.
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
- name: Notify recipients with a report in PDF format
  nutanix.ncp.ntnx_notify_report_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "9a1c8dfe-9c40-4c5f-8a5e-6f0c3b0d0d75"
    recipient_formats:
      - PDF
    recipients:
      - email_address: "admin@example.com"
        recipient_name: "Admin User"
  register: result
  ignore_errors: true

- name: Notify multiple recipients with a report in PDF and CSV formats
  nutanix.ncp.ntnx_notify_report_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "9a1c8dfe-9c40-4c5f-8a5e-6f0c3b0d0d75"
    recipient_formats:
      - PDF
      - CSV
    recipients:
      - email_address: "user1@example.com"
        recipient_name: "User One"
      - email_address: "user2@example.com"
        recipient_name: "User Two"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for notifying recipients with a report.
        - Task details when C(wait) is true.
        - Task reference (containing the task C(ext_id)) when C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2026-07-21T07:31:22.147000+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T07:31:18.612000+00:00",
            "entities_affected": [
                {
                    "ext_id": "9a1c8dfe-9c40-4c5f-8a5e-6f0c3b0d0d75",
                    "name": null,
                    "rel": "opsmgmt:config:report"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:c1c6d8fa-2f26-45f4-95ef-7f42b7c0d8b1",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T07:31:22.147000+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 0,
            "operation": "NotifyReport",
            "operation_description": "Notify user with a report",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2026-07-21T07:31:18.624000+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

task_ext_id:
    description:
        - The external ID of the task created by the notify recipients action.
    returned: always
    type: str
    sample: "ZXJnb24=:c1c6d8fa-2f26-45f4-95ef-7f42b7c0d8b1"

ext_id:
    description:
        - The external ID (UUID) of the report that was notified.
    returned: always
    type: str
    sample: "9a1c8dfe-9c40-4c5f-8a5e-6f0c3b0d0d75"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while notifying recipients for report"

error:
    description:
        - This field typically holds information about errors that occurred
          during the task execution.
    returned: When an error occurs
    type: str
    sample: "Failed to generate spec for notify report"

failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.opsmgmt.api_client import get_reports_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
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


def get_module_spec():
    recipient_spec = dict(
        email_address=dict(type="str", required=True),
        recipient_name=dict(type="str", required=False),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        recipient_formats=dict(
            type="list",
            elements="str",
            required=True,
            choices=["PDF", "CSV"],
        ),
        recipients=dict(
            type="list",
            elements="dict",
            options=recipient_spec,
            required=True,
            obj=ncm_operation_base_platform_sdk.ReportingRecipient,
        ),
    )

    return module_args


def notify_report(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["recipient_formats", "recipients"])

    # Only pass body-level attributes to the spec generator. The module's
    # ``ext_id`` targets the report in the URL path, NOT the notification
    # spec's own inherited ``ext_id`` field (setting the latter would trip
    # the SDK's UUID validator for callers that don't supply a UUID).
    spec_attr = {
        "recipient_formats": module.params.get("recipient_formats"),
        "recipients": module.params.get("recipients"),
    }
    sg = SpecGenerator(module)
    default_spec = ncm_operation_base_platform_sdk.ReportNotificationSpec()
    spec, err = sg.generate_spec(obj=default_spec, attr=spec_attr)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for notify report", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.notify_report(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while notifying recipients for report",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
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
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_reports_api_instance(module)
    notify_report(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
