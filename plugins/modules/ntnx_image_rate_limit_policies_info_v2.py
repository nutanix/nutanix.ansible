#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_image_rate_limit_policies_info_v2
short_description: Fetches information about Nutanix PC image rate limit policies.
version_added: "2.6.0"
author:
 - Abhinav Bansal (@abhinavbansal29)
description:
  - This module fetches information about Nutanix PC image rate limit policies.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Get an image rate limit policy) -
      Operation Name: View Image Rate Limit Policy -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(List image rate limit policies) -
      Operation Name: View Image Rate Limit Policy -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external ID of the image rate limit policy.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Get image rate limit policy by ID
  nutanix.ncp.ntnx_image_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "policy-12345"

- name: Get all image rate limit policies
  nutanix.ncp.ntnx_image_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: Get image rate limit policies with filter
  nutanix.ncp.ntnx_image_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'my_policy'"
"""


RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Image Rate Limit policies.
    - it can be single policy or list of policies as per spec.
  type: dict
  returned: always
  sample: {
            "cluster_entity_filter": {
                "category_ext_ids": [
                    "605a0cf9-d04e-3be7-911b-1e6f193f6ebe"
                ],
                "type": "CATEGORIES_MATCH_ALL"
            },
            "create_time": "2026-01-25T23:03:17.610346+00:00",
            "description": "Rate limit policy for images",
            "ext_id": "54fe0ed5-02d8-4588-b10b-3b9736bf3d06",
            "last_update_time": "2026-01-25T23:44:01.955468+00:00",
            "name": "my_rate_limit_policy",
            "rate_limit_kbps": 1024,
            "owner_ext_id": "00000000-0000-0000-0000-000000000000",
            "tenant_id": null
        }
ext_id:
    description:
        - The external ID of the policy.
    type: str
    sample: "98b9dc89-be08-3c56-b554-692b8b676fd2"
    returned: always
changed:
    description: Indicates whether the resource was changed.
    type: bool
    returned: always
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching image rate limit policy info"
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
        - The total number of available image rate limit policies in PC.
    type: int
    returned: when all image rate limit policies are fetched
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
    get_image_rate_limit_policy_api_instance,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_policy(module, api_instance, result):
    """
    Get a single image rate limit policy by ext_id.
    Args:
        module: Ansible module instance
        api_instance: ImageRateLimitPoliciesApi instance
        result: Result dict to populate
    """
    ext_id = module.params.get("ext_id")

    try:
        resp = api_instance.get_rate_limit_policy_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching image rate limit policy info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_policies(module, api_instance, result):
    """
    List all image rate limit policies with pagination support.
    Args:
        module: Ansible module instance
        api_instance: ImageRateLimitPoliciesApi instance
        result: Result dict to populate
    """
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating image rate limit policies info Spec", **result
        )

    try:
        resp = api_instance.list_rate_limit_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching image rate limit policies info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp_data = strip_internal_attributes(resp.to_dict()).get("data")
    if resp_data:
        result["response"] = resp_data
    else:
        result["response"] = []


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

    api_instance = get_image_rate_limit_policy_api_instance(module)

    if module.params.get("ext_id"):
        get_policy(module, api_instance, result)
    else:
        get_policies(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
