#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_sc_conflict_dependent_vms_info_v2
short_description: List dependent VMs of a VM startup policy start condition conflict
version_added: 2.7.0
description:
  - List dependent VMs of a Start condition conflict of a VM startup policy.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(List dependent VMs of a Start condition conflict of a VM startup policy) -
    Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager,
    Self-Service Admin (deprecated), Super Admin, Tenant Admin, Tenant Consumer,
    Virtual Machine Admin, Virtual Machine Viewer
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  vm_startup_policy_ext_id:
    description:
      - The external ID of the VM startup policy.
    type: str
    required: true
  start_condition_conflict_ext_id:
    description:
      - The external ID of the start condition conflict of a VM startup policy.
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
- name: List entities
  nutanix.ncp.ntnx_vm_startup_policy_sc_conflict_dependent_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
    start_condition_conflict_ext_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  register: result
  ignore_errors: true

- name: List entities with limit
  nutanix.ncp.ntnx_vm_startup_policy_sc_conflict_dependent_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
    start_condition_conflict_ext_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    limit: 1
  register: result
  ignore_errors: true

- name: List all entities with fetch_all
  nutanix.ncp.ntnx_vm_startup_policy_sc_conflict_dependent_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
    start_condition_conflict_ext_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description: The list of dependent VMs for the specified start condition conflict.
  type: list
  returned: always
  sample:
    [
      {
          "ext_id": "45805d6a-758f-4b32-4b6b-129058e1bf0a",
          "links": null,
          "tenant_id": null
      }
    ]

vm_startup_policy_ext_id:
  description: The external ID of the VM startup policy.
  type: str
  returned: always
  sample: "6f452990-bd1d-45ae-46d7-4622c5d323aa"

start_condition_conflict_ext_id:
  description: The external ID of the start condition conflict of a VM startup policy.
  type: str
  returned: always
  sample: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM startup policy start condition conflict dependent VMs"

error:
  description: This indicates the error message if any error occurred
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available results returned by the list API.
  type: int
  returned: when the list is fetched
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_startup_policies_api_instance,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_startup_policy_ext_id=dict(type="str", required=True),
        start_condition_conflict_ext_id=dict(type="str", required=True),
        page=dict(type="int"),
        limit=dict(type="int"),
        fetch_all=dict(type="bool", required=False, default=False),
    )
    return module_args


def list_entities_for_conflict(module, api_instance, result):
    policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    conflict_ext_id = module.params.get("start_condition_conflict_ext_id")
    result["vm_startup_policy_ext_id"] = policy_ext_id
    result["start_condition_conflict_ext_id"] = conflict_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM startup policy start condition conflict dependent VMs info spec",
            **result,
        )

    try:
        resp = list_entities(
            api_instance.list_vm_startup_policy_start_condition_conflict_dependent_vms,
            kwargs=kwargs,
            vmStartupPolicyExtId=policy_ext_id,
            startConditionConflictExtId=conflict_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM startup policy start condition conflict dependent VMs",
        )

    if getattr(resp, "metadata", None) is not None:
        total_available_results = getattr(
            resp.metadata, "total_available_results", None
        )
        if total_available_results is not None:
            result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        skip_info_args=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}

    api_instance = get_vm_startup_policies_api_instance(module)
    list_entities_for_conflict(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
