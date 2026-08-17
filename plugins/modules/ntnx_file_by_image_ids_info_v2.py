#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_file_by_image_ids_info_v2
short_description: Fetch image file information for a Nutanix Prism Central image
version_added: 2.5.0
description:
    - This module allows you to fetch information about the file associated
      with a Nutanix Prism Central image (the C(FileByImageId) resource in
      C(virtual_machine_management)).
    - Wraps the VMM v4.2 C(GetFileByImageId) API
      (C(GET /api/vmm/v4.2/content/images/{imageExtId}/file)).
    - The v4.2 SDK returns the downloaded file path as the response C(data)
      for a given image; this module surfaces that path as informational
      output without setting C(changed=True).
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get file by image ext_id) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - The external ID of the image whose file information should be
              fetched.
            - Required to fetch file information for a specific image.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get file information for an image using ext_id
  nutanix.ncp.ntnx_file_by_image_ids_info_v2:
    ext_id: "12345678-1234-1234-1234-123456789012"
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC C(GetFileByImageId) v4 API for the
          given image external ID.
        - Contains the local C(path) at which the SDK persisted the streamed
          file bytes.
    type: dict
    returned: always
    sample:
        {
            "path": "/tmp/tmpabc123/image_file.qcow2"
        }
ext_id:
    description:
        - The external ID of the image whose file information was fetched.
    type: str
    returned: always
    sample: "12345678-1234-1234-1234-123456789012"
changed:
    description:
        - This indicates whether the task resulted in any changes.
        - Always C(False) for an info module.
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching image file info"
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
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import raise_api_exception  # noqa: E402
from ..module_utils.v4.vmm.api_client import get_image_api_instance  # noqa: E402

SDK_IMP_ERROR = None

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_file_by_image_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    try:
        resp = api_instance.get_file_by_image_id(imageExtId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching image file info",
        )

    path = resp.to_dict().get("data", {}).get("path")
    result["response"] = {
        "path": path,
    }


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "ext_id": None}
    api_instance = get_image_api_instance(module)
    get_file_by_image_id(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
