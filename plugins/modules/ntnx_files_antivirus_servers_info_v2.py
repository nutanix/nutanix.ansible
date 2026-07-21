#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_antivirus_servers_info_v2
short_description: Fetch antivirus servers info of a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to fetch information about AntivirusServer in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific AntivirusServer.
  - If C(ext_id) is not provided, list multiple AntivirusServer optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - This module requires an existing Nutanix Files file server. The antivirus servers are configured under that file server.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external ID of the antivirus server.
      - If provided, the specific antivirus server details are fetched.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server on which the antivirus servers are configured.
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
- name: Fetch antivirus server using ext_id
  nutanix.ncp.ntnx_files_antivirus_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "b1c2d3e4-14a6-4c47-b5db-920460c4b668"
  register: result

- name: List all antivirus servers of a file server
  nutanix.ncp.ntnx_files_antivirus_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
  register: result

- name: List antivirus servers with filter
  nutanix.ncp.ntnx_files_antivirus_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    filter: "port eq 1344"
  register: result

- name: List antivirus servers with limit
  nutanix.ncp.ntnx_files_antivirus_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC AntivirusServer info v4 API.
    - It can be a single AntivirusServer if external ID is provided.
    - List of multiple AntivirusServer if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "address": {
          "fqdn": null,
          "ipv4": {
              "prefix_length": 32,
              "value": "10.44.10.100"
          },
          "ipv6": null
      },
      "connection_status": "NOT_TESTED",
      "description": "Antivirus server created by Ansible",
      "ext_id": "b1c2d3e4-14a6-4c47-b5db-920460c4b668",
      "links": null,
      "partner_service_name": "avscan",
      "port": 1344,
      "tenant_id": null
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
  sample: "Api Exception raised while fetching antivirus servers info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the antivirus server
  type: str
  returned: when external ID is provided
  sample: "b1c2d3e4-14a6-4c47-b5db-920460c4b668"

total_available_results:
  description: The total number of available antivirus servers on the file server.
  type: int
  returned: when all antivirus servers are fetched
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_antivirus_servers_api_instance,
)
from ..module_utils.v4.files.helpers import get_antivirus_server  # noqa: E402
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
        file_server_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_antivirus_server_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    resp = get_antivirus_server(module, api_instance, ext_id, file_server_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_antivirus_servers(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating antivirus servers info spec", **result)

    try:
        resp = api_instance.list_antivirus_servers(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching antivirus servers info",
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
    api_instance = get_antivirus_servers_api_instance(module)
    if module.params.get("ext_id"):
        get_antivirus_server_using_ext_id(module, api_instance, result)
    else:
        get_antivirus_servers(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
