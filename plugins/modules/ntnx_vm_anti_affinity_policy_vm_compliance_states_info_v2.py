#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_anti_affinity_policy_vm_compliance_states_info_v2
short_description: Fetch VM-VM anti-affinity policy VM compliance states in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about VmAntiAffinityPolicyVmComplianceState in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VmAntiAffinityPolicyVmComplianceState.
  - If C(ext_id) is not provided, list multiple VmAntiAffinityPolicyVmComplianceState optionally paginated
    via C(page) and C(limit).
  - The underlying API only exposes a list endpoint for VM compliance states; when C(ext_id) is
    supplied this module lists the compliance states under the given policy and filters
    client-side by the compliance state external identifier.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List compliance states of VMs in a VM-VM anti-affinity policy) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin,
      Super Admin, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  vm_anti_affinity_policy_ext_id:
    description:
      - A globally unique identifier of a VM-VM anti-affinity policy of type UUID.
      - This is the parent policy whose per-VM compliance states are being queried.
    type: str
    required: true
  ext_id:
    description:
      - External identifier of a specific VM compliance state under the given VM-VM anti-affinity policy.
      - When provided, the module lists compliance states under the parent policy and returns the
        entry whose external identifier matches (client-side filter — the API does not expose a
        dedicated get-by-id endpoint for compliance states).
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List VM compliance states for a VM-VM anti-affinity policy
  nutanix.ncp.ntnx_vm_anti_affinity_policy_vm_compliance_states_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_anti_affinity_policy_ext_id: "7bea69e9-684c-4736-7805-d658ee17c1b6"
  register: result
  ignore_errors: true

- name: List VM compliance states with pagination
  nutanix.ncp.ntnx_vm_anti_affinity_policy_vm_compliance_states_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_anti_affinity_policy_ext_id: "7bea69e9-684c-4736-7805-d658ee17c1b6"
    page: 0
    limit: 10
  register: result
  ignore_errors: true

- name: Fetch a specific VM compliance state by ext_id (client-side filter)
  nutanix.ncp.ntnx_vm_anti_affinity_policy_vm_compliance_states_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_anti_affinity_policy_ext_id: "7bea69e9-684c-4736-7805-d658ee17c1b6"
    ext_id: "0a5b9d0e-1234-4a7f-b8fa-9e5f4d1e78d1"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmAntiAffinityPolicyVmComplianceState info v4 API.
    - A single VM compliance state dict when C(ext_id) is provided.
    - A list of VM compliance state dicts when C(ext_id) is not provided.
  returned: always
  type: dict
  sample:
    [
      {
        "associated_categories": [
          {
            "ext_id": "b1c2f7d4-3a2b-4c56-8f01-1234567890ab"
          }
        ],
        "cluster": {
          "ext_id": "000647b8-ddb3-6bbb-0000-000000028f57"
        },
        "compliance_status": {
          "$objectType": "vmm.v4.ahv.policies.CompliantVmAntiAffinityPolicy"
        },
        "ext_id": "0a5b9d0e-1234-4a7f-b8fa-9e5f4d1e78d1",
        "host": {
          "ext_id": "8300384a-56ee-4750-aeb8-3d1c42908bee"
        },
        "links": null,
        "tenant_id": null
      }
    ]

changed:
  description: Whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Message describing the outcome. Populated on error and when a client-side filter
               fails to find a compliance state matching the supplied C(ext_id).
  returned: When there is an error or a client-side match is required
  type: str
  sample: "Api Exception raised while fetching VM-VM anti-affinity policy VM compliance states info"

error:
  description: Error details, populated when an exception is raised.
  type: str
  returned: when an error occurs

failed:
  description: Whether the module failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the VM compliance state (echoed when C(ext_id) is provided).
  type: str
  returned: when external ID is provided
  sample: "0a5b9d0e-1234-4a7f-b8fa-9e5f4d1e78d1"

vm_anti_affinity_policy_ext_id:
  description: External ID of the VM-VM anti-affinity policy whose compliance states were queried.
  type: str
  returned: always
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description: Total number of VM compliance states available for the parent policy.
  type: int
  returned: when all compliance states are listed
  sample: 3
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
    get_vm_anti_affinity_policies_api_instance,
)

# Suppress the InsecureRequestWarning; SDK import errors are surfaced by
# ``get_api_client`` via ``missing_required_lib`` when the SDK is missing.
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_anti_affinity_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def _list_compliance_states(module, api_instance, kwargs):
    """Invoke the list API and translate SDK errors into module failures."""
    vm_anti_affinity_policy_ext_id = module.params.get("vm_anti_affinity_policy_ext_id")
    try:
        return api_instance.list_vm_anti_affinity_policy_vm_compliance_states(
            vmAntiAffinityPolicyExtId=vm_anti_affinity_policy_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM-VM anti-affinity policy VM compliance states info",
        )


def get_vm_anti_affinity_policy_vm_compliance_state(module, api_instance, result):
    """Return the compliance state entry matching a specific compliance state ext_id.

    The v4 SDK does not expose a get-by-id endpoint for compliance states, so
    we list under the parent policy and filter client-side.
    """
    ext_id = module.params.get("ext_id")
    resp = _list_compliance_states(module, api_instance, kwargs={})
    result["ext_id"] = ext_id

    stripped = strip_internal_attributes(resp.to_dict()).get("data") or []
    match = next((item for item in stripped if item.get("ext_id") == ext_id), None)
    if not match:
        result["response"] = None
        module.fail_json(
            msg=(
                "VM compliance state with ext_id '{0}' was not found under "
                "VM-VM anti-affinity policy '{1}'."
            ).format(ext_id, module.params.get("vm_anti_affinity_policy_ext_id")),
            **result,
        )
    result["response"] = match


def get_vm_anti_affinity_policy_vm_compliance_states(module, api_instance, result):
    """Return the full list of compliance states for the parent policy."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM-VM anti-affinity policy VM compliance states info spec",
            **result,
        )
    kwargs.pop("_filter", None)
    kwargs.pop("_orderby", None)
    kwargs.pop("_select", None)

    resp = _list_compliance_states(module, api_instance, kwargs=kwargs)

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "vm_anti_affinity_policy_ext_id": module.params.get(
            "vm_anti_affinity_policy_ext_id"
        ),
    }
    api_instance = get_vm_anti_affinity_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_vm_anti_affinity_policy_vm_compliance_state(module, api_instance, result)
    else:
        get_vm_anti_affinity_policy_vm_compliance_states(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
