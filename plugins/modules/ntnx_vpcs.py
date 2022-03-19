#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpcs
short_description: Virtual Private Cloud (VPC) module which suports vpc CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete vpcs'
options:
  name:
    description: VPC name
    type: str
    required: false
  vpc_uuid:
    description: VPC uuid
    type: str
  dns_servers:
    description:
      - List of DNS servers IPs
      - DNS is advertised to Guest VMs via DHCP
    type: list
    elements: str
  routable_ips:
    description: Address space within the VPC which can talk externally without NAT. These are in effect when No-NAT External subnet is used
    type: list
    elements: dict
    suboptions:
      network_ip:
        description: Network ip address
        type: str
      network_prefix:
        description: Network ip address prefix length
        type: int
  external_subnets:
    description:
      - Subnet with external connectivity
      - Required if the VPC needs to send traffic to a destination outside of the VPC
    type: list
    elements: dict
    suboptions:
      subnet_uuid:
        description: External subnet uuid
        type: str
      subnet_name:
        description: External subnet name
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

  - name: Create min VPC
    ntnx_vpcs:
      validate_certs: False
      state: present
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      name: MinVPC
      external_subnets:
        - subnet_name: "{{ external_subnet.name }}"

  - name: Create VPC with dns_servers
    ntnx_vpcs:
      validate_certs: False
      state: present
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      name: vpc_with_dns_servers
      dns_servers: "{{ dns_servers }}"

  - name: Create VPC with all specfactions
    ntnx_vpcs:
      validate_certs: False
      state: present
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      name: vpc_with_add_specfactions
      external_subnets:
        - subnet_name: "{{ external_subnet.name }}"
      dns_servers: "{{ dns_servers }}"
      routable_ips:
        - network_ip: "{{ routable_ips.network_ip }}"
          network_prefix:  "{{ routable_ips.network_prefix }}"

  - name: Delete VPC
    ntnx_vpcs:
      state: absent
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      vpc_uuid: "{{ vpc_uuid }}"
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The VPC  metadata
  returned: always
  type: dict
  sample: {
                "categories": {},
                "categories_mapping": {},
                "creation_time": "2022-02-13T12:13:23Z",
                "kind": "vpc",
                "last_update_time": "2022-02-13T12:13:26Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "spec_version": 0,
                "uuid": "26f353fc-424b-4925-9d7d-16f19f1312a9"
            }
spec:
  description: An intentful representation of a VPC spec
  returned: always
  type: dict
  sample: {
                "name": "MinVPC",
                "resources": {
                    "common_domain_name_server_ip_list": [],
                    "external_subnet_list": [
                        {
                            "external_subnet_reference": {
                                "kind": "subnet",
                                "uuid": "57959f75-6b21-431c-b76b-516447d52621"
                            }
                        }
                    ],
                    "externally_routable_prefix_list": []
                }
            }
status:
  description: An intentful representation of a VPC status
  returned: always
  type: dict
  sample:  {
                "execution_context": {
                    "task_uuid": [
                        "9829d43d-85aa-4560-9862-81db1433a85a"
                    ]
                },
                "name": "MinVPC",
                "resources": {
                    "availability_zone_reference_list": [],
                    "common_domain_name_server_ip_list": [],
                    "external_subnet_list": [
                        {
                            "active_gateway_node": {
                                "host_reference": {
                                    "kind": "host",
                                    "uuid": "e16b6989-a149-4f93-989f-bc3e96f88a40"
                                },
                                "ip_address": "10.46.136.28"
                            },
                            "external_ip_list": [
                                "192.168.1.109"
                            ],
                            "external_subnet_reference": {
                                "kind": "subnet",
                                "uuid": "57959f75-6b21-431c-b76b-516447d52621"
                            }
                        }
                    ],
                    "externally_routable_prefix_list": []
                },
                "state": "COMPLETE"
}
vpc_uuid:
  description: The created VPC uuid
  returned: always
  type: str
  sample: "26f353fc-424b-4925-9d7d-16f19f1312a9"
task_uuid:
  description: The task uuid for the creation
  returned: always
  type: str
  sample: "9829d43d-85aa-4560-9862-81db1433a85a"
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.vpcs import Vpc  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    external_subnets_spec = dict(
        subnet_name=dict(type="str"), subnet_uuid=dict(type="str")
    )
    routable_ips_spec = dict(
        network_ip=dict(type="str"), network_prefix=dict(type="int")
    )
    module_args = dict(
        name=dict(type="str"),
        vpc_uuid=dict(type="str"),
        external_subnets=dict(
            type="list",
            elements="dict",
            options=external_subnets_spec,
            mutually_exclusive=[("subnet_name", "subnet_uuid")],
        ),
        routable_ips=dict(type="list", elements="dict", options=routable_ips_spec),
        dns_servers=dict(type="list", elements="str"),
    )

    return module_args


def create_vpc(module, result):
    vpc = Vpc(module)
    spec, error = vpc.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating vpc spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = vpc.create(spec)
    vpc_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["vpc_uuid"] = vpc_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = vpc.read(vpc_uuid)
        result["response"] = resp


def delete_vpc(module, result):
    vpc_uuid = module.params["vpc_uuid"]
    if not vpc_uuid:
        result["error"] = "Missing parameter vpc_uuid in playbook"
        module.fail_json(msg="Failed deleting vpc", **result)

    vpc = Vpc(module)
    resp = vpc.delete(vpc_uuid)
    result["changed"] = True
    result["response"] = resp
    result["vpc_uuid"] = vpc_uuid
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
        required_if=[
            ("state", "present", ("name",)),
            ("state", "absent", ("vpc_uuid",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vpc_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_vpc(module, result)
    elif state == "absent":
        delete_vpc(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
