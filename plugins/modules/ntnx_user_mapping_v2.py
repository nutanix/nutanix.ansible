#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_mapping_v2
short_description: Upload (bulk configure) user mappings for a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to upload user mappings to a file server in Nutanix Prism Central.
  - User mappings define how identities (users and groups) are mapped across the SMB and NFS
    protocols so that a multi-protocol share can be accessed consistently by both protocols.
  - The mappings are provided as a local CSV file which is uploaded to the file server; this
    bulk configures or replaces the existing user mappings on the file server.
  - This module uses PC v4 APIs based SDKs.
notes:
  - This module requires the Nutanix Files service (Files Manager) to be enabled on Prism Central.
  - The C(path) must point to a valid CSV file that follows the user mappings template supported
    by the file server.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the user mappings from the provided CSV file are uploaded to the file server.
    type: str
    choices:
      - present
    default: present
  file_server_ext_id:
    description:
      - The external identifier of the file server on which the user mappings will be uploaded.
    type: str
    required: true
  path:
    description:
      - Local path to the CSV file containing the user mappings to upload.
      - The file must exist and be readable.
    type: path
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Upload user mappings to a file server
  nutanix.ncp.ntnx_user_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d1e2f3a4-b5c6-47d8-9e0f-1a2b3c4d5e6f"
    path: "/tmp/user_mappings.csv"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for uploading user mappings to the file server.
    - Contains the list of application messages returned by the upload operation.
  returned: always
  type: dict
  sample:
    [
      {
        "code": "FILES-UPLOAD-USER-MAPPINGS-SUCCESS",
        "error_group": null,
        "locale": "en-US",
        "message": "User mappings uploaded successfully.",
        "severity": "INFO"
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

ext_id:
  description:
    - The external ID of the file server on which the user mappings were uploaded.
  returned: always
  type: str
  sample: "d1e2f3a4-b5c6-47d8-9e0f-1a2b3c4d5e6f"

task_ext_id:
  description:
    - The external ID of the task.
    - This is C(null) for user mappings upload because the operation is performed synchronously.
  returned: always
  type: str
  sample: null

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  returned: when an error occurs
  type: str
  sample: "Api Exception raised while uploading user mappings"

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error or in check mode
  type: str
  sample: "User mappings from file '/tmp/user_mappings.csv' will be uploaded to file server 'd1e2f3a4-b5c6-47d8-9e0f-1a2b3c4d5e6f'."
"""

import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_user_mappings_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        file_server_ext_id=dict(type="str", required=True),
        path=dict(type="path", required=True),
    )
    return module_args


def upload_user_mappings(module, result, user_mappings_api):
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = file_server_ext_id
    validate_required_params(module, ["file_server_ext_id", "path"])

    file_path = Path(module.params.get("path"))
    if not file_path.is_file():
        module.fail_json(
            msg="The provided path '{0}' is not a valid file.".format(file_path),
            **result,
        )

    if module.check_mode:
        result["msg"] = (
            "User mappings from file '{0}' will be uploaded to file server '{1}'.".format(
                file_path, file_server_ext_id
            )
        )
        return

    resp = None
    try:
        resp = user_mappings_api.upload_user_mappings(
            fileServerExtId=file_server_ext_id, path=file_path
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while uploading user mappings",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    user_mappings_api = get_user_mappings_api_instance(module)
    upload_user_mappings(module, result, user_mappings_api)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
