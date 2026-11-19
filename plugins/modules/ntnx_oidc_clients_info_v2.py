#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_oidc_clients_info_v2
short_description: Fetch OIDC clients from Nutanix Prism Central
version_added: "2.7.0"
description:
    - This module allows you to fetch information about OIDC clients in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific OIDC client.
    - If C(ext_id) is not provided, list multiple OIDC clients optionally paginated.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned
      to the user performing the operation.
    - >-
      B(View OIDC Client) -
      Required Roles: Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam&version=v4.1.b4#tag/OIDC)"
options:
  ext_id:
    description:
      - The External ID of the OIDC client.
    type: str
    required: false
  page:
    description:
      - A URL query parameter that specifies the page number of the result set.
      - It must be a positive integer between 0 and the maximum number of pages that are available for that resource.
      - Any number out of this range might lead to no results.
    type: int
    required: false
  limit:
    description:
      - A URL query parameter that specifies the total number of records returned in the result set.
      - Must be a positive integer between 1 and 100.
      - Any number out of this range will lead to a validation error.
      - If the limit is not provided, a default value of 50 records will be returned in the result set.
    type: int
    required: false
  fetch_all:
    description:
      - When C(true), paginate through the list API until all available entities are returned.
      - C(page) and C(limit) are ignored; each request uses the maximum page size (100).
      - When C(false), return a single page (API default limit).
      - Does not apply when fetching a single entity by C(ext_id).
    type: bool
    required: false
    default: false
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
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch OIDC client using External ID
  nutanix.ncp.ntnx_oidc_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0e820dbd-aa56-4257-9f99-2b9930a406bf"
  register: result

- name: List OIDC clients
  nutanix.ncp.ntnx_oidc_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List OIDC clients with limit
  nutanix.ncp.ntnx_oidc_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: List OIDC clients with fetch_all
  nutanix.ncp.ntnx_oidc_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
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
                "application_type": "Backend application",
                "client_id": "83704d9f-82e4-538c-a36d-faf668a3c838",
                "client_name": "oidc-sample-gt8f6w",
                "client_secret": "",
                "created_time": "2026-11-19T08:39:53.942972+00:00",
                "last_updated_time": "2026-11-19T08:39:53.942972+00:00",
                "redirect_uris": [
                    "https://example.com/callback",
                    "https://example.com/callback2"
                ],
                "sha256_thumbprint_list": [
                    "3BCbFA2eeDF0F6bf9E8Fc41ccA8eFAafBF1dCe1B3cEAB51De4fF0E2EB7B52E4d"
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
  returned: always
  type: str
  sample: false
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
ext_id:
  description:
    - The External ID of the OIDC client.
  returned: when ext_id is provided
  type: str
  sample: "0e820dbd-aa56-4257-9f99-2b9930a406bf"
total_available_results:
    description:
        - The total number of available OIDC clients in PC.
    type: int
    returned: when all OIDC clients are fetched
    sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_oidc_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_oidc_client  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402
from ..module_utils.v4.utils import list_entities, raise_api_exception  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        page=dict(type="int"),
        limit=dict(type="int"),
        fetch_all=dict(type="bool", required=False, default=False),
    )

    return module_args


def get_oidc_client_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_oidc_client(module, api_instance, ext_id=ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_oidc_clients(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating OIDC clients info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_oidc_clients,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching OIDC clients info",
        )

    # list_oidc_clients returns list directly when not paginated via fetch_all helper,
    # but list_entities wraps pagination and returns ListEntitiesResponse with metadata
    # Check if resp has metadata attribute (ListEntitiesResponse) vs direct list
    if hasattr(resp, "metadata") and resp.metadata is not None:
        total_available_results = getattr(
            resp.metadata, "total_available_results", None
        )
        if total_available_results is not None:
            result["total_available_results"] = total_available_results
        # data is list of OIDC clients
        data = getattr(resp, "data", None)
        if data is None:
            data = []
        # convert each item to dict
        resp_list = []
        for item in data:
            try:
                resp_list.append(strip_internal_attributes(item.to_dict()))
            except Exception:
                resp_list.append(item)
        result["response"] = resp_list
    elif isinstance(resp, list):
        # Direct list response without metadata
        resp_list = []
        for item in resp:
            try:
                resp_list.append(strip_internal_attributes(item.to_dict()))
            except Exception:
                # item may already be dict
                resp_list.append(item)
        result["response"] = resp_list
        result["total_available_results"] = len(resp_list)
    else:
        # Fallback: try to handle as dict-wrapped response
        try:
            resp_dict = strip_internal_attributes(resp.to_dict())
            total_available_results = resp_dict.get("metadata", {}).get(
                "total_available_results"
            )
            if total_available_results is not None:
                result["total_available_results"] = total_available_results
            data = resp_dict.get("data")
            if not data:
                data = []
            result["response"] = data
        except Exception:
            result["response"] = []


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
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
