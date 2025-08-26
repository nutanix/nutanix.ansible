#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_restore_protected_resources_v2
short_description: Module to restore a protected resource in Nutanix Prism Central.
version_added: 2.1.0
description:
  - This module can be used to restore a protected resource in Nutanix Prism Central.
  - Supported only for protected resources that have minutely scheduled protection policies.
  - Restore VM/VG will create new VM/VG in the secondary PC (PC) for the given VM/VG external ID
  - Restore VM/VG uses secondary PC IP and its credentials in C(nutanix_host), C(nutanix_username), C(nutanix_password).
  - You can provide restore time to restore the VM/VG to a specific point in time
options:
  state:
    description:
      - State of the module.
      - If state is present, the module will restore a protected resource.
      - If state is not present, the module will fail.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external identifier of a protected VM or volume group.
    type: str
    required: true
  cluster_ext_id:
    description:
      - The external identifier of the cluster on which the entity has valid restorable time ranges.
      - The restored entity is created on the same cluster.
    type: str
    required: false
  restore_time:
    description:
      - UTC date and time in ISO 8601 format representing the time from when the state of the entity should be restored.
      - This must be a valid time within the restorable time range(s) for the protected resource.
    type: str
    required: false
  wait:
    description:
      - Wait for the task to complete.
    type: bool
    required: false
    default: True
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Restore VM
  nutanix.ncp.ntnx_restore_protected_resources_v2:
    nutanix_host: "10.2.1.0"
    nutanix_username: "username"
    nutanix_password: "password"
    validate_certs: false
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    cluster_ext_id: "00062aa9-1234-1122-3333-ac1f6b6f97e2"
    restore_time: "2025-01-23T14:30:00-07:00"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description: Task response for restoring a protected resource.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
          "00062899-4a29-0cf9-0000-000000028f57"
      ],
      "completed_time": "2025-01-14T07:47:51.573218+00:00",
      "completion_details": null,
      "created_time": "2025-01-14T07:47:44.190257+00:00",
      "entities_affected": [
          {
              "ext_id": "4f1e2d82-eab6-420d-b8c1-97096d71df5a",
              "name": "george_test",
              "rel": "vmm:ahv:config:vm"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:af298405-1d59-4c28-9b78-f8f94a5adf2d",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2025-01-14T07:47:51.573216+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 0,
      "operation": "EntitySnapshotRealizeWithAction",
      "operation_description": "Restore Protected Resource",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2025-01-14T07:47:44.205725+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: When an error occurs
  type: str
  sample: false

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external identifier of the protected resource.
  returned: always
  type: str
  sample: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"

task_ext_id:
  description: The external identifier of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:af298405-1d59-4c28-9b78-f8f94a5adf2d"
"""

import traceback  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_protected_resource_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
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


def get_module_spec():

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        cluster_ext_id=dict(type="str", required=False),
        restore_time=dict(type="str", required=False),
    )
    return module_args


def restore_protected_resource(module, result):
    protected_resource = get_protected_resource_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    sg = SpecGenerator(module)
    default_spec = data_protection_sdk.ProtectedResourceRestoreSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating restore protected resource Spec", **result
        )
    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = protected_resource.restore_protected_resource(extId=ext_id, body=spec)

    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while restoring protected resource",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
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
    }

    restore_protected_resource(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
