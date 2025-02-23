#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_pc_restore_v2
short_description: Restores a domain manager from a cluster or object store backup location.
version_added: 2.1.0
description:
    - The restore domain manager is a task-driven operation to restore a domain manager
        from a cluster or object store backup location based on the selected restore point.
options:
    ext_id:
        description:
            - Restore point ID for the backup created in cluster/object store.
        type: str
        required: True
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        required: False
    restore_source_ext_id:
        description: A unique identifier obtained from the restore source API that corresponds to the details provided for the restore source.
        type: str
        required: True
    restorable_domain_manager_ext_id:
        description: External ID of the domain manager.
        type: str
        required: True
    domain_manager:
        description: Domain manager (Prism Central) details.
        type: dict
        required: True
        suboptions:
            config:
                description: Domain manager (Prism Central) cluster configuration details.
                type: dict
                required: true
                suboptions:
                    should_enable_lockdown_mode:
                        description: A boolean value indicating whether to enable lockdown mode for a cluster.
                        type: bool
                        required: false
                    build_info:
                        description: Currently representing the build information to be used for the cluster creation.
                        type: dict
                        required: true
                        suboptions:
                            version:
                                description: Software version.
                                type: str
                                required: false
                    name:
                        description: Name of the domain manager (Prism Central).
                        type: str
                        required: true
                    size:
                        description: Domain manager (Prism Central) size is an enumeration of starter, small, large, or extra large starter values.
                        type: str
                        required: true
                        choices:
                            - SMALL
                            - LARGE
                            - EXTRALARGE
                            - STARTER
                    resource_config:
                        description:
                            - This configuration is used to provide the resource-related details
                                like container external identifiers, number of VCPUs, memory size, data disk size of the domain manager (Prism Central).
                            - In the case of a multi-node setup, the sum of resources like number of VCPUs, memory size and data disk size are provided.
                        type: dict
                        required: false
                        suboptions:
                            container_ext_ids:
                                description: The external identifier of the container that will be used to create the domain manager (Prism Central) cluster.
                                type: list
                                required: false
                                elements: str
                            data_disk_size_bytes:
                                description: The size of the data disk in bytes.
                                type: int
                                required: false
                            memory_size_bytes:
                                description: The size of the memory in bytes.
                                type: int
                                required: false
                            num_vcpus:
                                description: The number of virtual CPUs.
                                type: int
                                required: false
            network:
                description: Domain manager (Prism Central) network configuration details.
                type: dict
                required: true
                suboptions:
                    external_address:
                        description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                        type: dict
                        required: false
                        suboptions:
                            ipv4:
                                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv4 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                            ipv6:
                                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv6 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                    name_servers:
                        description:
                            - List of name servers on a cluster.
                            - For create operation, only ipv4 address / fqdn values are supported currently.
                        type: list
                        required: true
                        elements: dict
                        suboptions:
                            ipv4:
                                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv4 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                            ipv6:
                                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv6 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                            fqdn:
                                description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: Fully Qualified Domain Name of the Host.
                                        type: str
                                        required: false
                    ntp_servers:
                        description:
                            - List of NTP servers on a cluster
                            - For create operation, only ipv4 address / fqdn values are supported currently.
                        type: list
                        required: true
                        elements: dict
                        suboptions:
                            ipv4:
                                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv4 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv4 address belongs.
                                        type: int
                                        required: false
                                        default: 32
                            ipv6:
                                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: The IPv6 address of the host.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description: The prefix length of the network to which this host IPv6 address belongs.
                                        type: int
                                        required: false
                                        default: 128
                            fqdn:
                                description: A fully qualified domain name that specifies its exact location in the tree hierarchy of the Domain Name System.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description: Fully Qualified Domain Name of the Host.
                                        type: str
                                        required: false
                    internal_networks:
                        description: This configuration is used to internally manage Prism Central network.
                        type: list
                        elements: dict
                        required: false
                        suboptions:
                            default_gateway:
                                description:
                                    - The default gateway of the network.
                                    - An unique address that identifies a device on the internet or a local network
                                        in IPv4/IPv6 format or a Fully Qualified Domain Name.
                                type: dict
                                required: true
                                suboptions:
                                    ipv4:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv4 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv4 address belongs.
                                                type: int
                                                required: false
                                                default: 32
                                    ipv6:
                                        description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv6 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv6 address belongs.
                                                type: int
                                                required: false
                                                default: 128
                                    fqdn:
                                        description: A fully qualified domain name that specifies its exact location
                                            in the tree hierarchy of the Domain Name System.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: Fully Qualified Domain Name of the Host.
                                                type: str
                                                required: false
                            subnet_mask:
                                description:
                                    - The subnet mask of the network.
                                    - An unique address that identifies a device on the internet or a local network in
                                        IPv4/IPv6 format or a Fully Qualified Domain Name.
                                type: dict
                                required: true
                                suboptions:
                                    ipv4:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv4 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv4 address belongs.
                                                type: int
                                                required: false
                                                default: 32
                                    ipv6:
                                        description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv6 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv6 address belongs.
                                                type: int
                                                required: false
                                                default: 128
                                    fqdn:
                                        description: A fully qualified domain name that specifies its exact location
                                            in the tree hierarchy of the Domain Name System.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: Fully Qualified Domain Name of the Host.
                                                type: str
                                                required: false
                            ip_ranges:
                                description: Range of IPs used for Prism Central network setup.
                                type: list
                                required: true
                                elements: dict
                                suboptions:
                                    begin:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            ipv4:
                                                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                                type: dict
                                                required: false
                                                suboptions:
                                                    value:
                                                        description: The IPv4 address of the host.
                                                        type: str
                                                        required: true
                                                    prefix_length:
                                                        description: The prefix length of the network to which this host IPv4 address belongs.
                                                        type: int
                                                        required: false
                                                        default: 32
                                            ipv6:
                                                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                                type: dict
                                                required: false
                                                suboptions:
                                                    value:
                                                        description: The IPv6 address of the host.
                                                        type: str
                                                        required: true
                                                    prefix_length:
                                                        description: The prefix length of the network to which this host IPv6 address belongs.
                                                        type: int
                                                        required: false
                                                        default: 128
                                    end:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            ipv4:
                                                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                                type: dict
                                                required: false
                                                suboptions:
                                                    value:
                                                        description: The IPv4 address of the host.
                                                        type: str
                                                        required: true
                                                    prefix_length:
                                                        description: The prefix length of the network to which this host IPv4 address belongs.
                                                        type: int
                                                        required: false
                                                        default: 32
                                            ipv6:
                                                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                                type: dict
                                                required: false
                                                suboptions:
                                                    value:
                                                        description: The IPv6 address of the host.
                                                        type: str
                                                        required: true
                                                    prefix_length:
                                                        description: The prefix length of the network to which this host IPv6 address belongs.
                                                        type: int
                                                        required: false
                                                        default: 128
                    external_networks:
                        description: This configuration is used to manage Prism Central.
                        type: list
                        elements: dict
                        required: true
                        suboptions:
                            default_gateway:
                                description:
                                    - The default gateway of the network.
                                    - An unique address that identifies a device on the internet or a local network in
                                        IPv4/IPv6 format or a Fully Qualified Domain Name.
                                type: dict
                                required: true
                                suboptions:
                                    ipv4:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv4 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv4 address belongs.
                                                type: int
                                                required: false
                                                default: 32
                                    ipv6:
                                        description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv6 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv6 address belongs.
                                                type: int
                                                required: false
                                                default: 128
                                    fqdn:
                                        description: A fully qualified domain name that specifies its exact location
                                            in the tree hierarchy of the Domain Name System.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: Fully Qualified Domain Name of the Host.
                                                type: str
                                                required: false
                            subnet_mask:
                                description:
                                    - The subnet mask of the network.
                                    - An unique address that identifies a device on the internet or a local network in
                                        IPv4/IPv6 format or a Fully Qualified Domain Name.
                                type: dict
                                required: true
                                suboptions:
                                    ipv4:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv4 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv4 address belongs.
                                                type: int
                                                required: false
                                                default: 32
                                    ipv6:
                                        description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: The IPv6 address of the host.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description: The prefix length of the network to which this host IPv6 address belongs.
                                                type: int
                                                required: false
                                                default: 128
                                    fqdn:
                                        description: A fully qualified domain name that specifies its exact location
                                            in the tree hierarchy of the Domain Name System.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description: Fully Qualified Domain Name of the Host.
                                                type: str
                                                required: false
                            ip_ranges:
                                description: Range of IPs used for Prism Central network setup.
                                type: list
                                required: true
                                elements: dict
                                suboptions:
                                    begin:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            ipv4:
                                                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                                type: dict
                                                required: false
                                                suboptions:
                                                    value:
                                                        description: The IPv4 address of the host.
                                                        type: str
                                                        required: true
                                                    prefix_length:
                                                        description: The prefix length of the network to which this host IPv4 address belongs.
                                                        type: int
                                                        required: false
                                                        default: 32
                                            ipv6:
                                                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                                type: dict
                                                required: false
                                                suboptions:
                                                    value:
                                                        description: The IPv6 address of the host.
                                                        type: str
                                                        required: true
                                                    prefix_length:
                                                        description: The prefix length of the network to which this host IPv6 address belongs.
                                                        type: int
                                                        required: false
                                                        default: 128
                                    end:
                                        description: An unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
                                        type: dict
                                        required: false
                                        suboptions:
                                            ipv4:
                                                description: An unique address that identifies a device on the internet or a local network in IPv4 format.
                                                type: dict
                                                required: false
                                                suboptions:
                                                    value:
                                                        description: The IPv4 address of the host.
                                                        type: str
                                                        required: true
                                                    prefix_length:
                                                        description: The prefix length of the network to which this host IPv4 address belongs.
                                                        type: int
                                                        required: false
                                                        default: 32
                                            ipv6:
                                                description: An unique address that identifies a device on the internet or a local network in IPv6 format.
                                                type: dict
                                                required: false
                                                suboptions:
                                                    value:
                                                        description: The IPv6 address of the host.
                                                        type: str
                                                        required: true
                                                    prefix_length:
                                                        description: The prefix length of the network to which this host IPv6 address belongs.
                                                        type: int
                                                        required: false
                                                        default: 128
                            network_ext_id:
                                description: The network external identifier to which Domain Manager (Prism Central) is to be deployed or is already configured.
                                type: str
                                required: true
            should_enable_high_availability:
                description: This configuration enables Prism Central to be deployed in scale-out mode.
                type: bool
                required: false
                default: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - Prem Karat (@premkarat)
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Restore PC
  nutanix.ncp.ntnx_pc_restore_v2:
    nutanix_host: <pe_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "95148523-1234-5678-9090-ac1f6b6f97e2"
    restore_source_ext_id: "84125478-6543-2131-5678-ac1f6b6f97e2"
    restorable_domain_manager_ext_id: "54678987-1222-5678-9090-ac1f6b6f97e2"
    domain_manager:
      config:
        should_enable_lockdown_mode: false
        build_info:
          version: "pc.2024.3"
        name: "PC_10.0.0.2"
        size: "SMALL"
        resource_config:
          data_disk_size_bytes: "536870912000"
          memory_size_bytes: "37580963840"
          num_vcpus: "10"
          container_ext_ids: ["6171a26e-7d08-4f10-b6fa-9304b333f6b6"]
      network:
        external_address:
          ipv4:
            value: "10.0.0.3"
        name_servers:
          - ipv4:
              value: "10.0.0.5"
          - ipv4:
              value: "10.0.0.6"
        ntp_servers:
          - fqdn:
              value: "1.example.org"
          - fqdn:
              value: "2.example.org"
          - fqdn:
              value: "3.example.org"
          - fqdn:
              value: "4.example.org"
        external_networks:
          - network_ext_id: "54678987-1764-3478-8050-ac1f6b6f97e2"
            default_gateway:
              ipv4:
                value: "10.0.0.0"
            subnet_mask:
              ipv4:
                value: "255.255.252.0"
            ip_ranges:
              - begin:
                  ipv4:
                    value: "10.1.1.1"
                end:
                  ipv4:
                    value: "10.1.1.1"
  register: result
"""

RETURN = r"""
response:
    description:
        - Task response for restoring a domain manager from a cluster or object store backup location.
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_ids": [
                "00062cd6-4569-8745-3655-ac1f6b6f97e2"
            ],
            "completed_time": "2025-01-30T07:24:37.119256+00:00",
            "completion_details": null,
            "created_time": "2025-01-30T05:54:29.372442+00:00",
            "entities_affected": [
                {
                    "ext_id": "cfddac63-aaaa-wwww-1qaa-54abf89ce234",
                    "name": "prism_central",
                    "rel": "prism:config:domain_manager"
                },
                {
                    "ext_id": "00062cd6-gggg-tred-5433-ac1f6b6f97e2",
                    "name": null,
                    "rel": "clustermgmt:config:cluster"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:45697502-d91c-9632-65e7-68f2b6e279bf",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2025-01-30T07:24:37.119251+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 2,
            "number_of_subtasks": 4,
            "operation": "kPcRecovery",
            "operation_description": "Prism Central Recovery",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2025-01-30T05:54:29.381981+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:1db87069-dbf8-43b8-7b96-86195e16f1c5",
                    "href": "https://10.46.136.32:9440/api/prism/v4.0/config/tasks/ZXJnb24=:1db87069-dbf8-43b8-7b96-86195e16f1c5",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:3b5cea6c-933b-4239-4b9a-6730624546a9",
                    "href": "https://10.46.136.32:9440/api/prism/v4.0/config/tasks/ZXJnb24=:3b5cea6c-933b-4239-4b9a-6730624546a9",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:3c21bde8-606b-4a60-5ce5-aa5b655bd2eb",
                    "href": "https://10.46.136.32:9440/api/prism/v4.0/config/tasks/ZXJnb24=:3c21bde8-606b-4a60-5ce5-aa5b655bd2eb",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:7c98313d-ac92-4963-7f95-9d434cdd726f",
                    "href": "https://10.46.136.32:9440/api/prism/v4.0/config/tasks/ZXJnb24=:7c98313d-ac92-4963-7f95-9d434cdd726f",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }

task_ext_id:
    description: The external identifier of the task.
    returned: always
    type: str
    sample: ZXJnb24=:45697502-d91c-9632-65e7-68f2b6e279bf

restore_source_ext_id:
    description: Restore source external identifier.
    returned: always
    type: str
    sample: 84125478-6543-2131-5678-ac1f6b6f97e2

restorable_domain_manager_ext_id:
    description: Restorable domain manager external identifier.
    returned: always
    type: str
    sample: 54678987-1222-5678-9090-ac1f6b6f97e2

ext_id:
    description: Restore point extetrnal identifier.
    returned: always
    type: str
    sample: 54678987-1222-5678-9090-ac1f6b6f97e2

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str
    sample: false

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_backup_api_instance,
)
from ..module_utils.v4.prism.spec.pc import PrismSpecs as prism_specs  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        restore_source_ext_id=dict(type="str", required=True),
        restorable_domain_manager_ext_id=dict(type="str", required=True),
        domain_manager=dict(
            type="dict",
            options=prism_specs.prism_spec,
            obj=prism_sdk.DomainManager,
            required=True,
        ),
    )
    return module_args


def restore_domain_manager(module, result):
    sg = SpecGenerator(module)
    default_spec = prism_sdk.RestoreSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    domain_manager_api = get_domain_manager_backup_api_instance(module)
    restore_source_ext_id = module.params.get("restore_source_ext_id")
    restorable_domain_manager_ext_id = module.params.get(
        "restorable_domain_manager_ext_id"
    )
    ext_id = module.params.get("ext_id")
    result["restore_source_ext_id"] = restore_source_ext_id
    result["restorable_domain_manager_ext_id"] = restorable_domain_manager_ext_id
    result["ext_id"] = ext_id
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating restore domain manager spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = domain_manager_api.restore(
            restoreSourceExtId=restore_source_ext_id,
            restorableDomainManagerExtId=restorable_domain_manager_ext_id,
            extId=ext_id,
            body=spec,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while restoring domain manager",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    restore_domain_manager(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
