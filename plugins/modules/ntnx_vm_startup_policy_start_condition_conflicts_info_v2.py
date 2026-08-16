#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_start_condition_conflicts_info_v2
short_description: Fetch VM startup policy start condition conflicts info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about
    VmStartupPolicyStartConditionConflict in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific
    VmStartupPolicyStartConditionConflict scoped to the parent VM startup
    policy given by I(vm_startup_policy_ext_id).
  - If C(ext_id) is not provided, list the VmStartupPolicyStartConditionConflict
    entries for the parent VM startup policy given by
    I(vm_startup_policy_ext_id) - optionally paginated via I(page) and
    I(limit).
  - The C(dependent_vms) and C(dependee_vms) sub-lists of a specific
    start condition conflict can also be fetched by setting
    I(fetch_dependent_vms) or I(fetch_dependee_vms) together with both
    I(vm_startup_policy_ext_id) and I(ext_id).
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Read VM startup policy start condition conflicts) -
      Required Permission:
      View_VM_Startup_Policy_Start_Condition_Conflicts (present in Prism Admin,
      Super Admin, Prism Viewer and equivalent read-capable roles).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external ID of the VM startup policy start condition conflict.
      - When set, the module returns a single conflict via GET-by-ID.
    type: str
    required: false
  vm_startup_policy_ext_id:
    description:
      - The external ID of the parent VM startup policy that scopes the
        start condition conflicts.
      - Required for every operation this module performs, because start
        condition conflicts are always nested under a VM startup policy in
        the v4 API.
    type: str
    required: true
  fetch_dependent_vms:
    description:
      - If C(true) and both I(vm_startup_policy_ext_id) and I(ext_id) are
        provided, fetch the list of dependent VMs of the given start
        condition conflict instead of returning the conflict itself.
    type: bool
    required: false
    default: false
  fetch_dependee_vms:
    description:
      - If C(true) and both I(vm_startup_policy_ext_id) and I(ext_id) are
        provided, fetch the list of dependee VMs of the given start
        condition conflict instead of returning the conflict itself.
    type: bool
    required: false
    default: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all start condition conflicts for a VM startup policy
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflicts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "9b7c5c2e-9c9e-4f2d-a9c1-1e2f3a4b5c6d"
  register: result
  ignore_errors: true

- name: List start condition conflicts for a VM startup policy with pagination
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflicts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "9b7c5c2e-9c9e-4f2d-a9c1-1e2f3a4b5c6d"
    page: 0
    limit: 10
  register: result
  ignore_errors: true

- name: Get a specific start condition conflict by ext_id
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflicts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "9b7c5c2e-9c9e-4f2d-a9c1-1e2f3a4b5c6d"
    ext_id: "aa11bb22-cc33-dd44-ee55-ff6677889900"
  register: result
  ignore_errors: true

- name: Fetch dependent VMs of a start condition conflict
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflicts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "9b7c5c2e-9c9e-4f2d-a9c1-1e2f3a4b5c6d"
    ext_id: "aa11bb22-cc33-dd44-ee55-ff6677889900"
    fetch_dependent_vms: true
  register: result
  ignore_errors: true

- name: Fetch dependee VMs of a start condition conflict
  nutanix.ncp.ntnx_vm_startup_policy_start_condition_conflicts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "9b7c5c2e-9c9e-4f2d-a9c1-1e2f3a4b5c6d"
    ext_id: "aa11bb22-cc33-dd44-ee55-ff6677889900"
    fetch_dependee_vms: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmStartupPolicyStartConditionConflict info v4 API.
    - It can be a single VmStartupPolicyStartConditionConflict if C(ext_id) is
      provided and neither I(fetch_dependent_vms) nor I(fetch_dependee_vms) is
      set.
    - It is a list of VmStartupPolicyStartConditionConflict entries scoped to
      the parent VM startup policy identified by I(vm_startup_policy_ext_id) if
      C(ext_id) is not provided (optional paging via I(page)/I(limit)).
    - It is a list of dependent/dependee VMs when the corresponding
      I(fetch_dependent_vms) / I(fetch_dependee_vms) toggle is set together
      with both parent and conflict external IDs.
  returned: always
  type: dict
  sample:
    {
      "conflicting_policy": {
          "ext_id": "d13a2c9a-3d5e-4a6c-8c9d-1e2f3a4b5c6d",
          "name": "startup-policy-web-tier"
      },
      "conflicting_start_condition": {
          "delay_duration_secs": 300,
          "power_state_criteria": "GUEST_OS_READY"
      },
      "dependee_category": {
          "ext_id": "c1a2b3c4-d5e6-4f78-90ab-cdef01234567",
          "name": "Environment:Prod"
      },
      "dependee_vms_associated_categories": [
          {
              "ext_id": "c1a2b3c4-d5e6-4f78-90ab-cdef01234567",
              "name": "Environment:Prod"
          }
      ],
      "dependent_category": {
          "ext_id": "d2a3b4c5-e6f7-4089-a1b2-c3d4e5f60718",
          "name": "AppTier:Web"
      },
      "dependent_vms_associated_categories": [
          {
              "ext_id": "d2a3b4c5-e6f7-4089-a1b2-c3d4e5f60718",
              "name": "AppTier:Web"
          }
      ],
      "ext_id": "aa11bb22-cc33-dd44-ee55-ff6677889900",
      "links": null,
      "start_condition": {
          "delay_duration_secs": 60,
          "power_state_criteria": "POWERED_ON"
      },
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM startup policy start condition conflicts info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the VM startup policy start condition conflict.
  type: str
  returned: when external ID is provided
  sample: "aa11bb22-cc33-dd44-ee55-ff6677889900"

total_available_results:
  description: The total number of available start condition conflicts on the parent VM startup policy.
  type: int
  returned: when all start condition conflicts are fetched (list operations)
  sample: 3
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_startup_policies_api_instance,
)
from ..module_utils.v4.vmm.helpers import (  # noqa: E402
    get_vm_startup_policy_start_condition_conflict,
)

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as virtual_machine_management_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as virtual_machine_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Reference the SDK's StartConditionConflict model so the import above is
# consumed. This is a read-only, derived entity so we do not need any SDK
# constructors here, but keeping a live reference means the module fails
# cleanly at import time if the SDK layout ever changes.
SDK_START_CONDITION_CONFLICT_MODEL = getattr(
    virtual_machine_management_sdk, "StartConditionConflict", None
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        vm_startup_policy_ext_id=dict(type="str", required=True),
        fetch_dependent_vms=dict(type="bool", default=False),
        fetch_dependee_vms=dict(type="bool", default=False),
    )
    return module_args


def _paging_kwargs(module):
    """Return only the paging kwargs the nested list APIs accept."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        return None, err
    return {k: v for k, v in kwargs.items() if k in ("_page", "_limit")}, None


def get_vm_startup_policy_start_condition_conflict_using_ext_id(
    module, api_instance, result
):
    ext_id = module.params.get("ext_id")
    parent_ext_id = module.params.get("vm_startup_policy_ext_id")
    resp = get_vm_startup_policy_start_condition_conflict(
        module=module,
        api_instance=api_instance,
        ext_id=ext_id,
        vm_startup_policy_ext_id=parent_ext_id,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def _list_and_flatten(module, list_call, err_msg, result, kwargs):
    try:
        resp = list_call(**kwargs)
    except Exception as e:
        raise_api_exception(module=module, exception=e, msg=err_msg)

    resp = strip_internal_attributes(resp.to_dict())
    metadata = resp.get("metadata") or {}
    total_available_results = metadata.get("total_available_results")
    result["total_available_results"] = total_available_results
    data = resp.get("data")
    if not data:
        data = []
    result["response"] = data


def list_vm_startup_policy_start_condition_conflicts(module, api_instance, result):
    parent_ext_id = module.params.get("vm_startup_policy_ext_id")
    kwargs, err = _paging_kwargs(module)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM startup policy start condition conflicts info spec",
            **result,
        )
    kwargs["vmStartupPolicyExtId"] = parent_ext_id
    _list_and_flatten(
        module,
        api_instance.list_vm_startup_policy_start_condition_conflicts,
        "Api Exception raised while fetching VM startup policy start condition conflicts info",
        result,
        kwargs,
    )


def list_start_condition_conflict_dependent_vms(module, api_instance, result):
    parent_ext_id = module.params.get("vm_startup_policy_ext_id")
    ext_id = module.params.get("ext_id")
    kwargs, err = _paging_kwargs(module)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM startup policy start condition conflict dependent VMs info spec",
            **result,
        )
    kwargs["vmStartupPolicyExtId"] = parent_ext_id
    kwargs["startConditionConflictExtId"] = ext_id
    result["ext_id"] = ext_id
    _list_and_flatten(
        module,
        api_instance.list_vm_startup_policy_start_condition_conflict_dependent_vms,
        "Api Exception raised while fetching dependent VMs of VM startup policy start condition conflict",
        result,
        kwargs,
    )


def list_start_condition_conflict_dependee_vms(module, api_instance, result):
    parent_ext_id = module.params.get("vm_startup_policy_ext_id")
    ext_id = module.params.get("ext_id")
    kwargs, err = _paging_kwargs(module)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM startup policy start condition conflict dependee VMs info spec",
            **result,
        )
    kwargs["vmStartupPolicyExtId"] = parent_ext_id
    kwargs["startConditionConflictExtId"] = ext_id
    result["ext_id"] = ext_id
    _list_and_flatten(
        module,
        api_instance.list_vm_startup_policy_start_condition_conflict_dependee_vms,
        "Api Exception raised while fetching dependee VMs of VM startup policy start condition conflict",
        result,
        kwargs,
    )


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
            ("fetch_dependent_vms", "fetch_dependee_vms"),
        ],
        required_if=[
            ("fetch_dependent_vms", True, ("ext_id",)),
            ("fetch_dependee_vms", True, ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vm_startup_policies_api_instance(module)
    ext_id = module.params.get("ext_id")
    if ext_id and module.params.get("fetch_dependent_vms"):
        list_start_condition_conflict_dependent_vms(module, api_instance, result)
    elif ext_id and module.params.get("fetch_dependee_vms"):
        list_start_condition_conflict_dependee_vms(module, api_instance, result)
    elif ext_id:
        get_vm_startup_policy_start_condition_conflict_using_ext_id(
            module, api_instance, result
        )
    else:
        list_vm_startup_policy_start_condition_conflicts(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
