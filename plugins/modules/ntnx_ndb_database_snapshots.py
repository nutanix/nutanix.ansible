#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_database_snapshots
short_description: module for creating, updating and deleting database snapshots
version_added: 1.8.0
description: 
    - module for creating, updating and deleting database snapshots
    - currently, this module only polls for snapshot create in primary source cluster
    - it doesn't poll of replication task if multiple clusters are mentioned
    - check_mode is not supported for snapshot update
options:
      snapshot_uuid:
        description:
            - snapshot uuid for delete or update
        type: str
      name:
        description:
            - name of snaphsot.
            - update is allowed
        type: str
      clusters:
        description:
            - list of clusters where snapshot should be present
            - if secondary clusters of time machines are mentioned, then this module won't track the replication process
            - clusters changes are not considered during update, for replication use ntnx_ndb_replicate_database_snapshots
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - name of cluster
                    - mutually_exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - uuid of cluster
                    - mutually_exclusive with c(name)
                type: str
      expiry_days:
            description:
                - write
            type: int
      remove_expiry:
            description:
                - write
            type: bool
      time_machine_uuid:
            description:
                - write
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
"""

RETURN = r"""
"""
import time  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.ndb.snapshots import Snapshot  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    module_args = dict(
        snapshot_uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        time_machine_uuid=dict(type="str", required=False),
        clusters=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        expiry_days=dict(type="int", required=False),
        remove_expiry=dict(type="bool", required=False),
    )
    return module_args


# Notes:
# 1. Currently we only poll for source snapshot create. Replication task is not polled.

# Create snapshot
def create_snapshot(module, result):
    time_machine_uuid = module.params.get("time_machine_uuid")
    if not time_machine_uuid:
        return module.fail_json(
            msg="time_machine_uuid is required for creating snapshot"
        )

    snapshots = Snapshot(module)
    spec, err = snapshots.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating snapshot create spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = snapshots.create_snapshot(time_machine_uuid, spec)
    result["response"] = resp

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)
        operations.wait_for_completion(ops_uuid, delay=5)

        # get snapshot info after its finished
        resp, err = snapshots.get_snapshot(
            time_machine_uuid=time_machine_uuid, name=module.params.get("name")
        )
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed fetching snapshot info post creation", **result
            )
        result["response"] = resp
        result["snapshot_uuid"] = resp.get("id")

    result["changed"] = True


def verify_snapshot_expiry_idempotency(old_spec, new_spec):
    if old_spec.get("expireInDays") != new_spec.get("expireInDays"):
        return False
    return True


def update_snapshot(module, result):
    uuid = module.params.get("snapshot_uuid")
    if not uuid:
        module.fail_json(msg="snapshot_uuid is required field for update", **result)

    # get current details of snapshot
    _snapshot = Snapshot(module)
    snapshot = _snapshot.read(uuid=uuid)

    # compare and update accordingly
    updated = False

    # check if rename is required
    if module.params.get("name") and module.params.get("name") != snapshot.get("name"):
        spec = _snapshot.get_rename_snapshot_spec(name=module.params["name"])
        snapshot = _snapshot.rename_snapshot(uuid=uuid, data=spec)
        updated = True

    # check if update/removal of expiry schedule is required
    if module.params.get("remove_expiry"):
        spec = _snapshot.get_remove_expiry_spec(uuid=uuid, name=snapshot.get("name"))
        snapshot = _snapshot.remove_expiry(uuid=uuid, data=spec)
        updated = True

    elif module.params.get("expiry_days"):
        spec = _snapshot.get_expiry_update_spec(config=module.params)
        lcm_config = snapshot.get("lcmConfig", {}) or {}
        expiry_details = lcm_config.get("expiryDetails", {})
        if not verify_snapshot_expiry_idempotency(
            expiry_details, spec.get("lcmConfig", {}).get("expiryDetails", {})
        ):
            snapshot = _snapshot.update_expiry(uuid, spec)
            updated = True

    if not updated:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    snapshot = _snapshot.read(
        uuid=uuid, query={"load-replicated-child-snapshots": True}
    )
    result["snapshot_uuid"] = uuid
    result["response"] = snapshot
    result["changed"] = True


# Delete snapshot
def delete_snapshot(module, result):
    snapshot_uuid = module.params.get("snapshot_uuid")
    if not snapshot_uuid:
        module.fail_json(msg="snapshot_uuid is required field for delete", **result)

    snapshots = Snapshot(module)
    resp = snapshots.delete(uuid=snapshot_uuid)

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get ops ID functional
        resp = operations.wait_for_completion(ops_uuid, delay=2)

    result["response"] = resp
    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ("snapshot_uuid", "time_machine_uuid"),
            ("remove_expiry", "expiry_days"),
        ],
        required_if=[
            ("state", "present", ("name", "snapshot_uuid"), True),
            ("state", "present", ("snapshot_uuid", "time_machine_uuid"), True),
            ("state", "absent", ("snapshot_uuid",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "snapshot_uuid": None}

    if module.params["state"] == "present":
        if module.params.get("snapshot_uuid"):
            update_snapshot(module, result)
        else:
            create_snapshot(module, result)
    else:
        delete_snapshot(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
