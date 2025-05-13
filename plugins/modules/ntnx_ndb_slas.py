#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_slas
short_description: moudle for creating, updating and deleting slas
version_added: 1.8.0
description: moudle for creating, updating and deleting slas
options:
      name:
        description:
            - sla name
        type: str
      desc:
        description:
            - sla description
        type: str
      sla_uuid:
        description:
            - sla uuid
            - will be used to update if C(state) is C(present) and to delete if C(state) is C(absent)
        type: str
      frequency:
        description:
            - frequency of retention
        type: dict
        suboptions:
            logs_retention:
                description:
                    - duration in days for which the transaction logs are retained in NDB
                type: int
            snapshots_retention:
                description:
                    - snapshot retention details
                type: dict
                suboptions:
                    daily:
                        description:
                            - duration in days for which a daily snapshot must be retained in NDB
                        type: int
                    weekly:
                        description:
                            - duration in weeks for which a weekly snapshot must be retained in NDB
                        type: int
                    monthly:
                        description:
                            - duration in months for which a monthly snapshot must be retained in NDB
                        type: int
                    quarterly:
                        description:
                            - duration in quarters for which a quarterly snapshot must be retained in NDB
                        type: int
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Verify creation of slas
  ntnx_ndb_slas:
    name: "{{profile1_name}}"
    desc: "testdesc"
    frequency:
      logs_retention: "{{frequency.logs_retention}}"
      snapshots_retention:
        daily: "{{frequency.snapshots_retention.daily}}"
        weekly: "{{frequency.snapshots_retention.weekly}}"
        monthly: "{{frequency.snapshots_retention.monthly}}"
        quarterly: "{{frequency.snapshots_retention.quarterly}}"
  register: result
"""

RETURN = r"""
response:
  description: slas create response
  returned: always
  type: dict
  sample: {
        "id": "13d1dabe-d4aa-4ab5-b8c4-7adb4c41af03",
        "name": "check",
        "uniqueName": "CHECK",
        "description": "check",
        "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
        "systemSla": false,
        "dateCreated": null,
        "dateModified": null,
        "continuousRetention": 30,
        "dailyRetention": 7,
        "weeklyRetention": 2,
        "monthlyRetention": 2,
        "quarterlyRetention": 1,
        "yearlyRetention": 0,
        "referenceCount": 0,
        "pitrEnabled": true,
        "currentActiveFrequency": "CONTINUOUS"
        }
sla_uuid:
  description: sla uuid
  returned: always
  type: str
  sample: "be524e70-60ad-4a8c-a0ee-8d72f954d7e6"
"""

from ..module_utils.utils import (  # noqa: E402
    remove_param_with_none_value,
    strip_extra_attrs,
)
from ..module_utils.v3.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.v3.ndb.slas import SLA  # noqa: E402


def get_module_spec():

    snapshot_retention = dict(
        daily=dict(type="int"),
        weekly=dict(type="int"),
        monthly=dict(type="int"),
        quarterly=dict(type="int"),
    )
    frequency = dict(
        logs_retention=dict(type="int"),
        snapshots_retention=dict(type="dict", options=snapshot_retention),
    )
    module_args = dict(
        sla_uuid=dict(type="str"),
        name=dict(type="str"),
        desc=dict(type="str"),
        frequency=dict(type="dict", options=frequency),
    )
    return module_args


def create_sla(module, result):
    sla = SLA(module)

    name = module.params["name"]
    uuid = sla.get_uuid(value=name, raise_error=False)
    if uuid:
        module.fail_json(msg="sla with given name already exists", **result)

    spec, err = sla.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create sla spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = sla.create(data=spec)
    result["response"] = resp
    result["sla_uuid"] = resp["id"]
    result["changed"] = True


def update_sla(module, result):
    _sla = SLA(module)

    uuid = module.params.get("sla_uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for update", **result)
    result["sla_uuid"] = uuid

    sla, err = _sla.get_sla(uuid=uuid)
    if err:
        module.fail_json(msg="Failed fetching sla info", **result)

    if sla.get("systemSla"):
        module.fail_json(msg="system slas update is not allowed", **result)

    default_update_spec = _sla.get_default_update_spec()
    strip_extra_attrs(sla, default_update_spec)

    spec, err = _sla.get_spec(old_spec=sla)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update sla spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    if spec == sla:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")
    spec["id"] = uuid
    resp = _sla.update(data=spec, uuid=uuid)
    result["response"] = resp
    result["sla_uuid"] = uuid
    result["changed"] = True


def delete_sla(module, result):
    _sla = SLA(module)

    uuid = module.params.get("sla_uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for delete", **result)

    sla, err = _sla.get_sla(uuid=uuid)
    if err:
        module.fail_json(msg="Failed fetching sla info", **result)

    if sla.get("systemSla"):
        module.fail_json(msg="system slas delete is not allowed", **result)

    resp = _sla.delete(data=sla, uuid=uuid)
    result["response"] = resp
    if resp.get("status") != "success":
        module.fail_json(
            msg="sla delete failed",
            response=resp,
        )
    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        required_if=[
            ("state", "present", ("name", "sla_uuid"), True),
            ("state", "absent", ("sla_uuid",)),
        ],
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "sla_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("sla_uuid"):
            update_sla(module, result)
        else:
            create_sla(module, result)
    else:
        delete_sla(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
