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
  - Restore a new AHV VM from an existing AHV VM recovery point in Nutanix Prism Central.
  - The restored VM's configuration can optionally be overridden (name, description, NIC spec,
    categories, ownership, guest tools) via C(vm_config_override_spec).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Restore an AHV VM Recovery Point) -
      Required Roles: Backup Admin, Disaster Recovery Admin, Prism Admin, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - State of the module.
      - If state is C(present), the module will restore a new AHV VM from a recovery point.
      - If state is anything else, the module will fail.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - A globally unique identifier of an AHV VM recovery point. It should be of type UUID.
      - This is the recovery point that will be restored.
    type: str
    required: true
  is_strict_mode:
    description:
      - If set to C(false), any VM configuration that cannot be restored will be dropped or
        reset to system defaults (currently applies to subnets, NIC profiles, project and
        categories, plus dropping unknown features on older PEs).
      - If set to C(true), the restore will run in normal mode where any failures are raised
        as errors and the VM is not restored until the issues are resolved.
    type: bool
    required: false
    default: true
  vm_config_override_spec:
    description:
      - Optional overrides to apply on the VM configuration captured by the recovery point.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - Name to assign to the restored VM.
        type: str
        required: false
      description:
        description:
          - Description to assign to the restored VM.
        type: str
        required: false
      nic_spec:
        description:
          - NIC configuration overrides for the restored VM. If omitted, the NICs captured
            in the recovery point are restored as-is.
        type: dict
        required: false
        suboptions:
          nic_remove_list:
            description:
              - List of NIC UUIDs from the VM recovery point to drop when restoring the VM.
            type: list
            elements: str
            required: false
          nic_override_list:
            description:
              - Per-NIC override specifications.
            type: list
            elements: dict
            required: false
            suboptions:
              nic_ext_id:
                description:
                  - External identifier of the NIC being overridden from the VM recovery point.
                type: str
                required: false
              guest_nic_info:
                description:
                  - Guest NIC info overrides (currently supports guest static IP list).
                type: dict
                required: false
                suboptions:
                  guest_static_ip_list:
                    description:
                      - List of guest static IP entries to override.
                    type: list
                    elements: dict
                    required: false
      categories:
        description:
          - List of AHV category references to associate with the restored VM.
        type: list
        elements: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External identifier of the category.
            type: str
            required: true
      ownership_info:
        description:
          - Ownership override for the restored VM.
        type: dict
        required: false
        suboptions:
          owner:
            description:
              - Owner reference for the restored VM.
            type: dict
            required: false
            suboptions:
              ext_id:
                description:
                  - External identifier of the owning user.
                type: str
                required: true
      guest_tools_spec:
        description:
          - Guest tools override for the restored VM (only applicable when NGT is installed).
        type: dict
        required: false
        suboptions:
          should_clear_in_guest_volume_group_attachments:
            description:
              - If C(true), the restored VM will drop all in-guest volume group attachments
                captured in the recovery point.
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
- name: Restore a new VM from an AHV VM recovery point with default configuration
  nutanix.ncp.ntnx_vm_recovery_point_restore_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b387359d-fa5c-4d58-9eb2-3af1a4976319"
  register: result

- name: Restore a new VM from an AHV VM recovery point with overrides
  nutanix.ncp.ntnx_vm_recovery_point_restore_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b387359d-fa5c-4d58-9eb2-3af1a4976319"
    is_strict_mode: false
    vm_config_override_spec:
      name: "restored-vm-ansible"
      description: "VM restored from recovery point by Ansible"
      guest_tools_spec:
        should_clear_in_guest_volume_group_attachments: true
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for restoring a new VM from an AHV VM recovery point.
    - Task details are returned; the restored VM's external ID is exposed via C(vm_ext_id)
      when the task completes successfully.
  returned: always
  type: dict
  sample:
    {
        "cluster_ext_ids": [
            "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
        ],
        "completed_time": "2026-07-21T05:20:11.524581+00:00",
        "completion_details": [
            {
                "name": "vmExtIds",
                "value": "e44621b1-da4e-40d1-87b1-cbb640001347"
            }
        ],
        "created_time": "2026-07-21T05:20:07.167906+00:00",
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
        "operation_description": "Restore VM Recovery Point",
        "progress_percentage": 100,
        "started_time": "2026-07-21T05:20:07.185754+00:00",
        "status": "SUCCEEDED"
    }

task_ext_id:
  description: The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the source AHV VM recovery point that was restored.
  returned: always
  type: str
  sample: "b387359d-fa5c-4d58-9eb2-3af1a4976319"

vm_ext_id:
  description: The external ID of the restored AHV VM (populated when the task completes and C(wait) is C(true)).
  returned: when restore task completes successfully
  type: str
  sample: "e44621b1-da4e-40d1-87b1-cbb640001347"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when an error occurs
  type: str
  sample: "Failed to get etag for AHV VM recovery point"

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
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
    get_vm_recovery_points_api_instance,
)

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    guest_static_ip_sub_spec = dict()

    guest_nic_info_sub_spec = dict(
        guest_static_ip_list=dict(
            type="list",
            elements="dict",
            options=guest_static_ip_sub_spec,
            obj=vmm_sdk.GuestStaticIpSpec,
        ),
    )

    nic_override_sub_spec = dict(
        nic_ext_id=dict(type="str"),
        guest_nic_info=dict(
            type="dict",
            options=guest_nic_info_sub_spec,
            obj=vmm_sdk.VmRestoreGuestNicInfoOverrideSpec,
        ),
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

    category_ref_sub_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    owner_ref_sub_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    ownership_info_sub_spec = dict(
        owner=dict(
            type="dict",
            options=owner_ref_sub_spec,
            obj=vmm_sdk.AhvConfigOwnerReference,
        ),
    )

    guest_tools_sub_spec = dict(
        should_clear_in_guest_volume_group_attachments=dict(type="bool", default=False),
    )

    vm_config_override_spec_sub_spec = dict(
        name=dict(type="str"),
        description=dict(type="str"),
        nic_spec=dict(
            type="dict",
            options=nic_spec_sub_spec,
            obj=vmm_sdk.VmRestoreNicConfigSpecification,
        ),
        categories=dict(
            type="list",
            elements="dict",
            options=category_ref_sub_spec,
            obj=vmm_sdk.AhvConfigCategoryReference,
        ),
        ownership_info=dict(
            type="dict",
            options=ownership_info_sub_spec,
            obj=vmm_sdk.AhvConfigOwnershipInfo,
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
        is_strict_mode=dict(type="bool", default=True),
        vm_config_override_spec=dict(
            type="dict",
            options=vm_config_override_spec_sub_spec,
            obj=vmm_sdk.VmConfigOverrideSpecification,
        ),
    )
    return module_args


def restore_vm_recovery_point(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.RestoreVmRecoveryPointParams()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating restore AHV VM recovery point spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.restore_vm_recovery_point(extId=ext_id, body=spec)
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
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        vm_ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.VM
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
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_vm_recovery_points_api_instance(module)
    restore_vm_recovery_point(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
