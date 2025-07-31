#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ova_deploy_vm_v2
short_description: "Deploy VM from an ova"
version_added: 2.3.0
description:
    - Deploy a VM from an OVA.
    - This module uses PC v4 APIs based SDKs.
options:
    ext_id:
        description:
            - External ID of the OVA used to deploy VM.
        type: str
        required: true
    override_vm_config:
        description:
            - VM config override spec for OVA VM deploy endpoint.
        type: dict
        options:
            name:
                description: Name of the VM.
                type: str
            num_sockets:
                description: Number of vCPU sockets.
                type: int
            num_cores_per_socket:
                description: Number of cores per socket for the VM.
                type: int
            num_threads_per_core:
                description: Number of threads per core for the VM.
                type: int
            memory_size_bytes:
                description: Memory size in bytes for the VM.
                type: int
            nics:
                description:
                    - The list of NICs for the VM.
                required: true
                type: list
                elements: dict
                suboptions:
                    backing_info:
                        description:
                            - The backing information for the NIC.
                        type: dict
                        suboptions:
                            model:
                                description:
                                    - The model of the NIC.
                                type: str
                                choices:
                                    - VIRTIO
                                    - E1000
                                required: false
                            mac_address:
                                description:
                                    - The MAC address of the NIC.
                                type: str
                                required: false
                            is_connected:
                                description:
                                    - Whether the NIC needs to be connected or not.
                                type: bool
                                required: false
                            num_queues:
                                description:
                                    - The number of queues for the NIC.
                                type: int
                                required: false
                    network_info:
                        description:
                            - The network configuration for the NIC.
                        type: dict
                        suboptions:
                            nic_type:
                                description:
                                    - The type of the NIC.
                                type: str
                                choices:
                                    - NORMAL_NIC
                                    - DIRECT_NIC
                                    - NETWORK_FUNCTION_NIC
                                    - SPAN_DESTINATION_NIC
                                required: false
                            network_function_chain:
                                description:
                                    - The network function chain for the NIC.
                                type: dict
                                suboptions:
                                    ext_id:
                                        description:
                                            - The external ID of the network function chain.
                                        type: str
                                        required: true
                                required: false
                            network_function_nic_type:
                                description:
                                    - The type of the network function NIC.
                                type: str
                                choices:
                                    - INGRESS
                                    - EGRESS
                                    - TAP
                                required: false
                            subnet:
                                description:
                                    - The subnet for the NIC.
                                type: dict
                                suboptions:
                                    ext_id:
                                        description:
                                            - The external ID of the subnet.
                                        type: str
                                        required: true
                                required: false
                            vlan_mode:
                                description:
                                    - The VLAN mode for the NIC.
                                type: str
                                choices:
                                    - ACCESS
                                    - TRUNK
                                required: false
                            trunked_vlans:
                                description:
                                    - The trunked VLANs for the NIC.
                                type: list
                                elements: int
                                required: false
                            should_allow_unknown_macs:
                                description:
                                    - Whether to allow unknown MAC addresses or not.
                                type: bool
                                required: false
                            ipv4_config:
                                description:
                                    - The IPv4 configuration for the NIC.
                                type: dict
                                suboptions:
                                    should_assign_ip:
                                        description:
                                            - Whether to assign an IP address or not.
                                        type: bool
                                        required: false
                                    ip_address:
                                        description:
                                            - The IP address for the NIC.
                                        type: dict
                                        suboptions:
                                            value:
                                                description:
                                                    - The IP address value.
                                                type: str
                                                required: True
                                            prefix_length:
                                                description:
                                                    - The prefix length for the IP address.
                                                    - Can be skipped, default it will be 32.
                                                type: int
                                                required: false
                                    secondary_ip_address_list:
                                        description:
                                            - The list of secondary IP addresses for the NIC.
                                        type: list
                                        elements: dict
                                        suboptions:
                                            value:
                                                description:
                                                    - The IP address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - The prefix length for the IP address.
                                                    - Can be skipped, default it will be 32.
                                                type: int
                                                required: false
                                required: false
            cd_roms:
                description:
                    - The list of CD-ROMs for the VM.
                required: false
                type: list
                elements: dict
                suboptions:
                    backing_info:
                        description:
                            - Storage provided by Nutanix ADSF
                        type: dict
                        suboptions:
                            disk_size_bytes:
                                description:
                                    - The size of the CDROM in bytes.
                                type: int
                            storage_container:
                                description:
                                    - The storage container reference.
                                type: dict
                                suboptions:
                                    ext_id:
                                        description:
                                            - The external ID of the storage container.
                                        type: str
                                        required: true
                            storage_config:
                                description:
                                    - The storage configuration.
                                type: dict
                                suboptions:
                                    is_flash_mode_enabled:
                                        description:
                                            - Indicates whether the virtual disk is pinned to the hot tier or not.
                                        type: bool
                            data_source:
                                description:
                                    - The data source for the disk.
                                type: dict
                                suboptions:
                                    reference:
                                        description:
                                            - The reference to the data source.
                                        type: dict
                                        suboptions:
                                            image_reference:
                                                description:
                                                    - The reference to an image.
                                                    - Mutually exclusive with C(vm_disk_reference).
                                                type: dict
                                                suboptions:
                                                    image_ext_id:
                                                        description:
                                                            - The external ID of the image.
                                                        type: str
                                            vm_disk_reference:
                                                description:
                                                    - The reference to a VM disk.
                                                    - Mutually exclusive with C(image_reference).
                                                type: dict
                                                suboptions:
                                                    disk_ext_id:
                                                        description:
                                                            - The external ID of the VM disk.
                                                        type: str
                                                    disk_address:
                                                        description:
                                                            - The address of the disk.
                                                        type: dict
                                                        suboptions:
                                                            bus_type:
                                                                description:
                                                                    - The bus type of the disk.
                                                                type: str
                                                                required: true
                                                                choices:
                                                                    - 'SCSI'
                                                                    - 'IDE'
                                                                    - 'PCI'
                                                                    - 'SATA'
                                                                    - 'SPAPR'
                                                            index:
                                                                description:
                                                                    - The index of the disk.
                                                                type: int
                                                    vm_reference:
                                                        description:
                                                            - The reference to the VM.
                                                        type: dict
                                                        suboptions:
                                                            ext_id:
                                                                description:
                                                                    - The external ID of the VM.
                                                                type: str
                                                                required: true
            categories:
                description:
                    - The list of categories for the VM.
                required: false
                type: list
                elements: dict
                suboptions:
                    ext_id:
                        description:
                            - The external ID of the category.
                        required: true
                        type: str
            wait:
                description:
                    - Whether to wait for the task to complete.
                required: false
                type: bool
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Deploy VM from Ova
  nutanix.ncp.ntnx_ova_deploy_vm_v2:
    ext_id: "79b8f0c2-1d3e-4c5a-9f6b-7d8e9f0a1b2c"
    override_vm_config:
      nics:
        - backing_info:
            is_connected: true
          network_info:
            nic_type: "NORMAL_NIC"
            subnet:
              ext_id: "12345678-1234-1234-1234-123456789012"
            vlan_mode: "ACCESS"
    cluster_location_ext_id: "000636a4-e7ce-389e-185b-ac1f6b6f97e2"
  register: result
"""

RETURN = r"""
response:
    description: 
        - The response from the Nutanix API after deploying the VM from the OVA.
        - VM details if C(wait) is true.
        - Task details if C(wait) is false.
    type: dict
    returned: always
    sample:
        {
            "apc_config": {
                "cpu_model": null,
                "is_apc_enabled": false
            },
            "availability_zone": null,
            "bios_uuid": "ae577c01-f7ce-4fed-772e-dc012fcbb5ea",
            "boot_config": {
                "boot_device": null,
                "boot_order": [
                    "CDROM",
                    "DISK",
                    "NETWORK"
                ]
            },
            "categories": null,
            "cd_roms": null,
            "cluster": {
                "ext_id": "00063a1c-a953-2048-0000-000000028f57"
            },
            "create_time": "2025-07-29T09:54:09.819114+00:00",
            "description": "ansible test ova",
            "disks": null,
            "enabled_cpu_features": null,
            "ext_id": "ae577c01-f7ce-4fed-772e-dc012fcbb5ea",
            "generation_uuid": "f78ffa80-3f99-4693-bf24-a4e7c8c9f4f0",
            "gpus": null,
            "guest_customization": null,
            "guest_tools": null,
            "hardware_clock_timezone": "UTC",
            "host": null,
            "is_agent_vm": false,
            "is_branding_enabled": true,
            "is_cpu_hotplug_enabled": true,
            "is_cpu_passthrough_enabled": false,
            "is_cross_cluster_migration_in_progress": false,
            "is_gpu_console_enabled": false,
            "is_live_migrate_capable": true,
            "is_memory_overcommit_enabled": false,
            "is_scsi_controller_enabled": true,
            "is_vcpu_hard_pinning_enabled": false,
            "is_vga_console_enabled": true,
            "links": null,
            "machine_type": "PC",
            "memory_size_bytes": 1073741824,
            "name": "HuuzuTMvSlsZansible-agvm",
            "nics": [
                {
                    "backing_info": {
                        "is_connected": true,
                        "mac_address": "50:6b:8d:f5:3b:de",
                        "model": null,
                        "num_queues": 1
                    },
                    "ext_id": "009a3dac-f658-41fc-8def-7aaba6f46248",
                    "links": null,
                    "network_info": {
                        "ipv4_config": null,
                        "ipv4_info": null,
                        "network_function_chain": null,
                        "network_function_nic_type": null,
                        "nic_type": "NORMAL_NIC",
                        "should_allow_unknown_macs": null,
                        "subnet": {
                            "ext_id": "99a0e219-ac21-4ba5-93dd-a4f2ac889d27"
                        },
                        "trunked_vlans": null,
                        "vlan_mode": "ACCESS"
                    },
                    "nic_backing_info": {
                        "is_connected": true,
                        "mac_address": "50:6b:8d:f5:3b:de",
                        "model": null,
                        "num_queues": 1
                    },
                    "nic_network_info": {
                        "ipv4_config": null,
                        "ipv4_info": null,
                        "ipv6_info": null,
                        "network_function_chain": null,
                        "network_function_nic_type": null,
                        "nic_type": "NORMAL_NIC",
                        "should_allow_unknown_macs": null,
                        "subnet": {
                            "ext_id": "99a0e219-ac21-4ba5-93dd-a4f2ac889d27"
                        },
                        "trunked_vlans": null,
                        "vlan_mode": "ACCESS"
                    },
                    "tenant_id": null
                }
            ],
            "num_cores_per_socket": 1,
            "num_numa_nodes": 0,
            "num_sockets": 2,
            "num_threads_per_core": 1,
            "ownership_info": {
                "owner": {
                    "ext_id": "00000000-0000-0000-0000-000000000000"
                }
            },
            "pcie_devices": null,
            "power_state": "OFF",
            "project": {
                "ext_id": "d6f340a9-e7e1-48c6-89ea-17dc196111af"
            },
            "protection_policy_state": null,
            "protection_type": "UNPROTECTED",
            "serial_ports": null,
            "source": null,
            "storage_config": null,
            "tenant_id": null,
            "update_time": "2025-07-29T09:54:10.235342+00:00",
            "vtpm_config": {
                "is_vtpm_enabled": false,
                "version": null,
                "vtpm_device": null
            }
        }
ext_id: The external ID of the ova used to deploy the VM.
    type: str
    returned: always
    sample: "ae577c01-f7ce-4fed-772e-dc012fcbb5ea"
task_ext_id:
    description: The external ID of the task created for deploying the VM.
    type: str
    returned: when the task is created
    sample: "ZXJnb24=:b520149f-f189-4007-9c56-9c1c40680306"
changed:
    description: Indicates whether the task resulted in any changes.
    type: bool
    returned: always
    sample: true
error:
    description: The error message if an error occurs.
    type: str
    returned: always
vm_ext_id:
    description: The external ID of the VM created from the OVA.
    type: str
    returned: when the VM is created successfully
    sample: "ae577c01-f7ce-4fed-772e-dc012fcbb5ea"
failed:
    description: Indicates whether the task failed.
    type: bool
    returned: always
    sample: false
"""


import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_ova_api_instance,
    get_vm_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402
from ..module_utils.v4.vmm.spec.vms import VmSpecs as vm_specs  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    reference_spec = dict(
        ext_id=dict(type="str"),
    )
    override_vm_config_spec = dict(
        name=dict(type="str"),
        num_sockets=dict(type="int"),
        num_cores_per_socket=dict(type="int"),
        num_threads_per_core=dict(type="int"),
        memory_size_bytes=dict(type="int"),
        nics=dict(
            type="list",
            elements="dict",
            options=vm_specs.get_nic_spec(),
            obj=vmm_sdk.AhvConfigNic,
            required=True,
        ),
        cd_roms=dict(
            type="list",
            elements="dict",
            options=vm_specs.get_cd_rom_spec(),
            obj=vmm_sdk.AhvConfigCdRom,
        ),
        categories=dict(
            type="list",
            elements="dict",
            options=reference_spec,
            obj=vmm_sdk.AhvConfigCategoryReference,
        ),
    )
    module_args = dict(
        ext_id=dict(type="str", required=True),
        override_vm_config=dict(
            type="dict",
            options=override_vm_config_spec,
            obj=vmm_sdk.OvaVmConfigOverrideSpec,
            required=True,
        ),
        cluster_location_ext_id=dict(type="str", required=True),
    )

    return module_args


def deploy_vm_using_ova(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    ova = get_ova_api_instance(module)
    vm = get_vm_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.OvaDeploymentSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating deploy vm using ova spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = ova.deploy_ova(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deploying vm using ova",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        vm_ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.VM
        )
        if vm_ext_id:
            resp = get_vm(module, vm, vm_ext_id)
            result["vm_ext_id"] = vm_ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    deploy_vm_using_ova(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
