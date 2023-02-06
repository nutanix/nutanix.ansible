#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ndb_maintenance_tasks
short_description: write
version_added: 1.8.0
description: 'write'
options:
      db_server_vms:
        description:
            - write
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - write
                type: str
            uuid:
                description:
                    - write
                type: str

      db_server_clusters:
        description:
            - write
        type: list
        elements: dict
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

from copy import deepcopy  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.maintenance_window import (  # noqa: E402
    AutomatedPatchingSpec,
    MaintenanceWindow,
)
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    automated_patching = deepcopy(
        AutomatedPatchingSpec.automated_patching_argument_spec
    )
    module_args = dict(
        db_server_vms=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        db_server_clusters=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
    )
    module_args.update(automated_patching)

    # maintenance window ID is always required for updating maintenance tasks
    module_args["maintenance_window"]["required"] = True
    return module_args


def update_maintenance_tasks(module, result):
    maintenance_window = MaintenanceWindow(module)

    spec, err = maintenance_window.get_spec(configure_automated_patching=True)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed getting spec for updating maitenance tasks",
            **result,
        )

    if module.check_mode:
        result["response"] = spec
        return

    uuid = spec.get("maintenanceWindowId")

    maintenance_window.update_tasks(data=spec)

    query = {"load-task-associations": True, "load-entities": True}
    resp = maintenance_window.read(uuid=uuid, query=query)
    result["response"] = resp
    result["uuid"] = uuid
    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("db_server_vms", "db_server_clusters"), True)
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    update_maintenance_tasks(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
