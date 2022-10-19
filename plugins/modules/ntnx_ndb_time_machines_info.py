#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_time_machines_info
short_description: tm  info module
version_added: 1.8.0-beta.1
description: 'Get tm info'
options:
      name:
        description:
            - time machine name
        type: str
      uuid:
        description:
            - time machine id
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List all era time machines
  ntnx_ndb_time_machines_info:
    ndb_host: "<ndb_era_ip>"
    ndb_username: "<ndb_era_username>"
    ndb_password: "<ndb_era_password>"
    validate_certs: false
  register: tms

- name: get era time machines using it's name
  ntnx_ndb_time_machines_info:
    ndb_host: "<ndb_era_ip>"
    ndb_username: "<ndb_era_username>"
    ndb_password: "<ndb_era_password>"
    validate_certs: false
    name: "test_name"
  register: result

- name: List time machines use id
  ntnx_ndb_time_machines_info:
    ndb_host: "<ndb_era_ip>"
    ndb_username: "<ndb_era_username>"
    ndb_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of time mashine>"
  register: result
"""
RETURN = r"""

"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.time_machines import TimeMachine  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
    )

    return module_args


def get_tm(module, result):
    tm = TimeMachine(module)

    uuid = module.params.get("uuid")
    name = module.params.get("name")
    resp, err = tm.get_time_machine(uuid=uuid, name=name)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching sla info", **result)
    result["response"] = resp


def get_tms(module, result):
    tm = TimeMachine(module)

    resp = tm.read()

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_tm(module, result)
    else:
        get_tms(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
