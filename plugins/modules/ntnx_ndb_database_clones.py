#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ndb_database_clones
short_description: module for create, update and delete of ndb database clones
version_added: 1.8.0
description: module for create, update and delete of ndb database clones
options:
      uuid:
        description:
            - uuid of database clone for update and delete
        type: str
      name:
        description:
            - name of database clone
            - update is allowed
            - mandatory for creation
        type: str
      desc:
        description:
            - description of database clone
            - update is allowed
        type: str
      db_params_profile:
        description:
            - database parameter profile for creating database clone
            - mandatory for creation
        type: dict
        suboptions:
            name:
                description:
                    - profile name
                    - Mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - profile UUID
                    - Mutually exclusive with C(name)
                type: str
      db_vm:
        description:
            - database server vm details for hosting clone
            - mandatory for creation
        type: dict
        suboptions:
            create_new_server:
                description:
                    - configuration for creating new database server vm for hosting db clone
                    - Mutually exclusive with C(use_authorized_server)
                type: dict
                suboptions:
                    name:
                        description:
                            - name of db server vm
                        type: str
                        required: true
                    desc:
                        description:
                            - description of database server vm
                        type: str
                    pub_ssh_key:
                        description:
                            - use SSH public key to access the database server VM
                        type: str
                        required: true
                    password:
                        description:
                            - password for newly created db server vm
                        type: str
                        required: true
                    cluster:
                        description:
                            - cluster details to host the vm
                        type: dict
                        required: true
                        suboptions:
                            name:
                                description:
                                    - cluster name
                                    - Mutually exclusive with C(uuid)
                                type: str
                            uuid:
                                description:
                                    - cluster UUID
                                    - Mutually exclusive with C(name)
                                type: str
                    network_profile:
                        description:
                            - network profile details
                        type: dict
                        required: true
                        suboptions:
                            name:
                                description:
                                    - profile name
                                    - Mutually exclusive with C(uuid)
                                type: str
                            uuid:
                                description:
                                    - profile UUID
                                    - Mutually exclusive with C(name)
                                type: str
                    compute_profile:
                        description:
                            - compute profile details
                        type: dict
                        required: true
                        suboptions:
                            name:
                                description:
                                    - profile name
                                    - Mutually exclusive with C(uuid)
                                type: str
                            uuid:
                                description:
                                    - profile UUID
                                    - Mutually exclusive with C(name)
                                type: str

            use_authorized_server:
                description:
                    - configure authorized database server VM for hosting database clone
                type: dict
                suboptions:
                    name:
                        description:
                            - authorized database server vm name
                            - Mutually exclusive with C(uuid)
                        type: str
                    uuid:
                        description:
                            - authorized database server vm uuid
                            - Mutually exclusive with C(name)
                        type: str
      time_machine:
        description:
            - source time machine details
            - mandatory for creation
        type: dict
        suboptions:
            name:
                description:
                    - name of time machine
                    - mutually_exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - UUId of time machine
                    - mutually_exclusive with C(name)
                type: str
            snapshot_uuid:
                description:
                    - source snapshot uuid
                    - mutually exclusive with C(pitr_timestamp)
                type: str
            timezone:
                description:
                    - timezone related to C(pitr_timestamp)
                type: str
                default: "Asia/Calcutta"
            pitr_timestamp:
                description:
                    - timestamp for create clone from point in time
                type: str
            latest_snapshot:
                description:
                    - write
                type: bool
      postgres:
        description:
            - postgres database related config
            - mandatory for creation
        type: dict
        suboptions:
            db_password:
                description:
                    - set database password
                type: str
                required: true
            pre_clone_cmd:
                description:
                    - commands to run before database clone creation
                type: str
            post_clone_cmd:
                description:
                    - commands to run after database clone creation
                type: str
      tags:
        description:
            - list of tags name and  value pairs to be associated with clone
            - during update, given input tags override the exiting tags of clone
        type: dict
      removal_schedule:
        description:
            - clone removal schedule
            - update is allowed
        type: dict
        suboptions:
            state:
                description:
                    - state of schedule if added
                    - create, update and delete is allowed
                type: str
                choices: ["present", "absent"]
                default: "present"
            days:
                description:
                    - number of days after which clone will be removed
                    - mutually exclusive to C(timestamp)
                type: int
            timestamp:
                description:
                    - exact timestamp to remove database clone
                    - format is 'yyyy-mm-dd hh:mm:ss'
                    - mutually exclusive to C(days)
                type: str
            timezone:
                description:
                    - timezone related to C(timestamp)
                type: str
            delete_database:
                description:
                    - whether to delete database as well from clone instance during removal
                type: bool
                default: false
            remind_before_in_days:
                description:
                    - reminder in days before removal
                type: int
      refresh_schedule:
        description:
            - clone refresh schedule
            - update is allowed
        type: dict
        suboptions:
            state:
                description:
                    - state of schedule if added
                    - create, update and delete is allowed
                type: str
                choices: ["present", "absent"]
                default: "present"
            days:
                description:
                    - number of days after which clone will be refreshed
                type: int
            timezone:
                description:
                    - timezone related to C(time) give
                type: str
            time:
                description:
                    - exact time on particular day when clone will be refreshed
                type: str
      delete_from_vm:
        description:
            - during delete, flag for deleting the database from database server vm as well
            - mutually exclusive with C(soft_remove)
        type: bool
      soft_remove:
        description:
            - soft remove during delete process
            - mutually exclusive with C(delete_from_vm)
        type: bool
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: create clone using snapshot
  ntnx_ndb_database_clones:
    name: "{{clone_db1}}"
    desc: "ansible-created-clone"

    db_params_profile:
      name: "{{db_params_profile.name}}"

    db_vm:
      create_new_server:
        name: "{{ vm1_name }}"
        desc: "vm for db server"
        password: "{{ vm_password }}"
        cluster:
          name: "{{cluster.cluster1.name}}"
        network_profile:
          name: "{{ network_profile.name }}"
        compute_profile:
          name: "{{ compute_profile.name }}"
        pub_ssh_key: "{{ public_ssh_key }}"

    postgres:
      db_password: "{{vm_password}}"

    time_machine:
      name: "{{tm1}}"
      snapshot_uuid: "{{snapshot_uuid}}"

    removal_schedule:
      days: 2
      timezone: "Asia/Calcutta"
      remind_before_in_days: 1
      delete_database: true

    refresh_schedule:
      days: 2
      time: "12:00:00"
      timezone: "Asia/Calcutta"

    tags:
      ansible-clones: ansible-test-db-clones
  register: result

- name: create clone using point in time
  ntnx_ndb_database_clones:
    name: "{{clone_db1}}"
    desc: "ansible-created-clone"

    db_params_profile:
      name: "{{db_params_profile.name}}"

    db_vm:
      create_new_server:
        name: "{{ vm1_name }}"
        desc: "vm for db server"
        password: "{{ vm_password }}"
        cluster:
          name: "{{cluster.cluster1.name}}"
        network_profile:
          name: "{{ network_profile.name }}"
        compute_profile:
          name: "{{ compute_profile.name }}"
        pub_ssh_key: "{{ public_ssh_key }}"

    postgres:
      db_password: "{{vm_password}}"

    time_machine:
      name: "{{tm1}}"
      pitr_timestamp: "2023-02-28 12:00:00"
      timestamp: "Asia/Calcutta"

    removal_schedule:
      days: 2
      timezone: "Asia/Calcutta"
      remind_before_in_days: 1
      delete_database: true

    refresh_schedule:
      days: 2
      time: "12:00:00"
      timezone: "Asia/Calcutta"

    tags:
      ansible-clones: ansible-test-db-clones
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
                      \"ffdb3000-22bc-4994-86f5-5bb668422e5e\":
                      {\"size\": 303677440, \"allocatedSize\": 0, \"usedSize\": 0, \"unit\": \"B\"},
                      \"55034431-4f5b-48e0-bc58-13676bf9ed9b\": {\"size\": 9267200, \"allocatedSize\": 0, \"usedSize\": 0, \"unit\": \"B\"},
                      \"57e55810-0702-4f63-87b9-ff67921b6466\": {\"size\": 5439488, \"allocatedSize\": 0, \"usedSize\": 0, \"unit\": \"B\"}}}}",
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
from ..module_utils.v3.ndb.db_server_vm import DBServerVM  # noqa: E402
from ..module_utils.v3.ndb.operations import Operation  # noqa: E402
from ..module_utils.v3.ndb.tags import Tag  # noqa: E402
from ..module_utils.v3.ndb.time_machines import TimeMachine  # noqa: E402


def get_module_spec():

    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    new_server = dict(
        name=dict(type="str", required=True),
        desc=dict(type="str", required=False),
        pub_ssh_key=dict(type="str", required=True, no_log=True),
        password=dict(type="str", required=True, no_log=True),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        network_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        compute_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
    )

    db_vm = dict(
        create_new_server=dict(type="dict", options=new_server, required=False),
        use_authorized_server=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
    )

    time_machine = dict(
        name=dict(type="str", required=False),
        uuid=dict(type="str", required=False),
        snapshot_uuid=dict(type="str", required=False),
        pitr_timestamp=dict(type="str", required=False),
        latest_snapshot=dict(type="bool", required=False),
        timezone=dict(type="str", default="Asia/Calcutta", required=False),
    )

    postgres = dict(
        db_password=dict(type="str", required=True, no_log=True),
        pre_clone_cmd=dict(type="str", required=False),
        post_clone_cmd=dict(type="str", required=False),
    )

    removal_schedule = dict(
        state=dict(
            type="str", choices=["present", "absent"], default="present", required=False
        ),
        days=dict(type="int", required=False),
        timezone=dict(type="str", required=False),
        delete_database=dict(type="bool", default=False, required=False),
        timestamp=dict(type="str", required=False),
        remind_before_in_days=dict(type="int", required=False),
    )

    refresh_schedule = dict(
        state=dict(
            type="str", choices=["present", "absent"], default="present", required=False
        ),
        days=dict(type="int", required=False),
        timezone=dict(type="str", required=False),
        time=dict(type="str", required=False),
    )

    module_args = dict(
        uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        db_params_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        db_vm=dict(
            type="dict",
            options=db_vm,
            mutually_exclusive=[("create_new_server", "use_authorized_server")],
            required=False,
        ),
        time_machine=dict(
            type="dict",
            options=time_machine,
            mutually_exclusive=[("snapshot_uuid", "pitr_timestamp", "latest_snapshot")],
            required=False,
        ),
        postgres=dict(type="dict", options=postgres, required=False),
        tags=dict(type="dict", required=False),
        removal_schedule=dict(
            type="dict",
            options=removal_schedule,
            mutually_exclusive=[
                ("days", "timestamp"),
            ],
            required=False,
        ),
        refresh_schedule=dict(type="dict", options=refresh_schedule, required=False),
        delete_from_vm=dict(type="bool", required=False),
        soft_remove=dict(type="bool", required=False),
    )
    return module_args


def get_clone_spec(module, result, time_machine_uuid):

    # create database instance obj
    db_clone = DatabaseClone(module=module)

    spec, err = db_clone.get_spec(create=True)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed getting database clone spec", **result)

    # populate database engine related spec
    spec, err = db_clone.get_db_engine_spec(spec)
    if err:
        result["error"] = err
        err_msg = "Failed getting database engine related spec for database clone"
        module.fail_json(msg=err_msg, **result)

    # populate database instance related spec
    db_server_vms = DBServerVM(module)

    provision_new_server = (
        True if module.params.get("db_vm", {}).get("create_new_server") else False
    )
    use_authorized_server = not provision_new_server

    kwargs = {
        "time_machine_uuid": time_machine_uuid,
        "db_clone": True,
        "provision_new_server": provision_new_server,
        "use_authorized_server": use_authorized_server,
    }

    spec, err = db_server_vms.get_spec(old_spec=spec, **kwargs)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed getting vm spec for database clone", **result)

    # populate tags related spec
    tags = Tag(module)
    spec, err = tags.get_spec(old_spec=spec, associate_to_entity=True, type="CLONE")
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for tags for database clone", **result
        )

    return spec


def create_db_clone(module, result):
    db_clone = DatabaseClone(module)
    time_machine = TimeMachine(module)

    time_machine_config = module.params.get("time_machine")
    if not time_machine_config:
        return module.fail_json(
            msg="time_machine is required field for create", **result
        )
    time_machine_uuid, err = time_machine.get_time_machine_uuid(time_machine_config)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting time machine uuid for database clone", **result
        )
    spec = get_clone_spec(module, result, time_machine_uuid=time_machine_uuid)

    if module.check_mode:
        result["response"] = spec
        return

    resp = db_clone.create(time_machine_uuid=time_machine_uuid, data=spec)
    result["response"] = resp
    result["uuid"] = resp["entityId"]
    uuid = resp["entityId"]

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=15)
        resp = db_clone.read(uuid)
        db_clone.format_response(resp)
        result["response"] = resp

    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):
    if (
        old_spec["name"] != update_spec["name"]
        or old_spec["description"] != update_spec["description"]
    ):
        return False

    if update_spec.get("removeRefreshConfig") or update_spec.get("removeExpiryConfig"):
        return False

    if old_spec["lcmConfig"].get("expiryDetails") != update_spec["lcmConfig"].get(
        "expiryDetails"
    ):
        return False

    if old_spec["lcmConfig"].get("refreshDetails") != update_spec["lcmConfig"].get(
        "refreshDetails"
    ):
        return False

    if len(old_spec["tags"]) != len(update_spec["tags"]):
        return False

    old_tag_values = {}
    new_tag_values = {}
    for i in range(len(old_spec["tags"])):
        old_tag_values[old_spec["tags"][i]["tagName"]] = old_spec["tags"][i]["value"]
        new_tag_values[update_spec["tags"][i]["tagName"]] = update_spec["tags"][i][
            "value"
        ]

    if old_tag_values != new_tag_values:
        return False

    return True


def update_db_clone(module, result):
    _clones = DatabaseClone(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for update", **result)
    result["uuid"] = uuid

    resp = _clones.read(uuid)
    old_spec = _clones.get_default_update_spec(override_spec=resp)

    spec, err = _clones.get_spec(old_spec=old_spec, update=True)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update database clone spec", **result)

    # populate tags related spec
    if module.params.get("tags"):
        tags = Tag(module)
        spec, err = tags.get_spec(old_spec=spec, associate_to_entity=True, type="CLONE")
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed getting spec for tags for updating database clone", **result
            )

    if module.check_mode:
        result["response"] = spec
        return

    if check_for_idempotency(old_spec, spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = _clones.update(data=spec, uuid=uuid)
    _clones.format_response(resp)
    result["response"] = resp
    result["uuid"] = uuid
    result["changed"] = True


def delete_db_clone(module, result):
    _clones = DatabaseClone(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for delete", **result)

    default_spec = _clones.get_default_delete_spec()
    spec, err = _clones.get_spec(old_spec=default_spec, delete=True)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for deleting database clone", **result
        )

    if module.check_mode:
        result["response"] = spec
        return

    resp = _clones.delete(uuid, data=spec)

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        time.sleep(5)  # to get operation ID functional
        operations = Operation(module)
        resp = operations.wait_for_completion(ops_uuid, delay=5)

    result["response"] = resp
    result["changed"] = True


def run_module():
    mutually_exclusive_list = [
        ("uuid", "db_params_profile"),
        ("uuid", "db_vm"),
        ("uuid", "postgres"),
        ("uuid", "time_machine"),
        ("delete_from_vm", "soft_remove"),
    ]
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=mutually_exclusive_list,
        required_if=[
            ("state", "present", ("name", "uuid"), True),
            ("state", "absent", ("uuid",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    if module.params["state"] == "present":
        if module.params.get("uuid"):
            update_db_clone(module, result)
        else:
            create_db_clone(module, result)
    else:
        delete_db_clone(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
