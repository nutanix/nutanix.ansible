#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_dns_records_info_v2
short_description: Fetch DNS records for a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to fetch information about DnsRecord in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific DnsRecord.
  - If C(ext_id) is not provided, list multiple DnsRecord optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(List DNS records) -
    Required Roles: File Server Admin, File Server Viewer, Prism Admin,
    Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - The external identifier of the file server whose DNS records should be
        listed.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of an individual DNS record.
      - When provided, the returned response contains only the matching DNS
        record filtered from the DNS records of the file server.
      - The Nutanix Files v4 DNS API only exposes a list endpoint, so this
        module lists records for the file server and then filters by
        C(ext_id) locally.
    type: str
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
- name: List all DNS records for a file server
  nutanix.ncp.ntnx_files_dns_records_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
  register: result
  ignore_errors: true

- name: Get a specific DNS record by external ID
  nutanix.ncp.ntnx_files_dns_records_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List DNS records filtered by isVerified
  nutanix.ncp.ntnx_files_dns_records_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    filter: "isVerified eq true"
  register: result
  ignore_errors: true

- name: List DNS records with limit
  nutanix.ncp.ntnx_files_dns_records_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC DnsRecord info v4 API.
    - It can be a single DnsRecord if external ID is provided.
    - List of multiple DnsRecord if external ID is not provided with optional
      filter or limit.
  returned: always
  type: dict
  sample:
    [
      {
        "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
        "host_address": {
          "fqdn": null,
          "ipv4": {
            "prefix_length": 32,
            "value": "10.44.76.28"
          },
          "ipv6": null
        },
        "is_verified": true,
        "links": null,
        "ptr_record": {
          "fqdn": {
            "value": "fs-ansible.example.com"
          },
          "ipv4": null,
          "ipv6": null
        },
        "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the DNS record when provided.
  returned: when external ID is provided
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

total_available_results:
  description: The total number of DNS records available on the file server.
  returned: when all DNS records are fetched
  type: int
  sample: 5

msg:
  description: Contextual message emitted by the module.
  returned: When there is an error or when no matching record is found
  type: str
  sample: "Api Exception raised while fetching DNS records for file server"

error:
  description: Error details when an API failure occurs.
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the module task failed.
  returned: always
  type: bool
  sample: false
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
        ext_id=dict(type="str"),
    )

    return module_args


def _list_dns_records(module, api_instance):
    """
    Invoke the ``ListDnsRecords`` API for the file server and return the
    stripped response dict along with the ``total_available_results`` count.
    """
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        module.fail_json(msg="Failed generating DNS records info spec", error=err)

    try:
        resp = api_instance.list_dns_records(
            fileServerExtId=module.params.get("file_server_ext_id"), **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching DNS records for file server",
        )

    resp_dict = strip_internal_attributes(resp.to_dict())
    total_available_results = (
        resp_dict.get("metadata", {}).get("total_available_results")
        if resp_dict.get("metadata")
        else None
    )
    data = resp_dict.get("data")
    if not data:
        data = []
    return data, total_available_results


def get_dns_record_by_ext_id(module, api_instance, result):
    """
    The Files v4 DNS API only exposes a list endpoint. To emulate get-by-id
    behaviour, list all DNS records for the referenced file server and then
    filter by the supplied ``ext_id``.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    records, _total = _list_dns_records(module, api_instance)
    match = next((r for r in records if r.get("ext_id") == ext_id), None)
    if match is None:
        module.fail_json(
            msg=("DNS record with ext_id '{0}' not found on file server '{1}'.").format(
                ext_id, module.params.get("file_server_ext_id")
            ),
            **result,
        )
    result["response"] = match


def get_dns_records(module, api_instance, result):
    """Retrieve all DNS records for a file server."""
    records, total_available_results = _list_dns_records(module, api_instance)
    result["total_available_results"] = total_available_results
    result["response"] = records


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
    api_instance = get_dns_api_instance(module)
    if module.params.get("ext_id"):
        get_dns_record_by_ext_id(module, api_instance, result)
    else:
        get_dns_records(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
