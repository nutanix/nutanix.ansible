#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
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
    default: true
  name:
    description: security_rule Name
    required: false
    type: str
  security_rule_uuid:
    description: security_rule UUID
    type: str
  allow_ipv6_traffic:
    description: Allow traffic from ipv6
    type: bool
  is_policy_hitlog_enabled:
    description: write
    type: bool
  ad_rule:
    description: >-
      These rules are used for quarantining suspected VMs. Target group is a
      required attribute. Empty inbound_allow_list will not allow anything into
      target group. Empty outbound_allow_list will allow everything from target
      group.
    type: dict
    suboptions:
      action:
        description: Type of deployment of the rule.
        type: str
      target_group:
        description: Target Group
        type: dict
        suboptions:
          peer_specification_type:
            description: Way to identify the object for which rule is applied.
            type: str
          default_internal_policy:
            description: Default policy for communication within target group.
            type: str
          filter:
            description: A category filter.
            type: dict
            suboptions:
              type:
                description: The type of the filter being used.
                type: str
              params:
                description: A list of category key and list of values.
                type: dict
              kind_list:
                description: List of kinds associated with this filter.
                type: list
                elements: str
      inbound_allow_list:
        description: Array of inbound Network rule
        type: list
        elements: dict
        suboptions:
          peer_specification_type:
            description: Way to identify the object for which rule is applied.
            type: str
          expiration_time:
            description: Timestamp of expiration time.
            type: str
          description:
            type: str
            description: >-
              Description for network security rule that is for inbound or
              outbound
          rule_id:
            type: int
            description: >-
              Unique identifier for inbound or outbound rule. This is system
              generated and used internally. User should not set this field
              while creating a new rule or should not modify it while updating
              the existing rule.
          protocol:
            type: str
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
          filter:
            description: A category filter.
            type: dict
            suboptions:
              type:
                description: The type of the filter being used.
                type: str
              params:
                description: A list of category key and list of values.
                type: dict
              kind_list:
                description: List of kinds associated with this filter.
                type: list
                elements: str
          address_group_inclusion_list:
            type: list
            elements: dict
            description: List of address groups that are allowed access by this rule
            suboptions:
              uuid:
                description: UUID
                type: str
          service_group_list:
            type: list
            elements: dict
            description: >-
              List of service groups associated with this rule. The exiting
              fields for protocol or ports is not recommended for use and will
              be deprecated for these new fields at the API level.
            suboptions:
              uuid:
                description: UUID
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix:
                description: prefix length
                type: str
          tcp_port_range_list:
            description: List of TCP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          udp_port_range_list:
            description: List of UDP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          icmp:
            description: List of ICMP types and codes allowed by this rule.
            elements: dict
            type: list
            suboptions:
              any:
                description: any
                type: bool
              code:
                description: ICMP code
                type: int
              type:
                description: ICMP type
                type: int
          network_function_chain_reference:
            type: dict
            description: The reference to a network_function_chain
            suboptions:
              uuid:
                type: str
                description: UUID
      outbound_allow_list:
        description: Array of Outbound Network rule
        type: list
        elements: dict
        suboptions:
          peer_specification_type:
            description: Way to identify the object for which rule is applied.
            type: str
          expiration_time:
            description: Timestamp of expiration time.
            type: str
          description:
            type: str
            description: >-
              Description for network security rule that is for inbound or
              outbound
          rule_id:
            type: int
            description: >-
              Unique identifier for inbound or outbound rule. This is system
              generated and used internally. User should not set this field
              while creating a new rule or should not modify it while updating
              the existing rule.
          protocol:
            type: str
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
          filter:
            description: A category filter.
            type: dict
            suboptions:
              type:
                description: The type of the filter being used.
                type: str
              params:
                description: A list of category key and list of values.
                type: dict
              kind_list:
                description: List of kinds associated with this filter.
                type: list
                elements: str
          address_group_inclusion_list:
            type: list
            elements: dict
            description: List of address groups that are allowed access by this rule
            suboptions:
              uuid:
                description: UUID
                type: str
          service_group_list:
            type: list
            elements: dict
            description: >-
              List of service groups associated with this rule. The exiting
              fields for protocol or ports is not recommended for use and will
              be deprecated for these new fields at the API level.
            suboptions:
              uuid:
                description: UUID
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix:
                description: prefix length
                type: str
          tcp_port_range_list:
            description: List of TCP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          udp_port_range_list:
            description: List of UDP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          icmp:
            description: List of ICMP types and codes allowed by this rule.
            elements: dict
            type: list
            suboptions:
              any:
                description: any
                type: bool
              code:
                description: ICMP code
                type: int
              type:
                description: ICMP type
                type: int
          network_function_chain_reference:
            type: dict
            description: The reference to a network_function_chain
            suboptions:
              uuid:
                type: str
                description: UUID
  app_rule:
    description: >-
      These rules are used for quarantining suspected VMs. Target group is a
      required attribute. Empty inbound_allow_list will not allow anything into
      target group. Empty outbound_allow_list will allow everything from target
      group.
    type: dict
    suboptions:
      action:
        description: Type of deployment of the rule.
        type: str
      target_group:
        description: Target Group
        type: dict
        suboptions:
          peer_specification_type:
            description: Way to identify the object for which rule is applied.
            type: str
          default_internal_policy:
            description: Default policy for communication within target group.
            type: str
          filter:
            description: A category filter.
            type: dict
            suboptions:
              type:
                description: The type of the filter being used.
                type: str
              params:
                description: A list of category key and list of values.
                type: dict
              kind_list:
                description: List of kinds associated with this filter.
                type: list
                elements: str
      inbound_allow_list:
        description: Array of inbound Network rule
        type: list
        elements: dict
        suboptions:
          peer_specification_type:
            description: Way to identify the object for which rule is applied.
            type: str
          expiration_time:
            description: Timestamp of expiration time.
            type: str
          description:
            type: str
            description: >-
              Description for network security rule that is for inbound or
              outbound
          rule_id:
            type: int
            description: >-
              Unique identifier for inbound or outbound rule. This is system
              generated and used internally. User should not set this field
              while creating a new rule or should not modify it while updating
              the existing rule.
          protocol:
            type: str
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
          filter:
            description: A category filter.
            type: dict
            suboptions:
              type:
                description: The type of the filter being used.
                type: str
              params:
                description: A list of category key and list of values.
                type: dict
              kind_list:
                description: List of kinds associated with this filter.
                type: list
                elements: str
          address_group_inclusion_list:
            type: list
            elements: dict
            description: List of address groups that are allowed access by this rule
            suboptions:
              uuid:
                description: UUID
                type: str
          service_group_list:
            type: list
            elements: dict
            description: >-
              List of service groups associated with this rule. The exiting
              fields for protocol or ports is not recommended for use and will
              be deprecated for these new fields at the API level.
            suboptions:
              uuid:
                description: UUID
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix:
                description: prefix length
                type: str
          tcp_port_range_list:
            description: List of TCP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          udp_port_range_list:
            description: List of UDP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          icmp:
            description: List of ICMP types and codes allowed by this rule.
            elements: dict
            type: list
            suboptions:
              any:
                description: any
                type: bool
              code:
                description: ICMP code
                type: int
              type:
                description: ICMP type
                type: int
          network_function_chain_reference:
            type: dict
            description: The reference to a network_function_chain
            suboptions:
              uuid:
                type: str
                description: UUID
      outbound_allow_list:
        description: Array of Outbound Network rule
        type: list
        elements: dict
        suboptions:
          peer_specification_type:
            description: Way to identify the object for which rule is applied.
            type: str
          expiration_time:
            description: Timestamp of expiration time.
            type: str
          description:
            type: str
            description: >-
              Description for network security rule that is for inbound or
              outbound
          rule_id:
            type: int
            description: >-
              Unique identifier for inbound or outbound rule. This is system
              generated and used internally. User should not set this field
              while creating a new rule or should not modify it while updating
              the existing rule.
          protocol:
            type: str
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
          filter:
            description: A category filter.
            type: dict
            suboptions:
              type:
                description: The type of the filter being used.
                type: str
              params:
                description: A list of category key and list of values.
                type: dict
              kind_list:
                description: List of kinds associated with this filter.
                type: list
                elements: str
          address_group_inclusion_list:
            type: list
            elements: dict
            description: List of address groups that are allowed access by this rule
            suboptions:
              uuid:
                description: UUID
                type: str
          service_group_list:
            type: list
            elements: dict
            description: >-
              List of service groups associated with this rule. The exiting
              fields for protocol or ports is not recommended for use and will
              be deprecated for these new fields at the API level.
            suboptions:
              uuid:
                description: UUID
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix:
                description: prefix length
                type: str
          tcp_port_range_list:
            description: List of TCP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          udp_port_range_list:
            description: List of UDP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          icmp:
            description: List of ICMP types and codes allowed by this rule.
            elements: dict
            type: list
            suboptions:
              any:
                description: any
                type: bool
              code:
                description: ICMP code
                type: int
              type:
                description: ICMP type
                type: int
          network_function_chain_reference:
            type: dict
            description: The reference to a network_function_chain
            suboptions:
              uuid:
                type: str
                description: UUID
  isolation_rule:
    description: These rules are used for environmental isolation.
    type: dict
    suboptions:
      action:
        description: Type of deployment of the rule.
        type: str
      first_entity_filter:
        description: A category filter.
        type: dict
        suboptions:
          type:
            description: The type of the filter being used.
            type: str
          params:
            description: A list of category key and list of values.
            type: dict
          kind_list:
            description: List of kinds associated with this filter.
            type: list
            elements: str
      second_entity_filter:
        description: A category filter.
        type: dict
        suboptions:
          type:
            description: The type of the filter being used.
            type: str
          params:
            description: A list of category key and list of values.
            type: dict
          kind_list:
            description: List of kinds associated with this filter.
            type: list
            elements: str
  quarantine_rule:
    description: >-
      These rules are used for quarantining suspected VMs. Target group is a
      required attribute. Empty inbound_allow_list will not allow anything into
      target group. Empty outbound_allow_list will allow everything from target
      group.
    type: dict
    suboptions:
      action:
        description: Type of deployment of the rule.
        type: str
      target_group:
        description: Target Group
        type: dict
        suboptions:
          peer_specification_type:
            description: Way to identify the object for which rule is applied.
            type: str
          default_internal_policy:
            description: Default policy for communication within target group.
            type: str
          filter:
            description: A category filter.
            type: dict
            suboptions:
              type:
                description: The type of the filter being used.
                type: str
              params:
                description: A list of category key and list of values.
                type: dict
              kind_list:
                description: List of kinds associated with this filter.
                type: list
                elements: str
      inbound_allow_list:
        description: Array of inbound Network rule
        type: list
        elements: dict
        suboptions:
          peer_specification_type:
            description: Way to identify the object for which rule is applied.
            type: str
          expiration_time:
            description: Timestamp of expiration time.
            type: str
          description:
            type: str
            description: >-
              Description for network security rule that is for inbound or
              outbound
          rule_id:
            type: int
            description: >-
              Unique identifier for inbound or outbound rule. This is system
              generated and used internally. User should not set this field
              while creating a new rule or should not modify it while updating
              the existing rule.
          protocol:
            type: str
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
          filter:
            description: A category filter.
            type: dict
            suboptions:
              type:
                description: The type of the filter being used.
                type: str
              params:
                description: A list of category key and list of values.
                type: dict
              kind_list:
                description: List of kinds associated with this filter.
                type: list
                elements: str
          address_group_inclusion_list:
            type: list
            elements: dict
            description: List of address groups that are allowed access by this rule
            suboptions:
              uuid:
                description: UUID
                type: str
          service_group_list:
            type: list
            elements: dict
            description: >-
              List of service groups associated with this rule. The exiting
              fields for protocol or ports is not recommended for use and will
              be deprecated for these new fields at the API level.
            suboptions:
              uuid:
                description: UUID
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix:
                description: prefix length
                type: str
          tcp_port_range_list:
            description: List of TCP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          udp_port_range_list:
            description: List of UDP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          icmp:
            description: List of ICMP types and codes allowed by this rule.
            elements: dict
            type: list
            suboptions:
              any:
                description: any
                type: bool
              code:
                description: ICMP code
                type: int
              type:
                description: ICMP type
                type: int
          network_function_chain_reference:
            type: dict
            description: The reference to a network_function_chain
            suboptions:
              uuid:
                type: str
                description: UUID
      outbound_allow_list:
        description: Array of Outbound Network rule
        type: list
        elements: dict
        suboptions:
          peer_specification_type:
            description: Way to identify the object for which rule is applied.
            type: str
          expiration_time:
            description: Timestamp of expiration time.
            type: str
          description:
            type: str
            description: >-
              Description for network security rule that is for inbound or
              outbound
          rule_id:
            type: int
            description: >-
              Unique identifier for inbound or outbound rule. This is system
              generated and used internally. User should not set this field
              while creating a new rule or should not modify it while updating
              the existing rule.
          protocol:
            type: str
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
          filter:
            description: A category filter.
            type: dict
            suboptions:
              type:
                description: The type of the filter being used.
                type: str
              params:
                description: A list of category key and list of values.
                type: dict
              kind_list:
                description: List of kinds associated with this filter.
                type: list
                elements: str
          address_group_inclusion_list:
            type: list
            elements: dict
            description: List of address groups that are allowed access by this rule
            suboptions:
              uuid:
                description: UUID
                type: str
          service_group_list:
            type: list
            elements: dict
            description: >-
              List of service groups associated with this rule. The exiting
              fields for protocol or ports is not recommended for use and will
              be deprecated for these new fields at the API level.
            suboptions:
              uuid:
                description: UUID
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix:
                description: prefix length
                type: str
          tcp_port_range_list:
            description: List of TCP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          udp_port_range_list:
            description: List of UDP ports that are allowed by this rule.
            type: list
            elements: dict
            suboptions:
              src:
                description: start_port
                type: list
                elements: str
                default: '*'
              dst:
                description: end_port
                type: list
                elements: str
                default: '*'
          icmp:
            description: List of ICMP types and codes allowed by this rule.
            elements: dict
            type: list
            suboptions:
              any:
                description: any
                type: bool
              code:
                description: ICMP code
                type: int
              type:
                description: ICMP type
                type: int
          network_function_chain_reference:
            type: dict
            description: The reference to a network_function_chain
            suboptions:
              uuid:
                type: str
                description: UUID
author:
  - Prem Karat (@premkarat)
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)

"""

EXAMPLES = r"""
# Step 5
"""

RETURN = r"""
# Step 6
"""


from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.security_rules import SecurityRule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    group_spec = dict(uuid=dict(type="str"))

    tcp_and_udp_spec = dict(
        start_port=dict(type="int"),
        end_port=dict(type="int"),
    )

    network_spec = dict(ip=dict(type="str"), prefix_length=dict(type="int"))

    icmp_spec = dict(
        code=dict(type="int"), type=dict(type="int")
    )

    filters_spec = dict(
        type=dict(type="str"),
        kind_list=dict(type="list", elements="str", required=True),
        params=dict(type="dict", required=True),
    )

    target_spec = dict(
        peer_specification_type=dict(type="str"),
        filter=dict(type="dict", options=filters_spec),
        default_internal_policy=dict(type="str"),
    )

    bound_allow_spec = dict(
        peer_specification_type=dict(type="str", choices=['ALL', 'FILTER', 'IP_SUBNET'], required=True),
        filter=dict(type="dict", options=filters_spec, required=True),
        address_group_inclusion_list=dict(
            type="list", elements="dict", options=group_spec
        ),
        ip_subnet=dict(type="dict", options=network_spec),
        service_group_list=dict(type="list", elements="dict", options=group_spec),
        protocol=dict(type="str", choices=['ALL', 'ICMP', 'TCP', 'UDP']),
        tcp_port_range_list=dict(
            type="list", elements="dict", options=tcp_and_udp_spec
        ),
        udp_port_range_list=dict(
            type="list", elements="dict", options=tcp_and_udp_spec
        ),
        icmp_type_code_list=dict(type="list", elements="dict", options=icmp_spec),
        network_function_chain_reference=dict(
            type="dict", options=dict(uuid=dict(type="str"))
        ),
        expiration_time=dict(type="str"),
        description=dict(type="str"),
        rule_id=dict(type="int"),
    )

    rule_spec = dict(
        target_group=dict(type="dict", options=target_spec),
        inbound_allow_list=dict(type="list", elements="dict", options=bound_allow_spec),
        outbound_allow_list=dict(
            type="list", elements="dict", options=bound_allow_spec
        ),
        action=dict(type="str", choices=["MONITOR", "APPLY"]),
    )

    isolation_rule_spec = dict(
        first_entity_filter=dict(type="dict", options=filters_spec, required=True),
        second_entity_filter=dict(type="dict", options=filters_spec, required=True),
        action=dict(type="str", choices=["MONITOR", "APPLY"]),
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


def update_security_rule(module, result):
    security_rule_uuid = module.params["security_rule_uuid"]
    state = module.params.get("state")

    security_rule = SecurityRule(module)
    resp = security_rule.read(security_rule_uuid)
    result["response"] = resp
    utils.strip_extra_attrs_from_status(resp["status"], resp["spec"])
    resp.pop("status")

    spec, error = security_rule.get_spec(resp)

    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating security_rule spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    if utils.check_for_idempotency(spec, resp, state=state):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change")

    resp = security_rule.update(spec, security_rule_uuid)
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
    module = BaseModule(argument_spec=get_module_spec(),
                        supports_check_mode=True,
                        mutually_exclusive=[("ad_rule", "app_rule", "isolation_rule", "quarantine_rule")],
                        required_by={
                            "quarantine_rule": "security_rule_uuid",
                        }
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
    if state == "absent":
        delete_security_rule(module, result)
    elif module.params.get("security_rule_uuid"):
        update_security_rule(module, result)
    else:
        create_security_rule(module, result)


    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
