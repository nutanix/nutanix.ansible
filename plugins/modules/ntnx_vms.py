#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vms
short_description: VM module which suports VM CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete, Power-on, Power-off Nutanix VM''s'
options:
  nutanix_host:
    description:
      - PC hostname or IP address
    type: str
    required: true
  nutanix_port:
    description:
      - PC port
    type: str
    default: 9440
    required: false
  nutanix_username:
    description:
      - PC username
    type: str
    required: true
  nutanix_password:
    description:
      - PC password;
    required: true
    type: str
  validate_certs:
    description:
      - Set value to C(False) to skip validation for self signed certificates
      - This is not recommended for production setup
    type: bool
    default: true
  state:
    description:
      - Specify state of Virtual Machine
      - If C(state) is set to C(present) the VM is created.
      - >-
        If C(state) is set to C(absent) and the VM exists in the cluster, VM
        with specified name is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: This is the wait description.
    type: bool
    required: false
    default: True
  name:
    description: VM Name
    required: False
    type: str
  vm_uuid:
    description: VM UUID
    type: str
  desc:
    description: A description for VM.
    required: false
    type: str
  project:
    description: Name or UUID of the project.
    required: false
    type: dict
    suboptions:
      name:
        description:
          - Project Name
          - Mutually exclusive with C(uuid)
        type: str
      uuid:
        description:
          - Project UUID
          - Mutually exclusive with C(name)
        type: str
  cluster:
    description:
      - Name or UUID of the cluster on which the VM will be placed.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - Cluster Name
          - Mutually exclusive with C(uuid)
        type: str
      uuid:
        description:
          - Cluster UUID
          - Mutually exclusive with C(name)
        type: str
  vcpus:
    description:
      - Number number of sockets.
    required: false
    type: int
    default: 1
  cores_per_vcpu:
    description:
      - This is the number of vcpus per socket.
    required: false
    type: int
    default: 1
  memory_gb:
    description:
      - Memory size in GB
    required: false
    type: int
    default: 1
  networks:
    description:
      - list of subnets to which the VM needs to connect to.
    type: list
    elements: dict
    required: false
    suboptions:
      subnet:
        description:
          - Name or UUID of the subnet to which the VM should be connnected.
        type: dict
        suboptions:
          name:
            description:
              - Subnet Name
              - Mutually exclusive with C(uuid)
            type: str
          uuid:
            description:
              - Subnet UUID
              - Mutually exclusive with C(name)
            type: str
      private_ip:
        description:
          - Optionally assign static IP to the VM.
        type: str
        required: false
      is_connected:
        description:
          - connect or disconnect the VM to the subnet.
        type: bool
        required: false
        default: true
  disks:
    description:
      - List of disks attached to the VM
    type: list
    elements: dict
    suboptions:
      type:
        description:
          - CDROM or DISK
        choices:
          - CDROM
          - DISK
        default: DISK
        type: str
      size_gb:
        description:
          - The Disk Size in GB.
          - This option is applicable for only DISK type above.
        type: int
      bus:
        description: Bus type of the device
        default: SCSI
        choices:
          - SCSI
          - PCI
          - SATA
          - IDE
        type: str
      storage_container:
        description:
          - Mutually exclusive with C(clone_image) and C(empty_cdrom)
        type: dict
        suboptions:
          name:
            description:
              - Storage containter Name
              - Mutually exclusive with C(uuid)
            type: str
          uuid:
            description:
              - Storage container UUID
              - Mutually exclusive with C(name)
            type: str
      clone_image:
        description:
          - Mutually exclusive with C(storage_container) and C(empty_cdrom)
        type: dict
        suboptions:
          name:
            description:
              - Image Name
              - Mutually exclusive with C(uuid)
            type: str
          uuid:
            description:
              - Image UUID
              - Mutually exclusive with C(name)
            type: str
      empty_cdrom:
        type: bool
        description:
          - Mutually exclusive with C(clone_image) and C(storage_container)
  boot_config:
    description:
      - >-
        Indicates whether the VM should use Secure boot, UEFI boot or Legacy
        boot.
    type: dict
    required: false
    suboptions:
      boot_type:
        description:
          - Boot type of VM.
        choices:
          - LEGACY
          - UEFI
          - SECURE_BOOT
        default: LEGACY
        type: str
      boot_order:
        description:
          - Applicable only for LEGACY boot_type
          - Boot device order list
        type: list
        elements: str
        default:
          - CDROM
          - DISK
          - NETWORK
  guest_customization:
    description:
      - cloud_init or sysprep guest customization
    type: dict
    suboptions:
      type:
        description:
          - cloud_init or sysprep type
        type: str
        required: True
        choices:
          - cloud_init
          - sysprep
      script_path:
        description:
          - Absolute file path to the script.
        type: path
        required: true
      is_overridable:
        description:
          - Flag to allow override of customization during deployment.
        type: bool
        default: false
        required: false
  timezone:
    description:
      - VM's hardware clock timezone in IANA TZDB format (America/Los_Angeles).
    type: str
    default: UTC
    required: false
  categories:
    description:
      - categories to be attached to the VM.
    type: dict
    required: false
author:
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
# TODO
"""

RETURN = r"""
# TODO
"""

from ..module_utils.base_module import BaseModule # noqa: E402
from ..module_utils.prism.tasks import Task # noqa: E402
from ..module_utils.prism.vms import VM # noqa: E402
from ..module_utils.utils import remove_param_with_none_value # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    network_spec = dict(
        subnet=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        private_ip=dict(type="str", required=False),
        is_connected=dict(type="bool", default=True),
    )

    disk_spec = dict(
        type=dict(type="str", choices=["CDROM", "DISK"], default="DISK"),
        size_gb=dict(type="int"),
        bus=dict(type="str", choices=["SCSI", "PCI", "SATA", "IDE"], default="SCSI"),
        storage_container=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        clone_image=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        empty_cdrom=dict(type="bool"),
    )

    boot_config_spec = dict(
        boot_type=dict(
            type="str", choices=["LEGACY", "UEFI", "SECURE_BOOT"], default="LEGACY"
        ),
        boot_order=dict(
            type="list", elements="str", default=["CDROM", "DISK", "NETWORK"]
        ),
    )

    gc_spec = dict(
        type=dict(type="str", choices=["cloud_init", "sysprep"], required=True),
        script_path=dict(type="path", required=True),
        is_overridable=dict(type="bool", default=False),
    )

    module_args = dict(
        name=dict(type="str", required=False),
        vm_uuid=dict(type="str"),
        desc=dict(type="str"),
        project=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        cluster=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        vcpus=dict(type="int", default=1),
        cores_per_vcpu=dict(type="int", default=1),
        memory_gb=dict(type="int", default=1),
        networks=dict(type="list", elements="dict", options=network_spec),
        disks=dict(
            type="list",
            elements="dict",
            options=disk_spec,
            mutually_exclusive=[
                ("storage_container", "clone_image", "empty_cdrom"),
                ("size_gb", "empty_cdrom"),
            ],
        ),
        boot_config=dict(type="dict", options=boot_config_spec),
        guest_customization=dict(type="dict", options=gc_spec),
        timezone=dict(type="str", default="UTC"),
        categories=dict(type="dict"),
    )

    return module_args


def create_vm(module, result):
    vm = VM(module)
    spec, error = vm.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating VM Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp, status = vm.create(spec)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed creating VM", **result)

    vm_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["vm_uuid"] = vm_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp, tmp = vm.read(vm_uuid)
        result["response"] = resp


def delete_vm(module, result):
    vm_uuid = module.params["vm_uuid"]
    if not vm_uuid:
        result["error"] = "Missing parameter vm_uuid in playbook"
        module.fail_json(msg="Failed deleting VM", **result)

    vm = VM(module)
    resp, status = vm.delete(vm_uuid)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed deleting VM", **result)

    result["changed"] = True
    result["response"] = resp
    result["vm_uuid"] = vm_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp, status = task.wait_for_completion(task_uuid)
    result["response"] = resp
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed creating VM", **result)


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name",)),
            ("state", "absent", ("vm_uuid",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_vm(module, result)
    elif state == "absent":
        delete_vm(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
