#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_vlans_info
short_description: info module for ndb vlans
version_added: 1.8.0-beta.1
description: 'Get vlan info'
options:
      name:
        description:
            - vlan name
        type: str
      uuid:
        description:
            - vlan id
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List all era vlans
  ntnx_ndb_vlans_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
  register: vlans

- name: get era vlans using it's name
  ntnx_ndb_vlans_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    name: "test_name"
  register: result

- name: List vlans use id
  ntnx_ndb_vlans_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of vlan>"
  register: result

"""
RETURN = r"""
response:
  description: listing all vlans
  returned: always
  type: list
  sample: []
"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.vlans import VLAN  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
    )

    return module_args


def get_vlan(module, result):
    vlan = VLAN(module)
    resp, err = vlan.get_vlan(
        uuid=module.params.get("uuid"), name=module.params.get("name")
    )

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching vlan info", **result)
    result["response"] = resp


def get_vlans(module, result):
    vlan = VLAN(module)

    resp = vlan.read()

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_vlan(module, result)
    else:
        get_vlans(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
