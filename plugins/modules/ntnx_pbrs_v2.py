#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_pbrs_v2
short_description: Module for create, update and delete of Policy based routing.
version_added: 2.0.0
description:
  - Create, Update, Delete Routing Policies
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - if C(state) is present, it will create or update the routing policy.
      - If C(state) is set to C(present) and ext_id is not provided then the operation will be create the routing policy
      - If C(state) is set to C(present) and ext_id is provided then the operation will be update the routing policy
      - If C(state) is set to C(absent) and ext_id is provided , then operation will be delete the routing policy
    type: str
    choices: ['present', 'absent']
  wait:
    description:
      - Wait for the task to complete
    type: bool
    default: true
  description:
    description: A description of the routing policy.
    type: str
  ext_id:
    description:
      - external ID of the routing policy.
      - Required for updating or deleting the routing policy.
    type: str
  metadata:
    description: Metadata associated with this resource.
    suboptions:
      category_ids:
        description: A list of globally unique identifiers that represent all the categories the resource is associated with.
        elements: str
        type: list
      owner_reference_id:
        description: A globally unique identifier that represents the owner of this resource.
        type: str
      project_reference_id:
        description: A globally unique identifier that represents the project this resource belongs to.
        type: str
    type: dict
  name:
    description: Name of the routing policy.
    type: str
  policies:
    description: List of routing policy rules.
    elements: dict
    suboptions:
      is_bidirectional:
        description: If True, policies in the reverse direction will be installed with the same action but source and destination will be swapped.
        type: bool
      policy_action:
        description: The action to be taken on the traffic matching the routing policy.
        type: dict
        suboptions:
          action_type:
            description: Routing policy action type.
            choices:
              - PERMIT
              - DENY
              - REROUTE
              - FORWARD
            type: str
          reroute_params:
            description: Parameters for rerouting action.
            elements: dict
            type: list
            suboptions:
                reroute_fallback_action:
                  description: Type of fallback action in reroute case when service VM is down.
                  choices:
                    - ALLOW
                    - DROP
                    - PASSTHROUGH
                    - NO_ACTION
                  type: str
                service_ip:
                  description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                  type: dict
                  suboptions:
                    ipv4:
                      description: IPv4 subnet specification.
                      type: dict
                      suboptions:
                            prefix_length:
                              description: Prefix length.
                              type: int
                            value:
                              description: IP address value.
                              type: str
                    ipv6:
                      description: IPv6 subnet specification.
                      type: dict
                      suboptions:
                            prefix_length:
                              description: Prefix length.
                              type: int
                            value:
                              description: IP address value.
                              type: str
                ingress_service_ip:
                  description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                  type: dict
                  suboptions:
                    ipv4:
                      description: IPv4 subnet specification.
                      type: dict
                      suboptions:
                            prefix_length:
                              description: Prefix length.
                              type: int
                            value:
                              description: IP address value.
                              type: str
                    ipv6:
                      description: IPv6 subnet specification.
                      type: dict
                      suboptions:
                            prefix_length:
                              description: Prefix length.
                              type: int
                            value:
                              description: IP address value.
                              type: str
                egress_service_ip:
                  description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                  type: dict
                  suboptions:
                    ipv4:
                      description: IPv4 subnet specification.
                      type: dict
                      suboptions:
                            prefix_length:
                              description: Prefix length.
                              type: int
                            value:
                              description: IP address value.
                              type: str
                    ipv6:
                      description: IPv6 subnet specification.
                      type: dict
                      suboptions:
                            prefix_length:
                              description: Prefix length.
                              type: int
                            value:
                              description: IP address value.
                              type: str
          nexthop_ip_address:
            description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
            type: dict
            suboptions:
              ipv4:
                description: IPv4 subnet specification.
                type: dict
                suboptions:
                      prefix_length:
                        description: Prefix length.
                        type: int
                      value:
                        description: IP address value.
                        type: str
              ipv6:
                description: IPv6 subnet specification.
                type: dict
                suboptions:
                      prefix_length:
                        description: Prefix length.
                        type: int
                      value:
                        description: IP address value.
                        type: str

      policy_match:
        description: Match condition for the traffic that is entering the VPC.
        type: dict
        suboptions:
          source:
            description: Address Type like "EXTERNAL" or "ANY".
            type: dict
            suboptions:
              address_type:
                description: Address type.
                choices:
                  - ANY
                  - EXTERNAL
                  - SUBNET
                type: str
              subnet_prefix:
                description: Subnet prefix specification.
                type: dict
                suboptions:
                  ipv4:
                    description: IPv4 subnet specification.
                    type: dict
                    suboptions:
                      ip:
                        description: IPv4 address specification.
                        type: dict
                        suboptions:
                          prefix_length:
                            description: Prefix length.
                            type: int
                          value:
                            description: IP address value.
                            type: str
                      prefix_length:
                        description: Prefix length.
                        type: int
                  ipv6:
                    description: IPv6 subnet specification.
                    type: dict
                    suboptions:
                      ip:
                        description: IPv6 address specification.
                        type: dict
                        suboptions:
                          prefix_length:
                            description: Prefix length.
                            type: int
                          value:
                            description: IP address value.
                            type: str
                      prefix_length:
                        description: Prefix length.
                        type: int
          destination:
            description: Address Type like "EXTERNAL" or "ANY".
            type: dict
            suboptions:
              address_type:
                description: Address type.
                choices:
                  - ANY
                  - EXTERNAL
                  - SUBNET
                type: str
              subnet_prefix:
                description: Subnet prefix specification.
                type: dict
                suboptions:
                  ipv4:
                    description: IPv4 subnet specification.
                    type: dict
                    suboptions:
                      ip:
                        description: IPv4 address specification.
                        type: dict
                        suboptions:
                          prefix_length:
                            description: Prefix length.
                            type: int
                          value:
                            description: IP address value.
                            type: str
                      prefix_length:
                        description: Prefix length.
                        type: int
                  ipv6:
                    description: IPv6 subnet specification.
                    type: dict
                    suboptions:
                      ip:
                        description: IPv6 address specification.
                        type: dict
                        suboptions:
                          prefix_length:
                            description: Prefix length.
                            type: int
                          value:
                            description: IP address value.
                            type: str
                      prefix_length:
                        description: Prefix length.
                        type: int
          protocol_parameters:
            description: Protocol parameters.
            type: dict
            suboptions:
              icmp:
                description: ICMP parameters.
                type: dict
                suboptions:
                  icmp_code:
                    description: ICMP code.
                    type: int
                  icmp_type:
                    description: ICMP type.
                    type: int
              protocol_number:
                description: Protocol number.
                type: dict
                suboptions:
                  protocol_number:
                    description: Protocol number.
                    type: int
              tcp:
                description: TCP parameters.
                type: dict
                suboptions:
                  destination_port_ranges:
                    description: Destination port ranges.
                    elements: dict
                    type: list
                    suboptions:
                      end_port:
                        description: End port of the range.
                        type: int
                      start_port:
                        description: Start port of the range.
                        type: int
                  source_port_ranges:
                    description: Source port ranges.
                    elements: dict
                    type: list
                    suboptions:
                      end_port:
                        description: End port of the range.
                        type: int
                      start_port:
                        description: Start port of the range.
                        type: int
              udp:
                description: UDP parameters.
                type: dict
                suboptions:
                  destination_port_ranges:
                    description: Destination port ranges.
                    elements: dict
                    type: list
                    suboptions:
                      end_port:
                        description: End port of the range.
                        type: int
                      start_port:
                        description: Start port of the range.
                        type: int
                  source_port_ranges:
                    description: Source port ranges.
                    elements: dict
                    type: list
                    suboptions:
                      end_port:
                        description: End port of the range.
                        type: int
                      start_port:
                        description: Start port of the range.
                        type: int
          protocol_type:
            description: Type of protocol.
            choices:
              - ANY
              - ICMP
              - TCP
              - UDP
              - PROTOCOL_NUMBER
            type: str
    type: list
  priority:
    description: Priority of the routing policy.
    type: int
  vpc_ext_id:
    description: ExtId of the VPC extId to which the routing policy belongs.
    type: str

extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Create PBR with vpc, custom source network, external destination, reroute action and udp port rangelist
  nutanix.ncp.ntnx_pbrs_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpc_ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
    state: present
    priority: 207
    name: "test_name"
    policies:
      -
        policy_action:
          action_type: REROUTE
          reroute_params:
            -
              reroute_fallback_action: NO_ACTION
              service_ip:
                ipv4:
                  value: 10.0.0.16
                  prefix_length: 32
        policy_match:
          source:
            address_type: SUBNET
            subnet_prefix:
              ipv4:
                ip:
                  value: 192.168.1.0
                  prefix_length: 24
          destination:
            address_type: ANY
          protocol_type: UDP
          protocol_parameters:
            udp:
              source_port_ranges:
                - start_port: 10
                  end_port: 20
              destination_port_ranges:
                - start_port: 30
                  end_port: 40
  register: result
  ignore_errors: true

- name: Create a routing policy for a VPC to permit certain source for certain destination
  nutanix.ncp.ntnx_pbrs_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: test
    priority: 2
    vpc_ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
    policies:
      -
        policy_action:
          action_type: PERMIT
        policy_match:
          source:
            address_type: SUBNET
            subnet_prefix:
              ipv4:
                ip:
                  value: 192.168.1.0
                prefix_length: 24
          destination:
            address_type: EXTERNAL
          protocol_type: ICMP
          protocol_parameters:
            icmp:
              icmp_type: 25
              icmp_code: 1
  register: result


- name: Create PBR with vpc, any source, any destination, any protocol and deny action
  nutanix.ncp.ntnx_pbrs_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpc_ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
    state: present
    priority: 3
    name: test2
    policies:
      -
        policy_action:
          action_type: DENY
        policy_match:
          source:
            address_type: ANY
          destination:
            address_type: ANY
          protocol_type: ANY
  register: result

- name: Update PBR name ,description, priority
  nutanix.ncp.ntnx_pbrs_v2:
    state: present
    ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
    priority: "156"
    name: "new_name"
    description: "Updated Test desc"
  register: result
  ignore_errors: true

- name: Delete created pbr
  nutanix.ncp.ntnx_pbrs_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
  register: result
"""

RETURN = r"""
response:
  description:
        - Response for the routing policy operations.
        - routing policy details if C(wait) is true.
        - Task details if C(wait) is false.
  returned: always
  type: dict
  sample:
      {
        "description": null,
        "ext_id": "d58da731-6baa-4d36-8afd-f400619012f1",
        "links": null,
        "metadata": {
            "category_ids": null,
            "owner_reference_id": "00000000-0000-0000-0000-000000000000",
            "owner_user_name": null,
            "project_name": null,
            "project_reference_id": null
        },
        "name": "HBLzQdIgfKUoansible-pbr-4",
        "policies": [
            {
                "is_bidirectional": false,
                "policy_action": {
                    "action_type": "REROUTE",
                    "nexthop_ip_address": null,
                    "reroute_params": [
                        {
                            "egress_service_ip": {
                                "ipv4": {
                                    "prefix_length": 32,
                                    "value": "10.0.0.15"
                                },
                                "ipv6": null
                            },
                            "ingress_service_ip": {
                                "ipv4": {
                                    "prefix_length": 32,
                                    "value": "10.0.0.15"
                                },
                                "ipv6": null
                            },
                            "reroute_fallback_action": "NO_ACTION",
                            "service_ip": {
                                "ipv4": {
                                    "prefix_length": 32,
                                    "value": "10.0.0.15"
                                },
                                "ipv6": null
                            }
                        }
                    ]
                },
                "policy_match": {
                    "destination": {
                        "address_type": "SUBNET",
                        "subnet_prefix": {
                            "ipv4": {
                                "ip": {
                                    "prefix_length": 32,
                                    "value": "192.168.2.0"
                                },
                                "prefix_length": null
                            },
                            "ipv6": null
                        }
                    },
                    "protocol_parameters": {
                        "destination_port_ranges": [
                            {
                                "end_port": 120,
                                "start_port": 100
                            }
                        ],
                        "source_port_ranges": [
                            {
                                "end_port": 80,
                                "start_port": 80
                            }
                        ]
                    },
                    "protocol_type": "TCP",
                    "source": {
                        "address_type": "EXTERNAL",
                        "subnet_prefix": null
                    }
                }
            }
        ],
        "priority": 208,
        "tenant_id": null,
        "vpc": null,
        "vpc_ext_id": "41a565cc-f669-4ce1-807f-56a71ae946ad"
    }

changed:
  description:
    - Whether the routing policy is changed or not.
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: str
  sample: false


ext_id:
  description:
          - External ID of the routing policy.
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"

skipped:
    description:
        - Whether the operation is skipped or not.
        - Will be returned if operation is skipped.
    type: bool
    returned: always
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_routing_policies_api_instance,
)
from ..module_utils.v4.network.helpers import get_routing_policy  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as net_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as net_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    protocol_param_obj_map = {
        "icmp": net_sdk.ICMPObject,
        "tcp": net_sdk.LayerFourProtocolObject,
        "udp": net_sdk.LayerFourProtocolObject,
        "protocol_number": net_sdk.ProtocolNumberObject,
    }

    ip_address_sub_spec = dict(
        value=dict(type="str"),
        prefix_length=dict(type="int"),
    )

    ip_address_spec = dict(
        ipv4=dict(type="dict", options=ip_address_sub_spec, obj=net_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ip_address_sub_spec, obj=net_sdk.IPv6Address),
    )

    ipv4_subnet_spec = dict(
        ip=dict(type="dict", options=ip_address_sub_spec, obj=net_sdk.IPv4Address),
        prefix_length=dict(type="int"),
    )

    ipv6_subnet_spec = dict(
        ip=dict(type="dict", options=ip_address_sub_spec, obj=net_sdk.IPv6Address),
        prefix_length=dict(type="int"),
    )

    ip_subnet_spec = dict(
        ipv4=dict(type="dict", options=ipv4_subnet_spec, obj=net_sdk.IPv4Subnet),
        ipv6=dict(type="dict", options=ipv6_subnet_spec, obj=net_sdk.IPv6Subnet),
    )

    address_type_object_spec = dict(
        address_type=dict(type="str", choices=["ANY", "EXTERNAL", "SUBNET"]),
        subnet_prefix=dict(type="dict", options=ip_subnet_spec, obj=net_sdk.IPSubnet),
    )

    icmp_spec = dict(
        icmp_type=dict(type="int"),
        icmp_code=dict(type="int"),
    )

    port_range_spec = dict(
        start_port=dict(type="int"),
        end_port=dict(type="int"),
    )

    tcp_udp_spec = dict(
        source_port_ranges=dict(
            type="list", elements="dict", options=port_range_spec, obj=net_sdk.PortRange
        ),
        destination_port_ranges=dict(
            type="list", elements="dict", options=port_range_spec, obj=net_sdk.PortRange
        ),
    )

    protocol_number_spec = dict(protocol_number=dict(type="int"))

    protocol_params_spec = dict(
        icmp=dict(type="dict", options=icmp_spec),
        tcp=dict(type="dict", options=tcp_udp_spec),
        udp=dict(type="dict", options=tcp_udp_spec),
        protocol_number=dict(type="dict", options=protocol_number_spec),
    )

    rpmc_spec = dict(
        source=dict(
            type="dict", options=address_type_object_spec, obj=net_sdk.AddressTypeObject
        ),
        destination=dict(
            type="dict", options=address_type_object_spec, obj=net_sdk.AddressTypeObject
        ),
        protocol_type=dict(
            type="str", choices=["ANY", "ICMP", "TCP", "UDP", "PROTOCOL_NUMBER"]
        ),
        protocol_parameters=dict(
            type="dict",
            options=protocol_params_spec,
            obj=protocol_param_obj_map,
            mutually_exclusive=[("icmp", "tcp", "udp", "protocol_number")],
        ),
    )

    reroute_param_spec = dict(
        service_ip=dict(type="dict", options=ip_address_spec, obj=net_sdk.IPAddress),
        reroute_fallback_action=dict(
            type="str", choices=["ALLOW", "DROP", "PASSTHROUGH", "NO_ACTION"]
        ),
        ingress_service_ip=dict(
            type="dict", options=ip_address_spec, obj=net_sdk.IPAddress
        ),
        egress_service_ip=dict(
            type="dict", options=ip_address_spec, obj=net_sdk.IPAddress
        ),
    )

    rpa_spec = dict(
        action_type=dict(type="str", choices=["PERMIT", "DENY", "REROUTE", "FORWARD"]),
        reroute_params=dict(
            type="list",
            elements="dict",
            options=reroute_param_spec,
            obj=net_sdk.RerouteParam,
        ),
        nexthop_ip_address=dict(
            type="dict", options=ip_address_spec, obj=net_sdk.IPAddress
        ),
    )

    rpr_spec = dict(
        policy_match=dict(
            type="dict", options=rpmc_spec, obj=net_sdk.RoutingPolicyMatchCondition
        ),
        policy_action=dict(
            type="dict", options=rpa_spec, obj=net_sdk.RoutingPolicyAction
        ),
        is_bidirectional=dict(type="bool"),
    )

    metadata_spec = dict(
        owner_reference_id=dict(type="str"),
        project_reference_id=dict(type="str"),
        category_ids=dict(type="list", elements="str"),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        priority=dict(type="int"),
        vpc_ext_id=dict(type="str"),
        policies=dict(
            type="list",
            elements="dict",
            options=rpr_spec,
            obj=net_sdk.RoutingPolicyRule,
        ),
        metadata=dict(type="dict", options=metadata_spec, obj=net_sdk.Metadata),
    )

    return module_args


def get_routing_policy_ext_id(module, result, api_instance, vpc_ext_id, priority):
    params = {
        "filter": "priority eq {0} and vpcExtId eq '{1}'".format(priority, vpc_ext_id)
    }
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=params)
    if err:
        result["error"] = err
        msg = "Failed generating spec for fetching routing policy using priority and vpc_ext_id"
        module.fail_json(msg=msg, **result)

    try:
        resp = api_instance.list_routing_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching routing policies info",
        )

    if resp and getattr(resp, "data", []):
        return resp.data[0].ext_id
    else:
        return None


def create_pbr(module, result):
    if not module.params.get("vpc_ext_id") and module.params.get("priority"):
        msg = "vpc_ext_id and priority are required for creating routing policy"
        module.fail_json(msg=msg, **result)

    pbrs = get_routing_policies_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = net_sdk.RoutingPolicy()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create pbrs Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = pbrs.create_routing_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating pbr",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_routing_policy_ext_id(
            module,
            result,
            pbrs,
            module.params.get("vpc_ext_id"),
            module.params.get("priority"),
        )
        if ext_id:
            resp = get_routing_policy(module, pbrs, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_pbrs_idempotency(old_spec, update_spec):
    if old_spec != update_spec:
        return False
    return True


def update_pbr(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    pbrs = get_routing_policies_api_instance(module)
    current_spec = get_routing_policy(module, pbrs, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating pbrs update spec", **result)

    # check for idempotency
    if check_pbrs_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = pbrs.update_routing_policy_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating pbr",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_routing_policy(module, pbrs, ext_id)
        result["ext_id"] = ext_id
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_pbr(module, result):
    pbrs = get_routing_policies_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_routing_policy(module, pbrs, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("unable to fetch etag for deleting pbr", **result)

    kwargs = {"if_match": etag}

    try:
        resp = pbrs.delete_routing_policy_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting pbr",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id", "priority", "vpc_ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_pbr(module, result)
        else:
            create_pbr(module, result)
    else:
        delete_pbr(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
