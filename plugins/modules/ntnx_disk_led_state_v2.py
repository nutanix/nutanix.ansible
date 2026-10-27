#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_disk_led_state_v2
short_description: Update the LED state of a physical Disk in a Nutanix cluster
version_added: 2.7.0
description:
  - This module allows you to update (turn on / turn off) the physical LED of a Disk
    in a Nutanix cluster.
  - The action is used to visually locate a specific drive in a chassis — typically
    while replacing a failed disk or performing hardware maintenance in the datacenter.
  - The operation is asynchronous — an ergon task is returned by the API and, when
    C(wait) is true (default), the module polls until the task completes.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Update LED State Disk) -
    Required Roles: Prism Admin, Prism Viewer, Project Manager, Super Admin,
    Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - state is not supported for this module.
      - It will always be present.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external identifier (UUID) of the Disk whose LED state must be updated.
    type: str
    required: true
  is_engaged:
    description:
      - Indicates the target LED status of the Disk.
      - C(true) turns the LED on (engaged / locate mode) so the drive can be
        visually identified.
      - C(false) turns the LED off (disengaged).
    type: bool
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
- name: Turn ON the LED of a disk to locate it in the chassis
  nutanix.ncp.ntnx_disk_led_state_v2:
    ext_id: "5a2b0e5c-4a2b-4c9b-8d5a-2f0e0e3b9a11"
    is_engaged: true
  register: result
  ignore_errors: true

- name: Turn OFF the LED of a disk after maintenance
  nutanix.ncp.ntnx_disk_led_state_v2:
    ext_id: "5a2b0e5c-4a2b-4c9b-8d5a-2f0e0e3b9a11"
    is_engaged: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating the LED state of a Disk.
    - Task details (final task object) if C(wait) is true.
    - Initial task submission response if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "app_name": null,
      "batch_summary": null,
      "cluster_ext_ids": [
        "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-20T13:14:44.070871+00:00",
      "completion_details": null,
      "created_time": "2026-07-20T13:14:43.918054+00:00",
      "entities_affected": [
        {
          "ext_id": "4542a93c-f79a-43fc-a515-ec8c066000a0",
          "name": null,
          "rel": "clustermgmt:config:disks"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:75a28b33-dfcd-4a52-6e32-b2faf70eb417",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T13:14:44.070870+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 0,
      "operation": "kUpdateLed",
      "operation_description": "Update Disk Led state",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "project_ext_id": "00000000-0000-0000-0000-000000000000",
      "resource_links": null,
      "root_task": null,
      "started_time": "2026-07-20T13:14:43.933314+00:00",
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
  returned: When there is an error
  type: str
  sample: "Api Exception raised while updating disk LED state"

error:
  description:
    - This field typically holds information about if the task have errors that
      occurred during the task execution.
  returned: when an error occurs
  type: str
  sample: "Failed generating disk LED state update spec"

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

task_ext_id:
  description: The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:75a28b33-dfcd-4a52-6e32-b2faf70eb417"

ext_id:
  description: The external ID of the Disk whose LED state was updated.
  returned: always
  type: str
  sample: "4542a93c-f79a-43fc-a515-ec8c066000a0"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_disks_api_instance,
    get_etag,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_disk  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as cluster_management_sdk  # noqa: E402  # fmt: skip

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        is_engaged=dict(type="bool", required=True),
    )
    return module_args


def update_disk_led_state(module, result, api_instance):
    """Update the LED state of an existing Disk.

    The GET Disk API does not expose the current LED state, so an
    idempotency check cannot be based on it. The module verifies the
    target Disk exists via GET-by-ext_id and forwards the desired LED
    state to the platform.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_disk = get_disk(module, api_instance, ext_id)

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.LEDStateUpdationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating disk LED state update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    etag = get_etag(data=current_disk)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.update_disk_led_state(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating disk LED state",
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
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_disks_api_instance(module)
    update_disk_led_state(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
