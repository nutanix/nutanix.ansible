#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_gpus_v2
short_description: Module to attach/detach GPUs to/from VMs in Nutanix prism central.
description:
  - This module allows you to attach or detach GPUs to or from virtual machines in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - State of the GPU. Whether to attach or detach the GPU.
      - Present -> Attaches the GPU to the VM.
      - Absent -> Detaches the GPU from the VM.
    required: false
    type: str
    choices: ["present", "absent"]
  ext_id:
    description:
      - The external ID of the GPU.
      - Required for attaching or detaching a GPU.
    required: false
    type: str
  vm_ext_id:
    description:
      - The external ID of the virtual machine.
      - Required for attaching or detaching a GPU.
    required: true
    type: str
  mode:
    description:
      - The mode of the GPU.
    choices: ["PASSTHROUGH_GRAPHICS", "PASSTHROUGH_COMPUTE", "VIRTUAL"]
    required: false
    type: str
  device_id:
    description:
      - The ID of the GPU device.
    required: false
    type: int
  vendor:
    description:
      - The vendor of the GPU.
    choices: ["NVIDIA", "AMD", "INTEL"]
    required: false
    type: str
  wait:
    description:
      - Wait for the task to complete.
    type: bool
    required: false
    default: True
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Attach GPU to VM
  nutanix.ncp.ntnx_gpus_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "d7db5aa1-34cc-4f96-a436-eb2d85c7ff9e"
    vm_ext_id: "9a1aa5ca-20ff-4703-672a-f41ad0a401b9"
    name: test-gpu
    mode: VIRTUAL
    device_id: 123
    vendor: NVIDIA

- name: Detach GPU from VM
  nutanix.ncp.ntnx_gpus_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "d7db5aa1-34cc-4f96-a436-eb2d85c7ff9e"
    vm_ext_id: "9a1aa5ca-20ff-4703-672a-f41ad0a401b9"
    state: absent
    wait: true
"""

RETURN = r"""
response:
  description:
    - The response of the GPU operation.
    - It will have updated list of GPUs attached to the VM.
  type: dict
  returned: always
  sample:
      [
        {
          "device_id": 5053,
          "ext_id": "16bbf848-5926-46f2-857a-87d4825bd347",
          "fraction": null,
          "frame_buffer_size_bytes": null,
          "guest_driver_version": null,
          "links": null,
          "mode": "PASSTHROUGH_GRAPHICS",
          "name": null,
          "num_virtual_display_heads": null,
          "pci_address": null,
          "tenant_id": null,
          "vendor": "NVIDIA",
        },
      ]

task_ext_id:
  description: The external ID of the task.
  type: str
  returned: always
vm_ext_id:
  description: The external ID of the virtual machine.
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
  sample: "Failed generating attach GPU Spec"
error:
  description: The error message, if any.
  type: str
  returned: when an error occurs
"""

import traceback  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402)
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_gpu, get_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=False),
        vm_ext_id=dict(type="str", required=True),
        mode=dict(
            type="str",
            choices=["PASSTHROUGH_GRAPHICS", "PASSTHROUGH_COMPUTE", "VIRTUAL"],
            obj=vmm_sdk.GpuMode,
            required=False,
        ),
        device_id=dict(type="int", required=False),
        vendor=dict(
            type="str",
            choices=["NVIDIA", "INTEL", "AMD"],
            obj=vmm_sdk.GpuVendor,
            required=False,
        ),
    )
    return module_args


def attach_gpu(module, vms, result):
    vm_ext_id = module.params["vm_ext_id"]
    result["vm_ext_id"] = vm_ext_id
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.Gpu()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating attach GPU Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vm = get_vm(module, vms, vm_ext_id)
    etag = get_etag(vm)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.create_gpu(vmExtId=vm_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while attaching GPU",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id, True)
        resp = get_vm(module, vms, vm_ext_id)
        if not resp.gpus:
            return module.fail_json(
                "GPUs list is empty when fetching VM info", **result
            )
        result["response"] = strip_internal_attributes(resp.gpus.to_dict())
    result["changed"] = True


def detach_gpu(module, vms, result):
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    current_spec = get_gpu(module, vms, ext_id, vm_ext_id)
    result["vm_ext_id"] = vm_ext_id
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("unable to fetch etag for detaching GPU", **result)
    kwargs = {"if_match": etag}

    try:
        resp = vms.delete_gpu_by_id(vmExtId=vm_ext_id, extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while detaching GPU",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id, True)
        resp = get_vm(module, vms, vm_ext_id)
        if not resp.gpus:
            result["response"] = []
        else:
            result["response"] = strip_internal_attributes(resp.gpus.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_ext_id": None,
    }
    state = module.params["state"]
    vms = get_vm_api_instance(module)
    if state == "present":
        attach_gpu(module, vms, result)
    else:
        detach_gpu(module, vms, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
