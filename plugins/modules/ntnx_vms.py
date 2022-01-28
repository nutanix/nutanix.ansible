#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: ntnx_vm
short_description: VM module which suports VM CRUD operations
version_added: 1.0.9
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
    required: false
    default: false
  name:
    description: VM Name
    required: true
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
        required: true
      uuid:
        description:
          - Project UUID
          - Mutually exclusive with C(name)
        type: str
        required: true
  cluster:
    description:
      - Name or UUID of the cluster on which the VM will be placed.
    required: false
    suboptions:
      name:
        description:
          - Cluster Name
          - Mutually exclusive with C(uuid)
        type: str
        required: true
      uuid:
        description:
          - Cluster UUID
          - Mutually exclusive with C(name)
        type: str
        required: true
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
        suboptions:
          name:
            description:
              - Subnet Name
              - Mutually exclusive with C(uuid)
            type: str
            required: true
          uuid:
            description:
              - Subnet UUID
              - Mutually exclusive with C(name)
            type: str
            required: true
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
        choices:
          - SCSI
          - PCI
          - SATA
          - IDE
        type: str
      storage_container:
        description:
          - Mutually exclusive with C(clone_image) and C(empty_cdrom)
        suboptions:
          name:
            description:
              - Storage containter Name
              - Mutually exclusive with C(uuid)
            type: str
            required: true
          uuid:
            description:
              - Storage container UUID
              - Mutually exclusive with C(name)
            type: str
            required: true
      clone_image:
        description:
          - Mutually exclusive with C(storage_container) and C(empty_cdrom)
        suboptions:
          name:
            description:
              - Image Name
              - Mutually exclusive with C(uuid)
            type: str
            required: true
          uuid:
            description:
              - Image UUID
              - Mutually exclusive with C(name)
            type: str
            required: true
      empty_cdrom:
        type: bool
        description:
          - Mutually exclusive with C(clone_image) and C(storage_container)
  boot_config:
    description:
      - >-
        Indicates whether the VM should use Secure boot, UEFI boot or Legacy
        boot.
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
        default:
          - CDROM
          - DISK
          - NETWORK
  guest_customization:
    description:
      - cloud_init or sysprep guest customization
    type: dict
    required: false
    suboptions:
      type:
        description:
          - cloud_init or sysprep type
        type: str
        choices:
          - cloud_init
          - sysprep
        default: sysprep
        required: true
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


"""

EXAMPLES = r"""
# TODO
"""

RETURN = r"""
# TODO
"""


from ansible.module_utils.basic import env_fallback

from ..module_utils.base_module import BaseModule
from ..module_utils.prism.vms import VM
from ..module_utils.prism.tasks import Task


def run_module():
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    network_spec = dict(
        subnet=dict(type="dict", options=entity_by_spec),
        private_ip=dict(type="str"),
        is_connected=dict(type="bool", default=True),
    )

    disk_spec = dict(
        # TODO
        # if type='CDROM', then bus==['SATA', 'IDE']
        # this check needs to be implemented.
        type=dict(type="str", choices=["CDROM", "DISK"], default="DISK"),
        size_gb=dict(type="int"),
        bus=dict(type="str", choices=["SCSI", "PCI", "SATA", "IDE"], default="SCSI"),
        storage_container=dict(type="dict", options=entity_by_spec),
        clone_image=dict(type="dict", options=entity_by_spec),
        empty_cdrom=dict(type="bool"),
        mutually_exclusive=[
            ("storage_container", "empty_cdrom", "clone_image"),
            ("empty_cdrom", "size_gb"),
        ],
        required_one_of=[("storage_container", "empty_cdrom", "clone_image")],
        required_by={"storage_container": "size_gb", "clone_image": "size_gb"},
    )

    boot_config_spec = dict(
        # TODO
        # if boot_type=UEFI OR SECURE_BOOT, then boot_order is not required.
        boot_type=dict(type="str", choices=["LEGACY", "UEFI", "SECURE_BOOT"]),
        boot_order=dict(
            type="list", elements=str, default=["CDROM", "DISK", "NETWORK"]
        ),
    )

    gc_spec = dict(
        type=dict(type="str", choices=["cloud_init", "sysprep"], required=True),
        script_path=dict(type="path", required=True),
        is_overridable=dict(type="bool", default=False),
    )

    module_args = dict(
        nutanix_host=dict(
            type="str", required=True, fallback=(env_fallback, ["NUTANIX_HOST"])
        ),
        nutanix_port=dict(default="9440", type="str"),
        nutanix_username=dict(
            type="str", required=True, fallback=(env_fallback, ["NUTANIX_USERNAME"])
        ),
        nutanix_password=dict(
            type="str",
            required=True,
            no_log=True,
            fallback=(env_fallback, ["NUTANIX_PASSWORD"]),
        ),
        validate_certs=dict(
            type="bool", default=True, fallback=(env_fallback, ["VALIDATE_CERTS"])
        ),
        state=dict(type="str", choices=["present", "absent"], default="present"),
        wait=dict(type="bool", default=True),
        name=dict(type="str", required=True),
        desc=dict(type="str"),
        project=dict(type="dict", options=entity_by_spec),
        cluster=dict(type="dict", options=entity_by_spec),
        vcpus=dict(type="int", default=1),
        cores_per_vcpu=dict(type="int", default=1),
        memory_gb=dict(type="int", default=1),
        networks=dict(type="list", elements=dict, options=network_spec),
        disks=dict(type="list", elements=dict, options=disk_spec),
        boot_config=dict(type="dict", options=boot_config_spec),
        guest_customization=dict(type="dict", options=gc_spec),
        timezone=dict(type="str", default="UTC"),
        categories=dict(type="dict"),
    )

    module = BaseModule(argument_spec=module_args, supports_check_mode=True)

    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_uuid": None,
        "task_uuid": None,
        "msg": "",
    }

    vm = VM(module)

    module.debug("Generating VM spec")
    spec, error = vm.get_spec()
    if error:
        module.debug(error)
        result["error"] = error
        module.fail_json(**result)

    if module.check_mode:
        result["response"] = spec
        return module.exit_json(**result)

    module.debug("VM spec: {0}".format(spec))

    resp, status = vm.create(spec)
    if status["error"]:
        module.debug(status["error"])
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(**result)

    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["task_uuid"] = task_uuid
    result["vm_uuid"] = resp["metadata"]["uuid"]

    if module.params["wait"]:
        task = Task(module)
        resp, status = task.wait_for_completion(task_uuid)
        if status["error"]:
            module.debug(status["error"])
            result["error"] = status["error"]
            result["response"] = resp
            module.fail_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
