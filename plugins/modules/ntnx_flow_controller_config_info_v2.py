#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_flow_controller_config_info_v2
short_description: Get Flow Controller configuration in Nutanix Prism Central
version_added: "2.7.0"
description:
    - This module allows you to fetch Flow Controller configuration in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Flow Controller Configuration) -
      Required Roles: Prism Viewer, Prism Admin, Super Admin, Network Infra Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options: {}
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get Flow Controller configuration
  nutanix.ncp.ntnx_flow_controller_config_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix Flow Controller config info v4 API.
        - It contains the Flow Controller configuration details.
    type: dict
    returned: always
    sample:
        {
            "capabilities": {
                "containers": {
                    "is_enabled": true,
                    "scale": {
                        "kubernetes_cluster_count": 5
                    }
                },
                "network_security_app_centric": {
                    "is_enabled": true,
                    "scale": {
                        "security_policy_count": 100
                    }
                },
                "network_security_rule_centric": {
                    "is_enabled": true,
                    "scale": {
                        "security_policy_count": 50
                    }
                },
                "security_analytics": {
                    "is_enabled": true,
                    "scale": {
                        "analytics_retention_days": 7,
                        "analytics_storage_gib": 100
                    }
                },
                "virtual_networking": {
                    "is_enabled": true,
                    "scale": {
                        "vpc_count": 20
                    }
                },
                "vlan_networking": {
                    "is_enabled": true
                }
            },
            "required_resources": [
                {
                    "cpu": 4,
                    "deployment_mode": "DEFAULT",
                    "disk_mib": 102400,
                    "memory_mib": 16384
                },
                {
                    "cpu": 8,
                    "deployment_mode": "HIGH_AVAILABILITY",
                    "disk_mib": 204800,
                    "memory_mib": 32768
                }
            ],
            "subnet_count": 200,
            "vm_count": 1000
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
    type: str
    returned: When there is an error
    sample: "Api Exception raised while fetching Flow Controller config info"
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: when an error occurs
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_flow_controller_config_api_instance,
)
from ..module_utils.v4.network.helpers import get_flow_controller_config  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict()
    return module_args


def get_flow_controller_config_info(module, result, api_instance):
    resp = get_flow_controller_config(module, api_instance)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    api_instance = get_flow_controller_config_api_instance(module)
    get_flow_controller_config_info(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
