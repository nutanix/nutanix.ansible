#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_object_stores_certificate_download_v2
short_description: Download Object Stores certificate authority
version_added: 2.6.0
description:
    - Download the certificate authority (CA) for a specific object store certificate.
    - The certificate authority is returned as an C(application/octet-stream) download and saved to a local file.
    - The local downloaded file path is returned under C(response.path).
    - This module uses PC v4 APIs based GA SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Download the certificate authority of an Object store certificate) -
      Required Roles: Objects Admin, Objects Editor, Objects Viewer, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=objects)"
options:
    object_store_ext_id:
        description: Object store External ID.
        type: str
        required: true
    ext_id:
        description: External ID of certificate whose certificate authority should be downloaded.
        type: str
        required: true
    dest:
        description:
            - Local destination file path where the downloaded certificate authority (CA) should be saved.
            - The parent directory is created if it does not already exist.
            - If not provided, the CA is saved to the SDK default download location and that path is returned.
        type: path
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
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Download the certificate authority (CA) of an object store certificate
  nutanix.ncp.ntnx_object_stores_certificate_download_v2:
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    ext_id: "f3197423-f486-4037-6037-95442e58484e"
  register: result

- name: Download the certificate authority (CA) to a specific destination path
  nutanix.ncp.ntnx_object_stores_certificate_download_v2:
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    ext_id: "f3197423-f486-4037-6037-95442e58484e"
    dest: "/tmp/object_store_ca.pem"
  register: result
"""

RETURN = r"""
response:
    description: A dict containing local path of downloaded certificate authority file.
    type: dict
    returned: always
    sample:
        {
            "path": "/tmp/object_store_ca.pem"
        }

ext_id:
    description: External ID of the object store certificate.
    returned: always
    type: str
    sample: "f3197423-f486-4037-6037-95442e58484e"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false

msg:
    description: Message returned when an error occurs.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while downloading object store certificate authority"

error:
    description: Details about errors that occurred during task execution.
    returned: When an error occurs
    type: str

failed:
    description: This field indicates whether the task failed.
    returned: always
    type: bool
    sample: false
"""

import os  # noqa: E402
import shutil  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.objects.api_client import get_objects_api_instance  # noqa: E402
from ..module_utils.v4.objects.helpers import (  # noqa: E402
    get_object_store_certificate_authority,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        object_store_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        dest=dict(type="path"),
    )
    return module_args


def download_object_store_certificate_ca(module, object_stores_api, result):
    ext_id = module.params.get("ext_id")
    object_store_ext_id = module.params.get("object_store_ext_id")
    dest = module.params.get("dest")
    result["ext_id"] = ext_id

    if dest:
        dest_dir = os.path.dirname(os.path.abspath(dest))
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        object_stores_api.api_client.configuration.download_directory = dest_dir

    resp = get_object_store_certificate_authority(
        module, object_stores_api, ext_id, object_store_ext_id
    )

    data = resp.data
    if isinstance(data, dict):
        downloaded_path = data.get("path")
    else:
        downloaded_path = getattr(data, "path", None)

    if not downloaded_path:
        module.fail_json(
            msg="Failed to determine the downloaded certificate authority file path",
            **result,
        )

    downloaded_path = str(downloaded_path)
    if dest and os.path.abspath(downloaded_path) != os.path.abspath(dest):
        shutil.move(downloaded_path, dest)
        downloaded_path = dest

    result["response"] = {"path": downloaded_path}


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    object_stores_api = get_objects_api_instance(module)
    download_object_store_certificate_ca(module, object_stores_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
