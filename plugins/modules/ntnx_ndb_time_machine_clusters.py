#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_time_machine_clusters
short_description: Module for create, update and delete for data access management in time machines.
version_added: 1.8.0
description:
    - Module for create, update and delete for data access management i.e. clusters for snapshots in time machines.
    - Currently only postgres type database is tested and supported
options:
  time_machine_uuid:
    description: UUID of the time machine
    type: str
    required: true
  cluster:
    description:
        - Name or UUID of the cluster
        - if cluster is not present in time machine, then it will add it
        - if cluster is present then it will update cluster config in time machine
    type: dict
    suboptions:
        name:
            description:
                - Cluster Name
                - Mutually exclusive with C(uuid)
            type: str
        uuid:
            description:
                - Cluster UUID
                - Mutually exclusive with C(name)
            type: str
  type:
    description:
        - type of data access instance
        - update allowed
    type: str
    default: "OTHER"
    choices: ["OTHER", "PRIMARY"]
  sla:
    description:
        - Name or UUID of the sla
        - Update allowed
    type: dict
    suboptions:
        name:
            description:
                - Sla Name
                - Mutually exclusive with C(uuid)
            type: str
        uuid:
            description:
                - Sla UUID
                - Mutually exclusive with C(name)
            type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_ndb_base_module
  - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: create data access instance with cluster name and sla name
  ntnx_ndb_time_machine_clusters:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    time_machine_uuid: "<time_machine-uuid>"
    cluster:
      name: "<cluster-uuid>"
    sla:
      name: "<sla-uuid>"
  register: out

- name: update data access instance with new sla name
  ntnx_ndb_time_machine_clusters:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    time_machine_uuid: "<time_machine-uuid>"
    cluster:
      name: "<cluster-uuid>"
    sla:
      name: "<sla-uuid>"
  register: result

- name: delete time machine
  ntnx_ndb_time_machine_clusters:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: absent
    time_machine_uuid: "<time_machine-uuid>"
    cluster:
      uuid: "<cluster-uuid>"
  register: result
"""
RETURN = r"""
response:
  description: An intentful representation of a TM status
  returned: always
  type: dict
  sample: {
            "dateCreated": "2023-01-22 08:03:46",
            "dateModified": "2023-01-22 08:03:46",
            "description": null,
            "forceVGBasedLogDrive": false,
            "info": null,
            "logDrive": null,
            "logDriveId": null,
            "logDriveStatus": "NOT_INITIALIZED",
            "metadata": null,
            "nxCluster": null,
            "nxClusterId": "0000000-000000-00000-0000",
            "ownerId": "0000000-000000-00000-0000",
            "resetDescription": false,
            "resetSlaId": false,
            "resetType": false,
            "schedule": null,
            "scheduleId": "0000000-000000-00000-0000",
            "sla": null,
            "slaId": "0000000-000000-00000-0000",
            "source": false,
            "sourceClusters": null,
            "status": "ACTIVE",
            "storageResourceId": null,
            "submitActivateTimeMachineOp": false,
            "timeMachineId": "0000000-000000-00000-0000",
            "type": "OTHER",
            "updateOperationSummary": null
        }
time_machine_uuid:
  description: created data access instance UUID
  returned: always
  type: str
  sample: "0000000-000000-00000-0000"
"""

import time  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.ndb.time_machines import TimeMachine, get_cluster_uuid  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    module_args = dict(
        time_machine_uuid=dict(type="str", required=True),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
        ),
        type=dict(
            type="str", required=False, default="OTHER", choices=["OTHER", "PRIMARY"]
        ),
        sla=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
        ),
    )
    return module_args


def create_data_access_instance(module, result):
    tm = TimeMachine(module)
    tm_uuid = module.params["time_machine_uuid"]
    if not module.params.get("cluster"):
        module.fail_json(msg="cluster is required field", **result)

    cluster_uuid, err = get_cluster_uuid(module, module.params["cluster"])
    if err:
        result["error"] = err
        err_msg = "'cluster' is required field for adding cluster in time machine"
        module.fail_json(msg=err_msg, **result)

    cluster_in_time_machine = tm.check_if_cluster_exists(tm_uuid, cluster_uuid)

    # if cluster exist in time machine trigger update flow
    if cluster_in_time_machine:
        update_data_access_instance(module, result)
        return

    spec, err = tm.get_data_access_management_spec()
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for adding cluster in time machine", **result
        )
    result["time_machine_uuid"] = tm_uuid

    if module.check_mode:
        result["response"] = spec
        return

    resp = tm.create_data_access_instance(tm_uuid, spec)

    if (
        module.params.get("wait")
        and resp.get("updateOperationSummary")
        and resp["updateOperationSummary"].get("operationId")
    ):
        ops_uuid = resp["updateOperationSummary"]["operationId"]
        operations = Operation(module)
        time.sleep(5)  # wait for ops ID for functional
        operations.wait_for_completion(ops_uuid)
        resp = tm.read_data_access_instance(tm_uuid, cluster_uuid)
        result["response"] = resp

    result["response"] = resp
    result["cluster_uuid"] = resp["nxClusterId"]
    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):
    attrs = ["slaId", "type"]
    for attr in attrs:
        if old_spec.get(attr) != update_spec.get(attr):
            return False
    return True


def update_data_access_instance(module, result):
    tm = TimeMachine(module)

    tm_uuid = module.params["time_machine_uuid"]
    if not module.params.get("cluster"):
        module.fail_json(msg="'cluster' is required field for update", **result)

    cluster_uuid, err = get_cluster_uuid(module, module.params["cluster"])
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for updating cluster in time machine", **result
        )

    result["time_machine_uuid"] = tm_uuid

    resp = tm.read_data_access_instance(tm_uuid, cluster_uuid)

    old_spec = tm.get_default_data_access_management_spec(override_spec=resp)

    spec, err = tm.get_data_access_management_spec(old_spec=old_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for updating cluster in time machine", **result
        )

    if module.check_mode:
        result["response"] = spec
        return

    if check_for_idempotency(old_spec, spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = tm.update_data_access_instance(
        data=spec, tm_uuid=tm_uuid, cluster_uuid=cluster_uuid
    )

    if (
        module.params.get("wait")
        and resp.get("updateOperationSummary")
        and resp["updateOperationSummary"].get("operationId")
    ):
        ops_uuid = resp["updateOperationSummary"]["operationId"]
        operations = Operation(module)
        operations.wait_for_completion(ops_uuid)

    resp = tm.read_data_access_instance(tm_uuid, cluster_uuid)
    result["response"] = resp

    result["cluster_uuid"] = cluster_uuid
    result["changed"] = True


def delete_data_access_instance(module, result):
    tm = TimeMachine(module)

    tm_uuid = module.params["time_machine_uuid"]
    if not module.params.get("cluster"):
        module.fail_json(msg="cluster is required field", **result)
    cluster_uuid, err = get_cluster_uuid(module, module.params["cluster"])
    if err:
        result["error"] = err
        err_msg = "'cluster' is required field for removing cluster from time machine"
        module.fail_json(msg=err_msg, **result)
    resp = tm.delete_data_access_instance(tm_uuid, cluster_uuid)

    result["response"] = resp
    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("sla",)),
        ],
    )
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "time_machine_uuid": None,
    }
    if module.params["state"] == "present":
        create_data_access_instance(module, result)
    else:
        delete_data_access_instance(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
