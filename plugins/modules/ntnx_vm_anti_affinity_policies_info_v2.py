#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vm_anti_affinity_policies_info_v2
short_description: Fetches information about VM-VM anti-affinity policies in Nutanix Prism Central.
version_added: "2.6.0"
description:
    - This module fetches information about VM-VM anti-affinity policies in Nutanix Prism Central.
    - It supports fetching a single policy by external ID or listing all policies with optional filter.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get VM Anti-Affinity Policy) -
      Operation Name: Get VM Anti-Affinity Policy -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager, Super Admin, Virtual Machine Admin,
      Virtual Machine Viewer, Self-Service Admin (deprecated)
    - >-
      B(List VM Anti-Affinity Policies) -
      Operation Name: List VM Anti-Affinity Policies -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager, Super Admin, Virtual Machine Admin,
      Virtual Machine Viewer, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - The external ID of the VM anti-affinity policy.
            - If provided, fetches a single policy by its external ID.
        type: str
        required: false
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Get a VM anti-affinity policy by ID
  nutanix.ncp.ntnx_vm_anti_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "605a0cf9-d04e-3be7-911b-1e6f193f6eb9"
  register: result

- name: List all VM anti-affinity policies
  nutanix.ncp.ntnx_vm_anti_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List VM anti-affinity policies with filter
  nutanix.ncp.ntnx_vm_anti_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'my_policy'"
  register: result

- name: List all VM anti-affinity policies with limit
  nutanix.ncp.ntnx_vm_anti_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
"""


RETURN = r"""
response:
    description:
        - The response for fetching VM anti-affinity policy(s).
        - Single VM anti-affinity policy if external ID is provided.
        - List of VM anti-affinity policies if external ID is not provided.
    type: dict
    returned: always
    sample:
        {
            "categories": [
                {
                    "ext_id": "e4bda88f-e5da-5eb1-a031-2c0bb00d923d"
                },
                {
                    "ext_id": "4d552748-e119-540a-b06c-3c6f0d213fa2"
                },
                {
                    "ext_id": "0e7eee83-4313-5066-bd39-3834ac350f81"
                }
            ],
            "create_time": "2026-05-12T07:13:51.724117+00:00",
            "created_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000"
            },
            "description": "ansible_lBrqyhPVeYWw_anti_affinity_test_3_description",
            "ext_id": "c673c650-4afe-419c-59b0-441a645df9e9",
            "links": null,
            "name": "ansible_lBrqyhPVeYWw_anti_affinity_test_3",
            "num_compliant_vms": 0,
            "num_non_compliant_vms": 0,
            "num_pending_vms": 0,
            "tenant_id": null,
            "update_time": "2026-05-12T07:13:52.055646+00:00",
            "updated_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000"
            }
        }
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: always
    sample: null

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

ext_id:
    description: The external ID of the VM anti-affinity policy.
    type: str
    returned: always
    sample: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"

total_available_results:
    description: The total number of available VM anti-affinity policies in PC.
    type: int
    returned: when all VM anti-affinity policies are fetched
    sample: 10
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
from ..module_utils.v4.vmm.helpers import get_vm_anti_affinity_policy  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_policy(module, api_instance, result):
    """Fetch a single VM anti-affinity policy by ext_id."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_vm_anti_affinity_policy(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_policies(module, api_instance, result):
    """List VM anti-affinity policies with pagination support."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM anti-affinity policies info spec", **result
        )

    try:
        resp = api_instance.list_vm_anti_affinity_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM anti-affinity policies info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp_data = strip_internal_attributes(resp.to_dict()).get("data")
    if resp_data:
        result["response"] = resp_data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    api_instance = get_vm_anti_affinity_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_policy(module, api_instance, result)
    else:
        get_policies(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
