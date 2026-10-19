#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_login_providers_info_v2
short_description: Fetch login providers info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to list LoginProvider entities in Nutanix Prism Central.
  - The IAM LoginProviders API exposes list only; there is no get-by-ext_id
    endpoint on Prism Central.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List login providers) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
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
- name: List all login providers configured on Prism Central
  nutanix.ncp.ntnx_login_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: providers

- name: List login providers and filter by name
  nutanix.ncp.ntnx_login_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'local'"
  register: local_providers

- name: List login providers with limit
  nutanix.ncp.ntnx_login_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 2
  register: limited_providers

- name: Fetch all login providers using fetch_all
  nutanix.ncp.ntnx_login_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: all_providers
"""

RETURN = r"""
response:
  description:
    - Response for the login providers info API.
    - Contains the list of login providers configured on Prism Central.
  returned: always
  type: list
  sample:
    [
        {
            "created_time": "2026-06-29T07:18:36.283028+00:00",
            "ext_id": "d607d664-cc19-559f-a95c-4e8b4b7f6606",
            "isSharedWithAllProjects": true,
            "is_browser_login_supported": true,
            "last_updated_time": "2026-06-29T07:18:36.283028+00:00",
            "links": null,
            "name": "local",
            "projectExtId": "00000000-0000-0000-0000-000000000000",
            "tenant_id": null,
            "type": "local"
        }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching login providers info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available login providers in PC.
  type: int
  returned: when login providers are listed
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_login_providers_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_login_providers(module, login_providers_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating login providers info spec", **result)

    try:
        resp = list_entities(
            login_providers_api.list_login_providers,
            kwargs=kwargs,
            fetch_all=module.params.get("fetch_all"),
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching login providers info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=dict(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    login_providers_api = get_login_providers_api_instance(module)
    get_login_providers(module, login_providers_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
