#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vm_host_affinity_policies_info_v2
short_description: Fetches information about Nutanix PC VM-host affinity policies.
version_added: "2.6.0"
author:
 - Abhinav Bansal (@abhinavbansal29)
description:
  - This module fetches information about Nutanix PC VM-host affinity policies.
  - It can retrieve a single policy by ext_id or list all policies with pagination support.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Get a VM-host affinity policy) -
      Operation Name: View VM Host Affinity Policy -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List VM-host affinity policies) -
      Operation Name: View VM Host Affinity Policy -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external ID of the VM-host affinity policy.
      - If provided, fetches the specific policy.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Get a VM-host affinity policy by ID
  nutanix.ncp.ntnx_vm_host_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ policy_ext_id }}"

- name: List all VM-host affinity policies
  nutanix.ncp.ntnx_vm_host_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: List VM-host affinity policies with filter
  nutanix.ncp.ntnx_vm_host_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'my_policy'"
"""


RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VM-host affinity policies.
    - It can be a single policy or list of policies as per spec.
  type: dict
  returned: always
  sample: {
            "name": "my_affinity_policy",
            "description": "My VM host affinity policy",
            "vm_categories": [
                {"ext_id": "605a0cf9-d04e-3be7-911b-1e6f193f6ebe"}
            ],
            "host_categories": [
                {"ext_id": "98b9dc89-be08-3c56-b554-692b8b676fd1"}
            ],
            "ext_id": "54fe0ed5-02d8-4588-b10b-3b9736bf3d06",
            "links": null,
            "tenant_id": null
        }
ext_id:
    description:
        - The external ID of the policy.
    type: str
    sample: "98b9dc89-be08-3c56-b554-692b8b676fd2"
    returned: when ext_id is provided
changed:
    description: Indicates whether the resource was changed.
    type: bool
    returned: always
msg:
    description: A message describing the result of the operation.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching VM-host affinity policy info"
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
failed:
    description: Indicates whether the operation failed.
    type: bool
    returned: always
total_available_results:
    description:
        - The total number of available VM-host affinity policies in PC.
    type: int
    returned: when all policies are fetched
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
    get_vm_host_affinity_policy_api_instance,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_policy(module, result):
    """
    Fetch a single VM-host affinity policy by ext_id.
    Args:
        module: Ansible module
        result: Result dict to populate
    """
    api_instance = get_vm_host_affinity_policy_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = api_instance.get_vm_host_affinity_policy_by_id(ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM-host affinity policy info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_policies(module, result):
    """
    Fetch all VM-host affinity policies with pagination support.
    Args:
        module: Ansible module
        result: Result dict to populate
    """
    api_instance = get_vm_host_affinity_policy_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM-host affinity policies info Spec", **result
        )

    try:
        resp = api_instance.list_vm_host_affinity_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM-host affinity policies info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if resp:
        result["response"] = resp


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
    if module.params.get("ext_id"):
        get_policy(module, result)
    else:
        get_policies(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
