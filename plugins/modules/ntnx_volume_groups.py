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
 # ...............TODO
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
            mutually_exclusive=mutually_exclusive
        ),
        load_balance=dict(type="bool", default=False),
        clients=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive
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
        return

    resp = volume_group.create(spec)
    task_uuid = resp["data"]["extId"][-36:]
    result["changed"] = True
    result["response"] = resp
    result["task_uuid"] = task_uuid
    wait_for_task_completion(module, result)

    volume_group_uuid = result["volume_group_uuid"]
    resp = volume_group.read(volume_group_uuid)
    result["response"] = resp

    # create disks
    if module.params.get("disks"):
        vdisk = VDisks()
        disks_response = []
        for disk in module.params["disks"]:
            spec, _ = vdisk.get_spec(module, disk)
            resp = volume_group.update(
                spec, volume_group_uuid, method="POST", endpoint="disks"
            )
            disks_response.append(resp)
        result["response"]["disks"] = disks_response

    # attach vms
    if module.params.get("vms"):
        vms_response = []
        for vm in module.params["vms"]:
            spec, _ = volume_group.get_vm_spec(vm)
            resp = volume_group.update(
                spec, volume_group_uuid, method="POST", endpoint="$actions/attach-vm"
            )
            vms_response.append(resp)
        result["response"]["vms"] = vms_response

    # attach clients
    if module.params.get("clients"):
        clients_response = []
        for client in module.params["clients"]:
            spec, _ = volume_group.get_client_spec(client)
            resp = volume_group.update(
                spec, volume_group_uuid, method="POST", endpoint="/$actions/attach-iscsi-client"
            )
            clients_response.append(resp)
        result["response"]["clients"] = clients_response


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


# def delete_volume_group(module, result):
#     volume_group_uuid = module.params["volume_group_uuid"]
#     if not volume_group_uuid:
#         result["error"] = "Missing parameter volume_group_uuid in playbook"
#         module.fail_json(msg="Failed deleting volume_groups", **result)
#
#     volume_group = VolumeGroup(module)
#     resp = volume_group.delete(volume_group_uuid, no_response=True)
#     result["changed"] = True
#     result["response"] = resp
#     result["volume_group_uuid"] = volume_group_uuid


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid)
    result["response"] = resp
    result["volume_group_uuid"] = resp["entity_reference_list"][0]["uuid"]


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "volume_group_uuid"), True),
            ("state", "absent", ("volume_group_uuid",)),
        ],
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
