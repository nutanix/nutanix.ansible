#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_database_log_catchup
short_description: module for performing log catchups action
version_added: 1.8.0
description: module for performing log catchups action
options:
      time_machine_uuid:
        description:
            - time machine UUID
        type: str
        required: true
      for_restore:
        description:
            - enable this flag if log catchup is to be done for restore process
        type: bool
        default: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: perform log catchup
  ntnx_ndb_database_log_catchup:
    time_machine_uuid: "{{time_machine_uuid}}"
  register: result

- name: perform log catchup for restore
  ntnx_ndb_database_log_catchup:
    time_machine_uuid: "{{time_machine_uuid}}"
    for_restore: true
  register: result
"""
RETURN = r"""
response:
  description: An intentful representation of a task status post log catchup
  returned: always
  type: dict
  sample: {
    "entityName": "OWZWuxlTgBhX-time-machine",
    "work": null,
    "stepGenEnabled": false,
    "setStartTime": false,
    "timeZone": "UTC",
    "id": "92e426d8-680c-4c93-8042-63c97aafa818",
    "name": "Performing Log Catchup before Restore Instance OWZWuxlTgBhX on host xx.xx.xx.xx",
    "uniqueName": null,
    "type": "perform_log_catchup",
    "startTime": "2023-02-27 19:12:21",
    "timeout": 70,
    "timeoutInfo": {
        "timeoutTimestamp": "2023-02-27 20:22:21",
        "timeRemaining": 0,
        "timeout": 70,
        "timezone": "UTC"
    },
    "endTime": "2023-02-27 19:14:07",
    "instanceId": null,
    "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
    "status": "5",
    "percentageComplete": "100",
    "steps": [{}, {}],
    "properties": [],
    "parentId": null,
    "parentStep": 0,
    "message": null,
    "metadata": {},
    "entityId": "5da0150a-c476-4fce-9ce2-cc8f28e652e5",
    "entityType": "ERA_TIME_MACHINE",
    "systemTriggered": false,
    "userVisible": true,
    "dbserverId": "4a19a165-d682-4ca3-b740-826ac206c18b",
    "dateSubmitted": "2023-02-27 19:12:17",
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
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.ndb.time_machines import TimeMachine  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    module_args = dict(
        time_machine_uuid=dict(type="str", required=True),
        for_restore=dict(type="bool", required=False, default=False),
    )
    return module_args


def log_catchup(module, result):
    time_machine_uuid = module.params.get("time_machine_uuid")
    if not time_machine_uuid:
        return module.fail_json(msg="time_machine_uuid is required for log catchups")

    time_machine = TimeMachine(module)
    for_restore = module.params.get("for_restore")
    spec = time_machine.get_log_catchup_spec(for_restore)
    if module.check_mode:
        result["response"] = spec
        return

    resp = time_machine.log_catchup(time_machine_uuid=time_machine_uuid, data=spec)
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        time.sleep(5)  # to get operation ID functional
        operations = Operation(module)
        resp = operations.wait_for_completion(ops_uuid)
        result["response"] = resp

    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}

    log_catchup(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
