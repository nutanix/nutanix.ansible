#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_database_snapshots
short_description: module for creating, updating and deleting database snapshots
version_added: 1.8.0
description:
    - module for creating, updating and deleting database snapshots
    - currently, this module only polls for snapshot create in primary source cluster
    - it doesn't poll for replication task if multiple clusters are mentioned
    - check_mode is not supported for snapshot update
options:
      snapshot_uuid:
        description:
            - snapshot uuid for delete or update
            - will be used to update if C(state) is C(present) and to delete if C(state) is C(absent)
        type: str
      name:
        description:
            - name of snapshot.
            - required for create
            - update is allowed
        type: str
      clusters:
        description:
            - list of clusters in case snapshots needs to be replicated to secondary clusters
            - if secondary clusters of time machines are mentioned, then this module won't track the replication process
            - clusters changes are not considered during update, for replication use ntnx_ndb_replicate_database_snapshots
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - name of cluster
                    - mutually_exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - uuid of cluster
                    - mutually_exclusive with c(name)
                type: str
      expiry_days:
            description:
                - expiry in days
            type: int
      remove_expiry:
            description:
                - use this flag for removing expiry schedule of snapshot
            type: bool
      time_machine_uuid:
            description:
                - time machine uuid
                - required for creation
            type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""


EXAMPLES = r"""
- name: create snapshot with expiry
  ntnx_ndb_database_snapshots:
    name: "{{snapshot_name}}2"
    time_machine_uuid: "{{time_machine_uuid}}"
    expiry_days: 4
  register: result

- name: create snapshot on secondary cluster
  ntnx_ndb_database_snapshots:
    name: "ansible-created-snapshot-on-{{cluster.cluster2.name}}"
    time_machine_uuid: "{{time_machine.uuid}}"
    clusters:
      - name: "{{cluster.cluster2.name}}"
  register: result
"""

RETURN = r"""
response:
  description: An intentful representation of a snapshot
  returned: always
  type: dict
  sample: {
    "id": "10a7fb55-bda4-4f09-9797-70af1f90e137",
    "name": "test_snapshot",
    "description": null,
    "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
    "dateCreated": "2023-02-28 07:24:25",
    "dateModified": "2023-02-28 09:27:51",
    "accessLevel": null,
    "properties": [],
    "tags": [],
    "snapshotId": "119454",
    "snapshotUuid": "119454",
    "nxClusterId": "0a3b964f-8616-40b9-a564-99cf35f4b8d8",
    "protectionDomainId": "6f555d69-df00-4cad-a714-2a96042fec5a",
    "parentSnapshotId": null,
    "timeMachineId": "7a39664b-dfb7-4529-887c-6d91f7e18604",
    "databaseNodeId": "07073f2c-8d90-437b-9bf4-ab02a11ff01d",
    "appInfoVersion": "4",
    "status": "ACTIVE",
    "type": "MANUAL",
    "applicableTypes": [
        "MANUAL"
    ],
    "snapshotTimeStamp": "2023-02-28 07:23:58",
    "info": {
        "secureInfo": null,
        "info": null,
        "linkedDatabases": [
            {
                "id": "d013a63f-c9ba-4533-989d-57e57d8a4d6f",
                "databaseName": "template1",
                "status": "READY",
                "info": {
                    "info": {
                        "created_by": "system"
                    }
                },
                "appConsistent": false,
                "message": null,
                "clone": false
            },
            {
                "id": "c18419fd-df31-4e54-b35a-ee004c0faafb",
                "databaseName": "template0",
                "status": "READY",
                "info": {
                    "info": {
                        "created_by": "system"
                    }
                },
                "appConsistent": false,
                "message": null,
                "clone": false
            },
            {
                "id": "779f1f6a-502d-4ffd-9030-d21447c5ca3d",
                "databaseName": "prad",
                "status": "READY",
                "info": {
                    "info": {
                        "created_by": "user"
                    }
                },
                "appConsistent": false,
                "message": null,
                "clone": false
            },
            {
                "id": "6e3733cf-2994-49d2-945c-c1873564be97",
                "databaseName": "postgres",
                "status": "READY",
                "info": {
                    "info": {
                        "created_by": "system"
                    }
                },
                "appConsistent": false,
                "message": null,
                "clone": false
            }
        ],
        "databases": null,
        "databaseGroupId": null,
        "missingDatabases": null,
        "replicationHistory": null
    },
    "metadata": {
        "secureInfo": null,
        "info": null,
        "deregisterInfo": null,
        "fromTimeStamp": "2023-02-28 07:23:58",
        "toTimeStamp": "2023-02-28 07:23:58",
        "replicationRetryCount": 0,
        "lastReplicationRetryTimestamp": null,
        "lastReplicationRetrySourceSnapshotId": null,
        "async": false,
        "standby": false,
        "curationRetryCount": 0,
        "operationsUsingSnapshot": []
    },
    "metric": {
        "lastUpdatedTimeInUTC": null,
        "storage": {
            "lastUpdatedTimeInUTC": null,
            "controllerNumIops": null,
            "controllerAvgIoLatencyUsecs": null,
            "size": 3.5749888E7,
            "allocatedSize": 0.0,
            "usedSize": 0.0,
            "unit": "B"
        }
    },
    "softwareSnapshotId": "e08b73dd-9503-4053-8a01-4bfe59f3feb4",
    "softwareDatabaseSnapshot": false,
    "dbServerStorageMetadataVersion": 2,
    "sanitised": false,
    "sanitisedFromSnapshotId": null,
    "timeZone": "UTC",
    "processed": false,
    "databaseSnapshot": false,
    "fromTimeStamp": "2023-02-28 07:23:58",
    "toTimeStamp": "2023-02-28 07:23:58",
    "dbserverId": null,
    "dbserverName": null,
    "dbserverIp": null,
    "replicatedSnapshots": null,
    "softwareSnapshot": null,
    "sanitisedSnapshots": null,
    "snapshotFamily": null,
    "snapshotTimeStampDate": 1677569038000,
    "lcmConfig": null,
    "parentSnapshot": true,
    "snapshotSize": 3.5749888E7
}
snapshot_uuid:
  description: snapshot uuid
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""
import time  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.v3.ndb.operations import Operation  # noqa: E402
from ..module_utils.v3.ndb.snapshots import Snapshot  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    module_args = dict(
        snapshot_uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        time_machine_uuid=dict(type="str", required=False),
        clusters=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        expiry_days=dict(type="int", required=False),
        remove_expiry=dict(type="bool", required=False),
    )
    return module_args


# Notes:
# 1. Currently we only poll for source snapshot create. Replication task is not polled.

# Create snapshot
def create_snapshot(module, result):
    time_machine_uuid = module.params.get("time_machine_uuid")
    if not time_machine_uuid:
        return module.fail_json(
            msg="time_machine_uuid is required for creating snapshot"
        )

    snapshots = Snapshot(module)
    spec, err = snapshots.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating snapshot create spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = snapshots.create_snapshot(time_machine_uuid, spec)
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)
        operations.wait_for_completion(ops_uuid, delay=5)

        # get snapshot info after its finished
        resp, err = snapshots.get_snapshot(
            time_machine_uuid=time_machine_uuid, name=module.params.get("name")
        )
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed fetching snapshot info post creation", **result
            )
        result["response"] = resp
        result["snapshot_uuid"] = resp.get("id")

    result["changed"] = True


def verify_snapshot_expiry_idempotency(old_spec, new_spec):
    if old_spec.get("expireInDays") != new_spec.get("expireInDays"):
        return False
    return True


def update_snapshot(module, result):
    uuid = module.params.get("snapshot_uuid")
    if not uuid:
        module.fail_json(msg="snapshot_uuid is required field for update", **result)

    # get current details of snapshot
    _snapshot = Snapshot(module)
    snapshot = _snapshot.read(uuid=uuid)

    # compare and update accordingly
    updated = False

    # check if rename is required
    if module.params.get("name") and module.params.get("name") != snapshot.get("name"):
        spec = _snapshot.get_rename_snapshot_spec(name=module.params["name"])
        snapshot = _snapshot.rename_snapshot(uuid=uuid, data=spec)
        updated = True

    # check if update/removal of expiry schedule is required
    if module.params.get("remove_expiry"):
        spec = _snapshot.get_remove_expiry_spec(uuid=uuid, name=snapshot.get("name"))
        snapshot = _snapshot.remove_expiry(uuid=uuid, data=spec)
        updated = True

    elif module.params.get("expiry_days"):
        spec = _snapshot.get_expiry_update_spec(config=module.params)
        lcm_config = snapshot.get("lcmConfig", {}) or {}
        expiry_details = lcm_config.get("expiryDetails", {})
        if not verify_snapshot_expiry_idempotency(
            expiry_details, spec.get("lcmConfig", {}).get("expiryDetails", {})
        ):
            snapshot = _snapshot.update_expiry(uuid, spec)
            updated = True

    if not updated:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    snapshot = _snapshot.read(
        uuid=uuid, query={"load-replicated-child-snapshots": True}
    )
    result["snapshot_uuid"] = uuid
    result["response"] = snapshot
    result["changed"] = True


# Delete snapshot
def delete_snapshot(module, result):
    snapshot_uuid = module.params.get("snapshot_uuid")
    if not snapshot_uuid:
        module.fail_json(msg="snapshot_uuid is required field for delete", **result)

    snapshots = Snapshot(module)
    resp = snapshots.delete(uuid=snapshot_uuid)

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get ops ID functional
        resp = operations.wait_for_completion(ops_uuid, delay=2)

    result["response"] = resp
    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ("snapshot_uuid", "time_machine_uuid"),
            ("remove_expiry", "expiry_days"),
        ],
        required_if=[
            ("state", "present", ("name", "snapshot_uuid"), True),
            ("state", "present", ("snapshot_uuid", "time_machine_uuid"), True),
            ("state", "absent", ("snapshot_uuid",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "snapshot_uuid": None}

    if module.params["state"] == "present":
        if module.params.get("snapshot_uuid"):
            update_snapshot(module, result)
        else:
            create_snapshot(module, result)
    else:
        delete_snapshot(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
