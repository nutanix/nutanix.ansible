#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_subnets_v2
short_description: subnets module which supports Create, Update, Delete subnets
version_added: 2.0.0
description:
  - Create, Update, Delete subnets
  - This module uses PC v4 APIs based SDKs
notes:
  - For updating IPAM config using C(ip_config), provide all details again. Module will not fetch existing IPAM config.
  - For subnet create and delete, module will return tasks status in response after operation.
  - For subnet update, module will return subnet info if C(wait) is true, else task status.
options:
  state:
    description:
      - if C(state) is present, it will create or update the subnet.
      - If C(state) is set to C(present) and ext_id is not provided then the operation will be create the subnet
      - If C(state) is set to C(present) and ext_id is provided then the operation will be update the subnet
      - If C(state) is set to C(absent) and ext_id is provided , then operation will be delete the subnet
    type: str
    choices: ['present', 'absent']
  name:
    description:
      - Subnet name
    type: str
  ext_id:
    description:
      - Subnet external ID
      - Required only for updating or deleting the subnet.
    type: str
  subnet_type:
    description:
      - Type of the subnet
    type: str
    choices: ['OVERLAY', 'VLAN']
  network_id:
    description:
      - Network ID
    type: int
  dhcp_options:
    description:
      - DHCP options
    type: dict
    suboptions:
      domain_name_servers:
        description:
          - Domain name servers
        type: list
        elements: dict
        suboptions:
          ipv4:
            description:
              - IPv4 address
            type: dict
            suboptions:
              value:
                description:
                  - IP address
                type: str
              prefix_length:
                description:
                  - Prefix length
                type: int
          ipv6:
            description:
              - IPv6 address
            type: dict
            suboptions:
              value:
                description:
                  - IP address
                type: str
              prefix_length:
                description:
                  - Prefix length
                type: int
      domain_name:
        description:
          - Domain name
        type: str
      tftp_server_name:
        description:
          - TFTP server name
        type: str
      boot_file_name:
        description:
          - Boot file name
        type: str
      ntp_servers:
        description:
          - NTP servers
        type: list
        elements: dict
        suboptions:
          ipv4:
            description:
              - IPv4 address
            type: dict
            suboptions:
              value:
                description:
                  - IP address
                type: str
              prefix_length:
                description:
                  - Prefix length
                type: int
          ipv6:
            description:
              - IPv6 address
            type: dict
            suboptions:
              value:
                description:
                  - IP address
                type: str
              prefix_length:
                description:
                  - Prefix length
                type: int
      search_domains:
        description:
          - Search domains
        type: list
        elements: str
  ip_config:
    description:
      - IPAM configuration
    type: list
    elements: dict
    suboptions:
      ipv4:
        description:
          - IPv4 configuration
        type: dict
        suboptions:
          ip_subnet:
            description:
              - IP subnet
            type: dict
            suboptions:
              ip:
                description:
                  - IP address
                type: dict
                suboptions:
                  value:
                    description:
                      - IP address
                    type: str
                  prefix_length:
                    description:
                      - Prefix length
                    type: int
              prefix_length:
                description:
                  - Prefix length
                  - Required field
                type: int
          default_gateway_ip:
            description:
              - Default gateway IP
            type: dict
            suboptions:
              value:
                description:
                  - IP address
                type: str
              prefix_length:
                description:
                  - Prefix length
                type: int
          dhcp_server_address:
            description:
              - DHCP server address
            type: dict
            suboptions:
              value:
                description:
                  - IP address
                type: str
              prefix_length:
                description:
                  - Prefix length
                type: int
          pool_list:
            description:
              - Pool list
            type: list
            elements: dict
            suboptions:
              start_ip:
                description:
                  - Start IP
                type: dict
                suboptions:
                  value:
                    description:
                      - IP address
                    type: str
                  prefix_length:
                    description:
                      - Prefix length
                    type: int
              end_ip:
                description:
                  - End IP
                type: dict
                suboptions:
                  value:
                    description:
                      - IP address
                    type: str
                  prefix_length:
                    description:
                      - Prefix length
                    type: int
      ipv6:
        description:
          - IPv6 configuration
        type: dict
        suboptions:
          ip_subnet:
            description:
              - IP subnet
            type: dict
            suboptions:
              ip:
                description:
                  - IP address
                type: dict
                suboptions:
                  value:
                    description:
                      - IP address
                    type: str
                  prefix_length:
                    description:
                      - Prefix length
                    type: int
              prefix_length:
                description:
                  - Prefix length
                type: int
          default_gateway_ip:
            description:
              - Default gateway IP
            type: dict
            suboptions:
              value:
                description:
                  - IP address
                type: str
              prefix_length:
                description:
                  - Prefix length
                type: int
          dhcp_server_address:
            description:
              - DHCP server address
            type: dict
            suboptions:
              value:
                description:
                  - IP address
                type: str
              prefix_length:
                description:
                  - Prefix length
                type: int
          pool_list:
            description:
              - Pool list
            type: list
            elements: dict
            suboptions:
              start_ip:
                description:
                  - Start IP
                type: dict
                suboptions:
                  value:
                    description:
                      - IP address
                    type: str
                  prefix_length:
                    description:
                      - Prefix length
                    type: int
              end_ip:
                description:
                  - End IP
                type: dict
                suboptions:
                  value:
                    description:
                      - IP address
                    type: str
                  prefix_length:
                    description:
                      - Prefix length
                    type: int
  cluster_reference:
    description:
      - Cluster external ID
      - Required for VLAN subnet type
    type: str
  virtual_switch_reference:
    description:
      - Virtual switch external ID
    type: str
  vpc_reference:
    description:
      - VPC external ID
      - Required for OVERLAY subnet type
    type: str
  is_nat_enabled:
    description:
      - flag to enable NAT
    type: bool
  is_external:
    description:
      - flag to mark the subnet as external
    type: bool
  network_function_chain_reference:
    description:
      - Network function chain external ID
    type: str
  is_advanced_networking:
    description:
      - flag to enable advanced networking
    type: bool
  ip_prefix:
    description:
      - IP prefix
    type: str
  wait:
    description:
      - Wait for the task to complete
    type: bool
    default: true
  metadata:
    description: Metadata associated with this resource.
    type: dict
    suboptions:
      owner_reference_id:
        description: owner external_id
        type: str
      project_reference_id:
        description: project external id
        type: str
      category_ids:
        description: A list of globally unique identifiers that represent all the categories the resource will be associated with.
        type: list
        elements: str
  hypervisor_type:
      description: Hypervisor type
      type: str
  description:
    type: str
    description: Description of the subnet.
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: VLAN subnet with IPAM IP pools
  nutanix.ncp.ntnx_subnets_v2:
    state: present
    nutanix_host: "{{ ip }}"
    validate_certs: false
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: VLAN subnet with IPAM IP pools
    subnet_type: VLAN
    cluster_reference: 00061663-9fa0-28ca-185b-ac1f6b6f97e2
    virtual_switch_reference: 18dbfce0-f7e1-4b19-a9e6-43b0be8c2507
    network_id: 226
    ip_config:
      - ipv4:
          ip_subnet:
            ip:
              value: 192.168.0.0
            prefix_length: 24
          default_gateway_ip:
            value: 192.168.0.254
            prefix_length: 24
          pool_list:
            - start_ip:
                value: 192.168.0.20
                prefix_length: 24
              end_ip:
                value: 192.168.0.30
                prefix_length: 24

- name: External subnet with NAT
  nutanix.ncp.ntnx_subnets_v2:
    state: present
    nutanix_host: "{{ ip }}"
    validate_certs: false
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: "External subnet with NAT"
    subnet_type: VLAN
    cluster_reference: 00061663-9fa0-28ca-185b-ac1f6b6f97e2
    network_id: 103
    is_external: true
    ip_config:
      - ipv4:
          ip_subnet:
            ip:
              value: 10.44.3.192
            prefix_length: 27
          default_gateway_ip:
            value: 10.44.3.193
            prefix_length: 27
          pool_list:
            - start_ip:
                value: 10.44.3.198
                prefix_length: 27
              end_ip:
                value: 10.44.3.207
                prefix_length: 27
            - start_ip:
                value: 10.44.3.208
                prefix_length: 27
              end_ip:
                value: 10.44.3.217
                prefix_length: 27

- name: Overlay Subnet with IP_pools
  nutanix.ncp.ntnx_subnets_v2:
    state: present
    nutanix_host: "{{ ip }}"
    validate_certs: false
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: Overlay Subnet with IP_pools and DHCP
    subnet_type: OVERLAY
    vpc_reference: 4c92c01e-2eb7-4a50-bda3-09729b62b634
    ip_config:
      - ipv4:
          ip_subnet:
            ip:
              value: 192.168.0.0
            prefix_length: 24
          default_gateway_ip:
            value: 192.168.0.254
            prefix_length: 24
          pool_list:
            - start_ip:
                value: 192.168.0.20
                prefix_length: 24
              end_ip:
                value: 192.168.0.30
                prefix_length: 24

- name: Delete subnets
  nutanix.ncp.ntnx_subnets_v2:
    state: absent
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    subnet_uuid: a3265671-de53-41be-af9b-f06241b95356
"""

RETURN = r"""
response:
    description:
        - Response for the subnet operations.
        - Subnet details if C(wait) is true.
        - Task details if C(wait) is false.
    type: dict
    returned: always
    sample: {
            "bridge_name": "br0",
            "cluster_name": null,
            "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
            "description": null,
            "dhcp_options": {
                "boot_file_name": null,
                "domain_name": null,
                "domain_name_servers": null,
                "ntp_servers": null,
                "search_domains": null,
                "tftp_server_name": null
            },
            "dynamic_ip_addresses": null,
            "ext_id": "1d42d222-a065-4ed8-9f74-dc5818dfab41",
            "hypervisor_type": "acropolis",
            "ip_config": [
                {
                    "ipv4": {
                        "default_gateway_ip": null,
                        "dhcp_server_address": null,
                        "ip_subnet": null,
                        "pool_list": null
                    },
                    "ipv6": null
                }
            ],
            "ip_prefix": null,
            "is_advanced_networking": null,
            "is_external": false,
            "is_nat_enabled": null,
            "links": null,
            "metadata": {
                "category_ids": null,
                "owner_reference_id": "00000000-0000-0000-0000-000000000000",
                "owner_user_name": null,
                "project_name": null,
                "project_reference_id": null
            },
            "name": "VLAN subnet without IPAM",
            "network_function_chain_reference": null,
            "network_id": 221,
            "reserved_ip_addresses": null,
            "subnet_type": "VLAN",
            "tenant_id": null,
            "virtual_switch": null,
            "virtual_switch_reference": "18dbfce0-f7e1-4b19-a9e6-43b0be8c2507",
            "vpc": null,
            "vpc_reference": null
        }
ext_id:
    description:
        - External ID of the subnet.
    type: str
    returned: always
task_ext_id:
    description:
        - Task external ID.
    type: str
    returned: always
changed:
    description:
        - Whether the subnet is changed or not.
    type: bool
    returned: always
skipped:
    description:
        - Whether the operation is skipped or not.
        - Will be returned if operation is skipped.
    type: bool
    returned: always
error:
    description:
        - Error message if an error occurs.
    type: str
    returned: when an error occurs
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
    get_subnet_api_instance,
)
from ..module_utils.v4.network.helpers import get_subnet  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    remove_empty_ip_config,
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

    ip = dict(
        value=dict(type="str"),
        prefix_length=dict(type="int"),
    )

    ipv4_pool_spec = dict(
        start_ip=dict(type="dict", options=ip, obj=net_sdk.IPv4Address),
        end_ip=dict(type="dict", options=ip, obj=net_sdk.IPv4Address),
    )

    ipv4_subnet_spec = dict(
        ip=dict(type="dict", options=ip, obj=net_sdk.IPv4Address),
        prefix_length=dict(type="int"),
    )

    ipv4_config_sub_spec = dict(
        ip_subnet=dict(type="dict", options=ipv4_subnet_spec, obj=net_sdk.IPv4Subnet),
        default_gateway_ip=dict(type="dict", options=ip, obj=net_sdk.IPv4Address),
        dhcp_server_address=dict(type="dict", options=ip, obj=net_sdk.IPv4Address),
        pool_list=dict(
            type="list", elements="dict", options=ipv4_pool_spec, obj=net_sdk.IPv4Pool
        ),
    )

    ipv6_subnet_spec = dict(
        ip=dict(type="dict", options=ip, obj=net_sdk.IPv6Address),
        prefix_length=dict(type="int"),
    )

    ipv6_pool_spec = dict(
        start_ip=dict(type="dict", options=ip, obj=net_sdk.IPv6Address),
        end_ip=dict(type="dict", options=ip, obj=net_sdk.IPv6Address),
    )

    ipv6_config_sub_spec = dict(
        ip_subnet=dict(type="dict", options=ipv6_subnet_spec, obj=net_sdk.IPv6Subnet),
        default_gateway_ip=dict(type="dict", options=ip, obj=net_sdk.IPv6Address),
        dhcp_server_address=dict(type="dict", options=ip, obj=net_sdk.IPv6Address),
        pool_list=dict(
            type="list", elements="dict", options=ipv6_pool_spec, obj=net_sdk.IPv6Pool
        ),
    )

    ip_config_spec = dict(
        ipv4=dict(type="dict", options=ipv4_config_sub_spec, obj=net_sdk.IPv4Config),
        ipv6=dict(type="dict", options=ipv6_config_sub_spec, obj=net_sdk.IPv6Config),
    )

    ip_address = dict(
        ipv4=dict(type="dict", options=ip, obj=net_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ip, obj=net_sdk.IPv6Address),
    )

    dhcp_spec = dict(
        domain_name_servers=dict(
            type="list", elements="dict", options=ip_address, obj=net_sdk.IPAddress
        ),
        domain_name=dict(type="str"),
        tftp_server_name=dict(type="str"),
        boot_file_name=dict(type="str"),
        ntp_servers=dict(
            type="list", elements="dict", options=ip_address, obj=net_sdk.IPAddress
        ),
        search_domains=dict(type="list", elements="str"),
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
        subnet_type=dict(type="str", choices=["OVERLAY", "VLAN"]),
        network_id=dict(type="int"),
        dhcp_options=dict(type="dict", options=dhcp_spec, obj=net_sdk.DhcpOptions),
        ip_config=dict(
            type="list", elements="dict", options=ip_config_spec, obj=net_sdk.IPConfig
        ),
        cluster_reference=dict(type="str"),
        virtual_switch_reference=dict(type="str"),
        vpc_reference=dict(type="str"),
        is_nat_enabled=dict(type="bool"),
        is_external=dict(type="bool"),
        network_function_chain_reference=dict(type="str"),
        is_advanced_networking=dict(type="bool"),
        hypervisor_type=dict(type="str"),
        ip_prefix=dict(type="str"),
        metadata=dict(type="dict", options=metadata_spec, obj=net_sdk.Metadata),
    )

    return module_args


def create_subnet(module, result):
    subnets = get_subnet_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = net_sdk.Subnet()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create subnets Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = subnets.create_subnet(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating subnet",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.SUBNET
        )
        if ext_id:
            resp = get_subnet(module, subnets, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_subnets_idempotency(old_spec, update_spec):
    if old_spec != update_spec:
        return False
    return True


def update_subnet(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    subnets = get_subnet_api_instance(module)
    current_spec = get_subnet(module, subnets, ext_id=ext_id)
    remove_empty_ip_config(current_spec)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating subnets update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    # check for idempotency
    if check_subnets_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    subnets = get_subnet_api_instance(module)
    try:
        resp = subnets.update_subnet_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating subnet",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_subnet(module, subnets, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_subnet(module, result):
    subnets = get_subnet_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Subnet with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_subnet(module, subnets, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("unable to fetch etag for deleting subnet", **result)

    kwargs = {"if_match": etag}

    try:
        resp = subnets.delete_subnet_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting subnet",
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
            (
                "state",
                "present",
                ("ext_id", "cluster_reference", "vpc_reference"),
                True,
            ),
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
            update_subnet(module, result)
        else:
            create_subnet(module, result)
    else:
        delete_subnet(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
