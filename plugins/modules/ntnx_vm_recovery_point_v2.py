#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_recovery_point_v2
short_description: Create, Delete AHV VM recovery points in Nutanix Prism Central
version_added: 2.7.0
description:
    - Create and Delete AHV VM recovery points using the vmm v4.2 AHV
      VmRecoveryPoints API.
    - AHV VM recovery points are immutable point-in-time snapshots of an AHV VM.
      They cannot be updated once created; providing C(ext_id) with
      C(state=present) will therefore result in a no-op skipped result.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation. The required roles depend on the operation
      being performed.
    - >-
      B(Create an AHV VM Recovery Point) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin,
      Kubernetes Data Services System, NCM Connector, Prism Admin,
      Project Manager, Super Admin, Self-Service Admin (deprecated)
    - >-
      B(Delete an AHV VM Recovery Point) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin,
      Kubernetes Data Services System, NCM Connector, Prism Admin,
      Project Manager, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - If C(state) is set to C(present) and C(ext_id) is not provided
              then the operation will be create AHV VM recovery point.
            - If C(state) is set to C(present) and C(ext_id) is provided the
              module will report the recovery point as immutable and skip
              (AHV VM recovery points cannot be updated).
            - If C(state) is set to C(absent) and C(ext_id) is provided the
              operation will delete the AHV VM recovery point.
        type: str
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - External ID (UUID) of the AHV VM recovery point.
            - Required for delete operation.
        type: str
    name:
        description:
            - User-visible name of the AHV VM recovery point.
            - Required for create operation.
        type: str
    vm_ext_id:
        description:
            - External ID (UUID) of the source AHV VM that will be captured in
              the recovery point.
            - Required for create operation.
        type: str
    expiration_time:
        description:
            - The UTC date and time in ISO-8601 format when the recovery point
              expires. Once expired, the recovery point is eligible for
              garbage collection.
        type: str
    recovery_point_type:
        description:
            - The type of the recovery point.
            - C(CRASH_CONSISTENT) captures the VM state without quiescing the
              guest.
            - C(APPLICATION_CONSISTENT) requires the guest VM to be Windows
              with NGT installed and VSS enabled; the guest is quiesced via
              VSS before the snapshot is taken.
        type: str
        choices:
            - CRASH_CONSISTENT
            - APPLICATION_CONSISTENT
        default: CRASH_CONSISTENT
    consistency_group_ext_id:
        description:
            - External ID (UUID) of the consistency group this recovery point
              belongs to. Used to group recovery points of related entities.
        type: str
    vm_categories:
        description:
            - List of category external IDs (UUIDs) applied to the VM at the
              time of the recovery point.
        type: list
        elements: str
    application_consistent_properties:
        description:
            - Application-consistent (VSS) properties used when
              C(recovery_point_type=APPLICATION_CONSISTENT).
            - Only applicable to Windows VMs with NGT and VSS enabled.
        type: dict
        suboptions:
            backup_type:
                description:
                    - The backup type that defines the criteria for selecting
                      files for application-consistent recovery points on
                      Windows VMs/agents.
                    - C(FULL_BACKUP) - backs up all files and updates their
                      backup history.
                    - C(COPY_BACKUP) - backs up all files without updating
                      their backup history.
                type: str
                choices:
                    - FULL_BACKUP
                    - COPY_BACKUP
                required: true
            should_include_writers:
                description:
                    - Whether the listed VSS writer UUIDs should be included
                      or excluded from the application-consistent recovery
                      point. Defaults to false (writers are excluded).
                type: bool
                default: false
            writers:
                description:
                    - List of VSS writer UUIDs used in an application
                      consistent recovery point.
                type: list
                elements: str
            should_store_vss_metadata:
                description:
                    - Whether to store VSS metadata for application-specific
                      backup/restore.
                type: bool
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
- name: Create a crash-consistent AHV VM recovery point
  nutanix.ncp.ntnx_vm_recovery_point_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "ansible_vm_rp_crash"
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    recovery_point_type: "CRASH_CONSISTENT"
    expiration_time: "2027-01-01T00:00:00Z"
  register: create_result

- name: Create an application-consistent AHV VM recovery point (Windows + VSS)
  nutanix.ncp.ntnx_vm_recovery_point_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "ansible_vm_rp_app"
    vm_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    recovery_point_type: "APPLICATION_CONSISTENT"
    expiration_time: "2027-01-01T00:00:00Z"
    vm_categories:
      - "16b7f7ea-40c7-4bde-9b1c-8e7d3b3f6a90"
    application_consistent_properties:
      backup_type: "FULL_BACKUP"
      should_include_writers: true
      writers:
        - "e8132975-6d3a-4d67-807e-8d0d5b8e0b8b"
      should_store_vss_metadata: true
  register: create_app_result

- name: Delete an AHV VM recovery point
  nutanix.ncp.ntnx_vm_recovery_point_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "b387359d-fa5c-4d58-9eb2-3af1a4976319"
  register: delete_result
"""

RETURN = r"""
response:
    description:
        - Response for creating or deleting an AHV VM recovery point.
        - For create when C(wait=true), the fetched AHV VM recovery point details.
        - For create when C(wait=false), the task details.
        - For delete, the task details.
    returned: always
    type: dict
    sample:
        {
            "application_consistent_properties": null,
            "consistency_group_ext_id": null,
            "creation_time": "2026-07-20T22:35:00.000Z",
            "disk_recovery_points": [
                {
                    "disk_ext_id": "839feff9-bac0-4a70-9523-82ea9e431517",
                    "disk_recovery_point_ext_id": "21d467f0-ccef-4733-91cc-f04db58a92eb"
                }
            ],
            "expiration_time": "2027-01-01T00:00:00Z",
            "ext_id": "b387359d-fa5c-4d58-9eb2-3af1a4976319",
            "links": null,
            "location_agnostic_id": "51264897-07a8-4292-831b-ae28a37135e5",
            "name": "ansible_vm_rp_crash",
            "recovery_point_type": "CRASH_CONSISTENT",
            "status": "COMPLETE",
            "tenant_id": null,
            "total_exclusive_usage_bytes": 0,
            "vm": null,
            "vm_categories": null,
            "vm_ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
        }

task_ext_id:
    description: The external ID of the task performing the operation.
    returned: always
    type: str
    sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
    description:
        - The external ID (UUID) of the AHV VM recovery point.
        - Set for create (after C(wait_for_completion)) and delete.
    returned: always
    type: str
    sample: "b387359d-fa5c-4d58-9eb2-3af1a4976319"

changed:
    description: Whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

skipped:
    description:
        - Whether the operation was skipped (recovery points are immutable so
          "update" is always a no-op).
    returned: When the operation is skipped
    type: bool
    sample: false

failed:
    description: Whether the operation failed.
    returned: always
    type: bool
    sample: false

error:
    description: Error message set on failure.
    returned: When an error occurs
    type: str

msg:
    description: Additional status/context message.
    returned: When present (idempotent skip, check mode, or error)
    type: str
    sample: "AHV VM recovery point with ext_id:b387359d... will be deleted."
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
    get_etag,
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

    application_consistent_properties_spec = dict(
        backup_type=dict(
            type="str",
            choices=["FULL_BACKUP", "COPY_BACKUP"],
            required=True,
        ),
        should_include_writers=dict(type="bool", default=False),
        writers=dict(type="list", elements="str"),
        should_store_vss_metadata=dict(type="bool", default=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        vm_ext_id=dict(type="str"),
        expiration_time=dict(type="str"),
        recovery_point_type=dict(
            type="str",
            choices=["CRASH_CONSISTENT", "APPLICATION_CONSISTENT"],
            default="CRASH_CONSISTENT",
        ),
        consistency_group_ext_id=dict(type="str"),
        vm_categories=dict(type="list", elements="str"),
        application_consistent_properties=dict(
            type="dict",
            options=application_consistent_properties_spec,
            obj=vmm_sdk.VssProperties,
        ),
    )
    return module_args


def _build_create_spec(module):
    """Build a VmRecoveryPoint SDK spec from module params.

    ``SpecGenerator`` cannot populate the ``OneOf`` field
    ``application_consistent_properties`` on its own, so we handle that
    attribute explicitly with a ``VssProperties`` object.
    """
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.VmRecoveryPoint()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        return None, err

    acp = module.params.get("application_consistent_properties")
    if acp:
        vss = vmm_sdk.VssProperties()
        vss.backup_type = acp.get("backup_type")
        vss.should_include_writers = acp.get("should_include_writers")
        vss.writers = acp.get("writers")
        vss.should_store_vss_metadata = acp.get("should_store_vss_metadata")
        spec.application_consistent_properties = vss
    return spec, None


def create_vm_recovery_point(module, result, api_instance):
    validate_required_params(module, ["name", "vm_ext_id"])
    spec, err = _build_create_spec(module)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating AHV VM recovery point create spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

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
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task, rel=TASK_CONSTANTS.RelEntityType.VM_RECOVERY_POINT
        )
        if ext_id:
            result["ext_id"] = ext_id
            fetched = get_vm_recovery_point(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(fetched.data.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for AHV VM recovery point"
                ),
                msg="Failed to get entity ext_id from task for AHV VM recovery point",
            )
    result["changed"] = True


def update_vm_recovery_point(module, result, api_instance):
    """AHV VM recovery points are immutable — no-op with informative skip."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current = get_vm_recovery_point(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(current.data.to_dict())

    if module.check_mode:
        result["msg"] = (
            "AHV VM recovery points are immutable; ext_id:{0} cannot be updated. "
            "No changes will be made.".format(ext_id)
        )
        return

    result["skipped"] = True
    module.exit_json(
        msg=(
            "AHV VM recovery points are immutable; ext_id:{0} cannot be updated. "
            "Nothing to change.".format(ext_id)
        ),
        **result,
    )


def delete_vm_recovery_point(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "AHV VM recovery point with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    current = get_vm_recovery_point(module, api_instance, ext_id)
    etag = get_etag(current)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    try:
        resp = api_instance.delete_vm_recovery_point_by_ext_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting AHV VM recovery point",
        )

    task_ext_id = getattr(getattr(resp, "data", None), "ext_id", None)
    if task_ext_id:
        result["task_ext_id"] = task_ext_id
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        if module.params.get("wait"):
            task = wait_for_completion(module, task_ext_id, True)
            result["response"] = strip_internal_attributes(task.to_dict())
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
            msg=missing_required_lib("ntnx_vmm_py_client"),
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
    api_instance = get_vm_recovery_points_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_vm_recovery_point(module, result, api_instance)
        else:
            create_vm_recovery_point(module, result, api_instance)
    else:
        delete_vm_recovery_point(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
