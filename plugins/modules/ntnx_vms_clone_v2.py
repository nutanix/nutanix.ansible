#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_clone_v2
short_description: Clone a virtual machine in Nutanix AHV.
version_added: "2.0.0"
description:
    - This module allows you to clone a virtual machine in Nutanix AHV.
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will clone a VM.
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external ID of the VM.
            - Required for cloning VM.
        required: true
        type: str
    name:
        description:
            - VM name.
        required: false
        type: str
    num_sockets:
        description:
            - Number of vCPU sockets.
        required: false
        type: int
    num_cores_per_socket:
        description:
            - Number of cores per socket.
        required: false
        type: int
    num_threads_per_core:
        description:
            - Number of cores per socket.
        required: false
        type: int
    memory_size_bytes:
        description:
            - Memory size in bytes.
        required: false
        type: int
    nics:
        description:
            - NICs attached to the VM.
        required: false
        type: list
        elements: dict
        suboptions:
            backing_info:
                description:
                    - The backing information for the NIC.
                    - Deprecated, use C(nic_backing_info) instead.
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
            nic_backing_info:
                description:
                    - Backing Information about how NIC is associated with a VM.
                type: dict
                suboptions:
                    virtual_ethernet_nic:
                        description:
                            - The virtual ethernet NIC information.
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
                    - Deprecated, use C(nic_network_info) instead.
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
            nic_network_info:
                description:
                    - Network configuration for the NIC.
                type: dict
                suboptions:
                    virtual_ethernet_nic_network_info:
                        description:
                            - The network configuration for the virtual ethernet NIC.
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
                required: false
    boot_config:
        description:
            - Indicates the order of device types in which the VM should try to boot from.
              If the boot device order is not provided the system will decide an appropriate boot device order.
        required: false
        type: dict
        suboptions:
            legacy_boot:
                description:
                    - The legacy boot configuration.
                required: false
                type: dict
                suboptions:
                    boot_device:
                        description:
                            - The boot device for legacy boot.
                        type: dict
                        suboptions:
                            boot_device_disk:
                                description: Specification for booting from disk.
                                type: dict
                                suboptions:
                                    disk_address:
                                        description: Address specification for the disk.
                                        type: dict
                                        suboptions:
                                            bus_type:
                                                description: Bus type for the device. The acceptable values are SCSI, IDE, PCI, SATA, SPAPR (only PPC).
                                                type: str
                                                choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                required: true
                                            index:
                                                description: Device index on the bus. This field is ignored unless the bus details are specified.
                                                type: int
                            boot_device_nic:
                                description: Specification for booting from network interface controller (NIC).
                                type: dict
                                suboptions:
                                        mac_address:
                                                description: Mac address
                                                type: str
                    boot_order:
                        description:
                            - Indicates the order of device types in which the VM should try to boot from.
                              If the boot device order is not provided the system will decide an appropriate boot device order.
                        type: list
                        elements: str
                        choices: ["CDROM", "DISK", "NETWORK"]
            uefi_boot:
                description:
                    - The UEFI boot configuration.
                required: false
                type: dict
                suboptions:
                    boot_device:
                        description:
                            - The boot device settings for UEFI boot.
                        type: dict
                        suboptions:
                            boot_device_disk:
                                description: Specification for booting from disk.
                                type: dict
                                suboptions:
                                    disk_address:
                                        description: Address specification for the disk.
                                        type: dict
                                        suboptions:
                                            bus_type:
                                                description:
                                                    - Bus type for the device.
                                                    - The acceptable values are SCSI, IDE, PCI, SATA, SPAPR (only PPC).
                                                type: str
                                                choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                required: true
                                            index:
                                                description:
                                                    - Device index on the bus.
                                                    - This field is ignored unless the bus details are specified.
                                                type: int
                            boot_device_nic:
                                description: Specification for booting from network interface controller (NIC).
                                type: dict
                                suboptions:
                                        mac_address:
                                                description: Mac address
                                                type: str
                    boot_order:
                        description:
                            - Indicates the order of device types in which the VM should try to boot from.
                              If the boot device order is not provided the system will decide an appropriate boot device order.
                        type: list
                        elements: str
                        choices: ["CDROM", "DISK", "NETWORK"]
                    is_secure_boot_enabled:
                        description: Indicate whether to enable secure boot or not.
                        type: bool
                    nvram_device:
                        description: Configuration for NVRAM to be presented to the VM.
                        type: dict
                        suboptions:
                            backing_storage_info:
                                description: Storage provided by Nutanix ADSF
                                type: dict
                                suboptions:
                                    disk_size_bytes:
                                        description: Size of the disk in Bytes
                                        type: int
                                    storage_container:
                                        description:
                                            - This reference is for disk level storage container preference.
                                              This preference specifies the storage container to which this disk belongs.
                                        type: dict
                                        suboptions:
                                            ext_id:
                                                description:
                                                    - The globally unique identifier of a VM disk container. It should be of type UUID.
                                                required: true
                                                type: str
                                    storage_config:
                                        description: Storage configuration for VM disks.
                                        type: dict
                                        suboptions:
                                            is_flash_mode_enabled:
                                                description: Indicates whether the virtual disk is pinned to the hot tier or not.
                                                type: bool
                                    data_source:
                                        description: A reference to a disk or image that contains the contents of a disk.
                                        type: dict
                                        suboptions:
                                            reference:
                                                description: Reference to the data source, mutually exclusive with either image_reference or vm_disk_reference.
                                                type: dict
                                                suboptions:
                                                        image_reference:
                                                            description: Reference to an image.
                                                            type: dict
                                                            suboptions:
                                                                image_ext_id:
                                                                    description: The globally unique identifier of an image. It should be of type UUID.
                                                                    type: str
                                                        vm_disk_reference:
                                                            description: Reference to a virtual machine disk.
                                                            type: dict
                                                            suboptions:
                                                                disk_ext_id:
                                                                    description: The globally unique identifier of a VM disk. It should be of type UUID.
                                                                    type: str
                                                                disk_address:
                                                                    description: The address of the disk.
                                                                    type: dict
                                                                    suboptions:
                                                                        bus_type:
                                                                            description:
                                                                                - Bus type for the device. The acceptable values
                                                                                  are SCSI, IDE, PCI, SATA, SPAPR (only PPC).
                                                                            type: str
                                                                            required: true
                                                                            choices: ["SCSI", "IDE", "PCI", "SATA", "SPAPR"]
                                                                        index:
                                                                            description:
                                                                                - Device index on the bus.
                                                                                  This field is ignored unless the bus details are specified.
                                                                            type: int
                                                                vm_reference:
                                                                    description: This is a reference to a VM.
                                                                    type: dict
                                                                    suboptions:
                                                                        ext_id:
                                                                            description:
                                                                                - The globally unique identifier of a VM. It should be of type UUID.
                                                                            required: true
                                                                            type: str

    guest_customization:
        description:
            - Stage a Sysprep or cloud-init configuration file to be used by the guest for the next boot.
              Note that the Sysprep command must be used to generalize the Windows VMs before triggering this API call.
        required: false
        type: dict
        suboptions:
            config:
                description:
                    - The Nutanix Guest Tools customization settings.
                required: false
                type: dict
                suboptions:
                    sysprep:
                        description:
                            - sysprep config
                        required: false
                        type: dict
                        suboptions:
                            install_type:
                                description:
                                    - Indicates whether the guest will be freshly installed using this unattend configuration,
                                      or this unattend configuration will be applied to a pre-prepared image.
                                type: str
                                choices: ["FRESH", "PREPARED"]
                            sysprep_script:
                                description: Sysprep script configuration.
                                type: dict
                                suboptions:
                                    unattendxml:
                                        description: Configuration for Unattend XML.
                                        type: dict
                                        suboptions:
                                            value:
                                                description: The Vales of the field
                                                type: str
                                    custom_key_values:
                                        description: Custom key-value pairs for system preparation.
                                        type: dict
                                        suboptions:
                                            key_value_pairs:
                                                description: The list of the individual KeyValuePair elements.
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    name:
                                                        description: Key Name
                                                        type: str
                                                    value:
                                                        description: Key Value
                                                        type: raw
                    cloudinit:
                        description:
                            - cloudinit
                        required: false
                        type: dict
                        suboptions:
                            datasource_type:
                                description:
                                    - The type of the data source.
                                    - Required when using user_data.
                                type: str
                                choices: ["CONFIG_DRIVE_V2"]
                            metadata:
                                description: Metadata configuration.
                                type: str
                            cloud_init_script:
                                description: Cloud init script configuration.
                                type: dict
                                suboptions:
                                    user_data:
                                        description: User data for cloud-init.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - base64 encoded cloud init script.
                                                type: str
                                                required: true
                                    custom_key_values:
                                        description: Custom key-value pairs for cloud-init.
                                        type: dict
                                        suboptions:
                                            key_value_pairs:
                                                description: The list of the individual KeyValuePair elements.
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    name:
                                                        description: Key Name
                                                        type: str
                                                    value:
                                                        description: Key Value
                                                        type: raw
                                                        required: false
    wait:
        description:
            - Whether to wait for the clone operation to complete.
        required: false
        type: bool
        default: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Clone VM with same attributes values
  nutanix.ncp.ntnx_vms_clone_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "de84a538-32bf-4a42-913b-340540af18fd"
    name: "cloned_VM"

- name: Clone VM with different attributes values
  nutanix.ncp.ntnx_vms_clone_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "de84a538-32bf-4a42-913b-340540af18fd"
    name: "cloned_VM"
    num_sockets: 2
    num_cores_per_socket: 2
    num_threads_per_core: 2
"""

RETURN = r"""
response:
    description:
        - If C(wait) is true, then it will give cloned vm details. Else it will be task details
        - It will have the new cloned VM details.
    type: dict
    returned: always
    sample: {
            "apc_config": {
                "cpu_model": null,
                "is_apc_enabled": false
            },
            "availability_zone": null,
            "bios_uuid": "14e05447-fd70-4348-4a69-ec90f427f638",
            "boot_config": {
                "boot_device": null,
                "boot_order": [
                    "CDROM",
                    "DISK",
                    "NETWORK"
                ]
            },
            "categories": [
                {
                    "ext_id": "eb8b4155-b3d1-5772-8d2f-d566d43d8e46"
                }
            ],
            "cd_roms": null,
            "cluster": {
                "ext_id": "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
            },
            "create_time": "2024-05-19T11:13:37.764820+00:00",
            "description": null,
            "disks": null,
            "enabled_cpu_features": null,
            "ext_id": "14e05447-fd70-4348-4a69-ec90f427f638",
            "generation_uuid": "56e9e929-ae56-4ecc-a62b-cba2930ea522",
            "gpus": null,
            "guest_customization": null,
            "guest_tools": null,
            "hardware_clock_timezone": "UTC",
            "host": null,
            "is_agent_vm": false,
            "is_branding_enabled": true,
            "is_cpu_passthrough_enabled": false,
            "is_cross_cluster_migration_in_progress": false,
            "is_gpu_console_enabled": false,
            "is_live_migrate_capable": null,
            "is_memory_overcommit_enabled": false,
            "is_vcpu_hard_pinning_enabled": false,
            "is_vga_console_enabled": true,
            "links": null,
            "machine_type": "PC",
            "memory_size_bytes": 4294967296,
            "name": "PRTZlmWgHjkg_vm_test_clone2",
            "nics": null,
            "num_cores_per_socket": 2,
            "num_numa_nodes": 0,
            "num_sockets": 2,
            "num_threads_per_core": 2,
            "ownership_info": {
                "owner": {
                    "ext_id": "00000000-0000-0000-0000-000000000000"
                }
            },
            "power_state": "OFF",
            "protection_policy_state": null,
            "protection_type": "UNPROTECTED",
            "serial_ports": null,
            "source": {
                "entity_type": "VM",
                "ext_id": "de84a538-32bf-4a42-913b-340540af18fd"
            },
            "storage_config": null,
            "tenant_id": null,
            "update_time": "2024-05-19T11:13:38.529699+00:00",
            "vtpm_config": {
                "is_vtpm_enabled": false,
                "version": null
            }
        }
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Failed generating create vms Spec"
error:
    description: The error message if an error occurred.
    type: str
    returned: on error
changed:
    description: Whether the state of the VM has changed.
    type: bool
    returned: always
    sample: true
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:ad73eb98-367b-5997-9f79-14e4b10bd1ed"
vm_ext_id:
    description: The external ID of the VM.
    type: str
    returned: always
    sample: "de84a538-32bf-4a42-913b-340540af18fd"
ext_id:
    description:
        - The external ID of the new cloned VM.
    type: str
    returned: always
    sample: "14e05447-fd70-4348-4a69-ec90f427f638"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
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
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
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
        ),
        boot_config=dict(
            type="dict",
            options=vm_specs.get_boot_config_spec(),
            obj=vm_specs.get_boot_config_allowed_types(),
            mutually_exclusive=[("legacy_boot", "uefi_boot")],
        ),
        guest_customization=dict(
            type="dict",
            options=vm_specs.get_gc_spec(),
            obj=vmm_sdk.GuestCustomizationParams,
        ),
    )

    return module_args


def clone_vm(module, result):
    vmm = get_vm_api_instance(module)
    vm_ext_id = module.params["ext_id"]
    result["vm_ext_id"] = vm_ext_id

    current_spec = get_vm(module, vmm, vm_ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for initiate guest os update", **result
        )

    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.CloneOverrideParams()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create vms Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = vmm.clone_vm(extId=vm_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while cloning vm",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        if len(resp.entities_affected) > 0:
            for item in resp.entities_affected:
                if (
                    item.ext_id != vm_ext_id
                    and item.rel == TASK_CONSTANTS.RelEntityType.VM
                ):
                    ext_id = item.ext_id
                    resp = get_vm(module, vmm, ext_id)
                    result["ext_id"] = ext_id
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
    }
    clone_vm(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
