# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

__metaclass__ = type


class DefaultVMSpec:
    """Basic VM module with common arguments"""

    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    subnet_spec = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        cluster=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
    )
    network_spec = dict(
        uuid=dict(type="str"),
        state=dict(type="str", choices=["absent"]),
        subnet=dict(
            type="dict", options=subnet_spec, mutually_exclusive=mutually_exclusive
        ),
        mac_address=dict(type="str", required=False),
        private_ip=dict(type="str", required=False),
        is_connected=dict(type="bool", default=True),
    )

    boot_config_spec = dict(
        boot_type=dict(
            type="str", choices=["LEGACY", "UEFI", "SECURE_BOOT"], default="LEGACY"
        ),
        boot_order=dict(
            type="list", elements="str", default=["CDROM", "DISK", "NETWORK"]
        ),
    )

    gc_spec = dict(
        type=dict(type="str", choices=["cloud_init", "sysprep"], required=True),
        script_path=dict(type="path", required=True),
        is_overridable=dict(type="bool", default=False),
    )

    vm_argument_spec = dict(
        name=dict(type="str", required=False),
        vm_uuid=dict(type="str"),
        project=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        cluster=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        vcpus=dict(type="int"),
        cores_per_vcpu=dict(type="int"),
        memory_gb=dict(type="int"),
        networks=dict(type="list", elements="dict", options=network_spec),
        boot_config=dict(type="dict", options=boot_config_spec),
        guest_customization=dict(type="dict", options=gc_spec),
        timezone=dict(type="str", default="UTC"),
        categories=dict(type="dict"),
        force_power_off=dict(type="bool", default=False),
    )
