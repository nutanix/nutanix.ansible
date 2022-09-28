#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_era_profiles_info
short_description: profile  info module
version_added: 1.7.0
description: 'Get profile info'
options:
      profile_name:
        description:
            - profile name
        type: str
      profile_id:
        description:
            - profile id
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
  - name: List profiles
    ntnx_era_profiles_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
    register: result

  - name: Get profile using name
    ntnx_profiles_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      profile_name: "profile-name"
    register: result

  - name: Get profile using id
    ntnx_profiles_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      profile_id: "profile-id"
    register: result

"""
RETURN = r"""
"""

from ..module_utils.era.base_info_module import BaseEraInfoModule  # noqa: E402
from ..module_utils.era.profiles import Profile  # noqa: E402


def get_module_spec():

    module_args = dict(
        profile_name=dict(type="str"),
        profile_id=dict(type="str"),
        profile_type=dict(type="str", choices=["Software", "Compute", "Network", "Database_Parameter"]),
        version_id=dict(type="str"),
        latest_version=dict(type="bool", default=False),

    )

    return module_args


def get_profiles_used_query(module, result):
    profile = Profile(module)
    query = {}
    if module.params.get("profile_name"):
        query["name"] = module.params["profile_name"]
    elif module.params.get("profile_id"):
        query["id"] = module.params["profile_id"]
    if module.params.get("profile_type"):
        query["type"] = module.params["profile_type"]

    resp = profile.read(query=query)

    result["response"] = resp


def get_profiles(module, result):
    profile = Profile(module)

    resp = profile.read()

    result["response"] = resp


def get_profiles_version(module, result):
    profile = Profile(module)
    endpoint = "{0}/versions/{1}".format(module.params["profile_id"], module.params.get("version_id") or "latest")

    resp = profile.read(endpoint=endpoint)

    result["response"] = resp


def run_module():
    module = BaseEraInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
        mutually_exclusive=[
            ("profile_name", "profile_id"),
            ("version_id", "latest_version"),
        ],
        required_by={"version_id": "profile_id"},
        required_if=[("latest_version", True, ("profile_id",))],

    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("version_id") or module.params.get("latest_version"):
        get_profiles_version(module, result)
    elif module.params.get("profile_name") or module.params.get("profile_id") or module.params.get("profile_type"):
        get_profiles_used_query(module, result)
    else:
        get_profiles(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
