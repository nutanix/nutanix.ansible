#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_snapshots_info
short_description: info module for ndb snapshots info
version_added: 1.8.0-beta.1
description: 'Get snapshots info'
options:
      uuid:
        description:
            - server id
        type: str
      get_files:
        description:
            - get snapshot files
        type: bool

extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List era snapshots
  ntnx_ndb_snapshots_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
  register: snapshots

- name: get era snapshots using it's id
  ntnx_ndb_snapshots_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of snapshot>"
  register: result

- name: get era snapshot files using it's id
  ntnx_ndb_snapshots_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of snapshot>"
    get_files: true
  register: result

"""
RETURN = r"""
response:
  description: listing all db servers
  returned: always
  type: list
  sample: [
  
        ]
"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.snapshots import Snapshots  # noqa: E402


def get_module_spec():

    module_args = dict(
        uuid=dict(type="str"),
        get_files=dict(type="bool"),
    )

    return module_args


def get_snapshot(module, result):
    snapshot = Snapshots(module)
    uuid = module.params["uuid"]
    get_files = module.params["get_files"]
    if get_files:
        resp = snapshot.get_snapshot_files(uuid=uuid)
    else:
        resp = snapshot.read(uuid=uuid)

    result["response"] = resp
    result["snapshot_uuid"] = uuid


def get_snapshots(module, result):
    snapshot = Snapshots(module)

    resp = snapshot.read()

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_by={"get_files": "uuid"},
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("uuid"):
        get_snapshot(module, result)
    else:
        get_snapshots(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
