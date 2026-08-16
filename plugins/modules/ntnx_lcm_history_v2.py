#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_history_v2
short_description: Export LCM history of connected clusters in Nutanix Prism Central
version_added: 2.7.0
description:
    - This module allows you to export the LCM (Life Cycle Manager) history
      of connected clusters in Nutanix Prism Central.
    - The export is performed asynchronously. When C(wait) is true the module
      waits for the task to complete and returns the task response containing
      the URL/completion details for downloading the exported file.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Export LCM histories.) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer,
      Security Dashboard Admin, Security Dashboard Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    state:
        description:
            - State of the module.
            - If state is C(present), the module will trigger an LCM history export.
            - This module does not support any other state.
        type: str
        choices:
            - present
        default: present
    file_format:
        description:
            - File format of the exported LCM history data.
            - Currently only C(CSV) is supported by the API.
        type: str
        choices:
            - CSV
        default: CSV
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
- name: Export LCM histories as CSV
  nutanix.ncp.ntnx_lcm_history_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_format: CSV
  register: lcm_history_export
"""

RETURN = r"""
response:
    description:
        - Response for exporting LCM histories.
        - Task details containing progress and completion metadata.
        - If C(wait) is true, contains the full task response including
          the exported file URL in C(completion_details).
        - If C(wait) is false, contains the initial task reference.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2026-07-20T14:00:00.000000+00:00",
            "completion_details": [
                {
                    "name": "url",
                    "value": "https://10.44.76.28:9440/api/lifecycle/v4.2/resources/lcm-histories/downloads/exports/history_export.csv"
                }
            ],
            "created_time": "2026-07-20T13:59:55.000000+00:00",
            "entities_affected": null,
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T14:00:00.000000+00:00",
            "legacy_error_message": null,
            "operation": "kLcmExportHistoryTask",
            "operation_description": "Export LCM histories",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T13:59:55.000000+00:00",
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

ext_id:
    description:
        - The external ID of the LCM history export.
        - This module does not target a specific LCM history entry, so this
          field is C(null) for the export action.
    returned: always
    type: str
    sample: null

task_ext_id:
    description: The external ID of the task created for the export operation.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while exporting LCM histories"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    returned: When an error occurs
    type: str
    sample: "Failed generating spec for exporting LCM histories"

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
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_lcm_histories_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as life_cycle_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as life_cycle_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        file_format=dict(type="str", choices=["CSV"], default="CSV"),
    )
    return module_args


def export_histories(module, api_instance, result):
    """Trigger the LCM histories export action and populate the result dict."""
    sg = SpecGenerator(module)
    default_spec = life_cycle_management_sdk.ExportHistorySpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for exporting LCM histories", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.export_histories(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while exporting LCM histories",
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
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_lcm_histories_api_instance(module)
    export_histories(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
