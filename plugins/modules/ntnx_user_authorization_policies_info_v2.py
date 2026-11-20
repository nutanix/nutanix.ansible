#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_authorization_policies_info_v2
short_description: Fetch user authorization policies info
version_added: "2.7.0"
description:
    - This module allows you to fetch information about user authorization
      policies in Nutanix Prism Central.
    - List authorization policies associated with the identity making the API
      call.
    - This module uses PC v4 APIs based SDKs
notes:
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    page:
        description:
            - A URL query parameter that specifies the page number of the
              result set.
            - It must be a positive integer between 0 and the maximum number
              of pages that are available for that resource.
            - Any number out of this range might lead to no results.
        type: int
        required: false
    limit:
        description:
            - A URL query parameter that specifies the total number of records
              returned in the result set.
            - Must be a positive integer between 1 and 100.
            - Any number out of this range will lead to a validation error.
            - If the limit is not provided, a default value of 50 records will
              be returned in the result set.
        type: int
        required: false
    read_timeout:
        description: Read timeout in milliseconds for API calls.
        type: int
        required: false
        default: 30000
    fetch_all:
        description:
            - When C(true), paginate through the list API until all available
              entities are returned.
            - C(page) and C(limit) are ignored; each request uses the maximum
              page size (100).
            - Does not apply when fetching a single entity by C(ext_id).
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
- name: List all user authorization policies
  nutanix.ncp.ntnx_user_authorization_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List user authorization policies with limit
  nutanix.ncp.ntnx_user_authorization_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: List all user authorization policies with fetch_all
  nutanix.ncp.ntnx_user_authorization_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix user authorization policies info v4
          API.
        - List of user authorization policies associated with the current
          identity.
    returned: always
    type: dict
    sample:
        {
            "authoring_scope": null,
            "client_name": "Prism",
            "description": null,
            "display_name": "Super Admin_acp",
            "domain_ext_ids": null,
            "entities": [
                {
                    "entity_filter": {
                        "*": {
                            "*": {
                                "eq": "*"
                            }
                        }
                    }
                }
            ],
            "ext_id": "2df41ccd-458b-435e-b725-edff9c77ade6",
            "is_global": null,
            "links": null,
            "role": "06f726dc-c243-423f-a8bc-d5a662589765",
            "tenant_id": null
        }
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false
error:
    description: This indicates the error message if any error occurred
    returned: when an error occurs
    type: str
failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching user authorization policies info"
total_available_results:
    description: The total number of available user authorization policies.
    returned: when listing user authorization policies
    type: int
    sample: 7
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_capabilities_api_instance  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        page=dict(type="int"),
        limit=dict(type="int"),
        fetch_all=dict(type="bool", required=False, default=False),
    )
    return module_args


def get_user_authorization_policies(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating user authorization policies info spec", **result
        )

    try:
        resp = list_entities(
            api_instance.list_user_authorization_policies,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching user authorization policies info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    data = resp.get("data") or []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_capabilities_api_instance(module)
    get_user_authorization_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
