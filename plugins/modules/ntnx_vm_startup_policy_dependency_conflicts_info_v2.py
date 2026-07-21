#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_dependency_conflicts_info_v2
short_description: Fetch VM startup policy dependency conflicts in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about VmStartupPolicyDependencyConflict in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VmStartupPolicyDependencyConflict.
  - If C(ext_id) is not provided, list multiple VmStartupPolicyDependencyConflict for the given VM startup policy.
  - Optionally fetch the dependee VMs or dependent VMs associated with a specific dependency conflict by
    setting C(fetch_type) together with C(ext_id).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get VM startup policy dependency conflict by ext_id) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
      Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer
    - >-
      B(List VM startup policy dependency conflicts) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
      Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  vm_startup_policy_ext_id:
    description:
      - The external ID of the parent VM startup policy.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the VM startup policy dependency conflict.
      - Required when fetching a single dependency conflict or when using C(fetch_type).
    type: str
    required: false
  fetch_type:
    description:
      - When set, fetch a sub-collection scoped to the dependency conflict referenced by C(ext_id).
      - C(dependee_vms) lists the dependee VMs of the dependency conflict.
      - C(dependent_vms) lists the dependent VMs of the dependency conflict.
      - Requires C(ext_id) to be provided.
    type: str
    choices:
      - dependee_vms
      - dependent_vms
    required: false
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
- name: List all dependency conflicts for a VM startup policy
  nutanix.ncp.ntnx_vm_startup_policy_dependency_conflicts_info_v2:
    vm_startup_policy_ext_id: "8c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true

- name: List dependency conflicts with pagination
  nutanix.ncp.ntnx_vm_startup_policy_dependency_conflicts_info_v2:
    vm_startup_policy_ext_id: "8c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    page: 0
    limit: 5
  register: result
  ignore_errors: true

- name: Fetch a specific dependency conflict by external ID
  nutanix.ncp.ntnx_vm_startup_policy_dependency_conflicts_info_v2:
    vm_startup_policy_ext_id: "8c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    ext_id: "0b0f7f13-3d13-4bfb-9df0-2af1a4a3e21b"
  register: result
  ignore_errors: true

- name: List dependee VMs for a specific dependency conflict
  nutanix.ncp.ntnx_vm_startup_policy_dependency_conflicts_info_v2:
    vm_startup_policy_ext_id: "8c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    ext_id: "0b0f7f13-3d13-4bfb-9df0-2af1a4a3e21b"
    fetch_type: dependee_vms
  register: result
  ignore_errors: true

- name: List dependent VMs for a specific dependency conflict
  nutanix.ncp.ntnx_vm_startup_policy_dependency_conflicts_info_v2:
    vm_startup_policy_ext_id: "8c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    ext_id: "0b0f7f13-3d13-4bfb-9df0-2af1a4a3e21b"
    fetch_type: dependent_vms
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmStartupPolicyDependencyConflict info v4 API.
    - It can be a single VmStartupPolicyDependencyConflict if external ID is provided.
    - List of multiple VmStartupPolicyDependencyConflict if external ID is not provided.
    - When C(fetch_type=dependee_vms) or C(fetch_type=dependent_vms), it contains the list of associated VMs.
  returned: always
  type: dict
  sample:
    {
      "category_dependency_chain": [
        {
          "dependee_category": {
            "ext_id": "9dc2b6b4-6b04-4c1c-9d24-ad46d5b7b7e2"
          },
          "dependent_category": {
            "ext_id": "8f0f7e42-9c1f-4d0a-9c53-5f7a3d84f3c8"
          }
        }
      ],
      "dependee_category": {
        "ext_id": "9dc2b6b4-6b04-4c1c-9d24-ad46d5b7b7e2"
      },
      "dependee_vms_associated_categories": null,
      "dependent_category": {
        "ext_id": "8f0f7e42-9c1f-4d0a-9c53-5f7a3d84f3c8"
      },
      "dependent_vms_associated_categories": null,
      "ext_id": "0b0f7f13-3d13-4bfb-9df0-2af1a4a3e21b",
      "links": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - The external ID of the VM startup policy dependency conflict when fetched by ID.
  returned: when external ID is provided
  type: str
  sample: "0b0f7f13-3d13-4bfb-9df0-2af1a4a3e21b"

vm_startup_policy_ext_id:
  description:
    - The external ID of the parent VM startup policy.
  returned: always
  type: str
  sample: "8c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

total_available_results:
  description:
    - The total number of available dependency conflicts for the given VM startup policy
      (or associated VMs when C(fetch_type) is used).
  type: int
  returned: when a list operation is executed
  sample: 0

msg:
  description: Status/error message.
  returned: When there is an error or a validation message
  type: str
  sample: "Api Exception raised while fetching VM startup policy dependency conflicts info"

error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

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
    get_vm_startup_policy_dependency_conflict,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_startup_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        fetch_type=dict(
            type="str",
            choices=["dependee_vms", "dependent_vms"],
        ),
    )
    return module_args


def _get_pagination_kwargs(module):
    """Build page/limit kwargs from module params (only fields the SDK accepts)."""
    kwargs = {}
    if module.params.get("page") is not None:
        kwargs["_page"] = module.params.get("page")
    if module.params.get("limit") is not None:
        kwargs["_limit"] = module.params.get("limit")
    return kwargs


def get_dependency_conflict_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    vm_startup_policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    resp = get_vm_startup_policy_dependency_conflict(
        module=module,
        api_instance=api_instance,
        ext_id=ext_id,
        vm_startup_policy_ext_id=vm_startup_policy_ext_id,
    )
    result["ext_id"] = ext_id
    result["vm_startup_policy_ext_id"] = vm_startup_policy_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_dependency_conflicts(module, api_instance, result):
    vm_startup_policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    result["vm_startup_policy_ext_id"] = vm_startup_policy_ext_id

    sg = SpecGenerator(module)
    _kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM startup policy dependency conflicts info spec",
            **result,
        )

    kwargs = _get_pagination_kwargs(module)
    try:
        resp = api_instance.list_vm_startup_policy_dependency_conflicts(
            vmStartupPolicyExtId=vm_startup_policy_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM startup policy dependency conflicts info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp_dict = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp_dict:
        resp_dict = []
    result["response"] = resp_dict


def list_dependency_conflict_vms(module, api_instance, result):
    """List dependee VMs or dependent VMs for a specific dependency conflict."""
    vm_startup_policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    ext_id = module.params.get("ext_id")
    fetch_type = module.params.get("fetch_type")
    result["vm_startup_policy_ext_id"] = vm_startup_policy_ext_id
    result["ext_id"] = ext_id

    kwargs = _get_pagination_kwargs(module)

    if fetch_type == "dependee_vms":
        sdk_method = (
            api_instance.list_vm_startup_policy_dependency_conflict_dependee_vms
        )
        error_msg = "Api Exception raised while fetching dependee VMs of VM startup policy dependency conflict"
    else:
        sdk_method = (
            api_instance.list_vm_startup_policy_dependency_conflict_dependent_vms
        )
        error_msg = "Api Exception raised while fetching dependent VMs of VM startup policy dependency conflict"

    try:
        resp = sdk_method(
            vmStartupPolicyExtId=vm_startup_policy_ext_id,
            dependencyConflictExtId=ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=error_msg,
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp_dict = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp_dict:
        resp_dict = []
    result["response"] = resp_dict


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_if=[
            ("fetch_type", "dependee_vms", ("ext_id",)),
            ("fetch_type", "dependent_vms", ("ext_id",)),
        ],
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "vm_startup_policy_ext_id": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_vm_startup_policies_api_instance(module)

    if module.params.get("fetch_type"):
        list_dependency_conflict_vms(module, api_instance, result)
    elif module.params.get("ext_id"):
        get_dependency_conflict_by_ext_id(module, api_instance, result)
    else:
        list_dependency_conflicts(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
