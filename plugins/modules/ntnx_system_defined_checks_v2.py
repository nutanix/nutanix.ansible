#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_system_defined_checks_v2
short_description: Run System-Defined Checks on a cluster in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Run System-Defined Checks on a cluster.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Run System Defined Checks Cluster) -
      Required Roles: Monitoring Admin, Prism Admin, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will run System-Defined Checks.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    cluster_ext_id:
        description:
            - Unique identifier for the cluster for which run System-Defined Checks is requested.
        type: str
        required: true
    sda_ext_ids:
        description:
            - List of Check IDs to be executed. This field cannot be set simultaneously with
              shouldRunAllChecks; only one of them should be specified.
        type: list
        elements: str
    should_anonymize:
        description:
            - Indicates whether to mask sensitive data in the check run summary.
        type: bool
    should_send_report_to_configured_recipients:
        description:
            - Determines if the run summary should be sent to the email address set in the alert
              email configuration.
            - Either this should be true or additionalRecipients should be provided.
            - If both are set then email would be sent to all the recipients.
            - "Note: SMTP server must be configured on the cluster for sending emails."
        type: bool
    additional_recipients:
        description:
            - A list of additional email addresses for sending the run summary.
            - Either this should be set or shouldSendReportToConfiguredRecipients should be true.
            - If both are set then email would be sent to all the recipients.
            - "Note: SMTP server must be configured on the cluster for sending emails."
        type: list
        elements: str
    node_ips:
        description:
            - List of node IP addresses where the Check will run.
            - This field will be ignored if the check scope is a cluster.
        type: list
        elements: dict
        suboptions:
            value:
                description:
                    - The IPv4 address of the host.
                type: str
                required: true
            prefix_length:
                description:
                    - The prefix length of the network to which this host IPv4 address belongs.
                type: int
                default: 32
    should_run_all_checks:
        description:
            - Indicates whether all System-Defined Checks applicable to the specified cluster
              should be executed.
            - This field is mutually exclusive with the sdaExtIds parameter, meaning that only one
              of these should be set at a time.
            - Please use this field with caution, as it is resource-intensive.
        type: bool
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
- name: Run selected System-Defined Checks
  nutanix.ncp.ntnx_system_defined_checks_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    sda_ext_ids:
      - "3034"
    should_anonymize: true
    should_send_report_to_configured_recipients: true
  register: result

- name: Run all System-Defined Checks
  nutanix.ncp.ntnx_system_defined_checks_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    should_run_all_checks: true
    additional_recipients:
      - ops@example.com
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for run System-Defined Checks.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    type: dict
    returned: always
    sample:
        {
            "ext_id": "ZXJnb24=:1a1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e5e",
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
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error or in check mode operation
    sample: "System-Defined Checks will be run for cluster with ext_id:00061de6-4a87-6b06-185b-ac1f6b6f97e2."
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
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
    import ntnx_monitoring_py_client as sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", default=32),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str", required=True),
        sda_ext_ids=dict(type="list", elements="str"),
        should_anonymize=dict(type="bool"),
        should_send_report_to_configured_recipients=dict(type="bool"),
        additional_recipients=dict(type="list", elements="str"),
        node_ips=dict(
            type="list",
            elements="dict",
            options=ipv4_address_spec,
            obj=sdk.IPv4Address,
        ),
        should_run_all_checks=dict(type="bool"),
    )
    return module_args


def run_system_defined_checks(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    default_spec = sdk.RunSystemDefinedChecksSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for running System-Defined Checks",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "System-Defined Checks will be run for cluster with ext_id:{0}.".format(
                cluster_ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.run_system_defined_checks(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while running System-Defined Checks",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
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
        mutually_exclusive=[("sda_ext_ids", "should_run_all_checks")],
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
    api_instance = get_system_defined_checks_api_instance(module)
    run_system_defined_checks(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
