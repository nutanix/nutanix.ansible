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
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.ndb.profiles.profile_types import get_profile_type_obj  # noqa: E402
from ..module_utils.ndb.profiles.profiles import Profile  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402

profile_types_with_version_support = ["software"]
profile_types_with_wait_support = ["software"]


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
        state=dict(type="str", choices=["present", "absent"], default="present"),
        version_uuid=dict(type="str"),
        name=dict(type="str"),
        desc=dict(type="str"),
        notes=dict(type="dict", options=notes),
        db_server=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        clusters=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        database_type=dict(type="str", options=["postgres"]),
    )

    database_parameters = dict(postgres=dict(type="dict", options=postgres_params))

    module_args = dict(
        profile_uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        type=dict(
            type="str",
            choices=["software", "compute", "network", "database_parameters"],
            required=True,
        ),
        database_type=dict(type="str", options=["postgres"]),
        compute=dict(type="dict", options=compute, required=False),
        software=dict(type="dict", options=software, required=False),
        network=dict(type="dict", options=network, required=False),
        database_parameters=dict(
            type="dict", options=database_parameters, required=False
        ),
        publish=dict(type="bool", required=False),
        deprecate=dict(type="bool", required=False),
    )
    return module_args


def check_profile_idempotency(old_spec, new_spec):
    """
    This routine is used to check idempotency of a profile
    """

    if old_spec.get("name") != new_spec.get("name"):
        return False
    if old_spec.get("description") != new_spec.get("description"):
        return False

    # check cluster availability update for software profile
    if new_spec.get("updateClusterAvailability"):
        old_clusters = []
        for cluster in old_spec.get("clusterAvailability", []):
            if cluster["status"] == "ACTIVE":
                old_clusters.append(cluster["nxClusterId"])

        new_clusters = new_spec.get("availableClusterIds", [])

        if len(new_clusters) != len(old_clusters):
            return False

        # update if availibility of cluster is required
        for cluster in new_clusters:
            if cluster not in old_clusters:
                return False

    return True


def create_profile_version(module, result, profile_uuid, profile_type):
    _profile, err = get_profile_type_obj(module, profile_type=profile_type)

    spec, err = _profile.get_spec(create=True, version=True)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating profile version create spec", **result)

    if module.check_mode:
        result["response"]["version"] = spec
        return

    resp = _profile.create_version(profile_uuid, data=spec)
    version_uuid = resp.get("entityId") or resp.get("id")
    result["version_uuid"] = version_uuid
    result["response"]["version"] = resp

    if module.params.get("wait") and profile_type in profile_types_with_wait_support:

        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=10)

        resp = _profile.get_profile_by_version(
            uuid=profile_uuid, version_uuid=version_uuid
        )

    result["response"]["version"] = resp


def update_profile_version(module, result, profile_uuid, profile_type):
    config = module.params.get(profile_type)

    _profile, err = get_profile_type_obj(module, profile_type=profile_type)

    version_uuid = "latest"
    if config and config.get("version_uuid"):
        version_uuid = config.get("version_uuid")

    version = _profile.get_profile_by_version(
        uuid=profile_uuid, version_uuid=version_uuid
    )
    version_uuid = version.get("entityId") or version.get("id")
    result["version_uuid"] = version_uuid

    default_spec = _profile.get_default_version_update_spec(override_spec=version)
    spec, err = _profile.get_spec(old_spec=default_spec, version=True, update=True)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating profile version update spec", **result)

    if spec.get("propertiesMap"):
        spec.pop("propertiesMap")

    if module.check_mode:
        result["response"]["version"] = spec
        return

    resp = _profile.update_version(profile_uuid, version_uuid, spec)
    result["response"]["version"] = resp

    if (
        module.params.get("wait")
        and profile_type in profile_types_with_wait_support
        and resp.get("operationId")
    ):

        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=10)

        resp = _profile.get_profile_by_version(
            uuid=profile_uuid, version_uuid=version_uuid
        )

    result["response"]["version"] = resp


def delete_profile_version(module, result, profile_uuid, profile_type):
    _profile, err = get_profile_type_obj(profile_type=profile_type)

    config = module.params.get(profile_type)

    version_uuid = config.get("version_uuid")
    if not version_uuid:
        module.fail_json(msg="uuid is required field for version delete", **result)

    resp = _profile.delete_profile(profile_uuid=profile_uuid, version_uuid=version_uuid)
    result["response"]["version"] = resp


def version_operations(module, result, profile_uuid, profile_type):
    if profile_type not in profile_types_with_version_support:
        update_profile_version(module, result, profile_uuid, profile_type)
    else:
        profile_config = module.params.get(profile_type)
        state = profile_config.get("state", "present")
        if state == "present":
            if profile_config.get("version_uuid"):
                update_profile_version(module, result, profile_uuid, profile_type)
            else:
                create_profile_version(module, result, profile_uuid, profile_type)
        else:
            delete_profile_version(module, result, profile_uuid, profile_type)


def create_profile(module, result):
    profile_type = module.params.get("type")

    _profile, err = get_profile_type_obj(module, profile_type=profile_type)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating object for profile type {0}".format(profile_type),
            **result,
        )

    spec, err = _profile.get_spec(create=True)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create profile spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = _profile.create(data=spec)
    result["response"] = resp

    if profile_type == "software":
        uuid = resp.get("entityId")
    else:
        uuid = resp.get("id")

    if not uuid:
        return module.fail_json(
            msg="Failed fetching uuid post profile creation", **result
        )

    result["profile_uuid"] = uuid

    # polling is only required for software profile
    if module.params.get("wait") and profile_type == "software":

        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=10)

        resp = _profile.get_profiles(uuid=uuid)
        result["response"] = resp

    result["changed"] = True


def update_profile(module, result):
    uuid = module.params.get("profile_uuid")
    if not uuid:
        module.fail_json(msg="profile_uuid is required field for update", **result)

    result["profile_uuid"] = uuid

    profile_type = module.params.get("type")

    _profile, err = get_profile_type_obj(module, profile_type=profile_type)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating object for profile type {0}".format(profile_type),
            **result,
        )

    profile = _profile.get_profiles(uuid=uuid)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching profile info", **result)

    # profile update operations
    default_update_spec = _profile.get_default_update_spec(override_spec=profile)

    profile_update_spec, err = _profile.get_spec(
        old_spec=default_update_spec,
        update=True
    )
    if err:
        result["error"] = err
        module.fail_json(msg="Failed creating profile update spec", **result)

    result["response"] = {}

    if module.check_mode:
        result["response"]["profile"] = profile_update_spec

    if not module.check_mode and not check_profile_idempotency(
        profile, profile_update_spec
    ):
        resp = _profile.update(data=profile_update_spec, uuid=uuid)
        result["response"]["profile"] = resp

    # perform versions related crud as per support
    version_operations(module, result, profile_uuid=uuid, profile_type=profile_type)

    if not module.check_mode:
        resp = _profile.get_profiles(uuid=uuid)
        result["response"]["profile"] = resp
    result["changed"] = True


def delete_profile(module, result):
    profiles = Profile(module)

    uuid = module.params.get("profile_uuid")
    if not uuid:
        return module.fail_json(msg="'profile_uuid' is a required for deleting profile")

    resp = profiles.delete(uuid)

    result["response"] = resp
    result["changed"] = True


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
