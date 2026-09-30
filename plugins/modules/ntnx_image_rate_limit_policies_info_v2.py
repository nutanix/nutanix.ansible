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
description:
  - This module fetches information about Nutanix PC image rate limit policies.
  - This module can be used to get a single image rate limit policy by its external ID or list all image rate limit policies with optional filter.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Get an image rate limit policy) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List image rate limit policies) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external ID of the image rate limit policy.
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
- name: Get image rate limit policy by external ID
  nutanix.ncp.ntnx_image_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"

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
    filter: "name eq 'my_rate_limit_policy'"
"""

RETURN = r"""
response:
  description:
    - Response for fetching image rate limit policies info
    - Specific image rate limit policy info if External ID is provided
    - List of multiple image rate limit policies info if External ID is not provided
  returned: always
  type: dict
  sample:
    {
      "cluster_entity_filter": {
          "category_ext_ids": [
              "e4bda88f-e5da-5eb1-a031-2c0bb00d923d"
          ],
          "type": "CATEGORIES_MATCH_ALL"
      },
      "create_time": "2026-05-24T11:11:24.765102+00:00",
      "description": "ansible_rate_limit_policy_LBZXZWtFgMFT_updated_description",
      "ext_id": "7a2b62cb-c706-4bc8-ac8b-cc3dd170996f",
      "last_update_time": "2026-05-24T11:11:42.509214+00:00",
      "links": null,
      "matching_cluster_ext_ids": null,
      "name": "ansible_rate_limit_policy_LBZXZWtFgMFT_updated",
      "owner_ext_id": "00000000-0000-0000-0000-000000000000",
      "owner_name": "admin",
      "rate_limit_kbps": 4096,
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
  sample: "Api Exception raised while fetching image rate limit policies info"

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
  description: External ID of the image rate limit policy
  type: str
  returned: when external ID is provided
  sample: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"

total_available_results:
  description: The total number of available image rate limit policies in PC.
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
from ..module_utils.v4.vmm.helpers import get_rate_limit_policy  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_rate_limit_policy(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_policies(module, api_instance, result):
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
    result = {"changed": False, "failed": False, "response": None}

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
