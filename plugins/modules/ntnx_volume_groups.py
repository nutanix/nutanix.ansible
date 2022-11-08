#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups
short_description: volume_groups module which suports volume_groups CRUD operations
version_added: 1.4.0
description: 'Create, Update, Delete volume_group'
options:
  state:
    description:
      - Specify state of volume_groups
      - If C(state) is set to C(present) then volume_groups is created.
      - >-
        If C(state) is set to C(absent) and if the volume_groups exists, then
        volume_groups is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for volume_groups CRUD operation to complete.
    type: bool
    required: false
    default: True
  name:
    description: volume_groups Name
    required: False
    type: str
  volume_group_uuid:
    description: volume_group UUID
    type: str
  desc:
    description: volume_groups description
    type: str
  cluster:
    description: Name or UUID of the cluster on which the volume group will be placed
    type: dict
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
  target_prefix:
    description:  iSCSI target prefix-name.
    type: str
  flash_mode:
    description:  if enabled all volume disks of the VG will be pinned to SSD tier.
    type: bool
    default: false
  disks:
    description:  Volume group disk specification.
    type: list
    elements: dict
    suboptions:
        size_gb:
            description: The Disk Size in GB.
            type: int
        state:
            description: write
            type: str
            choices: ["absent"]
        uuid:
            description: write
            type: str
        storage_container:
            description: Container  on which to create the disk.
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
  vms:
    description: write
    type: list
    elements: dict
    suboptions:
                name:
                    description:
                        - VM name
                        - Mutually exclusive with C(uuid)
                    type: str
                uuid:
                    description:
                        - VM UUID
                        - Mutually exclusive with C(name)
                    type: str
                state:
                    description:
                        - write
                    type: str
                    choices: ["absent"]
  load_balance:
    description: write
    type: bool
    default: false
  clients:
    description: write
    type: list
    elements: dict
    suboptions:
                state:
                    description:
                    - write
                    type: str
                    choices: ["absent"]
                iscsi_iqn:
                    description:
                    - write
                    type: str
                uuid:
                    description:
                    - write
                    type: str
                iscsi_ip:
                    description:
                    - write
                    type: str
                client_password:
                    description:
                    - write
                    type: str
  CHAP_auth:
    description: Use Challenge-Handshake Authentication Protocol
    type: bool
    default: false
  target_password:
    description: CHAP secret
    type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""

"""

RETURN = r"""

"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.iscsi_clients import Clients  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.vdisks import VDisks  # noqa: E402
from ..module_utils.prism.volume_groups import VolumeGroup  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    disk_spec = dict(
        state=dict(type="str", choices=["absent"]),
        uuid=dict(type="str"),
        size_gb=dict(type="int"),
        storage_container=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
    )

    vm_spec = dict(
        state=dict(type="str", choices=["absent"]),
        name=dict(type="str"),
        uuid=dict(type="str"),
    )

    client_spec = dict(
        state=dict(type="str", choices=["absent"]),
        uuid=dict(type="str"),
        iscsi_iqn=dict(type="str"),
        iscsi_ip=dict(type="str"),
        client_password=dict(type="str", no_log=True),
    )

    module_args = dict(
        name=dict(type="str"),
        desc=dict(type="str"),
        cluster=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        target_prefix=dict(type="str"),
        volume_group_uuid=dict(type="str"),
        flash_mode=dict(type="bool", default=False),
        disks=dict(
            type="list",
            elements="dict",
            options=disk_spec,
            mutually_exclusive=[
                ("uuid", "storage_container"),
                ("state", "size_gb"),
            ],
            required_if=[("state", "absent", ("uuid",))],
        ),
        vms=dict(
            type="list",
            elements="dict",
            options=vm_spec,
            mutually_exclusive=mutually_exclusive,
        ),
        load_balance=dict(type="bool", default=False),
        clients=dict(
            type="list",
            elements="dict",
            options=client_spec,
            mutually_exclusive=[("uuid", "iscsi_iqn", "iscsi_ip")],
        ),
        CHAP_auth=dict(type="bool", default=False),
        target_password=dict(type="str", no_log=True),
    )

    return module_args


def create_volume_group(module, result):
    volume_group = VolumeGroup(module)
    vg_disks = module.params.get("disks")
    vg_vms = module.params.get("vms")
    vg_clients = module.params.get("clients")

    spec, error = volume_group.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating volume_groups spec", **result)

    if module.check_mode:
        result["response"] = spec
        result["response"]["disks"] = vg_disks
        result["response"]["vms"] = vg_vms
        result["response"]["clients"] = vg_clients
        return

    resp = volume_group.create(spec)
    task_uuid = resp["data"]["extId"][-36:]
    result["changed"] = True
    result["response"] = resp
    result["task_uuid"] = task_uuid
    resp = wait_for_task_completion(module, result)
    volume_group_uuid = resp["entity_reference_list"][0]["uuid"]
    result["volume_group_uuid"] = volume_group_uuid
    resp = volume_group.read(volume_group_uuid)
    result["response"] = resp.get("data")

    # create disks
    if vg_disks:
        for disk in vg_disks:
            spec, err = VDisks.get_spec(module, disk)
            if err:
                result["warning"] = "Disk is not created. Error: {0}".format(err)
                result["skipped"] = True
                continue

            vdisk_resp = volume_group.create_vdisk(spec, volume_group_uuid)

            task_uuid = vdisk_resp["task_uuid"]
            wait_for_task_completion(module, {"task_uuid": task_uuid})

        disks_resp = volume_group.get_vdisks(volume_group_uuid)
        result["response"]["disks"] = disks_resp.get("data")

    # attach vms
    if vg_vms:
        for vm in vg_vms:

            spec, err = volume_group.get_vm_spec(vm)
            if err:
                result["warning"] = "VM is not attached. Error: {0}".format(err)
                result["skipped"] = True
                continue

            attach_resp = volume_group.attach_vm(spec, volume_group_uuid)

            task_uuid = attach_resp["task_uuid"]
            wait_for_task_completion(module, {"task_uuid": task_uuid})

        vms_resp = volume_group.get_vms(volume_group_uuid)
        result["response"]["vms"] = vms_resp.get("data")

    # attach clients
    if vg_clients:
        for client in vg_clients:

            spec, err = Clients.get_spec(client, module.params.get("CHAP_auth"))
            if err:
                result["warning"] = "Client is not attached. Error: {0}".format(err)
                result["skipped"] = True
                continue

            attach_resp = volume_group.attach_iscsi_client(spec, volume_group_uuid)

            task_uuid = attach_resp["task_uuid"]
            wait_for_task_completion(module, {"task_uuid": task_uuid})

        clients_resp = volume_group.get_clients(volume_group_uuid)
        result["response"]["clients"] = clients_resp.get("data")


def update_volume_group(module, result):
    volume_group = VolumeGroup(module)
    volume_group_uuid = module.params.get("volume_group_uuid")
    vg_disks = module.params.get("disks")
    vg_vms = module.params.get("vms")
    vg_clients = module.params.get("clients")
    if not volume_group_uuid:
        result["error"] = "Missing parameter volume_group_uuid in playbook"
        module.fail_json(msg="Failed updating volume_group", **result)
    result["volume_group_uuid"] = volume_group_uuid

    # read the current state of volume_group
    resp = volume_group.read(volume_group_uuid)
    resp = resp.get("data")

    # new spec for updating volume_group
    update_spec, error = volume_group.get_update_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating volume_group update spec", **result)

    # check for idempotency
    if check_volume_groups_idempotency(resp, update_spec, volume_group):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. Refer docs to check for fields which can be updated"
        )

    if module.check_mode:
        result["response"] = update_spec
        result["response"]["disks"] = vg_disks
        result["response"]["vms"] = vg_vms
        result["response"]["clients"] = vg_clients
        return

    # update volume_group
    resp = volume_group.update(update_spec, uuid=volume_group_uuid, method="PATCH")
    # result["response"] = resp
    resp = volume_group.read(volume_group_uuid)

    result["changed"] = True
    result["response"] = resp.get("data")

    # update disks
    if vg_disks:
        for disk in vg_disks:
            if disk.get("uuid"):
                disk_uuid = disk["uuid"]
                if disk.get("state") == "absent":
                    vdisk_resp = volume_group.delete_disk(volume_group_uuid, disk_uuid)

                else:
                    spec, err = VDisks.get_spec(module, disk)
                    if err:
                        result["warning"].append(
                            "Disk is not updated. Error: {0}".format(err)
                        )
                        result["skipped"] = True
                        continue
                    vdisk_resp = volume_group.update_disk(
                        spec, volume_group_uuid, disk_uuid
                    )

            else:
                spec, err = VDisks.get_spec(module, disk)
                if err:
                    result["warning"].append(
                        "Disk is not created. Error: {0}".format(err)
                    )
                    result["skipped"] = True
                    continue

                vdisk_resp = volume_group.create_vdisk(spec, volume_group_uuid)

            task_uuid = vdisk_resp["task_uuid"]
            wait_for_task_completion(module, {"task_uuid": task_uuid})

        disks_resp = volume_group.get_vdisks(volume_group_uuid)
        result["response"]["disks"] = disks_resp.get("data")

    # update vms
    if vg_vms:
        for vm in vg_vms:
            if vm.get("state") == "absent":
                vm_resp, err = volume_group.detach_vm(volume_group_uuid, vm)
                if err:
                    result["warning"].append(
                        "VM is not detached. Error: {0}".format(err)
                    )
                    result["skipped"] = True
                    continue
            else:
                spec, err = volume_group.get_vm_spec(vm)
                if err:
                    result["warning"].append(
                        "VM is not attached. Error: {0}".format(err)
                    )
                    result["skipped"] = True
                    continue

                vm_resp = volume_group.attach_vm(spec, volume_group_uuid)

            task_uuid = vm_resp["task_uuid"]
            wait_for_task_completion(module, {"task_uuid": task_uuid})

        vms_resp = volume_group.get_vms(volume_group_uuid)
        result["response"]["vms"] = vms_resp.get("data")

    # update clients
    if vg_clients:
        for client in vg_clients:

            spec, err = Clients.get_spec(client, module.params.get("CHAP_auth"))
            if err:
                result["warning"].append(
                    "Client is not attached. Error: {0}".format(err)
                )
                result["skipped"] = True
                continue

            attach_resp = volume_group.attach_iscsi_client(spec, volume_group_uuid)

            task_uuid = attach_resp["task_uuid"]
            wait_for_task_completion(module, {"task_uuid": task_uuid})

        clients_resp = volume_group.get_clients(volume_group_uuid)
        result["response"]["clients"] = clients_resp.get("data")


def delete_volume_group(module, result):
    volume_group_uuid = module.params["volume_group_uuid"]
    if not volume_group_uuid:
        result["error"] = "Missing parameter volume_group_uuid in playbook"
        module.fail_json(msg="Failed deleting volume_groups", **result)

    volume_group = VolumeGroup(module)

    # detach iscsi_clients
    clients_resp = volume_group.get_clients(volume_group_uuid)
    detached_clients = []
    for client in clients_resp.get("data", []):
        detach_resp = volume_group.detach_iscsi_client(volume_group_uuid, client)

        task_uuid = detach_resp["task_uuid"]
        wait_for_task_completion(module, {"task_uuid": task_uuid})
        detached_clients.append(client["extId"])

    result["detached_clients"] = detached_clients

    # detach vms
    vms_resp = volume_group.get_vms(volume_group_uuid)
    detached_vms = []
    for vm in vms_resp.get("data", []):
        detach_resp = volume_group.detach_vm(volume_group_uuid, vm)

        task_uuid = detach_resp["task_uuid"]
        wait_for_task_completion(module, {"task_uuid": task_uuid})
        detached_vms.append(vm["extId"])

    result["detached_vms"] = detached_vms

    resp = volume_group.delete(volume_group_uuid)
    resp.pop("metadata")
    result["changed"] = True
    result["response"] = resp
    result["volume_group_uuid"] = volume_group_uuid


def check_volume_groups_idempotency(old_spec, update_spec, volume_group):

    for key, value in update_spec.items():
        if old_spec.get(key) != value:
            return False
    volume_group_uuid = volume_group.module.params.get("volume_group_uuid")
    updated_disks = volume_group.module.params.get("disks")
    updated_vms = volume_group.module.params.get("vms")
    updated_clients = volume_group.module.params.get("clients")

    if updated_disks:
        #     vg_disks = volume_group.get_vdisks(volume_group_uuid).get("data")
        #     for disk in updated_disks:
        #         if disk not in vg_disks:
        return False

    if updated_vms:
        vg_vms = volume_group.get_vms(volume_group_uuid).get("data")
        for vm in updated_vms:
            if vm not in vg_vms:
                return False

    if updated_clients:
        vg_clients = volume_group.get_clients(volume_group_uuid).get("data")
        for client in updated_disks:
            if client not in vg_clients:
                return False

    return True


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid)
    return resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "volume_group_uuid"), True),
            ("state", "absent", ("volume_group_uuid",)),
            ("CHAP_auth", True, ("target_password",)),
        ],
        mutually_exclusive=[("vms", "clients")],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "volume_group_uuid": None,
        "warning": [],
    }
    state = module.params["state"]
    if state == "absent":
        delete_volume_group(module, result)
    elif module.params.get("volume_group_uuid"):
        update_volume_group(module, result)
    else:
        create_volume_group(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
