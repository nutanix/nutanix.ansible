#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_approval_policies_info_v2
short_description: Fetch Approval Policies info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ApprovalPolicy in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ApprovalPolicy.
  - If C(ext_id) is not provided, list multiple ApprovalPolicy optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Get Approval Policy by ext_id) -
      Required Roles: Prism Admin, Security Admin, Security Viewer, Super Admin
    - >-
      B(List Approval Policies) -
      Required Roles: Prism Admin, Security Admin, Security Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
  ext_id:
    description:
      - The external ID of the Approval Policy.
    type: str
    required: false
  filter:
    description:
      - OData C($filter) expression used to filter the list of Approval Policies.
    type: str
    required: false
  orderby:
    description:
      - OData C($orderby) expression used to order the list of Approval Policies.
    type: str
    required: false
  select:
    description:
      - OData C($select) expression used to select a specific set of
        properties from each Approval Policy in the response.
    type: str
    required: false
  read_timeout:
    description: Read timeout in milliseconds for API calls.
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
- name: Get an approval policy using ext_id
  nutanix.ncp.ntnx_approval_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "8f7e6d5c-4b3a-2109-fedc-ba0987654321"
  register: result

- name: List all approval policies
  nutanix.ncp.ntnx_approval_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List approval policies with a filter
  nutanix.ncp.ntnx_approval_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'ansible_approval_policy'"
  register: result

- name: List approval policies ordered by name
  nutanix.ncp.ntnx_approval_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    orderby: "name asc"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ApprovalPolicy info v4 API.
    - It can be a single ApprovalPolicy if external ID is provided.
    - List of multiple ApprovalPolicy if external ID is not provided with optional filter, orderby or select.
  returned: always
  type: dict
  sample:
    {
      "approver_groups": [
        {
          "approvers": [
            {
              "display_name": "Approver One",
              "email_id": "approver1@example.com",
              "ext_id": "0005b0f1-6c1e-4d10-9c5a-1234567890ab",
              "first_name": "Approver",
              "last_name": "One",
              "username": "approver_user_one"
            }
          ],
          "expiry_hours": 48,
          "name": "primary_approvers"
        }
      ],
      "description": "Approval policy created by Ansible",
      "ext_id": "8f7e6d5c-4b3a-2109-fedc-ba0987654321",
      "is_update_pending": false,
      "last_updated_by": "admin",
      "last_update_time": "2026-07-20T15:00:00.000Z",
      "links": null,
      "name": "ansible_approval_policy",
      "secured_policies": [],
      "tenant_id": null
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
  description: External ID of the Approval Policy
  type: str
  returned: when external ID is provided
  sample: "8f7e6d5c-4b3a-2109-fedc-ba0987654321"

total_available_results:
  description: The total number of available Approval Policies in PC.
  type: int
  returned: when all approval policies are fetched
  sample: 3
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        filter=dict(type="str"),
        orderby=dict(type="str"),
        select=dict(type="str"),
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
        skip_info_args=True,
        mutually_exclusive=[
            ("ext_id", "filter"),
            ("ext_id", "orderby"),
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
