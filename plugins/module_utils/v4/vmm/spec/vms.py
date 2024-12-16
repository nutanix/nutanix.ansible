# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from copy import deepcopy

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ...sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


class VmSpecs:
    """Module specs related to Vms"""

    # Allowed object types for variouse attributes

    disk_backing_info_allowed_types = {
        "vm_disk": vmm_sdk.AhvConfigVmDisk,
        "adsf_volume_group": vmm_sdk.ADSFVolumeGroupReference,
    }

    guest_customization_param_allowed_types = {
        "sysprep": vmm_sdk.Sysprep,
        "cloudinit": vmm_sdk.CloudInit,
    }

    sysprep_param_allowed_types = {
        "unattendxml": vmm_sdk.Unattendxml,
        "custom_key_values": vmm_sdk.CustomKeyValues,
    }

    cloud_init_script_allowed_types = {
        "user_data": vmm_sdk.Userdata,
        "custom_key_values": vmm_sdk.CustomKeyValues,
    }

    boot_device_allowed_types = {
        "boot_device_disk": vmm_sdk.BootDeviceDisk,
        "boot_device_nic": vmm_sdk.BootDeviceNic,
    }

    data_source_reference_allowed_types = {
        "image_reference": vmm_sdk.ImageReference,
        "vm_disk_reference": vmm_sdk.VmDiskReference,
    }

    boot_config_allowed_types = {
        "legacy_boot": vmm_sdk.LegacyBoot,
        "uefi_boot": vmm_sdk.UefiBoot,
    }

    reference_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    disk_storage_config_spec = dict(is_flash_mode_enabled=dict(type="bool"))

    image_reference_spec = dict(
        image_ext_id=dict(type="str"),
    )

    disk_address_spec = dict(
        bus_type=dict(
            type="str", choices=["SCSI", "IDE", "PCI", "SATA", "SPAPR"], required=True
        ),
        index=dict(type="int"),
    )

    vm_disk_reference_spec = dict(
        disk_ext_id=dict(type="str"),
        disk_address=dict(
            type="dict", options=disk_address_spec, obj=vmm_sdk.AhvConfigDiskAddress
        ),
        vm_reference=dict(
            type="dict", options=reference_spec, obj=vmm_sdk.AhvConfigVmReference
        ),
    )

    data_source_reference_spec = dict(
        image_reference=dict(type="dict", options=image_reference_spec),
        vm_disk_reference=dict(type="dict", options=vm_disk_reference_spec),
    )

    data_source_spec = dict(
        reference=dict(
            type="dict",
            options=data_source_reference_spec,
            obj=data_source_reference_allowed_types,
            mutually_exclusive=[("image_reference", "vm_disk_reference")],
        ),
    )

    vm_disk_spec = dict(
        disk_size_bytes=dict(type="int"),
        storage_container=dict(
            type="dict",
            options=reference_spec,
            obj=vmm_sdk.AhvConfigVmDiskContainerReference,
        ),
        storage_config=dict(
            type="dict",
            options=disk_storage_config_spec,
            obj=vmm_sdk.AhvConfigVmDiskStorageConfig,
        ),
        data_source=dict(type="dict", options=data_source_spec, obj=vmm_sdk.DataSource),
    )

    adsf_volume_group_spec = dict(
        volume_group_ext_id=dict(type="str"),
    )

    disk_backing_info_spec = dict(
        vm_disk=dict(type="dict", options=vm_disk_spec),
        adsf_volume_group=dict(type="dict", options=adsf_volume_group_spec),
    )

    disk_spec = dict(
        backing_info=dict(
            type="dict",
            options=disk_backing_info_spec,
            obj=disk_backing_info_allowed_types,
            mutually_exclusive=[("vm_disk", "adsf_volume_group")],
        ),
        disk_address=dict(
            type="dict", options=disk_address_spec, obj=vmm_sdk.AhvConfigDiskAddress
        ),
    )

    cd_rom_address_spec = dict(
        bus_type=dict(type="str", choices=["IDE", "SATA"]), index=dict(type="int")
    )

    cd_rom_spec = dict(
        backing_info=dict(
            type="dict", options=vm_disk_spec, obj=vmm_sdk.AhvConfigVmDisk
        ),
        disk_address=dict(
            type="dict", options=cd_rom_address_spec, obj=vmm_sdk.AhvConfigCdRomAddress
        ),
    )

    ip_address_sub_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int"),
    )

    ipv4_config_spec = dict(
        should_assign_ip=dict(type="bool"),
        ip_address=dict(
            type="dict", options=ip_address_sub_spec, obj=vmm_sdk.IPv4Address
        ),
        secondary_ip_address_list=dict(
            type="list",
            elements="dict",
            options=ip_address_sub_spec,
            obj=vmm_sdk.IPv4Address,
        ),
    )

    nic_backup_info_spec = dict(
        model=dict(type="str", choices=["VIRTIO", "E1000"]),
        mac_address=dict(type="str"),
        is_connected=dict(type="bool"),
        num_queues=dict(type="int"),
    )

    nic_info_spec = dict(
        nic_type=dict(
            type="str",
            choices=[
                "NORMAL_NIC",
                "DIRECT_NIC",
                "NETWORK_FUNCTION_NIC",
                "SPAN_DESTINATION_NIC",
            ],
        ),
        network_function_chain=dict(
            type="dict",
            options=reference_spec,
            obj=vmm_sdk.NetworkFunctionChainReference,
        ),
        network_function_nic_type=dict(
            type="str", choices=["INGRESS", "EGRESS", "TAP"]
        ),
        subnet=dict(type="dict", options=reference_spec, obj=vmm_sdk.SubnetReference),
        vlan_mode=dict(type="str", choices=["ACCESS", "TRUNK"]),
        trunked_vlans=dict(type="list", elements="int"),
        should_allow_unknown_macs=dict(type="bool"),
        ipv4_config=dict(type="dict", options=ipv4_config_spec, obj=vmm_sdk.Ipv4Config),
    )

    nic_spec = dict(
        backing_info=dict(
            type="dict", options=nic_backup_info_spec, obj=vmm_sdk.EmulatedNic
        ),
        network_info=dict(
            type="dict", options=nic_info_spec, obj=vmm_sdk.AhvConfigNicNetworkInfo
        ),
    )

    unattendxml_spec = dict(
        value=dict(type="str"),
    )

    kvpair_spec = dict(name=dict(type="str"), value=dict(type="raw", no_log=False))

    custom_key_values_spec = dict(
        key_value_pairs=dict(
            type="list",
            elements="dict",
            options=kvpair_spec,
            obj=vmm_sdk.KVPair,
            no_log=False,
        ),
    )

    sysprep_param_spec = dict(
        unattendxml=dict(
            type="dict", options=unattendxml_spec, obj=vmm_sdk.Unattendxml
        ),
        custom_key_values=dict(
            type="dict",
            options=custom_key_values_spec,
            obj=vmm_sdk.CustomKeyValues,
            no_log=False,
        ),
    )

    sysprep_spec = dict(
        install_type=dict(type="str", choices=["FRESH", "PREPARED"]),
        sysprep_script=dict(
            type="dict",
            options=sysprep_param_spec,
            no_log=False,
            obj=sysprep_param_allowed_types,
            mutually_exclusive=[("unattendxml", "custom_key_values")],
        ),
    )

    user_data = dict(
        value=dict(type="str", required=True),
    )

    cloud_init_script = dict(
        user_data=dict(type="dict", options=user_data, obj=vmm_sdk.Userdata),
        custom_key_values=dict(
            type="dict",
            options=custom_key_values_spec,
            obj=vmm_sdk.CustomKeyValues,
            no_log=False,
        ),
    )

    cloudinit_spec = dict(
        datasource_type=dict(type="str", choices=["CONFIG_DRIVE_V2"]),
        metadata=dict(type="str"),
        cloud_init_script=dict(
            type="dict",
            options=cloud_init_script,
            obj=cloud_init_script_allowed_types,
            mutually_exclusive=[("user_data", "custom_key_values")],
        ),
    )

    guest_customization_param_spec = dict(
        sysprep=dict(type="dict", options=sysprep_spec, obj=vmm_sdk.Sysprep),
        cloudinit=dict(type="dict", options=cloudinit_spec, obj=vmm_sdk.CloudInit),
    )

    guest_customization_spec = dict(
        config=dict(
            type="dict",
            options=guest_customization_param_spec,
            obj=guest_customization_param_allowed_types,
            mutually_exclusive=[("sysprep", "cloudinit")],
        ),
    )

    boot_device_disk_spec = dict(
        disk_address=dict(
            type="dict", options=disk_address_spec, obj=vmm_sdk.AhvConfigDiskAddress
        ),
    )

    boot_device_nic_spec = dict(
        mac_address=dict(type="str"),
    )

    boot_device_spec = dict(
        boot_device_disk=dict(type="dict", options=boot_device_disk_spec),
        boot_device_nic=dict(type="dict", options=boot_device_nic_spec),
    )

    legacy_boot_spec = dict(
        boot_device=dict(
            type="dict",
            options=boot_device_spec,
            obj=boot_device_allowed_types,
            mutually_exclusive=[("boot_device_disk", "boot_device_nic")],
        ),
        boot_order=dict(
            type="list", elements="str", choices=["CDROM", "NETWORK", "DISK"]
        ),
    )

    nvram_device_spec = dict(
        backing_storage_info=dict(
            type="dict", options=vm_disk_spec, obj=vmm_sdk.AhvConfigVmDisk
        ),
    )

    uefi_boot_spec = dict(
        is_secure_boot_enabled=dict(type="bool"),
        nvram_device=dict(
            type="dict", options=nvram_device_spec, obj=vmm_sdk.NvramDevice
        ),
    )

    boot_config_spec = dict(
        legacy_boot=dict(type="dict", options=legacy_boot_spec),
        uefi_boot=dict(type="dict", options=uefi_boot_spec),
    )

    vtpm_config_spec = dict(
        is_vtpm_enabled=dict(type="bool"),
        version=dict(type="str"),
    )

    cpu_model_reference_spec = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
    )

    apc_config_spec = dict(
        is_apc_enabled=dict(type="bool"),
        cpu_model=dict(
            type="dict", options=cpu_model_reference_spec, obj=vmm_sdk.CpuModelReference
        ),
    )

    qos_config_spec = dict(
        throttled_iops=dict(type="int"),
    )

    storage_config_spec = dict(
        is_flash_mode_enabled=dict(type="bool"),
        qos_config=dict(type="dict", options=qos_config_spec, obj=vmm_sdk.QosConfig),
    )

    pci_address_spec = dict(
        segment=dict(type="int"),
        bus=dict(type="int"),
        device=dict(type="int"),
        func=dict(type="int"),
    )

    gpu_spec = dict(
        name=dict(type="str"),
        mode=dict(
            type="str",
            choices=["PASSTHROUGH_GRAPHICS", "PASSTHROUGH_COMPUTE", "VIRTUAL"],
        ),
        device_id=dict(type="int"),
        vendor=dict(type="str", choices=["NVIDIA", "INTEL", "AMD"]),
        pci_address=dict(type="dict", options=pci_address_spec, obj=vmm_sdk.SBDF),
    )

    serial_port_spec = dict(
        ext_id=dict(type="str"),
        is_connected=dict(type="bool"),
        index=dict(type="int"),
    )

    guest_tools_spec = dict(
        is_enabled=dict(type="bool"),
        capabilities=dict(
            type="list",
            elements="str",
            choices=["SELF_SERVICE_RESTORE", "VSS_SNAPSHOT"],
        ),
    )

    vm_spec = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        num_sockets=dict(type="int"),
        num_cores_per_socket=dict(type="int"),
        num_threads_per_core=dict(type="int"),
        num_numa_nodes=dict(type="int"),
        memory_size_bytes=dict(type="int"),
        is_vcpu_hard_pinning_enabled=dict(type="bool"),
        is_cpu_passthrough_enabled=dict(type="bool"),
        enabled_cpu_features=dict(
            type="list", elements="str", choices=["HARDWARE_VIRTUALIZATION"]
        ),
        is_memory_overcommit_enabled=dict(type="bool"),
        is_gpu_console_enabled=dict(type="bool"),
        categories=dict(
            type="list",
            elements="dict",
            options=reference_spec,
            obj=vmm_sdk.AhvConfigCategoryReference,
        ),
        cluster=dict(
            type="dict", options=reference_spec, obj=vmm_sdk.AhvConfigClusterReference
        ),
        availability_zone=dict(
            type="dict", options=reference_spec, obj=vmm_sdk.AvailabilityZoneReference
        ),
        guest_customization=dict(
            type="dict",
            options=guest_customization_spec,
            obj=vmm_sdk.GuestCustomizationParams,
        ),
        guest_tools=dict(type="dict", options=guest_tools_spec, obj=vmm_sdk.GuestTools),
        hardware_clock_timezone=dict(type="str"),
        is_branding_enabled=dict(type="bool"),
        boot_config=dict(
            type="dict",
            options=boot_config_spec,
            obj=boot_config_allowed_types,
            mutually_exclusive=[("legacy_boot", "uefi_boot")],
        ),
        is_vga_console_enabled=dict(type="bool"),
        machine_type=dict(type="str", choices=["PC", "PSERIES", "Q35"]),
        vtpm_config=dict(type="dict", options=vtpm_config_spec, obj=vmm_sdk.VtpmConfig),
        is_agent_vm=dict(type="bool"),
        apc_config=dict(type="dict", options=apc_config_spec, obj=vmm_sdk.ApcConfig),
        storage_config=dict(
            type="dict", options=storage_config_spec, obj=vmm_sdk.ADSFVmStorageConfig
        ),
        disks=dict(
            type="list", elements="dict", options=disk_spec, obj=vmm_sdk.AhvConfigDisk
        ),
        cd_roms=dict(
            type="list",
            elements="dict",
            options=cd_rom_spec,
            obj=vmm_sdk.AhvConfigCdRom,
        ),
        nics=dict(
            type="list", elements="dict", options=nic_spec, obj=vmm_sdk.AhvConfigNic
        ),
        gpus=dict(type="list", elements="dict", options=gpu_spec, obj=vmm_sdk.Gpu),
        serial_ports=dict(
            type="list",
            elements="dict",
            options=serial_port_spec,
            obj=vmm_sdk.SerialPort,
        ),
    )

    @classmethod
    def get_vm_spec(cls):
        return deepcopy(cls.vm_spec)

    @classmethod
    def get_nic_spec(cls):
        return deepcopy(cls.nic_spec)

    @classmethod
    def get_gc_spec(cls):
        return deepcopy(cls.guest_customization_spec)

    @classmethod
    def get_boot_config_spec(cls):
        return deepcopy(cls.boot_config_spec)

    @classmethod
    def get_boot_config_allowed_types(cls):
        return deepcopy(cls.boot_config_allowed_types)

    @classmethod
    def get_disk_spec(cls):
        return deepcopy(cls.disk_spec)

    @classmethod
    def get_cd_rom_spec(cls):
        return deepcopy(cls.cd_rom_spec)

    @classmethod
    def get_vm_disk_spec(cls):
        return deepcopy(cls.vm_disk_spec)

    @classmethod
    def get_gc_param_spec(cls):
        return deepcopy(cls.guest_customization_param_spec)

    @classmethod
    def get_gc_allowed_types_spec(cls):
        return deepcopy(cls.guest_customization_param_allowed_types)
