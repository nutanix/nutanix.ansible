#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_domain_manager_size_config_info_v2
short_description: Fetch domain manager size config info
version_added: "2.7.0"
description:
    - This module allows you to fetch information about domain manager size config in Nutanix Prism Central.
    - Get the supported Domain Manager (Prism Central) sizes and their resource requirements.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get the supported Domain Manager (Prism Central) sizes and their resource requirements) -
      Required Roles: Cluster Admin, Cluster Viewer, Domain Manager Admin, Domain Manager Viewer, Internal Super Admin, NCM Connector, Prism Admin,
      Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
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
- name: Get domain manager size config
  nutanix.ncp.ntnx_domain_manager_size_config_info_v2:
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC domain manager size config info v4 API.
        - Singleton resource describing all supported Domain Manager (Prism Central) sizes and the resources required for each.
    returned: always
    type: dict
    sample:
        {
            "specs": [
                {
                    "data_disk_size_bytes": 536870912000,
                    "memory_size_bytes": 37580963840,
                    "num_vcpus": 10,
                    "scale_limits": {
                        "max_clusters": 100,
                        "max_hosts": 1000,
                        "max_vms": 5000
                    },
                    "size": "SMALL"
                },
                {
                    "data_disk_size_bytes": 1073741824000,
                    "memory_size_bytes": 75161927680,
                    "num_vcpus": 20,
                    "scale_limits": {
                        "max_clusters": 200,
                        "max_hosts": 2000,
                        "max_vms": 10000
                    },
                    "size": "LARGE"
                }
            ]
        }
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching domain manager size config info"
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: when an error occurs
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_domain_manager_size_config  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict()
    return module_args


def get_domain_manager_size_config_info(module, api_instance, result):
    resp = get_domain_manager_size_config(module, api_instance)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_domain_manager_api_instance(module)
    get_domain_manager_size_config_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
