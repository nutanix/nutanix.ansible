#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_vlans
short_description: Module for create, update and delete of single instance vlan. Currently, postgres type vlan is officially supported.
version_added: 1.8.0-beta.1
description: Module for create, update and delete of single instance vlan in Nutanix vlan Service
options:
  vlan_uuid:
    description:
      - uuid for update or delete of vlan instance
    type: str
  name:
    description:
      - name of vlan instance
      - update allowed
    type: str
  vlan_type:
    description:
      - write
    type: str
    choices: ["DHCP", "Static"]
  cluster:
        description:
          - write
        type: dict
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
  gateway:
    description:
      - write
    type: str
  subnet_mask:
    description:
      - write
    type: str
  primary_dns:
    description:
      - write
    type: str
  secondary_dns:
    description:
      - write
    type: str
  dns_domain:
    description:
      - write
    type: str
  ip_pool:
        description:
          - write
        type: dict
        suboptions:
            start_ip:
                description:
                - write
                type: str
            end_ip:
                description:
                - write
                type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_ndb_base_module
  - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: Create postgres vlan instance using with new vm
  ntnx_ndb_vlans:
    name: "test"
    vlan_type: "DHCP"
  register: vlan
"""

RETURN = r"""
response:
  description: vlan creation response after provisioning
  returned: always
  type: dict
  sample: {}
vlan_uuid:
  description: created vlan UUID
  returned: always
  type: str
  sample: "be524e70-60ad-4a8c-a0ee-8d72f954d7e6"
"""

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.vlans import VLAN  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    ip_pool_spec = dict(start_ip=dict(type="str"), end_ip=dict(type="str"))

    module_args = dict(
        name=dict(type="str"),
        vlan_type=dict(type="str", choices=["DHCP", "Static"]),
        vlan_uuid=dict(type="str"),
        cluster=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        ip_pools=dict(
            type="list",
            elements="dict",
            options=ip_pool_spec,
            required_together=[("start_ip", "end_ip")],
        ),
        remove_ip_pools=dict(type="list", elements="str"),
        gateway=dict(type="str"),
        subnet_mask=dict(type="str"),
        primary_dns=dict(type="str"),
        secondary_dns=dict(type="str"),
        dns_domain=dict(type="str"),
    )
    return module_args


def create_vlan(module, result):
    vlan = VLAN(module)

    name = module.params["name"]
    uuid, err = vlan.get_uuid(name)
    if uuid:
        module.fail_json(msg="vlan instance with given name already exists", **result)

    spec, err = vlan.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create vlan instance spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = vlan.create(data=spec)
    result["response"] = resp
    vlan_uuid = resp["id"]
    result["vlan_uuid"] = vlan_uuid
    result["changed"] = True


def update_vlan(module, result):
    vlan = VLAN(module)

    uuid = module.params.get("vlan_uuid")
    ip_pools = module.params.pop("ip_pools", None)
    remove_ip_pools = module.params.pop("remove_ip_pools", None)
    if not uuid:
        module.fail_json(msg="vlan_uuid is required field for update", **result)

    resp, err = vlan.get_vlan(uuid=uuid, detailed=False)

    old_spec = vlan.get_default_update_spec(override_spec=resp)

    update_spec, err = vlan.get_spec(old_spec=old_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update vlan instance spec", **result)

    if module.check_mode:
        result["response"] = update_spec
        return

    if check_for_idempotency(old_spec, update_spec) and not remove_ip_pools and not ip_pools:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = vlan.update(data=update_spec, uuid=uuid)

    if remove_ip_pools:
        vlan.remove_ip_pools(vlan_uuid=uuid, ip_pools=remove_ip_pools)
    if ip_pools:
        resp = vlan.add_ip_pools(vlan_uuid=uuid, ip_pools=ip_pools)


    result["response"] = resp
    result["vlan_uuid"] = uuid
    result["changed"] = True


def delete_vlan(module, result):
    vlan = VLAN(module)

    uuid = module.params.get("vlan_uuid")
    if not uuid:
        module.fail_json(msg="vlan_uuid is required field for delete", **result)

    resp = vlan.delete(uuid)

    result["response"] = resp
    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):

    for key, value in update_spec.items():
        if old_spec.get(key) != value:
            return False

    return True


def run_module():
    mutually_exclusive_list = [
        ("vlan_uuid", "name"),
    ]
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        mutually_exclusive=mutually_exclusive_list,
        required_if=[
            ("state", "present", ("name", "vlan_uuid"), True),
            ("state", "absent", ("vlan_uuid",)),
        ],
        required_by={"remove_ip_pools": "vlan_uuid"},
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "vlan_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("vlan_uuid"):
            update_vlan(module, result)
        else:
            create_vlan(module, result)
    else:
        delete_vlan(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
