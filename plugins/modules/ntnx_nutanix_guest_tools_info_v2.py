#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_nutanix_guest_tools_info_v2
short_description: Fetch Nutanix Guest Tools (NGT) configuration for an ESXi VM
version_added: 2.5.0
description:
  - This module allows you to fetch information about NutanixGuestTool in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific NutanixGuestTool configuration for an ESXi-hosted VM.
  - The v4 SDK does not expose a "list all NGT configs" endpoint - NGT is always
    scoped to a single VM - so C(ext_id) is required.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get VM NGT configuration) -
    Required Roles: Backup Admin, Consumer, Developer, NCM Connector, Network Infra Admin, Operator, Prism Admin,
    Prism Viewer, Project Admin, Project Manager, Storage Admin, Super Admin, Virtual Machine Admin,
    Virtual Machine Operator, Virtual Machine Viewer, VPC Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external ID of the ESXi-hosted VM whose NGT configuration is being queried.
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
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get NGT config for a single ESXi-hosted VM
  nutanix.ncp.ntnx_nutanix_guest_tools_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC NutanixGuestTool info v4 API.
    - It is a single NutanixGuestTool configuration for the VM identified by C(ext_id).
    - The NGT list endpoint is intentionally unsupported by the SDK, so this
      module always returns a single dict.
  returned: always
  type: dict
  sample:
    {
      "available_version": "4.1",
      "capabilities": [
        "SELF_SERVICE_RESTORE"
      ],
      "guest_info": null,
      "guest_os_version": "linux:64:CentOS Linux-7.9",
      "is_enabled": true,
      "is_installed": true,
      "is_iso_inserted": false,
      "is_reachable": true,
      "is_vm_mobility_drivers_installed": null,
      "is_vss_snapshot_capable": true,
      "version": "4.1"
    }

changed:
  description: Always false for the info module.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the VM whose NGT config was fetched.
  returned: when ext_id is provided
  type: str
  sample: "98b9dc89-be08-3c56-b554-692b8b676fd1"

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching Nutanix Guest Tools info for given ESXi VM"

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
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402
from ..module_utils.v4.vmm.api_client import get_esxi_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_esxi_ngt_status  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_nutanix_guest_tools_by_vm_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    status = get_esxi_ngt_status(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(status.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False, "ext_id": None}
    api_instance = get_esxi_vm_api_instance(module)
    get_nutanix_guest_tools_by_vm_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
