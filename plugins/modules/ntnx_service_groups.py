#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_service_groups
short_description: service_groups module which suports service_groups CRUD operations
version_added: 1.4.0
description: 'Create, Update, Delete service_group'
options:
  state:
    description:
      - Specify state of service_groups
      - If C(state) is set to C(present) then service_groups is created.
      - >-
        If C(state) is set to C(absent) and if the service_groups exists, then
        service_groups is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for service_groups CRUD operation to complete.
    type: bool
    required: false
    default: True
  name:
    description: service_groups Name
    required: False
    type: str
  service_group_uuid:
    description: service_group UUID
    type: str
  desc:
    description: service_groups description
    type: str
  service_details:
    type: dict
    description: List of port, protocol or icmp codes
    suboptions:
      any_icmp:
        description: any icmp code or type
        type: bool
        default: false
      tcp:
        description: List of TCP ports in the service
        type: list
        elements: str
      udp:
        description: List of UDP ports in the service
        type: list
        elements: str
      icmp:
        description: List of ICMP types and codes in the service
        type: list
        elements: dict
        suboptions:
          code:
            type: int
            description: ICMP code
          type:
            description: ICMP type
            type: int
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: create  service group with tcp and udp and icmp
  ntnx_service_groups:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    name: app_srvive_group
    desc: desc
    service_details:
      tcp:
        - "*"
      udp:
        - "10-50"
        - "60-90"
        - "99"
      any_icmp: True
  register: result

- name: create  service group with icmp
  ntnx_service_groups:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    name: icmp_srvive_group
    desc: desc
    service_details:
      icmp:
        - code: 10
        - type: 1
        - type: 2
          code: 3
  register: result

- name: update tcp service group name and description and other protocols
  ntnx_service_groups:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: False
    service_group_uuid: "{{service_group_uuid}}"
    name: updated_name
    desc: updated_desc
    service_details:
      tcp:
        - "60-90"
      icmp:
        - type: 2
          code: 3
  register: result
"""

RETURN = r"""
service_group_uuid:
  description: The created service group  uuid
  returned: always
  type: str
  sample: 00000000000-0000-0000-0000-00000000000
kind:
  description: The  service group  kind name
  returned: always
  type: str
  sample: service_group
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.service_groups import ServiceGroup  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    icmp_spec = dict(code=dict(type="int"), type=dict(type="int"))

    service_spec = dict(
        tcp=dict(type="list", elements="str"),
        udp=dict(type="list", elements="str"),
        icmp=dict(
            type="list",
            elements="dict",
            options=icmp_spec,
        ),
        any_icmp=dict(type="bool", default=False),
    )

    module_args = dict(
        name=dict(type="str"),
        desc=dict(type="str"),
        service_group_uuid=dict(type="str"),
        service_details=dict(
            type="dict", options=service_spec, mutually_exclusive=[("icmp", "any_icmp")]
        ),
    )

    return module_args


def create_service_group(module, result):
    service_group = ServiceGroup(module)
    spec, error = service_group.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating service_groups spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = service_group.create(spec)
    service_group_uuid = resp["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["service_group_uuid"] = service_group_uuid


def update_service_group(module, result):
    service_group = ServiceGroup(module)
    service_group_uuid = module.params.get("service_group_uuid")
    if not service_group_uuid:
        result["error"] = "Missing parameter service_group_uuid in playbook"
        module.fail_json(msg="Failed updating service_group", **result)
    result["service_group_uuid"] = service_group_uuid

    # read the current state of service_group
    resp = service_group.read(service_group_uuid)
    resp = resp.get("service_group")

    # new spec for updating service_group
    update_spec, error = service_group.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating service_group update spec", **result)

    # check for idempotency
    if resp == update_spec:
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. Refer docs to check for fields which can be updated"
        )

    if module.check_mode:
        result["response"] = update_spec
        return

    # update service_group
    service_group.update(update_spec, uuid=service_group_uuid, no_response=True)

    resp = service_group.read(service_group_uuid)

    result["changed"] = True
    result["response"] = resp


def delete_service_group(module, result):
    service_group_uuid = module.params["service_group_uuid"]
    if not service_group_uuid:
        result["error"] = "Missing parameter service_group_uuid in playbook"
        module.fail_json(msg="Failed deleting service_groups", **result)

    if module.check_mode:
        result["service_group_uuid"] = service_group_uuid
        result["msg"] = "Service group with uuid:{0} will be deleted.".format(service_group_uuid)
        return

    service_group = ServiceGroup(module)
    resp = service_group.delete(service_group_uuid, no_response=True)
    result["changed"] = True
    result["response"] = resp
    result["service_group_uuid"] = service_group_uuid


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "service_group_uuid"), True),
            ("state", "absent", ("service_group_uuid",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "service_group_uuid": None,
    }
    state = module.params["state"]
    if state == "absent":
        delete_service_group(module, result)
    elif module.params.get("service_group_uuid"):
        update_service_group(module, result)
    else:
        create_service_group(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
