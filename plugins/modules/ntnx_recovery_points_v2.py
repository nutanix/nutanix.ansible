#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_points_v2
short_description: Create, Update, Delete  recovery points
version_added: 2.0.0
description:
    - Create, Update Expiry Date, Delete recovery points
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - The state of the recovery point, whether to create, update or delete.
            - present -> Create recovery point if external ID is not provided, Update recovery point if external ID is provided.
            - absent -> Delete recovery point using the provided recovery point external ID
        type: str
        choices: ["present", "absent"]

    ext_id:
        description:
            - External ID of the top level recovery point.
            - Required for updating expiry date and deleting recovery point.
        type: str

    name:
        description:
            - Name of the recovery point.
        type: str

    expiration_time:
        description:
            - The UTC date and time in ISO-8601 format when the current Recovery point expires.
        type: str

    recovery_point_type:
        description:
            - Type of the recovery point.
        choices: ["CRASH_CONSISTENT", "APPLICATION_CONSISTENT"]
        type: str

    vm_recovery_points:
        description:
            - List of VM recovery point that are a part of the specified top-level recovery point.
            - Note that a recovery point can contain a maximum number of 30 entities. These entities can be a combination of VM(s) and volume group(s).
        type: list
        elements: dict
        suboptions:
            vm_ext_id:
                description:
                    - VM external identifier which is captured as a part of this recovery point.
                type: str
            application_consistent_properties:
                description:
                    - User-defined application-consistent properties for the recovery point.
                type: dict
                suboptions:
                    application_consistent_properties_spec:
                        description:
                            - Application consistent properties spec.
                        type: dict
                        suboptions:
                            backup_type:
                                description:
                                    - The backup type defines the criteria for selecting files for application-consistent recovery points on Windows VMs/agents.
                                    - FULL_BACKUP, Backs up all files, updating their backup history.
                                    - COPY_BACKUP, Backs up all files without updating their backup history.
                                type: str
                                choices: ["FULL_BACKUP", "COPY_BACKUP"]
                                required: true
                            should_include_writers:
                                description:
                                    - Indicates whether the given set of VSS writers' UUIDs should be included or excluded from the \
                                        application consistent recovery point.
                                    - By default, the value is set to false, indicating that all listed VSS writers' UUIDs will be excluded.
                                type: bool
                                default: false
                            writers:
                                description:
                                    - List of VSS writer UUIDs that are used in an application consistent recovery point.
                                    - The default values are the system and the registry writer UUIDs.
                                type: list
                                elements: str
                            should_store_vss_metadata:
                                description:
                                    - Specifies whether to store VSS metadata for application-specific backup/restore.
                                    - VSS metadata, including writer and requester details, is compressed into a .cab file \
                                        during backup and must be saved for restoration.
                                type: bool
                                default: false

    volume_group_recovery_points:
        description:
            - List of volume group recovery point that are a part of the specified top-level recovery point.
            - Note that a recovery point can contain a maximum number of 30 entities. These entities can be a combination of VM(s) and volume group(s).
        type: list
        elements: dict
        suboptions:
            volume_group_ext_id:
                description:
                    - Volume Group external identifier which is captured as part of this top level recovery point.
                type: str
                required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: Create Recovery Point for 2 VMs and 2 Volume Groups
  nutanix.ncp.ntnx_recovery_points_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: present
    name: "Recovery Point 1"
    expiration_time: "2024-09-30T14:15:22Z"
    status: "COMPLETE"
    recovery_point_type: "CRASH_CONSISTENT"
    vm_recovery_points:
      - vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
      - vm_ext_id: "3f50a1b2-4c3d-4e6a-9b8e-1a2b3c4d5e6f"
    volume_group_recovery_points:
      - volume_group_ext_id: "9b8a7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d"
      - volume_group_ext_id: "2d3e4f5a-6b7c-8d9e-0f1a-2b3c4d5e6f7g"

- name: Update a Recovery Point
  nutanix.ncp.ntnx_recovery_points_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: present
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    expiration_time: "2024-11-30T14:15:22Z"

- name: Delete a Recovery Point
  nutanix.ncp.ntnx_recovery_points_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: absent
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
"""
RETURN = r"""
response:
    description:
        - Response for the recovery point operation
        - Recovery point details if C(wait) is True
        - Task details if C(wait) is False
    returned: always
    type: dict
    sample: {
            "creation_time": "2024-09-03T06:15:25.920305+00:00",
            "expiration_time": "2024-09-30T14:15:22+00:00",
            "ext_id": "d492e754-1792-41a5-8960-e2e87c8fea7d",
            "links": null,
            "location_agnostic_id": "86275d66-80e0-4744-90e9-b5ed3ff573bf",
            "location_references": [
                {
                    "location_ext_id": "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
                }
            ],
            "name": "Recovery Point 1",
            "owner_ext_id": "00000000-0000-0000-0000-000000000000",
            "recovery_point_type": "CRASH_CONSISTENT",
            "status": "COMPLETE",
            "tenant_id": null,
            "vm_recovery_points": [
                {
                    "application_consistent_properties": null,
                    "consistency_group_ext_id": null,
                    "disk_recovery_points": [
                        {
                            "disk_ext_id": "14caad84-02e8-4425-8604-4e492ad89fa3",
                            "disk_recovery_point_ext_id": "94e61902-1954-4d54-917a-a28205454fce"
                        },
                        {
                            "disk_ext_id": "870fa4d7-0999-4d39-91b7-c51640e3704c",
                            "disk_recovery_point_ext_id": "7e96075e-4786-4409-82bd-764e23d877a6"
                        }
                    ],
                    "ext_id": "d06acb73-b057-4f47-85b9-43ddaf8726a5",
                    "links": null,
                    "location_agnostic_id": "a71ac990-70f4-4552-96c3-6031215d4bbb",
                    "tenant_id": null,
                    "vm_categories": null,
                    "vm_ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
                }
            ],
            "volume_group_recovery_points": null
        }
task_ext_id:
    description: The task external ID for the operation.
    returned: always
    type: str
    sample: "ZXJnb24=:7cdb5481-dade-44a9-8239-7afbde1c1b82"
ext_id:
    description: The external ID of the top level recovery point.
    returned: always
    type: str
    sample: "d492e754-1792-41a5-8960-e2e87c8fea7d"
error:
    description: The error message if an error occurs.
    type: str
    returned: when an error occurs
    sample: "Error occurred while creating recovery point"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
warning:
    description: Warning message if any
    type: str
    returned: when a warning occurs
    sample: "Only Expiration time Updation is allowed. Can't update other fields."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402
from datetime import datetime  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_etag,
    get_recovery_point_api_instance,
)
from ..module_utils.v4.data_protection.helpers import get_recovery_point  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_ext_id_from_task_completion_details,
    wait_for_completion,
)
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    application_consistent_properties_obj_map = {
        "application_consistent_properties_spec": data_protection_sdk.VssProperties,
    }
    application_consistent_properties_sub_spec = dict(
        backup_type=dict(
            type="str", choices=["FULL_BACKUP", "COPY_BACKUP"], required=True
        ),
        should_include_writers=dict(type="bool", default=False),
        writers=dict(type="list", elements="str"),
        should_store_vss_metadata=dict(type="bool", default=False),
    )

    vm_recovery_points_sub_spec = dict(
        vm_ext_id=dict(type="str"),
        application_consistent_properties=dict(
            type="dict",
            options=dict(
                application_consistent_properties_spec=dict(
                    type="dict", options=application_consistent_properties_sub_spec
                )
            ),
            obj=application_consistent_properties_obj_map,
        ),
    )

    volume_group_recovery_points_sub_spec = dict(
        volume_group_ext_id=dict(type="str", required=True),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        state=dict(type="str", choices=["present", "absent"], default="present"),
        name=dict(type="str"),
        expiration_time=dict(type="str"),
        recovery_point_type=dict(
            type="str",
            choices=[
                "CRASH_CONSISTENT",
                "APPLICATION_CONSISTENT",
            ],
        ),
        vm_recovery_points=dict(
            type="list",
            elements="dict",
            options=vm_recovery_points_sub_spec,
            obj=data_protection_sdk.VmRecoveryPoint,
        ),
        volume_group_recovery_points=dict(
            type="list",
            elements="dict",
            options=volume_group_recovery_points_sub_spec,
            obj=data_protection_sdk.VolumeGroupRecoveryPoint,
        ),
    )
    return module_args


def create_recovery_point(module, result):
    recovery_points = get_recovery_point_api_instance(module)
    sg = SpecGenerator(module)
    default_spec = data_protection_sdk.RecoveryPoint()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create recovery point Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return
    try:
        resp = recovery_points.create_recovery_point(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating recovery point",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_ext_id_from_task_completion_details(
            task_status, name=TASK_CONSTANTS.CompletetionDetailsName.RECOVERY_POINT
        )
        if ext_id:
            resp = get_recovery_point(module, recovery_points, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def check_recovery_point_idempotency_without_expiration(old_spec, update_spec):
    old_spec.pop("expiration_time")
    update_spec.pop("expiration_time")
    return old_spec == update_spec


def update_expiry_date_recovery_point(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    recovery_points = get_recovery_point_api_instance(module)
    old_spec = get_recovery_point(module, recovery_points, ext_id)

    etag_value = get_etag(data=old_spec)
    if not etag_value:
        return module.fail_json(
            "Unable to fetch etag for Updating Expiry Date", **result
        )
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update recovery point Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    old_expiration_time = old_spec.to_dict().get("expiration_time")
    new_expiration_time = module.params.get("expiration_time")

    if new_expiration_time is None:
        result[
            "error"
        ] = "Expiration time is required for updating recovery point and other fields can't be updated."
        module.fail_json(msg="Expiration time is required", **result)

    if int(old_expiration_time.timestamp()) == int(
        datetime.fromisoformat(
            new_expiration_time
        ).timestamp()  # Converted time to epochs
    ):
        if not check_recovery_point_idempotency_without_expiration(
            old_spec.to_dict(), update_spec.to_dict()
        ):
            result["skipped"] = True
            msg = "Update of other operations is not supported. Only updation of Expiration time is allowed."
            module.exit_json(msg=msg, **result)
        else:
            result["skipped"] = True
            module.exit_json(msg="Nothing to change.", **result)
    elif not check_recovery_point_idempotency_without_expiration(
        old_spec.to_dict(), update_spec.to_dict()
    ):
        result[
            "warning"
        ] = "Only Expiration time Updation is allowed. Can't update other fields."

    expirationTimeSpec = data_protection_sdk.ExpirationTimeSpec()
    expirationTimeSpec.expiration_time = new_expiration_time

    resp = None
    try:
        resp = recovery_points.set_recovery_point_expiration_time(
            extId=ext_id, body=expirationTimeSpec, if_match=etag_value
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating recovery point",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        resp = get_recovery_point(module, recovery_points, ext_id)
        result["ext_id"] = ext_id
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_recovery_point(module, result):
    recovery_points = get_recovery_point_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_recovery_point(module, recovery_points, ext_id)

    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for Deletion", **result)

    kwargs = {"if_match": etag}

    try:
        resp = recovery_points.delete_recovery_point_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting recovery point",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            (
                "state",
                "absent",
                ("ext_id",),
            ),
        ],
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
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_expiry_date_recovery_point(module, result)
        else:
            create_recovery_point(module, result)
    else:
        delete_recovery_point(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
