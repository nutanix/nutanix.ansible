#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_database_restore
short_description: module for restoring database instance
version_added: 1.8.0
description: 
    - module for restoring database instance to certain point in time or snapshot
    - module will use latest snapshot if pitr timestamp or snapshot uuid is not given
options:
      pitr_timestamp:
        description:
            - timestamp of point in time restore
            - "format: 'yyyy-mm-dd hh:mm:ss'"
            - mutually exclusive with C(snapshot_uuid)
        type: str
      snapshot_uuid:
        description:
            - snapshot uuid for restore
            - mutually exclusive with C(pitr_timestamp)
        type: str
      timezone:
        description:
            - timezone related to given C(pitr_timestamp)
        type: str
      db_uuid:
        description:
            - database instance uuid
        type: str
        required: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: perform restore using latest snapshot
  ntnx_ndb_database_restore:
    db_uuid: "{{db_uuid}}"
    snapshot_uuid: "{{snapshot_uuid}}"
  register: result

- name: perform restore using snapshot uuid
  ntnx_ndb_database_restore:
    db_uuid: "{{db_uuid}}"
    snapshot_uuid: "{{snapshot_uuid}}"
  register: result

- name: perform restore using pitr
  ntnx_ndb_database_restore:
    db_uuid: "{{db_uuid}}"
    pitr_timestamp: "{{snapshot_uuid}}"
    timezone: "UTC"
  register: result
"""
RETURN = r"""
response:
  description: An intentful representation of a task status post restore
  returned: always
  type: dict
  sample: {
    "entityName": "OWZWuxlTgBhX",
    "work": null,
    "stepGenEnabled": false,
    "setStartTime": false,
    "timeZone": "UTC",
    "id": "4cdf6937-6f99-4662-9f46-46c1ad7e83b2",
    "name": "Restore Postgres Instance to Snapshot a1d5afdb-5890-4b41-a0e1-e6e79cad70cf",
    "uniqueName": null,
    "type": "restore_database",
    "startTime": "2023-02-27 19:25:48",
    "timeout": 250,
    "timeoutInfo": {
        "timeoutTimestamp": "2023-02-27 23:35:48",
        "timeRemaining": 0,
        "timeout": 250,
        "timezone": "UTC"
    },
    "endTime": "2023-02-27 19:33:50",
    "instanceId": null,
    "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
    "status": "5",
    "percentageComplete": "100",
    "steps": [],
    "properties": [],
    "parentId": null,
    "parentStep": 0,
    "message": null,
    "metadata": {},
    "entityId": "117760dc-c766-46f1-9ffd-126826cf37a9",
    "entityType": "ERA_DATABASE",
    "systemTriggered": false,
    "userVisible": true,
    "dbserverId": "4a19a165-d682-4ca3-b740-826ac206c18b",
    "dateSubmitted": "2023-02-27 19:23:33",
    "deferredBy": null,
    "deferredByOpIds": null,
    "scheduleTime": null,
    "isInternal": false,
    "nxClusterId": "0a3b964f-8616-40b9-a564-99cf35f4b8d8",
    "dbserverStatus": "DELETED",
    "childOperations": [],
    "ancestorOpIds": null,
    "userRequestedAction": "0",
    "userRequestedActionTime": null
} 

"""
import time  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.database_instances import DatabaseInstance  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        snapshot_uuid=dict(type="str", required=False),
        pitr_timestamp=dict(type="str", required=False),
        db_uuid=dict(type="str", required=True),
        timezone=dict(type="str", required=False),
    )
    return module_args


def restore_database(module, result):
    db = DatabaseInstance(module)
    db_uuid = module.params.get("db_uuid")
    if not db_uuid:
        module.fail_json(msg="db_uuid is required field for restoring", **result)

    spec = db.get_restore_spec(module.params)

    if module.check_mode:
        result["response"] = spec
        return

    resp = db.restore(uuid=db_uuid, data=spec)
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        time.sleep(5)  # to get operation ID functional
        operations = Operation(module)
        resp = operations.wait_for_completion(ops_uuid)
        result["response"] = resp

    result["changed"] = True
    result["db_uuid"] = db_uuid


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_together=[("pitr_timestamp", "timezone")],
        mutually_exclusive=[("snapshot_uuid", "pitr_timestamp")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "db_uuid": None}

    restore_database(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
