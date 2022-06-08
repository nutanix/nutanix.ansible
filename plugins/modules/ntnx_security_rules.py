#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_rules
short_description: security_rule module which suports security_rule CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete security_rule'
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
      - Specify state of security_rule
      - If C(state) is set to C(present) then security_rule is created.
      - >-
        If C(state) is set to C(absent) and if the security_rule exists, then
        security_rule is removed.
    choices:
      - present
      - absent
    type: str
    default: present
  wait:
    description: Wait for security_rule CRUD operation to complete.
    type: bool
    required: false
    default: True
  name:
    description: security_rule Name
    required: False
    type: str
  security_rule_uuid:
    description: security_rule UUID
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
from ..module_utils.prism.security_rules import SecurityRule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    group_spec = dict(
        uuid=dict(type="str")
    )
    tcp_and_udp_spec = dict(
        src=dict(type="list", default=["*"], elements="str"),
        dst=dict(type="list", default=["*"], elements="str"),
    )

    network_spec = dict(ip=dict(type="str"), prefix=dict(type="str"))

    icmp_spec = dict(
        any=dict(type="bool"), code=dict(type="int"), type=dict(type="int")
    )
    filters_spec = dict(
        type=dict(type="str"),
        kind_list=dict(type="list", elements="str"),
        params=dict(type="dict"),
    )

    target_spec = dict(
        peer_specification_type=dict(type="str"),
        filter=dict(type="dict", options=filters_spec),
        default_internal_policy=dict(type="str"),
    )
    bound_allow_spec = dict(
        peer_specification_type=dict(type="str"),
        filter=dict(type="dict", options=filters_spec),
        address_group_inclusion_list=dict(type="list", elements="dict", options=group_spec),
        ip_subnet=dict(type="dict", options=network_spec),
        service_group_list=dict(type="list", elements="dict", options=group_spec),
        protocol=dict(type="str"),
        tcp_port_range_list=dict(type="list", elements="dict", options=tcp_and_udp_spec),
        udp_port_range_list=dict(type="list", elements="dict", options=tcp_and_udp_spec),
        icmp=dict(type="list", elements="dict", options=icmp_spec),
        network_function_chain_reference=dict(type="dict", options=dict(uuid=dict(type="str"))),
        expiration_time=dict(type="str"),
        description=dict(type="str"),
        rule_id=dict(type="int"),
    )

    rule_spec = dict(
        target_group=dict(type="dict", options=target_spec),
        inbound_allow_list=dict(type="list", elements="dict", options=bound_allow_spec),
        outbound_allow_list=dict(type="list", elements="dict", options=bound_allow_spec),
        action=dict(type="str"),
    )

    isolation_rule_spec = dict(
        first_entity_filter=dict(type="dict", options=filters_spec),
        second_entity_filter=dict(type="dict", options=filters_spec),
        action=dict(type="str"),
    )
    module_args = dict(
        name=dict(type="str"),
        security_rule_uuid=dict(type="str"),
        allow_ipv6_traffic=dict(type="bool"),
        is_policy_hitlog_enabled=dict(type="bool"),
        ad_rule=dict(type="dict", options=rule_spec),
        app_rule=dict(type="dict", options=rule_spec),
        isolation_rule=dict(type="dict", options=isolation_rule_spec),
        quarantine_rule=dict(type="dict", options=rule_spec),
    )

    return module_args


def create_security_rule(module, result):
    security_rule = SecurityRule(module)
    spec, error = security_rule.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating security_rule spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = security_rule.create(spec)
    security_rule_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    result["security_rule_uuid"] = security_rule_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = security_rule.read(security_rule_uuid)
        result["response"] = resp


def delete_security_rule(module, result):
    security_rule_uuid = module.params["security_rule_uuid"]
    if not security_rule_uuid:
        result["error"] = "Missing parameter security_rule_uuid in playbook"
        module.fail_json(msg="Failed deleting security_rule", **result)

    security_rule = SecurityRule(module)
    resp = security_rule.delete(security_rule_uuid)
    result["changed"] = True
    result["response"] = resp
    result["security_rule_uuid"] = security_rule_uuid
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
        "security_rule_uuid": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_security_rule(module, result)
    elif state == "absent":
        delete_security_rule(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
