#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ova
short_description: VM module which supports VM CRUD operations
version_added: 1.0.0
description: "Create, Update, Delete, Power-on, Power-off Nutanix VM's"
options:
  vm_uuid:
    description: VM UUID
    required: true
    type: str
  name:
      description:
        - Name of the OVA
      required: true
      type: str
  file_format:
      description:
        - File format of disk in OVA
      required: true
      type: str
      choices:
        - QCOW2
        - VMDK
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


def get_module_spec():
    module_args = dict(
        vm_uuid=dict(type="str", required=True),
        name=dict(type="str", required=True),
        file_format=dict(type="str", choices=["QCOW2", "VMDK"], required=True),
    )

    return module_args


def create(module, result):
    vm_uuid = module.params["vm_uuid"]

    vm = VM(module)
    spec = vm.get_ova_image_spec()
    result["vm_uuid"] = vm_uuid

    if module.check_mode:
        result["response"] = spec
        return

    resp = vm.create_ova_image(spec)

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
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_uuid": None,
        "task_uuid": None,
    }
    create(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
