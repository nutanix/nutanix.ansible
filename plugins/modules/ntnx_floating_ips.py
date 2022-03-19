#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_floating_ips
short_description: floating_ips module which suports floating_ip CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete floating_ips'
options:
  fip_uuid:
    description: floating_ip UUID
    type: str
  external_subnet:
    description: A subnet with external connectivity
    type: dict
    suboptions:
      uuid:
        description: Subnet UUID
        type: str
      name:
        description: Subnet Name
        type: str
  private_ip:
    description: the assigned ip
    type: str
  vpc:
        description:
          - Virtual Private Clouds
          - VPCs are required to be attached to Subnets with External Connectivity to send traffic outside the VPC
        type: dict
        suboptions:
          name:
            description:
              - VPC Name
              - Mutually exclusive with (uuid)
            type: str
          uuid:
            description:
              - VPC UUID
              - Mutually exclusive with (name)
            type: str
  vm:
        description:
          - The Vm that will connected with floating ip
        type: dict
        suboptions:
          name:
            description:
              - VM Name
              - Mutually exclusive with (uuid)
            type: str
          uuid:
            description:
              - VM UUID
              - Mutually exclusive with (name)
            type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_opperations
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
"""

EXAMPLES = r"""
- name: create Floating IP with External Subnet Name
  ntnx_floating_ips:
    validate_certs: False
    state: present
    nutanix_host: "{{ IP }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    external_subnet:
      uuid: "{{external_subnet.subnet_uuiid}}"

- name: create Floating IP with vpc Name with external subnet uuid
  ntnx_floating_ips:
    validate_certs: False
    state: present
    nutanix_host: "{{ IP }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    external_subnet:
      uuid: "{{external_subnet.subnet_uuiid}}"
    vpc:
       name: "{{vpc.vpc_name}}"
    private_ip: "{{private_ip}}"

- name: create Floating IP with External Subnet with vm
  ntnx_floating_ips:
    validate_certs: False
    state: present
    nutanix_host: "{{ IP }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    external_subnet:
      name: "{{vm_subnet_name}}"
    vm:
      name: "{{vm.vm_name}}"
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The Floating ips  metadata
  returned: always
  type: dict
  sample: {
                "categories": {},
                "categories_mapping": {},
                "creation_time": "2022-02-14T12:51:12Z",
                "kind": "floating_ip",
                "last_update_time": "2022-02-14T12:51:13Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "spec_version": 0,
                "uuid": "d34a85bc-67c5-4888-892c-76f51b1935fd"
            }
spec:
  description: An intentful representation of a Floating ip spec
  returned: always
  type: dict
  sample: {
                "resources": {
                    "external_subnet_reference": {
                        "kind": "subnet",
                        "uuid": "3f9face6-43ad-4b93-91c7-99db3155ea32"
                    }
                }
            }
status:
  description: An intentful representation of a VPC status
  returned: always
  type: dict
  sample: {
                "execution_context": {
                    "task_uuid": [
                        "e6e8cbd9-3f8e-46e5-90d2-3d395031090c"
                    ]
                },
                "name": "",
                "resources": {
                    "external_subnet_reference": {
                        "kind": "subnet",
                        "uuid": "3f9face6-43ad-4b93-91c7-99db3155ea32"
                    },
                    "floating_ip": "192.168.1.32"
                },
                "state": "COMPLETE"
}
fip_uuid:
  description: The created Floating ip uuid
  returned: always
  type: str
  sample: "d34a85bc-67c5-4888-892c-76f51b1935fd"
task_uuid:
  description: The task uuid for the creation
  returned: always
  type: str
  sample: "e6e8cbd9-3f8e-46e5-90d2-3d395031090c"
"""


from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.floating_ips import FloatingIP  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    module_args = dict(
        fip_uuid=dict(type="str", required=False),
        external_subnet=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        vm=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        vpc=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        private_ip=dict(type="str"),
    )

    return module_args


def create_floating_ip(module, result):
    floating_ip = FloatingIP(module)
    spec, error = floating_ip.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating floating_ip spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = floating_ip.create(spec)
    fip_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["fip_uuid"] = fip_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = floating_ip.read(fip_uuid)
        result["response"] = resp


def delete_floating_ip(module, result):
    fip_uuid = module.params["fip_uuid"]
    if not fip_uuid:
        result["error"] = "Missing parameter fip_uuid in playbook"
        module.fail_json(msg="Failed deleting floating_ip", **result)

    floating_ip = FloatingIP(module)
    resp = floating_ip.delete(fip_uuid)
    result["changed"] = True
    result["response"] = resp
    result["fip_uuid"] = fip_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid)
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ("vm", "vpc"),
            ("fip_uuid", "external_subnet"),
            ("fip_uuid", "vm"),
            ("fip_uuid", "vpc"),
        ],
        required_if=[
            ("state", "present", ("external_subnet",)),
            ("state", "absent", ("fip_uuid",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "fip_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_floating_ip(module, result)
    elif state == "absent":
        delete_floating_ip(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
