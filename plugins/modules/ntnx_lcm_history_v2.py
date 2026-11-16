#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_history_v2
short_description: Export LCM history information from connected clusters
version_added: "2.7.0"
description:
    - This module Exports the LCM operation history of connected clusters as a downloadable file
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Export the LCM history information of connected clusters.) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    state:
        description:
            - State of the module.
            - If state is C(present), the module will trigger an LCM histories export.
            - If C(state) is C(absent) the module will fail.
        type: str
        choices:
            - present
        default: present
    file_format:
        description:
            - File format of the exported LCM history data.
            - Required for the export operation.
        type: str
        choices:
            - CSV
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
- name: Export LCM histories in CSV format
  nutanix.ncp.ntnx_lcm_history_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_format: "CSV"
  register: export_result
"""

RETURN = r"""
response:
    description:
        - Task response for exporting LCM histories.
        - If C(wait) is true, this will contain the completed task details.
        - If C(wait) is false, this will contain the task submission details.
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2026-07-20T12:34:56.789012+00:00",
            "completion_details": [
                {
                    "name": "file_path",
                    "value": "/home/nutanix/data/lcm/histories_export.csv"
                }
            ],
            "created_time": "2026-07-20T12:34:50.123456+00:00",
            "entities_affected": null,
            "error_messages": null,
            "ext_id": "ZXJnb24=:8e5b9e3a-7c39-4d3f-b0d8-4b7c1c9e42a1",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T12:34:56.789012+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 0,
            "number_of_subtasks": 0,
            "operation": "kLcmExportHistoriesTask",
            "operation_description": "Export LCM histories",
            "owned_by": null,
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2026-07-20T12:34:50.123456+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }
task_ext_id:
    description: The external ID of the export task.
    type: str
    returned: always
    sample: "ZXJnb24=:8e5b9e3a-7c39-4d3f-b0d8-4b7c1c9e42a1"
ext_id:
    description:
        - The external ID of the entity affected by the task, if any.
        - Populated only when the API returns an entity reference for the exported histories.
    type: str
    returned: when applicable
    sample: "8e5b9e3a-7c39-4d3f-b0d8-4b7c1c9e42a1"
changed:
    description: Whether the module made any changes.
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the task failed.
    type: bool
    returned: always
    sample: false
error:
    description: Error details if any error occurred.
    type: str
    returned: When an error occurs
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error or the module runs in check mode
    sample: "LCM histories will be exported in 'CSV' format."
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
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        file_format=dict(type="str", required=False, choices=["CSV"]),
    )
    return module_args


def export_lcm_histories(module, api_instance, result):
    validate_required_params(module, ["file_format"])

    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.ExportHistorySpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating export LCM histories spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "LCM histories will be exported in '{0}' format.".format(
            module.params.get("file_format")
        )
        return

    resp = None
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
        entities_affected = getattr(task, "entities_affected", None) or []
        for entity in entities_affected:
            ext_id = getattr(entity, "ext_id", None)
            if ext_id:
                result["ext_id"] = ext_id
                break

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
        "failed": False,
    }
    api_instance = get_lcm_histories_api_instance(module)
    export_lcm_histories(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
