#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_flow_controller_config_info_v2
short_description: Get Flow Controller configuration
version_added: "2.7.0"
description:
    - Returns the current Flow Controller configuration.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Flow Controller configuration) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin, Prism Viewer
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
"""

RETURN = r"""
response:
    description:
        - The Flow Controller configuration.
    type: dict
    returned: always
    sample:
        {
            "capabilities": {
                "containers": {
                    "is_enabled": false,
                    "scale": null
                },
                "network_security_app_centric": {
                    "is_enabled": true,
                    "scale": {
                        "address_group_count": 50,
                        "entity_group_count": 20,
                        "security_policy_count": 100,
                        "service_group_count": 50
                    }
                },
                "network_security_rule_centric": {
                    "is_enabled": false,
                    "scale": null
                },
                "security_analytics": {
                    "is_enabled": false,
                    "scale": null
                },
                "virtual_networking": {
                    "is_enabled": true,
                    "scale": {
                        "gateway_node_count": 2,
                        "load_balancer_count": 5,
                        "vpc_count": 10
                    }
                },
                "vlan_networking": {
                    "is_enabled": true
                }
            },
            "required_resources": [
                {
                    "cpu": 4,
                    "deployment_mode": "SMALL",
                    "disk_mib": 102400,
                    "memory_mib": 8192
                }
            ],
            "subnet_count": 500,
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
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_flow_controller_config_api_instance,
)
from ..module_utils.v4.network.helpers import get_flow_controller_config  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

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
