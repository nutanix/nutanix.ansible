#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_approval_policies_info_v2
short_description: Fetch approval policy information
version_added: "2.7.0"
description:
    - This module allows you to fetch information about approval policies in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific approval policy.
    - If C(ext_id) is not provided, list multiple approval policies optionally filtered.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(View Approval Policy) -
      Required Roles: Prism Admin, Prism Viewer, Secure Policy Admin, Secure Policy Editor,
      Secure Policy Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
    ext_id:
        description:
            - External ID of the approval policy.
        type: str
        required: false
    filter:
        description:
            - The filter in OData syntax used for the results.
            - The filter can be applied to the following fields C(name).
        type: str
        required: false
    orderby:
        description:
            - The sort order in which results are returned.
        type: str
        required: false
    select:
        description:
            - The attribute name to select.
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
- name: Fetch approval policy by External ID
  nutanix.ncp.ntnx_approval_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "f19af988-ea11-46ca-8958-e8158d87383b"
  register: result

- name: List approval policies
  nutanix.ncp.ntnx_approval_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List approval policies with filter
  nutanix.ncp.ntnx_approval_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'Platinum Approval Policy'"
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC approval policies info v4 API.
        - It can be a single approval policy if External ID is provided.
        - List of multiple approval policies if External ID is not provided with optional filter.
    type: dict
    returned: always
    sample:
        {
            "approver_groups": [
                {
                    "approvers": [
                        {
                            "display_name": "john jane doe",
                            "email_id": "john.doe@example.com",
                            "username": "john_doe",
                            "user_type": "LOCAL"
                        }
                    ],
                    "expiry_hours": 44,
                    "name": "Platinum Approvers"
                }
            ],
            "description": "This policy is for platinum snapshots",
            "ext_id": "f19af988-ea11-46ca-8958-e8158d87383b",
            "is_update_pending": false,
            "last_update_time": null,
            "last_updated_by": null,
            "links": null,
            "name": "Platinum Approval Policy",
            "secured_policies": null,
            "tenant_id": null
        }
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: false
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
ext_id:
    description: The external ID of the approval policy.
    type: str
    returned: when External ID is provided
    sample: "f19af988-ea11-46ca-8958-e8158d87383b"
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Failed generating approval policies info Spec"
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
total_available_results:
    description:
        - The total number of available approval policies in PC.
    type: int
    returned: when all approval policies are fetched
    sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_approval_policies_api_instance,
)
from ..module_utils.v4.security.helpers import (  # noqa: E402
    get_approval_policy_by_ext_id,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

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
    resp = get_approval_policy_by_ext_id(
        module, api_instance, ext_id, select=module.params.get("select")
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_approval_policies(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating approval policies info Spec", **result)

    try:
        resp = list_entities(
            api_instance.list_approval_policies,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching approval policies info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    metadata = resp.get("metadata") or {}
    result["total_available_results"] = metadata.get("total_available_results")
    resp = resp.get("data")

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
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
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
