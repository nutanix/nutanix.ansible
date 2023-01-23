#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_stretched_vlans
short_description: Module for create, update and delete of single instance vlan. Currently, postgres type vlan is officially supported.
version_added: 1.8.0-beta.1
description: Module for create, update and delete of single instance vlan in Nutanix vlan Service
options:
  vlan_uuid:
    description:
      - uuid for update or delete of vlan instance
    type: str
  vlans:
    description:
      - write
    type: list
    elements: str
  vlan_type:
    description:
      - wheather the vlan is mannaged or no
    type: str
    choices: ["DHCP", "Static"]
  name:
    description:
      - name of vlan instance
      - update allowed
    type: str
  desc:
    description:
      - description of vlan instance
    type: str
  gateway:
    description:
      - The gateway ip address
    type: str
  subnet_mask:
    description:
      - Subnet network address
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_ndb_base_module
  - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
# - name: create static ndb vlan
#   ntnx_ndb_stretched_vlans:
#     nutanix_host: <pc_ip>
#     nutanix_username: <user>
#     nutanix_password: <pass>
#     validate_certs: false
#     name:  test-vlan-name
#         vlans:
#             - "00000000-0000-0000-0000-000000000000"
#             - "00000000-0000-0000-0000-000000000000"
#   register: result

# - name: update ndb vlan type
#   ntnx_ndb_stretched_vlans:
#     nutanix_host: <pc_ip>
#     nutanix_username: <user>
#     nutanix_password: <pass>
#     validate_certs: false
#     vlan_uuid: "<vlan-uuid>"
#   register: result

# - name: Delete vlan
#   ntnx_ndb_stretched_vlans:
#     nutanix_host: "<pc_ip>"
#     nutanix_username: <user>
#     nutanix_password: <pass>
#     validate_certs: false
#     state: absent
#     vlan_uuid: "<vlan-uuid>"
#   register: result

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
  sample: "00000-0000-000-0000-000000"
name:
  description: vlan name
  returned: always
  type: str
  sample: "test-name"
"""

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.vlans import VLAN  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        desc=dict(type="str"),
        vlan_type=dict(type="str", choices=["DHCP", "Static"]),
        vlan_uuid=dict(type="str"),
        gateway=dict(type="str"),
        subnet_mask=dict(type="str"),
        vlans=dict(type="list", elements="str"),
    )
    return module_args


def create_stretched_vlan(module, result):
    vlan = VLAN(module, is_stretched=True)

    spec, err = vlan.get_stretched_vlan_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create vlan instance spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = vlan.create_stretched_vlan(data=spec)

    result["response"] = resp
    vlan_uuid = resp["id"]
    result["vlan_uuid"] = vlan_uuid
    result["changed"] = True


def update_stretched_vlan(module, result):
    vlan = VLAN(module, is_stretched=True)

    uuid = module.params.get("vlan_uuid")
    if not uuid:
        module.fail_json(msg="vlan_uuid is required field for update", **result)
    resp, err = vlan.get_stretched_vlan(uuid=uuid)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update stretched vlan instance spec", **result
        )

    old_spec = vlan.get_default_stretched_update_spec(override_spec=resp)

    update_spec, err = vlan.get_spec(old_spec=old_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update stretched vlan instance spec", **result
        )

    if module.check_mode:
        result["response"] = update_spec
        return

    if check_for_idempotency(old_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")
    else:
        resp = vlan.update_stretched_vlan(data=update_spec, uuid=uuid)

    result["response"] = resp
    result["vlan_uuid"] = uuid
    result["changed"] = True


def delete_stretched_vlan(module, result):
    vlan = VLAN(module, is_stretched=True)

    uuid = module.params.get("vlan_uuid")
    if not uuid:
        module.fail_json(msg="vlan_uuid is required field for delete", **result)

    resp = vlan.delete_stretched_vlan(uuid)

    result["response"] = resp
    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):

    for key, value in update_spec.items():
        if old_spec.get(key) != value:
            return False

    return True


def run_module():

    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        required_if=[
            ("state", "present", ("name", "vlan_uuid"), True),
            ("state", "absent", ("vlan_uuid",)),
        ],
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "vlan_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("vlan_uuid"):
            update_stretched_vlan(module, result)
        else:
            create_stretched_vlan(module, result)
    else:
        delete_stretched_vlan(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
