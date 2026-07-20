#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_stage_v2
short_description: Create, Update, Delete a Recovery stage in a Nutanix Recovery Plan
version_added: 2.7.0
description:
  - This module allows you to create, update and delete a Recovery stage inside a Recovery Plan in Nutanix Prism Central.
  - A Recovery stage defines a group of VMs or Volume Groups to be recovered together during a disaster recovery event.
  - Recovery stages control the boot / power-on ordering of entities during a failover.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation. The required roles depend on the operation
    being performed.
  - >-
    B(Create a Recovery stage) -
    Required Roles: Account Owner, Administrator, Disaster Recovery Admin, NCM Connector, Prism Admin, Project Manager, Super Admin
  - >-
    B(Update a Recovery stage) -
    Required Roles: Account Owner, Administrator, Disaster Recovery Admin, NCM Connector, Prism Admin, Project Manager, Super Admin
  - >-
    B(Delete a Recovery stage) -
    Required Roles: Account Owner, Administrator, Disaster Recovery Admin, NCM Connector, Prism Admin, Project Manager, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create Recovery stage.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update Recovery stage.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete Recovery stage.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  recovery_plan_ext_id:
    description:
      - External identifier of the parent Recovery Plan under which the Recovery stage resides.
      - Required for all Create, Update, Delete operations.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the Recovery stage.
      - Required for update and delete operations.
    type: str
    required: false
  entity_type:
    description:
      - Type of entities that are recovered as part of this Recovery stage.
      - This field is required for Create operation.
    type: str
    required: false
    choices:
      - VM
      - VOLUME_GROUP
  entities:
    description:
      - List of external references of entities of type I(entity_type) to be recovered in the Recovery stage.
      - Mutually exclusive with C(category_ext_ids) at the API level for VM stages.
    type: list
    elements: dict
    required: false
    suboptions:
      ext_id:
        description:
          - External identifier of the referenced entity (VM or Volume Group).
        type: str
        required: true
      name:
        description:
          - Name of the referenced entity.
        type: str
        required: false
  category_ext_ids:
    description:
      - List of external identifiers of categories for which entities of I(entity_type)
        are to be recovered in the Recovery stage.
    type: list
    elements: str
    required: false
  priority:
    description:
      - Recovery priority of the Stage. Determines the shutdown and power-on order of the VMs.
      - Only priority value of 1 is acceptable for I(entity_type=VOLUME_GROUP).
      - Minimum value is 1.
    type: int
    required: false
  post_actions:
    description:
      - List of actions to be executed after completion of the stage.
    type: list
    elements: dict
    required: false
    suboptions:
      config:
        description:
          - Configuration of the stage action.
        type: dict
        required: true
        suboptions:
          delay_action:
            description:
              - Configuration for a DELAY stage action.
              - Instructs the Recovery plan to wait for the configured seconds after this stage completes.
            type: dict
            required: false
            suboptions:
              delay_secs:
                description:
                  - Number of seconds by which the Recovery plan is delayed after this stage completes.
                  - Minimum value is 1.
                type: int
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
- name: Create a Recovery stage for VMs (single VM, priority 1)
  nutanix.ncp.ntnx_recovery_stage_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    recovery_plan_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    entity_type: "VM"
    entities:
      - ext_id: "9e9c7f6a-4b28-4d5f-a1d9-1f1b3a92aa11"
        name: "webserver-vm"
    priority: 1
    post_actions:
      - config:
          delay_action:
            delay_secs: 30
  register: result

- name: Create a Recovery stage for Volume Groups (using categories)
  nutanix.ncp.ntnx_recovery_stage_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    recovery_plan_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    entity_type: "VOLUME_GROUP"
    category_ext_ids:
      - "bbc3555a-133b-5348-9764-bfff196e84e4"
    priority: 1
  register: result

- name: Update Recovery stage - change priority and update post actions
  nutanix.ncp.ntnx_recovery_stage_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    recovery_plan_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    ext_id: "1ab8a1c3-2ff9-4b57-b6ce-2e6c74aaa72c"
    entity_type: "VM"
    entities:
      - ext_id: "9e9c7f6a-4b28-4d5f-a1d9-1f1b3a92aa11"
    priority: 2
    post_actions:
      - config:
          delay_action:
            delay_secs: 60
  register: result

- name: Delete Recovery stage
  nutanix.ncp.ntnx_recovery_stage_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    recovery_plan_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    ext_id: "1ab8a1c3-2ff9-4b57-b6ce-2e6c74aaa72c"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating or deleting a Recovery stage.
    - If the operation is create or update and C(wait) is true, it will return the Recovery stage details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "category_ext_ids": null,
      "entities": [
        {
          "ext_id": "9e9c7f6a-4b28-4d5f-a1d9-1f1b3a92aa11",
          "name": "webserver-vm"
        }
      ],
      "entity_type": "VM",
      "ext_id": "1ab8a1c3-2ff9-4b57-b6ce-2e6c74aaa72c",
      "links": null,
      "post_actions": [
        {
          "config": {
            "delay_secs": 30
          }
        }
      ],
      "priority": 1,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external identifier of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external identifier of the Recovery stage.
  returned: always
  type: str
  sample: "1ab8a1c3-2ff9-4b57-b6ce-2e6c74aaa72c"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency.
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating recovery stage"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_etag,
    get_recovery_plans_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_recovery_stage  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_datapolicies_py_client as data_policies_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_policies_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    entity_reference_spec = dict(
        ext_id=dict(type="str", required=True),
        name=dict(type="str", required=False),
    )

    delay_action_spec = dict(
        delay_secs=dict(type="int", required=True),
    )

    config_obj_map = {
        "delay_action": data_policies_sdk.DelayAction,
    }

    config_spec = dict(
        delay_action=dict(
            type="dict",
            options=delay_action_spec,
            required=False,
        ),
    )

    stage_action_spec = dict(
        config=dict(
            type="dict",
            options=config_spec,
            obj=config_obj_map,
            required=True,
        ),
    )

    module_args = dict(
        recovery_plan_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
        entity_type=dict(
            type="str",
            required=False,
            choices=["VM", "VOLUME_GROUP"],
            obj=data_policies_sdk.RecoverableEntityType,
        ),
        entities=dict(
            type="list",
            elements="dict",
            options=entity_reference_spec,
            required=False,
            obj=data_policies_sdk.EntityReference,
        ),
        category_ext_ids=dict(
            type="list",
            elements="str",
            required=False,
        ),
        priority=dict(type="int", required=False),
        post_actions=dict(
            type="list",
            elements="dict",
            options=stage_action_spec,
            required=False,
            obj=data_policies_sdk.StageAction,
        ),
    )

    return module_args


def create_RecoveryStage(module, result, api_instance):
    validate_required_params(module, ["entity_type"])

    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    sg = SpecGenerator(module)
    default_spec = data_policies_sdk.RecoveryStage()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create recovery stage spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.create_recovery_stage(
            recoveryPlanExtId=recovery_plan_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating recovery stage",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_data = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_data.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_data, rel=TASK_CONSTANTS.RelEntityType.RECOVERY_STAGE
        )
        if ext_id:
            result["ext_id"] = ext_id
            fetched = get_recovery_stage(
                module, api_instance, recovery_plan_ext_id, ext_id
            )
            result["response"] = strip_internal_attributes(fetched.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Recovery Stage"
                ),
                msg="Failed to get entity ext_id from task for Recovery Stage",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    return old_spec_dict == update_spec_dict


def update_RecoveryStage(module, result, api_instance):
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_recovery_stage(module, api_instance, recovery_plan_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating recovery stage", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update recovery stage spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change.",
            **result,
        )

    strip_read_only_fields(update_spec, fields=["links", "tenant_id"])

    kwargs = {"if_match": etag}
    try:
        resp = api_instance.update_recovery_stage_by_id(
            recoveryPlanExtId=recovery_plan_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating recovery stage",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        fetched = get_recovery_stage(module, api_instance, recovery_plan_ext_id, ext_id)
        result["response"] = strip_internal_attributes(fetched.to_dict())
    result["changed"] = True


def delete_RecoveryStage(module, result, api_instance):
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Recovery stage with ext_id:{0} will be deleted.".format(ext_id)
        return

    # Fetch the existing entity to obtain the etag, which the DELETE API requires
    # via the if_match header (missing etag returns HTTP 428).
    old_spec = get_recovery_stage(module, api_instance, recovery_plan_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for deleting recovery stage", **result
        )
    kwargs = {"if_match": etag}
    try:
        resp = api_instance.delete_recovery_stage_by_id(
            recoveryPlanExtId=recovery_plan_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting recovery stage",
        )
    task_ext_id = resp.data.ext_id if resp and resp.data else None
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, raise_error=True)
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
            msg=missing_required_lib("ntnx_datapolicies_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_recovery_plans_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_RecoveryStage(module, result, api_instance)
        else:
            create_RecoveryStage(module, result, api_instance)
    else:
        delete_RecoveryStage(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
