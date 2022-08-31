#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_karbon_registries
short_description: Create, Delete a k8s registry with the provided configuration.
version_added: 1.6.0
description: "Create, Delete registries"
options:
    name:
        type: str
        description: Unique name of the k8s registry.
    cert:
        type: str
        description: Certificate of the private registry in format of base64-encoded byte array.
    username:
        type: str
        description: Username for authentication to the private registry.
    password:
        type: str
        description: Password for authentication to the private registry.
    url:
        type: str
        description: URL of the private registry.
    port:
        type: int
        description: Port of the private registry.

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

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.karbon.registries import Registry  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        cert=dict(type="str"),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
        url=dict(type="str"),
        port=dict(type="int"),
    )

    return module_args


def create_registry(module, result):
    registry = Registry(module)

    spec, error = registry.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating create registry spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = registry.create(spec)
    registry_uuid = resp["registry_uuid"]
    task_uuid = resp["task_uuid"]
    result["registry_uuid"] = registry_uuid
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = registry.read(resp["registry_name"])

    result["response"] = resp


def delete_registry(module, result):
    registry_name = module.params["name"]
    if not registry_name:
        result["error"] = "Missing parameter name in playbook"
        module.fail_json(msg="Failed deleting registry", **result)

    registry = Registry(module)
    resp = registry.delete(registry_name)
    result["changed"] = True
    result["registry_name"] = registry_name
    task_uuid = resp["task_uuid"]
    result["task_uuid"] = task_uuid

    if module.params.get("wait"):
        task = Task(module)
        resp = task.wait_for_completion(task_uuid)

    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("name",)),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"response": {}, "error": None, "changed": False}
    state = module.params["state"]
    if state == "present":
        create_registry(module, result)
    else:
        delete_registry(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
