#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_legacy_vm_anti_affinity_policies_info_v2
short_description: Fetch legacy VM-VM anti-affinity policies info from Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about LegacyVmAntiAffinityPolicy in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific LegacyVmAntiAffinityPolicy.
  - If C(ext_id) is not provided, list multiple LegacyVmAntiAffinityPolicy optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get / List Legacy VM-VM Anti-Affinity Policies) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, Cluster Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=virtual_machine_management)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the legacy VM-VM anti-affinity policy.
      - When provided, a single policy is fetched. When omitted, the module lists all legacy policies.
    type: str
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
- name: Fetch a legacy VM-VM anti-affinity policy using ext_id
  nutanix.ncp.ntnx_legacy_vm_anti_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "3f6a1c5c-4b7f-4a5f-8e2e-6a1e5b9c2d3f"
  register: result
  ignore_errors: true

- name: List all legacy VM-VM anti-affinity policies
  nutanix.ncp.ntnx_legacy_vm_anti_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List legacy VM-VM anti-affinity policies with an OData filter
  nutanix.ncp.ntnx_legacy_vm_anti_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'legacy_aaf_policy'"
  register: result
  ignore_errors: true

- name: List legacy VM-VM anti-affinity policies with a limit
  nutanix.ncp.ntnx_legacy_vm_anti_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC LegacyVmAntiAffinityPolicy info v4 API.
    - It can be a single LegacyVmAntiAffinityPolicy if external ID is provided.
    - List of multiple LegacyVmAntiAffinityPolicy if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster": {
          "ext_id": "000647b8-ddb3-6bbb-0000-000000028f57"
      },
      "ext_id": "3f6a1c5c-4b7f-4a5f-8e2e-6a1e5b9c2d3f",
      "links": null,
      "name": "legacy_aaf_policy",
      "tenant_id": null,
      "vms": [
          {
              "ext_id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0"
          },
          {
              "ext_id": "b2c3d4e5-f6a7-8901-2345-6789abcdef01"
          }
      ]
    }

changed:
  description: Whether the operation resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Contextual status or error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching legacy VM-VM anti-affinity policies info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: When an error occurs

failed:
  description: Whether the module invocation failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the legacy VM-VM anti-affinity policy that was fetched.
  type: str
  returned: When an external ID is provided
  sample: "3f6a1c5c-4b7f-4a5f-8e2e-6a1e5b9c2d3f"

total_available_results:
  description: The total number of legacy VM-VM anti-affinity policies available on the Prism Central.
  type: int
  returned: When all legacy VM-VM anti-affinity policies are listed
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
from ..module_utils.v4.vmm.helpers import (  # noqa: E402
    get_legacy_vm_anti_affinity_policy,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_legacy_vm_anti_affinity_policy_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_legacy_vm_anti_affinity_policy(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_legacy_vm_anti_affinity_policies(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating legacy VM-VM anti-affinity policies info spec",
            **result,
        )

    try:
        resp = api_instance.list_legacy_vm_anti_affinity_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching legacy VM-VM anti-affinity policies info",
        )

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
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vm_anti_affinity_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_legacy_vm_anti_affinity_policy_using_ext_id(module, api_instance, result)
    else:
        get_legacy_vm_anti_affinity_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
