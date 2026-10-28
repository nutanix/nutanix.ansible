#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_transfer_files_to_guest_v2
short_description: Transfer files to an AHV guest VM in Nutanix Prism Central
version_added: 2.7.0
description:
  - Transfer files into a guest VM from a volume disk or an external data source disk.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Transfer Files To Virtual Machine) -
    Required Roles: Account Owner, Administrator, Backup Admin,
    Disaster Recovery Admin, Prism Admin, Project Manager,
    Self-Service Admin (deprecated), Super Admin, Virtual Machine Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module transfers files to the guest VM.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external ID of the VM that receives the files.
    type: str
    required: true
  guest_authentication:
    description:
      - Authentication information for the guest VM.
    type: dict
    required: true
    suboptions:
      username:
        description:
          - Username for the guest VM.
        type: str
        required: true
      password:
        description:
          - Password for the guest VM.
        type: str
        required: true
  transfer_files_spec:
    description:
      - Specification for transferring files to the guest VM.
      - Provide exactly one of C(transfer_files_from_volume_disk) or
        C(transfer_files_from_external_data_source_disk).
    type: dict
    required: true
    suboptions:
      transfer_files_from_volume_disk:
        description:
          - Mounts a vdisk file from a volume group to copy data from a
            specified source path inside the disk to a destination path in
            the guest OS.
        type: dict
        suboptions:
          volume_disk_reference:
            description:
              - Reference to a Volume Disk.
            type: dict
            required: true
            suboptions:
              disk_ext_id:
                description:
                  - An external identifier of the Volume disk. It should be of type UUID.
                type: str
              volume_group_ext_id:
                description:
                  - The external identifier of the Volume Group. It should be of type UUID.
                type: str
          files_to_transfer:
            description:
              - List of files to transfer from the volume disk into the guest VM.
            type: list
            elements: dict
            required: true
            suboptions:
              source_path:
                description:
                  - Path inside the provided data source to copy from.
                  - Should be relative without a leading slash or drive letter.
                type: str
              destination_path:
                description:
                  - Full path in the guest OS where the file will be written.
                type: str
              should_overwrite:
                description:
                  - Boolean flag to allow overwriting existing files.
                type: bool
      transfer_files_from_external_data_source_disk:
        description:
          - Mounts a vdisk file from an external repository via NFS to copy
            data from a specified source path inside the disk to a destination
            path in the guest OS.
        type: dict
        suboptions:
          external_data_source_disk_reference:
            description:
              - Reference to an external data source disk.
            type: dict
            required: true
            suboptions:
              external_repository_ext_id:
                description:
                  - A globally unique identifier of type UUID for the external repository.
                type: str
                required: true
              external_disk_relative_path:
                description:
                  - The relative path of the external data source disk.
                type: str
                required: true
          files_to_transfer:
            description:
              - List of files to transfer from the external data source disk into the guest VM.
            type: list
            elements: dict
            required: true
            suboptions:
              source_path:
                description:
                  - Path inside the provided data source to copy from.
                  - Should be relative without a leading slash or drive letter.
                type: str
              destination_path:
                description:
                  - Full path in the guest OS where the file will be written.
                type: str
              should_overwrite:
                description:
                  - Boolean flag to allow overwriting existing files.
                type: bool
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Transfer files to guest from a volume disk
  nutanix.ncp.ntnx_vm_transfer_files_to_guest_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    guest_authentication:
      username: "admin"
      password: "secret"
    transfer_files_spec:
      transfer_files_from_volume_disk:
        volume_disk_reference:
          disk_ext_id: "0f34a2a7-6068-48ba-859d-1ced14d7f5da"
          volume_group_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
        files_to_transfer:
          - source_path: "payload/app.bin"
            destination_path: "/tmp/app.bin"
            should_overwrite: true
  register: result
  ignore_errors: true

- name: Transfer files to guest from an external data source disk
  nutanix.ncp.ntnx_vm_transfer_files_to_guest_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    guest_authentication:
      username: "admin"
      password: "secret"
    transfer_files_spec:
      transfer_files_from_external_data_source_disk:
        external_data_source_disk_reference:
          external_repository_ext_id: "11111111-1111-1111-1111-111111111111"
          external_disk_relative_path: "disks/source.vmdk"
        files_to_transfer:
          - source_path: "scripts/setup.sh"
            destination_path: "/tmp/setup.sh"
            should_overwrite: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for transferring files to the guest VM.
    - Task details after completion when C(wait) is true.
    - Initial task response when C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "status": "SUCCEEDED",
      "operation": "TransferFilesToGuest",
      "progress_percentage": 100
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while transferring files to guest VM"

error:
  description: This indicates the error message if any error occurred
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

task_ext_id:
  description: The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the VM.
  returned: always
  type: str
  sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    file_attributes_spec = dict(
        source_path=dict(type="str"),
        destination_path=dict(type="str"),
        should_overwrite=dict(type="bool"),
    )
    files_to_transfer_spec = dict(
        type="list",
        elements="dict",
        options=file_attributes_spec,
        obj=vmm_sdk.TransferFileAttributes,
        required=True,
    )

    volume_disk_spec = dict(
        volume_disk_reference=dict(
            type="dict",
            required=True,
            options=dict(
                disk_ext_id=dict(type="str"),
                volume_group_ext_id=dict(type="str"),
            ),
            obj=vmm_sdk.VolumeDiskReference,
        ),
        files_to_transfer=deepcopy(files_to_transfer_spec),
    )
    external_disk_spec = dict(
        external_data_source_disk_reference=dict(
            type="dict",
            required=True,
            options=dict(
                external_repository_ext_id=dict(type="str", required=True),
                external_disk_relative_path=dict(type="str", required=True),
            ),
            obj=vmm_sdk.TransferFilesExternalDataSourceDiskReference,
        ),
        files_to_transfer=deepcopy(files_to_transfer_spec),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        guest_authentication=dict(
            type="dict",
            required=True,
            options=dict(
                username=dict(type="str", required=True),
                password=dict(type="str", required=True, no_log=True),
            ),
            obj=vmm_sdk.Credential,
        ),
        transfer_files_spec=dict(
            type="dict",
            required=True,
            options=dict(
                transfer_files_from_volume_disk=dict(
                    type="dict",
                    options=volume_disk_spec,
                ),
                transfer_files_from_external_data_source_disk=dict(
                    type="dict",
                    options=external_disk_spec,
                ),
            ),
            obj={
                "transfer_files_from_volume_disk": vmm_sdk.TransferFilesFromVolumeDisk,
                "transfer_files_from_external_data_source_disk": (
                    vmm_sdk.TransferFilesFromExternalDataSourceDisk
                ),
            },
            mutually_exclusive=[
                (
                    "transfer_files_from_volume_disk",
                    "transfer_files_from_external_data_source_disk",
                )
            ],
            required_one_of=[
                (
                    "transfer_files_from_volume_disk",
                    "transfer_files_from_external_data_source_disk",
                )
            ],
        ),
    )
    return module_args


def transfer_files_to_guest(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    vms = get_vm_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.TransferFilesToGuestSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for transfer files to guest VM", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = vms.transfer_files_to_guest(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while transferring files to guest VM",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    transfer_files_to_guest(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
