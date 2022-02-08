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
  nutanix_host:
    description:
      - PC hostname or IP address
    type: str
    required: true
  nutanix_port:
    description:
      - PC port
    type: str
    default: 9440
    required: false
  nutanix_username:
    description:
      - PC username
    type: str
    required: true
  nutanix_password:
    description:
      - PC password;
    required: true
    type: str
  validate_certs:
    description:
      - Set value to C(False) to skip validation for self signed certificates
      - This is not recommended for production setup
    type: bool
    default: true
  state:
    description:
      - Specify state of subnet
      - If C(state) is set to C(present) then subnet is created.
      - >-
        If C(state) is set to C(absent) and if the subnet exists, then
        subnet is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for subnet CRUD operation to complete.
    type: bool
    required: false
    default: True
  name:
    description: subnet Name
    required: False
    type: str
  subnet_uuid:
    description: subnet UUID
    type: str
  vlan_subnet:
    description: TO_WRITE
    type: dict
    suboptions:
      vlan_id:
        description: TO_WRITE
        type: int
        required: True
      cluster:
        description:
          - Name or UUID of the cluster on which the VM will be placed.
        type: dict
        required: True
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
          - Name or UUID of the virtual_switch on which the VM will be placed.
        type: dict
        required: True
        suboptions:
          name:
            description:
              - virtual switch Name
              - Mutually exclusive with (uuid)
            type: str
          uuid:
            description:
              - virtual switch UUID
              - Mutually exclusive with (name)
            type: str
      ipam:
        description:
          -  TO_WRITE
        type: dict
        suboptions:
          network_ip:
            description:
              -  TO_WRITE
            type: str
          network_prefix:
            description:
              -  TO_WRITE
            type: int
          gateway_ip:
            description:
              -  TO_WRITE
            type: str
          ip_pools:
            description:
              -  TO_WRITE
            type: list
            elements: dict
            suboptions:
              start_ip:
                description:
                  -  TO_WRITE
                type: str
              end_ip:
                description:
                  -  TO_WRITE
                type: str
          dhcp:
            description:
              -  TO_WRITE
            type: dict
            suboptions:
              dns_servers:
                description:
                  -  TO_WRITE
                type: list
                elements: str
              domain_name:
                description:
                  -  TO_WRITE
                type: str
              tftp_server_name:
                description:
                  -  TO_WRITE
                type: str
              boot_file:
                description:
                  -  TO_WRITE
                type: str
              dhcp_server_ip:
                description:
                  -  TO_WRITE
                type: str
              domain_search:
                description:
                  -  TO_WRITE
                type: list
                elements: str
  external_subnet:
    description: TO_WRITE
    type: dict
    suboptions:
      vlan_id:
        description: TO_WRITE
        type: int
        required: True
      cluster:
        description:
          - Name or UUID of the cluster on which the VM will be placed.
        type: dict
        required: True
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
          -  TO_WRITE
        type: bool
        default: True
      ipam:
        description:
          -  TO_WRITE
        type: dict
        suboptions:
          network_ip:
            description:
              -  TO_WRITE
            type: str
          network_prefix:
            description:
              -  TO_WRITE
            type: int
          gateway_ip:
            description:
              -  TO_WRITE
            type: str
          ip_pools:
            description:
              -  TO_WRITE
            type: list
            elements: dict
            suboptions:
              start_ip:
                description:
                  -  TO_WRITE
                type: str
              end_ip:
                description:
                  -  TO_WRITE
                type: str
          dhcp:
            description:
              -  TO_WRITE
            type: dict
            suboptions:
              dns_servers:
                description:
                  -  TO_WRITE
                type: list
                elements: str
              domain_name:
                description:
                  -  TO_WRITE
                type: str
              tftp_server_name:
                description:
                  -  TO_WRITE
                type: str
              boot_file:
                description:
                  -  TO_WRITE
                type: str
              dhcp_server_ip:
                description:
                  -  TO_WRITE
                type: str
              domain_search:
                description:
                  -  TO_WRITE
                type: list
                elements: str
  overlay_subnet:
    description:
      -  TO_WRITE
    type: dict
    suboptions:
      vpc:
        description:
          -  TO_WRITE
        type: dict
        required: true
        suboptions:
          name:
            description:
              - Vpc Name
              - Mutually exclusive with (uuid)
            type: str
          uuid:
            description:
              - VPC UUID
              - Mutually exclusive with (name)
            type: str
      ipam:
        description:
          -  TO_WRITE
        type: dict
        suboptions:
          network_ip:
            description:
              -  TO_WRITE
            type: str
          network_prefix:
            description:
              -  TO_WRITE
            type: int
          gateway_ip:
            description:
              -  TO_WRITE
            type: str
          ip_pools:
            description:
              -  TO_WRITE
            type: list
            elements: dict
            suboptions:
              start_ip:
                description:
                  -  TO_WRITE
                type: str
              end_ip:
                description:
                  -  TO_WRITE
                type: str
          dhcp:
            description:
              -  TO_WRITE
            type: dict
            suboptions:
              dns_servers:
                description:
                  -  TO_WRITE
                type: list
                elements: str
              domain_name:
                description:
                  -  TO_WRITE
                type: str
              tftp_server_name:
                description:
                  -  TO_WRITE
                type: str
              boot_file:
                description:
                  -  TO_WRITE
                type: str
              dhcp_server_ip:
                description:
                  -  TO_WRITE
                type: str
              domain_search:
                description:
                  -  TO_WRITE
                type: list
                elements: str

author:
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
# TODO
"""

RETURN = r"""
# TODO
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
            required_together=[
                ("start_ip", "end_ip"),
            ],
        ),
        dhcp=dict(
            type="dict",
            options=dhcp_spec,
        ),
    )
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
        ipam=dict(type="dict", options=ipam_spec),
    )
    overlay_subnet_spec = dict(
        vpc=dict(
            type="dict",
            required=True,
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
        ),
        ipam=dict(type="dict", options=ipam_spec),
    )

    module_args = dict(
        name=dict(type="str", required=False),
        subnet_uuid=dict(type="str", required=False),
        vlan_subnet=dict(
            type="dict",
            options=vlan_subnet_spec,
        ),
        external_subnet=dict(
            type="dict",
            options=external_subnet_spec,
        ),
        overlay_subnet=dict(
            type="dict",
            options=overlay_subnet_spec,
        ),
        # TODO: Ansible module spec and spec validation
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

    resp, status = subnet.create(spec)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed creating subnet", **result)

    subnet_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["subnet_uuid"] = subnet_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp, tmp = subnet.read(subnet_uuid)
        result["response"] = resp


def delete_subnet(module, result):
    subnet_uuid = module.params["subnet_uuid"]
    if not subnet_uuid:
        result["error"] = "Missing parameter subnet_uuid in playbook"
        module.fail_json(msg="Failed deleting subnet", **result)

    subnet = Subnet(module)
    resp, status = subnet.delete(subnet_uuid)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed deleting subnet", **result)

    result["changed"] = True
    result["response"] = resp
    result["subnet_uuid"] = subnet_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp, status = task.wait_for_completion(task_uuid)
    result["response"] = resp
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed creating subnet", **result)


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ("vlan_subnet", "external_subnet", "subnet_uuid", "overlay_subnet")
        ],
        required_one_of=[  # check
            ("vlan_subnet", "external_subnet", "subnet_uuid", "overlay_subnet"),
        ],
        required_if=[
            ["state", "absent", ["subnet_uuid"]],
        ],
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
