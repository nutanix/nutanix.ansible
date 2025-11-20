#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ova_v2
short_description: "Create, Update and Delete Ova from VM, url or object lite"
version_added: 2.3.0
description:
    - Create, Update and Delete Ova from VM, url or object lite
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - State of the Ova to be created, updated or deleted
            - if C(state) is present, it will create or update the ova.
            - If C(state) is set to C(present) and ext_id is not provided then the operation will be create the ova
            - If C(state) is set to C(present) and ext_id is provided then the operation will be update the ova
            - If C(state) is set to C(absent) and ext_id is provided , then operation will be delete the ova
        type: str
        choices: ["present", "absent"]
        default: "present"
    wait:
        description:
            - Wait for the task to complete
        type: bool
        default: true
    name:
        description:
            - Name of the Ova to be created or updated
        type: str
    ext_id:
        description:
            - External ID of the Ova to be updated or deleted
        type: str
    checksum:
        description:
            - Checksum of the Ova
        type: dict
        suboptions:
            ova_sha1_checksum:
                description:
                    - SHA1 checksum of the Ova
                type: dict
                suboptions:
                    hex_digest:
                        description:
                            - The SHA1 digest of an OVA file in hexadecimal format.
                        type: str
                        required: true
            ova_sha256_checksum:
                description:
                    - SHA256 checksum of the Ova
                type: dict
                suboptions:
                    hex_digest:
                        description:
                            - The SHA256 digest of an OVA file in hexadecimal format.
                        type: str
                        required: true
    source:
        description:
            - Source of the created OVA file.
            - The source can either be a VM, URL, or a Object lite.
        type: dict
        suboptions:
            ova_url_source:
                description:
                    - Source of the Ova file from a URL.
                type: dict
                suboptions:
                    url:
                        description:
                            - The URL that can be used to download an OVA.
                        type: str
                        required: true
                    should_allow_insecure_url:
                        description:
                            Ignore the certificate errors if the value is true.
                        type: bool
                        default: false
                    basic_auth:
                        description:
                            - Basic authentication credentials for image source HTTP/S URL.
                        type: dict
                        suboptions:
                            username:
                                description:
                                    - Username for basic authentication.
                                type: str
                                required: true
                            password:
                                description:
                                    - Password for basic authentication.
                                type: str
                                required: true
            ova_vm_source:
                description:
                    - Source of the Ova file from a VM.
                type: dict
                suboptions:
                    vm_ext_id:
                        description:
                            - The identifier of a VM to be exported to an OVA.
                        type: str
                        required: true
                    disk_file_format:
                        description:
                            - Disk format of an OVA.
                        type: str
                        choices: ["VMDK", "QCOW2"]
                        required: true
            objects_lite_source:
                description:
                    - Key that identifies the source object in the bucket.
                    - The resource implies the bucket, 'vmm-ovas' for OVA.
                type: dict
                suboptions:
                    key:
                        description:
                            - Key that identifies the source object in the bucket.
                        type: str
                        required: true
    cluster_location_ext_ids:
        description:
            - List of cluster identifiers where the OVA is located.
            - This field is required when creating an OVA from URL or Objects lite upload.
        type: list
        elements: str
    disk_format:
        description:
            - Disk format of the OVA.
        type: str
        choices: ["VMDK", "QCOW2"]

extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create Ova from the VM
  nutanix.ncp.ntnx_ova_v2:
    name: "name"
    source:
      ova_vm_source:
        vm_ext_id: "12345678-1234-1234-1234-123456789012"
        disk_file_format: "QCOW2"
  register: result

- name: Create Ova from a valid url
  nutanix.ncp.ntnx_ova_v2:
    name: "{{ ova_name }}_url"
    source:
      ova_url_source:
        url: "https://example.com/path/to/ova/file.ova"
        should_allow_insecure_url: true
    cluster_location_ext_ids:
      - "000636a4-e7ce-389e-185b-ac1f6b6f97e2"
  register: result

- name: Create ova using object store source
  nutanix.ncp.ntnx_ova_v2:
    name: "object-ova"
    source:
      objects_lite_source:
        key: "object_name"
    cluster_location_ext_ids:
      - "000636a4-e7ce-389e-185b-ac1f6b6f97e2"
  register: result

- name: Update Ova
  nutanix.ncp.ntnx_ova_v2:
    ext_id: "12345678-1234-1234-1234-123456789012"
    name: "name_updated"
  register: result

- name: Delete Ova
  nutanix.ncp.ntnx_ova_v2:
    ext_id: "12345678-1234-1234-1234-123456789012"
    state: absent
  register: result
"""

RETURN = r"""
response:
    description:
        - Response when we create, update or delete an Ova.
        - Response will contain Ova details if C(wait) is true, if creating or updating Ova.
        - Response will contain Task details if C(wait) is true, if deleting Ova.
        - Response will contain Task details if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "checksum": {
                "hex_digest": "8b6b28a02d0630a7140adac3466bc5dabd4b3de2a02d1051b9815e82f5957390"
            },
            "cluster_location_ext_ids": [
                "000636a4-e7ce-389e-185b-ac1f6b6f97e2"
            ],
            "create_time": "2025-06-09T10:32:38.810439+00:00",
            "created_by": {
                "additional_attributes": null,
                "buckets_access_keys": null,
                "created_by": null,
                "created_time": null,
                "creation_type": null,
                "description": null,
                "display_name": null,
                "email_id": null,
                "ext_id": "30303030-3030-3030-2d30-3030302d3030",
                "first_name": null,
                "idp_id": null,
                "is_force_reset_password_enabled": null,
                "last_login_time": null,
                "last_name": null,
                "last_updated_by": null,
                "last_updated_time": null,
                "links": null,
                "locale": null,
                "middle_initial": null,
                "password": null,
                "region": null,
                "status": null,
                "tenant_id": null,
                "user_type": null,
                "username": "admin"
            },
            "disk_format": "QCOW2",
            "ext_id": "aab776d5-d83f-4e32-a9de-63e91f9f5e47",
            "last_update_time": "2025-06-09T10:32:38.810439+00:00",
            "links": null,
            "name": "JSVJIbifvyVgansible-agova",
            "parent_vm": "JSVJIbifvyVgansible-agvm",
            "size_bytes": 10240,
            "source": null,
            "tenant_id": null,
            "vm_config": {
                "apc_config": null,
                "availability_zone": null,
                "bios_uuid": null,
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
                "cluster": null,
                "create_time": null,
                "custom_attributes": null,
                "description": "ansible test ova",
                "disks": null,
                "enabled_cpu_features": null,
                "ext_id": null,
                "generation_uuid": null,
                "gpus": null,
                "guest_customization": null,
                "guest_tools": null,
                "hardware_clock_timezone": "UTC",
                "host": null,
                "is_agent_vm": false,
                "is_branding_enabled": null,
                "is_cpu_hotplug_enabled": true,
                "is_cpu_passthrough_enabled": false,
                "is_cross_cluster_migration_in_progress": null,
                "is_gpu_console_enabled": null,
                "is_live_migrate_capable": null,
                "is_memory_overcommit_enabled": null,
                "is_scsi_controller_enabled": true,
                "is_vcpu_hard_pinning_enabled": null,
                "is_vga_console_enabled": null,
                "links": null,
                "machine_type": "PC",
                "memory_size_bytes": 1073741824,
                "name": "JSVJIbifvyVgansible-agvm",
                "nics": null,
                "num_cores_per_socket": 1,
                "num_numa_nodes": null,
                "num_sockets": 2,
                "num_threads_per_core": 1,
                "ownership_info": null,
                "pcie_devices": null,
                "power_state": null,
                "project": null,
                "protection_policy_state": null,
                "protection_type": null,
                "serial_ports": null,
                "source": null,
                "storage_config": null,
                "tenant_id": null,
                "update_time": null,
                "vtpm_config": null
            }
        }
task_ext_id:
    description: Task ext_id if the operation is async
    returned: always
    type: str
    sample: "ZXJnb24=:350f0fd5-097d-4ece-8f44-6e5bfbe2dc08"
ext_id:
    description: External id of the Ova
    returned: always
    type: str
    sample: "aab776d5-d83f-4e32-a9de-63e91f9f5e47"
error:
    description: Error message if any
    returned: always
    type: str
changed:
    description: Indicates if the module made any changes
    returned: always
    type: bool
    sample: true
failed:
    description: Indicates if the module failed
    returned: when failed
    type: bool
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
    get_etag,
    get_ova_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_ova  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    checksum_allowed_types = {
        "ova_sha1_checksum": vmm_sdk.OvaSha1Checksum,
        "ova_sha256_checksum": vmm_sdk.OvaSha256Checksum,
    }
    source_allowed_types = {
        "ova_url_source": vmm_sdk.OvaUrlSource,
        "ova_vm_source": vmm_sdk.OvaVmSource,
        "objects_lite_source": vmm_sdk.ObjectsLiteSource,
    }
    ova_sha_checksum_spec = dict(
        hex_digest=dict(type="str", required=True),
    )
    checksum_spec = dict(
        ova_sha1_checksum=dict(type="dict", options=ova_sha_checksum_spec),
        ova_sha256_checksum=dict(type="dict", options=ova_sha_checksum_spec),
    )
    ova_url_source_spec = dict(
        url=dict(type="str", required=True),
        should_allow_insecure_url=dict(
            type="bool",
            default=False,
        ),
        basic_auth=dict(
            type="dict",
            options=dict(
                username=dict(type="str", required=True),
                password=dict(type="str", no_log=True, required=True),
            ),
        ),
    )
    ova_vm_source_spec = dict(
        vm_ext_id=dict(type="str", required=True),
        disk_file_format=dict(
            type="str",
            choices=["VMDK", "QCOW2"],
            required=True,
        ),
    )
    objects_lite_source_spec = dict(
        key=dict(type="str", required=True, no_log=True),
    )
    source_spec = dict(
        ova_url_source=dict(
            type="dict",
            options=ova_url_source_spec,
        ),
        ova_vm_source=dict(
            type="dict",
            options=ova_vm_source_spec,
        ),
        objects_lite_source=dict(
            type="dict",
            options=objects_lite_source_spec,
        ),
    )

    module_args = dict(
        name=dict(type="str"),
        ext_id=dict(type="str"),
        checksum=dict(
            type="dict",
            options=checksum_spec,
            obj=checksum_allowed_types,
            mutually_exclusive=[("ova_sha1_checksum", "ova_sha256_checksum")],
        ),
        source=dict(
            type="dict",
            options=source_spec,
            obj=source_allowed_types,
            mutually_exclusive=[
                ("ova_url_source", "ova_vm_source", "objects_lite_source")
            ],
        ),
        cluster_location_ext_ids=dict(
            type="list",
            elements="str",
        ),
        disk_format=dict(
            type="str",
            choices=["VMDK", "QCOW2"],
        ),
    )

    return module_args


def create_ova(module, ova, result):
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.Ova()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create ova spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = ova.create_ova(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating ova",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.OVA
        )
        if ext_id:
            resp = get_ova(module, ova, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    if current_spec.get("name") != update_spec.get("name"):
        return False
    return True


def update_ova(module, ova, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_ova(module, ova, ext_id=ext_id)

    etag_value = get_etag(current_spec)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.Ova()
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating ova update spec", **result)

    # check for idempotency
    if check_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = ova.update_ova_by_id(extId=ext_id, body=update_spec, if_match=etag_value)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating ova",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_ova(module, ova, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_ova(module, ova, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Ova with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = ova.delete_ova_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting ova",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name",)),
            (
                "state",
                "present",
                (
                    "ext_id",
                    "source",
                ),
                True,
            ),
        ],
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
    state = module.params.get("state")
    ova = get_ova_api_instance(module)
    if state == "present":
        if module.params.get("ext_id"):
            update_ova(module, ova, result)
        else:
            create_ova(module, ova, result)
    else:
        delete_ova(module, ova, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
