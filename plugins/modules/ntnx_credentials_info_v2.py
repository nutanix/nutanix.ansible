#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_credentials_info_v2
short_description: Fetch credential info from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Credential in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Credential.
  - If C(ext_id) is not provided, list multiple Credential optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get credential by ext_id) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List credentials) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
  ext_id:
    description:
      - The external ID of the credential.
    type: str
    required: false
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
- name: Get credential using ext_id
  nutanix.ncp.ntnx_credentials_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all credentials
  nutanix.ncp.ntnx_credentials_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List credentials with filter
  nutanix.ncp.ntnx_credentials_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'bmc_credential_ansible'"
  register: result
  ignore_errors: true

- name: List credentials with limit
  nutanix.ncp.ntnx_credentials_info_v2:
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
    - The response from the Nutanix PC Credential info v4 API.
    - It can be a single Credential if external ID is provided.
    - List of multiple Credential if external ID is not provided with optional filter, limit, orderby or select.
  returned: always
  type: dict
  sample:
    {
      "credential_details": {
          "credential": {
              "password": null,
              "username": "ADMIN"
          },
          "type": null
      },
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "is_valid": true,
      "links": null,
      "name": "bmc_credential_ansible",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching Credential info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the credential.
  type: str
  returned: when external ID is provided
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

total_available_results:
  description: The total number of credentials available in Prism Central.
  type: int
  returned: when all credentials are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_credentials_api_instance,
)
from ..module_utils.v4.security.helpers import get_credential_by_ext_id  # noqa: E402
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
    )
    return module_args


def get_credential_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_credential_by_ext_id(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_credentials(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Credentials info spec", **result)

    try:
        resp = api_instance.list_credentials(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Credentials info",
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
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_credentials_api_instance(module)
    if module.params.get("ext_id"):
        get_credential_using_ext_id(module, api_instance, result)
    else:
        get_credentials(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
