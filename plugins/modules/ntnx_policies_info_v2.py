#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_policies_info_v2
short_description: Fetch approval policies info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Policy in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Policy.
  - If C(ext_id) is not provided, list multiple Policy optionally filtered.
  - Note - the underlying v4 list approval policies API supports only
    C(filter), C(orderby) and C(select); C(page) and C(limit) options are
    accepted for interface parity but are silently ignored.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get approval policy by ext_id) -
      Required Roles: Super Admin, Prism Admin, Secure Policy Viewer
    - >-
      B(List approval policies) -
      Required Roles: Super Admin, Prism Admin, Secure Policy Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
  ext_id:
    description:
      - External ID of the approval policy.
      - When provided, only that specific approval policy is returned.
    type: str
    required: false
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
- name: Get approval policy details using ext_id
  nutanix.ncp.ntnx_policies_info_v2:
    ext_id: "22222222-2222-2222-2222-222222222222"
  register: single_policy

- name: List all approval policies
  nutanix.ncp.ntnx_policies_info_v2:
  register: all_policies

- name: List approval policies with an OData filter
  nutanix.ncp.ntnx_policies_info_v2:
    filter: "name eq 'ansible-approval-policy'"
  register: filtered_policies

- name: List approval policies with a specific ordering
  nutanix.ncp.ntnx_policies_info_v2:
    orderby: "name asc"
  register: ordered_policies

- name: List approval policies selecting a subset of fields
  nutanix.ncp.ntnx_policies_info_v2:
    select: "extId,name,description"
  register: selected_policies
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Policy info v4 API.
    - It can be a single Policy if external ID is provided.
    - List of multiple Policy if external ID is not provided.
  returned: always
  type: dict
  sample:
    {
      "approver_groups": [
        {
          "approvers": [
            {
              "ext_id": "00000000-0000-0000-0000-000000000000",
              "username": "admin",
              "user_type": "LOCAL"
            }
          ],
          "expiry_hours": 24,
          "name": "admin-approvers"
        }
      ],
      "description": "Approval policy created by Ansible",
      "ext_id": "22222222-2222-2222-2222-222222222222",
      "is_update_pending": false,
      "last_update_time": "2026-07-20T12:00:00.000Z",
      "last_updated_by": "00000000-0000-0000-0000-000000000000",
      "links": null,
      "name": "ansible-approval-policy",
      "secured_policies": [
        {
          "policy_ext_id": "11111111-1111-1111-1111-111111111111",
          "policy_type": "PROTECTION_POLICY"
        }
      ],
      "tenant_id": null
    }

total_available_results:
  description: The total number of available approval policies in PC.
  type: int
  returned: when all approval policies are fetched
  sample: 3

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching approval policies info"

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
  description: External ID of the approval policy.
  type: str
  returned: when external ID is provided
  sample: "22222222-2222-2222-2222-222222222222"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_approval_policies_api_instance,
)
from ..module_utils.v4.security.helpers import get_approval_policy  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_approval_policy_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_approval_policy(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_approval_policies(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating approval policies info spec", **result)

    # The SDK's list_approval_policies method only supports _filter, _orderby
    # and _select. Silently drop _page/_limit generated by the base info spec.
    for unsupported in ("_page", "_limit"):
        kwargs.pop(unsupported, None)

    try:
        resp = api_instance.list_approval_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching approval policies info",
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
    api_instance = get_approval_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_approval_policy_using_ext_id(module, api_instance, result)
    else:
        get_approval_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
