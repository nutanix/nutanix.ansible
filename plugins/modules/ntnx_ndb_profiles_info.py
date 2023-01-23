#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_profiles_info
short_description: profile  info module
version_added: 1.8.0-beta.1
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
            - wheater the lastet version of profile or no
        type: bool
        default: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.profiles import Profile  # noqa: E402


def get_module_spec():

    queries_spec = dict(
        engine=dict(
            type="str",
            choices=[
                "oracle_database",
                "postgres_database",
                "sqlserver_database",
                "mariadb_database",
                "mysql_database",
                "saphana_database",
                "mongodb_database",
            ]
        ),
        type=dict(
            type="str",
            choices=[
                "Software",
                "Compute",
                "Network",
                "Database_Parameter",
            ]
        ),
    )

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        # profile_type=dict(
        #     type="str", choices=["Software", "Compute", "Network", "Database_Parameter"]
        # ),
        version_id=dict(type="str"),
        latest_version=dict(type="bool", default=False),
        queries=dict(
            type="dict",
            options=queries_spec,
        )
    )

    return module_args


def get_profile(module, result):
    profile = Profile(module)
    name = module.params.get("name")
    uuid = module.params.get("uuid")
    # type = module.params.get("profile_type")
    resp, err = profile.get_profiles(uuid, name) #, type)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching profile info", **result)

    result["response"] = resp


def get_profiles(module, result):
    profile = Profile(module)
    query_params = module.params.get("queries")

    resp = profile.read(query=query_params)

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
    module = NdbBaseModule(
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
        # or module.params.get("profile_type")
    ):
        get_profile(module, result)
    else:
        get_profiles(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
