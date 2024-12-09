#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_serial_port_info_v2
short_description: Fetch information about Nutanix VM's serial ports
description:
  - This module fetches information about Nutanix VM's serial ports.
  - The module can fetch information about all serial ports or a specific serial ports.
version_added: "2.0.0"
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    ext_id:
        description:
        - The external ID of the serial port.
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
- name: Fetch information about all serial ports of a vm
  ntnx_vms_serial_port_info_v2:
        nutanix_host: "{{ ip }}"
        nutanix_username: "{{ username }}"
        nutanix_password: "{{ password }}"
        validate_certs: false
        vm_ext_id: 00000-00000-000000-000000

- name: Fetch information about a specific serial port
  ntnx_vms_serial_port_info_v2:
        nutanix_host: "{{ ip }}"
        nutanix_username: "{{ username }}"
        nutanix_password: "{{ password }}"
        validate_certs: false
        vm_ext_id: 00000-00000-000000-000000
        ext_id: 00000-00000-000000-000000
"""


RETURN = r"""
response:
  description:
    - The response from the Nutanix PC serial ports v4 API.
    - it can be single serial port or list of serial ports as per spec.
  type: dict
  returned: always
  sample:
                {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "index": 0,
                "is_connected": true,
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
    sample: "00000-00000-000000-000000"
ext_id:
    description:
        - The external ID of the serial port when specific serial port is fetched.
    type: str
    returned: always
    sample: "00000-00000-000000-000000"
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        vm_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_serial_port(module, result):
    vmm = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")

    try:
        resp = vmm.get_serial_port_by_id(vmExtId=vm_ext_id, extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm serial port info",
        )

    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_serial_ports(module, result):
    vmm = get_vm_api_instance(module)
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vm serial ports info Spec", **result)

    try:
        resp = vmm.list_serial_ports_by_vm_id(vmExtId=vm_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm serial ports info",
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
    if module.params.get("ext_id"):
        get_serial_port(module, result)
    else:
        get_serial_ports(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
