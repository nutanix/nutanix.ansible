#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_image_download_v2
short_description: Download an image file from Nutanix Prism Central
version_added: 2.5.0
description:
    - Download an image file from Nutanix Prism Central using its external ID.
    - Wraps the VMM v4.2 C(GetFileByImageId) API
      (C(GET /api/vmm/v4.2/content/images/{imageExtId}/file)).
    - The image bytes are streamed by Prism Central from the hosting Prism
      Element cluster; the module returns the local path where the SDK
      persisted the downloaded file.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Download an Image) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    image_ext_id:
        description:
            - External ID of the image whose file should be downloaded.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Download image using ext_id
  nutanix.ncp.ntnx_image_download_v2:
    image_ext_id: "12345678-1234-1234-1234-123456789012"
  register: result
"""

RETURN = r"""
response:
    description:
        - The path where the image file has been downloaded on the Ansible
          controller host.
        - Populated on a successful download.
    type: dict
    returned: always
    sample:
        {
            "path": "/tmp/tmpabc123/image_file.qcow2"
        }
ext_id:
    description:
        - The external ID of the image that was downloaded.
    type: str
    returned: always
    sample: "12345678-1234-1234-1234-123456789012"
changed:
    description:
        - Indicates whether the download action was performed.
        - Always C(True) after a real (non check_mode) download because a new
          file is written to disk.
    type: bool
    returned: always
    sample: true
msg:
    description:
        - This indicates the message if any message occurred.
        - Populated on error or in check_mode.
    type: str
    returned: When there is an error or in check_mode operation
    sample: "Api Exception raised while downloading image"
error:
    description: The error message if an error occurred.
    type: str
    returned: When an error occurs
failed:
    description: Indicates whether the module execution failed.
    type: bool
    returned: always
    sample: false
"""

import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.utils import raise_api_exception  # noqa: E402
from ..module_utils.v4.vmm.api_client import get_image_api_instance  # noqa: E402

SDK_IMP_ERROR = None

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        image_ext_id=dict(type="str", required=True),
    )
    return module_args


def download_image(module, api_instance, result):
    image_ext_id = module.params.get("image_ext_id")
    result["ext_id"] = image_ext_id

    if module.check_mode:
        result["msg"] = "Image with ext_id:{0} will be downloaded.".format(image_ext_id)
        return

    try:
        resp = api_instance.get_file_by_image_id(imageExtId=image_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while downloading image",
        )

    path = resp.to_dict().get("data", {}).get("path")
    result["response"] = {
        "path": path,
    }
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "response": None,
        "ext_id": None,
        "changed": False,
    }
    api_instance = get_image_api_instance(module)
    download_image(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
