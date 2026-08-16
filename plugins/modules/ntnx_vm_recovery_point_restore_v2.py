#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_recovery_point_restore_v2
short_description: Restore a new AHV VM from an AHV VM recovery point
version_added: 2.7.0
description:
    - Restore a new AHV VM from an existing AHV VM recovery point.
    - A brand new VM is created from the recovery point; the operation does
      not modify the source VM.
    - Optional overrides let you rename the restored VM, override its
      description, categories, NICs, guest tools state and ownership info.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Restore an AHV VM recovery point) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin,
      Kubernetes Data Services System, NCM Connector, Prism Admin,
      Project Manager, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present) the module will restore a VM from the
              recovery point.
            - Any other value causes the module to fail (only C(present) is
              supported for action modules).
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - External ID (UUID) of the AHV VM recovery point to restore.
        type: str
        required: true
    is_strict_mode:
        description:
            - When true, the restore operation fails if any of the requested
              override entities cannot be honored exactly.
            - When false, the API restores on a best-effort basis and may
              silently drop overrides that cannot be applied.
        type: bool
    vm_config_override_spec:
        description:
            - Overrides applied to the restored VM. All fields are optional
              and default to the values captured in the recovery point.
        type: dict
        suboptions:
            name:
                description:
                    - Name for the restored VM. If not provided the original
                      VM name from the recovery point is used.
                type: str
            description:
                description:
                    - Description for the restored VM. If not provided the
                      original description is used.
                type: str
            categories:
                description:
                    - Category references to attach to the restored VM.
                type: list
                elements: dict
                suboptions:
                    ext_id:
                        description:
                            - External ID (UUID) of the category.
                        type: str
                        required: true
            nic_spec:
                description:
                    - NIC override specification for the restored VM. Lets
                      you skip specific NICs from the recovery point or
                      override individual NIC attributes such as subnet.
                type: dict
                suboptions:
                    nic_remove_list:
                        description:
                            - List of NIC external IDs (from the recovery
                              point) to skip when restoring.
                        type: list
                        elements: str
                    nic_override_list:
                        description:
                            - List of per-NIC overrides applied to the
                              restored VM.
                        type: list
                        elements: dict
                        suboptions:
                            nic_ext_id:
                                description:
                                    - External ID of the NIC from the
                                      recovery point to override.
                                type: str
                                required: true
                            subnet_ext_id:
                                description:
                                    - External ID of the subnet the NIC
                                      should be attached to on restore.
                                type: str
            guest_tools_spec:
                description:
                    - Guest Tools override configuration applied to the
                      restored VM.
                type: dict
                suboptions:
                    should_clear_in_guest_volume_group_attachments:
                        description:
                            - When true, in-guest volume-group attachments
                              (typically discovered through NGT) are cleared
                              on restore.
                        type: bool
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
- name: Restore a new AHV VM from a recovery point (defaults)
  nutanix.ncp.ntnx_vm_recovery_point_restore_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b387359d-fa5c-4d58-9eb2-3af1a4976319"
  register: restore_result

- name: Restore a new AHV VM with overrides
  nutanix.ncp.ntnx_vm_recovery_point_restore_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b387359d-fa5c-4d58-9eb2-3af1a4976319"
    is_strict_mode: true
    vm_config_override_spec:
      name: "ansible_restored_vm"
      description: "Restored by Ansible integration test"
      categories:
        - ext_id: "16b7f7ea-40c7-4bde-9b1c-8e7d3b3f6a90"
      nic_spec:
        nic_remove_list:
          - "cf0f8020-0d3d-4c9c-bad7-2d7d1e1caa00"
        nic_override_list:
          - nic_ext_id: "d5b0aa5f-42d2-4cd3-a11c-4a4d0ec6a4d5"
            subnet_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
      guest_tools_spec:
        should_clear_in_guest_volume_group_attachments: true
  register: restore_result_overrides
"""

RETURN = r"""
response:
    description:
        - Response for restoring the AHV VM recovery point.
        - Task details if C(wait) is true.
        - Async task submit response if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-20T22:45:11.524581+00:00",
            "completion_details": [
                {
                    "name": "vmExtId",
                    "value": "e44621b1-da4e-40d1-87b1-cbb640001347"
                }
            ],
            "created_time": "2026-07-20T22:45:07.167906+00:00",
            "entities_affected": [
                {
                    "ext_id": "b387359d-fa5c-4d58-9eb2-3af1a4976319",
                    "rel": "dataprotection:config:vm-recovery-point"
                },
                {
                    "ext_id": "e44621b1-da4e-40d1-87b1-cbb640001347",
                    "rel": "vmm:ahv:config:vm"
                }
            ],
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "operation": "RestoreVmRecoveryPoint",
            "operation_description": "Restore AHV VM Recovery Point",
            "progress_percentage": 100,
            "status": "SUCCEEDED"
        }

task_ext_id:
    description: External ID of the task performing the restore.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: External ID of the AHV VM recovery point being restored.
    returned: always
    type: str
    sample: "b387359d-fa5c-4d58-9eb2-3af1a4976319"

vm_ext_id:
    description:
        - External ID of the newly restored AHV VM.
        - Populated only after C(wait_for_completion) succeeds and the task
          reports the restored VM entity.
    returned: When the restore task completes and returns the VM ext_id
    type: str
    sample: "e44621b1-da4e-40d1-87b1-cbb640001347"

changed:
    description: Whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

failed:
    description: Whether the task failed.
    returned: always
    type: bool
    sample: false

error:
    description: Error message set on failure.
    returned: When an error occurs
    type: str

msg:
    description: Contextual message (error, idempotent skip, or check mode).
    returned: When present
    type: str
    sample: "Api Exception raised while restoring AHV VM recovery point"
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

    nic_override_sub_spec = dict(
        nic_ext_id=dict(type="str", required=True),
        subnet_ext_id=dict(type="str"),
    )

    nic_spec_sub_spec = dict(
        nic_remove_list=dict(type="list", elements="str"),
        nic_override_list=dict(
            type="list",
            elements="dict",
            options=nic_override_sub_spec,
            obj=vmm_sdk.VmRestoreNicConfigOverrideParams,
        ),
    )

    guest_tools_sub_spec = dict(
        should_clear_in_guest_volume_group_attachments=dict(type="bool"),
    )

    categories_sub_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    vm_config_override_sub_spec = dict(
        name=dict(type="str"),
        description=dict(type="str"),
        categories=dict(
            type="list",
            elements="dict",
            options=categories_sub_spec,
        ),
        nic_spec=dict(
            type="dict",
            options=nic_spec_sub_spec,
            obj=vmm_sdk.VmRestoreNicConfigSpecification,
        ),
        guest_tools_spec=dict(
            type="dict",
            options=guest_tools_sub_spec,
            obj=vmm_sdk.VmRestoreGuestToolsSpecification,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        is_strict_mode=dict(type="bool"),
        vm_config_override_spec=dict(
            type="dict",
            options=vm_config_override_sub_spec,
            obj=vmm_sdk.VmConfigOverrideSpecification,
        ),
    )
    return module_args


def _resolve_category_reference_cls():
    """VmConfigOverrideSpecification.categories expects the AHV-config
    variant of CategoryReference. Prefer that name explicitly and fall back
    to any other CategoryReference variant if the SDK renames the class."""
    for preferred in ("AhvConfigCategoryReference", "CategoryReference"):
        cls = getattr(vmm_sdk, preferred, None)
        if cls is not None:
            return cls
    for name in dir(vmm_sdk):
        if name.endswith("CategoryReference"):
            return getattr(vmm_sdk, name)
    return None


def _build_restore_spec(module):
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.RestoreVmRecoveryPointParams()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        return None, err

    override_params = module.params.get("vm_config_override_spec") or {}
    categories = override_params.get("categories")
    if categories and spec.vm_config_override_spec is not None:
        category_cls = _resolve_category_reference_cls()
        if category_cls is None:
            return (
                None,
                "Unable to locate CategoryReference class in ntnx_vmm_py_client",
            )
        refs = []
        for cat in categories:
            ref = category_cls()
            ref.ext_id = cat.get("ext_id")
            refs.append(ref)
        spec.vm_config_override_spec.categories = refs
    return spec, None


def restore_vm_recovery_point(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec, err = _build_restore_spec(module)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating AHV VM recovery point restore spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current = get_vm_recovery_point(module, api_instance, ext_id)
    etag = get_etag(current)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    try:
        resp = api_instance.restore_vm_recovery_point(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while restoring AHV VM recovery point",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        vm_ext_id = get_entity_ext_id_from_task(
            task, rel=TASK_CONSTANTS.RelEntityType.VM
        )
        if vm_ext_id:
            result["vm_ext_id"] = vm_ext_id
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
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
    restore_vm_recovery_point(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
