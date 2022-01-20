#!/usr/bin/python

# Copyright: (c) 2021
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ..module_utils.base_module import BaseModule
from ..module_utils.prism.vms import VM

__metaclass__ = type

DOCUMENTATION = r"""
---
module: nutanix_vms

short_description: This module allows to communicate with the resource /vms

version_added: "1.0.0"

description: This module allows to perform the following tasks on /vms

options:
    action:
        description: This is the HTTP action used to indicate the type of request
        required: true
        type: str
    credentials:
        description: Credentials needed for authenticating to the subnet
        required: true
        type: dict (Variable from file)
    data:
        description: This acts as either the params or the body payload depending on the HTTP action
        required: false
        type: dict
    operation:
        description: This acts as the sub_url in the requested url
        required: false
        type: str
    ip_address:
        description: This acts as the ip_address of the subnet. It can be passed as a list in ansible using with_items
        required: True
        type: str

author:
 - Gevorg Khachatryan (@gevorg_khachatryan)
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""


def run_module():
    BaseModule.argument_spec.update(
        dict(
            spec__name=dict(type="str", required=False, aliases=["name"]),
            spec__description=dict(
                type="str", required=False, aliases=["desc", "description"]
            ),
            metadata__uuid=dict(type="str", aliases=["uuid"], required=False),
            spec__resources__num_sockets=dict(
                type="int", default=1, aliases=["core_count", "vcpus"]
            ),
            spec__resources__num_threads_per_core=dict(
                type="int", aliases=["threads_per_core"]  # default=1,#will not provide
            ),
            spec__resources__num_vcpus_per_socket=dict(
                type="int",
                default=1,
                aliases=["num_vcpus_per_socket", "cores_per_vcpu"],
            ),
            cluster=dict(
                type="dict",
                default={},
                options=dict(
                    spec__cluster_reference__uuid=dict(
                        type="str", aliases=["cluster_uuid", "uuid"], required=False
                    ),
                    spec__cluster_reference__name=dict(
                        type="str", aliases=["cluster_name", "name"], required=False
                    ),
                    spec__cluster_reference__kind=dict(
                        type="str",
                        aliases=["cluster_kind"],
                        required=False,
                        default="cluster",
                    ),
                ),
            ),
            spec__resources__nic_list=dict(
                type="list",
                aliases=["networks"],
                elements="dict",
                options=dict(
                    uuid=dict(type="str", aliases=["nic_uuid"]),
                    subnet_uuid=dict(type="str"),
                    subnet_name=dict(type="str"),
                    subnet_kind=dict(type="str", default="subnet"),
                    is_connected=dict(
                        type="bool", aliases=["connected"], default=False
                    ),
                    ip_endpoint_list=dict(
                        type="list", aliases=["private_ip"], default=[]
                    ),
                    nic_type=dict(type="str", default="NORMAL_NIC"),
                ),
                default=[],
            ),
            spec__resources__disk_list=dict(
                type="list",
                aliases=["disks"],
                options=dict(
                    type=dict(type="str"),
                    size_gb=dict(type="int"),
                    bus=dict(type="str"),
                    storage_config=dict(
                        type=dict,
                        aliases=["storage_container"],
                        options=dict(
                            storage_container_name=dict(type="str"),
                            storage_container_uuid=dict(type="str", aliases=["uuid"]),
                        ),
                    ),
                ),
                default=[],
            ),
            spec__resources__hardware_clock_timezone=dict(
                type="str", default="UTC", aliases=["timezone"]
            ),
            spec__resources__boot_config__boot_type=dict(
                type="str", default="LEGACY", aliases=["boot_type"]
            ),
            spec__resources__boot_config__boot_device_order_list=dict(
                type="list",
                default=["CDROM", "DISK", "NETWORK"],
                aliases=["boot_device_order_list"],
            ),
            spec__resources__memory_overcommit_enabled=dict(
                type="bool", default=False, aliases=["memory_overcommit_enabled"]
            ),
            spec__resources__memory_size_mib=dict(
                type="int", default=1, aliases=["memory_size_mib", "memory_gb"]
            ),
            metadata__categories_mapping=dict(type="dict", aliases=["categories"]),
            metadata__use_categories_mapping=dict(
                type="bool", aliases=["use_categories_mapping"], default=False
            ),
        )
    )

    module = BaseModule()
    if module.params.get("spec__resources__memory_size_mib"):
        module.params["spec__resources__memory_size_mib"] = (
            module.params["spec__resources__memory_size_mib"] * 1024
        )
    if module.params.get("metadata__categories_mapping"):
        module.params["metadata__use_categories_mapping"] = True
    VM(module)


def main():
    run_module()


if __name__ == "__main__":
    main()
