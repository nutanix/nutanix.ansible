#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_file_servers_info_v2
short_description: Fetch File Servers info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about FileServer in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific FileServer.
  - If C(ext_id) is not provided, list multiple FileServer optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get file server by ext_id) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - >-
      B(Get list of file servers) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external ID of the file server.
      - If provided, the module will fetch the specific file server.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Nutanix Ansible (@nutanix-ansible)
"""

EXAMPLES = r"""
- name: Get file server using ext_id
  nutanix.ncp.ntnx_files_file_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005c3f2-1a2b-4c5d-6e7f-8091a2b3c4d5"
  register: result
  ignore_errors: true

- name: List all file servers
  nutanix.ncp.ntnx_files_file_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List file servers with filter
  nutanix.ncp.ntnx_files_file_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'file_server_name'"
  register: result
  ignore_errors: true

- name: List file servers with limit
  nutanix.ncp.ntnx_files_file_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: List file servers ordered by name
  nutanix.ncp.ntnx_files_file_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    orderby: "name asc"
  register: result
  ignore_errors: true

- name: List file servers with select
  nutanix.ncp.ntnx_files_file_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    select: "name"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC FileServer info v4 API.
    - It can be a single FileServer if external ID is provided.
    - List of multiple FileServer if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "0005c3f2-1a2b-4c5d-6e7f-8091a2b3c4d5",
      "links": null,
      "name": "file_server_ansible",
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
  sample: "Api Exception raised while fetching file servers info"

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
  description: External ID of the file server
  type: str
  returned: When external ID is provided
  sample: "0005c3f2-1a2b-4c5d-6e7f-8091a2b3c4d5"

total_available_results:
  description: The total number of available file servers in PC.
  type: int
  returned: When all file servers are fetched
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_file_servers_api_instance,
)
from ..module_utils.v4.files.helpers import get_file_server  # noqa: E402
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


def get_file_server_using_ext_id(module, file_servers_api, result):
    ext_id = module.params.get("ext_id")
    resp = get_file_server(module, file_servers_api, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_file_servers(module, file_servers_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating file servers info spec", **result)

    try:
        resp = file_servers_api.list_file_servers(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching file servers info",
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
    file_servers_api = get_file_servers_api_instance(module)
    if module.params.get("ext_id"):
        get_file_server_using_ext_id(module, file_servers_api, result)
    else:
        get_file_servers(module, file_servers_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
