#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_oidc_well_known_config_info_v2
short_description: Fetch OIDC well-known configuration in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch OIDC well-known configuration in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View OIDC configuration) -
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
- name: Fetch OIDC well-known configuration
  nutanix.ncp.ntnx_oidc_well_known_config_info_v2:
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
    - The response from the Nutanix PC OIDC well-known config info v4 API.
  returned: always
  type: dict
  sample:
    {
      "authorization_endpoint": "https://10.44.76.17:9440/api/iam/v4.1.b4/authn/oidc/authorize",
      "claims_supported": [
        "sub",
        "email"
      ],
      "code_challenge_methods_supported": [
        "S256"
      ],
      "end_session_endpoint": "https://10.44.76.17:9440/api/iam/v4.1.b4/authn/logout",
      "grant_types_supported": [
        "authorization_code",
        "refresh_token"
      ],
      "id_token_signing_alg_values_supported": [
        "RS256"
      ],
      "issuer": "https://10.44.76.17:9440",
      "jwks_uri": "https://10.44.76.17:9440/api/iam/v4.1.b4/authn/oidc/keys",
      "post_logout_redirect_uri": "https://10.44.76.17:9440",
      "registration_endpoint": "https://10.44.76.17:9440/api/iam/v4.1.b4/authn/oidc/clients",
      "relative_authorization_endpoint": "/api/iam/v4.1.b4/authn/oidc/authorize",
      "relative_end_session_endpoint": "/api/iam/v4.1.b4/authn/logout",
      "response_types_supported": [
        "code"
      ],
      "scopes_supported": [
        "openid",
        "email"
      ],
      "subject_types_supported": [
        "public"
      ],
      "token_endpoint": "https://10.44.76.17:9440/api/iam/v4.1.b4/authn/oidc/token",
      "token_endpoint_auth_methods_supported": [
        "client_secret_basic"
      ],
      "userinfo_endpoint": "https://10.44.76.17:9440/api/iam/v4.1.b4/authn/oidc/userinfo"
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
  sample: "Api Exception raised while fetching OIDC well-known config"

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


def fetch_well_known_config(module, api_instance, result):
    try:
        resp = api_instance.get_oidc_wellknown_config()
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching OIDC well-known config",
        )
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
    fetch_well_known_config(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
