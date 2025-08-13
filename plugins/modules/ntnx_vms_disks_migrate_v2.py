#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_disks_migrate_v2
short_description: Migrate disks of a Virtual Machine to another storage container
description:
    - This module allows you to migrate VM disks from one storage container to another.
    - Use C(all_disks_migration_plan) to migrate all VM disks to a single destination storage container.
    - Use C(migration_plans) to migrate specific disks to different destination storage containers.
    - When migrating all disks to one container, provide only the target container's external ID via C(all_disks_migration_plan).
    - For selective or multi-destination migration, define separate entries in C(migration_plans) for each disk with its target container.
    - This module uses PC v4 APIs based SDKs
author:
    - George Ghawali (@george-ghawali)
options:
    wait:
        description: Wait for the operation to complete.
        type: bool
        required: false
        default: True
    vm_ext_id:
        description:
            - The external ID of the VM.
        type: str
        required: true
    migrate_disks:
        description:
            - A migration plan defines how VM disks are moved to new storage containers
            - Either all disks to one container with a single plan, or individual disks to different containers with separate plans.
        type: dict
        required: true
        suboptions:
            migration_plans:
                description:
                    - A list of plans mapping specific disks to their respective destination storage containers.
                type: dict
                suboptions:
                    plans:
                        description:
                            - A list of migration plans for specific disks.
                            - Each plan specifies a disk and its target storage container.
                        type: list
                        elements: dict
                        required: true
                        suboptions:
                            storage_container:
                                description:
                                    - The storage container to which the disk will be migrated.
                                type: dict
                                required: true
                                suboptions:
                                    ext_id:
                                        description:
                                            - The external ID of the storage container.
                                        type: str
                                        required: true
                            vm_disks:
                                description:
                                    - A list of disks to be migrated.
                                type: list
                                elements: dict
                                required: true
                                suboptions:
                                    disk_ext_id:
                                        description:
                                            - The external ID of the disk to be migrated.
                                        type: str
                                        required: true
            all_disks_migration_plan:
                description:
                    - A single plan to migrate all VM disks to the same storage container.
                type: dict
                suboptions:
                    storage_container:
                        description:
                            - The storage container to which all disks will be migrated.
                        type: dict
                        required: true
                        suboptions:
                            ext_id:
                                description:
                                    - The external ID of the storage container.
                                type: str
                                required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
- name: Migrate all disks of a VM to a new storage container
  nutanix.ncp.ntnx_vms_disks_migrate_v2:
    vm_ext_id: "12345678-1234-1234-1234-123456789012"
    migrate_disks:
      all_disks_migration_plan:
        storage_container:
          ext_id: "87654321-4321-4321-4321-210987654321"

- name: Migrate specific disks of a VM to different storage containers
  nutanix.ncp.ntnx_vms_disks_migrate_v2:
    vm_ext_id: "12345678-1234-1234-1234-123456789012"
    migrate_disks:
      migration_plans:
        plans:
          - storage_container:
              ext_id: "87654321-4321-4321-4321-210987654321"
            vm_disks:
              - disk_ext_id: "disk-12345678-1234-1234-1234-123456789012"
          - storage_container:
              ext_id: "12345678-4321-4321-4321-210987654321"
            vm_disks:
              - disk_ext_id: "disk-87654321-4321-4321-4321-210987654321"
"""

RETURNS = r"""
response:
    description:
        - For C(wait)=false, it will return task details
        - Else it will return the VM details after migration.
    type: dict
    returned: always
    sample:
        {
            "apc_config": {
                "cpu_model": null,
                "is_apc_enabled": false
            },
            "availability_zone": null,
            "bios_uuid": "17ad1cd0-7ef5-4713-5a55-4f4f59fede50",
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
            "create_time": "2025-08-13T08:08:31.453111+00:00",
            "description": "ansible test",
            "disks": [
                {
                    "backing_info": {
                        "data_source": null,
                        "disk_ext_id": "f93b57ba-46ac-415c-aacb-09e3c3b08312",
                        "disk_size_bytes": 26843545600,
                        "is_migration_in_progress": false,
                        "storage_config": null,
                        "storage_container": {
                            "ext_id": "77c1d0c6-aa90-4fdd-a63d-1eca02cbaaed"
                        }
                    },
                    "disk_address": {
                        "bus_type": "SCSI",
                        "index": 2
                    },
                    "ext_id": "f93b57ba-46ac-415c-aacb-09e3c3b08312",
                    "links": null,
                    "tenant_id": null
                },
                {
                    "backing_info": {
                        "data_source": null,
                        "disk_ext_id": "5ca0300c-40f6-4178-a6f1-9e8866603f1b",
                        "disk_size_bytes": 26843545600,
                        "is_migration_in_progress": false,
                        "storage_config": null,
                        "storage_container": {
                            "ext_id": "f279ee13-94c3-48b5-ad3c-22459a9cd950"
                        }
                    },
                    "disk_address": {
                        "bus_type": "SCSI",
                        "index": 3
                    },
                    "ext_id": "5ca0300c-40f6-4178-a6f1-9e8866603f1b",
                    "links": null,
                    "tenant_id": null
                },
                {
                    "backing_info": {
                        "data_source": null,
                        "disk_ext_id": "9c57b303-f910-4562-a517-4ac093fdbd37",
                        "disk_size_bytes": 26843545600,
                        "is_migration_in_progress": false,
                        "storage_config": null,
                        "storage_container": {
                            "ext_id": "f279ee13-94c3-48b5-ad3c-22459a9cd950"
                        }
                    },
                    "disk_address": {
                        "bus_type": "SCSI",
                        "index": 4
                    },
                    "ext_id": "9c57b303-f910-4562-a517-4ac093fdbd37",
                    "links": null,
                    "tenant_id": null
                },
                {
                    "backing_info": {
                        "data_source": null,
                        "disk_ext_id": "63020864-2753-48cf-9088-b794a6419859",
                        "disk_size_bytes": 26843545600,
                        "is_migration_in_progress": false,
                        "storage_config": null,
                        "storage_container": {
                            "ext_id": "f279ee13-94c3-48b5-ad3c-22459a9cd950"
                        }
                    },
                    "disk_address": {
                        "bus_type": "SCSI",
                        "index": 5
                    },
                    "ext_id": "63020864-2753-48cf-9088-b794a6419859",
                    "links": null,
                    "tenant_id": null
                },
                {
                    "backing_info": {
                        "data_source": null,
                        "disk_ext_id": "a2763684-1ca8-4a39-aec9-46b49190f271",
                        "disk_size_bytes": 26843545600,
                        "is_migration_in_progress": false,
                        "storage_config": null,
                        "storage_container": {
                            "ext_id": "f279ee13-94c3-48b5-ad3c-22459a9cd950"
                        }
                    },
                    "disk_address": {
                        "bus_type": "SCSI",
                        "index": 6
                    },
                    "ext_id": "a2763684-1ca8-4a39-aec9-46b49190f271",
                    "links": null,
                    "tenant_id": null
                }
            ],
            "enabled_cpu_features": null,
            "ext_id": "17ad1cd0-7ef5-4713-5a55-4f4f59fede50",
            "generation_uuid": "a61ae65f-5896-472e-aae4-96c65cfa1dde",
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
            "name": "ansible-testuQlyuukUEJltvm",
            "nics": null,
            "num_cores_per_socket": 1,
            "num_numa_nodes": 0,
            "num_sockets": 1,
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
            "update_time": "2025-08-13T08:08:51.522290+00:00",
            "vtpm_config": {
                "is_vtpm_enabled": false,
                "version": null,
                "vtpm_device": null
            }
        }
task_ext_id:
    description: The external ID of the task associated with the operation.
    type: str
changed:
    description: Indicates whether the module made any changes.
    type: bool
error:
    description: The error message, if any, encountered.
    type: str
vm_ext_id:
    description: VM external ID
    type: str
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    migrate_disks_allowed_types = {
        "migration_plans": vmm_sdk.MigrationPlans,
        "all_disks_migration_plan": vmm_sdk.AllDisksMigrationPlan,
    }

    storage_container = dict(
        ext_id=dict(type="str", required=True),
    )

    vm_disk_reference = dict(
        disk_ext_id=dict(type="str", required=True),
    )

    adsf_disk_migration_plan = dict(
        storage_container=dict(
            type="dict",
            options=storage_container,
            obj=vmm_sdk.AhvConfigVmDiskContainerReference,
            required=True,
        ),
        vm_disks=dict(
            type="list",
            elements="dict",
            options=vm_disk_reference,
            obj=vmm_sdk.MigrateDiskReference,
            required=True,
        ),
    )

    migration_plans = dict(
        plans=dict(
            type="list",
            elements="dict",
            options=adsf_disk_migration_plan,
            obj=vmm_sdk.ADSFDiskMigrationPlan,
            required=True,
        ),
    )

    all_disks_migration_plan = dict(
        storage_container=dict(
            type="dict",
            options=storage_container,
            obj=vmm_sdk.AhvConfigVmDiskContainerReference,
            required=True,
        ),
    )

    migrate_disks_spec = dict(
        migration_plans=dict(
            type="dict",
            options=migration_plans,
            obj=vmm_sdk.MigrationPlans,
            required=False,
        ),
        all_disks_migration_plan=dict(
            type="dict",
            options=all_disks_migration_plan,
            obj=vmm_sdk.AllDisksMigrationPlan,
            required=False,
        ),
    )

    migrate_disks = dict(
        migrate_disks=dict(
            type="dict",
            options=migrate_disks_spec,
            obj=migrate_disks_allowed_types,
            mutually_exclusive=[("migration_plans", "all_disks_migration_plan")],
        )
    )

    module_args = dict(
        vm_ext_id=dict(type="str", required=True),
        migrate_disks=dict(
            type="dict",
            options=migrate_disks_spec,
            obj=migrate_disks_allowed_types,
            mutually_exclusive=[("migration_plans", "all_disks_migration_plan")],
        )
    )
    return module_args


def migrate_disk(module, result):
    vms = get_vm_api_instance(module)
    vm_ext_id = module.params["vm_ext_id"]
    result["vm_ext_id"] = vm_ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.DiskMigrationParams()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Migrate Disk spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vm = get_vm(module, vms, vm_ext_id)
    etag = get_etag(vm)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.migrate_vm_disks(extId=vm_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while migrating disk of VM",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_vm(module, vms, vm_ext_id)
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
        "vm_ext_id": None,
    }
    migrate_disk(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
