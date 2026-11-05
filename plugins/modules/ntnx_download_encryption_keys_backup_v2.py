#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_download_encryption_keys_backup_v2
short_description: Download the encryption keys backup for cluster(s) in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module downloads the encryption key backup for the cluster(s) in Nutanix Prism Central.
  - This is an action module that retrieves the previously prepared encryption keys backup.
  - The backup must first be prepared using M(nutanix.ncp.ntnx_prepare_encryption_keys_backup_v2).
  - This module uses PC v4 APIs based SDKs.
notes:
  - This module talks to Prism Central (PC).
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View Encryption Keys Backup) -
    Required Roles: Prism Admin, Security Admin, Super Admin.
  - >-
    The C(ext_id) is the ID of the encryption key backup, which can be fetched as part of the
    prepare encryption keys backup task response.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - ID of the encryption key backup.
      - This ID can be fetched as part of the encryption task response from
        M(nutanix.ncp.ntnx_prepare_encryption_keys_backup_v2).
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
- name: Download encryption keys backup
  nutanix.ncp.ntnx_download_encryption_keys_backup_v2:
    ext_id: "3f8a6d2c-1b4e-4c7a-9d5e-2a1b3c4d5e6f"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for downloading the encryption keys backup.
    - Contains the downloaded encryption keys backup content.
  returned: always
  type: dict
  sample:
    {
      "value": "<base64-encoded-encryption-keys-backup-content>"
    }

ext_id:
  description:
    - The external ID of the encryption key backup that was downloaded.
  returned: always
  type: str
  sample: "3f8a6d2c-1b4e-4c7a-9d5e-2a1b3c4d5e6f"

changed:
  description: This indicates whether the action resulted in any changes. Downloading does not change cluster state.
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the status/error message if any occurred.
  returned: When there is an error or in check mode.
  type: str
  sample: "Encryption keys backup with ext_id: 3f8a6d2c-1b4e-4c7a-9d5e-2a1b3c4d5e6f will be downloaded."
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_encryption_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    download_encryption_keys_backup as download_encryption_keys_backup_helper,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def download_encryption_keys_backup(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Encryption keys backup with ext_id: {0} will be downloaded.".format(ext_id)
        )
        return

    resp = download_encryption_keys_backup_helper(module, api_instance, ext_id)
    data = resp.data
    if hasattr(data, "to_dict"):
        result["response"] = strip_internal_attributes(data.to_dict())
    else:
        result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        skip_info_args=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_encryption_api_instance(module)
    download_encryption_keys_backup(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
