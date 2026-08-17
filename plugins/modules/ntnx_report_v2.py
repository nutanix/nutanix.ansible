#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_report_v2
short_description: Generate and delete Report instances in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to generate (create) and delete Report instances in Nutanix Prism Central.
  - A Report is a rendered instance produced from an existing Report Configuration
    (a schedule/template registered under the opsmgmt v4 reporting service).
  - Report generation is asynchronous - the API returns a task reference and the
    module waits for the task to complete when C(wait) is true.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires an existing Report Configuration (C(config_ext_id))
      before a report instance can be generated. Create the configuration through
      the opsmgmt report configuration APIs first.
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Generate a Report) -
      Required Roles: NCM Admin, Intelligent Ops Admin, Operations Management Admin,
      Prism Admin, Super Admin.
    - >-
      B(Delete a Report) -
      Required Roles: NCM Admin, Intelligent Ops Admin, Operations Management Admin,
      Prism Admin, Super Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=opsmgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation
        will generate (create) a new report instance.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation
        will delete the report instance.
      - Report instances are immutable once generated; the update path is not supported.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the report instance.
      - Required for delete operation.
      - Must NOT be provided for create/generate operation.
    type: str
    required: false
  name:
    description:
      - Name assigned to the generated report instance.
      - Required for create operation.
      - Minimum 2 characters, maximum 100 characters.
    type: str
    required: false
  description:
    description:
      - Description of the generated report instance.
    type: str
    required: false
  config_ext_id:
    description:
      - External ID (UUID) of the Report Configuration to run.
      - The configuration determines the report contents (sections, widgets, filters).
      - Required for create operation.
      - Must be a valid UUID matching pattern
        C(/^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$/).
    type: str
    required: false
  start_time:
    description:
      - Inclusive start timestamp of the reporting window.
      - Required for create operation.
      - Must be provided as an ISO-8601 timestamp string, e.g. "2026-01-01T00:00:00Z".
    type: str
    required: false
  end_time:
    description:
      - Inclusive end timestamp of the reporting window.
      - Required for create operation.
      - Must be provided as an ISO-8601 timestamp string, e.g. "2026-01-31T23:59:59Z".
    type: str
    required: false
  is_persistent:
    description:
      - Whether the generated report should be persisted in blob storage
        (Cassandra/ChakrDB) so it can be downloaded/notified later.
      - Non-persistent reports are transient and only useful for immediate delivery.
    type: bool
    required: false
  timezone:
    description:
      - Timezone used to render timestamps and schedule the report window
        (e.g. "UTC", "America/Los_Angeles").
    type: str
    required: false
  owner_ext_id:
    description:
      - External ID (UUID) of the user who owns the generated report instance.
      - Used to attribute the report to a specific user for RBAC and quota purposes.
    type: str
    required: false
  override_supported_formats:
    description:
      - Optional list of report formats to generate for this run, overriding the
        formats declared on the underlying Report Configuration.
    type: list
    elements: str
    choices:
      - PDF
      - CSV
    required: false
  recipient_formats:
    description:
      - List of report formats to attach when notifying recipients.
      - Only meaningful when C(recipients) is provided.
    type: list
    elements: str
    choices:
      - PDF
      - CSV
    required: false
  recipients:
    description:
      - List of recipients to notify with the generated report.
    type: list
    elements: dict
    required: false
    suboptions:
      email_address:
        description:
          - Recipient's email address. Required when a recipient entry is
            provided.
        type: str
        required: true
      recipient_name:
        description:
          - Human-readable name of the recipient (e.g. "Ops Team Lead").
        type: str
        required: false
  entity_selection:
    description:
      - Scope of entities the report is generated for.
      - When omitted, the underlying Report Configuration's default scope is used.
    type: dict
    required: false
    suboptions:
      entity_type:
        description:
          - Type of entity the report will be generated for.
        type: str
        required: true
        choices:
          - VM
          - CLUSTER
          - HOST
          - CATEGORY
          - CONTAINER
          - DISK
          - VIRTUAL_DISK
          - VOLUME_GROUPS
          - ALERT
          - AUDIT
          - EVENT
          - CONFIG
          - PLAYBOOK
          - RECOVERY_PLAN_JOB
          - STIG_STATS
          - VCENTER_CLUSTER
          - VCENTER_DATASTORE
          - VCENTER_HOST
          - VCENTER_VM
          - VULNERABILITY
      entity_ext_id:
        description:
          - List of specific entity UUIDs of the selected C(entity_type) that the
            report should cover.
          - When omitted, the report covers all entities of the given type visible
            to the caller.
        type: list
        elements: str
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
- name: Generate a report with minimum required fields
  nutanix.ncp.ntnx_report_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "vm_efficiency_report"
    config_ext_id: "aaaaaaaa-1111-2222-3333-444444444444"
    start_time: "2026-01-01T00:00:00Z"
    end_time: "2026-01-31T23:59:59Z"
  register: result
  ignore_errors: true

- name: Generate a report with all attributes (recipients + persistence)
  nutanix.ncp.ntnx_report_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "monthly_vm_report_full"
    description: "Monthly VM efficiency report generated by Ansible"
    config_ext_id: "aaaaaaaa-1111-2222-3333-444444444444"
    start_time: "2026-01-01T00:00:00Z"
    end_time: "2026-01-31T23:59:59Z"
    is_persistent: true
    timezone: "UTC"
    override_supported_formats:
      - PDF
      - CSV
    recipient_formats:
      - PDF
    recipients:
      - email_address: "ops-lead@example.com"
        recipient_name: "Ops Lead"
    entity_selection:
      entity_type: "VM"
      entity_ext_id:
        - "11111111-2222-3333-4444-555555555555"
  register: result
  ignore_errors: true

- name: Delete a generated report by external ID
  nutanix.ncp.ntnx_report_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "77777777-8888-9999-aaaa-bbbbbbbbbbbb"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating or deleting a report.
    - If the operation is create and C(wait) is true, it will return the generated report details.
    - If the operation is create and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the API response (typically an empty payload).
  returned: always
  type: dict
  sample:
    {
      "available_formats": ["PDF"],
      "config_ext_id": "aaaaaaaa-1111-2222-3333-444444444444",
      "creation_time": "2026-02-01T00:00:00+00:00",
      "description": "Monthly VM efficiency report generated by Ansible",
      "end_time": "2026-01-31T23:59:59+00:00",
      "entity_selection": {
          "entity_ext_id": ["11111111-2222-3333-4444-555555555555"],
          "entity_type": "VM"
      },
      "ext_id": "77777777-8888-9999-aaaa-bbbbbbbbbbbb",
      "is_persistent": true,
      "links": null,
      "name": "monthly_vm_report_full",
      "override_supported_formats": ["PDF", "CSV"],
      "owner_ext_id": "00000000-0000-0000-0000-000000000001",
      "recipient_formats": ["PDF"],
      "recipients": [
          {
              "email_address": "ops-lead@example.com",
              "recipient_name": "Ops Lead"
          }
      ],
      "start_time": "2026-01-01T00:00:00+00:00",
      "tenant_id": null,
      "timezone": "UTC"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the generated report instance.
  returned: always
  type: str
  sample: "77777777-8888-9999-aaaa-bbbbbbbbbbbb"

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
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Report with ext_id:77777777-8888-9999-aaaa-bbbbbbbbbbbb will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.opsmgmt.api_client import get_reports_api_instance  # noqa: E402
from ..module_utils.v4.opsmgmt.helpers import get_report  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
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

    entity_selection_spec = dict(
        entity_type=dict(
            type="str",
            required=True,
            choices=[
                "VM",
                "CLUSTER",
                "HOST",
                "CATEGORY",
                "CONTAINER",
                "DISK",
                "VIRTUAL_DISK",
                "VOLUME_GROUPS",
                "ALERT",
                "AUDIT",
                "EVENT",
                "CONFIG",
                "PLAYBOOK",
                "RECOVERY_PLAN_JOB",
                "STIG_STATS",
                "VCENTER_CLUSTER",
                "VCENTER_DATASTORE",
                "VCENTER_HOST",
                "VCENTER_VM",
                "VULNERABILITY",
            ],
            obj=ncm_operation_base_platform_sdk.EntityType,
        ),
        entity_ext_id=dict(type="list", elements="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        config_ext_id=dict(type="str"),
        start_time=dict(type="str"),
        end_time=dict(type="str"),
        is_persistent=dict(type="bool"),
        timezone=dict(type="str"),
        owner_ext_id=dict(type="str"),
        override_supported_formats=dict(
            type="list",
            elements="str",
            choices=["PDF", "CSV"],
            obj=ncm_operation_base_platform_sdk.ConfigReportFormat,
        ),
        recipient_formats=dict(
            type="list",
            elements="str",
            choices=["PDF", "CSV"],
            obj=ncm_operation_base_platform_sdk.ConfigReportFormat,
        ),
        recipients=dict(
            type="list",
            elements="dict",
            options=recipient_spec,
            obj=ncm_operation_base_platform_sdk.ConfigRecipient,
        ),
        entity_selection=dict(
            type="dict",
            options=entity_selection_spec,
            obj=ncm_operation_base_platform_sdk.EntitySelection,
        ),
    )

    return module_args


def create_report(module, api_instance, result):
    """
    Generate (create) a new report instance from an existing Report
    Configuration. Waits for the underlying task to complete (when C(wait) is
    true) and then fetches the generated report so it can be returned to the
    caller.
    """
    validate_required_params(
        module, ["name", "config_ext_id", "start_time", "end_time"]
    )

    sg = SpecGenerator(module)
    default_spec = ncm_operation_base_platform_sdk.Report()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create report spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_report(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating report",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.REPORT
        )
        if ext_id:
            result["ext_id"] = ext_id
            report = get_report(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(report.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception("Failed to get entity ext_id from task for Report"),
                msg="Failed to get entity ext_id from task for Report",
            )
    result["changed"] = True


def update_report(module, api_instance, result):
    """
    Report instances are immutable once generated - the underlying API does
    NOT expose an update endpoint. When callers set C(state=present) with an
    C(ext_id), we surface a descriptive error so the intent is not silently
    ignored.
    """
    del api_instance  # signature kept for consistency with other v2 modules.
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    module.fail_json(
        msg=(
            "Report instances are immutable and cannot be updated. "
            "To regenerate content, delete this report (state=absent) and "
            "create a new one (state=present without ext_id)."
        ),
        **result,
    )


def delete_report(module, api_instance, result):
    """
    Delete a generated report instance by its external ID. The delete API is
    synchronous (returns an empty payload) so no task-wait is required.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Report with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_report_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting report",
        )
    if resp is not None and getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    else:
        result["response"] = None
    result["msg"] = "Report with ext_id:{0} deleted successfully.".format(ext_id)
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
        ],
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
    }
    api_instance = get_reports_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_report(module, api_instance, result)
        else:
            create_report(module, api_instance, result)
    else:
        delete_report(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
