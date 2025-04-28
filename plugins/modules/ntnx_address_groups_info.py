#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_address_groups_info
short_description: address groups info module
version_added: 1.4.0
description: 'Get address groups info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: address_group
    address_group_uuid:
        description:
            - address group UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
- name: List all address groups
  ntnx_address_groups_info:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
  register: result

- name: List address groups using uuid criteria
  ntnx_address_groups_info:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    address_group_uuid: "<uuid>"
  register: result

- name: List address groups using filter criteria
  ntnx_address_groups_info:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    filter:
      name: "<name>"
  register: result
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description:
    - Metadata for address groups list output
    - Below struct sample is was obtained when we used length=1 for listing address groups
  returned: always
  type: dict
  sample:  {
                "kind": "address_group",
                "total_matches": 2
            }
entities:
  description:
    - entities intent response
    - Below struct sample is was obtained when we used length=1 for listing address groups
  returned: always
  type: list
  sample: [
                {
                    "address_group": {
                        "address_group_string": "",
                        "description": "test_desc5",
                        "ip_address_block_list": [
                            {
                                "ip": "10.1.1.3",
                                "prefix_length": 32
                            }
                        ],
                        "name": "test_check2"
                    },
                    "uuid": "c19c83f0-2ac9-4f5f-9c51-64484d08e5db"
                }
            ]

"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v3.prism.address_groups import AddressGroup  # noqa: E402


def get_module_spec():

    module_args = dict(
        address_group_uuid=dict(type="str"),
        kind=dict(type="str", default="address_group"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_address_group(module, result):
    address_group = AddressGroup(module)
    address_group_uuid = module.params.get("address_group_uuid")
    resp = address_group.read(address_group_uuid)

    result["response"] = resp["address_group"]


def get_address_groups(module, result):
    address_group = AddressGroup(module)
    spec, err = address_group.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating info spec for Address group", **result)
    resp = address_group.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("address_group_uuid"):
        get_address_group(module, result)
    else:
        get_address_groups(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
