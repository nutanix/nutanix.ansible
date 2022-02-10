#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpcs
short_description: vpcs module which suports vpc CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete vpcs'
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
      - Specify state of vpc
      - If C(state) is set to C(present) then vpc is created.
      - >-
        If C(state) is set to C(absent) and if the vpc exists, then
        vpc is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for vpc CRUD operation to complete.
    type: bool
    required: false
    default: True
  name:
    description: vpc Name
    type: str
  vpc_uuid:
    description: vpc uuid
    type: str
  dns_servers:
    description: List of DNS servers IPs
    type: list
    elements: str
  routable_ips:
    description: Address space within the VPC which can talk externally without NAT. These are in effect when No-NAT External subnet is used.
    type: list
    elements: dict
    suboptions:
      network_ip:
        description: ip address
        type: str
      network_prefix:
        description: Subnet ip address prefix length
        type: int
  external_subnets:
    description: A subnet with external connectivity
    type: list
    elements: dict
    suboptions:
      subnet_uuid:
        description: Subnet UUID
        type: str
      subnet_name:
        description: Subnet Name
        type: str
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
"""

EXAMPLES = r"""
# TODO
"""

RETURN = r"""
# TODO
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

    resp, status = vpc.create(spec)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed creating vpc", **result)

    vpc_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["vpc_uuid"] = vpc_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp, tmp = vpc.read(vpc_uuid)
        result["response"] = resp


def delete_vpc(module, result):
    vpc_uuid = module.params["vpc_uuid"]
    if not vpc_uuid:
        result["error"] = "Missing parameter vpc_uuid in playbook"
        module.fail_json(msg="Failed deleting vpc", **result)

    vpc = Vpc(module)
    resp, status = vpc.delete(vpc_uuid)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed deleting vpc", **result)

    result["changed"] = True
    result["response"] = resp
    result["vpc_uuid"] = vpc_uuid
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
        module.fail_json(msg="Failed creating vpc", **result)


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
