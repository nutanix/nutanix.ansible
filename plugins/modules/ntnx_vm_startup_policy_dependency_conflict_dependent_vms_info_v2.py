#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_dependency_conflict_dependent_vms_info_v2
short_description: Fetch dependent VMs of a Dependency conflict of a VM startup policy in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about VmStartupPolicyDependencyConflictDependentVm in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VmStartupPolicyDependencyConflictDependentVm.
  - If C(ext_id) is not provided, list multiple VmStartupPolicyDependencyConflictDependentVm optionally paginated.
  - A Dependency conflict on a VM startup policy identifies category-based startup ordering loops.
    The dependent VMs are the VMs that would be blocked from starting because their startup depends on
    other VMs (dependee VMs) that participate in the conflicting startup chain.
  - The upstream v4 SDK exposes only a list endpoint for this entity - there is no GetById, Create, Update
    or Delete method for a dependent VM entry. When C(ext_id) is provided, the module lists all dependent
    VMs and filters client-side by C(extId) to return the single match.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List dependent VMs of a Dependency conflict of a VM startup policy) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
      Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  vm_startup_policy_ext_id:
    description:
      - The external ID of the VM startup policy.
      - Required to scope the query to a specific VM startup policy.
    type: str
    required: true
  dependency_conflict_ext_id:
    description:
      - The external ID of the Dependency conflict of the VM startup policy.
      - Required to scope the query to a specific Dependency conflict.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of a specific dependent VM to fetch.
      - When set, the module lists all dependent VMs for the given Dependency conflict and returns
        only the entry whose C(extId) matches, since the v4 SDK does not expose a get-by-ID endpoint
        for dependent VMs.
    type: str
    required: false
  page:
    description:
      - A URL query parameter that specifies the page number of the result set.
      - Must be a positive integer between 0 and the maximum number of pages that are available for that resource.
      - Any number out of this range might lead to no results.
    type: int
    required: false
  limit:
    description:
      - A URL query parameter that specifies the total number of records returned in the result set.
      - Must be a positive integer between 1 and 100.
      - Any number out of this range will lead to a validation error.
      - If the limit is not provided, a default value of 50 records will be returned in the result set.
    type: int
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all dependent VMs of a Dependency conflict of a VM startup policy
  nutanix.ncp.ntnx_vm_startup_policy_dependency_conflict_dependent_vms_info_v2:
    vm_startup_policy_ext_id: "b32c4b09-4b40-4d3f-8f97-2f81b06ba6ea"
    dependency_conflict_ext_id: "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"
  register: dependent_vms_list

- name: List dependent VMs with pagination
  nutanix.ncp.ntnx_vm_startup_policy_dependency_conflict_dependent_vms_info_v2:
    vm_startup_policy_ext_id: "b32c4b09-4b40-4d3f-8f97-2f81b06ba6ea"
    dependency_conflict_ext_id: "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"
    page: 0
    limit: 10
  register: dependent_vms_paged

- name: Fetch a specific dependent VM by ext_id (client-side filter over the list)
  nutanix.ncp.ntnx_vm_startup_policy_dependency_conflict_dependent_vms_info_v2:
    vm_startup_policy_ext_id: "b32c4b09-4b40-4d3f-8f97-2f81b06ba6ea"
    dependency_conflict_ext_id: "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"
    ext_id: "aabbccdd-1111-2222-3333-444455556666"
  register: dependent_vm_detail
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmStartupPolicyDependencyConflictDependentVm info v4 API.
    - It can be a single VmStartupPolicyDependencyConflictDependentVm if external ID is provided.
    - List of multiple VmStartupPolicyDependencyConflictDependentVm if external ID is not provided
      with optional page or limit.
    - The v4 SDK does not accept filter or orderby query params for this endpoint so those are
      intentionally not exposed by this module.
  returned: always
  type: dict
  sample:
    [
      {
        "ext_id": "aabbccdd-1111-2222-3333-444455556666",
        "links": null,
        "tenant_id": null
      },
      {
        "ext_id": "aabbccdd-1111-2222-3333-777788889999",
        "links": null,
        "tenant_id": null
      }
    ]

vm_startup_policy_ext_id:
  description:
    - The external ID of the parent VM startup policy the query was scoped to.
  returned: always
  type: str
  sample: "b32c4b09-4b40-4d3f-8f97-2f81b06ba6ea"

dependency_conflict_ext_id:
  description:
    - The external ID of the parent Dependency conflict the query was scoped to.
  returned: always
  type: str
  sample: "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"

ext_id:
  description:
    - The external ID of the dependent VM that matched the caller-supplied C(ext_id).
    - Only populated when C(ext_id) is provided and the entry is found in the list result.
  returned: when C(ext_id) is provided and the entry exists in the list result
  type: str
  sample: "aabbccdd-1111-2222-3333-444455556666"

total_available_results:
  description:
    - The total number of dependent VMs available for the given Dependency conflict.
    - Populated on every successful call (both list and get-by-ext_id modes).
  returned: always
  type: int
  sample: 5

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, or when C(ext_id) is provided but not found in the list
  type: str
  sample: "Api Exception raised while fetching VmStartupPolicyDependencyConflictDependentVms info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_startup_policies_api_instance,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_startup_policy_ext_id=dict(type="str", required=True),
        dependency_conflict_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
        page=dict(type="int", required=False),
        limit=dict(type="int", required=False),
    )
    return module_args


def _build_kwargs(module):
    kwargs = {}
    page = module.params.get("page")
    if page is not None:
        kwargs["_page"] = page
    limit = module.params.get("limit")
    if limit is not None:
        kwargs["_limit"] = limit
    return kwargs


def list_dependent_vms(module, api_instance, result):
    vm_startup_policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    dependency_conflict_ext_id = module.params.get("dependency_conflict_ext_id")

    kwargs = _build_kwargs(module)

    try:
        resp = api_instance.list_vm_startup_policy_dependency_conflict_dependent_vms(
            vmStartupPolicyExtId=vm_startup_policy_ext_id,
            dependencyConflictExtId=dependency_conflict_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching "
                "VmStartupPolicyDependencyConflictDependentVms info"
            ),
        )

    total_available_results = 0
    if resp.metadata is not None:
        total_available_results = (
            getattr(resp.metadata, "total_available_results", None) or 0
        )
    result["total_available_results"] = total_available_results
    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    return data


def get_dependent_vm_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    data = list_dependent_vms(module, api_instance, result)
    match = None
    for item in data:
        if item.get("ext_id") == ext_id:
            match = item
            break
    if match is None:
        result["response"] = {}
        result["msg"] = (
            "Dependent VM with ext_id '{0}' was not found for "
            "vm_startup_policy_ext_id '{1}' and dependency_conflict_ext_id '{2}'."
        ).format(
            ext_id,
            module.params.get("vm_startup_policy_ext_id"),
            module.params.get("dependency_conflict_ext_id"),
        )
        module.fail_json(**result)
    result["ext_id"] = ext_id
    result["response"] = match


def get_dependent_vms(module, api_instance, result):
    data = list_dependent_vms(module, api_instance, result)
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        skip_info_args=True,
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vm_startup_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_dependent_vm_by_ext_id(module, api_instance, result)
    else:
        get_dependent_vms(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
