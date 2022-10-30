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

def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    
    postgres_params = dict(
        max_connections = dict(type="int"),
        max_replication_slots = dict(type="int"),
        effective_io_concurrency = dict(type="int"),
        timezone = dict(type="str"),
        max_prepared_transactions = dict(type="int"),
        max_wal_senders = dict(type="int"),
        min_wal_size = dict(type="str"),
        max_wal_size = dict(type="str"),
        wal_keep_segments = dict(type="int"),
        max_worker_processes = dict(type="int"),
        checkpoint_timeout = dict(type="str"),
        autovacuum = dict(type="str", choices=["on", "off"]),
        checkpoint_completion_target = dict(type="float"),
        autovacuum_freeze_max_age = dict(type="int"),
        autovacuum_vacuum_threshold = dict(type="int"),
        autovacuum_vacuum_scale_factor = dict(type="float"),
        autovacuum_work_mem = dict(type="int"),
        autovacuum_max_workers = dict(type="int"),
        autovacuum_vacuum_cost_delay = dict(type="str"),
        wal_buffers = dict(type="int"),
        synchronous_commit = dict(type="str", choices=["on", "off", "local", "remote_apply", "remote_write"]),
        random_page_cost = dict(type="int"),
    )

    cluster_vlan_mapping = dict(
        cluster = dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        vlan_name = dict(type="str")
    )

    notes = dict(
        os = dict(type="str"),
        db_software = dict(type="str")
    )

    version = dict(
        state = dict(type="dict", choices=["present", "absent"], default="present"),
        uuid = dict(type="dict"),
        name = dict(type="str"),
        desc = dict(type="str"),
        notes = dict(type="dict", options=notes),
        db_server = dict(type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive),
        depreciate = dict(type="bool")
    )

    compute = dict(
        vcpus = dict(type="int"),
        cores_per_cpu = dict(type="int"),
        memory = dict(type="int"),
    )

    network = dict(
        topology = dict(type="str", choices=["single", "cluster", "all"]),
        cluster_vlan_mappings = dict(type="list", elements="dict", options=cluster_vlan_mapping)
    )

    software = dict(
        topology = dict(type="str", choices=["single", "cluster", "all"]),
        version = dict(type="dict", options=version),
    )

    db_params = dict(
        postgres = dict(type="dict", options=postgres_params)   
    )

    module_args = dict(
        profile_uuid = dict(type="str"),
        name = dict(type="str"),
        desc = dict(type="str"),
        database_type = dict(type="str", options=["postgres"]),
        compute = dict(type="dict", options=compute),
        software = dict(type="dict", options=software),
        network = dict(type="dict", options=network),
        db_params = dict(type="dict", options=db_params),
        publish = dict(type="bool"),
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
