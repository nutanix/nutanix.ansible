#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vms_disks_v2
short_description: Manage disks for Nutanix AHV VMs
version_added: "2.0.0"
description:
    - This module allows you to manage disks for Nutanix AHV VMs.
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then the operation will be  create the item.
            - if C(state) is set to C(present) and C(ext_id) is given then it will update that disk.
            - if C(state) is set to C(present) then C(ext_id) or C(name) needs to be set.
            - >-
                If C(state) is set to C(absent) and if the item exists, then
                item is removed.
        choices:
            - present
            - absent
        type: str
        default: present
    ext_id:
        description:
            - The external ID of the disk.
            - Required for updating or deleting a disk.
        type: str
        required: false
    vm_ext_id:
        description:
            - The external ID of the VM.
        type: str
        required: true
    backing_info:
        description:
            - Supporting storage to create virtual disk on.
        type: dict
        suboptions:
            vm_disk:
                description:
                    - The VM disk information.
                type: dict
                suboptions:
                    disk_size_bytes:
                        description:
                            - The size of the disk in bytes.
                            - Mutually exclusive with C(data_source) during update.
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
                            - The storage configuration for the disk.
                        type: dict
                        suboptions:
                            is_flash_mode_enabled:
                                description:
                                    - Indicates whether the virtual disk is pinned to the hot tier or not.
                                type: bool
                    data_source:
                        description:
                            - The data source for the disk.
                            - Mutually exclusive with C(disk_size_bytes) during update.
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
            adsf_volume_group:
                description:
                    - The ADSF volume group reference.
                type: dict
                suboptions:
                    volume_group_ext_id:
                        description:
                            - The external ID of the volume group.
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
- name: Create a disk for a VM
  nutanix.ncp.ntnx_vms_disks_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd6"
    backing_info:
      vm_disk:
        disk_size_bytes: 1073741824
        storage_container:
          ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd2"
        storage_config:
          is_flash_mode_enabled: true
        data_source:
          reference:
            image_reference:
              image_ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
    disk_address:
      bus_type: "SCSI"
      index: 1
    state: present
    wait: true

- name: Update a disk's storage container and size for a VM
  nutanix.ncp.ntnx_vms_disks_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd6"
    backing_info:
      vm_disk:
        disk_size_bytes: 29843545600
        storage_container:
          ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd7"
    state: present
    wait: true

- name: Delete a disk from a VM
  nutanix.ncp.ntnx_vms_disks_v2:
    vm_ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd6"
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd7"
    state: absent
    wait: true
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix v4 API.
        - For create/delete it will have task response depending on c(wait).
        - For update it will have disk latest info if c(wait) is true.
    type: dict
    returned: always
    sample: {
            "backing_info": {
                "data_source": null,
                "disk_ext_id": "530567f3-abda-4913-b5d0-0ab6758ec16e",
                "disk_size_bytes": 29843545600,
                "is_migration_in_progress": false,
                "storage_config": null,
                "storage_container": {
                    "ext_id": "78ec68c5-d9b0-4ba4-a3e9-96f90d580a0b"
                }
            },
            "disk_address": {
                "bus_type": "PCI",
                "index": 7
            },
            "ext_id": "530567f3-abda-4913-b5d0-0ab6758ec16e",
            "links": null,
            "tenant_id": null
        }
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent or check mode (in delete operation)
    type: str
    sample: "Api Exception raised while creating vm disk"
error:
    description: The error message if an error occurred.
    type: str
    returned: on error
    sample: "Failed generating create vm disk Spec"
changed:
    description: Whether the state of the disk has changed.
    type: bool
    returned: always
    sample: true
skipped:
    description: Whether the operation is skipped due to no state change
    type: bool
    returned: on skipping
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
        - The external ID of the disk.
        - It won't be returned during create due to know issue.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

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
from ..module_utils.v4.vmm.helpers import get_disk, get_vm  # noqa: E402
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
    module_args.update(vm_specs.get_disk_spec())
    return module_args


def create_disk(module, result):
    vmm = get_vm_api_instance(module)
    vm_ext_id = module.params["vm_ext_id"]
    result["vm_ext_id"] = vm_ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.AhvConfigDisk()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create vm disk Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # get etag of vm current state
    vm = get_vm(module, vmm, vm_ext_id)
    etag = get_etag(vm)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vmm.create_disk(vmExtId=vm_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating vm disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id, err = wait_for_entity_ext_id_in_task(
            module, task_ext_id, rel=TASK_CONSTANTS.RelEntityType.VM_DISK
        )
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed to get external ID of disk from task", **result
            )
        if ext_id:
            resp = get_disk(module, vmm, ext_id, vm_ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    if current_spec != update_spec:
        return False
    return True


def update_disk(module, result):
    vmm = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id

    current_spec = get_disk(
        module, api_instance=vmm, ext_id=ext_id, vm_ext_id=vm_ext_id
    )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vm disk update spec", **result)

    # check for idempotency
    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    # data source and disk_size_bytes cannot be sent together
    disk_size_bytes = (
        module.params.get("backing_info", {}).get("vm_disk", {}).get("disk_size_bytes")
    )
    data_source = (
        module.params.get("backing_info", {}).get("vm_disk", {}).get("data_source")
    )
    if disk_size_bytes and data_source:
        result["error"] = "data source and disk_size_bytes cannot be sent together"
        module.exit_json(**result)
    elif disk_size_bytes:
        update_spec.backing_info.data_source = None
    elif data_source:
        update_spec.backing_info.disk_size_bytes = None
    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = vmm.update_disk_by_id(vmExtId=vm_ext_id, extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating vm disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    # poll for the last unfinished task
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_disk(module, vmm, ext_id, vm_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_disk(module, result):
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "VM Disk with ext_id:{0} will be deleted.".format(ext_id)
        return

    vmm = get_vm_api_instance(module)
    disk = get_disk(module, vmm, ext_id, vm_ext_id=vm_ext_id)
    etag = get_etag(disk)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vmm.delete_disk_by_id(vmExtId=vm_ext_id, extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting vm disk",
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
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("ext_id", "backing_info", "disk_address"), True),
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
        "ext_id": None,
        "vm_ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_disk(module, result)
        else:
            create_disk(module, result)
    else:
        delete_disk(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
