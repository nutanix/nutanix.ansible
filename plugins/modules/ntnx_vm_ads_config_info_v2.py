#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_ads_config_info_v2
short_description: Fetch ADS configuration of a VM
version_added: "2.7.0"
description:
    - This module allows you to fetch ADS configuration of a VM in Nutanix Prism Central.
    - Fetch ADS configuration for the specified VM using the VM external ID.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get the ADS configuration of a Virtual Machine) -
      Required Roles: Account Owner, Administrator, Backup Admin, Consumer, CSI System, Developer,
      Disaster Recovery Admin, Disaster Recovery Viewer, Flow Admin, Flow Policy Author, Flow Viewer,
      NCM Connector, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Project Manager,
      Self-Service Admin (Deprecated), Storage Admin, Super Admin, Tenant Admin, Tenant Consumer, User,
      Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    vm_ext_id:
        description:
            - A globally unique identifier of a VM of type UUID.
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
- name: Get ADS config of a VM
  nutanix.ncp.ntnx_vm_ads_config_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "00000000-0000-0000-0000-000000000001"
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix VM ADS config info v4 API.
        - ADS configuration of the VM.
    returned: always
    type: dict
    sample:
        {
            "auto_migration": "INCLUDE",
            "ext_id": "00000000-0000-0000-0000-000000000001",
            "links": null,
            "tenant_id": null
        }
changed:
    description: This indicates whether the task resulted in any changes. Always false for info modules.
    returned: always
    type: bool
    sample: false
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    returned: when an error occurs
    type: str
failed:
    description: This indicates whether the task failed.
    returned: always
    type: bool
    sample: false
ext_id:
    description: The external ID of the VM
    returned: when VM external ID is provided
    type: str
    sample: "00000000-0000-0000-0000-000000000001"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm_ads_config  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vm_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_vm_ads_config_info(module, api_instance, result):
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = vm_ext_id
    ads_config = get_vm_ads_config(module, api_instance, vm_ext_id)
    result["response"] = strip_internal_attributes(ads_config.to_dict())


def run_module():
    module = BaseInfoModule(
        skip_info_args=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vm_api_instance(module)
    get_vm_ads_config_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
