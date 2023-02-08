#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_log_catchup
short_description: write
version_added: 1.8.0
description: 'write'
options:
      time_machine:
        description:
            - write
        type: dict
        suboptions:
            name:
                description:
                    - write
                type: str
            uuid:
                description:
                    - write
                type: str
      database:
        description:
            - write
        type: dict
        suboptions:
            name:
                description:
                    - write
                type: str
            uuid:
                description:
                    - write
                type: str
      for_restore:
        description:
            - write
        type: bool
        default: false
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
from ..module_utils.ndb.database_instances import DatabaseInstance  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.ndb.time_machines import TimeMachine  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    module_args = dict(
        time_machine_uuid = dict(type="str", required=True),
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
        mutually_exclusive=[("time_machine", "database")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}

    log_catchup(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
