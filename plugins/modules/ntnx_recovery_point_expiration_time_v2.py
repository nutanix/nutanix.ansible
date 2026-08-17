#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_point_expiration_time_v2
short_description: Set the expiration time of a recovery point in Nutanix Prism Central
version_added: 2.7.0
description:
    - This module allows you to set (update) the expiration time of an existing
      recovery point in Nutanix Prism Central using the
      C($actions/set-expiration-time) V4 API.
    - The expiration time controls when the recovery point is garbage
      collected.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Set the expiration time of the recovery point) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin,
      Kubernetes Data Services System, NCM Connector, Prism Admin,
      Project Manager, Super Admin, Self-Service Admin (deprecated).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported since this is an action module.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the top-level recovery point whose
              expiration time is being set.
        type: str
        required: true
    expiration_time:
        description:
            - The UTC date and time in ISO-8601 format when the recovery point
              expires.
            - Required for the C(set-expiration-time) action; the SDK does not
              accept a null expiration time.
        type: str
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
- name: Set the expiration time of a recovery point
  nutanix.ncp.ntnx_recovery_point_expiration_time_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    expiration_time: "2026-12-31T23:59:00+00:00"
  register: result
  ignore_errors: true

- name: Extend the expiration time of an existing recovery point
  nutanix.ncp.ntnx_recovery_point_expiration_time_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    expiration_time: "2027-06-30T12:00:00+00:00"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for setting the expiration time of a recovery point.
        - Task details when C(wait) is true.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2026-07-21T07:00:13.522381+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T07:00:12.944003+00:00",
            "entities_affected": [
                {
                    "ext_id": "70b0bd49-7c0d-410f-81e0-7e77b1c19c8c",
                    "name": "ansible_rp_exp_rp_joLAzSPk",
                    "rel": "dataprotection:config:recovery-point"
                },
                {
                    "ext_id": "5d0cc427-84cc-4d87-ba88-c977f760b2f6",
                    "name": "ansible_rp_exp_rp_joLAzSPk",
                    "rel": "dataprotection:config:vm-recovery-point"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:87ccbcf6-f204-4360-bd98-7032866b2105",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T07:00:13.522380+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 2,
            "number_of_subtasks": 0,
            "operation": "UpdateRecoveryPoint",
            "operation_description": "Update Recovery Point",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T07:00:12.955401+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

task_ext_id:
    description:
        - The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:87ccbcf6-f204-4360-bd98-7032866b2105"

ext_id:
    description:
        - The external ID of the recovery point.
    returned: always
    type: str
    sample: "70b0bd49-7c0d-410f-81e0-7e77b1c19c8c"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

failed:
    description: This indicates whether the task failed.
    returned: always
    type: bool
    sample: false

error:
    description: This indicates the error message if any error occurred.
    returned: When an error occurs
    type: str

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while setting recovery point expiration time"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_etag,
    get_recovery_point_api_instance,
)
from ..module_utils.v4.data_protection.helpers import get_recovery_point  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_dataprotection_py_client as data_protection_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_protection_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        expiration_time=dict(type="str", required=True),
    )
    return module_args


def set_recovery_point_expiration_time(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = data_protection_sdk.ExpirationTimeSpec()
    spec.expiration_time = module.params.get("expiration_time")

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current_spec = get_recovery_point(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        module.fail_json(
            msg="Failed to fetch etag for setting recovery point expiration time",
            **result,
        )

    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.set_recovery_point_expiration_time(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while setting recovery point expiration time",
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
            msg=missing_required_lib("ntnx_dataprotection_py_client"),
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
    api_instance = get_recovery_point_api_instance(module)
    set_recovery_point_expiration_time(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
