#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policies_info_v2
short_description: Fetch VM startup policies info in Nutanix Prism Central
version_added: "2.6.0"
description:
  - This module allows you to fetch VM startup policies info or a specific VM startup policy in Nutanix Prism Central.
  - If ext_id is provided, fetch a particular VM startup policy info using external ID.
  - If ext_id is not provided, fetch multiple VM startup policies info with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get VM Startup Policy by ext_id) -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager, Super Admin, Self-Service Admin (deprecated)
    - >-
      B(Get list of VM Startup Policies) -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external identifier of the VM startup policy.
    type: str
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
- name: Get VM startup policy using ext_id
  nutanix.ncp.ntnx_vm_startup_policies_info_v2:
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"
  register: result
  ignore_errors: true

- name: List all VM startup policies
  nutanix.ncp.ntnx_vm_startup_policies_info_v2:
  register: result
  ignore_errors: true

- name: List VM startup policies with filter
  nutanix.ncp.ntnx_vm_startup_policies_info_v2:
    filter: "name eq 'my_startup_policy'"
  register: result
  ignore_errors: true

- name: List VM startup policies with limit
  nutanix.ncp.ntnx_vm_startup_policies_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
    - Response for fetching VM startup policies info
    - Specific VM startup policy info if External ID is provided
    - List of multiple VM startup policies info if External ID is not provided
  returned: always
  type: dict
  sample:
    {
      "create_time": "2026-05-25T09:52:40.341137+00:00",
      "created_by": {
          "ext_id": null
      },
      "description": "Updated description for VM startup policy with all attributes",
      "ext_id": "58b9a9e4-567a-4cc1-73dc-4926331c8eb1",
      "groups": [
          {
              "categories": [
                  {
                      "ext_id": "46f433d5-016d-5b11-a75f-5d0f44da7fd5"
                  }
              ]
          },
          {
              "categories": [
                  {
                      "ext_id": "47798769-e459-5b2f-a67c-100711f94010"
                  }
              ]
          }
      ],
      "links": null,
      "name": "policy_ansible_hVQRuZXyBtrn_updated",
      "num_compliant_vms": 0,
      "num_dependency_conflicts": 0,
      "num_non_compliant_vms": 0,
      "num_pending_vms": 0,
      "num_start_condition_conflicts": 0,
      "start_conditions": [
          {
              "delay_duration_secs": 120,
              "power_state_criteria": {
                  "timeout_duration_secs": 600
              }
          }
      ],
      "tenant_id": null,
      "update_time": "2026-05-25T09:52:54.497327+00:00",
      "updated_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000"
      }
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM startup policies info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the VM startup policy
  type: str
  returned: when external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description: The total number of available VM startup policies in PC.
  type: int
  returned: when all VM startup policies are fetched
  sample: 5
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
from ..module_utils.v4.vmm.helpers import get_vm_startup_policy  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_vm_startup_policy_using_ext_id(module, policies, result):
    ext_id = module.params.get("ext_id")
    resp = get_vm_startup_policy(module, policies, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_vm_startup_policies(module, policies, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM startup policies info spec", **result
        )

    try:
        resp = policies.list_vm_startup_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM startup policies info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

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
    policies = get_vm_startup_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_vm_startup_policy_using_ext_id(module, policies, result)
    else:
        get_vm_startup_policies(module, policies, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
