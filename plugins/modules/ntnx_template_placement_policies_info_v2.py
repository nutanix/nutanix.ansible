#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_template_placement_policies_info_v2
short_description: Fetches information about Nutanix PC template placement policies.
version_added: "2.6.0"
description:
  - This module fetches information about Nutanix PC template placement policies.
  - It can fetch a single template placement policy by ext_id or list multiple template placement policies with optional filter.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Get a template placement policy) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List template placement policies) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external ID of the template placement policy.
      - Mutually exclusive with C(filter).
    type: str
    required: false
author:
 - Abhinav Bansal (@abhinavbansal29)
 - George Ghawali (@george-ghawali)
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Get template placement policy by ID
  nutanix.ncp.ntnx_template_placement_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "c4696582-29c0-4a23-454d-5c1128aeaffb"

- name: List all template placement policies
  nutanix.ncp.ntnx_template_placement_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: List all template placement policies with filter
  nutanix.ncp.ntnx_template_placement_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: name eq 'my_template_policy'

- name: List all template placement policies with limit
  nutanix.ncp.ntnx_template_placement_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC vms v4 API.
    - Single template placement policy if external ID is provided.
    - List of multiple template placement policies if external ID is not provided.
  type: dict
  returned: always
  sample: {
            "cluster_filter": {
                "category_ext_ids": [
                    "605a0cf9-d04e-3be7-911b-1e6f193f6ebe"
                ],
                "type": "CATEGORIES_MATCH_ANY"
            },
            "content_filter": {
                "category_ext_ids": [
                    "98b9dc89-be08-3c56-b554-692b8b676fd1"
                ],
                "type": "CATEGORIES_MATCH_ALL"
            },
            "create_time": "2024-03-25T23:03:17.610346+00:00",
            "description": "policy-description",
            "ext_id": "54fe0ed5-02d8-4588-b10b-3b9736bf3d06",
            "name": "policy-name",
            "placement_type": "SOFT",
            "tenant_id": null
        }
changed:
  description: This indicates whether the task resulted in any changes
  type: bool
  returned: always
  sample: false
ext_id:
    description:
        - The external ID of the template placement policy.
    type: str
    sample: "98b9dc89-be08-3c56-b554-692b8b676fd2"
    returned: always
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching template placement policies info"
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
failed:
    description: Indicates whether the operation failed.
    type: bool
    returned: on failure
total_available_results:
    description:
        - The total number of available template placement policies in PC.
    type: int
    returned: when all template placement policies are fetched
    sample: 125
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
    get_template_placement_policy_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_template_placement_policy  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_policy(module, policies, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_template_placement_policy(module, policies, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_policies(module, policies, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating template placement policies info Spec", **result
        )

    try:
        resp = policies.list_template_placement_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching template placement policies info",
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
    result = {"changed": False, "response": None}
    policies = get_template_placement_policy_api_instance(module)
    if module.params.get("ext_id"):
        get_policy(module, policies, result)
    else:
        get_policies(module, policies, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
