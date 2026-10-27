#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_recovery_point_v2
short_description: Create or delete an AHV VM recovery point in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create or delete an AHV VM recovery point in Nutanix Prism Central.
  - The AHV VM recovery point API does not support update. When C(ext_id) is provided with
    C(state=present), the module fetches the existing recovery point and reports skipped.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation. The required roles depend on the operation
    being performed.
  - >-
    B(Create AHV VM recovery point) -
    Required Roles: Account Owner, Administrator, Prism Admin, Super Admin,
    Virtual Machine Admin, Disaster Recovery Admin, Backup Admin, Project Manager,
    Project Admin, Tenant Admin, Tenant Consumer, Self-Service Admin (deprecated)
  - >-
    B(Delete AHV VM recovery point) -
    Required Roles: Account Owner, Administrator, Prism Admin, Super Admin,
    Virtual Machine Admin, Disaster Recovery Admin, Backup Admin, Project Manager,
    Project Admin, Tenant Admin, Tenant Consumer, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create an AHV VM recovery point.
      - If C(state) is set to C(present) and C(ext_id) is provided then the module fetches the existing recovery point
        (update is not supported by the API).
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the AHV VM recovery point.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - A globally unique identifier of an AHV VM recovery point. It should be of type UUID.
      - Required for delete operation.
    type: str
    required: false
  name:
    description:
      - The name of the recovery point.
      - Required for the create operation.
    type: str
    required: false
  expiration_time:
    description:
      - The UTC date and time in ISO-8601 format when the current recovery point expires and will be removed.
    type: str
    required: false
  recovery_point_type:
    description:
      - Type of the recovery point.
    type: str
    choices:
      - CRASH_CONSISTENT
      - APPLICATION_CONSISTENT
    required: false
  vm_ext_id:
    description:
      - VM external identifier which is captured as a part of this recovery point.
      - Required for the create operation.
    type: str
    required: false
  project_ext_id:
    description:
      - A globally unique identifier for the project associated with the resource.
      - This field is required in create requests for authorization and must match the project
        identifier of all associated entities.
    type: str
    required: false
  application_consistent_properties:
    description:
      - User-defined application-consistent properties for the recovery point.
    type: dict
    required: false
    suboptions:
      backup_type:
        description:
          - The backup type specifies the criteria for identifying the files to be backed up.
          - This property should be specified to the application-consistent recovery points for Windows VMs/agents.
          - C(FULL_BACKUP) - All files are backed up irrespective of their last backup date/time and state.
            Also, this backup type updates the backup history of every file that was involved in the recovery point.
          - C(COPY_BACKUP) - All files are backed up regardless of their last backup date/time and state.
            However, this backup type does not update the backup history of individual files involved in the recovery point.
        type: str
        choices:
          - FULL_BACKUP
          - COPY_BACKUP
        required: true
      should_include_writers:
        description:
          - Indicates whether the given set of VSS writers' UUIDs should be included or excluded
            from the application consistent recovery point.
          - By default, the value is set to false, indicating that all listed VSS writers' UUIDs will be excluded.
        type: bool
        required: false
        default: false
      writers:
        description:
          - List of VSS writer UUIDs that are used in an application consistent recovery point.
          - The default values are the system and the registry writer UUIDs.
        type: list
        elements: str
        required: false
      should_store_vss_metadata:
        description:
          - Indicates whether to store the VSS metadata if the user is interested in
            application-specific backup/restore.
        type: bool
        required: false
        default: false
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
- name: Create a crash consistent AHV VM recovery point
  nutanix.ncp.ntnx_vm_recovery_point_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "ansible-vm-rp"
    expiration_time: "2027-01-01T00:00:00+00:00"
    recovery_point_type: "CRASH_CONSISTENT"
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
  register: result
  ignore_errors: true

- name: Create an application consistent AHV VM recovery point
  nutanix.ncp.ntnx_vm_recovery_point_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "ansible-vm-rp-app"
    expiration_time: "2027-01-01T00:00:00+00:00"
    recovery_point_type: "APPLICATION_CONSISTENT"
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    application_consistent_properties:
      backup_type: "FULL_BACKUP"
      should_include_writers: true
      writers:
        - "0f95b402-67aa-431c-9eab-bf0907a99345"
      should_store_vss_metadata: true
  register: result
  ignore_errors: true

- name: Delete an AHV VM recovery point
  nutanix.ncp.ntnx_vm_recovery_point_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "b387359d-fa5c-4d58-9eb2-3af1a4976319"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating or deleting an AHV VM recovery point.
    - If the operation is create and C(wait) is C(true) it returns the AHV VM recovery point details.
    - If the operation is create and C(wait) is C(false) it returns the task details.
    - If the operation is delete it returns the task details.
  returned: always
  type: dict
  sample:
    {
      "application_consistent_properties": null,
      "creation_time": "2026-07-21T05:12:31.912+00:00",
      "disk_recovery_points": [
        {
          "disk_ext_id": "839feff9-bac0-4a70-9523-82ea9e431517",
          "disk_recovery_point_ext_id": "21d467f0-ccef-4733-91cc-f04db58a92eb"
        }
      ],
      "expiration_time": "2027-01-01T00:00:00+00:00",
      "ext_id": "b387359d-fa5c-4d58-9eb2-3af1a4976319",
      "links": null,
      "location_agnostic_id": "51264897-07a8-4292-831b-ae28a37135e5",
      "name": "ansible-vm-rp",
      "recovery_point_type": "CRASH_CONSISTENT",
      "status": "COMPLETE",
      "tenant_id": null,
      "vm_ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    }

task_ext_id:
  description: The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description: The external ID of the AHV VM recovery point.
  returned: always
  type: str
  sample: "b387359d-fa5c-4d58-9eb2-3af1a4976319"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: when the module is idempotent
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
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "AHV VM recovery point with ext_id:b387359d-fa5c-4d58-9eb2-3af1a4976319 will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
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
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_recovery_points_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_vm_recovery_point  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    vss_properties_sub_spec = dict(
        backup_type=dict(
            type="str",
            choices=["FULL_BACKUP", "COPY_BACKUP"],
            required=True,
            obj=vmm_sdk.BackupType,
        ),
        should_include_writers=dict(type="bool", required=False, default=False),
        writers=dict(type="list", elements="str", required=False),
        should_store_vss_metadata=dict(type="bool", required=False, default=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        expiration_time=dict(type="str"),
        recovery_point_type=dict(
            type="str",
            choices=["CRASH_CONSISTENT", "APPLICATION_CONSISTENT"],
            obj=vmm_sdk.RecoveryPointType,
        ),
        vm_ext_id=dict(type="str"),
        project_ext_id=dict(type="str"),
        application_consistent_properties=dict(
            type="dict",
            options=vss_properties_sub_spec,
            obj=vmm_sdk.VssProperties,
        ),
    )
    return module_args


def create_vm_recovery_point(module, result):
    validate_required_params(module, ["name", "vm_ext_id"])
    api_instance = get_vm_recovery_points_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.VmRecoveryPoint()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating AHV VM recovery point create spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_vm_recovery_point(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating AHV VM recovery point",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.VM_RECOVERY_POINT
        )
        if ext_id:
            result["ext_id"] = ext_id
            entity = get_vm_recovery_point(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(entity.to_dict())
    result["changed"] = True


def get_existing_vm_recovery_point(module, result):
    """Fetch existing recovery point when present+ext_id (API has no update)."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    api_instance = get_vm_recovery_points_api_instance(module)
    entity = get_vm_recovery_point(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(entity.to_dict())
    result["skipped"] = True
    module.exit_json(
        msg=(
            "AHV VM recovery point does not support update. "
            "Existing recovery point with ext_id '{0}' has been fetched.".format(ext_id)
        ),
        **result,
    )


def delete_vm_recovery_point(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    api_instance = get_vm_recovery_points_api_instance(module)

    if module.check_mode:
        result["msg"] = "AHV VM recovery point with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.delete_vm_recovery_point_by_ext_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting AHV VM recovery point",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            get_existing_vm_recovery_point(module, result)
        else:
            create_vm_recovery_point(module, result)
    else:
        delete_vm_recovery_point(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
