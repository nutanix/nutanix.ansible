#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpcs_v2
short_description: vpcs module which supports vpc CRUD operations
version_added: 2.0.0
description:
  - Create, Update, Delete vpcs
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
        - Specify state
        - If C(state) is set to C(present) then module will create vpc.
        - if C(state) is set to C(present) and C(ext_id) is given, then module will update vpc.
        - If C(state) is set to C(absent) with C(ext_id), then module will delete vpc.
    choices:
        - present
        - absent
    type: str
    default: present
  wait:
      description: Wait for the operation to complete.
      type: bool
      required: false
      default: True
  ext_id:
    description:
            - The external ID of the vpc.
            - Required for C(state)=absent for delete.
            - Required for C(state)=present to trigger update of vpc.
    type: str

  name:
    description: Name of the VPC.
    type: str

  description:
    description: Description of the VPC.
    type: str

  vpc_type:
    description: Type of the VPC.
    type: str
    choices:
      - REGULAR
      - TRANSIT

  common_dhcp_options:
    description: List of DHCP options to be configured.
    type: dict
    suboptions:
      domain_name_servers:
        description: List of Domain Name Server addresses .
        type: list
        elements: dict
        suboptions:
          ipv4:
            description: IPv4 address.
            type: dict
            suboptions:
              value:
                description: The IPv4 address value.
                type: str
              prefix_length:
                description: The prefix length of the IPv4 address.
                type: int
          ipv6:
            description: IPv6 address.
            type: dict
            suboptions:
              value:
                description: The IPv6 address value.
                type: str
              prefix_length:
                description: The prefix length of the IPv6 address.
                type: int

  external_subnets:
    description: List of external subnets that the VPC is attached to.
    type: list
    elements: dict
    suboptions:
      subnet_reference:
        description: External subnet reference.
        type: str
      external_ips:
        description:
            - List of IP Addresses used for SNAT, if NAT is enabled on the external subnet.
              If NAT is not enabled, this specifies the IP address of the VPC port connected to the external gateway.
        type: list
        elements: dict
        suboptions:
          ipv4:
            description: IPv4 address.
            type: dict
            suboptions:
              value:
                description: The IPv4 address value.
                type: str
              prefix_length:
                description: The prefix length of the IPv4 address.
                type: int
          ipv6:
            description: IPv6 address.
            type: dict
            suboptions:
              value:
                description: The IPv6 address value.
                type: str
              prefix_length:
                description: The prefix length of the IPv6 address.
                type: int
      gateway_nodes:
        description: List of gateway nodes that can be used for external connectivity.
        type: str
      active_gateway_node:
        description: Reference of gateway nodes
        type: dict
        suboptions:
          node_id:
            description: Node ID.
            type: str
          node_ip_address:
            description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
            type: dict
            suboptions:
              ipv4:
                description: IPv4 address.
                type: dict
                suboptions:
                  value:
                    description: The IPv4 address value.
                    type: str
                  prefix_length:
                    description: The prefix length of the IPv4 address.
                    type: int
              ipv6:
                description: IPv6 address.
                type: dict
                suboptions:
                  value:
                    description: The IPv6 address value.
                    type: str
                  prefix_length:
                    description: The prefix length of the IPv6 address.
                    type: int
      active_gateway_count:
        description: Number of active gateways.
        type: int

  external_routing_domain_reference:
    description: External routing domain associated with this route table
    type: str

  externally_routable_prefixes:
    description:
        - CIDR blocks from the VPC which can talk externally without performing NAT.
          This is applicable when connecting to external subnets which have disabled NAT.
    type: list
    elements: dict
    suboptions:
      ipv4:
        description: IPv4 subnet.
        type: dict
        suboptions:
          ip:
            description: IPv4 address.
            type: dict
            suboptions:
              value:
                description: The IPv4 address value.
                type: str
              prefix_length:
                description: The prefix length of the IPv4 address.
                type: int
          prefix_length:
            description: The prefix length of the subnet.
            type: int
      ipv6:
        description: IPv6 subnet.
        type: dict
        suboptions:
          ip:
            description: IPv6 address.
            type: dict
            suboptions:
              value:
                description: The IPv6 address value.
                type: str
              prefix_length:
                description: The prefix length of the IPv6 address.
                type: int
          prefix_length:
            description: The prefix length of the subnet.
            type: int

  metadata:
    description: Metadata associated with this resource.
    type: dict
    suboptions:
      owner_reference_id:
        description: A globally unique identifier that represents the owner of this resource.
        type: str
      owner_user_name:
        description: The userName of the owner of this resource.
        type: str
      project_reference_id:
        description: A globally unique identifier that represents the project this resource belongs to.
        type: str
      project_name:
        description: The name of the project this resource belongs to.
        type: str
      category_ids:
        description: A list of globally unique identifiers that represent all the categories the resource is associated with.
        type: list
        elements: str

extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Create min VPC with external_nat_subnet uuid
  nutanix.ncp.ntnx_vpcs_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    wait: true
    name: MinVPC
    external_subnets:
      - subnet_reference: "{{ external_nat_subnet.uuid }}"
  register: result

- name: Create VPC with routable_ips
  nutanix.ncp.ntnx_vpcs_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: vpc_with_routable_ips
    externally_routable_prefixes:
      -
        ipv4:
          ip:
            value: "{{ routable_ips.network_ip }}"
          prefix_length: "{{ routable_ips.network_prefix }}"

- name: Create VPC with dns_servers
  nutanix.ncp.ntnx_vpcs_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: vpc_with_dns_servers
    common_dhcp_options:
      domain_name_servers:
        -
          ipv4:
            value: "{{ dns_servers.0 }}"
            prefix_length: 32
        -
          ipv4:
            value: "{{ dns_servers.1 }}"
            prefix_length: 32
  register: result

- name: Delete all created vpcs
  nutanix.ncp.ntnx_vpcs_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "{{ item }}"
  register: result
  loop: "{{ todelete }}"
"""

RETURN = r"""
response:
  description: The created vpc object
  returned: always
  type: dict
  sample:
    {
            "common_dhcp_options": {
                "domain_name_servers": null
            },
            "description": null,
            "ext_id": "ce14a4cc-5a9a-4dd0-8f82-daadc1045e57",
            "external_routing_domain_reference": null,
            "external_subnets": [
                {
                    "active_gateway_count": 1,
                    "active_gateway_node": {
                        "node_id": "a9b4cb02-2487-4878-a6b6-395bd4f5fb61",
                        "node_ip_address": {
                            "ipv4": {
                                "prefix_length": 32,
                                "value": "000.000.000.000"
                            },
                            "ipv6": null
                        }
                    },
                    "active_gateway_nodes": [
                        {
                            "node_id": "a9b4cb02-2487-4878-a6b6-395bd4f5fb61",
                            "node_ip_address": {
                                "ipv4": {
                                    "prefix_length": 32,
                                    "value": "000.000.000.000"
                                },
                                "ipv6": null
                            }
                        }
                    ],
                    "external_ips": [
                        {
                            "ipv4": {
                                "prefix_length": 32,
                                "value": "000.000.000.000"
                            },
                            "ipv6": null
                        }
                    ],
                    "gateway_nodes": null,
                    "subnet_reference": "b000b263-8662-4a7f-a841-32eaf5b97d5d"
                }
            ],
            "externally_routable_prefixes": null,
            "links": null,
            "metadata": {
                "category_ids": null,
                "owner_reference_id": "00000000-0000-0000-0000-000000000000",
                "owner_user_name": null,
                "project_name": null,
                "project_reference_id": null
            },
            "name": "rohcTvGipSJQansible-ag2",
            "snat_ips": null,
            "tenant_id": null,
            "vpc_type": "REGULAR"
        }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false


ext_id:
  description: The external ID of VPC
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_vpc_api_instance,
)
from ..module_utils.v4.network.helpers import get_vpc  # noqa: E402
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
    import ntnx_networking_py_client as net_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as net_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    ip_address_sub_spec = dict(
        value=dict(type="str"),
        prefix_length=dict(type="int"),
    )

    ip_address_spec = dict(
        ipv4=dict(type="dict", options=ip_address_sub_spec, obj=net_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ip_address_sub_spec, obj=net_sdk.IPv6Address),
    )

    vpc_dhcp_options_spec = dict(
        domain_name_servers=dict(
            type="list", elements="dict", options=ip_address_spec, obj=net_sdk.IPAddress
        ),
    )

    gnr_spec = dict(
        node_id=dict(type="str"),
        node_ip_address=dict(
            type="dict", options=ip_address_spec, obj=net_sdk.IPAddress
        ),
    )

    external_subnet_spec = dict(
        subnet_reference=dict(type="str"),
        external_ips=dict(
            type="list", elements="dict", options=ip_address_spec, obj=net_sdk.IPAddress
        ),
        gateway_nodes=dict(type="str"),
        active_gateway_node=dict(
            type="dict", options=gnr_spec, obj=net_sdk.GatewayNodeReference
        ),
        active_gateway_count=dict(type="int"),
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

    metadata_spec = dict(
        owner_reference_id=dict(type="str"),
        owner_user_name=dict(type="str"),
        project_reference_id=dict(type="str"),
        project_name=dict(type="str"),
        category_ids=dict(type="list", elements="str"),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        vpc_type=dict(type="str", choices=["REGULAR", "TRANSIT"]),
        common_dhcp_options=dict(
            type="dict", options=vpc_dhcp_options_spec, obj=net_sdk.VpcDhcpOptions
        ),
        external_subnets=dict(
            type="list",
            elements="dict",
            options=external_subnet_spec,
            obj=net_sdk.ExternalSubnet,
        ),
        external_routing_domain_reference=dict(type="str"),
        externally_routable_prefixes=dict(
            type="list", elements="dict", options=ip_subnet_spec, obj=net_sdk.IPSubnet
        ),
        metadata=dict(type="dict", options=metadata_spec, obj=net_sdk.Metadata),
    )

    return module_args


def create_vpc(module, result):
    vpcs = get_vpc_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = net_sdk.Vpc()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create vpcs Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = vpcs.create_vpc(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating vpc",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.VPC
        )
        if ext_id:
            resp = get_vpc(module, vpcs, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_vpcs_idempotency(old_spec, update_spec):
    if old_spec != update_spec:
        return False
    return True


def update_vpc(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    vpcs = get_vpc_api_instance(module)

    current_spec = get_vpc(module, vpcs, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vpcs update spec", **result)

    # check for idempotency
    if check_vpcs_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    vpcs = get_vpc_api_instance(module)
    try:
        resp = vpcs.update_vpc_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating vpc",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_vpc(module, vpcs, ext_id)
        result["ext_id"] = ext_id
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_vpc(module, result):
    vpcs = get_vpc_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_vpc(module, vpcs, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("unable to fetch etag for deleting vpc", **result)

    kwargs = {"if_match": etag}

    try:
        resp = vpcs.delete_vpc_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting vpc",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
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
            update_vpc(module, result)
        else:
            create_vpc(module, result)
    else:
        delete_vpc(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
