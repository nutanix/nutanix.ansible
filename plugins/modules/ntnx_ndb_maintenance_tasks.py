#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ndb_maintenance_tasks
short_description: module to add and remove maintenance related tasks
version_added: 1.8.0
description: module to add and remove maintenance related tasks
options:
      db_server_vms:
        description:
            - list of database server vms to which maintenance tasks needs to be added
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - name of db server vm
                    - mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - uuid of db server vm
                    - mutually exclusive with C(name)
                type: str

      db_server_clusters:
        description:
            - list of database server clusters to which maintenance tasks needs to be added
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - name of db server cluster
                    - mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - uuid of db server cluster
                    - mutually exclusive with C(name)
                type: str
      maintenance_window:
        description:
            - maintenance window details
        type: dict
        required: true
        suboptions:
            name:
                description:
                    - name of maintenance window
                    - mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - uuid of maintenance window
                    - mutually exclusive with C(name)
                type: str
      tasks:
        description:
            - list of maintenance pre-post tasks
        type: list
        elements: dict
        suboptions:
            type:
                description:
                    - type of patching
                type: str
                choices: ["OS_PATCHING", "DB_PATCHING"]
            pre_task_cmd:
                description:
                    - full os command which needs to run before patching task in db server vm
                type: str
            post_task_cmd:
                description:
                    - full os command which needs to run after patching task in db server vm
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
- name: removing existing maintenance tasks for db server vm
  ntnx_ndb_maintenance_tasks:
    db_server_vms:
      - uuid: "{{db_server_uuid}}"
    maintenance_window:
      uuid: "{{maintenance.window_uuid}}"
    tasks: []
  register: result

- name: Add maintenance window task for vm
  ntnx_ndb_maintenance_tasks:
    db_server_vms:
      - name: "{{vm1_name_updated}}"
    maintenance_window:
      name: "{{maintenance.window_name}}"
    tasks:
      - type: "OS_PATCHING"
        pre_task_cmd: "python3 script.py"
        post_task_cmd: "python3 script.py"
      - type: "DB_PATCHING"
        pre_task_cmd: "python3 script.py"
        post_task_cmd: "python3 script.py"
  register: result
"""
RETURN = r"""
response:
  description: maintenance window response with associated tasks
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
  description: maintenance window uuid
  returned: always
  type: str
  sample: "be524e70-60ad-4a8c-a0ee-8d72f954d7e6"
"""

from copy import deepcopy  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.v3.ndb.maintenance_window import (  # noqa: E402
    AutomatedPatchingSpec,
    MaintenanceWindow,
)


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    automated_patching = deepcopy(
        AutomatedPatchingSpec.automated_patching_argument_spec
    )
    module_args = dict(
        db_server_vms=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        db_server_clusters=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
    )
    module_args.update(automated_patching)

    # maintenance window ID is always required for updating maintenance tasks
    module_args["maintenance_window"]["required"] = True
    return module_args


def update_maintenance_tasks(module, result):
    maintenance_window = MaintenanceWindow(module)

    spec, err = maintenance_window.get_spec(configure_automated_patching=True)
    if err:
        result["error"] = err
        err_msg = "Failed getting spec for updating maintenance tasks"
        module.fail_json(msg=err_msg, **result)

    uuid = spec.get("maintenanceWindowId")

    if not uuid:
        return module.fail_json(msg="Failed fetching maintenance window uuid")

    result["uuid"] = uuid
    if module.check_mode:
        result["response"] = spec
        return

    maintenance_window.update_tasks(data=spec)

    query = {"load-task-associations": True, "load-entities": True}
    resp = maintenance_window.read(uuid=uuid, query=query)
    result["response"] = resp
    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("db_server_vms", "db_server_clusters"), True)
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    update_maintenance_tasks(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
