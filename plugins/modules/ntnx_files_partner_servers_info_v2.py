#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_partner_servers_info_v2
short_description: Fetch partner servers info in Nutanix Files
version_added: 2.7.0
description:
  - This module allows you to fetch information about PartnerServer in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific PartnerServer.
  - If C(ext_id) is not provided, list multiple PartnerServer optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - The external identifier of the file server the partner server belongs to.
      - Required for all operations.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the partner server.
      - If provided, fetch details of the specific partner server.
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
- name: Get partner server using ext_id
  nutanix.ncp.ntnx_files_partner_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "aa04b8ce-6b23-4d5e-8f6a-9e0b3c1d2e4f"
  register: result
  ignore_errors: true

- name: List all partner servers for a file server
  nutanix.ncp.ntnx_files_partner_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true

- name: List partner servers with filter
  nutanix.ncp.ntnx_files_partner_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    filter: "name eq 'partner_server_ansible'"
  register: result
  ignore_errors: true

- name: List partner servers with limit
  nutanix.ncp.ntnx_files_partner_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC PartnerServer info v4 API.
    - It can be a single PartnerServer if external ID is provided.
    - List of multiple PartnerServer if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "backup_server_config": null,
      "description": "Notification partner server created by Ansible",
      "ext_id": "aa04b8ce-6b23-4d5e-8f6a-9e0b3c1d2e4f",
      "links": null,
      "name": "partner_server_ansible",
      "partner_type": "NOTIFICATION",
      "tenant_id": null,
      "vendor_name": "DataLens",
      "vendor_properties": {
          "address": {
              "fqdn": null,
              "ipv4": {
                  "prefix_length": 32,
                  "value": "10.44.77.10"
              },
              "ipv6": null
          },
          "connection_status": "NOT_TESTED",
          "custom_properties": [
              {
                  "name": "kafkatopic",
                  "value": "1P1R"
              }
          ],
          "port": 29092,
          "server_type": "PRIMARY"
      }
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
  sample: "Api Exception raised while fetching partner servers info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the partner server
  type: str
  returned: when external ID is provided
  sample: "aa04b8ce-6b23-4d5e-8f6a-9e0b3c1d2e4f"

total_available_results:
  description: The total number of available partner servers for the file server.
  type: int
  returned: when all partner servers are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_partner_servers_api_instance,
)
from ..module_utils.v4.files.helpers import get_partner_server  # noqa: E402
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


def get_partner_server_using_ext_id(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_partner_server(module, api_instance, file_server_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_partner_servers(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating partner servers info spec", **result)

    try:
        resp = api_instance.list_partner_servers(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching partner servers info",
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
    api_instance = get_partner_servers_api_instance(module)
    if module.params.get("ext_id"):
        get_partner_server_using_ext_id(module, api_instance, result)
    else:
        get_partner_servers(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
