#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_clones_info
short_description: clone  info module
version_added: 1.8.0-beta.1
description: 'Get clone info'
options:
      name:
        description:
            - clone name
        type: str
      uuid:
        description:
            - clone id
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List all era db clones
  ntnx_ndb_clones_info:
    ndb_host: "<ndb_era_ip>"
    ndb_username: "<ndb_era_username>"
    ndb_password: "<ndb_era_password>"
    validate_certs: false
  register: clones

- name: get era clones using it's name
  ntnx_ndb_clones_info:
    ndb_host: "<ndb_era_ip>"
    ndb_username: "<ndb_era_username>"
    ndb_password: "<ndb_era_password>"
    validate_certs: false
    name: "test_clone"
  register: result

- name: List clones use id
  ntnx_ndb_clones_info:
    ndb_host: "<ndb_era_ip>"
    ndb_username: "<ndb_era_username>"
    ndb_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of clone>"
  register: result

"""
RETURN = r"""
"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.clones import Clone  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
    )

    return module_args


def get_clone(module, result):
    clone = Clone(module)
    if module.params.get("name"):
        name = module.params["name"]
        resp, err = clone.get_clone(name=name)
    else:
        uuid = module.params["uuid"]
        resp, err = clone.get_clone(uuid=uuid)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching clone info", **result)

    result["response"] = resp


def get_clones(module, result):
    clone = Clone(module)

    resp = clone.read()

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_clone(module, result)
    else:
        get_clones(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
