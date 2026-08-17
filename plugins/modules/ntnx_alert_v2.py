#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_alert_v2
short_description: Acknowledge or resolve an Alert in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to manage an Alert in Nutanix Prism Central.
  - Perform the Acknowledge or Resolve action on an open alert identified by its external ID.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Acknowledge or Resolve an Alert) -
    Required Roles: Prism Admin, Super Admin, Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present) the module will perform the requested action
        (acknowledge or resolve) on the Alert identified by C(ext_id).
    type: str
    required: false
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
      - The action to perform on the alert.
      - C(ACKNOWLEDGE) marks the alert as seen by an administrator.
      - C(RESOLVE) marks the underlying issue as fixed and closes the alert.
    type: str
    required: true
    choices:
      - ACKNOWLEDGE
      - RESOLVE
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
  nutanix.ncp.ntnx_alert_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "1e8b6c9c-4a1e-4b7b-9f9e-5c1e2a3b4c5d"
    action_type: ACKNOWLEDGE
  register: result
  ignore_errors: true

- name: Resolve an alert
  nutanix.ncp.ntnx_alert_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "1e8b6c9c-4a1e-4b7b-9f9e-5c1e2a3b4c5d"
    action_type: RESOLVE
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the Acknowledge or Resolve alert action.
    - Task details when C(wait) is true.
    - Initial TaskReference from the API when C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "0006361b-6855-3644-7458-2268f8ffb2bd"
      ],
      "completed_time": "2026-07-20T12:34:56.123456+00:00",
      "completion_details": null,
      "created_time": "2026-07-20T12:34:55.100000+00:00",
      "entities_affected": [
        {
          "ext_id": "1e8b6c9c-4a1e-4b7b-9f9e-5c1e2a3b4c5d",
          "rel": "monitoring:v4:serviceability:alert"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:aa8e2f2b-1c78-45f7-8ad3-9d3f8bce41d1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T12:34:56.123456+00:00",
      "legacy_error_message": null,
      "operation": "ManageAlert",
      "operation_description": "Acknowledge or resolve the alert",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-20T12:34:55.150000+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description: The external ID of the task created for the alert action.
  returned: always
  type: str
  sample: "ZXJnb24=:aa8e2f2b-1c78-45f7-8ad3-9d3f8bce41d1"

ext_id:
  description: The external ID of the Alert that was acknowledged or resolved.
  returned: always
  type: str
  sample: "1e8b6c9c-4a1e-4b7b-9f9e-5c1e2a3b4c5d"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or in check mode.
  type: str
  sample: "Api Exception raised while managing alert"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  returned: when an error occurs
  type: str

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
    validate_required_params,
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
            required=True,
            choices=["ACKNOWLEDGE", "RESOLVE"],
            obj=monitoring_sdk.ActionType,
        ),
    )
    return module_args


def manage_alert(module, result, api_instance, alerts_api_instance):
    validate_required_params(module, ["ext_id", "action_type"])
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

    # ManageAlert requires the current Alert etag as the If-Match header.
    current_alert = get_alert(module, alerts_api_instance, ext_id)
    etag = get_etag(data=current_alert)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for managing alert with ext_id: {0}".format(
                ext_id
            ),
            **result,
        )
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
    alerts_api_instance = get_alerts_api_instance(module)
    manage_alert(module, result, api_instance, alerts_api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
