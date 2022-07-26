#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.address_groups import AddressGroup  # noqa: E402


def get_module_spec():
    subnet_detail = dict(
        network_prefix=dict(type=int, required=True),
        network_ip=dict(type="str", required=True),
    )

    module_args = dict(
        address_group_uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        subnets=dict(
            type="list", elements="dict", options=subnet_detail, required=False
        ),
    )
    return module_args


def create_address_group(module, result):
    _address_group = AddressGroup(module)
    name = module.params["name"]
    if _address_group.get_uuid(name):
        module.fail_json(msg="Address group with given name already exists", **result)

    spec, err = _address_group.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create Address group spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = _address_group.create(data=spec)

    # read current state of address group
    address_group = _address_group.read(uuid=resp["uuid"])
    result["response"] = address_group["address_group"]
    result["changed"] = True
    result["address_group_uuid"] = address_group["uuid"]


def update_address_group(module, result):
    _address_group = AddressGroup(module)
    uuid = module.params["address_group_uuid"]
    result["address_group_uuid"] = uuid

    resp = _address_group.read(uuid=uuid)
    address_group = resp["address_group"]
    address_group.pop("address_group_string")
    update_spec, err = _address_group.get_spec(address_group)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create Address group update spec", **result
        )

    # check for idempotency
    if update_spec == address_group:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    if module.check_mode:
        result["response"] = update_spec
        return

    _address_group.update(data=update_spec, uuid=uuid, no_response=True)
    resp = _address_group.read(uuid=uuid)
    result["response"] = resp["address_group"]
    result["changed"] = True


def delete_address_group(module, result):
    address_group = AddressGroup(module)
    uuid = module.params["address_group_uuid"]
    address_group.delete(uuid=uuid, no_response=True)
    result["response"] = {"msg": "Address group deleted successfully"}
    result["address_group_uuid"] = uuid
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "address_group_uuid"), True),
            ("state", "present", ("subnets", "address_group_uuid"), True),
            ("state", "absent", ("address_group_uuid",)),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "address_group_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        if module.params.get("address_group_uuid"):
            update_address_group(module, result)
        else:
            create_address_group(module, result)
    elif state == "absent":
        delete_address_group(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
