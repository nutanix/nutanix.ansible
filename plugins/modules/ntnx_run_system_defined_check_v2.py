#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_run_system_defined_check_v2
short_description: Run System-Defined Checks on a cluster in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module triggers an on-demand run of System-Defined Alert (SDA) health
    checks on a Prism Element (PE) cluster registered with Nutanix Prism Central.
  - The caller can either target a specific set of SDA policies via
    C(sda_ext_ids), or execute every check applicable to the cluster by setting
    C(should_run_all_checks) to C(true).
  - The run produces an asynchronous task; a summary report is emailed to the
    recipients configured on the cluster and/or to any addresses listed in
    C(additional_recipients).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Run System-Defined Checks on a cluster) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported for this action module.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - Unique identifier for the PE cluster on which the System-Defined Checks
        must be executed.
      - This is the C(clusterExtId) path parameter of the underlying v4 API.
      - Required for the action.
    type: str
    required: true
  sda_ext_ids:
    description:
      - List of System-Defined Alert (SDA) policy external IDs whose checks
        should be executed on the target cluster.
      - Mutually exclusive with C(should_run_all_checks).
    type: list
    elements: str
    required: false
  should_anonymize:
    description:
      - When set to C(true), sensitive data captured during the check run is
        masked in the summary report.
      - Defaults to C(true) on the server side when omitted.
    type: bool
    required: false
  should_send_report_to_configured_recipients:
    description:
      - When C(true), the run summary is emailed to the recipients configured
        on the cluster's alert email configuration.
      - Either C(should_send_report_to_configured_recipients) must be C(true)
        or C(additional_recipients) must be provided; if both are set, the
        report is delivered to the union of the two recipient sets.
      - Defaults to C(true) on the server side when omitted.
    type: bool
    required: false
  additional_recipients:
    description:
      - List of extra email addresses that must receive the run summary in
        addition to (or instead of) the cluster's configured recipients.
      - Either C(should_send_report_to_configured_recipients) must be C(true)
        or C(additional_recipients) must be provided.
    type: list
    elements: str
    required: false
  node_ips:
    description:
      - List of PE node IPv4 addresses on which the checks must be executed.
      - This field is ignored for checks whose scope is the whole cluster.
    type: list
    elements: dict
    required: false
    suboptions:
      value:
        description:
          - The IPv4 address value of the node.
        type: str
        required: true
      prefix_length:
        description:
          - Prefix length of the IPv4 address.
        type: int
        required: false
        default: 32
  should_run_all_checks:
    description:
      - When C(true), every System-Defined Check applicable to the target
        cluster is executed. This can be resource intensive and is mutually
        exclusive with C(sda_ext_ids).
      - Defaults to C(false) on the server side when omitted.
    type: bool
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
- name: Run all applicable System-Defined Checks on a cluster
  nutanix.ncp.ntnx_run_system_defined_check_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    should_run_all_checks: true
    should_anonymize: true
    should_send_report_to_configured_recipients: true
    additional_recipients:
      - "sre@example.com"
  register: result

- name: Run a targeted set of System-Defined Checks by SDA ext_id
  nutanix.ncp.ntnx_run_system_defined_check_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    sda_ext_ids:
      - "3000"
      - "3001"
    should_anonymize: false
    should_send_report_to_configured_recipients: false
    additional_recipients:
      - "ncc-reports@example.com"

- name: Run checks on a specific set of nodes only
  nutanix.ncp.ntnx_run_system_defined_check_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    sda_ext_ids:
      - "3000"
    node_ips:
      - value: "10.44.76.31"
      - value: "10.44.76.32"
"""

RETURN = r"""
response:
  description:
    - Response for running System-Defined Checks on the target cluster.
    - When C(wait) is C(true), it contains the task details for the underlying
      C(RunHealthChecksFromPC) task.
    - When C(wait) is C(false), it contains the task reference returned by the
      API call.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-20T15:35:12.524581+00:00",
      "completion_details": null,
      "created_time": "2026-07-20T15:34:47.167906+00:00",
      "entities_affected": [
        {
          "ext_id": "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2",
          "name": null,
          "rel": "clustermgmt:config:cluster"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T15:35:12.524581+00:00",
      "legacy_error_message": null,
      "operation": "RunHealthChecksFromPC",
      "operation_description": "Run System-Defined Check(s)",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-20T15:34:47.185754+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task created by the run-system-defined-checks
      action.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description:
    - The external ID of the PE cluster on which the checks were run.
  returned: always
  type: str
  sample: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or the module runs in check mode.
  type: str
  sample: "Api Exception raised while running system defined checks"

error:
  description: The error message if any error occurred during the run.
  returned: When an error occurs.
  type: str

failed:
  description: This field typically holds information about if the task has failed.
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_system_defined_checks_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        sda_ext_ids=dict(type="list", elements="str", required=False),
        should_anonymize=dict(type="bool", required=False),
        should_send_report_to_configured_recipients=dict(type="bool", required=False),
        additional_recipients=dict(type="list", elements="str", required=False),
        node_ips=dict(
            type="list",
            elements="dict",
            options=ipv4_address_spec,
            required=False,
            obj=monitoring_sdk.IPv4Address,
        ),
        should_run_all_checks=dict(type="bool", required=False),
    )

    return module_args


def _validate_recipient_selection(module):
    """Enforce the API rule that at least one recipient channel is selected.

    The API requires that either C(should_send_report_to_configured_recipients)
    is C(true) or C(additional_recipients) contains at least one address.
    The server defaults C(should_send_report_to_configured_recipients) to
    C(true) when the caller omits it, so we only fail when the caller
    explicitly disables it AND does not supply additional recipients.
    """
    send_to_configured = module.params.get(
        "should_send_report_to_configured_recipients"
    )
    additional = module.params.get("additional_recipients")
    if send_to_configured is False and not additional:
        module.fail_json(
            msg=(
                "Either 'should_send_report_to_configured_recipients' must be true or "
                "'additional_recipients' must contain at least one email address."
            )
        )


def run_system_defined_checks(module, api_instance, result):
    """Trigger the run-system-defined-checks action for the target cluster."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    _validate_recipient_selection(module)

    sg = SpecGenerator(module)
    default_spec = monitoring_sdk.RunSystemDefinedChecksSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for running system defined checks",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "System defined checks will be run on cluster ext_id:{0}.".format(ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.run_system_defined_checks(clusterExtId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while running system defined checks",
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
        mutually_exclusive=[
            ("sda_ext_ids", "should_run_all_checks"),
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
        "ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }
    api_instance = get_system_defined_checks_api_instance(module)
    run_system_defined_checks(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
