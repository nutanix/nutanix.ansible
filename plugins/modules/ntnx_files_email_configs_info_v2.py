#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_email_configs_info_v2
short_description: Fetch the email configuration of a file server in Nutanix Files
version_added: 2.7.0
description:
  - This module allows you to fetch information about the EmailConfig of a file server in Nutanix Prism Central.
  - The email configuration is a single (singleton) template per file server, identified by C(file_server_ext_id).
  - It fetches the email configuration used by the quota-notification workflow for the given file server.
  - This module uses PC v4 APIs based SDKs.
options:
  file_server_ext_id:
    description:
      - The external identifier of the file server whose email configuration is fetched.
      - The external ID of the file server can be fetched from Nutanix Prism Central.
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
- name: Fetch email configuration of a file server
  nutanix.ncp.ntnx_files_email_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "1f4f80e2-2b1f-4f9a-8d3c-1a2b3c4d5e6f"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC EmailConfig info v4 API.
    - It returns the email configuration of the file server identified by C(file_server_ext_id).
  returned: always
  type: dict
  sample:
    {
      "content": "You have exceeded the storage quota configured for your share. Please free up space.",
      "ext_id": "1f4f80e2-2b1f-4f9a-8d3c-1a2b3c4d5e6f",
      "links": null,
      "subject": "Quota notification for your file server share",
      "tenant_id": null
    }

ext_id:
  description: The external ID of the email configuration.
  returned: when the email configuration is fetched
  type: str
  sample: "1f4f80e2-2b1f-4f9a-8d3c-1a2b3c4d5e6f"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching email configuration for file server"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_quota_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_email_config  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_email_config_with_file_server_ext_id(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    resp = get_email_config(module, api_instance, file_server_ext_id)
    result["ext_id"] = resp.ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_quota_policies_api_instance(module)
    get_email_config_with_file_server_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
