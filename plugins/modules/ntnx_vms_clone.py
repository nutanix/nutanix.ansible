#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vms_clone
short_description: VM module which supports VM CRUD operations
version_added: 1.0.0
description: "Create, Update, Delete, Power-on, Power-off Nutanix VM's"


extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_opperations
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
from ..module_utils.prism.vms import VM  # noqa: E402
from ..module_utils import utils


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    network_spec = dict(
        uuid=dict(type="str"),
        state=dict(type="str", choices=["absent"]),
        subnet=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        private_ip=dict(type="str", required=False),
        is_connected=dict(type="bool", default=True),
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
        vcpus=dict(type="int"),
        cores_per_vcpu=dict(type="int"),
        memory_gb=dict(type="int"),
        networks=dict(type="list", elements="dict", options=network_spec),
        boot_config=dict(type="dict", options=boot_config_spec),
        guest_customization=dict(type="dict", options=gc_spec),
        timezone=dict(type="str", default="UTC"),
        categories=dict(type="dict"),
    )

    return module_args


def clone_vm(module, result):
    vm_uuid = module.params["vm_uuid"]

    vm = VM(module)

    spec, error = vm.get_clone_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating VM Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = vm.clone(spec)

    result["changed"] = True
    result["response"] = resp
    result["task_uuid"] = resp["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = vm.read(vm_uuid)
        result["response"] = resp


def wait_for_task_completion(module, result, raise_error=True):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid, raise_error=raise_error)
    result["response"] = resp
    if not result.get("vm_uuid") and resp.get("entity_reference_list"):
        result["vm_uuid"] = resp["entity_reference_list"][0]["uuid"]


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    utils.remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_uuid": None,
        "task_uuid": None,
    }
    clone_vm(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
