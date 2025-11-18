#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_ngt_info_v2
short_description: Get Nutanix Guest Tools (NGT) current config for a virtual machine.
description:
    - This module retrieves Nutanix Guest Tools (NGT) current config for a virtual machine in a Nutanix cluster.
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    ext_id:
        description:
            - The external ID of the virtual machine for which to retrieve NGT information.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_logger
"""

EXAMPLES = r"""
- name: Get NGT info for a virtual machine
  nutanix.ncp.ntnx_vms_ngt_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
  register: result
"""

RETURN = r"""
response:
    description: The NGT information for the virtual machine.
    type: dict
    returned: always
    sample: {
            "available_version": "4.1",
            "capabilities": [
                "SELF_SERVICE_RESTORE"
            ],
            "guest_os_version": "linux:64:CentOS Linux-7.3.1611",
            "is_enabled": true,
            "is_installed": true,
            "is_iso_inserted": true,
            "is_reachable": true,
            "is_vm_mobility_drivers_installed": null,
            "is_vss_snapshot_capable": null,
            "version": "4.1"
        }
changed:
    description: Indicates whether the NGT information has changed.
    type: bool
    returned: always
error:
    description: The error message, if any.
    type: str
    returned: on error
ext_id:
    description: The external ID of the virtual machine.
    type: str
    returned: always
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(ext_id=dict(type="str", required=True))
    return module_args


def get_ngt_config(module, result):
    vmm = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    if not ext_id:
        return module.fail_json(msg="ext_id is required to install NGT", **result)

    result["ext_id"] = ext_id

    status = None
    try:
        status = vmm.get_guest_tools_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching NGT info for given vm",
        )

    result["response"] = strip_internal_attributes(status.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        skip_info_args=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    get_ngt_config(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
