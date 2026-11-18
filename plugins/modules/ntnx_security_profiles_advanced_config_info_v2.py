#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_profiles_advanced_config_info_v2
short_description: Fetch advanced configs for a security profile
version_added: "2.7.0"
description:
    - Fetch advanced configs for a cluster security profile in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(View Security Profile Advanced Config) -
      Required Roles: Prism Admin, Prism Viewer, Security Dashboard Admin, Security Dashboard Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
    security_profile_ext_id:
        description:
            - External ID of the security profile.
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
- name: Fetch advanced config for a security profile
  nutanix.ncp.ntnx_security_profiles_advanced_config_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    security_profile_ext_id: "64eae63e-d671-483f-a8bf-e55e426a7168"
  register: result
"""

RETURN = r"""
response:
    description:
        - The advanced configuration for the security profile.
    type: dict
    returned: always
    sample:
        {
            "consent_banner_text": "",
            "is_consent_banner_enabled": false,
            "kernel_space_core_dump_level": "OFF",
            "user_space_core_dump_level": "OFF"
        }
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: false
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: >-
      Api Exception raised while fetching advanced config using security profile external ID
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_security_profiles_api_instance,
)
from ..module_utils.v4.security.helpers import (  # noqa: E402
    get_advanced_config_by_security_profile_ext_id,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        security_profile_ext_id=dict(type="str", required=True),
    )
    return module_args


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
    }
    api_instance = get_security_profiles_api_instance(module)
    resp = get_advanced_config_by_security_profile_ext_id(
        module, api_instance, module.params.get("security_profile_ext_id")
    )
    result["response"] = strip_internal_attributes(resp.to_dict())
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
