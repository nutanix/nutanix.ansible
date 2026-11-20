#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_iam_system_config_info_v2
short_description: Fetch system configurations in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Retrieve system configurations from Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs.
options:
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
- name: Fetch system configurations
  nutanix.ncp.ntnx_iam_system_config_info_v2:
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - The response from fetching system configurations.
        - Returns the system configuration details.
    returned: always
    type: dict
    sample:
        {
            "last_updated_time": "2026-07-21T06:36:56.065999+00:00",
            "name_value_pair": [
                {
                    "name": "sample_config_key",
                    "value": "sample_config_value"
                }
            ]
        }
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false
failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching system configuration"
error:
    description: This indicates the error message if any error occurred
    returned: When an error occurs
    type: str
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_system_config_api_instance,
)
from ..module_utils.v4.iam.helpers import get_system_config  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    return dict()


def fetch_system_config(module, api_instance, result):
    resp = get_system_config(module, api_instance)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_system_config_api_instance(module)
    fetch_system_config(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
