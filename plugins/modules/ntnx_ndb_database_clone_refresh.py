#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ndb_database_clone_refresh
short_description: module for database clone refresh.
version_added: 1.8.0
description: module for refreshing database clone to certain point in time or snapshot.
options:
      uuid:
        description:
            - uuid of database clone
        type: str
      snapshot_uuid:
        description:
            - snapshot uuid for clone refresh
        type: str
      timezone:
        description:
            - timezone related to pitr_timestamp given
        type: str
        default: "Asia/Calcutta"
      pitr_timestamp:
        description:
            - timestamp for point in time database cone refresh
            - format is 'yyyy-mm-dd hh:mm:ss'
        type: str
      latest_snapshot:
        description:
            - write
        type: bool
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
      - nutanix.ncp.ntnx_logger
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: create spec for refresh clone to a pitr timestamp
  ntnx_ndb_database_clone_refresh:
    uuid: "{{clone_uuid}}"
    pitr_timestamp: "2023-02-04 07:29:36"
    timezone: "UTC"
  register: result
  check_mode: true

- name: refresh db clone
  ntnx_ndb_database_clone_refresh:
    uuid: "{{clone_uuid}}"
    snapshot_uuid: "{{snapshot_uuid}}"
  register: result
"""
RETURN = r"""
response:
  description: An intentful representation of a clone status
  returned: always
  type: dict
  sample: {
    "id": "4b86551d-168f-405b-a888-89ac9082bdff",
    "name": "ansible-clone-updated-updated-updated-updated3s",
    "description": "ansible-clone-desc-updated-updated",
    "dateCreated": "2023-02-28 06:52:31",
    "dateModified": "2023-02-28 07:20:10",
    "properties": [
        {
            "ref_id": "4b86551d-168f-405b-a888-89ac9082bdff",
            "name": "CLONE_PD_OBJ_LIST",
            "value": "9f491f43-e343-45d7-b552-5f38a647e018",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "4b86551d-168f-405b-a888-89ac9082bdff",
            "name": "primaryHost",
            "value": "e748bcb4-a2bb-4b6b-bb9e-1cbfe7ff0e30",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "4b86551d-168f-405b-a888-89ac9082bdff",
            "name": "BASE_SIZE",
            "value": "{\"clusterStorage\": {\"0a3b964f-8616-40b9-a564-99cf35f4b8d8\":
                    {\"9b8f4814-4536-42ef-9760-73341dbdc85a\": {\"size\": 304740352, \"allocatedSize\": 0, \"usedSize\": 0, \"unit\": \"B\"},
                     \"ffdb3000-22bc-4994-86f5-5bb668422e5e\": {\"size\": 303677440, \"allocatedSize\": 0, \"usedSize\": 0, \"unit\": \"B\"},
                     \"55034431-4f5b-48e0-bc58-13676bf9ed9b\": {\"size\": 9267200, \"allocatedSize\": 0, \"usedSize\": 0, \"unit\": \"B\"},
                     \"57e55810-0702-4f63-87b9-ff67921b6466\"
                     : {\"size\": 5439488, \"allocatedSize\": 0, \"usedSize\": 0, \"unit\": \"B\"}}}}",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "4b86551d-168f-405b-a888-89ac9082bdff",
            "name": "version",
            "value": "10.4",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "4b86551d-168f-405b-a888-89ac9082bdff",
            "name": "vm_ip",
            "value": "xx.xx.xx.xx",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "4b86551d-168f-405b-a888-89ac9082bdff",
            "name": "postgres_software_home",
            "value": "%2Fusr%2Fpgsql-10.4",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "4b86551d-168f-405b-a888-89ac9082bdff",
            "name": "listener_port",
            "value": "2345",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "4b86551d-168f-405b-a888-89ac9082bdff",
            "name": "db_parameter_profile_id",
            "value": "6bc3ceef-1681-49fa-b65d-cd968a33775e",
            "secure": false,
            "description": null
        }
    ],
    "tags": [],
    "clustered": false,
    "clone": true,
    "eraCreated": true,
    "type": "postgres_database",
    "status": "READY",
    "timeMachineId": "2ec7d4a9-c6e6-4f51-a4bd-1af7f8ee8ca8",
    "parentTimeMachineId": "7a39664b-dfb7-4529-887c-6d91f7e18604",
    "timeZone": "UTC",
    "lastRefreshTimestamp": "2023-02-28 06:52:49",
    "sourceSnapshotId": "d8e62324-be91-4297-b116-10d42d186aff",
    "provisionOperationId": null,
    "metric": null,
    "category": "DB_GROUP_IMPLICIT",
    "parentDatabaseId": null,
    "parentSourceDatabaseId": null,
    "lcmConfig": null,
    "timeMachine": null,
    "databaseNodes": [
        {
            "id": "aa11923c-8cb6-442a-87c1-5897b3e41af1",
            "name": "ansible-clone-updated-updated-updated-updated3s",
            "description": "",
            "dateCreated": "2023-02-28 07:08:57",
            "dateModified": "2023-02-28 07:18:47",
            "properties": [],
            "tags": [],
            "databaseId": "4b86551d-168f-405b-a888-89ac9082bdff",
            "status": "READY",
            "databaseStatus": "READY",
            "primary": false,
            "dbserverId": "e748bcb4-a2bb-4b6b-bb9e-1cbfe7ff0e30",
            "softwareInstallationId": "2a3b5a9e-80c0-478d-b5da-d56dd8e6c628",
            "protectionDomainId": "9f491f43-e343-45d7-b552-5f38a647e018",
            "info": {
                "secureInfo": null,
                "info": null
            },
            "metadata": null,
            "dbserver": null,
            "protectionDomain": null
        }
    ],
    "linkedDatabases": [
        {
            "id": "7827ece1-7c86-46f1-8596-1b77ea179e87",
            "name": "postgres",
            "databaseName": "postgres",
            "description": null,
            "status": "READY",
            "databaseStatus": "READY",
            "parentDatabaseId": "4b86551d-168f-405b-a888-89ac9082bdff",
            "parentLinkedDatabaseId": "6e3733cf-2994-49d2-945c-c1873564be97",
            "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
            "dateCreated": "2023-02-28 07:18:16",
            "dateModified": "2023-02-28 07:18:16",
            "timeZone": null,
            "info": {
                "secureInfo": null,
                "info": {
                    "created_by": "system"
                }
            },
            "metadata": null,
            "metric": null,
            "tags": [],
            "parentDatabaseType": null,
            "parentDatabaseName": null,
            "snapshotId": null
        },
        {
            "id": "5251f347-8562-4bf3-aeb6-2105fc49cace",
            "name": "prad",
            "databaseName": "prad",
            "description": null,
            "status": "READY",
            "databaseStatus": "READY",
            "parentDatabaseId": "4b86551d-168f-405b-a888-89ac9082bdff",
            "parentLinkedDatabaseId": "779f1f6a-502d-4ffd-9030-d21447c5ca3d",
            "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
            "dateCreated": "2023-02-28 07:18:16",
            "dateModified": "2023-02-28 07:18:16",
            "timeZone": null,
            "info": {
                "secureInfo": null,
                "info": {
                    "created_by": "user"
                }
            },
            "metadata": null,
            "metric": null,
            "tags": [],
            "parentDatabaseType": null,
            "parentDatabaseName": null,
            "snapshotId": null
        },
        {
            "id": "df365e63-5b15-4d04-902f-2e871d7f339b",
            "name": "template1",
            "databaseName": "template1",
            "description": null,
            "status": "READY",
            "databaseStatus": "READY",
            "parentDatabaseId": "4b86551d-168f-405b-a888-89ac9082bdff",
            "parentLinkedDatabaseId": "d013a63f-c9ba-4533-989d-57e57d8a4d6f",
            "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
            "dateCreated": "2023-02-28 07:18:16",
            "dateModified": "2023-02-28 07:18:16",
            "timeZone": null,
            "info": {
                "secureInfo": null,
                "info": {
                    "created_by": "system"
                }
            },
            "metadata": null,
            "metric": null,
            "tags": [],
            "parentDatabaseType": null,
            "parentDatabaseName": null,
            "snapshotId": null
        },
        {
            "id": "82d14427-382e-4e3b-99e1-5359bb5f7abc",
            "name": "template0",
            "databaseName": "template0",
            "description": null,
            "status": "READY",
            "databaseStatus": "READY",
            "parentDatabaseId": "4b86551d-168f-405b-a888-89ac9082bdff",
            "parentLinkedDatabaseId": "c18419fd-df31-4e54-b35a-ee004c0faafb",
            "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
            "dateCreated": "2023-02-28 07:18:16",
            "dateModified": "2023-02-28 07:18:16",
            "timeZone": null,
            "info": {
                "secureInfo": null,
                "info": {
                    "created_by": "system"
                }
            },
            "metadata": null,
            "metric": null,
            "tags": [],
            "parentDatabaseType": null,
            "parentDatabaseName": null,
            "snapshotId": null
        }
    ],
    "databases": null,
}
uuid:
  description: Database clone uuid
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""
import time  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.v3.ndb.database_clones import DatabaseClone  # noqa: E402
from ..module_utils.v3.ndb.operations import Operation  # noqa: E402


def get_module_spec():

    module_args = dict(
        uuid=dict(type="str", required=False),
        snapshot_uuid=dict(type="str", required=False),
        timezone=dict(type="str", default="Asia/Calcutta", required=False),
        pitr_timestamp=dict(type="str", required=False),
        latest_snapshot=dict(type="bool", required=False),
    )
    return module_args


def refresh_clone(module, result):
    db_clone = DatabaseClone(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(
            msg="uuid is required field for database clone refresh", **result
        )

    spec, err = db_clone.get_clone_refresh_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed getting spec for database clone refresh", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = db_clone.refresh(uuid=uuid, data=spec)
    result["response"] = resp
    result["uuid"] = uuid

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid)
        resp = db_clone.read(uuid)
        result["response"] = resp

    result["changed"] = True


def run_module():
    mutually_exclusive_list = [
        ("snapshot_uuid", "pitr_timestamp", "latest_snapshot"),
    ]
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            (
                "state",
                "present",
                ("snapshot_uuid", "pitr_timestamp", "latest_snapshot"),
                True,
            )
        ],
        mutually_exclusive=mutually_exclusive_list,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    refresh_clone(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
