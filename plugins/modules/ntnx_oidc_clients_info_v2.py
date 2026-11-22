#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_oidc_clients_info_v2
short_description: Fetch OIDC clients info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch OIDC clients info in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific OIDC client.
  - If C(ext_id) is not provided, list multiple OIDC clients with optional pagination.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get OIDC client by ext_id) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin
  - >-
    B(List OIDC clients) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  ext_id:
    description:
      - The external ID of the OIDC client.
    type: str
    required: false
  page:
    description:
      - A URL query parameter that specifies the page number of the result set.
    type: int
    required: false
  limit:
    description:
      - A URL query parameter that specifies the total number of records returned in the result set.
    type: int
    required: false
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
  nutanix.ncp.ntnx_oidc_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00000000-0000-0000-0000-000000000000"
  register: result
  ignore_errors: true

- name: List all OIDC clients
  nutanix.ncp.ntnx_oidc_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List OIDC clients with limit
  nutanix.ncp.ntnx_oidc_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC OIDC clients info v4 API.
    - It can be a single OIDC client if External ID is provided.
    - List of multiple OIDC clients if External ID is not provided with optional limit.
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
  sample: "Api Exception raised while fetching OIDC clients info"

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

total_available_results:
  description: The total number of available OIDC clients in PC.
  type: int
  returned: when all OIDC clients are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_oidc_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_oidc_client  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        page=dict(type="int"),
        limit=dict(type="int"),
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


def get_oidc_clients(module, api_instance, result):
    kwargs = {}
    if module.params.get("page") is not None:
        kwargs["_page"] = module.params.get("page")
    if module.params.get("limit") is not None:
        kwargs["_limit"] = module.params.get("limit")
    try:
        resp = api_instance.list_oidc_clients(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching OIDC clients info",
        )

    # Try to handle both SDK response types
    if hasattr(resp, "to_dict"):
        resp_dict = strip_internal_attributes(resp.to_dict())
        # List APIs may return with metadata and data
        if isinstance(resp_dict, dict) and "data" in resp_dict:
            total = None
            if resp_dict.get("metadata") and isinstance(resp_dict["metadata"], dict):
                total = resp_dict["metadata"].get("total_available_results")
            if total is not None:
                result["total_available_results"] = total
            data = resp_dict.get("data")
            if not data:
                data = []
            result["response"] = data
        elif isinstance(resp_dict, list):
            result["response"] = resp_dict
            result["total_available_results"] = len(resp_dict)
        else:
            # Fallback: resp is list directly or dict single
            result["response"] = resp_dict
    elif isinstance(resp, list):
        result["response"] = (
            strip_internal_attributes({"data": resp}).get("data") or resp
        )
        result["total_available_results"] = len(resp)
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
    if module.params.get("ext_id"):
        get_oidc_client_using_ext_id(module, api_instance, result)
    else:
        get_oidc_clients(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
