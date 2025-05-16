#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_cd_rom_info_v2
short_description: Fetch information about Nutanix VM's CD ROM
description:
  - This module fetches information about Nutanix VM's CD ROM.
  - The module can fetch information about all CD ROMs or a specific CD ROM.
  - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    ext_id:
        description:
        - The external ID of the CD ROM.
        type: str
        required: false
    vm_ext_id:
        description:
        - The external ID of the vm.
        type: str
        required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
- name: Fetch information about all CD ROMs of a vm
  nutanix.ncp.ntnx_vms_cd_rom_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: 530567f3-abda-4913-b5d0-0ab6758ec16e

- name: Fetch information about a specific CD ROM
  nutanix.ncp.ntnx_vms_cd_rom_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: 530567f3-abda-4913-b5d0-0ab6758ec16e
    ext_id: 530567f3-abda-4913-b5d0-0ab6758ec1653
"""


RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Disks v4 API.
    - it can be single CD ROM or list of CD ROM as per spec.
  type: dict
  returned: always
  sample: {
            "backing_info": {
                "data_source": {
                    "reference": {
                        "image_ext_id": "b988b5ae-da2d-424c-8530-51529a0efb52"
                    }
                },
                "disk_ext_id": "e1651169-f9df-4785-bdff-7a94b1cf04e0",
                "disk_size_bytes": 48695296,
                "is_migration_in_progress": false,
                "storage_config": null,
                "storage_container": {
                    "ext_id": "ab76422d-d587-46aa-b25a-b005acdcd896"
                }
            },
            "disk_address": {
                "bus_type": "IDE",
                "index": 0
            },
            "ext_id": "e1651169-f9df-4785-bdff-7a94b1cf04e0",
            "iso_type": "OTHER",
            "links": null,
            "tenant_id": null
        }
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
vm_ext_id:
    description: The external ID of the vm.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
ext_id:
    description:
        - The external ID of the CD ROM when specific is fetched.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_cd_rom  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        vm_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_cd_rom_by_ext_id(module, vms, result):
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    resp = get_cd_rom(module, vms, ext_id, vm_ext_id)
    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_cd_roms(module, vms, result):
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vm cd roms info Spec", **result)

    try:
        resp = vms.list_cd_roms_by_vm_id(vmExtId=vm_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm cd roms info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    vms = get_vm_api_instance(module)
    if module.params.get("ext_id"):
        get_cd_rom_by_ext_id(module, vms, result)
    else:
        get_cd_roms(module, vms, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
