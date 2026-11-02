#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_compute_recommendations_info_v2
short_description: Get LCM compute recommendation info in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Get details of an LCM compute recommendation by external ID.
    - This module uses PC v4 APIs based SDKs
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get a specific LCM recommendation by external ID.) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    ext_id:
        description:
            - External identifier of the LCM update recommendation resource.
        type: str
        required: true
    read_timeout:
        description: Read timeout in milliseconds for API calls.
        type: int
        required: false
        default: 30000
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Fetch LCM compute recommendation using external ID
  nutanix.ncp.ntnx_compute_recommendations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "8d3d0c2f-1c8b-4bf1-8a5b-4a2f96b6f97e"
  register: lcm_recommendation
"""

RETURN = r"""
response:
    description:
        - The LCM compute recommendation details.
    type: dict
    returned: always
    sample:
        {
            "addable_entities": [],
            "cluster_ext_id": "1e9a1996-50e2-485f-a67c-22355cb43055",
            "deployable_versions": [],
            "entity_update_specs": [
                {
                    "entity_uuid": "3c196eac-e1d5-4c8a-9b01-c133f6907ca2",
                    "to_version": "4.0.0"
                }
            ],
            "ext_id": "8d3d0c2f-1c8b-4bf1-8a5b-4a2f96b6f97e",
            "modifiable_entities": [],
            "skipped_entities": []
        }
ext_id:
    description: The external ID of the recommendation resource.
    type: str
    returned: always
    sample: "8d3d0c2f-1c8b-4bf1-8a5b-4a2f96b6f97e"
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
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error
    sample: "Api Exception raised while fetching LCM recommendation using external identifier"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_recommendations_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_lcm_recommendation  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_recommendation_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_lcm_recommendation(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_recommendations_api_instance(module)
    get_recommendation_by_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
