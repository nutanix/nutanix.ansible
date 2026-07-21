#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_verify_dns_records_info_v2
short_description: Fetch DNS records of a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to fetch information about DNS records of a Nutanix Files file server in Nutanix Prism Central.
  - It always lists DNS records belonging to the file server referenced by C(file_server_ext_id).
  - The list can optionally be filtered / paginated / ordered using standard OData query parameters
    (C(filter), C(limit), C(page), C(orderby), C(select)).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List DNS records for a file server) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, File Server Admin, File Server Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - The external identifier of the file server whose DNS records should be listed.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""
EXAMPLES = r"""
- name: List all DNS records for a file server
  nutanix.ncp.ntnx_verify_dns_records_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
  register: result
  ignore_errors: true

- name: List DNS records for a file server filtered on isVerified
  nutanix.ncp.ntnx_verify_dns_records_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    filter: "isVerified eq true"
  register: result
  ignore_errors: true

- name: List first DNS record only, ordered by isVerified descending
  nutanix.ncp.ntnx_verify_dns_records_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    limit: 1
    orderby: "isVerified desc"
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
    - The response from the Nutanix PC DNS records info v4 API.
    - List of DNS records for the referenced file server, optionally filtered / paginated / ordered.
  returned: always
  type: dict
  sample:
    [
      {
        "ext_id": "0cabf1bd-9c9c-4d55-b7d0-8f8b6a8cf5a2",
        "host_address": {
          "fqdn": {
            "value": "fs01.example.com"
          },
          "ipv4": null,
          "ipv6": null
        },
        "is_verified": true,
        "links": null,
        "ptr_record": null,
        "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching DNS records info"

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
  description: The total number of available DNS records for the file server.
  type: int
  returned: when all DNS records are fetched
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import get_dns_api_instance  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
    )

    return module_args


def list_dns_records(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating DNS records info spec", **result)

    file_server_ext_id = module.params.get("file_server_ext_id")

    try:
        resp = api_instance.list_dns_records(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching DNS records info",
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
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_dns_api_instance(module)
    list_dns_records(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
