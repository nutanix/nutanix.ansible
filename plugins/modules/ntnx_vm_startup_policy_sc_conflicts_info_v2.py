#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_sc_conflicts_info_v2
short_description: Fetch start condition conflicts for a VM startup policy in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module fetches start condition conflicts for a VM startup policy in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch a particular start condition conflict using its external ID.
  - If C(ext_id) is not provided, list start condition conflicts for the VM startup policy.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(List Start condition conflicts of a VM startup policy) -
    Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager,
    Self-Service Admin (deprecated), Super Admin, Tenant Admin, Tenant Consumer,
    Virtual Machine Admin, Virtual Machine Viewer
  - >-
    B(Get Start condition conflict of a VM startup policy) -
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
  ext_id:
    description:
      - The external ID of the start condition conflict.
      - When set, fetch that start condition conflict; otherwise list start condition conflicts.
    type: str
    required: false
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
- name: List start condition conflicts for a VM startup policy
  nutanix.ncp.ntnx_vm_startup_policy_sc_conflicts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
  register: result
  ignore_errors: true

- name: List start condition conflicts with limit
  nutanix.ncp.ntnx_vm_startup_policy_sc_conflicts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
    limit: 1
  register: result
  ignore_errors: true

- name: List all start condition conflicts with fetch_all
  nutanix.ncp.ntnx_vm_startup_policy_sc_conflicts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
    fetch_all: true
  register: result
  ignore_errors: true

- name: Get a start condition conflict by ext_id
  nutanix.ncp.ntnx_vm_startup_policy_sc_conflicts_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_startup_policy_ext_id: "6f452990-bd1d-45ae-46d7-4622c5d323aa"
    ext_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for fetching VM startup policy start condition conflicts info
    - Specific start condition conflict info if External ID is provided
    - List of multiple start condition conflicts info if External ID is not provided
  type: dict
  returned: always
  sample:
    {
        "ext_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "dependent_category": {"ext_id": "e4bda88f-e5da-5eb1-a031-2c0bb00d923d"},
        "dependee_category": {"ext_id": "46f433d5-016d-5b11-a75f-5d0f44da7fd5"},
        "start_condition": null,
        "conflicting_policy": null,
        "links": null,
        "tenant_id": null
    }

vm_startup_policy_ext_id:
  description: The external ID of the VM startup policy.
  type: str
  returned: always
  sample: "6f452990-bd1d-45ae-46d7-4622c5d323aa"

ext_id:
  description: The external ID of the start condition conflict.
  type: str
  returned: when C(ext_id) is provided
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
  sample: "Api Exception raised while fetching VM startup policy start condition conflicts"

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
  description:
    - The total number of available start condition conflicts for the specified VM startup policy.
  type: int
  returned: when C(ext_id) is not provided
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
from ..module_utils.v4.vmm.helpers import (  # noqa: E402
    get_vm_startup_policy_start_condition_conflict,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_startup_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
        page=dict(type="int"),
        limit=dict(type="int"),
        fetch_all=dict(type="bool", required=False, default=False),
    )
    return module_args


def get_conflict_using_ext_id(module, api_instance, result):
    policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    ext_id = module.params.get("ext_id")
    result["vm_startup_policy_ext_id"] = policy_ext_id
    result["ext_id"] = ext_id

    resp = get_vm_startup_policy_start_condition_conflict(
        module, api_instance, policy_ext_id, ext_id
    )
    if resp is None:
        module.fail_json(
            msg="Failed fetching VM startup policy start condition conflict", **result
        )
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_conflicts(module, api_instance, result):
    policy_ext_id = module.params.get("vm_startup_policy_ext_id")
    result["vm_startup_policy_ext_id"] = policy_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM startup policy start condition conflicts info spec",
            **result,
        )

    try:
        resp = list_entities(
            api_instance.list_vm_startup_policy_start_condition_conflicts,
            kwargs=kwargs,
            vmStartupPolicyExtId=policy_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM startup policy start condition conflicts",
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
    if module.params.get("ext_id"):
        get_conflict_using_ext_id(module, api_instance, result)
    else:
        list_conflicts(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
