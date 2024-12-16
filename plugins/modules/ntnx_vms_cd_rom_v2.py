#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Pradeepsingh Bhati
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vms_cd_rom_v2
short_description: Manage CDROM for Nutanix AHV VMs
version_added: "2.0.0"
description:
    - This module allows you to create and remove CDROM for Nutanix AHV VMs.
options:
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then the operation will be  create the CDROM.
            - If C(state) is set to C(absent) then the operation will be remove the CDROM.
        choices:
            - present
            - absent
        type: str
        default: present
    ext_id:
        description:
            - The external ID of the CDROM.
            - Required for deleting a disk.
        type: str
        required: false
    vm_ext_id:
        description:
            - The external ID of the VM.
        type: str
        required: true
    backing_info:
        description:
            - Storage provided by Nutanix ADSF
        type: dict
        suboptions:
            disk_size_bytes:
                description:
                    - The size of the CDROM in bytes.
                type: int
            storage_container:
                description:
                    - The storage container reference.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - The external ID of the storage container.
                        type: str
                        required: true
            storage_config:
                description:
                    - The storage configuration.
                type: dict
                suboptions:
                    is_flash_mode_enabled:
                        description:
                            - Indicates whether the virtual disk is pinned to the hot tier or not.
                        type: bool
            data_source:
                description:
                    - The data source for the disk.
                type: dict
                suboptions:
                    reference:
                        description:
                            - The reference to the data source.
                        type: dict
                        suboptions:
                            image_reference:
                                description:
                                    - The reference to an image.
                                    - Mutually exclusive with C(vm_disk_reference).
                                type: dict
                                suboptions:
                                    image_ext_id:
                                        description:
                                            - The external ID of the image.
                                        type: str
                            vm_disk_reference:
                                description:
                                    - The reference to a VM disk.
                                    - Mutually exclusive with C(image_reference).
                                type: dict
                                suboptions:
                                    disk_ext_id:
                                        description:
                                            - The external ID of the VM disk.
                                        type: str
                                    disk_address:
                                        description:
                                            - The address of the disk.
                                        type: dict
                                        suboptions:
                                            bus_type:
                                                description:
                                                    - The bus type of the disk.
                                                type: str
                                                choices:
                                                    - 'SCSI'
                                                    - 'IDE'
                                                    - 'PCI'
                                                    - 'SATA'
                                                    - 'SPAPR'
                                                required: true
                                            index:
                                                description:
                                                    - The index of the disk.
                                                type: int
                                    vm_reference:
                                        description:
                                            - The reference to the VM.
                                        type: dict
                                        suboptions:
                                            ext_id:
                                                description:
                                                    - The external ID of the VM.
                                                type: str
                                                required: true
    disk_address:
        description:
            - The address of the CDROM.
        type: dict
        suboptions:
            bus_type:
                description:
                    - Bus type for the device
                type: str
                choices:
                    - 'IDE'
                    - 'SATA'
                required: false
            index:
                description:
                    - Device index on the bus.
                    - This field is ignored unless the bus details are specified.
                type: int
    wait:
        description:
            - Whether to wait for the task to complete.
        type: bool
        default: true
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
- name: Create a empty CD ROM for a VM
  nutanix.ncp.ntnx_vms_cd_rom_v2:
    state: "present"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "521ab899-2398-4a23-62cb-8cd5e46ee5d2"
    disk_address:
      bus_type: "IDE"
    wait: true

- name: Remove CD ROM from VM
  ntnx_vms_cd_rom_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd6"
    ext_id: "e1651169-f9df-4785-bdff-7a94b1cf04e0"
    state: absent
    wait: true
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix v4 API.
        - It will give prism central task details.
    type: dict
    returned: always
    sample: {
            "cluster_ext_ids": [
                "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2024-04-27T14:24:07.561731+00:00",
            "completion_details": null,
            "created_time": "2024-04-27T14:24:06.695534+00:00",
            "entities_affected": [
                {
                    "ext_id": "521ab899-2398-4a23-62cb-8cd5e46ee5d2",
                    "rel": "vmm:ahv:vm"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:d0eba95b-5ac1-5564-9be7-7137a82214ab",
            "is_cancelable": false,
            "last_updated_time": "2024-04-27T14:24:07.561730+00:00",
            "legacy_error_message": null,
            "operation": "CreateCdRom",
            "operation_description": null,
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2024-04-27T14:24:06.706222+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:82c22bf6-ca1f-5358-a13f-ec4e3c6fa077",
                    "href": "https://*****:9440/api/prism/v4.0.b1/config/tasks/ZXJnb24=:82c22bf6-ca1f-5358-a13f-ec4e3c6fa077",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }
error:
    description: The error message if an error occurred.
    type: str
    returned: on error
changed:
    description: Whether the state of the VM has changed.
    type: bool
    returned: always
    sample: true
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
vm_ext_id:
    description: The external ID of the vm.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
ext_id:
    description:
        - The external ID of the CD ROM.
        - It won't be returned during create due to know issue.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    wait_for_completion,
    wait_for_entity_ext_id_in_task,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_cd_rom, get_vm  # noqa: E402
from ..module_utils.v4.vmm.spec.vms import VmSpecs as vm_specs  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=False),
        vm_ext_id=dict(type="str", required=True),
    )
    module_args.update(vm_specs.get_cd_rom_spec())
    return module_args


def create_cd_rom(module, result):
    vms = get_vm_api_instance(module)
    vm_ext_id = module.params["vm_ext_id"]
    result["vm_ext_id"] = vm_ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.AhvConfigCdRom()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create vm cd rom Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # get etag of vm current state
    vm = get_vm(module, vms, vm_ext_id)
    etag = get_etag(vm)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.create_cd_rom(vmExtId=vm_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating vm cd rom",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id, err = wait_for_entity_ext_id_in_task(
            module, task_ext_id, rel=TASK_CONSTANTS.RelEntityType.CD_ROM
        )
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed to get external ID of CD ROM from task", **result
            )
        if ext_id:
            resp = get_cd_rom(module, vms, ext_id, vm_ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_cd_rom(module, result):
    vms = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    vm = get_vm(module, vms, vm_ext_id)
    etag = get_etag(vm)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.delete_cd_rom_by_id(vmExtId=vm_ext_id, extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting vm cd rom",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
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
        "ext_id": None,
        "vm_ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        create_cd_rom(module, result)
    else:
        delete_cd_rom(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
