#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_replicate_database_snapshots
short_description: module for replicating database snapshots across clusters of time machine
version_added: 1.8.0
description:
    - module for replicating snapshots across clusters of time machine
    - replication to one cluster at a time is supported
options:
      expiry_days:
        description:
            - expiry days for removal of snapshot
        type: str
      snapshot_uuid:
        description:
            - snapshot uuid
        type: str
      clusters:
        description:
            - cluster details where snapshot needs to be replicated
            - currently, replication to only one cluster at once is supported
        type: list
        elements: dict
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
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: replicate snapshot with expiry
  ntnx_ndb_replicate_database_snapshots:
    snapshot_uuid: "{{snapshot_uuid}}"
    clusters:
      - name: "{{cluster.cluster2.name}}"
    expiry_days: 20
  register: result
"""
RETURN = r"""
response:
  description: snapshot replication response
  returned: always
  type: dict
  sample: {
            "ancestorOpIds": null,
            "childOperations": [],
            "dateSubmitted": "2023-02-28 11:13:32",
            "dbserverId": "e507345b-c7d1-469a-8297-3088f017f120",
            "dbserverStatus": "UP",
            "deferredBy": null,
            "deferredByOpIds": null,
            "endTime": "2023-02-28 11:14:15",
            "entityId": "7a39664b-dfb7-4529-887c-6d91f7e18604",
            "entityName": "test-setup-dnd_TM (DATABASE)",
            "entityType": "ERA_TIME_MACHINE",
            "id": "79d57f0b-4ce6-4a22-a28b-dbd1839c4d0a",
            "instanceId": null,
            "isInternal": false,
            "message": null,
            "metadata": {
                "ancestorOpIds": null,
                "associatedEntities": null,
                "controlMessage": null,
                "executionContext": {
                    "affectedDBServers": [
                        "e507345b-c7d1-469a-8297-3088f017f120"
                    ],
                    "applicationType": "generic",
                    "extendedAffectedDBServers": [
                        "e507345b-c7d1-469a-8297-3088f017f120"
                    ]
                },
                "linkedOperations": null,
                "linkedOperationsDescription": "Associated operation(s)",
                "oldStatus": null,
                "retriedOperations": null,
                "retryImmediateParentId": null,
                "retryParentId": null,
                "rollbackForOperationId": null,
                "rollbackOperation": false,
                "scheduleTime": null,
                "scheduledBy": "2ba56951-859a-4548-893e-9a8649362786",
                "scheduledOn": "2023-02-28 11:13:31",
                "switchedDbservers": null,
                "userRequestedAction": "0",
                "userRequestedActionTimestamp": null,
                "workCompletionCallbackExecuted": true
            },
            "name": "xxxxxxxxx",
            "nxClusterId": "94c3e490-69e2-4144-83ff-68867e47889d",
            "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
            "parentId": null,
            "parentStep": 0,
            "percentageComplete": "100",
            "properties": [],
            "scheduleTime": null,
            "setStartTime": false,
            "startTime": "2023-02-28 11:13:36",
            "status": "5",
            "stepGenEnabled": false,
            "steps": [],
            "systemTriggered": false,
            "timeZone": "UTC",
            "timeout": 1450,
            "timeoutInfo": {
                "timeRemaining": 1449,
                "timeout": 1450,
                "timeoutTimestamp": "2023-03-01 11:23:36",
                "timezone": "UTC"
            },
            "type": "replicate_snapshot",
            "uniqueName": null,
            "userRequestedAction": "0",
            "userRequestedActionTime": null,
            "userVisible": true,
            "work": null
        }
snapshot_uuid:
  description: snapshot uuid
  returned: always
  type: str
  sample: "be524e70-60ad-4a8c-a0ee-8d72f954d7e6"
"""
import time  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.v3.ndb.operations import Operation  # noqa: E402
from ..module_utils.v3.ndb.snapshots import Snapshot  # noqa: E402

# Notes:
# 1. Snapshot replication to one cluster at a time is supported currently


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    module_args = dict(
        snapshot_uuid=dict(type="str", required=False),
        clusters=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        expiry_days=dict(type="str", required=False),
    )
    return module_args


def replicate_snapshot(module, result):

    snapshot_uuid = module.params.get("snapshot_uuid")
    if not snapshot_uuid:
        module.fail_json(
            msg="snapshot_uuid is required field for replication", **result
        )

    _snapshot = Snapshot(module)
    snapshot = _snapshot.read(uuid=snapshot_uuid)
    time_machine_uuid = snapshot.get("timeMachineId")

    spec, err = _snapshot.get_replicate_snapshot_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating snapshot create spec", **result)

    result["snapshot_uuid"] = snapshot_uuid

    if module.check_mode:
        result["response"] = spec
        return

    resp = _snapshot.replicate(
        uuid=snapshot_uuid, time_machine_uuid=time_machine_uuid, data=spec
    )
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)
        resp = operations.wait_for_completion(ops_uuid, delay=5)
        result["response"] = resp

    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("snapshot_uuid",), True),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "snapshot_uuid": None}

    replicate_snapshot(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
