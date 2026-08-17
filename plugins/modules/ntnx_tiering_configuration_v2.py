#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_tiering_configuration_v2
short_description: Create, Update, Delete tiering configurations for Nutanix Files in Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete tiering configurations for a Nutanix Files file server in Nutanix Prism Central.
  - A tiering configuration controls how cold data on the file server is automatically moved to a remote object store tier.
  - This module uses PC v4 APIs based SDKs.
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create tiering configuration.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update tiering configuration.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete tiering configuration.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the tiering configuration.
      - Required for update and delete operations.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server the tiering configuration belongs to.
      - Required for all operations.
    type: str
    required: true
  memory_threshold_percent:
    description:
      - Capacity threshold in percentage for tiering.
      - Range from 0 to 100 (inclusive).
      - Files tiering will trigger only when the used capacity of the file server exceeds this percentage.
    type: int
    required: false
  cooloff_period_seconds:
    description:
      - Cool off period in seconds for tiering.
      - Files older than the cool off period time will be considered for tiering.
      - Minimum value is 86400 (i.e. 1 day).
    type: int
    required: false
  minimum_file_size_bytes:
    description:
      - Minimum file size in bytes for tiering.
      - Files size greater than this will be considered for tiering.
      - Minimum value is 65536 (i.e. 64 KiB).
    type: int
    required: false
    default: 65536
  mount_targets_enablement_type:
    description:
      - Configuration to enable current and/or future mount targets (shares) for tiering.
    type: str
    required: false
    choices:
      - ALL_CURRENT_MOUNT_TARGETS
      - ALL_CURRENT_FUTURE_MOUNT_TARGETS
      - ALL_FUTURE_MOUNT_TARGETS
      - NONE
  mount_target_ext_ids:
    description:
      - Mount target external identifier list to include in the tiering configuration.
      - Only used when C(mount_targets_enablement_type) is C(ALL_CURRENT_MOUNT_TARGETS) or C(NONE).
    type: list
    elements: str
    required: false
  schedule:
    description:
      - Tiering schedule for on-prem tiering.
      - Auto tiering can happen at the specified time windows.
      - If not provided, tiering runs continuously (manual + automatic).
    type: list
    elements: dict
    required: false
    suboptions:
      day_of_week:
        description:
          - Day of the week for tiering schedule.
          - C(1) starts with Sunday and C(7) is Saturday.
        type: int
        required: true
      schedules:
        description:
          - List of tiering schedule details for the given day of week.
        type: list
        elements: dict
        required: false
        suboptions:
          start_hours:
            description:
              - Start hour (0-23) of the tiering schedule for the day.
            type: int
            required: false
          start_minutes:
            description:
              - Start minute (0-59) of the tiering schedule for the day.
            type: int
            required: false
          duration_minutes:
            description:
              - Duration of the tiering schedule in minutes.
            type: int
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
- name: Create tiering configuration for file server (all future mount targets)
  nutanix.ncp.ntnx_tiering_configuration_v2:
    state: present
    file_server_ext_id: "3ec0fb37-8c1e-40b3-9d7f-3cc45f0e1234"
    memory_threshold_percent: 80
    cooloff_period_seconds: 604800
    minimum_file_size_bytes: 65536
    mount_targets_enablement_type: ALL_FUTURE_MOUNT_TARGETS
    schedule:
      - day_of_week: 1
        schedules:
          - start_hours: 0
            start_minutes: 0
            duration_minutes: 240
  register: result
  ignore_errors: true

- name: Update tiering configuration
  nutanix.ncp.ntnx_tiering_configuration_v2:
    state: present
    file_server_ext_id: "3ec0fb37-8c1e-40b3-9d7f-3cc45f0e1234"
    ext_id: "b04eef3c-4a3f-4c6d-9d2c-1cd21f18e2af"
    memory_threshold_percent: 70
    cooloff_period_seconds: 1209600
    minimum_file_size_bytes: 131072
    mount_targets_enablement_type: ALL_CURRENT_FUTURE_MOUNT_TARGETS
  register: result
  ignore_errors: true

- name: Delete tiering configuration
  nutanix.ncp.ntnx_tiering_configuration_v2:
    state: absent
    file_server_ext_id: "3ec0fb37-8c1e-40b3-9d7f-3cc45f0e1234"
    ext_id: "b04eef3c-4a3f-4c6d-9d2c-1cd21f18e2af"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting tiering configuration.
    - If the operation is create or update and C(wait) is true, it will return the tiering configuration details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
        "cooloff_period_seconds": 604800,
        "ext_id": "b04eef3c-4a3f-4c6d-9d2c-1cd21f18e2af",
        "links": null,
        "memory_threshold_percent": 80,
        "minimum_file_size_bytes": 65536,
        "mount_target_ext_ids": null,
        "mount_targets_enablement_type": "ALL_FUTURE_MOUNT_TARGETS",
        "schedule": [
            {
                "day_of_week": 1,
                "schedules": [
                    {
                        "duration_minutes": 240,
                        "start_hours": 0,
                        "start_minutes": 0
                    }
                ]
            }
        ],
        "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the tiering configuration.
  returned: always
  type: str
  sample: "b04eef3c-4a3f-4c6d-9d2c-1cd21f18e2af"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating tiering configuration"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_tier_api_instance,
)
from ..module_utils.v4.files.helpers import get_tiering_configuration  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    schedule_details_spec = dict(
        start_hours=dict(type="int", required=False),
        start_minutes=dict(type="int", required=False),
        duration_minutes=dict(type="int", required=False),
    )

    day_schedule_spec = dict(
        day_of_week=dict(type="int", required=True),
        schedules=dict(
            type="list",
            elements="dict",
            options=schedule_details_spec,
            required=False,
            obj=files_sdk.ScheduleDetails,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        memory_threshold_percent=dict(type="int"),
        cooloff_period_seconds=dict(type="int"),
        minimum_file_size_bytes=dict(type="int", default=65536),
        mount_targets_enablement_type=dict(
            type="str",
            choices=[
                "ALL_CURRENT_MOUNT_TARGETS",
                "ALL_CURRENT_FUTURE_MOUNT_TARGETS",
                "ALL_FUTURE_MOUNT_TARGETS",
                "NONE",
            ],
            obj=files_sdk.MountTargetsEnablementType,
        ),
        mount_target_ext_ids=dict(type="list", elements="str"),
        schedule=dict(
            type="list",
            elements="dict",
            options=day_schedule_spec,
            obj=files_sdk.DaySchedule,
        ),
    )
    return module_args


def _fetch_tiering_config_after_task(module, tier_api, file_server_ext_id, ext_id):
    """Fetch the tiering configuration after task completion and update result."""
    return get_tiering_configuration(module, tier_api, file_server_ext_id, ext_id)


def create_tiering_configuration(module, tier_api, result):
    validate_required_params(
        module,
        [
            "memory_threshold_percent",
            "cooloff_period_seconds",
            "mount_targets_enablement_type",
        ],
    )
    file_server_ext_id = module.params.get("file_server_ext_id")
    sg = SpecGenerator(module)
    default_spec = files_sdk.TierConfiguration()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create tiering configuration spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = tier_api.create_tiering_configuration(
            fileServerExtId=file_server_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating tiering configuration",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_resp, rel=TASK_CONSTANTS.RelEntityType.TIER_CONFIGURATION
        )
        if ext_id:
            result["ext_id"] = ext_id
            entity = _fetch_tiering_config_after_task(
                module, tier_api, file_server_ext_id, ext_id
            )
            result["response"] = strip_internal_attributes(entity.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Tiering Configuration"
                ),
                msg="Failed to get entity ext_id from task for Tiering Configuration",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    return old_spec_dict == update_spec_dict


def update_tiering_configuration(module, tier_api, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_tiering_configuration(module, tier_api, file_server_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update tiering configuration spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. Tiering configuration is already in the desired state.",
            **result,
        )

    resp = None
    try:
        resp = tier_api.update_tiering_configuration_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating tiering configuration",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        entity = _fetch_tiering_config_after_task(
            module, tier_api, file_server_ext_id, ext_id
        )
        result["response"] = strip_internal_attributes(entity.to_dict())
    result["changed"] = True


def delete_tiering_configuration(module, tier_api, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Tiering configuration with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    old_spec = get_tiering_configuration(module, tier_api, file_server_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = tier_api.delete_tiering_configuration_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting tiering configuration",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_files_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    tier_api = get_tier_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_tiering_configuration(module, tier_api, result)
        else:
            create_tiering_configuration(module, tier_api, result)
    else:
        delete_tiering_configuration(module, tier_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
