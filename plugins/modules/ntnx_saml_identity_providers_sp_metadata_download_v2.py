#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_saml_identity_providers_sp_metadata_download_v2
short_description: Download SAML IdP SP metadata
version_added: 2.7.0
description:
    - Download SAML service provider (SP) metadata for a configured SAML identity provider.
    - The identity provider is selected using its external identifier.
    - The metadata is returned as a C(text/xml) document.
    - The module saves the downloaded metadata to a local file.
    - The local file path is returned in C(response.path).
    - The generated metadata reflects the selected identity provider's configuration, including its redirect URL and signing settings.
    - This module requires the external identifier of an existing SAML identity provider.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get SAML IdP SP Metadata) -
      Required Roles: Nutanix Central Admin, Super Admin, Tenant Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
    ext_id:
        description: External ID of the SAML identity provider whose SP metadata should be downloaded.
        type: str
        required: true
    dest:
        description:
            - Local destination file path where the downloaded SAML IdP SP metadata should be saved.
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
- name: Download SAML IdP SP metadata
  nutanix.ncp.ntnx_saml_identity_providers_sp_metadata_download_v2:
    ext_id: "18bb7b89-b297-44dc-abb6-b478c3276e82"
  register: result

- name: Download SAML IdP SP metadata to a specific destination path
  nutanix.ncp.ntnx_saml_identity_providers_sp_metadata_download_v2:
    ext_id: "18bb7b89-b297-44dc-abb6-b478c3276e82"
    dest: "/tmp/saml_idp_sp_metadata.xml"
  register: result
"""

RETURN = r"""
response:
    description: A dict containing local path of downloaded SAML IdP SP metadata file.
    type: dict
    returned: always
    sample:
        {
            "path": "/tmp/saml_idp_sp_metadata.xml"
        }

ext_id:
    description: External ID of the SAML identity provider.
    returned: always
    type: str
    sample: "18bb7b89-b297-44dc-abb6-b478c3276e82"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false

msg:
    description: Message returned when an error occurs or in check mode.
    returned: When there is an error or in check mode
    type: str
    sample: "Api Exception raised while downloading SAML IdP SP metadata"

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
import tempfile  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_identity_provider_api_instance,
)
from ..module_utils.v4.iam.helpers import get_saml_idp_sp_metadata  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        dest=dict(type="path"),
    )
    return module_args


def _normalize_metadata_content(data):
    if isinstance(data, dict):
        return None, data.get("path")
    if hasattr(data, "path") and getattr(data, "path", None) is not None:
        return None, getattr(data, "path")
    if isinstance(data, (bytes, bytearray)):
        return bytes(data), None
    if isinstance(data, str):
        return data.encode("utf-8"), None
    return None, None


def _save_metadata(module, data, dest, result):
    content, downloaded_path = _normalize_metadata_content(data)

    if downloaded_path:
        downloaded_path = str(downloaded_path)
        if dest and os.path.abspath(downloaded_path) != os.path.abspath(dest):
            dest_dir = os.path.dirname(os.path.abspath(dest))
            if dest_dir and not os.path.isdir(dest_dir):
                os.makedirs(dest_dir)
            shutil.move(downloaded_path, dest)
            downloaded_path = dest
        result["response"] = {"path": downloaded_path}
        return

    if content is None:
        module.fail_json(
            msg="Failed to determine the downloaded SAML IdP SP metadata content",
            **result,
        )

    if dest:
        dest_dir = os.path.dirname(os.path.abspath(dest))
        if dest_dir and not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        with open(dest, "wb") as f:
            f.write(content)
        result["response"] = {"path": dest}
        return

    fd, temp_path = tempfile.mkstemp(suffix=".xml", prefix="saml_idp_sp_metadata_")
    with os.fdopen(fd, "wb") as f:
        f.write(content)
    result["response"] = {"path": temp_path}


def download_saml_idp_sp_metadata(module, identity_providers_api, result):
    ext_id = module.params.get("ext_id")
    dest = module.params.get("dest")
    result["ext_id"] = ext_id

    if module.check_mode:
        if dest:
            result["msg"] = (
                "SAML IdP SP metadata for identity provider with ext_id:{0} "
                "will be downloaded to destination path:{1}".format(ext_id, dest)
            )
            result["response"] = {"path": dest}
        else:
            result["msg"] = (
                "SAML IdP SP metadata for identity provider with ext_id:{0} "
                "will be downloaded.".format(ext_id)
            )
        return

    resp = get_saml_idp_sp_metadata(module, identity_providers_api, ext_id)
    _save_metadata(module, resp.data, dest, result)


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None, "ext_id": None}
    identity_providers_api = get_identity_provider_api_instance(module)
    download_saml_idp_sp_metadata(module, identity_providers_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
