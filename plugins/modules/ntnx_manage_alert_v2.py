#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_manage_alert_v2
short_description: Acknowledge or resolve an alert in Nutanix Prism Central
version_added: 2.7.0
description:
    - Acknowledge or resolve an alert in Nutanix Prism Central using its external ID.
    - The operation is dispatched asynchronously by the monitoring service; when C(wait) is true
      the module polls the returned task until it completes.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Acknowledge or Resolve an alert) -
      Required Roles: Prism Admin, Super Admin, Cluster Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
    state:
        description:
            - State of the module.
            - If state is C(present), the module will acknowledge or resolve the specified alert.
            - Only C(present) is supported; there is no C(absent) counterpart for this action.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - External ID of the alert that must be acknowledged or resolved.
        type: str
        required: true
    action_type:
        description:
            - Action to perform on the alert.
            - C(ACKNOWLEDGE) marks the alert as acknowledged so operators know it is being investigated.
            - C(RESOLVE) marks the alert as resolved once the underlying issue has been addressed.
        type: str
        choices:
            - ACKNOWLEDGE
            - RESOLVE
        required: true
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
- name: Acknowledge an alert
  nutanix.ncp.ntnx_manage_alert_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6f9d2e12-1a1f-4c9c-8b1c-2f3d21e2f0a1"
    action_type: "ACKNOWLEDGE"
  register: result
  ignore_errors: true

- name: Resolve an alert
  nutanix.ncp.ntnx_manage_alert_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6f9d2e12-1a1f-4c9c-8b1c-2f3d21e2f0a1"
    action_type: "RESOLVE"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for acknowledging or resolving the alert.
        - If C(wait) is true, this contains the completed task details.
        - If C(wait) is false, this contains the immediate task reference returned by the API.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-20T15:30:44.510131+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T15:30:43.887321+00:00",
            "entities_affected": [
                {
                    "ext_id": "6f9d2e12-1a1f-4c9c-8b1c-2f3d21e2f0a1",
                    "name": null,
                    "rel": "monitoring:v4:serviceability:alert"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:83e58c9d-5b57-4b62-8b5f-6b57f4d0c2c1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T15:30:44.510131+00:00",
            "legacy_error_message": null,
            "operation": "APR-AlertManager",
            "operation_description": "Manage Alert",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T15:30:43.912541+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

task_ext_id:
    description: The external ID of the task tracking this action.
    returned: always
    type: str
    sample: "ZXJnb24=:83e58c9d-5b57-4b62-8b5f-6b57f4d0c2c1"

ext_id:
    description: The external ID of the alert on which the action was performed.
    returned: always
    type: str
    sample: "6f9d2e12-1a1f-4c9c-8b1c-2f3d21e2f0a1"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: Status or error message returned by the module.
    returned: When there is an error, or when running in check mode
    type: str
    sample: "Api Exception raised while managing alert"

error:
    description: Error details when the operation fails.
    returned: When an error occurs
    type: str
    sample: "Failed to get etag for alert"

failed:
    description: This indicates whether the task failed.
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
    get_alerts_api_instance,
    get_etag,
    get_manage_alerts_api_instance,
)
from ..module_utils.v4.monitoring.helpers import get_alert  # noqa: E402
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
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        action_type=dict(
            type="str",
            choices=["ACKNOWLEDGE", "RESOLVE"],
            required=True,
        ),
    )

    return module_args


def manage_alert(module, api_instance, result):
    """Perform the acknowledge/resolve action on the alert.

    Fetches the alert to obtain a fresh ETag (required by the API for
    optimistic concurrency control), builds an ``AlertActionSpec`` and
    submits it via ``ManageAlertsApi.manage_alert``. When ``wait`` is set,
    the returned task is polled until it reaches a terminal state.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = monitoring_sdk.AlertActionSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating manage alert spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    alerts_api = get_alerts_api_instance(module)
    alert_wrapper = get_alert(module, alerts_api, ext_id)
    etag = get_etag(alert_wrapper)
    if not etag:
        module.fail_json(msg="Failed to get etag for alert", **result)
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.manage_alert(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while managing alert",
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
            msg=missing_required_lib("ntnx_monitoring_py_client"),
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
    api_instance = get_manage_alerts_api_instance(module)
    manage_alert(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
