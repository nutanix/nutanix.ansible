#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_image_download_v2
short_description: Download an image
version_added: "2.7.0"
description:
    - Download an image.
    - Downloads the image with the given external identifier.
    - The local downloaded file path is returned under C(response.path).
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Download an image) -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager, Super Admin, Tenant Admin, Tenant Consumer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    image_ext_id:
        description:
            - The external identifier of an image.
        type: str
        required: true
    dest:
        description:
            - Local destination file path where the downloaded image should be saved.
            - The parent directory is created if it does not already exist.
            - If not provided, the image is saved to the SDK default download location and that path is returned.
        type: path
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
- name: Download an image
  nutanix.ncp.ntnx_image_download_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    image_ext_id: "12345678-1234-1234-1234-123456789012"
  register: result

- name: Download an image to a specific destination path
  nutanix.ncp.ntnx_image_download_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    image_ext_id: "12345678-1234-1234-1234-123456789012"
    dest: "/tmp/downloaded_image.qcow2"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for downloading an image.
        - Contains the local path where the downloaded file was saved.
    type: dict
    returned: always
    sample:
        {
            "path": "/tmp/downloaded_image.qcow2"
        }
ext_id:
    description: The external ID of the image.
    type: str
    returned: always
    sample: "12345678-1234-1234-1234-123456789012"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "Image with ext_id:12345678-1234-1234-1234-123456789012 will be downloaded."
"""

import os  # noqa: E402
import shutil  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.utils import raise_api_exception  # noqa: E402
from ..module_utils.v4.vmm.api_client import get_image_api_instance  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        image_ext_id=dict(type="str", required=True),
        dest=dict(type="path"),
    )
    return module_args


def download_image(module, result, api_instance):
    image_ext_id = module.params.get("image_ext_id")
    dest = module.params.get("dest")
    result["ext_id"] = image_ext_id

    if module.check_mode:
        if dest:
            result["msg"] = (
                "Image with ext_id:{0} will be downloaded to destination path:{1}".format(
                    image_ext_id, dest
                )
            )
            result["response"] = {"path": dest}
        else:
            result["msg"] = "Image with ext_id:{0} will be downloaded.".format(
                image_ext_id
            )
        return

    if dest:
        dest_dir = os.path.dirname(os.path.abspath(dest))
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        api_instance.api_client.configuration.download_directory = dest_dir

    resp = None
    try:
        resp = api_instance.get_file_by_image_id(imageExtId=image_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while downloading image",
        )

    data = resp.to_dict().get("data")
    if isinstance(data, dict):
        downloaded_path = data.get("path")
    else:
        downloaded_path = getattr(data, "path", None)

    if not downloaded_path:
        module.fail_json(
            msg="Failed to determine the downloaded image file path",
            **result,
        )

    downloaded_path = str(downloaded_path)
    if dest and os.path.abspath(downloaded_path) != os.path.abspath(dest):
        shutil.move(downloaded_path, dest)
        downloaded_path = dest

    result["response"] = {
        "path": downloaded_path,
    }
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
        "failed": False,
    }
    api_instance = get_image_api_instance(module)
    download_image(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
