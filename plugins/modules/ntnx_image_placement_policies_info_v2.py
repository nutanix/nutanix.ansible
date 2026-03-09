#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_image_placement_policies_info_v2
short_description: Fetches information about Nutanix PC image placement policies.
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
description:
  - This module fetches information about Nutanix PC image placement policies.
  - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external ID of the image placement policy.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Get image placement policy by ID
  nutanix.ncp.ntnx_image_placement_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "policy-12345"

- name: Get all image placement policies
  nutanix.ncp.ntnx_image_placement_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
"""


RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Image Placement policies.
    - it can be single policy or list of policies as per spec.
  type: dict
  returned: always
  sample: {
            "cluster_entity_filter": {
                "category_ext_ids": [
                    "605a0cf9-d04e-3be7-911b-1e6f193f6ebe"
                ],
                "type": "CATEGORIES_MATCH_ANY"
            },
            "create_time": "2024-03-25T23:03:17.610346+00:00",
            "description": "new1-description-updated",
            "enforcement_state": "SUSPENDED",
            "ext_id": "54fe0ed5-02d8-4588-b10b-3b9736bf3d06",
            "image_entity_filter": {
                "category_ext_ids": [
                    "98b9dc89-be08-3c56-b554-692b8b676fd1"
                ],
                "type": "CATEGORIES_MATCH_ALL"
            },
            "last_update_time": "2024-03-25T23:44:01.955468+00:00",
            "links": null,
            "name": "new1-updated",
            "owner_ext_id": "00000000-0000-0000-0000-000000000000",
            "placement_type": "SOFT",
            "tenant_id": null
        }
ext_id:
    description:
        - The external ID of the policy.
    type: str
    sample: "98b9dc89-be08-3c56-b554-692b8b676fd2"
    returned: always
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching image placement policy info"
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
total_available_results:
    description:
        - The total number of available image placement policies in PC.
    type: int
    returned: when all image placement policies are fetched
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
    get_image_placement_policy_api_instance,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_policy(module, result):
    policies = get_image_placement_policy_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = policies.get_placement_policy_by_id(ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching image placement policy info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_policies(module, result):
    policies = get_image_placement_policy_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating image placement policies info Spec", **result
        )

    try:
        resp = policies.list_placement_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching image placement policies info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


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
    if module.params.get("ext_id"):
        get_policy(module, result)
    else:
        get_policies(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
