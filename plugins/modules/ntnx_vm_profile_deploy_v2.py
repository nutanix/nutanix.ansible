#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_profile_deploy_v2
short_description: Deploy a VM from a VM profile in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Deploy a VM from a VM profile in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Deploy Virtual Machine From VM Profile) -
      Required Roles: Super Admin, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - Specify state.
            - If C(state) is set to C(present), a VM is deployed from the VM profile identified by C(ext_id).
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external ID (UUID) of the VM profile.
        type: str
        required: true
    vm_name:
        description:
            - VM name.
            - Maximum length is 80 characters.
        type: str
    vm_description:
        description:
            - VM description.
        type: str
    project_ext_id:
        description:
            - The external ID (UUID) of the project.
        type: str
    cluster:
        description:
            - Reference to a cluster.
        type: dict
        suboptions:
            ext_id:
                description:
                    - The globally unique identifier of a cluster type UUID.
                type: str
                required: true
    categories:
        description:
            - Categories for the VM.
        type: list
        elements: dict
        suboptions:
            ext_id:
                description:
                    - A globally unique identifier of a VM category of type UUID.
                type: str
                required: true
    nics:
        description:
            - The NICs to be attached to the VM deployed from the VM Profile.
        type: list
        elements: dict
        suboptions:
            vm_profile_nic_ext_id:
                description:
                    - The external ID (UUID) of the VM Profile NIC.
                    - >-
                      This UUID would be used by user to associate the information they want to give during
                      deployment with the NIC information inside the VM Profile.
                type: str
            subnet:
                description:
                    - Network identifier for this adapter.
                    - Only valid if nic_type is NORMAL_NIC or DIRECT_NIC.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - The globally unique identifier of a subnet of type UUID.
                        type: str
                        required: true
    disks:
        description:
            - The disks to be attached to the VM deployed from the VM Profile.
        type: list
        elements: dict
        suboptions:
            backing_info:
                description:
                    - The backing information for the disk to be attached to the VM deployed from the VM Profile.
                type: dict
                suboptions:
                    disk_size_bytes:
                        description:
                            - Size of the disk in bytes.
                            - Minimum value is 1.
                        type: int
                    data_source:
                        description:
                            - The data source reference to clone the contents of the disk from.
                        type: dict
                        suboptions:
                            reference:
                                description:
                                    - The data source reference to clone the contents of the disk from.
                                type: dict
                                suboptions:
                                    image:
                                        description:
                                            - Reference to an IMAGE.
                                        type: dict
                                        suboptions:
                                            image_ext_id:
                                                description:
                                                    - A globally unique identifier of an image of type UUID.
                                                type: str
    guest_customization:
        description:
            - >-
              The guest customization parameters for the VM deployed from the VM Profile. Accepts a cloud-init
              configuration file to be used by the guest for the next boot.
        type: dict
        suboptions:
            config:
                description:
                    - The Nutanix Guest customization settings.
                type: dict
                suboptions:
                    cloud_init:
                        description:
                            - >-
                              If this field is set, the guest will be customized using cloud-init. Either user_data or
                              custom_key_values should be provided. If custom_key_values are provided then the user
                              data will be generated using these key-value pairs.
                        type: dict
                        suboptions:
                            datasource_type:
                                description:
                                    - Type of datasource.
                                    - Default is C(CONFIG_DRIVE_V2).
                                type: str
                                choices:
                                    - CONFIG_DRIVE_V2
                            metadata:
                                description:
                                    - >-
                                      The contents of the meta_data configuration for cloud-init. This can be formatted
                                      as YAML or JSON. The value must be base64 encoded.
                                    - Maximum length is 32000 characters.
                                type: str
                            cloud_init_script:
                                description:
                                    - The script to use for cloud-init.
                                    - Only one of C(user_data) or C(custom_key_values) can be provided.
                                type: dict
                                suboptions:
                                    user_data:
                                        description:
                                            - >-
                                              The contents of the user_data configuration for cloud-init. This can be
                                              formatted as YAML, JSON, or could be a shell script. The value must be
                                              base64 encoded.
                                        type: dict
                                        suboptions:
                                            value:
                                                description:
                                                    - The value for the cloud-init user_data.
                                                    - Maximum length is 128000 characters.
                                                type: str
                                                required: true
                                    custom_key_values:
                                        description:
                                            - A collection of key/value pairs.
                                        type: dict
                                        suboptions:
                                            key_value_pairs:
                                                description:
                                                    - The list of the individual KeyValuePair elements.
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    name:
                                                        description:
                                                            - The key of the key-value pair.
                                                        type: str
                                                    value:
                                                        description:
                                                            - The value associated with the key for this key-value pair.
                                                        type: raw
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
- name: Deploy a VM from a VM profile
  nutanix.ncp.ntnx_vm_profile_deploy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11"
    vm_name: "vm-from-profile"
    vm_description: "VM deployed from a VM profile"
    cluster:
      ext_id: "00062e5f-9a19-0f5b-0000-000000028f57"
  register: result

- name: Deploy a VM from a VM profile with NICs, disks, categories and cloud-init
  nutanix.ncp.ntnx_vm_profile_deploy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11"
    vm_name: "vm-from-profile-full"
    cluster:
      ext_id: "00062e5f-9a19-0f5b-0000-000000028f57"
    categories:
      - ext_id: "6e50299a-b7c9-5c5c-9faf-246ee249c597"
    nics:
      - vm_profile_nic_ext_id: "5d0c9a4b-7a43-4d0e-9a2e-0d1b9f6a3c21"
        subnet:
          ext_id: "b1c3d5e7-1a2b-4c3d-8e9f-0a1b2c3d4e5f"
    disks:
      - backing_info:
          disk_size_bytes: 21474836480
          data_source:
            reference:
              image:
                image_ext_id: "c2d4e6f8-2b3c-4d5e-9f0a-1b2c3d4e5f60"
    guest_customization:
      config:
        cloud_init:
          datasource_type: CONFIG_DRIVE_V2
          cloud_init_script:
            user_data:
              value: "I2Nsb3VkLWNvbmZpZwpydW5jbWQ6CiAgLSBlY2hvIGhlbGxv"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for deploying a VM from a VM profile.
        - Task details.
    type: dict
    returned: always
    sample:
        {
            "completed_time": "2027-01-12T05:31:44.875612+00:00",
            "created_time": "2027-01-12T05:31:44.382175+00:00",
            "entities_affected": [
                {
                    "ext_id": "16023bcc-c1e2-4131-76eb-6bad6e0ddb66",
                    "name": "vm-from-profile",
                    "rel": "vmm:ahv:config:vm"
                },
                {
                    "ext_id": "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11",
                    "name": "ai.xlarge.h100.8gpu",
                    "rel": "vmm:ahv:config:vm-profile"
                }
            ],
            "ext_id": "ZXJnb24=:f1e19e35-8c51-53f5-a699-70dd11f8724d",
            "operation": "DeployVmFromVmProfile",
            "progress_percentage": 100,
            "status": "SUCCEEDED"
        }
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: when the VM profile is deployed
    sample: "ZXJnb24=:f1e19e35-8c51-53f5-a699-70dd11f8724d"
ext_id:
    description: The external ID of the VM profile.
    type: str
    returned: always
    sample: "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11"
vm_ext_id:
    description: The external ID of the deployed VM.
    type: str
    returned: when C(wait) is true and the VM is deployed
    sample: "16023bcc-c1e2-4131-76eb-6bad6e0ddb66"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error
    sample: "Api Exception raised while deploying VM from VM profile"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
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
    get_vm_profile_api_instance,
)

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    reference_spec = dict(
        ext_id=dict(type="str", required=True),
    )
    nic_spec = dict(
        vm_profile_nic_ext_id=dict(type="str"),
        subnet=dict(type="dict", options=reference_spec, obj=vmm_sdk.SubnetReference),
    )
    image_data_source_reference_spec = dict(
        image_ext_id=dict(type="str"),
    )
    data_source_reference_spec = dict(
        image=dict(type="dict", options=image_data_source_reference_spec),
    )
    data_source_spec = dict(
        reference=dict(
            type="dict",
            options=data_source_reference_spec,
            obj={
                "image": vmm_sdk.VmProfileDeployVmDiskImageDataSourceReference,
            },
        ),
    )
    disk_backing_info_spec = dict(
        disk_size_bytes=dict(type="int"),
        data_source=dict(
            type="dict",
            options=data_source_spec,
            obj=vmm_sdk.VmProfileDeployVmDiskDataSource,
        ),
    )
    disk_spec = dict(
        backing_info=dict(
            type="dict",
            options=disk_backing_info_spec,
            obj=vmm_sdk.VmProfileDeployVmDiskBackingInfo,
        ),
    )
    kvpair_spec = dict(
        name=dict(type="str"),
        value=dict(type="raw", no_log=False),
    )
    custom_key_values_spec = dict(
        key_value_pairs=dict(
            type="list",
            elements="dict",
            options=kvpair_spec,
            obj=vmm_sdk.KVPair,
            no_log=False,
        ),
    )
    user_data_spec = dict(
        value=dict(type="str", required=True),
    )
    cloud_init_script_spec = dict(
        user_data=dict(type="dict", options=user_data_spec),
        custom_key_values=dict(
            type="dict",
            options=custom_key_values_spec,
            no_log=False,
        ),
    )
    cloud_init_spec = dict(
        datasource_type=dict(type="str", choices=["CONFIG_DRIVE_V2"]),
        metadata=dict(type="str"),
        cloud_init_script=dict(
            type="dict",
            options=cloud_init_script_spec,
            obj={
                "user_data": vmm_sdk.Userdata,
                "custom_key_values": vmm_sdk.CustomKeyValues,
            },
            mutually_exclusive=[("user_data", "custom_key_values")],
            no_log=False,
        ),
    )
    guest_customization_config_spec = dict(
        cloud_init=dict(type="dict", options=cloud_init_spec),
    )
    guest_customization_spec = dict(
        config=dict(
            type="dict",
            options=guest_customization_config_spec,
            obj={
                "cloud_init": vmm_sdk.CloudInit,
            },
            no_log=False,
        ),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        vm_name=dict(type="str"),
        vm_description=dict(type="str"),
        project_ext_id=dict(type="str"),
        cluster=dict(
            type="dict", options=reference_spec, obj=vmm_sdk.AhvConfigClusterReference
        ),
        categories=dict(
            type="list",
            elements="dict",
            options=reference_spec,
            obj=vmm_sdk.AhvConfigCategoryReference,
        ),
        nics=dict(
            type="list",
            elements="dict",
            options=nic_spec,
            obj=vmm_sdk.VmProfileDeployVmNic,
        ),
        disks=dict(
            type="list",
            elements="dict",
            options=disk_spec,
            obj=vmm_sdk.VmProfileDeployVmDisk,
        ),
        guest_customization=dict(
            type="dict",
            options=guest_customization_spec,
            obj=vmm_sdk.VmProfileDeployVmGuestCustomizationParams,
            no_log=False,
        ),
    )
    return module_args


def deploy_vm_from_vm_profile(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.DeployVmFromVmProfileParams()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating deploy VM from VM profile spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.deploy_vm_from_vm_profile(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deploying VM from VM profile",
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
            result["vm_ext_id"] = vm_ext_id
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False, "ext_id": None}

    api_instance = get_vm_profile_api_instance(module)
    deploy_vm_from_vm_profile(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
