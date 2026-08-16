#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_custom_attribute_v2
short_description: Add or remove user-defined custom attributes of an AHV VM in Nutanix Prism Central.
version_added: 2.7.0
description:
  - This module adds to or removes from the C(customAttributes) list of an AHV Virtual Machine in Nutanix Prism Central.
  - Custom attributes are user-defined C(key:value) string pairs (e.g. C(environment:production))
    that carry per-VM metadata for tracking, classification, and automation workflows.
  - Only the attributes provided in C(custom_attributes) are affected. Existing attributes that are
    not listed remain untouched.
  - This module uses the Nutanix PC v4 APIs based SDKs (C(ntnx_vmm_py_client)).
notes:
  - >-
    This module requires the following Nutanix IAM roles/permissions to be assigned to the user
    performing the operation. The required roles depend on the operation being performed.
  - >-
    B(Add to the VM's custom attributes) -
    Required Permission: C(Update_Virtual_Machine_Custom_Attributes).
    Common Roles: Prism Admin, Super Admin, Virtual Machine Admin.
  - >-
    B(Remove from the VM's custom attributes) -
    Required Permission: C(Update_Virtual_Machine_Custom_Attributes).
    Common Roles: Prism Admin, Super Admin, Virtual Machine Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - If C(state) is set to C(present), the given C(custom_attributes) are added to the VM.
      - If C(state) is set to C(absent), the given C(custom_attributes) are removed from the VM.
      - The module is idempotent - only attributes that are actually missing/present on the VM
        are sent to the API. If nothing needs to change the task is skipped.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The globally unique identifier of the AHV VM (UUID) whose custom attributes are being modified.
    type: str
    required: true
  custom_attributes:
    description:
      - List of user-defined custom attribute strings in the C(key:value) format
        (e.g. C(environment:production), C(owner:team-a), C(tier:gold)).
      - For C(state=present), any attribute already set on the VM is filtered out
        and only the missing ones are sent to the add API.
      - For C(state=absent), only the attributes actually present on the VM are sent
        to the remove API.
    type: list
    elements: str
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
- name: Add custom attributes to an AHV VM
  nutanix.ncp.ntnx_vm_custom_attribute_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    custom_attributes:
      - "environment:production"
      - "owner:team-a"
      - "tier:gold"
  register: result

- name: Remove custom attributes from an AHV VM
  nutanix.ncp.ntnx_vm_custom_attribute_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    custom_attributes:
      - "environment:production"
      - "owner:team-a"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for adding or removing custom attributes of an AHV VM.
    - When C(wait=true) it is the up-to-date list of C(custom_attributes) currently set on the VM
      after the operation completes.
    - When C(wait=false) it is the raw task reference returned by the API.
    - In C(check_mode) it is the request spec the module would have sent.
  returned: always
  type: list
  elements: str
  sample:
    - "environment:production"
    - "owner:team-a"
    - "tier:gold"

ext_id:
  description:
    - The external ID (UUID) of the AHV VM.
  returned: always
  type: str
  sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"

task_ext_id:
  description:
    - The external ID of the async task created by the API.
  returned: when the API call is made
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

changed:
  description: Whether the VM's custom attributes changed as a result of this run.
  returned: always
  type: bool
  sample: true

skipped:
  description: Set to True when nothing needed to change (idempotent no-op).
  returned: on skipping
  type: bool
  sample: true

msg:
  description: Status / error message.
  returned: When there is an error, when the module is idempotent, or in check_mode.
  type: str
  sample: "Nothing to change."

error:
  description: Error details if an error occurred.
  returned: when an error occurs
  type: str

failed:
  description: True if the task failed.
  returned: always
  type: bool
  sample: false
"""

import time  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import get_tasks_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        custom_attributes=dict(
            type="list",
            elements="str",
            required=True,
        ),
    )
    return module_args


# Short retry: PC occasionally reports a freshly-created VM as "not found"
# while VMM metadata propagates across services. Retry a handful of times
# before giving up. Only matters on the very first call after VM creation.
_VM_READ_RETRIES = 3
_VM_READ_BACKOFF_SEC = 2

# The v4 VMM $action endpoints (add/remove custom attributes) can also
# transiently fail with VM_NOT_FOUND (error group ``VM_NOT_FOUND`` /
# code ``VMM-30100``) shortly after a VM is created, because the VMM
# action-plane services take longer to see a newly created VM than the
# read-plane services do. Retry the entire action on that specific error
# only; every other task failure is propagated as-is.
_ACTION_RETRIES = 3
_ACTION_BACKOFF_SEC = 3
_TASK_POLL_INTERVAL_SEC = 2
_VM_NOT_FOUND_ERROR_GROUP = "VM_NOT_FOUND"


def _fetch_vm_or_none(api_instance, vm_ext_id):
    """
    Best-effort GET of the VM.
    Returns the VM object on success or ``None`` if the VM is genuinely
    not-yet-visible (transient 404 during metadata propagation).
    Any non-404 error is re-raised for the caller to surface.
    """
    for attempt in range(_VM_READ_RETRIES):
        try:
            return api_instance.get_vm_by_id(extId=vm_ext_id).data
        except Exception as e:
            status = getattr(e, "status", None)
            if status != 404 or attempt == _VM_READ_RETRIES - 1:
                if status == 404:
                    return None
                raise
            time.sleep(_VM_READ_BACKOFF_SEC)
    return None


def _resolve_vm_or_fail(module, api_instance, vm_ext_id):
    """
    Fetch the VM, failing the module with a descriptive error if it is
    truly missing (used post-task to refresh the returned attribute list).
    """
    vm = _fetch_vm_or_none(api_instance, vm_ext_id)
    if vm is None:
        # Delegate the final failure to the shared helper so the error
        # shape stays consistent with other v4 modules.
        get_vm(module, api_instance, vm_ext_id)
    return vm


def _refresh_custom_attributes(module, api_instance, vm_ext_id, result):
    """
    Re-fetch the VM after a task completes and refresh
    ``result["response"]`` with the current attributes.
    """
    vm = _resolve_vm_or_fail(module, api_instance, vm_ext_id)
    result["response"] = list(vm.custom_attributes or [])


def _task_error_groups(task):
    """Return the list of error_group values on a task (may be empty)."""
    error_messages = getattr(task, "error_messages", None) or []
    groups = []
    for err in error_messages:
        group = getattr(err, "error_group", None)
        if group:
            groups.append(group)
    return groups


def _invoke_action_with_retry(
    module,
    api_instance,
    vm_ext_id,
    action_name,
    body,
    initial_vm,
    description,
):
    """
    Invoke a VMM $action call (with a fresh ``If-Match`` etag) and poll
    its task to completion, retrying ONLY on the transient
    ``VM_NOT_FOUND`` failure that occurs while VMM action services catch
    up to a freshly-created VM or after a concurrent modification
    invalidates the etag.

    Any other task failure is surfaced through the shared
    ``wait_for_completion`` path so error reporting stays consistent
    with the rest of the collection.

    Args:
        module: The Ansible module (for fail_json + wait polling).
        api_instance: The VMM API instance (``VmApi``).
        vm_ext_id: The VM UUID.
        action_name: SDK method name to invoke on ``api_instance``
            (either ``add_vm_custom_attributes`` or
            ``remove_vm_custom_attributes``).
        body: The ``UpdateCustomAttributesParams`` spec to send.
        initial_vm: The VM object we already fetched (source of the
            first etag). On retries we re-fetch a fresh one.
        description: Human-readable description of the operation used in
            error messages.
    Returns:
        The response object from the last (successful) invocation. The
        caller can read ``.data.ext_id`` to get the task id.
    """
    tasks_api = get_tasks_api_instance(module)
    action_callable = getattr(api_instance, action_name)

    vm = initial_vm
    resp = None
    for attempt in range(_ACTION_RETRIES):
        etag = get_etag(vm) if vm is not None else None
        try:
            if etag:
                resp = action_callable(extId=vm_ext_id, body=body, if_match=etag)
            else:
                resp = action_callable(extId=vm_ext_id, body=body)
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while {0}".format(description),
            )

        task_ext_id = resp.data.ext_id
        # Poll until the task reaches a terminal state so we can inspect
        # the error group BEFORE handing off to the shared wait helper
        # (which would call module.fail_json on any failure and prevent
        # the retry).
        task = None
        while True:
            task = tasks_api.get_task_by_id(task_ext_id).data
            status = getattr(task, "status", None)
            if status in ("SUCCEEDED", "FAILED"):
                break
            time.sleep(_TASK_POLL_INTERVAL_SEC)

        if task.status == "SUCCEEDED":
            return resp

        # FAILED — decide whether this is the transient VM_NOT_FOUND that
        # we want to retry, or a hard failure we should surface immediately.
        if (
            _VM_NOT_FOUND_ERROR_GROUP in _task_error_groups(task)
            and attempt < _ACTION_RETRIES - 1
        ):
            time.sleep(_ACTION_BACKOFF_SEC)
            # Refetch VM + etag so the next attempt sends a fresh
            # ``If-Match`` value in case the previous etag was rejected
            # because the entity state advanced on the server.
            vm, _etag = _refetch_etag(api_instance, vm_ext_id)
            continue

        # Non-retryable failure — delegate to the shared helper so it
        # emits the standard "Task Failed" error shape.
        wait_for_completion(module, task_ext_id)

    # Exhausted retries with only VM_NOT_FOUND failures — surface the last
    # attempt through the standard fail path.
    wait_for_completion(module, resp.data.ext_id)
    return resp


def _refetch_etag(api_instance, vm_ext_id):
    """Re-fetch the VM and return a fresh ``If-Match`` etag for it."""
    vm = _fetch_vm_or_none(api_instance, vm_ext_id)
    if vm is None:
        return None, None
    return vm, get_etag(vm)


def add_vm_custom_attributes(module, api_instance, result):
    """Add custom attributes to a VM using the AddVmCustomAttributes action."""
    vm_ext_id = module.params["ext_id"]
    requested = list(module.params.get("custom_attributes") or [])
    result["ext_id"] = vm_ext_id

    # In check_mode do NOT touch the API — just show what the module would send.
    # This mirrors the "pure action" contract and keeps check_mode usable even
    # when the caller does not have READ permission on the target VM.
    if module.check_mode:
        spec = vmm_sdk.UpdateCustomAttributesParams(custom_attributes=requested)
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Would add custom attributes to VM with ext_id: {0}".format(
            vm_ext_id
        )
        return

    # Fetch the VM once — used both for idempotency filtering AND to obtain
    # the ``If-Match`` etag required by the $action endpoint.
    vm = _resolve_vm_or_fail(module, api_instance, vm_ext_id)
    current = list(vm.custom_attributes or [])
    to_add = [attr for attr in requested if attr not in current]

    if not to_add:
        result["skipped"] = True
        result["response"] = current
        module.exit_json(msg="Nothing to change.", **result)

    spec = vmm_sdk.UpdateCustomAttributesParams(custom_attributes=to_add)

    if module.params.get("wait"):
        resp = _invoke_action_with_retry(
            module,
            api_instance,
            vm_ext_id,
            action_name="add_vm_custom_attributes",
            body=spec,
            initial_vm=vm,
            description="adding custom attributes to VM",
        )
        result["task_ext_id"] = resp.data.ext_id
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        _refresh_custom_attributes(module, api_instance, vm_ext_id, result)
    else:
        etag = get_etag(vm)
        try:
            resp = api_instance.add_vm_custom_attributes(
                extId=vm_ext_id, body=spec, if_match=etag
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while adding custom attributes to VM",
            )
        result["task_ext_id"] = resp.data.ext_id
        result["response"] = strip_internal_attributes(resp.data.to_dict())

    result["changed"] = True


def remove_vm_custom_attributes(module, api_instance, result):
    """Remove custom attributes from a VM using the RemoveVmCustomAttributes action."""
    vm_ext_id = module.params["ext_id"]
    requested = list(module.params.get("custom_attributes") or [])
    result["ext_id"] = vm_ext_id

    # In check_mode do NOT touch the API — just show what the module would send.
    if module.check_mode:
        spec = vmm_sdk.UpdateCustomAttributesParams(custom_attributes=requested)
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Would remove custom attributes from VM with ext_id: {0}".format(vm_ext_id)
        )
        return

    # Fetch the VM once — used both for idempotency filtering AND to obtain
    # the ``If-Match`` etag required by the $action endpoint.
    vm = _resolve_vm_or_fail(module, api_instance, vm_ext_id)
    current = list(vm.custom_attributes or [])
    to_remove = [attr for attr in requested if attr in current]

    if not to_remove:
        result["skipped"] = True
        result["response"] = current
        module.exit_json(msg="Nothing to change.", **result)

    spec = vmm_sdk.UpdateCustomAttributesParams(custom_attributes=to_remove)

    if module.params.get("wait"):
        resp = _invoke_action_with_retry(
            module,
            api_instance,
            vm_ext_id,
            action_name="remove_vm_custom_attributes",
            body=spec,
            initial_vm=vm,
            description="removing custom attributes from VM",
        )
        result["task_ext_id"] = resp.data.ext_id
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        _refresh_custom_attributes(module, api_instance, vm_ext_id, result)
    else:
        etag = get_etag(vm)
        try:
            resp = api_instance.remove_vm_custom_attributes(
                extId=vm_ext_id, body=spec, if_match=etag
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while removing custom attributes from VM",
            )
        result["task_ext_id"] = resp.data.ext_id
        result["response"] = strip_internal_attributes(resp.data.to_dict())

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
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_vm_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        add_vm_custom_attributes(module, api_instance, result)
    else:
        remove_vm_custom_attributes(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
