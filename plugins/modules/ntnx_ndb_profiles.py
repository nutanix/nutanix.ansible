#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_profiles
short_description: info module for ndb profiles
version_added: 1.8.0
description: 'Get profile info'
options:
      profile_uuid:
        description:
            - write
        type: str
      name:
        description:
            - write
        type: str
      desc:
        description:
            - write
        type: str
      type:
        description:
            - write
        type: str
        choices: ["software", "compute", "network", "database_parameter"]
        required: true
      database_type:
        description:
            - write
        type: str
        choices: ["postgres"]
      compute:
        description:
            - write
        type: dict
        suboptions:
            vcpus:
                description:
                    - write
                type: int
            cores_per_cpu:
                description:
                    - write
                type: int
            memory:
                description:
                    - write
                type: int
      software:
        description:
            - write
        type: dict
        suboptions:
            topology:
                description:
                    - write
                type: str
                choices: ["single", "cluster", "all"]
            state:
                description:
                    - write
                type: str
                choices: ["present", "absent"]
                default: "present"
            version_uuid:
                description:
                    - write
                type: str
            name:
                description:
                    - write
                type: str
            desc:
                description:
                    - write
                type: str
            notes:
                description:
                    - write
                type: dict
                suboptions:
                    os:
                        description:
                            - write
                        type: str
                    db_software:
                        description:
                            - write
                        type: str
            db_server:
                description:
                    - write
                type: dict
                suboptions:
                    name:
                        description:
                            - write
                        type: str
                    uuid:
                        description:
                            - write
                        type: str
            clusters:
                description:
                    - write
                type: list
                elements: dict
                suboptions:
                    name:
                        description:
                            - write
                        type: str
                    uuid:
                        description:
                            - write
                        type: str
            database_type:
                description:
                    - write
                type: str
                choices: ["postgres"]
      network:
        description:
            - write
        type: dict
        suboptions:
            topology:
                description:
                    - write
                type: str
                choices: ["single", "cluster", "all"]
            vlans:
                description:
                    - write
                type: list
                elements: dict
                suboptions:
                    cluster:
                        description:
                            - write
                        type: dict
                        required: true
                        suboptions:
                            name:
                                description:
                                    - write
                                type: str
                            uuid:
                                description:
                                    - write
                                type: str
                    vlan_name:
                        description:
                            - write
                        type: str
                        required: true
            enable_ip_address_selection:
                description:
                    - write
                type: bool
      database_parameters:
        description:
            - write
        type: dict
        suboptions:
            postgres:
                description:
                    - write
                type: dict
                suboptions:
                            max_connections:
                                description:
                                    - write
                                type: int
                            max_replication_slots:
                                description:
                                    - write
                                type: int
                            max_locks_per_transaction:
                                description:
                                    - write
                                type: int
                            effective_io_concurrency:
                                description:
                                    - write
                                type: int
                            timezone:
                                description:
                                    - write
                                type: str
                            max_prepared_transactions:
                                description:
                                    - write
                                type: int
                            max_wal_senders:
                                description:
                                    - write
                                type: int
                            min_wal_size:
                                description:
                                    - write
                                type: str
                            max_wal_size:
                                description:
                                    - write
                                type: str
                            wal_keep_segments:
                                description:
                                    - write
                                type: int
                            max_worker_processes:
                                description:
                                    - write
                                type: int
                            checkpoint_timeout:
                                description:
                                    - write
                                type: str
                            autovacuum:
                                description:
                                    - write
                                type: str
                                choices: ["on", "off"]
                            checkpoint_completion_target:
                                description:
                                    - write
                                type: float
                            autovacuum_freeze_max_age:
                                description:
                                    - write
                                type: int
                            autovacuum_vacuum_threshold:
                                description:
                                    - write
                                type: int
                            autovacuum_vacuum_scale_factor:
                                description:
                                    - write
                                type: float
                            autovacuum_work_mem:
                                description:
                                    - write
                                type: int
                            autovacuum_max_workers:
                                description:
                                    - write
                                type: int
                            autovacuum_vacuum_cost_delay:
                                description:
                                    - write
                                type: str
                            wal_buffers:
                                description:
                                    - write
                                type: int
                            synchronous_commit:
                                description:
                                    - write
                                type: str
                                choices: ["on", "off", "local", "remote_apply", "remote_write"]
                            random_page_cost:
                                description:
                                    - write
                                type: int
      publish:
        description:
            - write
        type: bool
      deprecate:
        description:
            - write
        type: bool
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""


"""
RETURN = r"""
"""
import time  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.ndb.profiles.profile_types import get_profile_type_obj  # noqa: E402
from ..module_utils.ndb.profiles.profiles import Profile  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402

profile_types_with_version_support = ["software"]
profile_types_with_wait_support = ["software"]

# Notes:
# 1. publish/deprecate/unpublish can only be done using update.
# 2. keep version spec as part of profile related spec,
#    as module avoids version operations if profile related spec is not found.
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
        topology=dict(type="str", choices=["single", "cluster"]),
        vlans=dict(type="list", elements="dict", options=vlan),
        enable_ip_address_selection=dict(type="bool"),
    )

    software = dict(
        topology=dict(type="str", choices=["single", "cluster"]),
        state=dict(type="str", choices=["present", "absent"], default="present"),
        version_uuid=dict(type="str"),
        name=dict(type="str"),
        desc=dict(type="str"),
        notes=dict(type="dict", options=notes),
        db_server_vm=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
    )

    database_parameter = dict(postgres=dict(type="dict", options=postgres_params))

    module_args = dict(
        profile_uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        type=dict(
            type="str",
            choices=["software", "compute", "network", "database_parameter"],
            required=False,
        ),
        database_type=dict(type="str", choices=["postgres"]),
        compute=dict(type="dict", options=compute, required=False),
        software=dict(type="dict", options=software, required=False),
        network=dict(type="dict", options=network, required=False),
        database_parameter=dict(
            type="dict", options=database_parameter, required=False
        ),
        clusters=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
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


def create_profile_version(module, result, profile_uuid, profile_obj):
    spec, err = profile_obj.get_spec(create=True, version=True)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating profile version create spec", **result)

    if module.check_mode:
        result["response"]["version"] = spec
        return

    resp = profile_obj.create_version(profile_uuid, data=spec)
    version_uuid = resp.get("entityId")
    result["version_uuid"] = version_uuid
    result["response"]["version"] = resp

    profile_type = profile_obj.get_type().lower()
    if module.params.get("wait") and profile_type in profile_types_with_wait_support and resp.get("operationId"):

        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=10)

        result["response"]["version"] = profile_obj.get_profile_by_version(
            uuid=profile_uuid, version_uuid=version_uuid
        )

    result["changed"] = True


def update_profile_version(module, result, profile_uuid, profile_obj):
    profile_type = profile_obj.get_type().lower()
    config = module.params.get(profile_type)

    version_uuid = "latest"
    if config and config.get("version_uuid"):
        version_uuid = config.get("version_uuid")

    version = profile_obj.get_profile_by_version(
        uuid=profile_uuid, version_uuid=version_uuid
    )
    version_uuid = version.get("entityId") or version.get("id")
    result["version_uuid"] = version_uuid

    engine_type = version.get("engineType")

    default_spec = profile_obj.get_default_version_update_spec(override_spec=version)

    kwargs = {
        "version": True,
        "update": True,
        "engine_type": engine_type
    }
    spec, err = profile_obj.get_spec(old_spec=default_spec, **kwargs)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating profile version update spec", **result)

    if spec.get("propertiesMap"):
        spec.pop("propertiesMap")

    if module.check_mode:
        result["response"]["version"] = spec
        return

    resp = profile_obj.update_version(profile_uuid, version_uuid, spec)
    result["response"]["version"] = resp
    result["changed"] = True

    if (
        module.params.get("wait")
        and profile_type in profile_types_with_wait_support
        and resp.get("operationId")
    ):

        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=10)

        result["response"]["version"] = profile_obj.get_profile_by_version(
            uuid=profile_uuid, version_uuid=version_uuid
        )


def delete_profile_version(module, result, profile_uuid, profile_obj):
    profile_type = profile_obj.get_type().lower()

    config = module.params.get(profile_type)

    version_uuid = config.get("version_uuid")
    if not version_uuid:
        module.fail_json(msg="uuid is required field for version delete", **result)

    resp = profile_obj.delete_version(profile_uuid=profile_uuid, version_uuid=version_uuid)
    result["response"]["version"] = resp
    result["changed"] = True


def version_operations(module, result, profile_uuid, profile_obj):
    profile_type = profile_obj.get_type().lower()
    result["profile_type"] = profile_type
    if profile_type not in profile_types_with_version_support:
        update_profile_version(module, result, profile_uuid, profile_obj)
    else:
        profile_config = module.params.get(profile_type)
        state = profile_config.get("state", "present")
        if state == "present":
            if profile_config.get("version_uuid"):
                update_profile_version(module, result, profile_uuid, profile_obj)
            else:
                create_profile_version(module, result, profile_uuid, profile_obj)
        else:
            delete_profile_version(module, result, profile_uuid, profile_obj)


def create_profile(module, result):
    profile_type = module.params.get("type")
    if not profile_type:
        return module.fail_json("'type' is required field for creating profile of certain type")

    _profile, err = get_profile_type_obj(module, profile_type=profile_type)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting object for profile type {0}".format(profile_type),
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
    uuid = resp.get("id")

    # incase there is process of replication triggered, operation info is recieved
    if profile_type=="software" and not uuid: 
        uuid = resp.get("entityId")

    if not uuid:
        return module.fail_json(
            msg="Failed fetching uuid post profile creation", **result
        )

    result["profile_uuid"] = uuid

    # polling is only required for software profile
    if module.params.get("wait") and profile_type in profile_types_with_wait_support and resp.get("operationId"):

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

    _profile = Profile(module)

    profile = _profile.get_profiles(uuid=uuid)

    profile_type = module.params.get("type") or profile.get("type", "").lower()
    if not profile_type:
        result["response"] = profile
        return module.fail_json(msg="Failed getting profile type", **result)

    _profile, err = get_profile_type_obj(module, profile_type=profile_type)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating object for profile type {0}".format(profile_type),
            **result,
        )

    # profile update operations
    default_update_spec = _profile.get_default_update_spec(override_spec=profile)

    profile_update_spec, err = _profile.get_spec(
        old_spec=default_update_spec, update=True
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
        result["changed"] = True
        if module.params.get("wait") and profile_type in profile_types_with_wait_support and resp.get("operationId"):

            ops_uuid = resp["operationId"]
            operations = Operation(module)
            time.sleep(3)  # to get operation ID functional
            operations.wait_for_completion(ops_uuid, delay=10)

            resp = _profile.get_profiles(uuid=uuid)
            result["response"]["profile"] = resp

    # perform versions related crud as per support
    # version spec needs to be part of spec of profile type
    if module.params.get(profile_type):
        version_operations(module, result, profile_uuid=uuid, profile_obj=_profile)

    if not module.check_mode:
        resp = _profile.get_profiles(uuid=uuid)
        result["response"]["profile"] = resp


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
