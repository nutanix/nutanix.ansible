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
  load_balance:
    description: write
    type: bool
    default: false
  clients:
    description: write
    type: list
    elements: dict
    suboptions:
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
        size_gb=dict(type="int"),
        storage_container=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
    )

    client_spec = dict(
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
        disks=dict(type="list", elements="dict", options=disk_spec),
        vms=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
        ),
        load_balance=dict(type="bool", default=False),
        clients=dict(
            type="list",
            elements="dict",
            options=client_spec,
            # mutually_exclusive=mutually_exclusive,
        ),
        CHAP_auth=dict(type="bool", default=False),
        target_password=dict(type="str", no_log=True),
    )

    return module_args


def create_volume_group(module, result):
    volume_group = VolumeGroup(module)
    spec, error = volume_group.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating volume_groups spec", **result)

    if module.check_mode:
        result["response"] = spec
        result["response"]["vms"] = module.params["vms"]
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
    if module.params.get("disks"):
        for disk in module.params["disks"]:
            spec, err = VDisks.get_spec(module, disk)
            update_resp = volume_group.update(
                spec, volume_group_uuid, method="POST", endpoint="disks"
            )
            task_uuid = update_resp["data"]["extId"][-36:]
            wait_for_task_completion(module, {"task_uuid": task_uuid})
        disks = volume_group.read(volume_group_uuid, endpoint="/disks")
        result["response"]["disks"] = disks.get("data")

    # attach vms
    if module.params.get("vms"):
        for vm in module.params["vms"]:
            spec, err = volume_group.get_vm_spec(vm)
            update_resp = volume_group.update(
                spec, volume_group_uuid, method="POST", endpoint="$actions/attach-vm"
            )
            task_uuid = update_resp["data"]["extId"][-36:]
            wait_for_task_completion(module, {"task_uuid": task_uuid})
        vms = volume_group.read(volume_group_uuid, endpoint="/vm-attachments")
        result["response"]["vms"] = vms.get("data")

    # attach clients
    if module.params.get("clients"):
        for client in module.params["clients"]:
            spec, err = Clients.get_spec(client, module.params.get("CHAP_auth"))
            update_resp = volume_group.update(
                spec,
                volume_group_uuid,
                method="POST",
                endpoint="/$actions/attach-iscsi-client",
            )
            task_uuid = update_resp["data"]["extId"][-36:]
            wait_for_task_completion(module, {"task_uuid": task_uuid})
        clients = volume_group.read(
            volume_group_uuid, endpoint="/iscsi-client-attachments"
        )
        result["response"]["clients"] = clients.get("data")


# def update_volume_group(module, result):
#     volume_group = VolumeGroup(module)
#     volume_group_uuid = module.params.get("volume_group_uuid")
#     if not volume_group_uuid:
#         result["error"] = "Missing parameter volume_group_uuid in playbook"
#         module.fail_json(msg="Failed updating volume_group", **result)
#     result["volume_group_uuid"] = volume_group_uuid
#
#     # read the current state of volume_group
#     resp = volume_group.read(volume_group_uuid)
#     resp = resp.get("volume_group")
#
#     # new spec for updating volume_group
#     update_spec, error = volume_group.get_spec(resp)
#     if error:
#         result["error"] = error
#         module.fail_json(msg="Failed generating volume_group update spec", **result)
#
#     # check for idempotency
#     if resp == update_spec:
#         result["skipped"] = True
#         module.exit_json(
#             msg="Nothing to change. Refer docs to check for fields which can be updated"
#         )
#
#     if module.check_mode:
#         result["response"] = update_spec
#         return
#
#     # update volume_group
#     volume_group.update(update_spec, uuid=volume_group_uuid, no_response=True)
#
#     resp = volume_group.read(volume_group_uuid)
#
#     result["changed"] = True
#     result["response"] = resp


def delete_volume_group(module, result):
    def detach_iscsi_clients():
        clients_resp = volume_group.read(
            volume_group_uuid, endpoint="/iscsi-client-attachments"
        )
        detached_clients = []
        for client in clients_resp.get("data", []):
            client_uuid = client["extId"]
            endpoint = "$actions/detach-iscsi-client/{0}".format(client_uuid)
            detach_resp = volume_group.update(
                uuid=volume_group_uuid, method="post", endpoint=endpoint
            )
            task_uuid = detach_resp["data"]["extId"][-36:]
            wait_for_task_completion(module, {"task_uuid": task_uuid})
            detached_clients.append(client_uuid)
        result["detached_clients"] = detached_clients

    def detach_vms():
        vms_resp = volume_group.read(volume_group_uuid, endpoint="/vm-attachments")
        detached_vms = []
        for vm in vms_resp.get("data", []):
            vm_uuid = vm["extId"]
            endpoint = "$actions/detach-vm/{0}".format(vm_uuid)
            detach_resp = volume_group.update(
                uuid=volume_group_uuid, method="post", endpoint=endpoint
            )
            task_uuid = detach_resp["data"]["extId"][-36:]
            wait_for_task_completion(module, {"task_uuid": task_uuid})
            detached_vms.append(vm_uuid)
        result["detached_vms"] = detached_vms

    volume_group_uuid = module.params["volume_group_uuid"]
    if not volume_group_uuid:
        result["error"] = "Missing parameter volume_group_uuid in playbook"
        module.fail_json(msg="Failed deleting volume_groups", **result)

    volume_group = VolumeGroup(module)
    detach_iscsi_clients()
    detach_vms()
    resp = volume_group.delete(volume_group_uuid)
    resp.pop("metadata")
    result["changed"] = True
    result["response"] = resp
    result["volume_group_uuid"] = volume_group_uuid


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