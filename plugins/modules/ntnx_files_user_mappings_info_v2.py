#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_user_mappings_info_v2
short_description: Download (fetch) user mappings of a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to fetch information about UserMapping in Nutanix Prism Central.
  - It downloads the user mappings configured on the given file server.
  - The user mappings describe how identities (users and groups) are mapped across the SMB and
    NFS protocols for multi-protocol shares on the file server.
  - Optionally, the downloaded user mappings can be saved to a local file using C(path).
  - This module uses PC v4 APIs based SDKs.
notes:
  - This module requires the Nutanix Files service (Files Manager) to be enabled on Prism Central.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - The external identifier of the file server whose user mappings will be downloaded.
    type: str
    required: true
  path:
    description:
      - Local path where the downloaded user mappings file will be saved.
      - If not provided, the downloaded file location is returned in the response without
        copying it to a user-defined location.
    type: path
    required: false
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
- name: Download user mappings of a file server
  nutanix.ncp.ntnx_files_user_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d1e2f3a4-b5c6-47d8-9e0f-1a2b3c4d5e6f"
  register: result
  ignore_errors: true

- name: Download user mappings of a file server and save to a local file
  nutanix.ncp.ntnx_files_user_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d1e2f3a4-b5c6-47d8-9e0f-1a2b3c4d5e6f"
    path: "/tmp/downloaded_user_mappings.csv"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC UserMapping info v4 API.
    - It contains the downloaded user mappings of the file server referenced by C(file_server_ext_id).
    - When there are no user mappings configured, an empty list is returned.
  returned: always
  type: dict
  sample: "/tmp/ansible-tmp/user-mappings-d1e2f3a4.csv"

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - The external ID of the file server whose user mappings were downloaded.
  returned: when file_server_ext_id is provided
  type: str
  sample: "d1e2f3a4-b5c6-47d8-9e0f-1a2b3c4d5e6f"

path:
  description:
    - The local path where the downloaded user mappings file was saved.
  returned: when C(path) is provided
  type: str
  sample: "/tmp/downloaded_user_mappings.csv"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  returned: when an error occurs
  type: str
  sample: "Api Exception raised while downloading user mappings"

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while downloading user mappings"
"""

import shutil  # noqa: E402
import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_user_mappings_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        path=dict(type="path", required=False),
    )
    return module_args


def download_user_mappings(module, result, user_mappings_api):
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = file_server_ext_id

    resp = None
    try:
        resp = user_mappings_api.download_user_mappings(
            fileServerExtId=file_server_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while downloading user mappings",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")

    target_path = module.params.get("path")
    downloaded = resp.data
    if target_path and isinstance(downloaded, Path) and downloaded.is_file():
        shutil.copyfile(str(downloaded), target_path)
        result["path"] = target_path


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    user_mappings_api = get_user_mappings_api_instance(module)
    download_user_mappings(module, result, user_mappings_api)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
