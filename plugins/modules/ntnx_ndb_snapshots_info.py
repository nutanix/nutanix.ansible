#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_snapshots_info
short_description: info module for ndb snapshots info
version_added: 1.8.0-beta.1
description: 'Get snapshots info'
options:
      uuid:
        description:
            - server id
        type: str
      get_files:
        description:
            - get snapshot files
        type: bool

extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List era snapshots
  ntnx_ndb_snapshots_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
  register: snapshots

- name: get era snapshots using it's id
  ntnx_ndb_snapshots_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of snapshot>"
  register: result

- name: get era snapshot files using it's id
  ntnx_ndb_snapshots_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of snapshot>"
    get_files: true
  register: result

"""
RETURN = r"""
response:
  description: listing all db servers
  returned: always
  type: list
  sample: [
{
                "accessLevel": null,
                "appInfoVersion": "2",
                "applicableTypes": [
                    "CONTINUOUS_EXTRA"
                ],
                "databaseNodeId": "000-0000-0000-0000",
                "databaseSnapshot": false,
                "dateCreated": "2022-11-29 09:21:26",
                "dateModified": "2022-12-01 06:22:22",
                "dbServerStorageMetadataVersion": 1,
                "dbserverId": null,
                "dbserverIp": null,
                "dbserverName": null,
                "description": null,
                "fromTimeStamp": "2022-11-29 09:20:52",
                "id": "000-0000-0000-0000",
                "info": {
                    "databaseGroupId": null,
                    "databases": null,
                    "info": null,
                    "linkedDatabases": [
                        {
                            "appConsistent": false,
                            "clone": false,
                            "databaseName": "template0",
                            "id": "000-0000-0000-0000",
                            "info": {
                                "info": {
                                    "created_by": "system"
                                }
                            },
                            "message": null,
                            "status": "READY"
                        },
                        {
                            "appConsistent": false,
                            "clone": false,
                            "databaseName": "postgres",
                            "id": "000-0000-0000-0000",
                            "info": {
                                "info": {
                                    "created_by": "system"
                                }
                            },
                            "message": null,
                            "status": "READY"
                        },
                        {
                            "appConsistent": false,
                            "clone": false,
                            "databaseName": "template1",
                            "id": "000-0000-0000-0000",
                            "info": {
                                "info": {
                                    "created_by": "system"
                                }
                            },
                            "message": null,
                            "status": "READY"
                        },
                        {
                            "appConsistent": false,
                            "clone": false,
                            "databaseName": "testdb1",
                            "id": "000-0000-0000-0000",
                            "info": {
                                "info": {
                                    "created_by": "user"
                                }
                            },
                            "message": null,
                            "status": "READY"
                        }
                    ],
                    "missingDatabases": null,
                    "replicationHistory": null,
                    "secureInfo": null
                },
                "lcmConfig": null,
                "metadata": {
                    "async": false,
                    "curationRetryCount": 0,
                    "deregisterInfo": null,
                    "fromTimeStamp": "2022-11-29 09:20:52",
                    "info": null,
                    "lastReplicationRetrySourceSnapshotId": null,
                    "lastReplicationRetryTimestamp": null,
                    "operationsUsingSnapshot": [],
                    "replicationRetryCount": 0,
                    "secureInfo": null,
                    "standby": false,
                    "toTimeStamp": "2022-11-29 09:20:52"
                },
                "metric": {
                    "lastUpdatedTimeInUTC": null,
                    "storage": {
                        "allocatedSize": 0.0,
                        "controllerAvgIoLatencyUsecs": null,
                        "controllerNumIops": null,
                        "lastUpdatedTimeInUTC": null,
                        "size": 67207168.0,
                        "unit": "B",
                        "usedSize": 0.0
                    }
                },
                "name": "era_auto_snapshot",
                "nxClusterId": "000-0000-0000-0000",
                "ownerId": "000-0000-0000-0000",
                "parentSnapshot": true,
                "parentSnapshotId": null,
                "processed": false,
                "properties": [],
                "protectionDomainId": "000-0000-0000-0000",
                "replicatedSnapshots": null,
                "sanitised": false,
                "sanitisedFromSnapshotId": null,
                "sanitisedSnapshots": null,
                "snapshotFamily": null,
                "snapshotId": "53553",
                "snapshotSize": 67207168.0,
                "snapshotTimeStamp": "2022-11-29 09:20:52",
                "snapshotTimeStampDate": 1669713652000,
                "snapshotUuid": "53553",
                "softwareDatabaseSnapshot": false,
                "softwareSnapshot": null,
                "softwareSnapshotId": "000-0000-0000-0000",
                "status": "ACTIVE",
                "tags": [],
                "timeMachineId": "000-0000-0000-0000",
                "timeZone": "UTC",
                "toTimeStamp": "2022-11-29 09:20:52",
                "type": "CONTINUOUS_EXTRA"
            },
        ]
"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.snapshots import Snapshot  # noqa: E402
from ..module_utils.utils import format_filters_map  # noqa: E402


def get_module_spec():

    filters_spec = dict(
        all=dict(type="bool"),
        database_ids=dict(type="list"),
        value=dict(type="str"),
        value_type=dict(
            type="str",
            choices=[
                "type",
                "status",
                "protection-domain-id",
                # "database-node",
                # "snapshot-id",
                "time-machine",
                # "latest"
            ]
        ),
        time_zone=dict(type="str"),
    )

    module_args = dict(
        uuid=dict(type="str"),
        get_files=dict(type="bool"),
        filters=dict(
            type="dict",
            options=filters_spec,
        )
    )

    return module_args


def get_snapshot(module, result):
    snapshot = Snapshot(module)
    uuid = module.params["uuid"]
    get_files = module.params["get_files"]
    if get_files:
        resp = snapshot.get_snapshot_files(uuid=uuid)
    else:
        resp = snapshot.read(uuid=uuid)

    result["response"] = resp
    result["snapshot_uuid"] = uuid


def get_snapshots(module, result):
    snapshot = Snapshot(module)
    query_params = module.params.get("filters")
    query_params = format_filters_map(query_params)

    resp = snapshot.get_snapshots(query_params=query_params)

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_by={"get_files": "uuid"},
        mutually_exclusive=[("uuid", "queries")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("uuid"):
        get_snapshot(module, result)
    else:
        get_snapshots(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
