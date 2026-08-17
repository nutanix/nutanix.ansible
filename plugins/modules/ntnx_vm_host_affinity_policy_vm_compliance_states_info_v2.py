#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_host_affinity_policy_vm_compliance_states_info_v2
short_description: Fetch VM compliance states of a VM-host affinity policy in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about VmHostAffinityPolicyVmComplianceState in Nutanix Prism Central.
  - The compliance states are always scoped under a parent VM-host affinity policy, therefore
    C(vm_host_affinity_policy_ext_id) is required.
  - If C(ext_id) is not provided, list all VM compliance states of the given VM-host affinity policy
    optionally paginated using C(page) and C(limit).
  - If C(ext_id) is provided, filter the listed VM compliance states client-side and return the
    single matching entry (the underlying v4.2 SDK does not expose a get-by-id endpoint for
    compliance states).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List VM compliance states of a VM-host affinity policy) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  vm_host_affinity_policy_ext_id:
    description:
      - The external ID (UUID) of the parent VM-host affinity policy whose VM
        compliance states are being fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external ID (UUID) of a specific VM compliance state entry.
      - When provided, the module lists all compliance states of the parent policy
        and returns the single entry whose C(ext_id) matches.
      - When not provided, the module returns the full list.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Nutanix (@nutanix)
"""

EXAMPLES = r"""
- name: List all VM compliance states of a VM-host affinity policy
  nutanix.ncp.ntnx_vm_host_affinity_policy_vm_compliance_states_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_host_affinity_policy_ext_id: "b8f4e94b-1234-4567-8b19-6c3f2d1e8a90"
  register: all_compliance_states

- name: Paginate VM compliance states of a VM-host affinity policy
  nutanix.ncp.ntnx_vm_host_affinity_policy_vm_compliance_states_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_host_affinity_policy_ext_id: "b8f4e94b-1234-4567-8b19-6c3f2d1e8a90"
    page: 0
    limit: 10
  register: paginated_compliance_states

- name: Fetch a single VM compliance state by ext_id
  nutanix.ncp.ntnx_vm_host_affinity_policy_vm_compliance_states_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_host_affinity_policy_ext_id: "b8f4e94b-1234-4567-8b19-6c3f2d1e8a90"
    ext_id: "3f2504e0-4f89-11d3-9a0c-0305e82c3301"
  register: single_compliance_state
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmHostAffinityPolicyVmComplianceState info v4 API.
    - When C(ext_id) is provided, this is a single VmHostAffinityPolicyVmComplianceState entry.
    - When C(ext_id) is not provided, this is the list of VmHostAffinityPolicyVmComplianceState
      entries for the parent VM-host affinity policy (optionally paginated by C(page)/C(limit)).
  returned: always
  type: dict
  sample:
    [
        {
            "associated_categories": [
                {
                    "ext_id": "eb8b02f8-9dc8-5f2e-bc5b-4a1c0c2b6c93"
                }
            ],
            "cluster": {
                "ext_id": "000647b8-ddb3-6bbb-0000-000000028f57"
            },
            "compliance_status": {
                "$objectType": "vmm.v4.ahv.policies.CompliantVmHostAffinityPolicy"
            },
            "ext_id": "3f2504e0-4f89-11d3-9a0c-0305e82c3301",
            "host": {
                "ext_id": "f28e7475-f835-42ef-ac35-ecbc48d5421e"
            },
            "links": null,
            "tenant_id": null
        }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Info modules never change cluster state.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, or when a specific ext_id was requested but not found.
  type: str
  sample: "Api Exception raised while fetching VM host affinity policy VM compliance states info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task has failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the VM compliance state entry, echoed back when a specific one is requested.
  type: str
  returned: when C(ext_id) is provided
  sample: "3f2504e0-4f89-11d3-9a0c-0305e82c3301"

vm_host_affinity_policy_ext_id:
  description: The external ID of the parent VM-host affinity policy.
  type: str
  returned: always
  sample: "b8f4e94b-1234-4567-8b19-6c3f2d1e8a90"

total_available_results:
  description: The total number of VM compliance state entries available under the parent policy.
  type: int
  returned: when C(ext_id) is not provided
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_host_affinity_policies_api_instance,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """Argument spec for the info module.

    The underlying SDK method ``list_vm_host_affinity_policy_vm_compliance_states``
    only accepts ``vmHostAffinityPolicyExtId``, ``_page`` and ``_limit``. It does
    NOT accept ``filter``, ``orderby`` or ``select`` — those come from
    :class:`BaseInfoModule` for the sake of the shared documentation fragment
    but are ignored by this module (see ``run_module``).
    """
    module_args = dict(
        vm_host_affinity_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def _list_compliance_states(module, api_instance, kwargs):
    vm_host_affinity_policy_ext_id = module.params.get("vm_host_affinity_policy_ext_id")
    try:
        return api_instance.list_vm_host_affinity_policy_vm_compliance_states(
            vmHostAffinityPolicyExtId=vm_host_affinity_policy_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching VM host affinity policy VM "
                "compliance states info"
            ),
        )


def get_vm_host_affinity_policy_vm_compliance_state(module, api_instance, result):
    """Return a single compliance state entry that matches C(ext_id).

    The v4.2 SDK does not expose a get-by-id endpoint for VM compliance states,
    so this helper lists all entries for the parent policy and filters
    client-side. This keeps the module's UX consistent with other v4 info
    modules while remaining honest about the API surface.
    """
    ext_id = module.params.get("ext_id")
    resp = _list_compliance_states(module, api_instance, kwargs={})
    data = strip_internal_attributes(resp.to_dict()).get("data") or []
    match = next((item for item in data if item.get("ext_id") == ext_id), None)
    if match is None:
        result["response"] = None
        result["failed"] = True
        module.fail_json(
            msg=(
                "VM host affinity policy VM compliance state with ext_id "
                "'{0}' was not found under parent policy '{1}'".format(
                    ext_id, module.params.get("vm_host_affinity_policy_ext_id")
                )
            ),
            **result,
        )
    result["response"] = match


def list_vm_host_affinity_policy_vm_compliance_states(module, api_instance, result):
    """List compliance states, honoring the SDK-supported pagination options."""
    kwargs = {}
    page = module.params.get("page")
    if page is not None:
        kwargs["_page"] = page
    limit = module.params.get("limit")
    if limit is not None:
        kwargs["_limit"] = limit

    resp = _list_compliance_states(module, api_instance, kwargs)

    total_available_results = resp.metadata.total_available_results
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
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "vm_host_affinity_policy_ext_id": module.params.get(
            "vm_host_affinity_policy_ext_id"
        ),
    }
    api_instance = get_vm_host_affinity_policies_api_instance(module)
    if module.params.get("ext_id"):
        result["ext_id"] = module.params.get("ext_id")
        get_vm_host_affinity_policy_vm_compliance_state(module, api_instance, result)
    else:
        list_vm_host_affinity_policy_vm_compliance_states(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
