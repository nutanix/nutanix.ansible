#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_slas_info
short_description: info module for ndb slas
version_added: 1.8.0-beta.1
description: 'Get sla info'
options:
      name:
        description:
            - sla name
        type: str
      uuid:
        description:
            - sla id
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List all era slas
  ntnx_ndb_slas_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
  register: slas

- name: get era slas using it's name
  ntnx_ndb_slas_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    name: "test_name"
  register: result

- name: List slas use id
  ntnx_ndb_slas_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of sla>"
  register: result

"""
RETURN = r"""
response:
  description: listing all slas
  returned: always
  type: list
  sample: [
            {
                "continuousRetention": 30,
                "currentActiveFrequency": "CONTINUOUS",
                "dailyRetention": 90,
                "dateCreated": "2022-04-08 16:21:51.591815",
                "dateModified": "2022-04-08 16:21:51.591815",
                "description": "Out of the box Gold SLA for Era Time Machines.",
                "id": "50dsad9-db5e-47af-8102-ff9dsad9bd81",
                "monthlyRetention": 12,
                "name": "DEFAULT_OOB_GOLD_SLA",
                "ownerId": "era-internal-user-id",
                "pitrEnabled": true,
                "quarterlyRetention": 35,
                "referenceCount": 1,
                "systemSla": true,
                "uniqueName": "DEFAULT_OOB_GOLD_SLA",
                "weeklyRetention": 16,
                "yearlyRetention": 0
            },
            {
                "continuousRetention": 14,
                "currentActiveFrequency": "CONTINUOUS",
                "dailyRetention": 60,
                "dateCreated": "2022-04-08 16:21:51.591815",
                "dateModified": "2022-04-08 16:21:51.591815",
                "description": "Out of the box Silver SLA for Era Time Machines.",
                "id": "27dasdd9-db5e-47af-8102-ff9354dsada0",
                "monthlyRetention": 12,
                "name": "DEFAULT_OOB_SILVER_SLA",
                "ownerId": "era-internal-user-id",
                "pitrEnabled": true,
                "quarterlyRetention": 0,
                "referenceCount": 0,
                "systemSla": true,
                "uniqueName": "DEFAULT_OOB_SILVER_SLA",
                "weeklyRetention": 12,
                "yearlyRetention": 0
            },
        ]
"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.slas import SLA  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
    )

    return module_args


def get_sla(module, result):
    sla = SLA(module)
    resp, err = sla.get_sla(
        uuid=module.params.get("uuid"), name=module.params.get("name")
    )

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching sla info", **result)
    result["response"] = resp


def get_slas(module, result):
    sla = SLA(module)

    resp = sla.read()

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_sla(module, result)
    else:
        get_slas(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
