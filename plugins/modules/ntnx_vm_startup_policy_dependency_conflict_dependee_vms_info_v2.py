#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_dependency_conflict_dependee_vms_info_v2
short_description: Fetch dependee VMs of a VM startup policy dependency conflict in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about VmStartupPolicyDependencyConflictDependeeVm in Nutanix Prism Central.
  - Lists the dependee VMs (VMs that other VMs depend on) that are involved in a specific dependency conflict of a VM startup policy.
  - A dependee VM is a VM referenced as a prerequisite by other VMs in a startup policy's dependency graph.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List dependee VMs of a VM startup policy dependency conflict) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  vm_startup_policy_ext_id:
    description:
      - The external ID (UUID) of the VM startup policy whose dependency conflict's dependee VMs need to be listed.
      - This is a path parameter required by the underlying v4 API.
    type: str
    required: true
  dependency_conflict_ext_id:
    description:
      - The external ID (UUID) of the dependency conflict of the specified VM startup policy.
      - This is a path parameter required by the underlying v4 API.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all dependee VMs of a VM startup policy dependency conflict
  nutanix.ncp.ntnx_vm_startup_policy_dependency_conflict_dependee_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "e3d33be5-ea1e-4b6a-a30d-4f1f8d0a1b21"
    dependency_conflict_ext_id: "9f6141a0-4a34-46e3-a4cf-4fe25d05c8f7"
  register: result
  ignore_errors: true

- name: List dependee VMs of a dependency conflict with pagination
  nutanix.ncp.ntnx_vm_startup_policy_dependency_conflict_dependee_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "e3d33be5-ea1e-4b6a-a30d-4f1f8d0a1b21"
    dependency_conflict_ext_id: "9f6141a0-4a34-46e3-a4cf-4fe25d05c8f7"
    page: 0
    limit: 10
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmStartupPolicyDependencyConflictDependeeVm info v4 API.
    - It is a list of dependee VMs of the given VM startup policy dependency conflict.
    - Each entry is a VM reference containing the external ID of the dependee VM.
    - The list can be paginated using the C(page) and C(limit) parameters.
  returned: always
  type: dict
  sample:
    [
      {
        "ext_id": "3ac9fb37-3c9d-4a11-b3f7-4f9e05c26e0a"
      },
      {
        "ext_id": "7b4c4f27-06a5-4a72-9d55-6b8e6acdbfa4"
      }
    ]

total_available_results:
  description:
    - The total number of dependee VMs available for the specified dependency conflict.
  type: int
  returned: always
  sample: 2

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM startup policy dependency conflict dependee VMs info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task has failed.
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_startup_policy_ext_id=dict(type="str", required=True),
        dependency_conflict_ext_id=dict(type="str", required=True),
    )
    return module_args


def list_vm_startup_policy_dependency_conflict_dependee_vms(
    module, api_instance, result
):
    """
    List the dependee VMs of a VM startup policy dependency conflict.

    Args:
        module: The AnsibleModule instance.
        api_instance: VmStartupPoliciesApi instance from ntnx_vmm_py_client.
        result: The result dict to populate.
    """
    vm_startup_policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    dependency_conflict_ext_id = module.params.get("dependency_conflict_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg=(
                "Failed generating VM startup policy dependency conflict "
                "dependee VMs info spec"
            ),
            **result,
        )

    # Drop unsupported query params — this list API only supports _page/_limit.
    for key in list(kwargs.keys()):
        if key not in ("_page", "_limit"):
            kwargs.pop(key)

    try:
        resp = api_instance.list_vm_startup_policy_dependency_conflict_dependee_vms(
            vmStartupPolicyExtId=vm_startup_policy_ext_id,
            dependencyConflictExtId=dependency_conflict_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching VM startup policy "
                "dependency conflict dependee VMs info"
            ),
        )

    total_available_results = 0
    if resp.metadata is not None:
        total_available_results = (
            getattr(resp.metadata, "total_available_results", None) or 0
        )
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vm_startup_policies_api_instance(module)
    list_vm_startup_policy_dependency_conflict_dependee_vms(
        module, api_instance, result
    )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
