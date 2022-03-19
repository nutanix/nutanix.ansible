#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_subnets
short_description: subnets module which suports subnet CRUD operations
version_added: 1.0.0
description: "Create, Update, Delete subnets"
options:
  name:
    description: Subnet Name
    required: false
    type: str
  subnet_uuid:
    description: Subnet UUID
    type: str
  vlan_subnet:
    description:
      - One of the subnets types
      - Mutually exclusive with C(external_subnet) and C(overlay_subnet)
    type: dict
    suboptions:
      vlan_id:
        description: Unique id of the vlan
        type: int
        required: true
      cluster:
        description:
          - Name or UUID of the cluster on which the subnet will be placed
        type: dict
        required: true
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
      virtual_switch:
        description:
          - Name or UUID of the virtual_switch that the subnet will use
        type: dict
        required: true
        suboptions:
          name:
            description:
              - Virtual switch name
              - Mutually exclusive with C(uuid)
            type: str
          uuid:
            description:
              - Virtual switch UUID
              - Mutually exclusive with C(name)
            type: str
      ipam:
        description:
          -  ip address management configurations of the subnet
        type: dict
        suboptions:
          network_ip:
            description:
              - Subnet network address
            type: str
          network_prefix:
            description:
              - Subnet network address prefix length
            type: int
          gateway_ip:
            description:
              - The gateway ip address
            type: str
          ip_pools:
            description:
              - Range of IPs
            type: list
            elements: dict
            suboptions:
              start_ip:
                description:
                  - The start address of the IPs pool range
                type: str
              end_ip:
                description:
                  - The end address of the IPs pool range
                type: str
          dhcp:
            description:
              - The DHCP settings of the subnet
            type: dict
            suboptions:
              dns_servers:
                description:
                  - List of DNS servers IPs
                type: list
                elements: str
              domain_name:
                description:
                  - The domain name
                type: str
              tftp_server_name:
                description:
                  - The TFTP server name
                type: str
              boot_file:
                description:
                  - The boot file name
                type: str
              dhcp_server_ip:
                description:
                  - The DHCP server IP
                type: str
              domain_search:
                description:
                  - List of domain search
                type: list
                elements: str
  external_subnet:
    description:
      - One of the subnets types
      - Mutually exclusive with C(vlan_subnet) and C(overlay_subnet)
    type: dict
    suboptions:
      vlan_id:
        description: Unique id of vlan
        type: int
        required: true
      cluster:
        description:
          - Name or UUID of the cluster on which the subnet will be placed.
        type: dict
        required: true
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
      enable_nat:
        description:
          - Perform Network Address Translation (NAT) on the traffic to / from the VPCs attached to it
        type: bool
        default: true
      ipam:
        description:
          - IP address management configurations of the subnet
        type: dict
        required: true
        suboptions:
          network_ip:
            description:
              - Subnet network address
            type: str
            required: true
          network_prefix:
            description:
              - Subnet network address prefix length
            type: int
            required: true
          gateway_ip:
            description:
              - The gateway ip address
            type: str
            required: true
          ip_pools:
            description:
              - Range of IPs
            type: list
            elements: dict
            suboptions:
              start_ip:
                description:
                  - The start address of the IPs pool range
                type: str
              end_ip:
                description:
                  - The end address of the IPs pool range
                type: str
  overlay_subnet:
    description:
      - One of the subnets types
      - Mutually exclusive with C(vlan_subnet) and C(external_subnet)
    type: dict
    suboptions:
      vpc:
        description:
          - Virtual Private Clouds
          - VPCs are required to be attached to Subnets with External Connectivity to send traffic outside the VPC
        type: dict
        required: true
        suboptions:
          name:
            description:
              - VPC Name
              - Mutually exclusive with C(uuid)
            type: str
          uuid:
            description:
              - VPC UUID
              - Mutually exclusive with C(name)
            type: str
      ipam:
        description:
          - IP address management configurations of the subnet
        type: dict
        required: true
        suboptions:
          network_ip:
            description:
              - Subnet network address
            type: str
            required: true
          network_prefix:
            description:
              - Subnet network address prefix length
            type: int
            required: true
          gateway_ip:
            description:
              - The gateway ip address
            type: str
            required: true
          ip_pools:
            description:
              - Range of IPs
            type: list
            elements: dict
            suboptions:
              start_ip:
                description:
                  - The start address of the IPs pool range
                type: str
              end_ip:
                description:
                  - The end address of the IPs pool range
                type: str
          dhcp:
            description:
              - The DHCP settings of the subnet
            type: dict
            suboptions:
              dns_servers:
                description:
                  - List of DNS servers IPs
                type: list
                elements: str
              domain_name:
                description:
                  - The domain name
                type: str
              tftp_server_name:
                description:
                  - The TFTP server name
                type: str
              boot_file:
                description:
                  - The boot file name
                type: str
              domain_search:
                description:
                  - List of domain search
                type: list
                elements: str
              dhcp_server_ip:
                description:
                  - The DHCP server IP
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
  - name: VLAN subnet with IPAM IP pools and DHCP
    ntnx_subnets:
      state: present
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      name: VLAN subnet with IPAM IP pools and DHCP
      vlan_subnet:
        vlan_id: "{{vlan_subnets_ids.3}}"
        virtual_switch:
          name: "{{ virtual_switch.name }}"
        cluster:
          name: "{{ cluster.name }}"
        ipam:
          network_ip: "{{ network_ip }}"
          network_prefix: "{{ network_prefix }}"
          gateway_ip: "{{ gateway_ip_address }}"
          ip_pools:
            - start_ip: "{{ start_address }}"
              end_ip: "{{ end_address }}"
          dhcp:
            dns_servers: "{{ dns_servers }}"
            domain_search: "{{ domain_search }}"
            domain_name: "{{ domain_name }}"
            tftp_server_name: "{{ tftp_server_name }}"
            boot_file: "{{ boot_file }}"
            dhcp_server_ip: "{{ dhcp_server_address }}"

  - name: External subnet with NAT
    ntnx_subnets:
      state: present
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      name: " External subnet with NAT "
      external_subnet:
        vlan_id: "{{ vlan_id }}"
        enable_nat: True
        cluster:
          name: "{{ cluster_name }}"
        ipam:
          network_ip: "{{ network_ip }}"
          network_prefix: "{{ network_prefix }}"
          gateway_ip: "{{ gateway_ip_address }}"
          ip_pools:
            - start_ip: "{{ dhcp.start_address }}"
              end_ip: "{{ dhcp.end_address }}"
            - start_ip: "{{ static.start_address }}"
              end_ip: "{{ static.end_address }}"

  - name: Overlay Subnet with IP_pools and DHCP
    ntnx_subnets:
      state: present
      nutanix_host: "{{ ip }}"
      validate_certs: false
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      name: Overlay Subnet with IP_pools and DHCP
      overlay_subnet:
        vpc:
          name: "{{ vpc_name }}"
        ipam:
          network_ip: "{{ network_ip }}"
          network_prefix: "{{ network_prefix }}"
          gateway_ip: "{{ gateway_ip_address }}"
          ip_pools:
            - start_ip: "{{ start_address }}"
              end_ip: "{{ end_address }}"
          dhcp:
            dns_servers: "{{ dns_servers }}"
            domain_search: "{{ domain_search }}"
            domain_name: "{{ domain_name }}"
            tftp_server_name: "{{ tftp_server_name }}"
            boot_file: "{{ boot_file }}"

  - name: Delete subnets
    ntnx_subnets:
      state: absent
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: false
      subnet_uuid: "{{ subnet_uuid }}"
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The subnet kind metadata
  returned: always
  type: dict
  sample: {
                "categories": {},
                "categories_mapping": {},
                "creation_time": "2022-02-13T14:19:41Z",
                "kind": "subnet",
                "last_update_time": "2022-02-13T14:19:44Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "spec_version": 1,
                "uuid": "f5043dec-aef6-4939-ba1b-81cdbd8f3bd2"
            }
spec:
  description: An intentful representation of a subnet spec
  returned: always
  type: dict
  sample: {
                "cluster_reference": {
                    "kind": "cluster",
                    "name": "auto_cluster_prod_1a642ea0a5c3",
                    "uuid": "0005d734-09d4-0462-185b-ac1f6b6f97e2"
                },
                "name": "VLAN subnet without IPAM",
                "resources": {
                    "subnet_type": "VLAN",
                    "virtual_switch_uuid": "91639374-c0b9-48c3-bfc1-f9c89343b3e7",
                    "vlan_id": 205,
                    "vswitch_name": "br0"
                }
            }
status:
  description: An intentful representation of a subnet status
  returned: always
  type: dict
  sample:  {
                "cluster_reference": {
                    "kind": "cluster",
                    "name": "auto_cluster_prod_1a642ea0a5c3",
                    "uuid": "0005d734-09d4-0462-185b-ac1f6b6f97e2"
                },
                "execution_context": {
                    "task_uuid": [
                        "ae015bd7-eada-4e23-a225-4f02f9b2b21e"
                    ]
                },
                "name": "VLAN subnet without IPAM",
                "resources": {
                    "subnet_type": "VLAN",
                    "virtual_switch_uuid": "91639374-c0b9-48c3-bfc1-f9c89343b3e7",
                    "vlan_id": 205,
                    "vswitch_name": "br0"
                },
                "state": "COMPLETE"
            }
subnet_uuid:
  description: The created subnet uuid
  returned: always
  type: str
  sample: "f5043dec-aef6-4939-ba1b-81cdbd8f3bd2"
task_uuid:
  description: The task uuid for the creation
  returned: always
  type: str
  sample: "ae015bd7-eada-4e23-a225-4f02f9b2b21e"
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.subnets import Subnet  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    ip_pool_spec = dict(start_ip=dict(type="str"), end_ip=dict(type="str"))
    dhcp_spec = dict(
        dns_servers=dict(type="list", elements="str"),
        domain_name=dict(type="str"),
        tftp_server_name=dict(type="str"),
        boot_file=dict(type="str"),
        dhcp_server_ip=dict(type="str"),
        domain_search=dict(type="list", elements="str"),
    )
    ipam_spec = dict(
        network_ip=dict(type="str"),
        network_prefix=dict(type="int"),
        gateway_ip=dict(type="str"),
        ip_pools=dict(
            type="list",
            elements="dict",
            options=ip_pool_spec,
            required_together=[("start_ip", "end_ip")],
        ),
        dhcp=dict(type="dict", options=dhcp_spec),
    )

    overlay_ipam_spec = dict(
        network_ip=dict(type="str", required=True),
        network_prefix=dict(type="int", required=True),
        gateway_ip=dict(type="str", required=True),
        ip_pools=dict(
            type="list",
            elements="dict",
            options=ip_pool_spec,
            required_together=[("start_ip", "end_ip")],
        ),
        dhcp=dict(type="dict", options=dhcp_spec),
    )

    external_ipam_spec = overlay_ipam_spec.copy()
    external_ipam_spec.pop("dhcp")

    vlan_subnet_spec = dict(
        vlan_id=dict(type="int", required=True),
        cluster=dict(
            type="dict",
            required=True,
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
        ),
        virtual_switch=dict(
            type="dict",
            required=True,
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
        ),
        ipam=dict(type="dict", options=ipam_spec),
    )
    external_subnet_spec = dict(
        vlan_id=dict(type="int", required=True),
        enable_nat=dict(type="bool", default=True),
        cluster=dict(
            type="dict",
            required=True,
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
        ),
        ipam=dict(type="dict", options=external_ipam_spec, required=True),
    )
    overlay_subnet_spec = dict(
        vpc=dict(
            type="dict",
            required=True,
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
        ),
        ipam=dict(type="dict", options=overlay_ipam_spec, required=True),
    )

    module_args = dict(
        name=dict(type="str", required=False),
        subnet_uuid=dict(type="str", required=False),
        vlan_subnet=dict(type="dict", options=vlan_subnet_spec),
        external_subnet=dict(type="dict", options=external_subnet_spec),
        overlay_subnet=dict(type="dict", options=overlay_subnet_spec),
    )

    return module_args


def create_subnet(module, result):
    subnet = Subnet(module)
    spec, error = subnet.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating subnet spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = subnet.create(spec)
    subnet_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["subnet_uuid"] = subnet_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = subnet.read(subnet_uuid)
        result["response"] = resp


def delete_subnet(module, result):
    subnet_uuid = module.params["subnet_uuid"]
    if not subnet_uuid:
        result["error"] = "Missing parameter subnet_uuid in playbook"
        module.fail_json(msg="Failed deleting subnet", **result)

    subnet = Subnet(module)
    resp = subnet.delete(subnet_uuid)
    result["changed"] = True
    result["response"] = resp
    result["subnet_uuid"] = subnet_uuid
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
            ("vlan_subnet", "external_subnet", "subnet_uuid", "overlay_subnet")
        ],
        required_one_of=[  # check
            ("vlan_subnet", "external_subnet", "subnet_uuid", "overlay_subnet")
        ],
        required_if=[["state", "absent", ["subnet_uuid"]]],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "subnet_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_subnet(module, result)
    elif state == "absent":
        delete_subnet(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
