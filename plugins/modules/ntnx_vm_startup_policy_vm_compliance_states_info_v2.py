#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_vm_compliance_states_info_v2
short_description: Fetch VM compliance states of a VM startup policy in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about VmStartupPolicyVmComplianceState in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VmStartupPolicyVmComplianceState.
  - If C(ext_id) is not provided, list multiple VmStartupPolicyVmComplianceState optionally paginated.
  - The SDK endpoint C(list_vm_startup_policy_vm_compliance_states) supports pagination
    (C(page), C(limit)) only. Filter and orderby query parameters are not supported by the API.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List VM compliance states of a VM startup policy) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, Virtual Machine Admin,
    Virtual Machine Operator, Virtual Machine Viewer
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  vm_startup_policy_ext_id:
    description:
      - The external ID of the parent VM startup policy whose VM compliance
        states are being fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of a specific VM compliance state.
      - When provided, the module filters the list to return the matching
        VM compliance state entry. If not provided, all compliance states for
        the parent VM startup policy are returned.
    type: str
  page:
    description:
      - A URL query parameter that specifies the page number of the result set.
      - Must be a positive integer between 0 and the maximum number of pages
        that are available for that resource. Any number out of this range
        might lead to no results.
    type: int
  limit:
    description:
      - A URL query parameter that specifies the total number of records
        returned in the result set.
      - Must be a positive integer between 1 and 100. If not provided, the
        API returns 50 records by default.
    type: int
  read_timeout:
    description:
      - Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all VM compliance states of a VM startup policy
  nutanix.ncp.ntnx_vm_startup_policy_vm_compliance_states_info_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    validate_certs: false
    vm_startup_policy_ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
  register: result
  ignore_errors: true

- name: List VM compliance states of a VM startup policy with pagination
  nutanix.ncp.ntnx_vm_startup_policy_vm_compliance_states_info_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    validate_certs: false
    vm_startup_policy_ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
    page: 0
    limit: 10
  register: result
  ignore_errors: true

- name: Fetch a specific VM compliance state by ext_id
  nutanix.ncp.ntnx_vm_startup_policy_vm_compliance_states_info_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    validate_certs: false
    vm_startup_policy_ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
    ext_id: "ea9c8f4c-97ec-4f7a-9e2b-33f36f9b6a19"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmStartupPolicyVmComplianceState info v4 API.
    - It can be a single VmStartupPolicyVmComplianceState if external ID is provided.
    - List of multiple VmStartupPolicyVmComplianceState if external ID is not provided.
  returned: always
  type: dict
  sample: []

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the VM compliance state when provided as input.
  returned: when C(ext_id) is provided
  type: str
  sample: "ea9c8f4c-97ec-4f7a-9e2b-33f36f9b6a19"

vm_startup_policy_ext_id:
  description: External ID of the parent VM startup policy.
  returned: always
  type: str
  sample: "9b1a818d-0d1a-4c4e-4bd2-094e27cae1d5"

total_available_results:
  description: The total number of VM compliance states available for the parent VM startup policy.
  returned: when the full list is fetched
  type: int
  sample: 0

msg:
  description: Status/error message returned by the module.
  returned: contextual
  type: str
  sample: "No VM compliance state with ext_id '00000000-0000-0000-0000-000000000000' was found for VM startup policy '9b1a818d-0d1a-4c4e-4bd2-094e27cae1d5'."

error:
  description: Error details when an API/operation failure occurs.
  returned: when an error occurs
  type: str

failed:
  description: Indicates whether the module failed.
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    from ..module_utils.v4.vmm.api_client import (  # noqa: E402
        get_vm_startup_policies_api_instance,
    )
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk  # noqa: E402

    get_vm_startup_policies_api_instance = mock_sdk  # type: ignore[assignment]
    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_startup_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        page=dict(type="int"),
        limit=dict(type="int"),
    )
    return module_args


def _list_all_compliance_states(module, api_instance, vm_startup_policy_ext_id, kwargs):
    """
    Fetch the raw ListVmStartupPolicyVmComplianceStatesApiResponse and return the
    (response_dict, total_available_results) tuple. Raises via
    C(raise_api_exception) on SDK errors.
    """
    try:
        resp = api_instance.list_vm_startup_policy_vm_compliance_states(
            vmStartupPolicyExtId=vm_startup_policy_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM startup policy VM compliance states info",
        )

    total_available_results = resp.metadata.total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    return resp, total_available_results


def _build_pagination_kwargs(module):
    """
    Build the SDK pagination kwargs from module params. Only C(_page) and
    C(_limit) are supported by the underlying SDK method; other info args
    like C(filter), C(orderby), C(select) are not accepted by this endpoint
    and are ignored to avoid sending unsupported query parameters.
    """
    kwargs = {}
    if module.params.get("page") is not None:
        kwargs["_page"] = module.params.get("page")
    if module.params.get("limit") is not None:
        kwargs["_limit"] = module.params.get("limit")
    return kwargs


def get_vm_startup_policy_vm_compliance_state_by_ext_id(module, api_instance, result):
    """
    The SDK does not expose a Get-by-Id endpoint for a single compliance
    state entry, so we fetch the full list and locate the matching item
    client-side. This preserves standard info-module get-by-id ergonomics.
    """
    vm_startup_policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    ext_id = module.params.get("ext_id")

    kwargs = _build_pagination_kwargs(module)
    entries, _total = _list_all_compliance_states(
        module, api_instance, vm_startup_policy_ext_id, kwargs
    )

    match = next((item for item in entries if item.get("ext_id") == ext_id), None)
    if match is None:
        module.fail_json(
            msg=(
                "No VM compliance state with ext_id '{0}' was found for VM "
                "startup policy '{1}'."
            ).format(ext_id, vm_startup_policy_ext_id),
            failed=True,
            response=None,
            changed=False,
        )

    result["ext_id"] = ext_id
    result["response"] = match


def list_vm_startup_policy_vm_compliance_states(module, api_instance, result):
    vm_startup_policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    kwargs = _build_pagination_kwargs(module)

    entries, total_available_results = _list_all_compliance_states(
        module, api_instance, vm_startup_policy_ext_id, kwargs
    )

    result["total_available_results"] = total_available_results
    result["response"] = entries


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)

    result = {
        "changed": False,
        "response": None,
        "vm_startup_policy_ext_id": module.params.get("vm_startup_policy_ext_id"),
        "failed": False,
    }

    api_instance = get_vm_startup_policies_api_instance(module)

    if module.params.get("ext_id"):
        get_vm_startup_policy_vm_compliance_state_by_ext_id(
            module, api_instance, result
        )
    else:
        list_vm_startup_policy_vm_compliance_states(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
