#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_vm_compliance_states_info_v2
short_description: Fetch VM compliance states for a VM startup policy in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module fetches VM compliance states for a VM startup policy in Nutanix Prism Central.
  - List VM compliances of the provided VM startup policy external identifier.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(List VM compliances of a VM startup policy) -
    Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager,
    Super Admin, Tenant Admin, Tenant Consumer, Virtual Machine Admin,
    Virtual Machine Viewer, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external ID of the VM startup policy.
    type: str
    required: true
  page:
    description:
      - A URL query parameter that specifies the page number of the result set.
    type: int
    required: false
  limit:
    description:
      - A URL query parameter that specifies the total number of records returned in the result set.
    type: int
    required: false
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
  fetch_all:
    description:
      - When C(true), paginate through the list API until all available entities are returned.
        C(page) and C(limit) are ignored; each request uses the maximum page size (100).
      - When C(false), return a single page (API default limit).
    type: bool
    required: false
    default: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch VM startup policy VM compliance states
  nutanix.ncp.ntnx_vm_startup_policy_vm_compliance_states_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
  register: result
  ignore_errors: true

- name: Fetch VM startup policy VM compliance states with limit
  nutanix.ncp.ntnx_vm_startup_policy_vm_compliance_states_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
    limit: 1
  register: result
  ignore_errors: true

- name: List all VM startup policy VM compliance states with fetch_all
  nutanix.ncp.ntnx_vm_startup_policy_vm_compliance_states_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The list of VMs for the specified VM startup policy with their compliance states.
  type: list
  returned: always
  sample:
    [
      {
          "associated_categories": [
              {
                  "ext_id": "e4bda88f-e5da-5eb1-a031-2c0bb00d923d"
              }
          ],
          "cluster": {
              "ext_id": "00065199-7144-6a68-04b8-52540041dd87"
          },
          "compliance_status": {},
          "ext_id": "45805d6a-758f-4b32-4b6b-129058e1bf0a",
          "links": null,
          "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM startup policy VM compliance states"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when there is an error
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

total_available_results:
  description:
    - The total number of available VMs for the specified VM startup policy.
  type: int
  returned: when all VMs for the specified VM startup policy are fetched
  sample: 10
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import list_entities, raise_api_exception  # noqa: E402
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_startup_policies_api_instance,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        page=dict(type="int"),
        limit=dict(type="int"),
        fetch_all=dict(type="bool", required=False, default=False),
    )
    return module_args


def get_policy_vm_compliance_states(module, api_instance, result):
    """List VM compliance states for a VM startup policy."""
    ext_id = module.params.get("ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM startup policy VM compliance info spec",
            **result,
        )

    try:
        resp = list_entities(
            api_instance.list_vm_startup_policy_vm_compliance_states,
            kwargs=kwargs,
            vmStartupPolicyExtId=ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM startup policy VM compliance states",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    # Preserve discriminator/internal fields for compliance_status oneOf payloads.
    # Stripping these fields can collapse compliant/pending states to empty objects.
    resp_data = resp.to_dict().get("data")
    if resp_data:
        result["response"] = resp_data
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        skip_info_args=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}

    api_instance = get_vm_startup_policies_api_instance(module)
    get_policy_vm_compliance_states(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
