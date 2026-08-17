#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_recommendations_info_v2
short_description: Fetch LCM recommendation info from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Recommendation in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Recommendation.
  - The v4 LCM SDK only exposes a get-by-ID endpoint for recommendations, so
    C(ext_id) is required for this module. The C(ext_id) is the one returned
    by M(nutanix.ncp.ntnx_recommendation_v2) after a successful compute
    operation.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get LCM recommendation details by external ID.) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer,
    Security Dashboard Admin, Security Dashboard Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  ext_id:
    description:
      - The external ID of the LCM recommendation resource returned by
        M(nutanix.ncp.ntnx_recommendation_v2).
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
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch an LCM recommendation using its external ID
  nutanix.ncp.ntnx_lcm_recommendations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: recommendation_info
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Recommendation info v4 API.
    - It will be a single Recommendation resource identified by C(ext_id).
    - The v4 LCM SDK does not expose a list endpoint, so this module always
      returns a single Recommendation (get-by-ID).
  returned: always
  type: dict
  sample:
    {
      "addable_entities": null,
      "cluster_ext_id": "1e9a1996-50e2-485f-a67c-22355cb43055",
      "deployable_versions": [],
      "entity_update_specs": [
        {
          "entity_uuid": "3c196eac-e1d5-4c8a-9b01-c133f6907ca2",
          "to_version": "4.0.0"
        }
      ],
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "links": null,
      "modifiable_entities": null,
      "skipped_entities": null,
      "tenant_id": null
    }

ext_id:
  description: The external ID of the LCM recommendation resource.
  returned: when single entity
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes. Always
    C(false) for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Status/error message emitted by the module.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching LCM recommendation info"

error:
  description: Details about the error that occurred, if any.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the module failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_recommendations_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_lcm_recommendation  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
    )

    return module_args


def get_recommendation_using_ext_id(module, api_instance, result):
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
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "failed": False,
    }

    api_instance = get_recommendations_api_instance(module)
    get_recommendation_using_ext_id(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
