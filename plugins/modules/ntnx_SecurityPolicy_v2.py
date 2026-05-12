#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_SecurityPolicy_v2
short_description: Manage network security policies in Nutanix Prism Central
version_added: "2.6.0"
description:
  - This module allows you to create, update, and delete network security policies in Nutanix Prism Central.
  - During update, the rules provided under C(rules) will replace existing rules.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Network Security Policy) -
      Operation Name: Create Flow Policy -
      Required Roles: Flow Admin, Prism Admin, Super Admin
    - >-
      B(Delete a Network Security Policy by ExtID) -
      Operation Name: Delete Flow Policy -
      Required Roles: Flow Admin, Prism Admin, Super Admin
    - >-
      B(Update a Network Security Policy by ExtID) -
      Operation Name: Update Flow Policy -
      Required Roles: Flow Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=microseg)"
options:
  wait:
    description:
      - Wait for the task to complete.
    type: bool
    default: true
  state:
    description:
      - The state of the network security policy.
      - If C(present) and C(ext_id) is not provided, the network security policy will be created.
      - If C(present) and C(ext_id) is provided, the network security policy will be updated.
      - If C(absent) and C(ext_id) is provided, the network security policy will be deleted.
    type: str
  ext_id:
    description:
      - External ID of the Flow Network Security Policy.
    type: str
  name:
    description:
      - Name of the Flow Network Security Policy.
    required: false
    type: str
  is_ipv6_traffic_allowed:
    description:
      - If Ipv6 Traffic needs to be allowed.
    type: bool
  is_hitlog_enabled:
    description:
      - If Hitlog needs to be enabled.
    type: bool
  description:
    description:
      - Description of policy
    required: false
    type: str
  vpc_references:
    description:
      - A list of external ids for VPCs, used only when the scope of policy is a list of VPCs.
    required: false
    type: list
    elements: str
  scope_references:
    description:
      - A list of external ids for scope references, used only when the scope of policy is a list of scope references.
    required: false
    type: list
    elements: str
  type:
    description:
      - Defines the type of rules that can be used in a policy.
    required: false
    type: str
    choices:
      - QUARANTINE
      - ISOLATION
      - APPLICATION
      - SHAREDSERVICE
  policy_state:
    description:
      - Whether the policy is just to be saved, applied, monitored.
    required: false
    type: str
    choices:
      - SAVE
      - MONITOR
      - ENFORCE
  scope:
    description:
      - Defines the scope of the policy. Currently, ALL_VLAN, VPC_LIST, GLOBAL, and VPC_AS_CATEGORY are supported.
        If a scope is not provided, the default value is determined by the presence or absence of
        the vpcReferences or scopeReferences fields.
    required: false
    type: str
    choices:
      - ALL_VLAN
      - ALL_VPC
      - VPC_LIST
      - GLOBAL
      - VPC_AS_CATEGORY
  rules:
    description:
      - A list of rules that form a policy. For isolation policies, use isolation rules.
      - For application or quarantine policies, use application rules.
    required: false
    type: list
    elements: dict
    suboptions:
      ext_id:
        description:
          - External ID of the rule.
        required: false
        type: str
      description:
        description:
          - Description of rule
        required: false
        type: str
      type:
        description:
          - The type for a rule - the value chosen here restricts which specification can be chosen.
        type: str
        choices:
          - QUARANTINE
          - TWO_ENV_ISOLATION
          - APPLICATION
          - INTRA_GROUP
          - MULTI_ENV_ISOLATION
          - SHARED_SERVICE
      spec:
        description:
          - The specification of the rule.
        type: dict
        suboptions:
          two_env_isolation_rule_spec:
            description:
              - The specification of the two environment isolation rule.
            required: false
            type: dict
            suboptions:
              first_isolation_group:
                description:
                  - Denotes the first group of category uuids that will be used in an isolation policy.
                type: list
                elements: str
              second_isolation_group:
                description:
                  - Denotes the second group of category uuids that will be used in an isolation policy.
                type: list
                elements: str
          application_rule_spec:
            description:
              - The specification of the application rule.
              - This can be used for application or quarantine policies.
            required: false
            type: dict
            suboptions:
              secured_group_category_references:
                description:
                  - A set of categories of vms which is protected by a Network Security Policy and defined as a list of categories.
                type: list
                elements: str
              secured_group_entity_group_reference:
                description:
                  - A reference to the secured group entity group.
                type: str
              src_allow_spec:
                description:
                  - A specification to how allow mode traffic should be applied, either ALL or NONE.
                type: str
                choices:
                  - ALL
                  - NONE
              dest_allow_spec:
                description:
                  - A specification to how allow mode traffic should be applied, either ALL or NONE.
                type: str
                choices:
                  - ALL
                  - NONE
              src_category_references:
                description:
                  - List of categories that define a set of network endpoints as inbound.
                type: list
                elements: str
              dest_category_references:
                description:
                  - List of categories that define a set of network endpoints as outbound.
                type: list
                elements: str
              dest_entity_group_reference:
                description:
                  - A reference to the destination entity group.
                type: str
              secured_group_category_associated_entity_type:
                description:
                  - The type of entity associated with the secured group category.
                  - Will have value only if secured_group_category_references is provided.
                type: str
                choices:
                  - VM
                  - SUBNET
                  - VPC
                default: VM
                required: false
              src_category_associated_entity_type:
                description:
                  - The type of entity associated with the source category.
                  - Will have value only if src_category_references is provided.
                type: str
                choices:
                  - VM
                  - SUBNET
                  - VPC
                default: VM
                required: false
              src_entity_group_reference:
                description:
                  - A reference to the source entity group.
                type: str
              dest_category_associated_entity_type:
                description:
                  - The type of entity associated with the destination category.
                  - Will have value only if dest_category_references is provided.
                type: str
                choices:
                  - VM
                  - SUBNET
                  - VPC
                default: VM
                required: false
              src_subnet:
                description:
                  - The source subnet/IP specification.
                type: dict
                suboptions:
                  value:
                    description:
                      - The value of the source subnet.
                    type: str
                  prefix_length:
                    description:
                      - The prefix length of the source subnet.
                    type: int
              dest_subnet:
                description:
                  - The destination subnet/IP specification.
                type: dict
                suboptions:
                  value:
                    description:
                      - The value of the destination subnet.
                    type: str
                  prefix_length:
                    description:
                      - The prefix length of the destination subnet.
                    type: int
              src_address_group_references:
                description:
                  - A list of address group references.
                type: list
                elements: str
              dest_address_group_references:
                description:
                  - A list of address group references.
                type: list
                elements: str
              service_group_references:
                description:
                  - The list of service group references.
                type: list
                elements: str
              is_all_protocol_allowed:
                description:
                  - Denotes whether the rule allows traffic for all protocols.
                  - If set to true, the rule allows traffic for all protocols.
                  - If set to false or not specified, specifying at least one protocol service or service group is mandatory.
                type: bool
              tcp_services:
                description:
                  - The list of TCP services.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description:
                      - The start port of the TCP service.
                    type: int
                  end_port:
                    description:
                      - The end port of the TCP service.
                    type: int
              udp_services:
                description:
                  - The list of UDP services.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description:
                      - The start port of the UDP service.
                    type: int
                  end_port:
                    description:
                      - The end port of the UDP service.
                    type: int
              icmp_services:
                description:
                  - Icmp Type Code List.
                type: list
                elements: dict
                suboptions:
                  is_all_allowed:
                    description:
                      - Icmp service All Allowed.
                    type: bool
                  type:
                    description:
                      - Icmp service Type. Ignore this field if Type has to be ANY.
                    type: int
                  code:
                    description:
                      - Icmp service Code. Ignore this field if Code has to be ANY.
                    type: int
              network_function_chain_reference:
                description:
                  - A reference to the network function chain in the rule.
                type: str
              network_function_reference:
                description:
                  - A reference to the network function in the rule.
                type: str
          intra_entity_group_rule_spec:
            description:
              - The specification of the intra entity group rule.
            required: false
            type: dict
            suboptions:
              secured_group_category_references:
                description:
                  - The list of secured group category references.
                type: list
                elements: str
              secured_group_action:
                description:
                  - A specification to whether traffic between intra secured group entities should be allowed or denied.
                type: str
                choices:
                  - ALLOW
                  - DENY
                required: true
              secured_group_category_associated_entity_type:
                description:
                  - The type of entity associated with the secured group category.
                  - Will have value only if secured_group_category_references is provided.
                type: str
                choices:
                  - VM
                  - SUBNET
                  - VPC
                default: VM
                required: false
              secured_group_entity_group_reference:
                description:
                  - The reference to the secured group entity group.
                type: str
                required: false
              secured_group_service_references:
                description:
                  - The list of secured group service references.
                type: list
                elements: str
                required: false
              tcp_services:
                description:
                  - The list of TCP services.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description:
                      - The start port of the TCP service.
                    type: int
                  end_port:
                    description:
                      - The end port of the TCP service.
                    type: int
              udp_services:
                description:
                  - The list of UDP services.
                type: list
                elements: dict
                suboptions:
                  start_port:
                    description:
                      - The start port of the UDP service.
                    type: int
                  end_port:
                    description:
                      - The end port of the UDP service.
                    type: int
              icmp_services:
                description:
                  - Icmp Type Code List.
                type: list
                elements: dict
                suboptions:
                  is_all_allowed:
                    description:
                      - Icmp service All Allowed.
                    type: bool
                  type:
                    description:
                      - Icmp service Type. Ignore this field if Type has to be ANY.
                    type: int
                  code:
                    description:
                      - Icmp service Code. Ignore this field if Code has to be ANY.
                    type: int
          multi_env_isolation_rule_spec:
            description:
              - The specification of the multi environment isolation rule.
            required: false
            type: dict
            suboptions:
              spec:
                description:
                  - The specification of the multi environment isolation rule.
                type: dict
                suboptions:
                  all_to_all_isolation_group:
                    description:
                      - The specification of the all to all isolation group.
                    type: dict
                    suboptions:
                      isolation_groups:
                        description:
                          - The list of isolation groups.
                        type: list
                        elements: dict
                        required: true
                        suboptions:
                          group_category_associated_entity_type:
                            description:
                              - The type of entity associated with the group category.
                            type: str
                            choices:
                              - VM
                              - SUBNET
                              - VPC
                            default: VM
                          group_category_references:
                            description:
                              - The list of group category references.
                            type: list
                            elements: str
                          group_entity_group_reference:
                            description:
                              - The reference to the group entity group.
                            type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)

"""

EXAMPLES = r"""
- name: Create an application security policy with ALL_VLAN scope
  nutanix.ncp.ntnx_SecurityPolicy_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    name: "app-security-policy"
    description: "Ansible created security policy"
    type: "APPLICATION"
    policy_state: "MONITOR"
    scope: "ALL_VLAN"
    is_hitlog_enabled: true
    is_ipv6_traffic_allowed: false
    rules:
      - description: "Intra group rule"
        type: "INTRA_GROUP"
        spec:
          intra_entity_group_rule_spec:
            secured_group_category_references:
              - "f83d766b-f3e8-42f0-a32f-24983848d032"
            secured_group_action: "DENY"
      - description: "Inbound application rule"
        type: "APPLICATION"
        spec:
          application_rule_spec:
            secured_group_category_references:
              - "f83d766b-f3e8-42f0-a32f-24983848d032"
            src_category_references:
              - "f83d766b-f3e8-42f0-a32f-24983848d035"
            is_all_protocol_allowed: true
  register: result

- name: Update a security policy
  nutanix.ncp.ntnx_SecurityPolicy_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    ext_id: "{{ result.ext_id }}"
    name: "app-security-policy-updated"
    policy_state: "ENFORCE"
  register: result

- name: Delete a security policy
  nutanix.ncp.ntnx_SecurityPolicy_v2:
    nutanix_host: "<pc_ip>"
    nutanix_username: "<pc_username>"
    nutanix_password: "<pc_password>"
    state: absent
    ext_id: "{{ result.ext_id }}"
  register: result
"""


RETURN = r"""
response:
  description:
    - If C(wait) is set to C(true), the response will contain the security policy details.
    - If C(wait) is set to C(false), the response will contain the task details.
    - For delete operation, the response will contain the task details.
  returned: always
  type: dict
  sample: {
            "created_by": "00000000-0000-0000-0000-000000000000",
            "creation_time": "2024-07-19T12:55:54.945000+00:00",
            "description": "Ansible created policy",
            "ext_id": "e8347a03-28a0-4eaa-9f43-64fd74cdee9e",
            "is_hitlog_enabled": false,
            "is_ipv6_traffic_allowed": false,
            "is_system_defined": false,
            "last_update_time": "2024-07-19T12:56:21.167000+00:00",
            "links": null,
            "name": "ansible-policy-1",
            "rules": [],
            "scope": "ALL_VLAN",
            "secured_groups": null,
            "state": "MONITOR",
            "tenant_id": null,
            "type": "APPLICATION",
            "vpc_references": null
        }
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating network security policy"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false
skipped:
  description: Flag is module operation is skipped due to no state changes
  returned: always
  type: bool
  sample: false
ext_id:
  description: The created security policy ext_id
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
task_ext_id:
  description: The task ext_id for the operation
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_etag,
    get_network_security_policy_api_instance,
)
from ..module_utils.v4.flow.helpers import get_network_security_policy  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_microseg_py_client as mic_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as mic_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    rule_spec_obj_map = {
        "two_env_isolation_rule_spec": mic_sdk.TwoEnvIsolationRuleSpec,
        "application_rule_spec": mic_sdk.ApplicationRuleSpec,
        "intra_entity_group_rule_spec": mic_sdk.IntraEntityGroupRuleSpec,
        "multi_env_isolation_rule_spec": mic_sdk.MultiEnvIsolationRuleSpec,
    }
    multi_env_isolation_rule_spec_obj_map = {
        "all_to_all_isolation_group": mic_sdk.AllToAllIsolationGroup,
    }

    icmp_service_spec = dict(
        is_all_allowed=dict(type="bool"),
        type=dict(type="int"),
        code=dict(type="int"),
    )

    range_spec = dict(
        start_port=dict(type="int"),
        end_port=dict(type="int"),
    )

    ip_address_sub_spec = dict(
        value=dict(type="str"),
        prefix_length=dict(type="int"),
    )

    isolation_rule_spec = dict(
        first_isolation_group=dict(type="list", elements="str"),
        second_isolation_group=dict(type="list", elements="str"),
    )
    application_rule_spec = dict(
        secured_group_category_references=dict(type="list", elements="str"),
        secured_group_entity_group_reference=dict(type="str"),
        secured_group_category_associated_entity_type=dict(
            type="str", choices=["VM", "SUBNET", "VPC"], default="VM"
        ),
        src_category_associated_entity_type=dict(
            type="str", choices=["VM", "SUBNET", "VPC"], default="VM"
        ),
        src_entity_group_reference=dict(type="str"),
        dest_category_associated_entity_type=dict(
            type="str", choices=["VM", "SUBNET", "VPC"], default="VM"
        ),
        src_allow_spec=dict(type="str", choices=["ALL", "NONE"]),
        dest_allow_spec=dict(type="str", choices=["ALL", "NONE"]),
        src_category_references=dict(type="list", elements="str"),
        dest_category_references=dict(type="list", elements="str"),
        dest_entity_group_reference=dict(type="str"),
        src_subnet=dict(
            type="dict", options=ip_address_sub_spec, obj=mic_sdk.IPv4Address
        ),
        dest_subnet=dict(
            type="dict", options=ip_address_sub_spec, obj=mic_sdk.IPv4Address
        ),
        src_address_group_references=dict(type="list", elements="str"),
        dest_address_group_references=dict(type="list", elements="str"),
        service_group_references=dict(type="list", elements="str"),
        is_all_protocol_allowed=dict(type="bool"),
        tcp_services=dict(
            type="list",
            elements="dict",
            options=range_spec,
            obj=mic_sdk.TcpPortRangeSpec,
        ),
        udp_services=dict(
            type="list",
            elements="dict",
            options=range_spec,
            obj=mic_sdk.UdpPortRangeSpec,
        ),
        icmp_services=dict(
            type="list",
            elements="dict",
            options=icmp_service_spec,
            obj=mic_sdk.IcmpTypeCodeSpec,
        ),
        network_function_chain_reference=dict(type="str"),
        network_function_reference=dict(type="str"),
    )
    entity_group_rule_spec = dict(
        secured_group_category_references=dict(type="list", elements="str"),
        secured_group_action=dict(type="str", choices=["ALLOW", "DENY"], required=True),
        secured_group_category_associated_entity_type=dict(
            type="str", choices=["VM", "SUBNET", "VPC"], default="VM"
        ),
        secured_group_entity_group_reference=dict(type="str"),
        secured_group_service_references=dict(type="list", elements="str"),
        tcp_services=dict(
            type="list",
            elements="dict",
            options=range_spec,
            obj=mic_sdk.TcpPortRangeSpec,
        ),
        udp_services=dict(
            type="list",
            elements="dict",
            options=range_spec,
            obj=mic_sdk.UdpPortRangeSpec,
        ),
        icmp_services=dict(
            type="list",
            elements="dict",
            options=icmp_service_spec,
            obj=mic_sdk.IcmpTypeCodeSpec,
        ),
    )

    isolation_groups_spec = dict(
        group_category_references=dict(type="list", elements="str"),
        group_category_associated_entity_type=dict(
            type="str", choices=["VM", "SUBNET", "VPC"], default="VM"
        ),
        group_entity_group_reference=dict(type="str"),
    )

    all_to_all_spec = dict(
        isolation_groups=dict(
            type="list",
            elements="dict",
            obj=mic_sdk.IsolationGroup,
            options=isolation_groups_spec,
            required=True,
        )
    )

    all_to_all_isolation_group_spec = dict(
        all_to_all_isolation_group=dict(
            type="dict",
            obj=mic_sdk.AllToAllIsolationGroup,
            options=all_to_all_spec,
        )
    )

    multi_env_isolation_rule_spec = dict(
        spec=dict(
            type="dict",
            options=all_to_all_isolation_group_spec,
            obj=multi_env_isolation_rule_spec_obj_map,
        )
    )

    rule_spec = dict(
        two_env_isolation_rule_spec=dict(type="dict", options=isolation_rule_spec),
        application_rule_spec=dict(type="dict", options=application_rule_spec),
        intra_entity_group_rule_spec=dict(type="dict", options=entity_group_rule_spec),
        multi_env_isolation_rule_spec=dict(
            type="dict", options=multi_env_isolation_rule_spec
        ),
    )

    policy_rule = dict(
        ext_id=dict(type="str"),
        description=dict(type="str"),
        type=dict(
            type="str",
            choices=[
                "QUARANTINE",
                "TWO_ENV_ISOLATION",
                "APPLICATION",
                "INTRA_GROUP",
                "MULTI_ENV_ISOLATION",
                "SHARED_SERVICE",
            ],
        ),
        spec=dict(
            type="dict",
            options=rule_spec,
            obj=rule_spec_obj_map,
            mutually_exclusive=[
                (
                    "two_env_isolation_rule_spec",
                    "application_rule_spec",
                    "intra_entity_group_rule_spec",
                    "multi_env_isolation_rule_spec",
                )
            ],
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        type=dict(
            type="str",
            choices=["QUARANTINE", "ISOLATION", "APPLICATION", "SHAREDSERVICE"],
        ),
        policy_state=dict(type="str", choices=["SAVE", "MONITOR", "ENFORCE"]),
        rules=dict(
            type="list",
            elements="dict",
            options=policy_rule,
            obj=mic_sdk.NetworkSecurityPolicyRule,
        ),
        scope=dict(
            type="str",
            choices=["ALL_VLAN", "ALL_VPC", "VPC_LIST", "GLOBAL", "VPC_AS_CATEGORY"],
        ),
        vpc_references=dict(type="list", elements="str"),
        scope_references=dict(type="list", elements="str"),
        is_ipv6_traffic_allowed=dict(type="bool"),
        is_hitlog_enabled=dict(type="bool"),
    )

    return module_args


def create_security_policy(module, api_instance, result):
    """Create a new network security policy."""
    sg = SpecGenerator(module)
    default_spec = mic_sdk.NetworkSecurityPolicy()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create network security policy spec", **result
        )

    if module.params.get("policy_state"):
        spec.state = module.params.get("policy_state")

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_network_security_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating network security policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.SECURITY_POLICY
        )
        if ext_id:
            resp = get_network_security_policy(module, api_instance, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_security_policy_idempotency(old_spec, update_spec):
    """Check if the update spec is same as the current spec."""
    if len(old_spec.get("rules", [])) != len(update_spec.get("rules", [])):
        return False

    for rule in old_spec.get("rules", []):
        rule["ext_id"] = None

    for rule in update_spec.get("rules", []):
        rule["ext_id"] = None
        spec = rule.get("spec", {})
        if (
            "src_category_references" in spec
            and spec["src_category_references"] is None
        ):
            spec["src_category_associated_entity_type"] = None
        if (
            "dest_category_references" in spec
            and spec["dest_category_references"] is None
        ):
            spec["dest_category_associated_entity_type"] = None
        if (
            "secured_group_category_references" in spec
            and spec["secured_group_category_references"] is None
        ):
            spec["secured_group_category_associated_entity_type"] = None

    old_rules = old_spec.pop("rules")
    update_rules = update_spec.pop("rules")

    for rule in update_rules:
        if rule not in old_rules:
            return False

    if old_spec != update_spec:
        return False
    return True


def update_security_policy(module, api_instance, result):
    """Update an existing network security policy."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_network_security_policy(module, api_instance, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating network security policy update spec", **result
        )

    if module.params.get("policy_state"):
        update_spec.state = module.params.get("policy_state")
    else:
        update_spec.state = current_spec.state

    current_spec_dict = strip_internal_attributes(current_spec.to_dict())
    update_spec_dict = strip_internal_attributes(update_spec.to_dict())
    if check_security_policy_idempotency(current_spec_dict, update_spec_dict):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    etag = get_etag(data=current_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.update_network_security_policy_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating network security policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_network_security_policy(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_security_policy(module, api_instance, result):
    """Delete an existing network security policy."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Network security policy with ext_id:{0} will be deleted.".format(ext_id)
        )
        return

    current_spec = get_network_security_policy(module, api_instance, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting network security policy", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = api_instance.delete_network_security_policy_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting network security policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_microseg_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }

    api_instance = get_network_security_policy_api_instance(module)

    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_security_policy(module, api_instance, result)
        else:
            create_security_policy(module, api_instance, result)
    else:
        delete_security_policy(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
