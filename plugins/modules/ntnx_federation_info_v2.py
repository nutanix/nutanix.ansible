#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_federation_info_v2
short_description: Fetch federation info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch federation info in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
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
- name: Get federation info
  nutanix.ncp.ntnx_federation_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix federation info v4 API.
    - It contains the federation details.
  returned: always
  type: dict
  sample:
    {
      "cloud_api_key": null,
      "cloud_tenant": null,
      "claim_map": {
        "email": "email",
        "name": "name"
      },
      "created_by": "admin",
      "created_time": "2026-07-21T06:36:56.065999+00:00",
      "ext_id": "00000000-0000-0000-0000-000000000001",
      "idp_id": "00000000-0000-0000-0000-000000000000",
      "last_updated_time": "2026-07-21T06:36:56.065999+00:00",
      "tenant_id": null,
      "well_known_config": "https://example.okta.com/.well-known/openid-configuration"
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
  sample: "Api Exception raised while fetching federation info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_federations_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_federation  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict()

    return module_args


def get_federation_info(module, api_instance, result):
    resp = get_federation(module, api_instance)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_federations_api_instance(module)
    get_federation_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
