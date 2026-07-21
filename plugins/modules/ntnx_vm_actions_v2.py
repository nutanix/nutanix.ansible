#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_actions_v2
short_description: Perform lifecycle and management actions on ESXi VMs in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to perform lifecycle and management actions on ESXi based virtual machines
    managed by Nutanix Prism Central using the C(vmm.v4.esxi) API family.
  - Supported actions are power control (power on/off, reset, suspend, guest reboot, guest shutdown),
    ownership assignment, category association / disassociation, Nutanix Guest Tools (NGT) lifecycle
    (install, insert ISO, upgrade, update, uninstall), and revert to a VM Recovery Point.
  - ESXi VMs are managed by vCenter; this module does not create or delete VMs, only performs actions
    on existing VMs.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Power operations on an ESXi VM) -
      Required Roles: Account Owner, Administrator, Prism Admin, Super Admin, Virtual Machine Admin,
      Virtual Machine Operator
    - >-
      B(Assign owner / Associate categories / Disassociate categories) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - >-
      B(Nutanix Guest Tools (NGT) actions) -
      Required Roles: Account Owner, Administrator, Prism Admin, Super Admin, Virtual Machine Admin
    - >-
      B(Revert ESXi VM to a VM Recovery Point) -
      Required Roles: Backup Admin, Disaster Recovery Admin, Prism Admin, Super Admin, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - The action to perform on the ESXi VM.
      - C(power_on) turns on or resumes the VM.
      - C(power_off) forcefully powers off the VM.
      - C(reset) sequentially powers off and on the VM.
      - C(suspend) pauses/suspends VM execution.
      - C(guest_reboot) issues a guest OS reboot command.
      - C(guest_shutdown) shuts down services on the guest OS.
      - C(revert) reverts the VM to a Nutanix VM Recovery Point.
      - C(assign_owner) assigns a new owner to the VM.
      - C(associate_categories) associates the provided categories with the VM.
      - C(disassociate_categories) removes the provided categories from the VM.
      - C(ngt_install) installs Nutanix Guest Tools on the VM.
      - C(ngt_insert_iso) inserts the NGT ISO into an available CD-ROM slot on the VM.
      - C(ngt_upgrade) upgrades NGT inside the VM.
      - C(ngt_update) updates the NGT configuration for the VM.
      - C(ngt_uninstall) uninstalls NGT from the VM.
    type: str
    choices:
      - power_on
      - power_off
      - reset
      - suspend
      - guest_reboot
      - guest_shutdown
      - revert
      - assign_owner
      - associate_categories
      - disassociate_categories
      - ngt_install
      - ngt_insert_iso
      - ngt_upgrade
      - ngt_update
      - ngt_uninstall
    default: power_on
  ext_id:
    description:
      - The external ID of the ESXi VM on which the action will be performed.
      - Required for every action.
    type: str
    required: true
  owner:
    description:
      - The new owner reference to be assigned to the VM.
      - Required when C(state=assign_owner).
    type: dict
    required: false
    suboptions:
      ext_id:
        description:
          - The external ID of the owner (typically a user).
        type: str
        required: true
      entity_type:
        description:
          - The type of the owner entity.
        type: str
        choices:
          - USER
        required: false
  categories:
    description:
      - The list of category references to associate with or disassociate from the VM.
      - Required when C(state=associate_categories) or C(state=disassociate_categories).
    type: list
    elements: dict
    required: false
    suboptions:
      ext_id:
        description:
          - The globally unique identifier of a category.
        type: str
        required: true
  vm_recovery_point_ext_id:
    description:
      - The external identifier of the VM Recovery Point to revert to.
      - Required when C(state=revert).
    type: str
    required: false
  ngt_install_config:
    description:
      - Arguments for installing Nutanix Guest Tools on the ESXi VM.
      - Used when C(state=ngt_install).
    type: dict
    required: false
    suboptions:
      capabilities:
        description:
          - List of NGT capabilities to enable on the guest VM.
        type: list
        elements: str
        choices:
          - SELF_SERVICE_RESTORE
          - VSS_SNAPSHOT
      credential:
        description:
          - Sign-in credentials to use for installing NGT inside the guest.
        type: dict
        suboptions:
          username:
            description:
              - Username for authentication on the guest.
            type: str
            required: true
          password:
            description:
              - Password for authentication on the guest.
              - Value is not logged (secret).
            type: str
            required: true
      reboot_preference:
        description:
          - Restart schedule to apply after NGT installation.
        type: dict
        suboptions:
          schedule_type:
            description:
              - The type of reboot schedule.
            type: str
            choices:
              - SKIP
              - IMMEDIATE
              - LATER
            required: true
          schedule:
            description:
              - The schedule for a delayed restart.
              - Required when C(schedule_type=LATER).
            type: dict
            suboptions:
              start_time:
                description:
                  - The start time for a scheduled restart (ISO 8601).
                type: str
                required: true
  ngt_insert_config:
    description:
      - Arguments for inserting the NGT ISO into an available CD-ROM slot.
      - Used when C(state=ngt_insert_iso).
    type: dict
    required: false
    suboptions:
      capabilities:
        description:
          - List of NGT capabilities to enable on the guest VM.
        type: list
        elements: str
        choices:
          - SELF_SERVICE_RESTORE
          - VSS_SNAPSHOT
  ngt_upgrade_config:
    description:
      - Arguments for upgrading NGT inside the ESXi VM.
      - Used when C(state=ngt_upgrade).
    type: dict
    required: false
    suboptions:
      reboot_preference:
        description:
          - Restart schedule to apply after NGT upgrade.
        type: dict
        suboptions:
          schedule_type:
            description:
              - The type of reboot schedule.
            type: str
            choices:
              - SKIP
              - IMMEDIATE
              - LATER
            required: true
          schedule:
            description:
              - The schedule for a delayed restart.
              - Required when C(schedule_type=LATER).
            type: dict
            suboptions:
              start_time:
                description:
                  - The start time for a scheduled restart (ISO 8601).
                type: str
                required: true
  ngt_update_config:
    description:
      - The NGT configuration payload sent when updating NGT configuration on the VM.
      - Used when C(state=ngt_update).
    type: dict
    required: false
    suboptions:
      capabilities:
        description:
          - The set of enabled NGT capabilities to persist on the VM.
        type: list
        elements: str
        choices:
          - SELF_SERVICE_RESTORE
          - VSS_SNAPSHOT
      is_enabled:
        description:
          - Whether NGT communications are enabled for the VM.
        type: bool
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Power on an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: power_on
  register: result

- name: Force power off an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: power_off
  register: result

- name: Suspend an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: suspend
  register: result

- name: Reset an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: reset
  register: result

- name: Guest reboot on an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: guest_reboot
  register: result

- name: Guest shutdown on an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: guest_shutdown
  register: result

- name: Assign an owner to an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: assign_owner
    owner:
      ext_id: "00000000-0000-0000-0000-000000000000"
      entity_type: USER
  register: result

- name: Associate categories to an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: associate_categories
    categories:
      - ext_id: "a3220c60-2ba2-4e91-8c1d-1111aabbccdd"
  register: result

- name: Disassociate categories from an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: disassociate_categories
    categories:
      - ext_id: "a3220c60-2ba2-4e91-8c1d-1111aabbccdd"
  register: result

- name: Revert an ESXi VM to a VM Recovery Point
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: revert
    vm_recovery_point_ext_id: "c3c3c3c3-9999-8888-7777-666655554444"
  register: result

- name: Install NGT on an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: ngt_install
    ngt_install_config:
      capabilities:
        - SELF_SERVICE_RESTORE
        - VSS_SNAPSHOT
      credential:
        username: "administrator"
        password: "Nutanix.123"
      reboot_preference:
        schedule_type: IMMEDIATE
  register: result

- name: Insert NGT ISO into an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: ngt_insert_iso
    ngt_insert_config:
      capabilities:
        - SELF_SERVICE_RESTORE
  register: result

- name: Upgrade NGT inside an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: ngt_upgrade
    ngt_upgrade_config:
      reboot_preference:
        schedule_type: SKIP
  register: result

- name: Update NGT configuration on an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: ngt_update
    ngt_update_config:
      capabilities:
        - VSS_SNAPSHOT
      is_enabled: true
  register: result

- name: Uninstall NGT from an ESXi VM
  nutanix.ncp.ntnx_vm_actions_v2:
    ext_id: "b8b5b5b5-1111-2222-3333-444455556666"
    state: ngt_uninstall
  register: result
"""

RETURN = r"""
response:
  description:
    - The full response from the ESXi VM action task.
    - When C(wait) is true, the completed task object is returned.
    - When C(wait) is false, the task reference object is returned.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": ["0006197f-3d06-ce49-1fc3-ac1f6b6029c1"],
      "completed_time": "2026-07-21T05:12:35.101832+00:00",
      "created_time": "2026-07-21T05:12:33.987654+00:00",
      "entities_affected": [
        {
          "ext_id": "b8b5b5b5-1111-2222-3333-444455556666",
          "name": "esxi-vm-1",
          "rel": "vmm:esxi:config:vm"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:8e0c14aa-4a76-4cc3-ac67-9d63fa7ec4a1",
      "operation": "PowerOnVm",
      "started_time": "2026-07-21T05:12:34.198765+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null
    }

task_ext_id:
  description:
    - The external ID of the ESXi VM action task.
  returned: always
  type: str
  sample: "ZXJnb24=:8e0c14aa-4a76-4cc3-ac67-9d63fa7ec4a1"

ext_id:
  description:
    - The external ID of the ESXi VM on which the action was invoked.
  returned: always
  type: str
  sample: "b8b5b5b5-1111-2222-3333-444455556666"

changed:
  description: Indicates whether the task resulted in any change.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - Indicates whether the action was skipped (e.g. because the VM was already in the desired state
      or NGT was already installed / already not installed).
  returned: when applicable
  type: bool
  sample: false

error:
  description: The error message if an error occurred.
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: A human-readable message about the result of the action.
  returned: When there is an error, when the module is idempotent, or in check mode
  type: str
  sample: "Api Exception raised while performing power_on on ESXi VM"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_esxi_vm_api_instance,
    get_etag,
)
from ..module_utils.v4.vmm.helpers import get_esxi_vm, get_esxi_vm_ngt  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as virtual_machine_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as virtual_machine_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

NGT_CAPABILITY_CHOICES = ["SELF_SERVICE_RESTORE", "VSS_SNAPSHOT"]
NGT_SCHEDULE_CHOICES = ["SKIP", "IMMEDIATE", "LATER"]
POWER_ON_STATES = ("ON",)
POWER_OFF_STATES = ("OFF",)
SUSPENDED_STATES = ("SUSPENDED", "PAUSED")


def _reboot_preference_spec():
    schedule = dict(
        start_time=dict(type="str", required=True),
    )
    return dict(
        schedule_type=dict(type="str", choices=NGT_SCHEDULE_CHOICES, required=True),
        schedule=dict(
            type="dict",
            options=schedule,
            obj=virtual_machine_management_sdk.NutanixRebootPreferenceSchedule,
        ),
    )


def get_module_spec():
    owner_spec = dict(
        ext_id=dict(type="str", required=True),
        entity_type=dict(type="str", choices=["USER"], required=False),
    )

    category_ref_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    credential_spec = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )

    ngt_install_config_spec = dict(
        capabilities=dict(type="list", elements="str", choices=NGT_CAPABILITY_CHOICES),
        credential=dict(
            type="dict",
            options=credential_spec,
            obj=virtual_machine_management_sdk.NutanixCredential,
        ),
        reboot_preference=dict(
            type="dict",
            options=_reboot_preference_spec(),
            obj=virtual_machine_management_sdk.NutanixRebootPreference,
        ),
    )

    ngt_insert_config_spec = dict(
        capabilities=dict(type="list", elements="str", choices=NGT_CAPABILITY_CHOICES),
    )

    ngt_upgrade_config_spec = dict(
        reboot_preference=dict(
            type="dict",
            options=_reboot_preference_spec(),
            obj=virtual_machine_management_sdk.NutanixRebootPreference,
        ),
    )

    ngt_update_config_spec = dict(
        capabilities=dict(type="list", elements="str", choices=NGT_CAPABILITY_CHOICES),
        is_enabled=dict(type="bool"),
    )

    module_args = dict(
        ext_id=dict(type="str", required=True),
        state=dict(
            type="str",
            choices=[
                "power_on",
                "power_off",
                "reset",
                "suspend",
                "guest_reboot",
                "guest_shutdown",
                "revert",
                "assign_owner",
                "associate_categories",
                "disassociate_categories",
                "ngt_install",
                "ngt_insert_iso",
                "ngt_upgrade",
                "ngt_update",
                "ngt_uninstall",
            ],
            default="power_on",
        ),
        owner=dict(
            type="dict",
            options=owner_spec,
            obj=virtual_machine_management_sdk.EsxiConfigOwnerReference,
        ),
        categories=dict(
            type="list",
            elements="dict",
            options=category_ref_spec,
            obj=virtual_machine_management_sdk.EsxiConfigCategoryReference,
        ),
        vm_recovery_point_ext_id=dict(type="str"),
        ngt_install_config=dict(
            type="dict",
            options=ngt_install_config_spec,
            obj=virtual_machine_management_sdk.NutanixGuestToolsInstallConfig,
        ),
        ngt_insert_config=dict(
            type="dict",
            options=ngt_insert_config_spec,
            obj=virtual_machine_management_sdk.NutanixGuestToolsInsertConfig,
        ),
        ngt_upgrade_config=dict(
            type="dict",
            options=ngt_upgrade_config_spec,
            obj=virtual_machine_management_sdk.NutanixGuestToolsUpgradeConfig,
        ),
        ngt_update_config=dict(
            type="dict",
            options=ngt_update_config_spec,
            obj=virtual_machine_management_sdk.NutanixGuestTools,
        ),
    )
    return module_args


def _finish_task(module, result, resp):
    """Persist task info on result and wait for completion when requested."""
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def _generate_sub_spec(module, result, sdk_class, module_args, params, error_msg):
    """Generate an SDK object from a sub-dict inside module.params (via SpecGenerator)."""
    if not params:
        return None
    sg = SpecGenerator(module)
    obj, err = sg.generate_spec(obj=sdk_class(), attr=params, module_args=module_args)
    if err:
        result["error"] = err
        module.fail_json(msg=error_msg, **result)
    return obj


def do_power_action(module, api_instance, result):
    state = module.params.get("state")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "ESXi VM with ext_id: {0} will be {1}".format(ext_id, state)
        return

    vm = get_esxi_vm(module, api_instance, ext_id)
    power_state = getattr(vm, "power_state", None)
    power_state_value = getattr(power_state, "value", power_state)

    if state == "power_on" and power_state_value in POWER_ON_STATES:
        result["skipped"] = True
        module.exit_json(
            msg="ESXi VM is already powered on. Nothing to change.", **result
        )
    if state == "power_off" and power_state_value in POWER_OFF_STATES:
        result["skipped"] = True
        module.exit_json(
            msg="ESXi VM is already powered off. Nothing to change.", **result
        )
    if state == "suspend" and power_state_value in SUSPENDED_STATES:
        result["skipped"] = True
        module.exit_json(
            msg="ESXi VM is already suspended. Nothing to change.", **result
        )

    etag = get_etag(vm)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    try:
        if state == "power_on":
            resp = api_instance.power_on_vm(extId=ext_id, **kwargs)
        elif state == "power_off":
            resp = api_instance.power_off_vm(extId=ext_id, **kwargs)
        elif state == "reset":
            resp = api_instance.reset_vm(extId=ext_id, **kwargs)
        elif state == "suspend":
            resp = api_instance.suspend_vm(extId=ext_id, **kwargs)
        elif state == "guest_reboot":
            resp = api_instance.reboot_guest_vm(extId=ext_id, **kwargs)
        elif state == "guest_shutdown":
            resp = api_instance.shutdown_guest_vm(extId=ext_id, **kwargs)
        else:
            module.fail_json(
                msg="Unsupported power action: {0}".format(state), **result
            )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing {0} on ESXi VM".format(state),
        )

    _finish_task(module, result, resp)


def do_assign_owner(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["owner"])

    module_args = get_module_spec().get("owner", {}).get("options")
    spec = _generate_sub_spec(
        module,
        result,
        virtual_machine_management_sdk.EsxiConfigOwnerReference,
        module_args,
        module.params.get("owner"),
        "Failed generating assign owner spec",
    )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.assign_vm_owner(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while assigning owner to ESXi VM",
        )

    _finish_task(module, result, resp)


def _build_categories_params(module, result, sdk_class, error_msg):
    module_args = get_module_spec().get("categories", {}).get("options")
    if not module_args:
        result["error"] = "categories argument spec missing"
        module.fail_json(msg=error_msg, **result)

    references = []
    sg = SpecGenerator(module)
    for cat in module.params.get("categories") or []:
        obj, err = sg.generate_spec(
            obj=virtual_machine_management_sdk.EsxiConfigCategoryReference(),
            attr=cat,
            module_args=module_args,
        )
        if err:
            result["error"] = err
            module.fail_json(msg=error_msg, **result)
        references.append(obj)

    spec = sdk_class()
    spec.categories = references
    return spec


def do_associate_categories(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["categories"])

    spec = _build_categories_params(
        module,
        result,
        virtual_machine_management_sdk.EsxiConfigAssociateVmCategoriesParams,
        "Failed generating associate categories spec",
    )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.associate_categories(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating categories to ESXi VM",
        )
    _finish_task(module, result, resp)


def do_disassociate_categories(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["categories"])

    spec = _build_categories_params(
        module,
        result,
        virtual_machine_management_sdk.EsxiConfigDisassociateVmCategoriesParams,
        "Failed generating disassociate categories spec",
    )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.disassociate_categories(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating categories from ESXi VM",
        )
    _finish_task(module, result, resp)


def do_revert(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["vm_recovery_point_ext_id"])

    spec = virtual_machine_management_sdk.EsxiConfigRevertParams()
    spec.vm_recovery_point_ext_id = module.params.get("vm_recovery_point_ext_id")

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.revert_vm(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while reverting ESXi VM",
        )
    _finish_task(module, result, resp)


def do_ngt_install(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["ngt_install_config"])

    module_args = get_module_spec().get("ngt_install_config", {}).get("options")
    spec = _generate_sub_spec(
        module,
        result,
        virtual_machine_management_sdk.NutanixGuestToolsInstallConfig,
        module_args,
        module.params.get("ngt_install_config"),
        "Failed generating NGT install spec",
    )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    status = get_esxi_vm_ngt(module, api_instance, ext_id)
    if getattr(status, "is_installed", False):
        result["skipped"] = True
        module.exit_json(
            msg="NGT is already installed on the ESXi VM. Nothing to change.",
            **result,
        )

    try:
        resp = api_instance.install_nutanix_guest_tools(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while installing NGT on ESXi VM",
        )
    _finish_task(module, result, resp)


def do_ngt_insert_iso(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    module_args = get_module_spec().get("ngt_insert_config", {}).get("options")
    spec = _generate_sub_spec(
        module,
        result,
        virtual_machine_management_sdk.NutanixGuestToolsInsertConfig,
        module_args,
        module.params.get("ngt_insert_config") or {},
        "Failed generating NGT insert ISO spec",
    )
    if spec is None:
        spec = virtual_machine_management_sdk.NutanixGuestToolsInsertConfig()

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.insert_nutanix_guest_tools(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while inserting NGT ISO on ESXi VM",
        )
    _finish_task(module, result, resp)


def do_ngt_upgrade(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["ngt_upgrade_config"])

    module_args = get_module_spec().get("ngt_upgrade_config", {}).get("options")
    spec = _generate_sub_spec(
        module,
        result,
        virtual_machine_management_sdk.NutanixGuestToolsUpgradeConfig,
        module_args,
        module.params.get("ngt_upgrade_config"),
        "Failed generating NGT upgrade spec",
    )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.upgrade_nutanix_guest_tools(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while upgrading NGT on ESXi VM",
        )
    _finish_task(module, result, resp)


def do_ngt_update(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["ngt_update_config"])

    module_args = get_module_spec().get("ngt_update_config", {}).get("options")
    spec = _generate_sub_spec(
        module,
        result,
        virtual_machine_management_sdk.NutanixGuestTools,
        module_args,
        module.params.get("ngt_update_config"),
        "Failed generating NGT update spec",
    )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    status = get_esxi_vm_ngt(module, api_instance, ext_id)
    etag = get_etag(status)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    try:
        resp = api_instance.update_nutanix_guest_tools_by_id(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating NGT configuration on ESXi VM",
        )
    _finish_task(module, result, resp)


def do_ngt_uninstall(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "NGT will be uninstalled from ESXi VM with ext_id: {0}".format(
            ext_id
        )
        return

    status = get_esxi_vm_ngt(module, api_instance, ext_id)
    if not getattr(status, "is_installed", False):
        result["skipped"] = True
        module.exit_json(
            msg="NGT is not installed on the ESXi VM. Nothing to uninstall.",
            **result,
        )
    etag = get_etag(status)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    try:
        resp = api_instance.uninstall_nutanix_guest_tools(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while uninstalling NGT on ESXi VM",
        )
    _finish_task(module, result, resp)


# Dispatch table mapping state to handler function.
ACTION_HANDLERS = {
    "power_on": do_power_action,
    "power_off": do_power_action,
    "reset": do_power_action,
    "suspend": do_power_action,
    "guest_reboot": do_power_action,
    "guest_shutdown": do_power_action,
    "assign_owner": do_assign_owner,
    "associate_categories": do_associate_categories,
    "disassociate_categories": do_disassociate_categories,
    "revert": do_revert,
    "ngt_install": do_ngt_install,
    "ngt_insert_iso": do_ngt_insert_iso,
    "ngt_upgrade": do_ngt_upgrade,
    "ngt_update": do_ngt_update,
    "ngt_uninstall": do_ngt_uninstall,
}


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "assign_owner", ("owner",)),
            ("state", "associate_categories", ("categories",)),
            ("state", "disassociate_categories", ("categories",)),
            ("state", "revert", ("vm_recovery_point_ext_id",)),
            ("state", "ngt_install", ("ngt_install_config",)),
            ("state", "ngt_upgrade", ("ngt_upgrade_config",)),
            ("state", "ngt_update", ("ngt_update_config",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)

    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_esxi_vm_api_instance(module)
    state = module.params.get("state")
    handler = ACTION_HANDLERS.get(state)
    if handler is None:
        module.fail_json(msg="Unsupported action state: {0}".format(state), **result)

    handler(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
