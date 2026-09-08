#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_claim_tokenss_info_v2
short_description: Fetch Foundation Central claim tokens info
version_added: 2.7.0
description:
  - This module allows you to fetch Foundation Central claim tokens info.
  - If C(ext_id) is not provided, it fetches the list of claim tokens (with optional filter, limit, etc.).
  - If C(ext_id) is provided, it fetches a specific claim token by external ID.
  - If C(ext_id) and C(fetch_secret) are provided, it fetches the claim token secret.
  - If C(ext_id) and C(node_ext_id) are provided, it fetches a specific node registered with the claim token.
  - If C(ext_id) and C(fetch_nodes) are provided, it fetches the list of nodes registered with the claim token.
  - This module uses the Life Cycle Management (lifecycle) v4 APIs based SDK.
notes:
  - This module talks to B(Foundation Central (FCVM)), not Prism Central.
    Point C(nutanix_host) and C(nutanix_port) at the Foundation Central VM endpoint.
  - >-
    This module requires the appropriate Foundation Central role/permissions to be assigned
    to the user performing the operation.
  - B(Get/List claim tokens, nodes and secret) - Requires an appropriate viewer/admin role on Foundation Central.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  ext_id:
    description:
      - The external ID of the claim token.
      - If provided, a single claim token is returned (unless C(node_ext_id), C(fetch_secret) or C(fetch_nodes) is set).
    type: str
    required: false
  node_ext_id:
    description:
      - The external ID of a node registered with the claim token.
      - When provided along with C(ext_id), a single node registered with the claim token is returned.
    type: str
    required: false
  fetch_secret:
    description:
      - When set to C(true) along with C(ext_id), the claim token secret is returned.
    type: bool
    required: false
    default: false
  fetch_nodes:
    description:
      - When set to C(true) along with C(ext_id), the list of nodes registered with the claim token is returned.
    type: bool
    required: false
    default: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all claim tokens
  nutanix.ncp.ntnx_claim_tokenss_info_v2:
    nutanix_host: "{{ foundation_central_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List claim tokens with filter
  nutanix.ncp.ntnx_claim_tokenss_info_v2:
    nutanix_host: "{{ foundation_central_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'claim_token_ansible'"
  register: result
  ignore_errors: true

- name: List claim tokens with limit
  nutanix.ncp.ntnx_claim_tokenss_info_v2:
    nutanix_host: "{{ foundation_central_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: Get claim token using ext_id
  nutanix.ncp.ntnx_claim_tokenss_info_v2:
    nutanix_host: "{{ foundation_central_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: Get claim token secret using ext_id
  nutanix.ncp.ntnx_claim_tokenss_info_v2:
    nutanix_host: "{{ foundation_central_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    fetch_secret: true
  register: result
  ignore_errors: true

- name: List nodes registered with a claim token
  nutanix.ncp.ntnx_claim_tokenss_info_v2:
    nutanix_host: "{{ foundation_central_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    fetch_nodes: true
  register: result
  ignore_errors: true

- name: Get a node registered with a claim token using node_ext_id
  nutanix.ncp.ntnx_claim_tokenss_info_v2:
    nutanix_host: "{{ foundation_central_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    node_ext_id: "5f1b6c7d-1234-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix claim tokens info v4 API. This module targets
      Foundation Central (FCVM), not Prism Central.
    - It can be a single claim token if external ID is provided.
    - List of multiple claim tokens if external ID is not provided (with optional filter or limit).
    - If C(fetch_secret) is set, it returns the claim token secret.
    - If C(node_ext_id) is set, it returns a single node registered with the claim token.
    - If C(fetch_nodes) is set, it returns the list of nodes registered with the claim token.
  returned: always
  type: dict
  sample:
    {
      "created_time": "2026-09-08T06:29:30.183575+00:00",
      "current_usage_count": 0,
      "expiry_time": "2026-11-01T00:00:00+00:00",
      "ext_id": "5b3a0229-c34b-40e1-92be-216f5256666b",
      "links": null,
      "max_usage_count": 5,
      "name": "claim_token_ansible",
      "owner_ext_id": "7cb3e9ea-7815-4d1a-9c1e-4e3a9277c17b",
      "tenant_id": "703c7c79-5e87-4813-a137-76c09b808db9"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always False for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching claim tokens info"

error:
  description: This field typically holds information about any error that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about whether the task has failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the claim token.
  type: str
  returned: When external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description: The total number of available claim tokens (or nodes) matching the query.
  type: int
  returned: When a list of claim tokens or nodes is fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_claim_tokens_api_instance  # noqa: E402
from ..module_utils.v4.lcm.helpers import get_claim_token  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        node_ext_id=dict(type="str"),
        fetch_secret=dict(type="bool", default=False),
        fetch_nodes=dict(type="bool", default=False),
    )

    return module_args


def get_claim_token_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_claim_token(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_claim_token_secret(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    try:
        resp = api_instance.get_secret_by_claim_token_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching claim token secret",
        )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_node_by_claim_token(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    node_ext_id = module.params.get("node_ext_id")
    try:
        resp = api_instance.get_node_by_claim_token_id(
            claimTokenExtId=ext_id, extId=node_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching node by claim token",
        )
    result["ext_id"] = node_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def list_nodes_by_claim_token(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating nodes by claim token info spec", **result
        )
    try:
        resp = api_instance.list_nodes_by_claim_token_id(
            claimTokenExtId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching nodes by claim token",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def get_claim_tokens(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating claim tokens info spec", **result)

    try:
        resp = api_instance.list_claim_tokens(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching claim tokens info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
            ("node_ext_id", "fetch_secret"),
            ("node_ext_id", "fetch_nodes"),
            ("fetch_secret", "fetch_nodes"),
        ],
        required_by={
            "node_ext_id": "ext_id",
        },
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_claim_tokens_api_instance(module)
    if module.params.get("ext_id"):
        if module.params.get("fetch_secret"):
            get_claim_token_secret(module, api_instance, result)
        elif module.params.get("node_ext_id"):
            get_node_by_claim_token(module, api_instance, result)
        elif module.params.get("fetch_nodes"):
            list_nodes_by_claim_token(module, api_instance, result)
        else:
            get_claim_token_using_ext_id(module, api_instance, result)
    else:
        get_claim_tokens(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
