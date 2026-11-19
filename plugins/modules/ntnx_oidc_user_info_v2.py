#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_oidc_user_info_v2
short_description: Fetch OIDC user info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch OIDC user info claims in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get identity claims of user) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
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
- name: Fetch OIDC user info
  nutanix.ncp.ntnx_oidc_user_info_v2:
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
    - The response from the Nutanix PC OIDC user info v4 API.
  returned: always
  type: dict
  sample:
    {
      "email": "admin@example.com",
      "exp": 1234567890,
      "groups": [],
      "iat": 1234567890,
      "is_email_verified": true,
      "iss": "https://10.44.76.17:9440",
      "name": "admin",
      "sub": "admin-uuid-123",
      "sub_type": "USER",
      "user_id": "00000000-0000-0000-0000-000000000000"
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
  sample: "Api Exception raised while fetching OIDC user info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when an error occurs
  type: str

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_oidc_api_instance  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    return dict()


def fetch_user_info(module, api_instance, result):
    try:
        resp = api_instance.get_user_info()
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching OIDC user info",
        )
    # Handle response which may be ApiResponse with data
    data = resp
    if hasattr(resp, "data") and resp.data is not None:
        data = resp.data
        if hasattr(data, "to_dict"):
            result["response"] = strip_internal_attributes(data.to_dict())
            return
        elif isinstance(data, dict):
            result["response"] = strip_internal_attributes(data)
            return
    if hasattr(resp, "to_dict"):
        result["response"] = strip_internal_attributes(resp.to_dict())
    elif isinstance(resp, dict):
        result["response"] = strip_internal_attributes(resp)
    else:
        result["response"] = str(resp)


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_oidc_api_instance(module)
    fetch_user_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
