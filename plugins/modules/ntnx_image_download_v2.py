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
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Download an image) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    image_ext_id:
        description:
            - The external identifier of an image.
        type: str
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
- name: Download an image
  nutanix.ncp.ntnx_image_download_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    image_ext_id: "12345678-1234-1234-1234-123456789012"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for downloading an image.
        - Contains the local path where the SDK persisted the downloaded file.
    type: dict
    returned: always
    sample:
        {
            "path": "/tmp/tmpabc123/image_file.qcow2"
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

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.utils import raise_api_exception  # noqa: E402
from ..module_utils.v4.vmm.api_client import get_image_api_instance  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client  # noqa: E402, F401  # pylint: disable=unused-import
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        image_ext_id=dict(type="str", required=True),
    )
    return module_args


def download_image(module, result, api_instance):
    image_ext_id = module.params.get("image_ext_id")
    result["ext_id"] = image_ext_id

    if module.check_mode:
        result["msg"] = "Image with ext_id:{0} will be downloaded.".format(image_ext_id)
        return

    resp = None
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
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
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
