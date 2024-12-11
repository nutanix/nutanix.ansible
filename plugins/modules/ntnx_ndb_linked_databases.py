#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_linked_databases
short_description: module to manage linked databases of a database instance
version_added: 1.8.0
description: module to manage linked databases of a database instance
options:
      state:
        description:
            - when C(state)=present, it will create databases in database instance
            - when C(state)=absent, it will delete linked database with database_uuid
      db_instance_uuid:
        description:
            - database instance uuid
        type: str
        required: true
      database_uuid:
        description:
            - linked database uuid
            - should be used with c(state)=absent, to delete linked database
        type: str
      databases:
        description:
            - list of database's name to be added in database instance
        type: list
        elements: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: add databases in database instance
  ntnx_ndb_linked_databases:
    db_instance_uuid: "{{db_uuid}}"
    databases:
      - test1
      - test2
  register: result

- name: remove linked databases from database instance
  ntnx_ndb_linked_databases:
    state: "absent"
    db_instance_uuid: "{{db_uuid}}"
    database_uuid: "{{linked_databases.test1}}"
  register: result
"""
RETURN = r"""
response:
  description: list of linked databases in database instance
  returned: always
  type: dict
  sample: [
            {
                "databaseName": "template1",
                "databaseStatus": "READY",
                "dateCreated": "2023-02-24 08:07:01",
                "dateModified": "2023-02-24 08:07:01",
                "description": null,
                "id": "d013a63f-c9ba-4533-989d-57e57d8a4d6f",
                "info": {
                    "info": {
                        "created_by": "system"
                    },
                    "secureInfo": null
                },
                "metadata": null,
                "metric": null,
                "name": "template1",
                "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                "parentDatabaseId": "50b8ce26-62ba-443b-a6b6-8739373f81eb",
                "parentDatabaseName": null,
                "parentDatabaseType": null,
                "parentLinkedDatabaseId": null,
                "snapshotId": null,
                "status": "READY",
                "tags": [],
                "timeZone": null
            },
            {
                "databaseName": "template0",
                "databaseStatus": "READY",
                "dateCreated": "2023-02-24 08:07:01",
                "dateModified": "2023-02-24 08:07:01",
                "description": null,
                "id": "c18419fd-df31-4e54-b35a-ee004c0faafb",
                "info": {
                    "info": {
                        "created_by": "system"
                    },
                    "secureInfo": null
                },
                "metadata": null,
                "metric": null,
                "name": "template0",
                "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                "parentDatabaseId": "50b8ce26-62ba-443b-a6b6-8739373f81eb",
                "parentDatabaseName": null,
                "parentDatabaseType": null,
                "parentLinkedDatabaseId": null,
                "snapshotId": null,
                "status": "READY",
                "tags": [],
                "timeZone": null
            },
            {
                "databaseName": "prad",
                "databaseStatus": "READY",
                "dateCreated": "2023-02-24 08:07:01",
                "dateModified": "2023-02-24 08:07:01",
                "description": null,
                "id": "779f1f6a-502d-4ffd-9030-d21447c5ca3d",
                "info": {
                    "info": {
                        "created_by": "user"
                    },
                    "secureInfo": null
                },
                "metadata": null,
                "metric": null,
                "name": "prad",
                "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                "parentDatabaseId": "50b8ce26-62ba-443b-a6b6-8739373f81eb",
                "parentDatabaseName": null,
                "parentDatabaseType": null,
                "parentLinkedDatabaseId": null,
                "snapshotId": null,
                "status": "READY",
                "tags": [],
                "timeZone": null
            },
            {
                "databaseName": "postgres",
                "databaseStatus": "READY",
                "dateCreated": "2023-02-24 08:07:01",
                "dateModified": "2023-02-24 08:07:01",
                "description": null,
                "id": "6e3733cf-2994-49d2-945c-c1873564be97",
                "info": {
                    "info": {
                        "created_by": "system"
                    },
                    "secureInfo": null
                },
                "metadata": null,
                "metric": null,
                "name": "postgres",
                "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                "parentDatabaseId": "50b8ce26-62ba-443b-a6b6-8739373f81eb",
                "parentDatabaseName": null,
                "parentDatabaseType": null,
                "parentLinkedDatabaseId": null,
                "snapshotId": null,
                "status": "READY",
                "tags": [],
                "timeZone": null
            },
            {
                "databaseName": "ansible1-new",
                "databaseStatus": "READY",
                "dateCreated": "2023-02-28 09:53:27",
                "dateModified": "2023-02-28 09:53:51",
                "description": null,
                "id": "742e41b9-1766-47ef-9c2c-97aadeac8c0f",
                "info": {
                    "info": {
                        "created_by": "user"
                    },
                    "secureInfo": null
                },
                "metadata": null,
                "metric": null,
                "name": "ansible1-new",
                "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                "parentDatabaseId": "50b8ce26-62ba-443b-a6b6-8739373f81eb",
                "parentDatabaseName": null,
                "parentDatabaseType": null,
                "parentLinkedDatabaseId": null,
                "snapshotId": null,
                "status": "READY",
                "tags": [],
                "timeZone": null
            },
            {
                "databaseName": "ansible2-new",
                "databaseStatus": "READY",
                "dateCreated": "2023-02-28 09:53:27",
                "dateModified": "2023-02-28 09:53:51",
                "description": null,
                "id": "04d4b431-e75f-4a14-86ad-674f447d6aec",
                "info": {
                    "info": {
                        "created_by": "user"
                    },
                    "secureInfo": null
                },
                "metadata": null,
                "metric": null,
                "name": "ansible2-new",
                "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                "parentDatabaseId": "50b8ce26-62ba-443b-a6b6-8739373f81eb",
                "parentDatabaseName": null,
                "parentDatabaseType": null,
                "parentLinkedDatabaseId": null,
                "snapshotId": null,
                "status": "READY",
                "tags": [],
                "timeZone": null
            }
        ]
database_instance_uuid:
  description: database instance uuid
  returned: always
  type: str
  sample: "be524e70-60ad-4a8c-a0ee-8d72f954d7e6"
"""
import time  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.v3.ndb.database_instances import DatabaseInstance  # noqa: E402
from ..module_utils.v3.ndb.operations import Operation  # noqa: E402


def get_module_spec():

    module_args = dict(
        db_instance_uuid=dict(type="str", required=True),
        database_uuid=dict(type="str", required=False),
        databases=dict(type="list", elements="str", required=False),
    )
    return module_args


def add_database(module, result):
    instance_uuid = module.params.get("db_instance_uuid")
    if not instance_uuid:
        err_msg = "db_instance_uuid is required field for adding databases to database instance"
        return module.fail_json(msg=err_msg, **result)
    result["db_instance_uuid"] = instance_uuid

    _databases = DatabaseInstance(module)
    databases = module.params.get("databases")
    if not databases:
        return module.exit_json(msg="No database to add", **result)

    spec = _databases.get_add_database_spec(databases)
    if module.check_mode:
        result["response"] = spec
        return

    resp = _databases.add_databases(instance_uuid, spec)
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        time.sleep(3)  # to get operation ID functional
        operations = Operation(module)
        operations.wait_for_completion(ops_uuid, delay=5)
        resp = _databases.read(uuid=instance_uuid)
        result["response"] = resp.get("linkedDatabases", [])

    result["changed"] = True


def remove_database(module, result):
    instance_uuid = module.params.get("db_instance_uuid")
    database_uuid = module.params.get("database_uuid")
    if not database_uuid or not instance_uuid:
        err_msg = "database_uuid and instance_uuid are required fields for deleting database from database instance"
        module.fail_json(msg=err_msg, **result)

    _databases = DatabaseInstance(module)
    resp = _databases.remove_linked_database(
        linked_database_uuid=database_uuid, database_instance_uuid=instance_uuid
    )
    result["response"] = resp
    result["db_instance_uuid"] = instance_uuid

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get ops ID functional
        operations.wait_for_completion(ops_uuid, delay=5)
        resp = _databases.read(uuid=instance_uuid)
        result["response"] = resp.get("linkedDatabases", [])

    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[("databases", "database_uuid")],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "db_instance_uuid": None,
    }

    if module.params["state"] == "present":
        add_database(module, result)
    else:
        remove_database(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
