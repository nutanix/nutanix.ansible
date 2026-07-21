#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_revise_dns_records_info_v2
short_description: Fetch DNS records of a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to fetch information about DNS records of a
    Nutanix Files file server in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific DNS record for the
    file server referenced by C(file_server_ext_id).
  - If C(ext_id) is not provided, list multiple DNS records for the file
    server referenced by C(file_server_ext_id), optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get DNS records for a Files file server) -
    Required Roles: File Server Admin, File Server Viewer, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - The external identifier of the file server whose DNS records must be fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the DNS record to fetch.
      - If not provided, the module will list all DNS records for the given
        file server.
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
- name: Get a specific DNS record for a file server using ext_id
  nutanix.ncp.ntnx_revise_dns_records_info_v2:
    file_server_ext_id: "b1c9c4a2-1cbb-4c9d-8f92-2f01f76fed44"
    ext_id: "3fbc4d31-4c7c-4e2a-9a8b-06a0f0ebd0e2"
  register: result
  ignore_errors: true

- name: List all DNS records for a file server
  nutanix.ncp.ntnx_revise_dns_records_info_v2:
    file_server_ext_id: "b1c9c4a2-1cbb-4c9d-8f92-2f01f76fed44"
  register: result
  ignore_errors: true

- name: List DNS records for a file server with filter (isVerified)
  nutanix.ncp.ntnx_revise_dns_records_info_v2:
    file_server_ext_id: "b1c9c4a2-1cbb-4c9d-8f92-2f01f76fed44"
    filter: "isVerified eq true"
  register: result
  ignore_errors: true

- name: List DNS records for a file server with limit
  nutanix.ncp.ntnx_revise_dns_records_info_v2:
    file_server_ext_id: "b1c9c4a2-1cbb-4c9d-8f92-2f01f76fed44"
    limit: 5
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ReviseDnsRecord info v4 API.
    - It can be a single DNS record if C(ext_id) is provided.
    - List of multiple DNS records if C(ext_id) is not provided, with
      optional filter or limit.
  returned: always
  type: dict
  sample:
    [
      {
        "ext_id": "3fbc4d31-4c7c-4e2a-9a8b-06a0f0ebd0e2",
        "host_address": {
          "ipv4": {
            "prefix_length": 32,
            "value": "10.44.76.100"
          },
          "ipv6": null,
          "fqdn": null
        },
        "is_verified": true,
        "links": null,
        "ptr_record": null,
        "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching DNS records for file server"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the DNS record.
  type: str
  returned: When external ID is provided
  sample: "3fbc4d31-4c7c-4e2a-9a8b-06a0f0ebd0e2"

total_available_results:
  description: The total number of available DNS records for the file server.
  type: int
  returned: When DNS records are listed (no ext_id)
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import get_dns_api_instance  # noqa: E402
from ..module_utils.v4.files.helpers import get_dns_record  # noqa: E402
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
        ext_id=dict(type="str", required=False),
    )

    return module_args


def get_dns_record_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    record = get_dns_record(module, api_instance, file_server_ext_id, ext_id)
    if record is None:
        module.fail_json(
            msg="DNS record with ext_id:{0} not found on file server {1}".format(
                ext_id, file_server_ext_id
            ),
            **result,
        )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(record.to_dict())


def get_dns_records(module, api_instance, result):

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
            msg="Api Exception raised while fetching DNS records for file server",
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
    api_instance = get_dns_api_instance(module)
    if module.params.get("ext_id"):
        get_dns_record_using_ext_id(module, api_instance, result)
    else:
        get_dns_records(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
