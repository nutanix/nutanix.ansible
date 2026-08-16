#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_report_config_v2
short_description: Create, Update, Delete report configurations in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete report configurations in Nutanix Prism Central.
  - Report configurations belong to the Nutanix Cloud Manager (NCM) Intelligent Operations reporting feature.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create/Update/Delete a Report Configuration) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=opsmgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create report configuration.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update report configuration.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete report configuration.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the report configuration.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the report configuration.
      - Required for create operation. Maximum 64 characters.
    type: str
    required: false
  description:
    description:
      - Description of the report configuration. Maximum 1000 characters.
    type: str
    required: false
  timezone:
    description:
      - The timezone in which the report will be generated.
      - Must be one of the timezones supported by C(pytz.all_timezones).
    type: str
    required: false
  is_private:
    description:
      - Flag specifying if the report configuration is private to the creator.
    type: bool
    required: false
  start_time_offset_secs:
    description:
      - Offset (in seconds) for the start time for data collection during report generation.
    type: int
    required: false
  end_time_offset_secs:
    description:
      - Offset (in seconds) for the end time for data collection during report generation.
    type: int
    required: false
  default_section_entity_type:
    description:
      - Default section entity type applied when a section does not specify its own repeat criteria.
    type: str
    required: false
    choices:
      - ALERT
      - AUDIT
      - CATEGORY
      - CLUSTER
      - CONFIG
      - CONTAINER
      - DISK
      - EVENT
      - HOST
      - PLAYBOOK
      - RECOVERY_PLAN_JOB
      - STIG_STATS
      - VCENTER_CLUSTER
      - VCENTER_DATASTORE
      - VCENTER_HOST
      - VCENTER_VM
      - VIRTUAL_DISK
      - VM
      - VOLUME_GROUPS
      - VULNERABILITY
  supported_formats:
    description:
      - List specifying the formats in which the report can be created.
    type: list
    elements: str
    required: false
    choices:
      - PDF
      - CSV
  schedule:
    description:
      - Defines the parameters for scheduling report creation from the report configuration.
    type: dict
    required: false
    suboptions:
      schedule_interval:
        description:
          - Schedule interval for report generation.
        type: str
        required: true
        choices:
          - NONE
          - DAILY
          - WEEKLY
          - MONTHLY
          - YEARLY
      frequency:
        description:
          - Frequency (unit multiplier) applied to the schedule interval.
        type: int
        required: false
      start_time:
        description:
          - Start time of the schedule in ISO 8601 format.
        type: str
        required: false
      end_time:
        description:
          - End time of the schedule in ISO 8601 format.
        type: str
        required: false
  retention_config:
    description:
      - Defines how long to retain a report generated from the report configuration.
      - Only one of C(retention_period_seconds) and C(retention_count) should be specified.
    type: dict
    required: false
    suboptions:
      retention_period_seconds:
        description:
          - Retention period (in seconds) for the generated reports.
        type: int
        required: false
      retention_count:
        description:
          - Maximum number of generated reports to retain.
        type: int
        required: false
  notification_policy:
    description:
      - Notification policy for sending the generated report by email.
    type: dict
    required: false
    suboptions:
      recipient_formats:
        description:
          - Formats in which the report is delivered to the recipients.
        type: list
        elements: str
        required: false
        choices:
          - PDF
          - CSV
      recipients:
        description:
          - Email recipients list.
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
              - Display name of the recipient.
            type: str
            required: false
      email_subject:
        description:
          - Subject line of the notification email.
        type: str
        required: false
      email_body:
        description:
          - Body of the notification email.
        type: str
        required: false
  report_customization:
    description:
      - Report-level customizations for header, footer, styling, and branding.
    type: dict
    required: false
    suboptions:
      header_html:
        description:
          - Custom header HTML for the report.
        type: str
        required: false
      footer_html:
        description:
          - Custom footer HTML for the report.
        type: str
        required: false
      css_style_sheet:
        description:
          - Custom CSS stylesheet for the report.
        type: str
        required: false
      logo_image_ext_id:
        description:
          - External ID of the logo image referenced by the report.
        type: str
        required: false
  sections:
    description:
      - List of sections in the report. A section is a group of rows consisting of widgets.
      - Required for create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      name:
        description:
          - Name of the section.
        type: str
        required: false
      description:
        description:
          - Description of the section.
        type: str
        required: false
      repeat_criteria:
        description:
          - Criteria for repeating a section for each entity of a given entity type.
        type: dict
        required: false
        suboptions:
          entity_type:
            description:
              - Entity type on which the repetition is applied.
            type: str
            required: true
            choices:
              - ALERT
              - AUDIT
              - CATEGORY
              - CLUSTER
              - CONFIG
              - CONTAINER
              - DISK
              - EVENT
              - HOST
              - PLAYBOOK
              - RECOVERY_PLAN_JOB
              - STIG_STATS
              - VCENTER_CLUSTER
              - VCENTER_DATASTORE
              - VCENTER_HOST
              - VCENTER_VM
              - VIRTUAL_DISK
              - VM
              - VOLUME_GROUPS
              - VULNERABILITY
          repetition_rule:
            description:
              - Additional rule expression that further constrains the repetition set.
            type: str
            required: false
      time_filter:
        description:
          - Time based filtering applied to the section data.
        type: str
        required: false
        choices:
          - CREATED_TIME
          - LAST_OCCURRED_TIME
      rows:
        description:
          - List of rows (maximum three widgets per row) contained in this section.
        type: list
        elements: dict
        required: false
        suboptions:
          widgets:
            description:
              - List of widgets displayed inside this row.
            type: list
            elements: dict
            required: false
            suboptions:
              widget_template:
                description:
                  - Predefined widget template used by the widget.
                  - Mutually exclusive with C(widget_config).
                type: dict
                required: false
                suboptions:
                  widget_template:
                    description:
                      - The predefined widget template type.
                    type: str
                    required: true
                    choices:
                      - ACCOUNT_OVERVIEW
                      - ALERTS_COUNT
                      - ALERTS_HISTOGRAM
                      - ALERTS_TIMELINE
                      - ANOMALIES_COUNT
                      - BLOCKS_SUMMARY
                      - CLUSTER_BULLY_VM_TABLE
                      - CLUSTER_CONSTRAINED_VM_TABLE
                      - CLUSTER_CPU_RUNWAY_CHART
                      - CLUSTER_INACTIVE_VM_TABLE
                      - CLUSTER_LICENSE_TABLE
                      - CLUSTER_MEMORY_RUNWAY_CHART
                      - CLUSTER_OVERPROVISIONED_VM_TABLE
                      - CLUSTER_POTENTIAL_CPU_RECLAIM
                      - CLUSTER_POTENTIAL_MEMORY_RECLAIM
                      - CLUSTER_POTENTIAL_STORAGE_RECLAIM
                      - CLUSTER_RUNWAY
                      - CLUSTER_STORAGE_RUNWAY_CHART
                      - IGNORE_TIME_WINDOW_TABLE
                      - IMPACTED_CLUSTER
                      - MULTICLUSTER_LICENSE_SUMMARY
                      - VCENTER_BLOCKS_SUMMARY
                      - VCENTER_BULLY_VM_TABLE
                      - VCENTER_CONSTRAINED_VM_TABLE
                      - VCENTER_CPU_RUNWAY_CHART
                      - VCENTER_INACTIVE_VM_TABLE
                      - VCENTER_MEMORY_RUNWAY_CHART
                      - VCENTER_OVERPROVISIONED_VM_TABLE
                      - VCENTER_POTENTIAL_CPU_RECLAIM
                      - VCENTER_POTENTIAL_MEMORY_RECLAIM
                      - VCENTER_POTENTIAL_STORAGE_RECLAIM
                      - VM_EFFICIENCY
              widget_config:
                description:
                  - Custom widget configuration.
                  - Mutually exclusive with C(widget_template).
                type: dict
                required: false
                suboptions:
                  entity_type:
                    description:
                      - Entity type on which the widget operates.
                    type: str
                    required: false
                    choices:
                      - ALERT
                      - AUDIT
                      - CATEGORY
                      - CLUSTER
                      - CONFIG
                      - CONTAINER
                      - DISK
                      - EVENT
                      - HOST
                      - PLAYBOOK
                      - RECOVERY_PLAN_JOB
                      - STIG_STATS
                      - VCENTER_CLUSTER
                      - VCENTER_DATASTORE
                      - VCENTER_HOST
                      - VCENTER_VM
                      - VIRTUAL_DISK
                      - VM
                      - VOLUME_GROUPS
                      - VULNERABILITY
                  heading:
                    description:
                      - Heading text displayed above the widget.
                    type: str
                    required: false
                  description:
                    description:
                      - Description of the widget.
                    type: str
                    required: false
                  type:
                    description:
                      - Visualisation type of the widget.
                    type: str
                    required: false
                    choices:
                      - ALERT_LIST
                      - BAR_CHART
                      - CONFIG_SUMMARY
                      - COUNT_SUMMARY
                      - DATA_TABLE
                      - GEO_MAP
                      - HISTOGRAM
                      - LINE_CHART
                      - METRIC_SUMMARY_CHART
                      - METRIC_SUMMARY_TEXT
                      - PIE_CHART
                      - STATS_SUMMARY
                      - TEXT
                  size:
                    description:
                      - Layout size of the widget on the report page.
                    type: str
                    required: false
                    choices:
                      - SMALL
                      - LARGE
                      - FULLSPAN
                  widget_id:
                    description:
                      - Unique identifier of the widget within the report.
                    type: str
                    required: false
                  repeat_criteria:
                    description:
                      - Criteria for repeating the widget for each entity of a given entity type.
                    type: dict
                    required: false
                    suboptions:
                      entity_type:
                        description:
                          - Entity type on which the widget is repeated.
                        type: str
                        required: true
                        choices:
                          - ALERT
                          - AUDIT
                          - CATEGORY
                          - CLUSTER
                          - CONFIG
                          - CONTAINER
                          - DISK
                          - EVENT
                          - HOST
                          - PLAYBOOK
                          - RECOVERY_PLAN_JOB
                          - STIG_STATS
                          - VCENTER_CLUSTER
                          - VCENTER_DATASTORE
                          - VCENTER_HOST
                          - VCENTER_VM
                          - VIRTUAL_DISK
                          - VM
                          - VOLUME_GROUPS
                          - VULNERABILITY
                      repetition_rule:
                        description:
                          - Additional rule expression that further constrains the repetition set.
                        type: str
                        required: false
                  time_filter:
                    description:
                      - Time based filtering applied to the widget data.
                    type: str
                    required: false
                    choices:
                      - CREATED_TIME
                      - LAST_OCCURRED_TIME
                  data_criteria:
                    description:
                      - Criteria describing how the widget selects and sorts data.
                    type: dict
                    required: false
                    suboptions:
                      filter_criteria:
                        description:
                          - Filter expression applied on the underlying entity list (OData style).
                        type: str
                        required: false
                      sort_column:
                        description:
                          - Column name to sort the widget data on.
                        type: str
                        required: false
                      sort_order:
                        description:
                          - Sort order for the widget data.
                        type: str
                        required: false
                        choices:
                          - ASCENDING
                          - DESCENDING
                      limit:
                        description:
                          - Maximum number of rows the widget should display.
                        type: int
                        required: false
                      sort_key:
                        description:
                          - Additional aggregation key controlling how sort_column is reduced.
                        type: str
                        required: false
                        choices:
                          - FIRST
                          - LAST
                          - LATEST
                          - MAX
                          - MIN
                      custom_parameters:
                        description:
                          - Widget-specific custom parameters expressed as name/value pairs.
                        type: list
                        elements: dict
                        required: false
                        suboptions:
                          name:
                            description:
                              - Name of the parameter.
                            type: str
                            required: true
                          value:
                            description:
                              - Value of the parameter (stored as a string).
                            type: str
                            required: false
                  type_specific_configs:
                    description:
                      - Widget-type-specific configuration expressed as name/value pairs.
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      name:
                        description:
                          - Name of the config entry.
                        type: str
                        required: true
                      value:
                        description:
                          - Value of the config entry.
                        type: str
                        required: false
                  fields:
                    description:
                      - Fields (metrics) displayed by the widget.
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      label:
                        description:
                          - Human readable label for the field.
                        type: str
                        required: false
                      name:
                        description:
                          - Metric or column name.
                        type: str
                        required: false
                      aggregate_function:
                        description:
                          - Aggregation function applied on the metric.
                        type: str
                        required: false
                        choices:
                          - AVG
                          - COUNT
                          - LAST
                          - MAX
                          - MIN
                          - SUM
                      unit:
                        description:
                          - Unit of measurement associated with the metric.
                        type: str
                        required: false
                        choices:
                          - ABSOLUTE
                          - BYTES
                          - GIBIBYTES
                          - GIGABYTES_PER_SECOND
                          - GIGAHERTZ
                          - HERTZ
                          - KIBIBYTES
                          - KILOBYTES_PER_SECOND
                          - KILOHERTZ
                          - MEBIBYTES
                          - MEGABYTES_PER_SECOND
                          - MEGAHERTZ
                          - MICROSECONDS
                          - MILLISECONDS
                          - PEBIBYTES
                          - PERCENT
                          - SECONDS
                          - TEBIBYTES
                      thresholds:
                        description:
                          - Colour thresholds applied to the metric value.
                        type: list
                        elements: dict
                        required: false
                        suboptions:
                          start_range:
                            description:
                              - Lower bound of the threshold range.
                            type: float
                            required: false
                          end_range:
                            description:
                              - Upper bound of the threshold range.
                            type: float
                            required: false
                          color:
                            description:
                              - Colour applied when the metric value falls in this range.
                            type: str
                            required: false
                      compound_metric:
                        description:
                          - Compound metric definition combining up to two base metrics via a formula.
                        type: dict
                        required: false
                        suboptions:
                          formula:
                            description:
                              - Formula referring to operands by letters (e.g. C((A/B)*100)).
                            type: str
                            required: false
                          operands:
                            description:
                              - List of compound metric operands used in the formula.
                            type: list
                            elements: dict
                            required: false
                            suboptions:
                              label:
                                description:
                                  - Human readable label for the operand.
                                type: str
                                required: false
                              name:
                                description:
                                  - Metric name of the operand.
                                type: str
                                required: false
                              aggregate_function:
                                description:
                                  - Aggregation function applied on the operand metric.
                                type: str
                                required: false
                                choices:
                                  - AVG
                                  - COUNT
                                  - LAST
                                  - MAX
                                  - MIN
                                  - SUM
                              unit:
                                description:
                                  - Unit of measurement of the operand metric.
                                type: str
                                required: false
                                choices:
                                  - ABSOLUTE
                                  - BYTES
                                  - GIBIBYTES
                                  - GIGABYTES_PER_SECOND
                                  - GIGAHERTZ
                                  - HERTZ
                                  - KIBIBYTES
                                  - KILOBYTES_PER_SECOND
                                  - KILOHERTZ
                                  - MEBIBYTES
                                  - MEGABYTES_PER_SECOND
                                  - MEGAHERTZ
                                  - MICROSECONDS
                                  - MILLISECONDS
                                  - PEBIBYTES
                                  - PERCENT
                                  - SECONDS
                                  - TEBIBYTES
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
- name: Create report configuration
  nutanix.ncp.ntnx_report_config_v2:
    state: present
    name: "ansible_report_config"
    description: "Report configuration created by Ansible"
    timezone: "UTC"
    is_private: false
    supported_formats:
      - PDF
      - CSV
    default_section_entity_type: VM
    start_time_offset_secs: 86400
    end_time_offset_secs: 0
    schedule:
      schedule_interval: DAILY
      frequency: 1
      start_time: "2026-01-01T00:00:00Z"
    retention_config:
      retention_count: 10
    notification_policy:
      recipient_formats:
        - PDF
      recipients:
        - email_address: "reports@example.com"
          recipient_name: "Reports Team"
      email_subject: "Daily VM report"
      email_body: "Please find the attached VM report."
    report_customization:
      header_html: "<h1>VM Report</h1>"
      footer_html: "<footer>Generated by Ansible</footer>"
    sections:
      - name: "vm_overview"
        description: "Overview of virtual machines"
        time_filter: CREATED_TIME
        repeat_criteria:
          entity_type: VM
        rows:
          - widgets:
              - widget_config:
                  entity_type: VM
                  heading: "VM Count"
                  type: COUNT_SUMMARY
                  size: SMALL
                  widget_id: "vm_count"
              - widget_template:
                  widget_template: CLUSTER_INACTIVE_VM_TABLE
  register: result
  ignore_errors: true

- name: Update report configuration
  nutanix.ncp.ntnx_report_config_v2:
    state: present
    ext_id: "d05b9c00-3d0e-4bab-9d18-2d5c8bd7d55c"
    name: "ansible_report_config_updated"
    description: "Updated by Ansible"
    timezone: "UTC"
    is_private: true
    supported_formats:
      - PDF
    schedule:
      schedule_interval: WEEKLY
      frequency: 2
    retention_config:
      retention_count: 5
    notification_policy:
      recipient_formats:
        - PDF
      recipients:
        - email_address: "ops@example.com"
      email_subject: "Weekly VM report"
    sections:
      - name: "vm_updated_section"
        rows:
          - widgets:
              - widget_config:
                  entity_type: VM
                  heading: "Top VMs"
                  type: DATA_TABLE
                  size: LARGE
                  widget_id: "vm_table"
  register: result
  ignore_errors: true

- name: Delete report configuration
  nutanix.ncp.ntnx_report_config_v2:
    state: absent
    ext_id: "d05b9c00-3d0e-4bab-9d18-2d5c8bd7d55c"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a report configuration.
    - If the operation is create or update and C(wait) is true, it will return the report configuration details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "creation_time": "2026-07-21T08:15:00.000Z",
      "default_section_entity_type": "VM",
      "description": "Report configuration created by Ansible",
      "end_time_offset_secs": 0,
      "ext_id": "d05b9c00-3d0e-4bab-9d18-2d5c8bd7d55c",
      "is_imported": false,
      "is_private": false,
      "is_system_defined": false,
      "links": null,
      "name": "ansible_report_config",
      "notification_policy": {
        "email_body": "Please find the attached VM report.",
        "email_subject": "Daily VM report",
        "recipient_formats": ["PDF"],
        "recipients": [
          {"email_address": "reports@example.com", "recipient_name": "Reports Team"}
        ]
      },
      "report_customization": {
        "css_style_sheet": null,
        "footer_html": "<footer>Generated by Ansible</footer>",
        "header_html": "<h1>VM Report</h1>",
        "logo_image_ext_id": null
      },
      "retention_config": {"retention_count": 10, "retention_period_seconds": null},
      "schedule": {
        "end_time": null,
        "frequency": 1,
        "schedule_interval": "DAILY",
        "start_time": "2026-01-01T00:00:00.000Z"
      },
      "sections": [
        {
          "description": "Overview of virtual machines",
          "name": "vm_overview",
          "repeat_criteria": {"entity_type": "VM", "repetition_rule": null},
          "rows": [
            {
              "widgets": [
                {"widget_info": {"entity_type": "VM", "heading": "VM Count", "size": "SMALL", "type": "COUNT_SUMMARY", "widget_id": "vm_count"}},
                {"widget_info": {"widget_template": "CLUSTER_INACTIVE_VM_TABLE"}}
              ]
            }
          ],
          "time_filter": "CREATED_TIME"
        }
      ],
      "start_time_offset_secs": 86400,
      "supported_formats": ["PDF", "CSV"],
      "tenant_id": null,
      "timezone": "UTC"
    }

task_ext_id:
  description: The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description: The external ID of the report configuration.
  returned: always
  type: str
  sample: "d05b9c00-3d0e-4bab-9d18-2d5c8bd7d55c"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (idempotency or check_mode).
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
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Report configuration with ext_id:d05b9c00-3d0e-4bab-9d18-2d5c8bd7d55c will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.opsmgmt.api_client import (  # noqa: E402
    get_etag,
    get_report_config_api_instance,
)
from ..module_utils.v4.opsmgmt.helpers import get_report_config  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_opsmgmt_py_client as opsmgmt_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as opsmgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


ENTITY_TYPE_CHOICES = [
    "ALERT",
    "AUDIT",
    "CATEGORY",
    "CLUSTER",
    "CONFIG",
    "CONTAINER",
    "DISK",
    "EVENT",
    "HOST",
    "PLAYBOOK",
    "RECOVERY_PLAN_JOB",
    "STIG_STATS",
    "VCENTER_CLUSTER",
    "VCENTER_DATASTORE",
    "VCENTER_HOST",
    "VCENTER_VM",
    "VIRTUAL_DISK",
    "VM",
    "VOLUME_GROUPS",
    "VULNERABILITY",
]

REPORT_FORMAT_CHOICES = ["PDF", "CSV"]

SCHEDULE_INTERVAL_CHOICES = ["NONE", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"]

TIME_FILTER_CHOICES = ["CREATED_TIME", "LAST_OCCURRED_TIME"]

WIDGET_TYPE_CHOICES = [
    "ALERT_LIST",
    "BAR_CHART",
    "CONFIG_SUMMARY",
    "COUNT_SUMMARY",
    "DATA_TABLE",
    "GEO_MAP",
    "HISTOGRAM",
    "LINE_CHART",
    "METRIC_SUMMARY_CHART",
    "METRIC_SUMMARY_TEXT",
    "PIE_CHART",
    "STATS_SUMMARY",
    "TEXT",
]

WIDGET_SIZE_CHOICES = ["SMALL", "LARGE", "FULLSPAN"]

AGGREGATE_FUNCTION_CHOICES = ["AVG", "COUNT", "LAST", "MAX", "MIN", "SUM"]

UNIT_CHOICES = [
    "ABSOLUTE",
    "BYTES",
    "GIBIBYTES",
    "GIGABYTES_PER_SECOND",
    "GIGAHERTZ",
    "HERTZ",
    "KIBIBYTES",
    "KILOBYTES_PER_SECOND",
    "KILOHERTZ",
    "MEBIBYTES",
    "MEGABYTES_PER_SECOND",
    "MEGAHERTZ",
    "MICROSECONDS",
    "MILLISECONDS",
    "PEBIBYTES",
    "PERCENT",
    "SECONDS",
    "TEBIBYTES",
]

SORT_ORDER_CHOICES = ["ASCENDING", "DESCENDING"]

SORT_KEY_CHOICES = ["FIRST", "LAST", "LATEST", "MAX", "MIN"]

WIDGET_TEMPLATE_CHOICES = [
    "ACCOUNT_OVERVIEW",
    "ALERTS_COUNT",
    "ALERTS_HISTOGRAM",
    "ALERTS_TIMELINE",
    "ANOMALIES_COUNT",
    "BLOCKS_SUMMARY",
    "CLUSTER_BULLY_VM_TABLE",
    "CLUSTER_CONSTRAINED_VM_TABLE",
    "CLUSTER_CPU_RUNWAY_CHART",
    "CLUSTER_INACTIVE_VM_TABLE",
    "CLUSTER_LICENSE_TABLE",
    "CLUSTER_MEMORY_RUNWAY_CHART",
    "CLUSTER_OVERPROVISIONED_VM_TABLE",
    "CLUSTER_POTENTIAL_CPU_RECLAIM",
    "CLUSTER_POTENTIAL_MEMORY_RECLAIM",
    "CLUSTER_POTENTIAL_STORAGE_RECLAIM",
    "CLUSTER_RUNWAY",
    "CLUSTER_STORAGE_RUNWAY_CHART",
    "IGNORE_TIME_WINDOW_TABLE",
    "IMPACTED_CLUSTER",
    "MULTICLUSTER_LICENSE_SUMMARY",
    "VCENTER_BLOCKS_SUMMARY",
    "VCENTER_BULLY_VM_TABLE",
    "VCENTER_CONSTRAINED_VM_TABLE",
    "VCENTER_CPU_RUNWAY_CHART",
    "VCENTER_INACTIVE_VM_TABLE",
    "VCENTER_MEMORY_RUNWAY_CHART",
    "VCENTER_OVERPROVISIONED_VM_TABLE",
    "VCENTER_POTENTIAL_CPU_RECLAIM",
    "VCENTER_POTENTIAL_MEMORY_RECLAIM",
    "VCENTER_POTENTIAL_STORAGE_RECLAIM",
    "VM_EFFICIENCY",
]

REPORT_CONFIG_READ_ONLY_FIELDS = (
    "is_system_defined",
    "is_imported",
    "creation_time",
)


def get_module_spec():
    recipient_spec = dict(
        email_address=dict(type="str", required=True),
        recipient_name=dict(type="str", required=False),
    )

    notification_policy_spec = dict(
        recipient_formats=dict(
            type="list", elements="str", choices=REPORT_FORMAT_CHOICES, required=False
        ),
        recipients=dict(
            type="list", elements="dict", options=recipient_spec, required=False
        ),
        email_subject=dict(type="str", required=False),
        email_body=dict(type="str", required=False),
    )

    schedule_spec = dict(
        schedule_interval=dict(
            type="str", required=True, choices=SCHEDULE_INTERVAL_CHOICES
        ),
        frequency=dict(type="int", required=False),
        start_time=dict(type="str", required=False),
        end_time=dict(type="str", required=False),
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

    kv_pair_spec = dict(
        name=dict(type="str", required=True),
        value=dict(type="str", required=False),
    )

    repeat_criteria_spec = dict(
        entity_type=dict(type="str", required=True, choices=ENTITY_TYPE_CHOICES),
        repetition_rule=dict(type="str", required=False),
    )

    threshold_spec = dict(
        start_range=dict(type="float", required=False),
        end_range=dict(type="float", required=False),
        color=dict(type="str", required=False),
    )

    compound_metric_operand_spec = dict(
        label=dict(type="str", required=False),
        name=dict(type="str", required=False),
        aggregate_function=dict(
            type="str", required=False, choices=AGGREGATE_FUNCTION_CHOICES
        ),
        unit=dict(type="str", required=False, choices=UNIT_CHOICES),
    )

    compound_metric_spec = dict(
        formula=dict(type="str", required=False),
        operands=dict(
            type="list",
            elements="dict",
            options=compound_metric_operand_spec,
            required=False,
        ),
    )

    widget_field_spec = dict(
        label=dict(type="str", required=False),
        name=dict(type="str", required=False),
        aggregate_function=dict(
            type="str", required=False, choices=AGGREGATE_FUNCTION_CHOICES
        ),
        unit=dict(type="str", required=False, choices=UNIT_CHOICES),
        thresholds=dict(
            type="list", elements="dict", options=threshold_spec, required=False
        ),
        compound_metric=dict(type="dict", options=compound_metric_spec, required=False),
    )

    data_criteria_spec = dict(
        filter_criteria=dict(type="str", required=False),
        sort_column=dict(type="str", required=False),
        sort_order=dict(type="str", required=False, choices=SORT_ORDER_CHOICES),
        limit=dict(type="int", required=False),
        sort_key=dict(type="str", required=False, choices=SORT_KEY_CHOICES),
        custom_parameters=dict(
            type="list", elements="dict", options=kv_pair_spec, required=False
        ),
    )

    widget_config_spec = dict(
        entity_type=dict(type="str", required=False, choices=ENTITY_TYPE_CHOICES),
        heading=dict(type="str", required=False),
        description=dict(type="str", required=False),
        type=dict(type="str", required=False, choices=WIDGET_TYPE_CHOICES),
        size=dict(type="str", required=False, choices=WIDGET_SIZE_CHOICES),
        widget_id=dict(type="str", required=False),
        repeat_criteria=dict(type="dict", options=repeat_criteria_spec, required=False),
        time_filter=dict(type="str", required=False, choices=TIME_FILTER_CHOICES),
        data_criteria=dict(type="dict", options=data_criteria_spec, required=False),
        type_specific_configs=dict(
            type="list", elements="dict", options=kv_pair_spec, required=False
        ),
        fields=dict(
            type="list", elements="dict", options=widget_field_spec, required=False
        ),
    )

    widget_template_spec = dict(
        widget_template=dict(
            type="str", required=True, choices=WIDGET_TEMPLATE_CHOICES
        ),
    )

    widget_spec = dict(
        widget_template=dict(type="dict", options=widget_template_spec, required=False),
        widget_config=dict(type="dict", options=widget_config_spec, required=False),
    )

    row_spec = dict(
        widgets=dict(type="list", elements="dict", options=widget_spec, required=False),
    )

    section_spec = dict(
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        repeat_criteria=dict(type="dict", options=repeat_criteria_spec, required=False),
        time_filter=dict(type="str", required=False, choices=TIME_FILTER_CHOICES),
        rows=dict(type="list", elements="dict", options=row_spec, required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        timezone=dict(type="str"),
        is_private=dict(type="bool"),
        start_time_offset_secs=dict(type="int"),
        end_time_offset_secs=dict(type="int"),
        default_section_entity_type=dict(type="str", choices=ENTITY_TYPE_CHOICES),
        supported_formats=dict(
            type="list", elements="str", choices=REPORT_FORMAT_CHOICES
        ),
        schedule=dict(type="dict", options=schedule_spec),
        retention_config=dict(type="dict", options=retention_config_spec),
        notification_policy=dict(type="dict", options=notification_policy_spec),
        report_customization=dict(type="dict", options=report_customization_spec),
        sections=dict(type="list", elements="dict", options=section_spec),
    )
    return module_args


def _build_kv_pairs(items):
    if not items:
        return None
    result = []
    for item in items:
        pair = opsmgmt_sdk.KVPair(name=item.get("name"))
        if item.get("value") is not None:
            pair.value = item.get("value")
        result.append(pair)
    return result


def _build_recipients(items):
    if not items:
        return None
    result = []
    for item in items:
        recipient = opsmgmt_sdk.ConfigRecipient(
            email_address=item.get("email_address"),
            recipient_name=item.get("recipient_name"),
        )
        result.append(recipient)
    return result


def _build_notification_policy(data):
    if not data:
        return None
    return opsmgmt_sdk.ConfigNotificationPolicy(
        recipient_formats=data.get("recipient_formats"),
        recipients=_build_recipients(data.get("recipients")),
        email_subject=data.get("email_subject"),
        email_body=data.get("email_body"),
    )


def _build_schedule(data):
    if not data:
        return None
    return opsmgmt_sdk.ReportSchedule(
        schedule_interval=data.get("schedule_interval"),
        frequency=data.get("frequency"),
        start_time=data.get("start_time"),
        end_time=data.get("end_time"),
    )


def _build_retention_config(data):
    if not data:
        return None
    return opsmgmt_sdk.RetentionConfig(
        retention_period_seconds=data.get("retention_period_seconds"),
        retention_count=data.get("retention_count"),
    )


def _build_report_customization(data):
    if not data:
        return None
    return opsmgmt_sdk.ConfigReportCustomization(
        header_html=data.get("header_html"),
        footer_html=data.get("footer_html"),
        css_style_sheet=data.get("css_style_sheet"),
        logo_image_ext_id=data.get("logo_image_ext_id"),
    )


def _build_repeat_criteria(data):
    if not data:
        return None
    return opsmgmt_sdk.RepeatCriteria(
        entity_type=data.get("entity_type"),
        repetition_rule=data.get("repetition_rule"),
    )


def _build_thresholds(items):
    if not items:
        return None
    result = []
    for item in items:
        result.append(
            opsmgmt_sdk.Threshold(
                start_range=item.get("start_range"),
                end_range=item.get("end_range"),
                color=item.get("color"),
            )
        )
    return result


def _build_compound_metric(data):
    if not data:
        return None
    operands = None
    if data.get("operands"):
        operands = []
        for op in data.get("operands"):
            operands.append(
                opsmgmt_sdk.CompoundMetricOperand(
                    label=op.get("label"),
                    name=op.get("name"),
                    aggregate_function=op.get("aggregate_function"),
                    unit=op.get("unit"),
                )
            )
    return opsmgmt_sdk.CompoundMetric(operands=operands, formula=data.get("formula"))


def _build_widget_fields(items):
    if not items:
        return None
    result = []
    for item in items:
        result.append(
            opsmgmt_sdk.WidgetField(
                label=item.get("label"),
                name=item.get("name"),
                aggregate_function=item.get("aggregate_function"),
                unit=item.get("unit"),
                thresholds=_build_thresholds(item.get("thresholds")),
                compound_metric=_build_compound_metric(item.get("compound_metric")),
            )
        )
    return result


def _build_data_criteria(data):
    if not data:
        return None
    return opsmgmt_sdk.DataCriteria(
        filter_criteria=data.get("filter_criteria"),
        sort_column=data.get("sort_column"),
        sort_order=data.get("sort_order"),
        limit=data.get("limit"),
        sort_key=data.get("sort_key"),
        custom_parameters=_build_kv_pairs(data.get("custom_parameters")),
    )


def _build_widget(module, data):
    if not data:
        return None
    widget_template = data.get("widget_template")
    widget_config = data.get("widget_config")
    if widget_template and widget_config:
        module.fail_json(
            msg="widget_template and widget_config are mutually exclusive inside a widget."
        )
    if widget_template:
        tmpl = opsmgmt_sdk.WidgetTemplate(
            widget_template=widget_template.get("widget_template")
        )
        return opsmgmt_sdk.Widget(widget_info=tmpl)
    if widget_config:
        cfg = opsmgmt_sdk.WidgetConfig(
            entity_type=widget_config.get("entity_type"),
            heading=widget_config.get("heading"),
            description=widget_config.get("description"),
            fields=_build_widget_fields(widget_config.get("fields")),
            type=widget_config.get("type"),
            size=widget_config.get("size"),
            repeat_criteria=_build_repeat_criteria(
                widget_config.get("repeat_criteria")
            ),
            data_criteria=_build_data_criteria(widget_config.get("data_criteria")),
            time_filter=widget_config.get("time_filter"),
            type_specific_configs=_build_kv_pairs(
                widget_config.get("type_specific_configs")
            ),
            widget_id=widget_config.get("widget_id"),
        )
        return opsmgmt_sdk.Widget(widget_info=cfg)
    return opsmgmt_sdk.Widget()


def _build_row(module, data):
    widgets = None
    if data.get("widgets"):
        widgets = [_build_widget(module, w) for w in data.get("widgets") if w]
    return opsmgmt_sdk.Row(widgets=widgets)


def _build_section(module, data):
    rows = None
    if data.get("rows"):
        rows = [_build_row(module, r) for r in data.get("rows") if r]
    return opsmgmt_sdk.Section(
        name=data.get("name"),
        description=data.get("description"),
        rows=rows,
        repeat_criteria=_build_repeat_criteria(data.get("repeat_criteria")),
        time_filter=data.get("time_filter"),
    )


def _build_sections(module, items):
    if items is None:
        return None
    return [_build_section(module, s) for s in items if s]


def build_report_config_spec(module, existing=None):
    """Assemble a ReportConfig SDK object from the module params.

    When ``existing`` is provided (update flow), each field is applied on top
    of a deep copy of the current spec so that unspecified fields retain their
    previous value.
    """

    if existing is not None:
        spec = deepcopy(existing)
    else:
        spec = opsmgmt_sdk.ReportConfig(name=module.params.get("name"), sections=[])

    params = module.params

    if params.get("name") is not None:
        spec.name = params.get("name")
    if params.get("description") is not None:
        spec.description = params.get("description")
    if params.get("timezone") is not None:
        spec.timezone = params.get("timezone")
    if params.get("is_private") is not None:
        spec.is_private = params.get("is_private")
    if params.get("start_time_offset_secs") is not None:
        spec.start_time_offset_secs = params.get("start_time_offset_secs")
    if params.get("end_time_offset_secs") is not None:
        spec.end_time_offset_secs = params.get("end_time_offset_secs")
    if params.get("default_section_entity_type") is not None:
        spec.default_section_entity_type = params.get("default_section_entity_type")
    if params.get("supported_formats") is not None:
        spec.supported_formats = params.get("supported_formats")

    if params.get("schedule") is not None:
        spec.schedule = _build_schedule(params.get("schedule"))
    if params.get("retention_config") is not None:
        spec.retention_config = _build_retention_config(params.get("retention_config"))
    if params.get("notification_policy") is not None:
        spec.notification_policy = _build_notification_policy(
            params.get("notification_policy")
        )
    if params.get("report_customization") is not None:
        spec.report_customization = _build_report_customization(
            params.get("report_customization")
        )
    if params.get("sections") is not None:
        spec.sections = _build_sections(module, params.get("sections"))

    return spec


def create_ReportConfig(module, result, api_instance):
    validate_required_params(module, ["name", "sections"])
    spec = build_report_config_spec(module)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_report_config(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating report configuration",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    if task_ext_id:
        result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    ext_id = _extract_ext_id_from_data(resp.data)
    if ext_id:
        result["ext_id"] = ext_id
        try:
            fetched = get_report_config(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(fetched.to_dict())
        except SystemExit:
            raise
        except Exception:
            pass
    else:
        raise_api_exception(
            module=module,
            exception=Exception(
                "Failed to extract ext_id from create report configuration response"
            ),
            msg="Failed to extract ext_id from create report configuration response",
        )

    result["changed"] = True


def _extract_ext_id_from_data(data):
    """Return the ReportConfig ext_id from a create/update response.

    The reporting APIs return the entity directly (not a task reference), so
    the data object itself carries the ext_id.
    """
    if data is None:
        return None
    ext_id = getattr(data, "ext_id", None)
    if ext_id:
        return ext_id
    if isinstance(data, dict):
        return data.get("ext_id")
    return None


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    for read_only in REPORT_CONFIG_READ_ONLY_FIELDS:
        old_spec_dict.pop(read_only, None)
        update_spec_dict.pop(read_only, None)
    old_spec_dict.pop("links", None)
    update_spec_dict.pop("links", None)
    old_spec_dict.pop("tenant_id", None)
    update_spec_dict.pop("tenant_id", None)
    return old_spec_dict == update_spec_dict


def update_ReportConfig(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["name", "sections"])

    old_spec = get_report_config(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for updating report configuration",
            **result,
        )

    update_spec = build_report_config_spec(module, existing=old_spec)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. Report configuration is identical to the existing one."
        )

    strip_read_only_fields(update_spec, fields=REPORT_CONFIG_READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_report_config_by_id(
            extId=ext_id, body=update_spec, if_match=etag
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating report configuration",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    if task_ext_id:
        result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    fetched = get_report_config(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(fetched.to_dict())
    result["changed"] = True


def delete_ReportConfig(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Report configuration with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.delete_report_config_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting report configuration",
        )

    task_ext_id = getattr(resp.data, "ext_id", None) if resp and resp.data else None
    if task_ext_id:
        result["task_ext_id"] = task_ext_id
    if resp and resp.data is not None:
        try:
            result["response"] = strip_internal_attributes(resp.data.to_dict())
        except AttributeError:
            result["response"] = resp.data
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
        "task_ext_id": None,
        "skipped": False,
    }
    api_instance = get_report_config_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_ReportConfig(module, result, api_instance)
        else:
            create_ReportConfig(module, result, api_instance)
    else:
        delete_ReportConfig(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
