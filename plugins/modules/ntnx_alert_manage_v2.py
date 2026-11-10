#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_alert_manage_v2
short_description: Acknowledge or resolve an alert in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Acknowledge or resolve an alert.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update Alert) -
      Required Roles: Account Owner, Administrator, Files Admin, Monitoring Admin, NCM Connector,
      Prism Admin, Project Admin, Project Manager, Super Admin, Tenant Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will acknowledge or resolve the alert.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - Unique identifier of an alert that can be resolved or acknowledged.
        type: str
        required: true
    action_type:
        description:
            - An alert can be resolved or acknowledged using the following parameters.
        type: str
        required: true
        choices:
            - RESOLVE
            - ACKNOWLEDGE
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
  nutanix.ncp.ntnx_alert_manage_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "af3a40be-d079-454a-968a-9903d1bf0549"
    action_type: ACKNOWLEDGE
  register: result

- name: Resolve an alert
  nutanix.ncp.ntnx_alert_manage_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "af3a40be-d079-454a-968a-9903d1bf0549"
    action_type: RESOLVE
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for acknowledge or resolve alert.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    type: dict
    returned: always
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
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:1a1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e5e"
ext_id:
    description: The external ID of the alert.
    type: str
    returned: always
    sample: "af3a40be-d079-454a-968a-9903d1bf0549"
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
    sample: "Alert with ext_id:af3a40be-d079-454a-968a-9903d1bf0549 will be acknowledged or resolved."
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
    import ntnx_monitoring_py_client as sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        action_type=dict(
            type="str",
            required=True,
            choices=["RESOLVE", "ACKNOWLEDGE"],
        ),
    )
    return module_args


def acknowledge_or_resolve_alert(module, result, manage_api, alerts_api):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_alert(module, alerts_api, ext_id)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        module.fail_json(
            msg="Failed to get etag value from the current alert",
            **result,
        )

    sg = SpecGenerator(module)
    default_spec = sdk.AlertActionSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for acknowledge or resolve alert",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Alert with ext_id:{0} will be acknowledged or resolved.".format(ext_id)
        return

    kwargs = {"if_match": etag_value}
    resp = None
    try:
        resp = manage_api.manage_alert(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while acknowledging or resolving alert",
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
        "response": None,
        "failed": False,
    }
    manage_api = get_manage_alerts_api_instance(module)
    alerts_api = get_alerts_api_instance(module)
    acknowledge_or_resolve_alert(module, result, manage_api, alerts_api)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
