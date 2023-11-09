#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_security_rules
short_description: security_rule module which suports security_rule CRUD operations
version_added: 1.3.0
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
  policy_hitlog:
    description: Allow policy hitlog
    type: bool
  vdi_rule:
    description: >-
      These rules are used for quarantining suspected VMs. Target group is a
      required attribute. Empty inbounds will not allow anything into
      target group. Empty outbounds will allow everything from target
      group.
    type: dict
    suboptions:
      policy_mode:
        description: Type of deployment of the rule.
        type: str
        choices:
          - MONITOR
          - APPLY
      target_group:
        description: Target Group
        type: dict
        suboptions:
          default_internal_policy:
            description: Default policy for communication within target group.
            type: str
            choices: ["ALLOW_ALL", "DENY_ALL"]
          categories:
            type: dict
            description: A category's key and values
            suboptions:
              apptype:
                description: A category value.
                type: str
              apptype_filter_by_category:
                description: A category key and value.
                type: dict
              apptiers:
                description:
                  - List of AppTier category values
                  - C(apptier) is deprecated
                type: list
                elements: str
              adgroup:
                description:
                    - A category value.
                    - Mutually exclusive with c(apptype).
                type: str
      allow_all_inbounds:
            description: Allow all inbounds
            type: bool
      allow_all_outbounds:
            description: Allow all outbounds
            type: bool
      inbounds:
        description: Array of inbound Network rule
        type: list
        elements: dict
        suboptions:
          state:
            description:
                - Item's state to delete it
            type: str
            choices:
              - absent
          categories:
            type: dict
            description: A category's key and values
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
            type: dict
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
            suboptions:
              tcp:
                description: List of TCP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              udp:
                description: List of UDP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              icmp:
                description: List of ICMP types and codes allowed by this rule.
                elements: dict
                type: list
                suboptions:
                  code:
                    description: ICMP code
                    type: int
                  type:
                    description: ICMP type
                    type: int
              service:
                type: dict
                description: A service groups associated with this rule.
                suboptions:
                  uuid:
                    type: str
                    description:
                        - Service group uuid.
                        - Mutually exclusive with c(name).
                  name:
                    description:
                        - Service group name.
                        - Mutually exclusive with c(uuid).
                    type: str
          address:
            type: dict
            description: Address groups that is allowed access by this rule
            suboptions:
              uuid:
                type: str
                description:
                    - Address group uuid.
                    - Mutually exclusive with c(name).
              name:
                description:
                    - Address group name.
                    - Mutually exclusive with c(uuid).
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix_length length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix_length:
                description: prefix length
                type: int

      outbounds:
        description: Array of Outbound Network rule
        type: list
        elements: dict
        suboptions:
          state:
            description:
                - Item's state to delete it
            type: str
            choices:
              - absent
          categories:
            type: dict
            description: A category's key and values
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
            type: dict
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
            suboptions:
              tcp:
                description: List of TCP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              udp:
                description: List of UDP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              icmp:
                description: List of ICMP types and codes allowed by this rule.
                elements: dict
                type: list
                suboptions:
                  code:
                    description: ICMP code
                    type: int
                  type:
                    description: ICMP type
                    type: int
              service:
                type: dict
                description: A service groups associated with this rule.
                suboptions:
                  uuid:
                    type: str
                    description:
                        - Service group uuid.
                        - Mutually exclusive with c(name).
                  name:
                    description:
                        - Service group name.
                        - Mutually exclusive with c(uuid).
                    type: str
          address:
            type: dict
            description: Address groups that is allowed access by this rule
            suboptions:
              uuid:
                type: str
                description:
                    - Address group uuid.
                    - Mutually exclusive with c(name).
              name:
                description:
                    - Address group name.
                    - Mutually exclusive with c(uuid).
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix_length length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix_length:
                description: prefix length
                type: int
  app_rule:
    description: >-
      These rules are used for quarantining suspected VMs. Target group is a
      required attribute. Empty inbounds will not allow anything into
      target group. Empty outbounds will allow everything from target
      group.
    type: dict
    suboptions:
      policy_mode:
        description: Type of deployment of the rule.
        type: str
        choices:
          - MONITOR
          - APPLY
      target_group:
        description: Target Group
        type: dict
        suboptions:
          default_internal_policy:
            description: Default policy for communication within target group.
            type: str
            choices: ["ALLOW_ALL", "DENY_ALL"]
          categories:
            type: dict
            description: A category's key and values
            suboptions:
              apptype:
                description: A category value.
                type: str
              apptype_filter_by_category:
                description: A category key and value.
                type: dict
              apptiers:
                description:
                  - List of AppTier category values
                  - C(apptier) is deprecated
                type: list
                elements: str
              adgroup:
                description:
                    - A category value.
                    - Mutually exclusive with c(apptype).
                type: str
      allow_all_inbounds:
            description: Allow all inbounds
            type: bool
      allow_all_outbounds:
            description: Allow all outbounds
            type: bool
      inbounds:
        description: Array of inbound Network rule
        type: list
        elements: dict
        suboptions:
          state:
            description:
                - Item's state to delete it
            type: str
            choices:
              - absent
          categories:
            type: dict
            description: A category's key and values
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
            type: dict
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
            suboptions:
              tcp:
                description: List of TCP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              udp:
                description: List of UDP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              icmp:
                description: List of ICMP types and codes allowed by this rule.
                elements: dict
                type: list
                suboptions:
                  code:
                    description: ICMP code
                    type: int
                  type:
                    description: ICMP type
                    type: int
              service:
                type: dict
                description: A service groups associated with this rule.
                suboptions:
                  uuid:
                    type: str
                    description:
                        - Service group uuid.
                        - Mutually exclusive with c(name).
                  name:
                    description:
                        - Service group name.
                        - Mutually exclusive with c(uuid).
                    type: str
          address:
            type: dict
            description: Address groups that is allowed access by this rule
            suboptions:
              uuid:
                type: str
                description:
                    - Address group uuid.
                    - Mutually exclusive with c(name).
              name:
                description:
                    - Address group name.
                    - Mutually exclusive with c(uuid).
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix_length length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix_length:
                description: prefix length
                type: int

      outbounds:
        description: Array of Outbound Network rule
        type: list
        elements: dict
        suboptions:
          state:
            description:
                - Item's state to delete it
            type: str
            choices:
              - absent
          categories:
            type: dict
            description: A category's key and values
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
            type: dict
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
            suboptions:
              tcp:
                description: List of TCP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              udp:
                description: List of UDP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              icmp:
                description: List of ICMP types and codes allowed by this rule.
                elements: dict
                type: list
                suboptions:
                  code:
                    description: ICMP code
                    type: int
                  type:
                    description: ICMP type
                    type: int
              service:
                type: dict
                description: A service groups associated with this rule.
                suboptions:
                  uuid:
                    type: str
                    description:
                        - Service group uuid.
                        - Mutually exclusive with c(name).
                  name:
                    description:
                        - Service group name.
                        - Mutually exclusive with c(uuid).
                    type: str
          address:
            type: dict
            description: Address groups that is allowed access by this rule
            suboptions:
              uuid:
                type: str
                description:
                    - Address group uuid.
                    - Mutually exclusive with c(name).
              name:
                description:
                    - Address group name.
                    - Mutually exclusive with c(uuid).
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix_length length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix_length:
                description: prefix length
                type: int
  quarantine_rule:
    description: >-
      These rules are used for quarantining suspected VMs. Target group is a
      required attribute. Empty inbounds will not allow anything into
      target group. Empty outbounds will allow everything from target
      group.
    type: dict
    suboptions:
      policy_mode:
        description: Type of deployment of the rule.
        type: str
        choices:
          - MONITOR
          - APPLY
      target_group:
        description: Target Group
        type: dict
        suboptions:
          default_internal_policy:
            description: Default policy for communication within target group.
            type: str
            choices: ["ALLOW_ALL", "DENY_ALL"]
          categories:
            type: dict
            description: A category's key and values
            suboptions:
              apptype:
                description: A category value.
                type: str
              apptype_filter_by_category:
                description: A category key and value.
                type: dict
              apptiers:
                description:
                  - List of AppTier category values
                  - C(apptier) is deprecated
                type: list
                elements: str
              adgroup:
                description:
                    - A category value.
                    - Mutually exclusive with c(apptype).
                type: str
      allow_all_inbounds:
            description: Allow all inbounds
            type: bool
      allow_all_outbounds:
            description: Allow all outbounds
            type: bool
      inbounds:
        description: Array of inbound Network rule
        type: list
        elements: dict
        suboptions:
          state:
            description:
                - Item's state to delete it
            type: str
            choices:
              - absent
          categories:
            type: dict
            description: A category's key and values
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
            type: dict
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
            suboptions:
              tcp:
                description: List of TCP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              udp:
                description: List of UDP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              icmp:
                description: List of ICMP types and codes allowed by this rule.
                elements: dict
                type: list
                suboptions:
                  code:
                    description: ICMP code
                    type: int
                  type:
                    description: ICMP type
                    type: int
              service:
                type: dict
                description: A service groups associated with this rule.
                suboptions:
                  uuid:
                    type: str
                    description:
                        - Service group uuid.
                        - Mutually exclusive with c(name).
                  name:
                    description:
                        - Service group name.
                        - Mutually exclusive with c(uuid).
                    type: str
          address:
            type: dict
            description: Address groups that is allowed access by this rule
            suboptions:
              uuid:
                type: str
                description:
                    - Address group uuid.
                    - Mutually exclusive with c(name).
              name:
                description:
                    - Address group name.
                    - Mutually exclusive with c(uuid).
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix_length length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix_length:
                description: prefix length
                type: int
      outbounds:
        description: Array of Outbound Network rule
        type: list
        elements: dict
        suboptions:
          state:
            description:
                - Item's state to delete it
            type: str
            choices:
              - absent
          categories:
            type: dict
            description: A category's key and values
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
            type: dict
            description: >-
              Select a protocol to allow. Multiple protocols can be allowed by
              repeating network_rule object. If a protocol is not configured in
              the network_rule object then it is allowed.
            suboptions:
              tcp:
                description: List of TCP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              udp:
                description: List of UDP ports that are allowed by this rule.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description: start_port
                    type: int
                  end_port:
                    description: end_port
                    type: int
              icmp:
                description: List of ICMP types and codes allowed by this rule.
                elements: dict
                type: list
                suboptions:
                  code:
                    description: ICMP code
                    type: int
                  type:
                    description: ICMP type
                    type: int
              service:
                type: dict
                description: A service groups associated with this rule.
                suboptions:
                  uuid:
                    type: str
                    description:
                        - Service group uuid.
                        - Mutually exclusive with c(name).
                  name:
                    description:
                        - Service group name.
                        - Mutually exclusive with c(uuid).
                    type: str
          address:
            type: dict
            description: Address groups that is allowed access by this rule
            suboptions:
              uuid:
                type: str
                description:
                    - Address group uuid.
                    - Mutually exclusive with c(name).
              name:
                description:
                    - Address group name.
                    - Mutually exclusive with c(uuid).
                type: str
          ip_subnet:
            description: IP subnet provided as an address and prefix_length length.
            type: dict
            suboptions:
              ip:
                type: str
                description: IPV4 address.
              prefix_length:
                description: prefix length
                type: int

  isolation_rule:
    description: These rules are used for environmental isolation.
    type: dict
    suboptions:
      policy_mode:
        description: Type of deployment of the rule.
        type: str
        choices:
          - MONITOR
          - APPLY
      isolate_category:
        description:
            - A category key and value.
            - Need to provide only one.
        type: dict
      from_category:
        description:
            - A category key and value.
            - Need to provide only one.
        type: dict
      subset_category:
        type: dict
        description:
            - A category key and value.
            - Need to provide only one.
author:
  - Prem Karat (@premkarat)
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: create app security rule
  ntnx_security_rules:
    name: test_app_rule
    allow_ipv6_traffic: true
    policy_hitlog: true
    app_rule:
      policy_mode: MONITOR
      target_group:
        categories:
            apptype: Apache_Spark
        default_internal_policy: DENY_ALL
      inbounds:
        - categories:
              AppFamily:
                - Databases
                - DevOps
          protocol:
            icmp:
              - code: 1
                type: 1
        - categories:
              AppFamily:
                - Databases
                - DevOps
          protocol:
            tcp:
              - start_port: 22
                end_port: 80
        - categories:
              AppFamily:
                - Databases
                - DevOps
          protocol:
            udp:
              - start_port: 82
                end_port: 8080
          description: test description
        - ip_subnet:
            ip: 192.168.1.0
            prefix_length: 24
      outbounds:
        - categories:
              AppFamily:
                - Databases
  register: result
- name: update app security rule with outbound list
  ntnx_security_rules:
    security_rule_uuid: '{{ result.response.metadata.uuid }}'
    app_rule:
      policy_mode: APPLY
      outbound:
        - icmp:
            - code: 1
              type: 1
          categories:
              AppFamily:
                - Databases
                - DevOps
  register: result
- name: update quarantine_rule by adding inbound and outbound list
  ntnx_security_rules:
    security_rule_uuid: '{{quarantine_rule_uuid}}'
    quarantine_rule:
      inbound:
        - categories:
              AppFamily:
                - Databases
                - DevOps
      outbound:
        - categories:
              AppFamily:
                - Databases
                - DevOps
      policy_mode: MONITOR
    allow_ipv6_traffic: true
    policy_hitlog:: true
  register: result
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: '3.1'
metadata:
  description: Metadata for security_rule  output
  returned: always
  type: dict
  sample:
    categories: {}
    categories_mapping: {}
    creation_time: '2022-06-15T11:59:38Z'
    kind: network_security_rule
    last_update_time: '2022-06-15T11:59:41Z'
    owner_reference:
      kind: user
      name: admin
      uuid: 00000000-0000-0000-0000-000000000000
    spec_hash: '00000000000000000000000000000000000000000000000000'
    spec_version: 0
    uuid: c340bc98-170b-4ead-a86c-861b023cc8ff
spec:
  description: An intentful representation of a subnet spec
  returned: always
  type: dict
  sample:
    name: test_app_rule
    resources:
      allow_ipv6_traffic: true
      app_rule:
        action: MONITOR
        inbound_allow_list:
          - description: test description
            filter:
              kind_list:
                - vm
              params:
                AppFamily:
                  - Databases
                  - DevOps
              type: CATEGORIES_MATCH_ALL
            icmp_type_code_list:
              - code: 1
                type: 1
            ip_subnet:
              ip: 192.168.1.1
              prefix_length: 24
            peer_specification_type: FILTER
            protocol: ALL
            rule_id: 1
            tcp_port_range_list:
              - end_port: 80
                start_port: 22
            udp_port_range_list:
              - end_port: 8080
                start_port: 82
        outbound_allow_list:
          - filter:
              kind_list:
                - vm
              params:
                AppFamily:
                  - Databases
                  - DevOps
              type: CATEGORIES_MATCH_ALL
            peer_specification_type: FILTER
            rule_id: 1
        target_group:
          default_internal_policy: DENY_ALL
          filter:
            kind_list:
              - vm
            params:
              AppType:
                - Apache_Spark
            type: CATEGORIES_MATCH_ALL
          peer_specification_type: FILTER
      policy_hitlog:: true
status:
  description: An intentful representation of a subnet status
  returned: always
  type: dict
  sample:
    execution_context:
      task_uuid:
        - ac7ae2c4-acbe-4ab7-b0b3-faca16395429
    name: test_app_rule
    resources:
      allow_ipv6_traffic: true
      app_rule:
        action: MONITOR
        inbound_allow_list:
          - description: test description
            filter:
              kind_list:
                - vm
              params:
                AppFamily:
                  - Databases
                  - DevOps
              type: CATEGORIES_MATCH_ALL
            peer_specification_type: FILTER
            protocol: ALL
            rule_id: 1
        outbound_allow_list:
          - filter:
              kind_list:
                - vm
              params:
                AppFamily:
                  - Databases
                  - DevOps
              type: CATEGORIES_MATCH_ALL
            peer_specification_type: FILTER
            rule_id: 1
        target_group:
          default_internal_policy: DENY_ALL
          filter:
            kind_list:
              - vm
            params:
              AppType:
                - Apache_Spark
            type: CATEGORIES_MATCH_ALL
          peer_specification_type: FILTER
      policy_hitlog:: true
    state: COMPLETE
security_rule_uuid:
  description: The created security rule  uuid
  returned: always
  type: str
  sample: 00000000000-0000-0000-0000-00000000000
task_uuid:
  description: The task uuid for the creation
  returned: always
  type: str
  sample: 00000000000-0000-0000-0000-00000000000
"""


from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.security_rules import SecurityRule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    group_spec = dict(uuid=dict(type="str"), name=dict(type="str"))

    tcp_and_udp_spec = dict(start_port=dict(type="int"), end_port=dict(type="int"))

    network_spec = dict(ip=dict(type="str"), prefix_length=dict(type="int"))

    icmp_spec = dict(code=dict(type="int"), type=dict(type="int"))

    categories_spec = dict(
        apptype=dict(type="str"),
        apptype_filter_by_category=dict(type="dict"),
        apptiers=dict(type="list", elements="str"),
        adgroup=dict(type="str"),
    )

    protocol_spec = dict(
        tcp=dict(type="list", elements="dict", options=tcp_and_udp_spec),
        udp=dict(type="list", elements="dict", options=tcp_and_udp_spec),
        icmp=dict(
            type="list",
            elements="dict",
            options=icmp_spec,
            required_by={"code": "type"},
        ),
        service=dict(type="dict", options=group_spec),
    )

    target_spec = dict(
        categories=dict(
            type="dict",
            options=categories_spec,
            mutually_exclusive=[("apptype", "adgroup")],
        ),
        default_internal_policy=dict(type="str", choices=["ALLOW_ALL", "DENY_ALL"]),
    )

    whitelisted_traffic = dict(
        categories=dict(type="dict"),
        address=dict(type="dict", options=group_spec),
        ip_subnet=dict(type="dict", options=network_spec),
        description=dict(type="str"),
        rule_id=dict(type="int"),
        state=dict(type="str", choices=["absent"]),
        protocol=dict(
            type="dict",
            options=protocol_spec,
            apply_defaults=True,
            mutually_exclusive=[("tcp", "udp", "icmp", "service")],
        ),
    )
    rule_spec = dict(
        target_group=dict(type="dict", options=target_spec),
        inbounds=dict(
            type="list",
            elements="dict",
            options=whitelisted_traffic,
            mutually_exclusive=[("address", "categories", "ip_subnet")],
        ),
        allow_all_inbounds=dict(type="bool"),
        outbounds=dict(
            type="list",
            elements="dict",
            options=whitelisted_traffic,
            mutually_exclusive=[("address", "categories", "ip_subnet")],
        ),
        allow_all_outbounds=dict(type="bool"),
        policy_mode=dict(type="str", choices=["MONITOR", "APPLY"]),
    )

    isolation_rule_spec = dict(
        isolate_category=dict(type="dict"),
        from_category=dict(type="dict"),
        subset_category=dict(type="dict"),
        policy_mode=dict(type="str", choices=["MONITOR", "APPLY"]),
    )
    module_args = dict(
        name=dict(type="str"),
        security_rule_uuid=dict(type="str"),
        allow_ipv6_traffic=dict(type="bool"),
        policy_hitlog=dict(type="bool"),
        vdi_rule=dict(
            type="dict",
            options=rule_spec,
            mutually_exclusive=[
                ("inbounds", "allow_all_inbounds"),
                ("outbounds", "allow_all_outbounds"),
            ],
        ),
        app_rule=dict(
            type="dict",
            options=rule_spec,
            mutually_exclusive=[
                ("inbounds", "allow_all_inbounds"),
                ("outbounds", "allow_all_outbounds"),
            ],
        ),
        isolation_rule=dict(type="dict", options=isolation_rule_spec),
        quarantine_rule=dict(
            type="dict",
            options=rule_spec,
            mutually_exclusive=[
                ("inbounds", "allow_all_inbounds"),
                ("outbounds", "allow_all_outbounds"),
            ],
        ),
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
    utils.strip_extra_attrs(resp["status"], resp["spec"])
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
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ("vdi_rule", "app_rule", "isolation_rule", "quarantine_rule"),
            ("allow_ipv6_traffic", "isolation_rule"),
        ],
        required_by={"quarantine_rule": "security_rule_uuid"},
        required_one_of=[("security_rule_uuid", "name")],
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
