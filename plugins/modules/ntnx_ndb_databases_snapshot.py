#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""
import time  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.databases import Database  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.ndb.snapshots import Snapshot  # noqa: E402
from ..module_utils.ndb.time_machines import TimeMachine  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    module_args = dict(
        snapshot_uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        time_machine=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        database=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        expiry_days=dict(type="str", required=False),
        remove_expiry=dict(type="bool", required=False),
        timezone=dict(type="str", required=False),
    )
    return module_args


# Create snapshot out of database instance or time machine
def create_snapshot(module, result):
    time_machine_uuid = ""

    # fetch uuid from time machine or database
    if module.params.get("time_machine"):
        tm = TimeMachine(module)
        time_machine_uuid, err = tm.get_time_machine_uuid(module.params["time_machine"])
        if err:
            result["error"] = err
            module.fail_json(msg="Failed fetching time machine uuid", **result)
    else:
        database = Database(module)
        db, err = database.get_database(
            name=module.params["database"].get("name"),
            uuid=module.params["database"].get("uuid"),
        )
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed fetching time machine uuid from database", **result
            )
        time_machine_uuid = db["timeMachineId"]

    snapshots = Snapshot(module)
    spec, err = snapshots.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating snapshot create spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = snapshots.create_snapshot(time_machine_uuid, spec)

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # for getting
        operations.wait_for_completion(ops_uuid)

        # get snapshot info after its finished
        resp, err = snapshots.get_snapshot(
            time_machine_uuid=time_machine_uuid, name=module.params.get("name")
        )
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed fetching snapshot info post creation", **result
            )

        result["snapshot_uuid"] = resp["id"]

    result["response"] = resp
    result["changed"] = True


def verify_snapshot_expiry_idempotency(old_spec, new_spec):
    if old_spec.get("expireInDays") != new_spec.get("expireInDays"):
        return False

    if old_spec.get("expiryDateTimezone") != new_spec.get("expiryDateTimezone"):
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
        old_spec = snapshot.get("lcmConfig", {}).get("expiryDetails", {})
        if verify_snapshot_expiry_idempotency(
            old_spec, spec["lcmConfig"]["expiryDetails"]
        ):
            snapshot = _snapshot.update_expiry(uuid, spec)
            updated = True

    if not updated:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

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
            ("time_machine", "database"),
            ("remove_expiry", "expiry_days"),
            ("remove_expiry", "timezone"),
        ],
        required_together=[("expiry_days", "timezone")],
        required_if=[
            ("state", "present", ("name", "snapshot_uuid"), True),
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
