#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_mappings_info_v2
short_description: Fetch user mappings info for a Nutanix Files file server in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about UserMapping in Nutanix Prism Central.
  - It downloads the current NFS/SMB user-mapping configuration for the given
    Nutanix Files file server via the v4 Files API.
  - The underlying API does not support get-by-ext_id, list, filter or
    limit for user mappings; the caller must always provide the parent
    C(file_server_ext_id) and the module returns the mapping payload for
    that specific file server.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Download user mappings for a file server) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - The external identifier of the file server whose user mappings are to
        be downloaded.
    type: str
    required: true
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Download user mappings for a file server
  nutanix.ncp.ntnx_user_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "0005d0f6-1c3f-4e15-1155-ac1f6b6d0e3c"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC UserMapping info v4 API.
    - It contains the user-mapping configuration downloaded from the
      specified file server.
  returned: always
  type: dict
  sample: {}

ext_id:
  description:
    - External ID of the file server whose user mappings were downloaded.
  returned: when C(file_server_ext_id) is provided
  type: str
  sample: "0005d0f6-1c3f-4e15-1155-ac1f6b6d0e3c"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while downloading user mappings for file server"

error:
  description:
    - This field typically holds information about if the task have errors
      that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_user_mappings_api_instance,
)
from ..module_utils.v4.files.helpers import get_user_mappings  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_user_mappings_for_file_server(module, api_instance, result):
    """
    Fetch the user mappings for the given file server and populate result.

    Args:
        module (object): Ansible module object
        api_instance (object): UserMappingsApi instance
        result (dict): Result object to populate for the caller
    """
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = file_server_ext_id

    resp = get_user_mappings(module, api_instance, file_server_ext_id)

    payload = {}
    if resp is not None:
        if getattr(resp, "data", None) is not None and hasattr(resp.data, "to_dict"):
            payload = strip_internal_attributes(resp.data.to_dict()) or {}
        elif hasattr(resp, "to_dict"):
            payload = strip_internal_attributes(resp.to_dict()) or {}

    result["response"] = payload


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False, "ext_id": None}
    api_instance = get_user_mappings_api_instance(module)
    get_user_mappings_for_file_server(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
