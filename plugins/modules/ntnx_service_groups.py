#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_service_groups
short_description: service_groups module which suports service_groups CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete service_group'
options:
  nutanix_host:
    description:
      - PC hostname or IP address
    type: str
    required: true
  nutanix_port:
    description:
      - PC port
    type: str
    default: 9440
    required: false
  nutanix_username:
    description:
      - PC username
    type: str
    required: true
  nutanix_password:
    description:
      - PC password;
    required: true
    type: str
  validate_certs:
    description:
      - Set value to C(False) to skip validation for self signed certificates
      - This is not recommended for production setup
    type: bool
    default: true
  state:
    description:
      - Specify state of service_groups
      - If C(state) is set to C(present) then service_groups is created.
      - >-
        If C(state) is set to C(absent) and if the service_groups exists, then
        service_groups is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for service_groups CRUD operation to complete.
    type: bool
    required: false
    default: True
  name:
    description: service_groups Name
    required: False
    type: str
  service_group_uuid:
    description: service_group UUID
    type: str

  # Step 4: here should be additional arguments documentation

"""

EXAMPLES = r"""
# Step 5
"""

RETURN = r"""
# Step 6
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.service_groups import ServiceGroup  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    icmp_spec = dict(code=dict(type="int"), type=dict(type="int"))

    service_spec = dict(
        tcp=dict(type="list", elements="str"),
        udp=dict(type="list", elements="str"),
        icmp=dict(
            type="list",
            elements="dict",
            options=icmp_spec,
        ),
        any_icmp=dict(type="bool", default=False),
    )

    module_args = dict(
        name=dict(type="str"),
        desc=dict(type="str"),
        service_group_uuid=dict(type="str"),
        services=dict(
            type="dict",
            options=service_spec,
            mutually_exclusive=[("icmp", "any_icmp")]
        ),
    )

    return module_args


def create_service_group(module, result):
    service_group = ServiceGroup(module)
    spec, error = service_group.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating service_groups spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = service_group.create(spec)
    service_group_uuid = resp["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["service_group_uuid"] = service_group_uuid
    # result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait") and result.get("task_uuid"):
        wait_for_task_completion(module, result)
        resp = service_group.read(service_group_uuid)
        result["response"] = resp


def update_service_group(module, result):
    service_group = ServiceGroup(module)
    service_group_uuid = module.params.get("service_group_uuid")
    if not service_group_uuid:
        result["error"] = "Missing parameter service_group_uuid in playbook"
        module.fail_json(msg="Failed updating service_group", **result)
    result["service_group_uuid"] = service_group_uuid

    # read the current state of service_group
    resp = service_group.read(service_group_uuid)
    resp = resp.get("service_group")

    # new spec for updating service_group
    update_spec, error = service_group.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating service_group update spec", **result)

    # check for idempotency
    if resp == update_spec:
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. Refer docs to check for fields which can be updated"
        )

    if module.check_mode:
        result["response"] = update_spec
        return

    # update service_group
    resp = service_group.update(update_spec, uuid=service_group_uuid, raise_error=False)

    result["changed"] = True
    result["response"] = resp


def delete_service_group(module, result):
    service_group_uuid = module.params["service_group_uuid"]
    if not service_group_uuid:
        result["error"] = "Missing parameter service_group_uuid in playbook"
        module.fail_json(msg="Failed deleting service_groups", **result)

    service_group = ServiceGroup(module)
    resp = service_group.delete(service_group_uuid)
    result["changed"] = True
    result["response"] = resp
    result["service_group_uuid"] = service_group_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid)
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "service_group_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "absent":
        delete_service_group(module, result)
    elif module.params.get("service_group_uuid"):
        update_service_group(module, result)
    else:
        create_service_group(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

