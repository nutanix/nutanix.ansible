#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_gpus_info_v2
short_description: Fetches GPU(s) information attached to VM in a Nutanix prism central.
description:
  - This module fetches GPU(s) information attached to a virtual machine in a Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - External ID of the GPU.
      - It can be used to get specific GPU info.
    required: false
    type: str
  vm_ext_id:
    description:
      - External ID of the virtual machine.
    required: true
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
author:
  - George Ghawali (@george-ghawali)

"""

EXAMPLES = r"""
- name: Fetch GPU information by GPU external ID and VM external ID
  nutanix.ncp.ntnx_gpus_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "d7db5aa1-34cc-4f96-a436-eb2d85c7ff9e"
    vm_ext_id: "9a1aa5ca-20ff-4703-672a-f41ad0a401b9"
  register: result

- name: Fetch all GPUs attached to a VM
  nutanix.ncp.ntnx_gpus_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "9a1aa5ca-20ff-4703-672a-f41ad0a401b9"
  register: result

- name: Fetch all GPUs attached to a VM using filter
  nutanix.ncp.ntnx_gpus_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "mode eq 'PASSTHROUGH_COMPUTE'"
    vm_ext_id: "9a1aa5ca-20ff-4703-672a-f41ad0a401b9"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for fetching GPU(s) information.
    - Returns GPU information if GPU external ID and VM external ID are provided.
    - Returns list of multiple GPUs information if only VM external ID is provided.
  type: dict
  returned: always
  sample:
    {
      "device_id": 5053,
      "ext_id": "ca1f8f73-88f2-4ded-879e-da623c374bd4",
      "fraction": 0,
      "frame_buffer_size_bytes": 0,
      "guest_driver_version": null,
      "links": null,
      "mode": "PASSTHROUGH_GRAPHICS",
      "name": "Tesla_M10",
      "num_virtual_display_heads": 0,
      "pci_address": { "bus": 8, "device": 0, "func": 0, "segment": 0 },
      "tenant_id": null,
      "vendor": "NVIDIA",
    }
ext_id:
  description: The external ID of the GPU.
  type: str
  returned: always
changed:
  description: Indicates whether the state of the GPU has changed.
  type: bool
  returned: always
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching GPUs list using VM external ID"
error:
  description: The error message, if any.
  type: str
  returned: always
failed:
  description: Indicates whether the task failed.
  type: bool
  returned: always
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_gpu  # noqa: E402


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        vm_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_gpu_by_ext_id(module, gpus, result):
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    resp = get_gpu(module, gpus, ext_id, vm_ext_id)
    result["ext_id"] = module.params.get("ext_id")
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_gpus(module, gpus, result):
    sg = SpecGenerator(module=module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating GPUs list Spec", **result)

    try:
        resp = gpus.list_gpus_by_vm_id(vmExtId=module.params.get("vm_ext_id"), **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching GPUs list using VM external ID",
        )

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


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
    gpus = get_vm_api_instance(module)
    if module.params.get("ext_id"):
        get_gpu_by_ext_id(module, gpus, result)
    else:
        get_gpus(module, gpus, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
