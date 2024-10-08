#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_maintenance_windows_info
short_description: module for fetching maintenance windows info
version_added: 1.8.0
description:
    - module for fetching maintenance windows info
    - it will fetch all entities if no spec is given
    - it will also load entities and task associations
options:
    uuid:
        description:
            - uuid of maintenance window
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_info_base_module
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: get certain window info
  ntnx_ndb_maintenance_windows_info:
    uuid: "{{window2_uuid}}"

  register: result

- name: get all windows info
  ntnx_ndb_maintenance_windows_info:
  register: result
"""
RETURN = r"""
response:
  description: maintenance window response with associated tasks when uuid is used.
  returned: always
  type: dict
  sample: {
            "accessLevel": null,
            "dateCreated": "2023-02-25 06:34:44",
            "dateModified": "2023-02-28 00:00:00",
            "description": "ansible-created-window",
            "entityTaskAssoc": [
                {
                    "accessLevel": null,
                    "dateCreated": "2023-02-28 10:39:23",
                    "dateModified": "2023-02-28 10:39:23",
                    "description": null,
                    "entity": {
                        "accessLevel": null,
                        "clones": [
                            {
                                "id": "4b86551d-168f-405b-a888-89ac9082bdff",
                                "status": "READY"
                            }
                        ],
                        "clusterDescription": null,
                        "clusterEraCreated": false,
                        "clusterOwner": null,
                        "clusterStatus": null,
                        "databaseType": "postgres_database",
                        "databases": [],
                        "dateCreated": null,
                        "dateModified": null,
                        "dbClusterId": null,
                        "dbClusterName": null,
                        "description": "vm_desc",
                        "eraCreated": true,
                        "id": "e748bcb4-a2bb-4b6b-bb9e-1cbfe7ff0e30",
                        "inUse": 1,
                        "ipAddresses": [
                            "10.44.78.8"
                        ],
                        "maintenanceWindowId": "69916cc2-eb2f-4198-984a-e8a4e507d680",
                        "maintenanceWindowName": "OACrBshrexJV1",
                        "name": "postgress_server_new1",
                        "nxClusterId": "0a3b964f-8616-40b9-a564-99cf35f4b8d8",
                        "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                        "properties": [
                            {
                                "name": "compute_profile_id",
                                "value": "19b1241e-d4e0-411e-abfc-6639ba713d13"
                            },
                            {
                                "name": "software_profile_id",
                                "value": "96b3c1a2-4427-41c1-87eb-a942c52247a2"
                            },
                            {
                                "name": "software_profile_version_id",
                                "value": "ab966132-7d7d-4418-b89d-dc814c2ef1b3"
                            },
                            {
                                "name": "network_profile_id",
                                "value": "6cf4fe44-5030-41a5-a0cd-4e62a55cd85a"
                            },
                            {
                                "name": "associated_time_machine_id",
                                "value": "2ec7d4a9-c6e6-4f51-a4bd-1af7f8ee8ca8"
                            }
                        ],
                        "status": "UP",
                        "tags": []
                    },
                    "entityId": "e748bcb4-a2bb-4b6b-bb9e-1cbfe7ff0e30",
                    "entityType": "ERA_DBSERVER",
                    "id": "889aaa2f-bc84-4202-86ec-5c7bc54a260f",
                    "maintenanceWindowId": "69916cc2-eb2f-4198-984a-e8a4e507d680",
                    "maintenanceWindowOwnerId": null,
                    "name": null,
                    "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                    "payload": {
                        "prePostCommand": {
                            "postCommand": "os_post",
                            "preCommand": "os_pre"
                        }
                    },
                    "properties": null,
                    "status": "ACTIVE",
                    "tags": null,
                    "taskType": "OS_PATCHING"
                },
                {
                    "accessLevel": null,
                    "dateCreated": "2023-02-28 10:39:23",
                    "dateModified": "2023-02-28 10:39:23",
                    "description": null,
                    "entity": {
                        "accessLevel": null,
                        "clones": [
                            {
                                "id": "4b86551d-168f-405b-a888-89ac9082bdff",
                                "status": "READY"
                            }
                        ],
                        "clusterDescription": null,
                        "clusterEraCreated": false,
                        "clusterOwner": null,
                        "clusterStatus": null,
                        "databaseType": "postgres_database",
                        "databases": [],
                        "dateCreated": null,
                        "dateModified": null,
                        "dbClusterId": null,
                        "dbClusterName": null,
                        "description": "vm_desc",
                        "eraCreated": true,
                        "id": "e748bcb4-a2bb-4b6b-bb9e-1cbfe7ff0e30",
                        "inUse": 1,
                        "ipAddresses": [
                            "10.44.78.8"
                        ],
                        "maintenanceWindowId": "69916cc2-eb2f-4198-984a-e8a4e507d680",
                        "maintenanceWindowName": "OACrBshrexJV1",
                        "name": "postgress_server_new1",
                        "nxClusterId": "0a3b964f-8616-40b9-a564-99cf35f4b8d8",
                        "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                        "properties": [
                            {
                                "name": "compute_profile_id",
                                "value": "19b1241e-d4e0-411e-abfc-6639ba713d13"
                            },
                            {
                                "name": "software_profile_id",
                                "value": "96b3c1a2-4427-41c1-87eb-a942c52247a2"
                            },
                            {
                                "name": "software_profile_version_id",
                                "value": "ab966132-7d7d-4418-b89d-dc814c2ef1b3"
                            },
                            {
                                "name": "network_profile_id",
                                "value": "6cf4fe44-5030-41a5-a0cd-4e62a55cd85a"
                            },
                            {
                                "name": "associated_time_machine_id",
                                "value": "2ec7d4a9-c6e6-4f51-a4bd-1af7f8ee8ca8"
                            }
                        ],
                        "status": "UP",
                        "tags": []
                    },
                    "entityId": "e748bcb4-a2bb-4b6b-bb9e-1cbfe7ff0e30",
                    "entityType": "ERA_DBSERVER",
                    "id": "3b842672-61dd-4635-857c-606e161fed1d",
                    "maintenanceWindowId": "69916cc2-eb2f-4198-984a-e8a4e507d680",
                    "maintenanceWindowOwnerId": null,
                    "name": null,
                    "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                    "payload": {
                        "prePostCommand": {
                            "postCommand": "db_post",
                            "preCommand": "db_pre"
                        }
                    },
                    "properties": null,
                    "status": "ACTIVE",
                    "tags": null,
                    "taskType": "DB_PATCHING"
                }
            ],
            "id": "69916cc2-eb2f-4198-984a-e8a4e507d680",
            "name": "OACrBshrexJV1",
            "nextRunTime": "2023-02-28 11:00:00",
            "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
            "properties": null,
            "schedule": {
                "dayOfWeek": "TUESDAY",
                "duration": 2,
                "hour": 11,
                "minute": 0,
                "recurrence": "WEEKLY",
                "startTime": "11:00:00",
                "threshold": null,
                "timeZone": "UTC",
                "weekOfMonth": null
            },
            "status": "SCHEDULED",
            "tags": null,
            "timezone": null
        }
uuid:
  description: maintenance window uuid when queried using uuid
  returned: always
  type: str
  sample: "be524e70-60ad-4a8c-a0ee-8d72f954d7e6"
"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.maintenance_window import MaintenanceWindow  # noqa: E402


def get_module_spec():

    module_args = dict(
        uuid=dict(type="str"),
    )

    return module_args


def get_maintenance_window(module, result):
    mw = MaintenanceWindow(module)
    query = {"load-task-associations": True, "load-entities": True}
    resp = mw.read(uuid=module.params.get("uuid"), query=query)
    result["response"] = resp
    result["uuid"] = module.params.get("uuid")


def get_maintenance_windows(module, result):
    mw = MaintenanceWindow(module)
    query = {"load-task-associations": True, "load-entities": True}
    resp = mw.read(query=query)
    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("uuid"):
        get_maintenance_window(module, result)
    else:
        get_maintenance_windows(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
