#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ndb_authorize_db_server_vms
short_description: module for authorizing db server vm
version_added: 1.8.0
description: module for authorizing db server vm with time machine
options:
      db_server_vms:
        description:
            - list of database server vms details
        type: list
        elements: dict
        required: true
        suboptions:
            name:
                description:
                    - name of database server vm
                    - mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - uuid of database server vm
                    - mutually exclusive with C(name)
                type: str
      time_machine:
        description:
            - time machine details
        type: dict
        required: true
        suboptions:
            name:
                description:
                    - name of time machine
                    - mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - uuid of time machine
                    - mutually exclusive with C(name)
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
- name: authorize db server vms
  ntnx_ndb_authorize_db_server_vms:
    time_machine:
      name: "{{tm1}}"
    db_server_vms:
      - name: "{{vm1_name}}"
  register: result

- name: deauthorize db server vms
  ntnx_ndb_authorize_db_server_vms:
    time_machine:
      name: "{{tm1}}"
    db_server_vms:
      - name: "{{vm1_name}}"
  register: result
"""
RETURN = r"""
response:
  description: An intentful representation of a authorization status
  returned: always
  type: dict
  sample: {
            "errorCode": 0,
            "info": null,
            "message": "The DBServer(s) [5c14b4d4-553f-4b93-a3c4-a6685da2732b]
                        got successfully associated with the Time Machine (id:7a39664b-dfb7-4529-887c-6d91f7e18604, name:test-setup-dnd_TM)",
            "status": "success"
        }
uuid:
  description: Time machine uuid
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""


from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.v3.ndb.time_machines import TimeMachine  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    module_args = dict(
        db_server_vms=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        time_machine=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
    )
    return module_args


def authorize_db_server_vms(module, result):
    time_machine = TimeMachine(module)
    if not module.params.get("time_machine"):
        module.fail_json(
            msg="'time_machine' is required for authorizing db server vms with time machine"
        )

    time_machine_uuid, err = time_machine.get_time_machine_uuid(
        module.params.get("time_machine")
    )
    if err:
        result["response"] = err
        module.fail_json(msg="Failed fetching time machine uuid", **result)

    spec, err = time_machine.get_authorize_db_server_vms_spec()
    if err:
        result["response"] = err
        module.fail_json(msg="Failed getting authorizing db server vm spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = time_machine.authorize_db_server_vms(uuid=time_machine_uuid, data=spec)
    result["response"] = resp
    result["uuid"] = time_machine_uuid
    result["changed"] = True


def deauthorize_db_server_vms(module, result):
    time_machine = TimeMachine(module)
    if not module.params.get("time_machine"):
        module.fail_json(
            msg="'time_machine' is required for deauthorizing db server vms with time machine"
        )

    time_machine_uuid, err = time_machine.get_time_machine_uuid(
        module.params.get("time_machine")
    )
    if err:
        result["response"] = err
        module.fail_json(msg="Failed fetching time machine uuid", **result)

    spec, err = time_machine.get_authorize_db_server_vms_spec()
    if err:
        result["response"] = err
        module.fail_json(msg="Failed getting deauthorizing db server vm spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = time_machine.deauthorize_db_server_vms(uuid=time_machine_uuid, data=spec)
    result["response"] = resp
    result["uuid"] = time_machine_uuid
    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    if module.params.get("state") == "present":
        authorize_db_server_vms(module, result)
    else:
        deauthorize_db_server_vms(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
