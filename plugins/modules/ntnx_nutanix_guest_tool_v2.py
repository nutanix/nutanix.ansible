#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_nutanix_guest_tool_v2
short_description: Manage Nutanix Guest Tools (NGT) on an ESXi-hosted VM in Nutanix Prism Central
version_added: 2.5.0
description:
  - Manage the Nutanix Guest Tools (NGT) lifecycle for a single ESXi-hosted VM.
  - Supports install, insert-iso, upgrade, update (enable/disable + capability edit)
    and uninstall operations exposed by the C(EsxiVmApi) NGT endpoints.
  - Which operation runs is determined by C(state) and C(operation)
    (see the parameter documentation for the mapping).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Install / Insert-ISO / Upgrade / Update / Uninstall NGT on an ESXi VM) -
    Required Roles: Backup Admin, Consumer, Developer, NCM Connector, Operator, Prism Admin, Project Admin,
    Project Manager, Super Admin, Virtual Machine Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - If C(state) is set to C(present) the module runs the operation named by C(operation)
        (defaults to C(install) when NGT is not yet installed, else C(update)).
      - If C(state) is set to C(absent) the module uninstalls NGT from the VM.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the ESXi-hosted VM whose Nutanix Guest Tools are being managed.
      - Required for every operation.
    type: str
    required: true
  operation:
    description:
      - The specific NGT operation to perform when C(state=present).
      - C(install) installs NGT (requires C(capabilities), C(credential)).
      - C(insert_iso) inserts the NGT ISO into an available CD-ROM (requires C(capabilities)).
      - C(upgrade) upgrades NGT to the available version. Optionally accepts C(reboot_preference).
      - C(update) updates the current NGT configuration (capabilities, is_enabled) via PUT.
      - When omitted, the module auto-selects C(install) if NGT is not installed and C(update) otherwise.
      - Ignored when C(state=absent).
    type: str
    required: false
    choices:
      - install
      - insert_iso
      - upgrade
      - update
  capabilities:
    description:
      - List of NGT capabilities to enable on the guest VM.
      - Used by C(install), C(insert_iso) and C(update) operations.
    type: list
    elements: str
    required: false
    choices:
      - SELF_SERVICE_RESTORE
      - VSS_SNAPSHOT
  is_enabled:
    description:
      - Whether NGT should be enabled on the guest VM.
      - Only honoured when C(operation=update). Ignored otherwise.
    type: bool
    required: false
  credential:
    description:
      - Sign-in credentials for the guest VM. Required for C(operation=install).
    type: dict
    required: false
    suboptions:
      username:
        description:
          - The username for the server.
        type: str
        required: true
      password:
        description:
          - The password for the server.
        type: str
        required: true
  reboot_preference:
    description:
      - Restart schedule after installing or upgrading NGT.
      - Used by C(install) and C(upgrade) operations.
    type: dict
    required: false
    suboptions:
      schedule_type:
        description:
          - Reboot schedule type.
        type: str
        required: true
        choices:
          - IMMEDIATE
          - LATER
          - SKIP
      schedule:
        description:
          - Schedule for a scheduled restart. Required when C(schedule_type=LATER).
        type: dict
        required: false
        suboptions:
          start_time:
            description:
              - The start time for a scheduled restart in ISO 8601 format.
            type: str
            required: true
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
- name: Install NGT on an ESXi-hosted VM
  nutanix.ncp.ntnx_nutanix_guest_tool_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    operation: install
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
    capabilities:
      - SELF_SERVICE_RESTORE
      - VSS_SNAPSHOT
    credential:
      username: "admin"
      password: "secret"
    reboot_preference:
      schedule_type: IMMEDIATE
  register: install_result
  ignore_errors: true

- name: Insert NGT ISO into an available CD-ROM
  nutanix.ncp.ntnx_nutanix_guest_tool_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    operation: insert_iso
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
    capabilities:
      - VSS_SNAPSHOT
  register: insert_result
  ignore_errors: true

- name: Upgrade NGT (deferred reboot)
  nutanix.ncp.ntnx_nutanix_guest_tool_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    operation: upgrade
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
    reboot_preference:
      schedule_type: LATER
      schedule:
        start_time: "2026-12-01T02:00:00Z"
  register: upgrade_result
  ignore_errors: true

- name: Update NGT configuration - disable and trim capabilities
  nutanix.ncp.ntnx_nutanix_guest_tool_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    operation: update
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
    is_enabled: false
    capabilities:
      - VSS_SNAPSHOT
  register: update_result
  ignore_errors: true

- name: Uninstall NGT from an ESXi-hosted VM
  nutanix.ncp.ntnx_nutanix_guest_tool_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
  register: uninstall_result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response of the NGT lifecycle operation.
    - When C(wait) is true, returns the NGT configuration of the VM after the operation.
    - When C(wait) is false, returns the task envelope (task ext_id, etc.).
    - For C(check_mode) it returns the generated spec that would be sent to the API.
  returned: always
  type: dict
  sample:
    {
      "available_version": "4.1",
      "capabilities": [
        "VSS_SNAPSHOT"
      ],
      "guest_info": null,
      "guest_os_version": "linux:64:CentOS Linux-7.9",
      "is_enabled": true,
      "is_installed": true,
      "is_iso_inserted": false,
      "is_reachable": true,
      "is_vm_mobility_drivers_installed": null,
      "is_vss_snapshot_capable": true,
      "version": "4.1"
    }

task_ext_id:
  description:
    - The external ID of the underlying task for the requested NGT operation.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description:
    - The external ID of the VM on which NGT was managed.
  returned: always
  type: str
  sample: "98b9dc89-be08-3c56-b554-692b8b676fd1"

changed:
  description: Whether the NGT state on the VM was mutated by this run.
  returned: always
  type: bool
  sample: true

skipped:
  description: Whether the operation was a no-op (idempotency short-circuit).
  returned: when applicable
  type: bool
  sample: false

msg:
  description:
    - Contextual status message.
    - Populated on idempotency, check-mode-only paths, and any error path.
  returned: contextual
  type: str
  sample: "NGT is already installed in given vm."

error:
  description: The error message, if any, encountered while running the operation.
  returned: when an error occurs
  type: str

failed:
  description: Whether the module invocation itself failed.
  returned: always
  type: bool
  sample: false
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
from ..module_utils.v4.vmm.helpers import get_esxi_ngt_status  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    credential = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )
    schedule = dict(
        start_time=dict(type="str", required=True),
    )
    reboot_preference = dict(
        schedule_type=dict(
            type="str",
            required=True,
            choices=["IMMEDIATE", "LATER", "SKIP"],
        ),
        schedule=dict(
            type="dict",
            required=False,
            options=schedule,
            obj=vmm_sdk.NutanixRebootPreferenceSchedule,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str", required=True),
        operation=dict(
            type="str",
            required=False,
            choices=["install", "insert_iso", "upgrade", "update"],
        ),
        capabilities=dict(
            type="list",
            elements="str",
            required=False,
            choices=["SELF_SERVICE_RESTORE", "VSS_SNAPSHOT"],
        ),
        is_enabled=dict(type="bool", required=False),
        credential=dict(
            type="dict",
            required=False,
            options=credential,
            obj=vmm_sdk.NutanixCredential,
        ),
        reboot_preference=dict(
            type="dict",
            required=False,
            options=reboot_preference,
            obj=vmm_sdk.NutanixRebootPreference,
        ),
    )
    return module_args


def _get_etag_kwargs(status):
    """Return an if_match kwargs dict when an etag can be extracted."""
    etag = get_etag(status)
    if etag:
        return {"if_match": etag}
    return {}


def _refresh_response(module, api_instance, ext_id, result, task_ext_id):
    """Wait for the task, then refresh the NGT status on `result`."""
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        status = get_esxi_ngt_status(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(status.to_dict())


def install_nutanix_guest_tool(module, result, api_instance):
    """Install NGT on the target ESXi VM."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["capabilities", "credential"])

    status = get_esxi_ngt_status(module, api_instance, ext_id)
    if getattr(status, "is_installed", False):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(status.to_dict())
        module.exit_json(msg="NGT is already installed in given vm.", **result)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.NutanixGuestToolsInstallConfig()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating install NGT spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    kwargs = _get_etag_kwargs(status)
    resp = None
    try:
        resp = api_instance.install_nutanix_guest_tools(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while installing NGT",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    _refresh_response(module, api_instance, ext_id, result, task_ext_id)
    result["changed"] = True


def insert_iso_nutanix_guest_tool(module, result, api_instance):
    """Insert the NGT ISO into an available CD-ROM slot on the ESXi VM."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    status = get_esxi_ngt_status(module, api_instance, ext_id)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.NutanixGuestToolsInsertConfig()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating insert NGT ISO spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    kwargs = _get_etag_kwargs(status)
    resp = None
    try:
        resp = api_instance.insert_nutanix_guest_tools(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while inserting NGT ISO",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    _refresh_response(module, api_instance, ext_id, result, task_ext_id)
    result["changed"] = True


def upgrade_nutanix_guest_tool(module, result, api_instance):
    """Upgrade NGT on the ESXi VM to the available version."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    status = get_esxi_ngt_status(module, api_instance, ext_id)
    if not getattr(status, "is_installed", False):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(status.to_dict())
        module.exit_json(
            msg="NGT is not installed on the given VM; nothing to upgrade.", **result
        )

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.NutanixGuestToolsUpgradeConfig()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating upgrade NGT spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    kwargs = _get_etag_kwargs(status)
    resp = None
    try:
        resp = api_instance.upgrade_nutanix_guest_tools(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while upgrading NGT",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    _refresh_response(module, api_instance, ext_id, result, task_ext_id)
    result["changed"] = True


def _check_update_idempotency(old_dict, new_dict):
    """
    Compare NGT config before/after the requested update.

    Only the mutable fields (``is_enabled``, ``capabilities``) are compared
    since everything else on the entity is read-only from the client's point
    of view.
    """
    old_caps = sorted(old_dict.get("capabilities") or [])
    new_caps = sorted(new_dict.get("capabilities") or [])
    return (
        old_dict.get("is_enabled") == new_dict.get("is_enabled")
        and old_caps == new_caps
    )


def update_nutanix_guest_tool(module, result, api_instance):
    """Update NGT configuration (enable/disable + capability edit)."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    status = get_esxi_ngt_status(module, api_instance, ext_id)
    if not getattr(status, "is_installed", False):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(status.to_dict())
        module.exit_json(
            msg="NGT is not installed on the given VM; nothing to update.", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=status)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update NGT spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if _check_update_idempotency(status.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        module.exit_json(msg="Nothing to change.", **result)

    kwargs = _get_etag_kwargs(status)
    resp = None
    try:
        resp = api_instance.update_nutanix_guest_tools_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating NGT",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    _refresh_response(module, api_instance, ext_id, result, task_ext_id)
    result["changed"] = True


def uninstall_nutanix_guest_tool(module, result, api_instance):
    """Uninstall NGT from the ESXi VM."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    status = get_esxi_ngt_status(module, api_instance, ext_id)
    if not getattr(status, "is_installed", False):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(status.to_dict())
        module.exit_json(msg="NGT is already not installed in the given vm", **result)

    if module.check_mode:
        result["msg"] = "NGT for VM with ext_id:{0} will be uninstalled.".format(ext_id)
        result["response"] = strip_internal_attributes(status.to_dict())
        return

    kwargs = _get_etag_kwargs(status)
    resp = None
    try:
        resp = api_instance.uninstall_nutanix_guest_tools(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while uninstalling NGT",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    _refresh_response(module, api_instance, ext_id, result, task_ext_id)
    result["changed"] = True


def _resolve_operation(module, api_instance):
    """
    Auto-pick an operation when C(operation) was not supplied and
    C(state=present). Returns the resolved operation name.
    """
    op = module.params.get("operation")
    if op:
        return op

    ext_id = module.params.get("ext_id")
    status = get_esxi_ngt_status(module, api_instance, ext_id)
    if getattr(status, "is_installed", False):
        return "update"
    return "install"


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("operation", "install", ("capabilities", "credential")),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_esxi_vm_api_instance(module)
    state = module.params.get("state")

    if state == "absent":
        uninstall_nutanix_guest_tool(module, result, api_instance)
    else:
        operation = _resolve_operation(module, api_instance)
        if operation == "install":
            install_nutanix_guest_tool(module, result, api_instance)
        elif operation == "insert_iso":
            insert_iso_nutanix_guest_tool(module, result, api_instance)
        elif operation == "upgrade":
            upgrade_nutanix_guest_tool(module, result, api_instance)
        else:
            update_nutanix_guest_tool(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
