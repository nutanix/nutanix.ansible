#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_oidc_client_info_v2
short_description: Fetch OIDC client info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about OIDC client in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific OIDC client.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get OIDC client by ext_id) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  ext_id:
    description:
      - The external ID of the OIDC client.
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
- name: Get OIDC client using ext_id
  nutanix.ncp.ntnx_oidc_client_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00000000-0000-0000-0000-000000000000"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC OIDC client info v4 API.
    - It can be a single OIDC client if External ID is provided.
  returned: always
  type: dict
  sample:
    {
      "application_type": "web",
      "client_id": "oidc-client-uuid-1234",
      "client_name": "test-oidc-client",
      "client_secret": "secret-value-xyz",
      "created_time": "2026-07-01T06:00:00.000000+00:00",
      "last_updated_time": "2026-07-01T06:00:00.000000+00:00",
      "redirect_uris": [
        "https://example.com/callback"
      ],
      "sha256_thumbprint_list": [
        "abc123thumbprint"
      ]
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
  sample: "Api Exception raised while fetching OIDC client info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when an error occurs
  type: str

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the OIDC client
  type: str
  returned: when external ID is provided
  sample: "00000000-0000-0000-0000-000000000000"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_oidc_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_oidc_client  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_oidc_client_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_oidc_client(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    if hasattr(resp, "to_dict"):
        result["response"] = strip_internal_attributes(resp.to_dict())
    elif isinstance(resp, dict):
        result["response"] = strip_internal_attributes(resp)
    else:
        result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_oidc_api_instance(module)
    get_oidc_client_using_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
