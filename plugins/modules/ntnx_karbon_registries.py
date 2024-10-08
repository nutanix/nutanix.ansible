#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_karbon_registries
short_description: Create and delete the private registry entry in Karbon.
version_added: 1.6.0
description: "Create and delete the private registry entry in Karbon with the provided configuration."
options:
    name:
        type: str
        description: Unique name of the k8s registry.
        required: true
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
        default: 5000
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
    - Prem Karat (@premkarat)
    - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
    - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: create registry
  ntnx_karbon_registries:
    name: "{{registry_name}}"
    url: "{{url}}"
    port: "{{port_number}}"
  register: result

- name: delete registry
  ntnx_karbon_registries:
    name: "{{registry_name}}"
    state: absent
  register: result

- name: create registry with username and password
  ntnx_karbon_registries:
    name: "{{registry_name}}"
    url: "{{url}}"
    username: "{{username}}"
    password: "{{password}}"
  register: result
"""

RETURN = r"""
name:
    description: K8s registry name.
    returned: always
    type: str
    sample: "test-module21"
uuid:
    description: The universally unique identifier (UUID) of the k8s registry.
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000000"
endpoint:
    description: "Endpoint of the private registry in format url:port. Example: prod-user-registry:5000"
    returned: always
    type: str
    sample: "xxx.xxx.xxx.xxx:5000"
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.karbon.registries import Registry  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str", required=True),
        cert=dict(type="str"),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
        url=dict(type="str"),
        port=dict(type="int", default=5000),
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
    result["changed"] = True
    result["response"] = resp


def delete_registry(module, result):
    registry_name = module.params["name"]
    if not registry_name:
        result["error"] = "Missing parameter name in playbook"
        module.fail_json(msg="Failed deleting registry", **result)

    registry = Registry(module)
    resp = registry.delete(registry_name)
    result["changed"] = True
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
