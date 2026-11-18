#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_summary_v2
short_description: Triggers a refresh operation for updating security stats on Prism Central and Prism Element.
version_added: 2.7.0
description:
    - Initiates a refresh operation to update security summary statistics.
    - Refreshes the security summary data for clusters associated with the target
      Prism Central or Prism Element, including STIG, vulnerability,
      security-configuration and password summaries.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Refresh Security Summaries) -
      Required Roles: Prism Admin, Security Dashboard Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
    state:
        description:
            - State of the module.
            - If state is C(present), the module will trigger a refresh of the security summaries.
            - If state is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
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
- name: Trigger refresh of security summaries
  nutanix.ncp.ntnx_security_summary_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for refreshing security summaries.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2026-07-20T10:20:15.523481+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T10:20:05.167906+00:00",
            "entities_affected": null,
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T10:20:15.523481+00:00",
            "legacy_error_message": null,
            "operation": "kRefreshSecuritySummaries",
            "operation_description": "Refresh Security Summaries",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T10:20:05.185754+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error or in check mode operation
    type: str
    sample: "Api Exception raised while triggering security summaries refresh"

failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the refresh task.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_security_summaries_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
    )
    return module_args


def refresh_security_summaries(module, api_instance, result):
    if module.check_mode:
        result["msg"] = "Security summaries refresh will be triggered."
        return

    resp = None
    try:
        resp = api_instance.refresh_security_summaries()
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while triggering security summaries refresh",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
    }
    api_instance = get_security_summaries_api_instance(module)
    refresh_security_summaries(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
