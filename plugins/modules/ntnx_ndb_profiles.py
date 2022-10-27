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

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.profiles import Profile
from ..module_utils.utils import remove_param_with_none_value

#TO-DO:
# 1. Add publish workflow for all
# 2. Add DB server params
# 3. Add topology based params as well
def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    
    cluster_vlan_mapping = dict(
        cluster = dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        vlan_name = dict(type="str")
    )

    notes = dict(
        os = dict(type="str"),
        db_software = dict(type="str")
    )

    version = dict(
        name = dict(type="str"),
        desc = dict(type="str")
    )

    compute = dict(
        vcpus = dict(type="int"),
        cores_per_cpu = dict(type="int"),
        memory = dict(type="int"), 
    )

    network = dict(
        cluster_vlan_mappings = dict(type="list", elements="dict", options=cluster_vlan_mapping)
    )

    software = dict(
        cluster = dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        db_server = dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        base_version = dict(type="dict", option=version),
        notes = dict(type="dict", option=notes)
    )

    module_args = dict(
        profile_uuid = dict(type="str"),
        name = dict(type="str"),
        desc = dict(type="str"),
        database_type = dict(type="str", options=["postgres"]),
        compute = dict(type="dict", options=compute),
        software = dict(type="dict", options=software),
        network = dict(type="dict", options=network)
    )
    return module_args


def create_profile(module, result):
    pass


def update_profile(module, result):
    pass


def delete_profile(module, result):
    pass


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        required_if=[
            ("state", "present", ("name", "profile_uuid"), True),
            ("state", "absent", ("profile_uuid",)),
        ],
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "profile_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("profile_uuid"):
            update_profile(module, result)
        else:
            create_profile(module, result)
    else:
        delete_profile(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
