#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_login_requests_info_v2
short_description: Fetch login request info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch login request info in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific login request.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get login request) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
  ext_id:
    description:
      - The external ID of the login request.
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
- name: Get login request using ext_id
  nutanix.ncp.ntnx_login_requests_info_v2:
    ext_id: "22222222-2222-2222-2222-222222222222"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix login requests info v4 API
    - It can be a single login request if external ID is provided.
  returned: always
  type: dict
  sample:
    {
      "approval_prompt": null,
      "audience": null,
      "client_id": "9a53c903-ba26-588b-ac0f-f8ab26f5a6b0",
      "ext_id": "fc8b3c56-e66c-5e7c-9988-2e45bfe85569",
      "is_service_provider_enabled": false,
      "is_user_logged_in": false,
      "links": null,
      "login_provider_id": "37f30135-455b-5ebd-995f-b47e817a59f2",
      "nonce": null,
      "redirect_uri": "https://10.44.76.17:9440",
      "response_type": "CODE",
      "scope": [
        "OPENID"
      ],
      "state": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching login request info"

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
  description: External ID of the login request
  type: str
  returned: when external ID is provided
  sample: "22222222-2222-2222-2222-222222222222"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_login_requests_api_instance,
)
from ..module_utils.v4.iam.helpers import get_login_request  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
    )

    return module_args


def get_login_request_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_login_request(module, api_instance, ext_id)
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
    api_instance = get_login_requests_api_instance(module)
    get_login_request_using_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
