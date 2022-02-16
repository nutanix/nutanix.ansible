#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_pbrs
short_description: pbr module which suports pbr CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete, Power-on, Power-off Nutanix pbr''s'
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
      - Specify state of Virtual Machine
      - If C(state) is set to C(present) the pbr is created.
      - >-
        If C(state) is set to C(absent) and the pbr exists in the cluster, pbr
        with specified name is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: This is the wait description.
    type: bool
    required: false
    default: True
  #TODO here should be additional arguments documentation
"""

EXAMPLES = r"""
# TODO
"""

RETURN = r"""
# TODO
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.pbrs import Pbr  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    network_spec = dict(
        ip=dict(),
        prefix=dict()
    )

    route_spec = dict(
        any=dict(type="bool", default=True),
        external=dict(type="bool"),
        network=dict(type="dict",
                     options=network_spec,
                     ),
    )

    tcp_and_udp_spec = dict(
        src=dict(type="list", default=["*"]),
        dst=dict(type="list", default=["*"])
    )

    icmp_spec = dict(
        code=dict(type="int"),
        type=dict(type="int")
    )

    protocol_spec = dict(
        any=dict(type="bool", default=True),
        tcp=dict(type="dict",
                 options=tcp_and_udp_spec),
        udp=dict(type="dict",
                 options=tcp_and_udp_spec),
        number=dict(type="int"),
        icmp=dict(type="dict",
                  options=icmp_spec),
    )

    action_spec = dict(
        deny=dict(type="bool"),
        allow=dict(type="bool", default=True),
        reroute=dict(type="str"),
    )

    module_args = dict(
        priority=dict(type="int", required=True),

        pbr_uuid=dict(type="str"),

        vpc=dict(type="dict",
                 options=entity_by_spec,
                 mutually_exclusive=mutually_exclusive),

        source=dict(type="dict",
                    options=route_spec,
                    apply_defaults=True,
                    mutually_exclusive=[("any", "external", "network")]),

        destination=dict(type="dict",
                         options=route_spec,
                         apply_defaults=True,
                         mutually_exclusive=[("any", "external", "network")]),

        protocol=dict(type="dict",
                      options=protocol_spec,
                      apply_defaults=True,
                      mutually_exclusive=[("any", "tcp", "udp", "number", "icmp")]
                      ),

        action=dict(type="dict",
                    options=action_spec,
                    apply_defaults=True,
                    mutually_exclusive=[("deny", "allow", "reroute")]
                    ),
    )

    return module_args


def create_pbr(module, result):
    pbr = Pbr(module)
    spec, error = pbr.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating pbr Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp, status = pbr.create(spec)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed creating pbr", **result)

    pbr_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["pbr_uuid"] = pbr_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp, tmp = pbr.read(pbr_uuid)
        result["response"] = resp


def delete_pbr(module, result):
    pbr_uuid = module.params["pbr_uuid"]
    if not pbr_uuid:
        result["error"] = "Missing parameter pbr_uuid in playbook"
        module.fail_json(msg="Failed deleting pbr", **result)

    pbr = Pbr(module)
    resp, status = pbr.delete(pbr_uuid)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed deleting pbr", **result)

    result["changed"] = True
    result["response"] = resp
    result["pbr_uuid"] = pbr_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)


def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp, status = task.wait_for_completion(task_uuid)
    result["response"] = resp
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed creating pbr", **result)


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
        "pbr_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_pbr(module, result)
    elif state == "absent":
        delete_pbr(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
