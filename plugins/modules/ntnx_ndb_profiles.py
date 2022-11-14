#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
import time

__metaclass__ = type

DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.profiles import Profile
from ..module_utils.ndb.operations import Operation
from ..module_utils.utils import remove_param_with_none_value


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    postgres_params = dict(
        max_connections=dict(type="int"),
        max_replication_slots=dict(type="int"),
        max_locks_per_transaction=dict(type="int"),
        effective_io_concurrency=dict(type="int"),
        timezone=dict(type="str"),
        max_prepared_transactions=dict(type="int"),
        max_wal_senders=dict(type="int"),
        min_wal_size=dict(type="str"),
        max_wal_size=dict(type="str"),
        wal_keep_segments=dict(type="int"),
        max_worker_processes=dict(type="int"),
        checkpoint_timeout=dict(type="str"),
        autovacuum=dict(type="str", choices=["on", "off"]),
        checkpoint_completion_target=dict(type="float"),
        autovacuum_freeze_max_age=dict(type="int"),
        autovacuum_vacuum_threshold=dict(type="int"),
        autovacuum_vacuum_scale_factor=dict(type="float"),
        autovacuum_work_mem=dict(type="int"),
        autovacuum_max_workers=dict(type="int"),
        autovacuum_vacuum_cost_delay=dict(type="str"),
        wal_buffers=dict(type="int"),
        synchronous_commit=dict(
            type="str", choices=["on", "off", "local", "remote_apply", "remote_write"]
        ),
        random_page_cost=dict(type="int"),
    )

    vlan = dict(
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        vlan_name=dict(type="str", required=True),
    )

    notes = dict(os=dict(type="str"), db_software=dict(type="str"))

    version = dict(
        state=dict(type="str", choices=["present", "absent"], default="present"),
        uuid=dict(type="str"),
        name=dict(type="str"),
        desc=dict(type="str"),
        notes=dict(type="dict", options=notes),
        db_server=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        deprecate=dict(type="bool"),
    )

    compute = dict(
        vcpus=dict(type="int"),
        cores_per_cpu=dict(type="int"),
        memory=dict(type="int"),
    )

    network = dict(
        topology=dict(type="str", choices=["single", "cluster", "all"]),
        vlans=dict(type="list", elements="dict", options=vlan),
        enable_ip_address_selection=dict(type="bool"),
    )

    software = dict(
        topology=dict(type="str", choices=["single", "cluster", "all"]),
        version=dict(type="dict", options=version),
        clusters=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),    
    )

    db_params = dict(postgres=dict(type="dict", options=postgres_params))

    module_args = dict(
        profile_uuid=dict(type="str"),
        name=dict(type="str"),
        desc=dict(type="str"),
        database_type=dict(type="str", options=["postgres"]),
        compute=dict(type="dict", options=compute),
        software=dict(type="dict", options=software),
        network=dict(type="dict", options=network),
        db_params=dict(type="dict", options=db_params),
        publish=dict(type="bool"),
    )
    return module_args


def create_profile(module, result):
    profiles = Profile(module)

    spec, err = profiles.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create profile spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = profiles.create(data=spec)
    result["response"] = resp
    uuid = resp.get("entityId")
    if not uuid:
        return module.fail_json(msg="Failed fetching uuid post profile creation", **result)

    result["profile_uuid"] = uuid

    # polling is only required for software profile
    if module.params.get("wait") and module.params.get("software"):
        
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=10)
        
        resp, err = profiles.get_profiles(uuid=uuid)
        if err:
            result["error"] = err
            module.fail_json(msg="Failed fetching profile info post creation", **result)
        
        result["response"] = resp

    result["changed"] = True

def check_profile_idempotency(old_spec, new_spec):
    if old_spec.get("name") != new_spec.get("name"):
        return False
    if old_spec.get("description") != new_spec.get("description"):
        return False
    
    return True

def check_version_idempotency(old_spec, new_spec):
    if old_spec.get("name") != new_spec.get("name"):
        return False
    if old_spec.get("description") != new_spec.get("description"):
        return False
    
    if old_spec.get("published") != new_spec.get("published"):
        return False
    if old_spec.get("deprecated") != new_spec.get("deprecated"):
        return False
    
    return True

def update_software_versions(module, result, profile_uuid):
    _profiles = Profile(module)
    version = module.params["software"].get("version")
    if version.get("state") == "present":

        # update version
        if version.get("uuid"):
            old_spec = _profiles.get_profile_by_version(profile_uuid, version["uuid"])
            spec = _profiles.build_software_version_update_spec(version, old_spec)

            # do ops when required
            resp = None
            if not check_version_idempotency(old_spec, spec):
                resp = _profiles.update_version(profile_uuid, version["uuid"], spec)
                result["response"]["version"] = resp
            
            result["response"]["version_uuid"]  = version["uuid"]
            return resp
        
        else:
            # create new software profile version
            spec, err = _profiles.build_software_version_create_spec(version)
            if err:
                result["error"] = err
                module.fail_json(msg="Failed generating software version create spec", **result)

            resp = _profiles.create_version(profile_uuid, data=spec)
            result["response"]["version"] = resp
            version_uuid = resp.get("entityId")
            if not version_uuid:
                return module.fail_json(msg="Failed fetching uuid post software version creation", **result)

            result["version_uuid"] = version_uuid
            if module.params.get("wait"):
                
                ops_uuid = resp["operationId"]
                operations = Operation(module)
                time.sleep(3)  # to get operation ID functional
                operations.wait_for_completion(ops_uuid, delay=10)
                
                resp = _profiles.get_profile_by_version(uuid=profile_uuid, version_id = version_uuid)
                
                result["response"]["version"] = resp
                return resp

    elif version.get("state") == "absent":

        # delete version
        version_uuid = version.get("uuid")
        if not version_uuid:
            module.fail_json(msg="uuid is required field for version delete", **result)
        
        resp = _profiles.delete_version(profile_uuid=profile_uuid, version_uuid=version_uuid)
        result["response"]["version"] = resp
        return resp

    return None


def update_profile(module, result):
    uuid = module.params.get("profile_uuid")
    if not uuid:
        module.fail_json(msg="profile_uuid is required field for update", **result)

    result["profile_uuid"] = uuid

    _profiles = Profile(module)
    profile, err = _profiles.get_profiles(uuid=uuid)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching profile info", **result)
    
    # basic profile update spec
    profile_update_spec = _profiles.get_update_profile_spec(old_spec = profile)

    result["response"] = {}

    updated = False
    # update basic attributes of profile like name, desc, etc.
    if not check_profile_idempotency(profile, profile_update_spec):
        resp = _profiles.update(data=profile_update_spec, uuid=uuid)
        result["response"]["profile"] = resp
        updated = True
    

    # check if properties of any profile or version create/update/delete/deprecate/publish
    if module.params.get("software"):
        resp = update_software_versions(module, result, uuid)
        if resp:
            updated = True

    if not updated:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    result["changed"] = True

    if not result["response"].get("profile"):
        result["response"]["profile"], err = _profiles.get_profiles(uuid=uuid)
        if err:
            return module.fail_json(msg="Failed fetching profile info", **result) 

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
