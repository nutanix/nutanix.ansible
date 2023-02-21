#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_database_replicate_snapshots
short_description: write
version_added: 1.8.0
description: 'write'
options:
      expiry_days:
        description:
            - write
        type: str
      snapshot_uuid:
        description:
            - write
        type: str
      timezone:
        description:
            - write
        type: str
      clusters:
        description:
            - write
        type: list
        elements: dict
        required: true
        suboptions:
            name:
                description:
                    - write
                type: str
            uuid:
                description:
                    - write
                type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
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

# Notes:
# 1. Snapshot replication to one cluster at a time is supported currently
# 2. For snapshot on secondary cluster, this module only tracks primary cluster snapshot process


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
        timezone=dict(type="str", required=False),
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
        required_together=[("expiry_days", "timezone")],
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
