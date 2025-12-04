#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_database_scale
short_description: module for scaling database instance
version_added: 1.8.0
description:
    - module for scaling database instance
    - currently, extension of database storage is only supported
options:
      pre_update_cmd:
        description:
            - complete OS command that you want to run before scaling
        type: str
      post_update_cmd:
        description:
            - complete OS command that you want to run post scaling
        type: str
      storage_gb:
        description:
            - storage to be added in GB
        type: int
        required: true
      db_uuid:
        description:
            - database instance uuid
        type: str
        required: true
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
- name: extend database storage for scaling database
  ntnx_ndb_database_scale:
    db_uuid: "{{db_uuid}}"
    storage_gb: 2
    pre_update_cmd: "ls"
    post_update_cmd: "ls -a"
  register: result
"""
RETURN = r"""
response:
  description: An intentful representation of a task status post scaling
  returned: always
  type: dict
  sample: {
    "entityName": "OWZWuxlTgBhX",
    "work": null,
    "stepGenEnabled": false,
    "setStartTime": false,
    "timeZone": "UTC",
    "id": "8778ef1b-9278-4f0e-a80a-7be5d8998e86",
    "name": "Extend Database Storage",
    "uniqueName": null,
    "type": "extend_database_storage",
    "startTime": "2023-02-27 19:36:39",
    "timeout": 70,
    "timeoutInfo": {
        "timeoutTimestamp": "2023-02-27 20:46:39",
        "timeRemaining": 0,
        "timeout": 70,
        "timezone": "UTC"
    },
    "endTime": "2023-02-27 19:42:42",
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
    "dateSubmitted": "2023-02-27 19:34:25",
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

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.v3.ndb.database_instances import DatabaseInstance  # noqa: E402
from ..module_utils.v3.ndb.operations import Operation  # noqa: E402


def get_module_spec():

    module_args = dict(
        db_uuid=dict(type="str", required=True),
        storage_gb=dict(type="int", required=True),
        pre_update_cmd=dict(type="str", required=False),
        post_update_cmd=dict(type="str", required=False),
    )
    return module_args


def scale_db_instance(module, result):
    _databases = DatabaseInstance(module)
    uuid = module.params.get("db_uuid")
    if not uuid:
        module.fail_json(msg="db_uuid is required field for scaling", **result)

    resp = _databases.read(uuid)
    result["response"] = resp

    database_type = resp.get("type")
    if not database_type:
        module.fail_json(msg="failed fetching database type", **result)

    spec = _databases.get_scaling_spec(
        scale_config=module.params, database_type=database_type
    )

    if module.check_mode:
        result["response"] = spec
        return

    resp = _databases.scale(uuid=uuid, data=spec)
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        time.sleep(5)  # to get operation ID functional
        operations = Operation(module)
        resp = operations.wait_for_completion(ops_uuid)
        result["response"] = resp

    result["changed"] = True
    result["db_uuid"] = uuid


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "db_uuid": None}

    scale_db_instance(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
