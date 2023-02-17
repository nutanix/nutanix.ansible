#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_profiles_info
short_description: info module for ndb profiles
version_added: 1.8.0
description: 'Get profile info'
options:
      name:
        description:
            - profile name
        type: str
      uuid:
        description:
            - profile id
        type: str
      profile_type:
        description:
            - profile type
        type: str
        choices: ["Software", "Compute", "Network", "Database_Parameter"]
      version_id:
        description:
            - vrsion id
        type: str
      latest_version:
        description:
            - whether the lastet version of profile or no
        type: bool
        default: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List profiles
  ntnx_ndb_profiles_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
  register: profiles

- name: List Database_Parameter profiles
  ntnx_ndb_profiles_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    profile_type: Database_Parameter
  register: result

- name: List Network profiles
  ntnx_ndb_profiles_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    profile_type: Network
  register: result

- name: List Compute profiles
  ntnx_ndb_profiles_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    profile_type: Compute
  register: result

- name: List Software profiles
  ntnx_ndb_profiles_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    profile_type: Software
  register: result

- name: get era profile using era profile name
  ntnx_ndb_profiles_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    name: "test_name"
  register: result


- name: List profiles
  ntnx_ndb_profiles_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of profile>"
    latest_version: true
  register: result

"""
RETURN = r"""
response:
  description: list of db_profiles
  returned: always
  type: list
  sample: [
    {
        "dbVersion": "ALL",
        "description": "Default Database Storage Profile",
        "engineType": "Generic",
        "id": "a1c3033d-f999-47b2-8565-feced1a33503",
        "latestVersion": "1.0",
        "latestVersionId": "a1cdasdd-f999-47b2-8565-feced1a33503",
        "name": "DB_DEFAULT_STORAGE_PROFILE",
        "owner": "eacdasbf-22fb-462b-9498-949796ca1f73",
        "status": "READY",
        "systemProfile": true,
        "topology": "ALL",
        "type": "Storage",
        "versions": [
            {
                "dbVersion": "ALL",
                "deprecated": false,
                "description": "Default Database Storage Profile",
                "engineType": "Generic",
                "id": "a1c3033d-f999-47b2-8565-feced1a33503",
                "name": "DB_DEFAULT_STORAGE_PROFILE",
                "owner": "eacdsaf-22fb-462b-9498-94979dsaf73",
                "profileId": "a1c30dsa-f999-47b2-8565-fecedsa3503",
                "properties": [
                    {
                        "name": "DEFAULT_CONTAINER",
                        "secure": false,
                        "value": ""
                    },
                    {
                        "name": "MAX_VDISK_SIZE",
                        "secure": false,
                        "value": "200"
                    }
                ],
                "propertiesMap": {
                    "DEFAULT_CONTAINER": "",
                    "MAX_VDISK_SIZE": "200"
                },
                "published": true,
                "status": "READY",
                "systemProfile": false,
                "topology": "ALL",
                "type": "Storage",
                "version": "1.0",
                "versionClusterAssociation": []
            }
        ]
    }
    ]
"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.profiles.profiles import Profile  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        profile_type=dict(
            type="str", choices=["Software", "Compute", "Network", "Database_Parameter"]
        ),
        version_id=dict(type="str"),
        latest_version=dict(type="bool", default=False),
    )

    return module_args


def get_profile(module, result):
    profile = Profile(module)
    name = module.params.get("name")
    uuid = module.params.get("uuid")
    type = module.params.get("profile_type")
    resp, err = profile.get_profiles(uuid, name, type)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching profile info", **result)

    result["response"] = resp


def get_profiles(module, result):
    profile = Profile(module)

    resp = profile.read()

    result["response"] = resp


def get_profiles_version(module, result):
    profile = Profile(module)

    version_id = ""
    if module.params.get("latest_version"):
        version_id = "latest"
    else:
        version_id = module.params.get("version_id")
    resp = profile.get_profile_by_version(module.params["uuid"], version_id)

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("name", "uuid"),
            ("version_id", "latest_version"),
        ],
        required_by={"version_id": "uuid"},
        required_if=[("latest_version", True, ("uuid",))],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("version_id") or module.params.get("latest_version"):
        get_profiles_version(module, result)
    elif (
        module.params.get("name")
        or module.params.get("uuid")
        or module.params.get("profile_type")
    ):
        get_profile(module, result)
    else:
        get_profiles(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
