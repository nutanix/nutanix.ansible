#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_saml_sp_metadata_info_v2
short_description: Get SAML SP metadata
version_added: 2.7.0
description:
    - Retrieve the generic SAML service provider (SP) metadata for Prism Central.
    - The metadata is returned as a C(text/xml) document.
    - The module saves the downloaded metadata to a local file.
    - The local file path is returned in C(response.path).
    - This module does not require a SAML identity provider external ID.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(View SP Metadata For SAML IdP) -
      Required Roles: Nutanix Central Admin, Super Admin, Tenant Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
    dest:
        description:
            - Local destination file path where the downloaded SAML SP metadata should be saved.
            - The parent directory is created if it does not already exist.
            - If not provided, the metadata is saved to a temporary file and that path is returned.
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
- name: Get SAML SP metadata
  nutanix.ncp.ntnx_saml_sp_metadata_info_v2:
  register: result

- name: Get SAML SP metadata to a specific destination path
  nutanix.ncp.ntnx_saml_sp_metadata_info_v2:
    dest: "/tmp/saml_sp_metadata.xml"
  register: result
"""

RETURN = r"""
response:
    description: A dict containing local path of downloaded SAML SP metadata file.
    type: dict
    returned: always
    sample:
        {
            "path": "/tmp/saml_sp_metadata.xml"
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false

msg:
    description: Message returned when an error occurs or in check mode.
    returned: When there is an error or in check mode
    type: str
    sample: "Failed to determine the downloaded SAML SP metadata content"

failed:
    description: This field indicates whether the task failed.
    returned: always
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_identity_provider_api_instance,
)
from ..module_utils.v4.iam.helpers import get_saml_sp_metadata  # noqa: E402
from ..module_utils.v4.utils import save_bytes_to_file  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        dest=dict(type="path"),
    )
    return module_args


def get_saml_sp_metadata_info(module, identity_providers_api, result):
    dest = module.params.get("dest")

    if module.check_mode:
        if dest:
            result["msg"] = (
                "SAML SP metadata will be downloaded to destination path:{0}".format(
                    dest
                )
            )
            result["response"] = {"path": dest}
        else:
            result["msg"] = "SAML SP metadata will be downloaded."
        return

    resp = get_saml_sp_metadata(module, identity_providers_api)
    save_bytes_to_file(
        module,
        resp.data,
        dest,
        result,
        fail_msg="Failed to determine the downloaded SAML SP metadata content",
        temp_prefix="saml_sp_metadata_",
        temp_suffix=".xml",
    )


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    identity_providers_api = get_identity_provider_api_instance(module)
    get_saml_sp_metadata_info(module, identity_providers_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
