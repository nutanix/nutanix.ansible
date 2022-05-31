#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters
short_description: pbr module which suports pbr CRUD operations
version_added: 1.0.0
description: 'Create, Update, Delete, Power-on, Power-off Nutanix pbr''s'
options:
  priority:
    description: The policy priority number
    type: int
  pbr_uuid:
    description: PBR UUID
    type: str
  vpc:
    description:
      - Virtual Private Clouds
    type: dict
    suboptions:
      name:
        description:
          - VPC Name
          - Mutually exclusive with C(uuid)
        type: str
      uuid:
        description:
          - VPC UUID
          - Mutually exclusive with C(name)
        type: str
  source:
    description: Where the traffic come from
    type: dict
    suboptions:
      any:
        description:
          - Traffic from any source with no specification
          - Mutually exclusive with C(external) and C(network)
        type: bool
      external:
        description:
          - Traffic from external network
          - Mutually exclusive with C(any) and C(network)
        type: bool
      network:
        description:
          - Traffic from specfic network address
          - Mutually exclusive with C(any) and C(external)
        type: dict
        suboptions:
          ip:
            description: Subnet ip address
            type: str
          prefix:
            description: IP address prefix length
            type: str
  destination:
    type: dict
    description: Where the traffic going to
    suboptions:
      any:
        description:
          - Traffic to any destination with no specification
          - Mutually exclusive with C(external) and C(network)
        type: bool
      external:
        description:
          - Traffic to external network
          - Mutually exclusive with C(any) and C(network)
        type: bool
      network:
        description:
          - Traffic to specfic network address
          - Mutually exclusive with C(any) and C(external)
        type: dict
        suboptions:
          ip:
            description: Subnet ip address
            type: str
          prefix:
            description: IP address prefix length
            type: str
  protocol:
    type: dict
    description: The Network Protocol that will be used
    suboptions:
      any:
        description:
          - Any protcol number
          - Mutually exclusive with C(tcp) and C(udp) and C(number) and C(icmp)
        type: bool
      tcp:
        description:
          - The Transmission Control protocol will be used
          - Mutually exclusive with C(any) and C(udp) and C(number) and C(icmp)
        type: dict
        suboptions:
          src:
            default: '*'
            type: list
            elements: str
            description: The source port
          dst:
            default: '*'
            type: list
            elements: str
            description: The destination port
      udp:
        description:
          - User Datagram protocol will be used
          - Mutually exclusive with C(any) and C(tcp) and C(number) and C(icmp)
        type: dict
        suboptions:
          src:
            default: '*'
            type: list
            elements: str
            description: The source port
          dst:
            default: '*'
            type: list
            elements: str
            description: The destination port
      number:
        description:
          - The internet protocol number
          - Mutually exclusive with C(any) and C(tcp) and C(udp) and C(icmp)
        type: int
      icmp:
        description: Internet Control Message protocol will be used
        type: dict
        suboptions:
          code:
            type: int
            description:
              - ICMP code
              - Mutually exclusive with any
          type:
            description:
              - ICMP type it's required by code
              - Mutually exclusive with any
            type: int
          any:
            description: allow any icmp code or type
            type: bool
  action:
    type: dict
    description: The behavior on the request
    suboptions:
      deny:
        description:
          - Drop the request
          - Mutually exclusive with C(allow) and C(reroute)
        type: bool
      allow:
        description:
          - Accept the request
          - Mutually exclusive with C(deny) and C(reroute)
        type: bool
      reroute:
        description:
          - Change the request route
          - Mutually exclusive with C(allow) and C(deny)
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
  - Dina AbuHijleh (@dina-abuhijleh)
"""

EXAMPLES = r"""

- name: create PBR with vpc name with any source or destination or protocol with deny action
  ntnx_clusters:
    validate_certs: False
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    priority: "{{ priority.0 }}"
    vpc:
      name: "{{ vpc.name }}"
    source:
      any: True
    destination:
      any: True
    action:
      deny: True
    protocol:
      any: True

- name: create PBR with vpc uuid with source Any and destination external and allow action with protocol number
  ntnx_clusters:
    validate_certs: False
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    priority: "{{ priority.1 }}"
    vpc:
      uuid: "{{ vpc.uuid }}"
    source:
      any: True
    destination:
      external: True
    action:
      allow: True
      type: bool
    protocol:
      number: "{{ protocol.number }}"

- name: create PBR with vpc name with source external and destination network with reroute action and  tcp port rangelist
  ntnx_clusters:
    validate_certs: False
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    priority: "{{ priority.2 }}"
    vpc:
      name: "{{ vpc.name }}"
    source:
      external: True
    destination:
      network:
        ip: "{{ network.ip }}"
        prefix: "{{ network.prefix }}"
    action:
      reroute: "{{ reroute_ip }}"
    protocol:
      tcp:
        src: "{{ tcp.port }}"
        dst: "{{ tcp.port_rangelist }}"

- name: create PBR with vpc name with source network and destination external with reroute action and  udp port rangelist
  ntnx_clusters:
    validate_certs: False
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    priority: "{{ priority.3 }}"
    vpc:
      name: "{{ vpc.name }}"
    source:
      network:
        ip: "{{ network.ip }}"
        prefix: "{{ network.prefix }}"
    destination:
      any: True
    action:
      reroute: "{{reroute_ip}}"
    protocol:
      udp:
        src: "{{ udp.port_rangelist }}"
        dst: "{{ udp.port }}"

- name: create PBR with vpc name with source network and destination external with reroute action and icmp
  ntnx_clusters:
    validate_certs: False
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    priority: "{{ priority.5 }}"
    vpc:
      name: "{{ vpc.name }}"
    source:
      network:
        ip: "{{ network.ip }}"
        prefix: "{{ network.prefix }}"
    destination:
      external: True
    action:
      reroute: "{{ reroute_ip }}"
    protocol:
      icmp:
        code: "{{ icmp.code }}"
        type: "{{ icmp.type }}"

- name: Delete all Created pbrs
  ntnx_clusters:
    state: absent
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    pbr_uuid: "{{ item }}"
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The PBR metadata
  returned: always
  type: dict
  sample:  {
            "api_version": "3.1",
            "metadata": {
                "categories": {},
                "categories_mapping": {},
                "creation_time": "2022-02-17T08:29:31Z",
                "kind": "routing_policy",
                "last_update_time": "2022-02-17T08:29:33Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "spec_version": 0,
                "uuid": "64c5a93d-7cd4-45f9-81e9-e0b08d35077a"
            }
}
spec:
  description: An intentful representation of a PRB spec
  returned: always
  type: dict
  sample: {
                "name": "Policy with priority205",
                "resources": {
                    "action": {
                        "action": "DENY"
                    },
                    "destination": {
                        "address_type": "ALL"
                    },
                    "priority": 205,
                    "protocol_type": "ALL",
                    "source": {
                        "address_type": "ALL"
                    },
                    "vpc_reference": {
                        "kind": "vpc",
                        "uuid": "ebf8130e-09b8-48d9-a9d3-5ef29983f5fe"
                    }
                }
            }
status:
  description: An intentful representation of a PBR status
  returned: always
  type: dict
  sample:  {
                "execution_context": {
                    "task_uuid": [
                        "f83bbb29-3ca8-42c2-b29b-4fca4a7a25c3"
                    ]
                },
                "name": "Policy with priority205",
                "resources": {
                    "action": {
                        "action": "DENY"
                    },
                    "destination": {
                        "address_type": "ALL"
                    },
                    "priority": 205,
                    "protocol_type": "ALL",
                    "routing_policy_counters": {
                        "byte_count": 0,
                        "packet_count": 0
                    },
                    "source": {
                        "address_type": "ALL"
                    },
                    "vpc_reference": {
                        "kind": "vpc",
                        "name": "ET_pbr",
                        "uuid": "ebf8130e-09b8-48d9-a9d3-5ef29983f5fe"
                    }
                },
                "state": "COMPLETE"
            }
pbr_uuid:
  description: The created PBR uuid
  returned: always
  type: str
  sample: "64c5a93d-7cd4-45f9-81e9-e0b08d35077a"
task_uuid:
  description: The task uuid for the creation
  returned: always
  type: str
  sample: "f83bbb29-3ca8-42c2-b29b-4fca4a7a25c3"
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.clusters import Cluster  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    module_args = dict(
        cluster=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive, required=True,
        ),
        authorized_public_key_list=dict(type="list"),
    )

    return module_args


def create_public_key_entry(module, result):
    cluster = Cluster(module)
    old_spec = cluster.get_current_spec()
    spec, error = cluster.get_spec(old_spec)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating cluster Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return
    uuid = spec["metadata"]["uuid"]
    resp = cluster.update(spec, uuid)
    # does a return response value sense?
    # cluster_uuid = resp["metadata"]["uuid"]
    result["changed"] = True
    result["response"] = resp
    #result["pbr_uuid"] = pbr_uuid
    result["task_uuid"] = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        wait_for_task_completion(module, result)
        resp = cluster.read(uuid)
        result["response"] = resp

def wait_for_task_completion(module, result):
    task = Task(module)
    task_uuid = result["task_uuid"]
    resp = task.wait_for_completion(task_uuid)
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "task_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        create_public_key_entry(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
