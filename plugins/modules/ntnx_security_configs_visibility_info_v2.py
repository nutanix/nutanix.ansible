#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_configs_visibility_info_v2
short_description: Fetch the security configurations visibility setting
version_added: "2.7.0"
description:
    - Fetch the list of security configurations settings being displayed on the Prism Central dashboard.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(View Security Config Visibility Setting) -
      Required Roles: Prism Admin, Prism Viewer, Security Dashboard Admin, Security Dashboard Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
    select:
        description:
            - A URL query parameter that allows clients to request a specific set of properties.
            - The following selection keys are supported
              C(isClusterLockdownVisible), C(isConsentBannerVisible), C(isLogForwardingVisible),
              C(isNetworkSegmentationVisible), C(isSecureBootVisible), C(isSecurityProfileVisible).
        type: str
        required: false
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
- name: Fetch security configurations visibility setting
  nutanix.ncp.ntnx_security_configs_visibility_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Fetch selected visibility fields
  nutanix.ncp.ntnx_security_configs_visibility_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    select: "isSecureBootVisible,isClusterLockdownVisible"
  register: result
"""

RETURN = r"""
response:
    description:
        - The security configurations visibility setting from Prism Central.
    type: dict
    returned: always
    sample:
        {
            "is_cluster_lockdown_visible": true,
            "is_consent_banner_visible": false,
            "is_log_forwarding_visible": false,
            "is_network_segmentation_visible": true,
            "is_secure_boot_visible": true,
            "is_security_profile_visible": false
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
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_security_configs_visibility_api_instance,
)
from ..module_utils.v4.security.helpers import (  # noqa: E402
    get_security_configs_visibility_setting,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        select=dict(type="str"),
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
    api_instance = get_security_configs_visibility_api_instance(module)
    resp = get_security_configs_visibility_setting(
        module, api_instance, select=module.params.get("select")
    )
    result["response"] = strip_internal_attributes(resp.to_dict())
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
