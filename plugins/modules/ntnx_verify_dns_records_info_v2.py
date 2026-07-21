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
    - This module allows you to fetch information about DNS records of a Nutanix Files file server.
    - Given a file server C(file_server_ext_id), it lists the DNS records (A/AAAA/PTR) currently
      registered for that file server and their verification state.
    - Supports optional pagination (C(page), C(limit)), OData filtering (C(filter))
      on the C(isVerified) field, sorting (C(orderby)) and field selection (C(select)).
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List DNS records of a file server) -
      Required Roles: Files Admin, Files Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
    file_server_ext_id:
        description:
            - The external identifier of the parent file server whose DNS records should be listed.
        type: str
        required: true
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
- name: List DNS records of a file server
  nutanix.ncp.ntnx_verify_dns_records_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "b1cbe1cb-fc4a-4d1a-9c74-1c1ee1cbf1cb"
  register: result
  ignore_errors: true

- name: List only verified DNS records of a file server
  nutanix.ncp.ntnx_verify_dns_records_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "b1cbe1cb-fc4a-4d1a-9c74-1c1ee1cbf1cb"
    filter: "isVerified eq true"
  register: result
  ignore_errors: true

- name: List DNS records of a file server with a limit
  nutanix.ncp.ntnx_verify_dns_records_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "b1cbe1cb-fc4a-4d1a-9c74-1c1ee1cbf1cb"
    limit: 5
  register: result
  ignore_errors: true

- name: List DNS records of a file server sorted by verification state
  nutanix.ncp.ntnx_verify_dns_records_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "b1cbe1cb-fc4a-4d1a-9c74-1c1ee1cbf1cb"
    orderby: "isVerified desc"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC list DNS records v4 API.
        - A list of DNS records registered for the given file server; each entry
          contains the host address, PTR record, and its verification flag.
    returned: always
    type: list
    elements: dict
    sample:
        - ext_id: "d7431a2f-2fb9-4a5a-9c9c-1b28a2f61c4c"
          host_address:
              fqdn:
                  value: "files-server.example.com"
              ipv4: null
              ipv6: null
          is_verified: true
          links: null
          ptr_record:
              fqdn: null
              ipv4:
                  prefix_length: 32
                  value: "10.0.0.10"
              ipv6: null
          tenant_id: null
        - ext_id: "8c3b6df8-3d33-4b3d-8a63-6c6c9d0e1e12"
          host_address:
              fqdn:
                  value: "files-server-2.example.com"
              ipv4: null
              ipv6: null
          is_verified: false
          links: null
          ptr_record:
              fqdn: null
              ipv4:
                  prefix_length: 32
                  value: "10.0.0.11"
              ipv6: null
          tenant_id: null

changed:
    description: This indicates whether the task resulted in any changes. Always false for info modules.
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while listing DNS records for file server"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    type: str
    returned: when an error occurs

failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false

total_available_results:
    description: The total number of DNS records available for the given file server.
    type: int
    returned: when DNS records are fetched
    sample: 2
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
    )

    return module_args


def list_file_server_dns_records(module, dns_api, result):
    file_server_ext_id = module.params.get("file_server_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating DNS records info spec", **result)

    kwargs.pop("file_server_ext_id", None)

    try:
        resp = dns_api.list_dns_records(fileServerExtId=file_server_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing DNS records for file server",
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
    dns_api = get_dns_api_instance(module)
    list_file_server_dns_records(module, dns_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
