#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_oidc_token_v2
short_description: Create OIDC token in Nutanix Prism Central
version_added: 2.7.0
description:
  - Create OIDC token in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Create OIDC token) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  grant_type:
    description:
      - Type of grant for OIDC token.
    type: str
    required: true
    choices:
      - AUTHORIZATION_CODE
      - REFRESH_TOKEN
      - CLIENT_CREDENTIALS
      - PASSWORD
      - URN_IETF_PARAMS_OAUTH_GRANT_TYPE_TOKEN_EXCHANGE
      - _UNKNOWN
      - _REDACTED
  client_id:
    description:
      - Client identifier for OIDC token request.
    type: str
    required: true
  code:
    description:
      - Authorization code for token exchange.
    type: str
    required: false
  code_verifier:
    description:
      - Code verifier for PKCE flow.
    type: str
    required: false
  connector_id:
    description:
      - Connector identifier for authentication.
    type: str
    required: false
  scope:
    description:
      - Scope for the token request.
    type: str
    required: false
  refresh_token:
    description:
      - Refresh token for obtaining new access token.
    type: str
    required: false
  client_assertion_type:
    description:
      - Client assertion type.
    type: str
    required: false
  client_assertion:
    description:
      - Client assertion value.
    type: str
    required: false
  redirect_uri:
    description:
      - Redirect URI for the token request.
    type: str
    required: false
  audience:
    description:
      - Audience for the token.
    type: str
    required: false
  subject_token:
    description:
      - Subject token for token exchange.
    type: str
    required: false
  subject_token_type:
    description:
      - Subject token type for token exchange.
    type: str
    required: false
  non_tenant_issuer:
    description:
      - Non-tenant issuer flag.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create OIDC token with client credentials
  nutanix.ncp.ntnx_oidc_token_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    grant_type: "CLIENT_CREDENTIALS"
    client_id: "oidc-client-uuid-1234"
    scope: "openid"
  register: result
  ignore_errors: true

- name: Create OIDC token with authorization code
  nutanix.ncp.ntnx_oidc_token_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    grant_type: "AUTHORIZATION_CODE"
    client_id: "oidc-client-uuid-1234"
    code: "auth-code-xyz"
    redirect_uri: "https://example.com/callback"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating OIDC token.
  returned: always
  type: dict
  sample:
    {
      "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.sample",
      "expires_in": 3600,
      "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.sample-id",
      "refresh_token": "refresh-token-sample",
      "token_type": "Bearer"
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while creating OIDC token"

ext_id:
  description: The external ID of the OIDC token response if available
  returned: always
  type: str
  sample: "oidc-client-uuid-1234"

task_ext_id:
  description: The external ID of the task if available
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import get_oidc_api_instance  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        grant_type=dict(
            type="str",
            required=True,
            choices=[
                "AUTHORIZATION_CODE",
                "REFRESH_TOKEN",
                "CLIENT_CREDENTIALS",
                "PASSWORD",
                "URN_IETF_PARAMS_OAUTH_GRANT_TYPE_TOKEN_EXCHANGE",
                "_UNKNOWN",
                "_REDACTED",
            ],
        ),
        client_id=dict(type="str", required=True),
        code=dict(type="str"),
        code_verifier=dict(type="str"),
        connector_id=dict(type="str"),
        scope=dict(type="str"),
        refresh_token=dict(type="str", no_log=True),
        client_assertion_type=dict(type="str"),
        client_assertion=dict(type="str", no_log=True),
        redirect_uri=dict(type="str"),
        audience=dict(type="str"),
        subject_token=dict(type="str", no_log=True),
        subject_token_type=dict(type="str"),
        non_tenant_issuer=dict(type="str"),
    )
    return module_args


def run_action(module, result, api_instance):
    grant_type = module.params.get("grant_type")
    client_id = module.params.get("client_id")

    if module.check_mode:
        result["response"] = {
            "grant_type": grant_type,
            "client_id": client_id,
        }
        result["changed"] = True
        return

    # Build kwargs for API call
    kwargs = {}
    for param in [
        "code",
        "code_verifier",
        "connector_id",
        "scope",
        "refresh_token",
        "client_assertion_type",
        "client_assertion",
        "redirect_uri",
        "audience",
        "subject_token",
        "subject_token_type",
        "non_tenant_issuer",
    ]:
        val = module.params.get(param)
        if val is not None:
            kwargs[param] = val

    resp = None
    try:
        resp = api_instance.create_token(
            grant_type=grant_type, client_id=client_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating OIDC token",
        )

    if resp is not None:
        if hasattr(resp, "to_dict"):
            result["response"] = strip_internal_attributes(resp.to_dict())
        elif isinstance(resp, dict):
            result["response"] = strip_internal_attributes(resp)
        else:
            result["response"] = str(resp)
        # Set ext_id to client_id for tracking
        result["ext_id"] = client_id
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_oidc_api_instance(module)
    run_action(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
