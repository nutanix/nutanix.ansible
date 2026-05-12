#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vm_anti_affinity_policy_compliance_info_v2
short_description: Fetch VM compliance states for a VM anti-affinity policy in Nutanix Prism Central.
version_added: "2.6.0"
description:
    - This module fetches VM compliance states for a VM-VM anti-affinity policy in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List VM Anti-Affinity Policy VM Compliance States) -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager, Super Admin, Virtual Machine Admin,
      Virtual Machine Viewer, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - The external ID of the VM anti-affinity policy.
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
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Fetch VM anti-affinity policy compliance states
  nutanix.ncp.ntnx_vm_anti_affinity_policy_compliance_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"
  register: result

- name: Fetch VM anti-affinity policy compliance states with limit
  nutanix.ncp.ntnx_vm_anti_affinity_policy_compliance_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"
    limit: 1
  register: result
"""

RETURN = r"""
response:
    description:
        - The list of VMs for the specified VM anti-affinity policy with their compliance states.
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
                "host": null,
                "links": null,
                "tenant_id": null
            },
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
                "ext_id": "68790193-6fad-470d-69e0-eaf11051bab6",
                "host": null,
                "links": null,
                "tenant_id": null
            },
            {
                "associated_categories": [
                    {
                        "ext_id": "4d552748-e119-540a-b06c-3c6f0d213fa2"
                    }
                ],
                "cluster": {
                    "ext_id": "00065199-7144-6a68-04b8-52540041dd87"
                },
                "compliance_status": {},
                "ext_id": "779e8366-ba18-438d-7bde-c55fc2621b0f",
                "host": null,
                "links": null,
                "tenant_id": null
            },
            {
                "associated_categories": [
                    {
                        "ext_id": "4d552748-e119-540a-b06c-3c6f0d213fa2"
                    }
                ],
                "cluster": {
                    "ext_id": "00065199-7144-6a68-04b8-52540041dd87"
                },
                "compliance_status": {},
                "ext_id": "1f824b8b-f9a8-4832-79fc-d9f0c76b601f",
                "host": null,
                "links": null,
                "tenant_id": null
            },
            {
                "associated_categories": [
                    {
                        "ext_id": "0e7eee83-4313-5066-bd39-3834ac350f81"
                    }
                ],
                "cluster": {
                    "ext_id": "00065199-7144-6a68-04b8-52540041dd87"
                },
                "compliance_status": {},
                "ext_id": "7ec76b19-8bc2-408d-5ab5-f703dbb5f79d",
                "host": null,
                "links": null,
                "tenant_id": null
            },
            {
                "associated_categories": [
                    {
                        "ext_id": "0e7eee83-4313-5066-bd39-3834ac350f81"
                    }
                ],
                "cluster": {
                    "ext_id": "00065199-7144-6a68-04b8-52540041dd87"
                },
                "compliance_status": {},
                "ext_id": "9a49526c-e83c-4450-6a7a-a16248caca37",
                "host": null,
                "links": null,
                "tenant_id": null
            }
        ]

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching VM anti-affinity policy compliance states"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

total_available_results:
    description:
        - The total number of available VMs for the specified VM anti-affinity policy.
    type: int
    returned: when all VMs for the specified VM anti-affinity policy are fetched
    sample: 10
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import raise_api_exception  # noqa: E402
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_anti_affinity_policies_api_instance,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        page=dict(type="int"),
        limit=dict(type="int"),
    )
    return module_args


def get_policy_vm_compliance_states(module, api_instance, result):
    """List VM compliance states for a VM anti-affinity policy."""
    ext_id = module.params.get("ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM anti-affinity policy compliance info spec",
            **result,
        )

    try:
        resp = api_instance.list_vm_anti_affinity_policy_vm_compliance_states(
            vmAntiAffinityPolicyExtId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM anti-affinity policy compliance states",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    # Preserve discriminator/internal fields for compliance_status oneOf payloads.
    # Stripping these fields can collapse compliant/pending states to empty objects.
    resp_data = resp.to_dict().get("data")
    if resp_data:
        result["response"] = resp_data


def run_module():
    module = BaseInfoModule(
        skip_info_args=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}

    api_instance = get_vm_anti_affinity_policies_api_instance(module)
    get_policy_vm_compliance_states(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
