#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_profile_v2
short_description: Update a VM profile in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Update the VM configuration of a VM profile in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update a Virtual Machine Profile) -
      Required Roles: Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - Specify state.
            - If C(state) is set to C(present), the VM profile identified by C(ext_id) is updated.
            - If C(state) is set to C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external ID (UUID) of the VM profile.
        type: str
        required: true
    vm_configuration:
        description:
            - VM configuration settings of the VM Profile.
        type: dict
        suboptions:
            memory_size_bytes:
                description:
                    - Memory size in bytes.
                type: int
            num_cores:
                description:
                    - Number of CPU cores.
                type: int
            nics:
                description:
                    - Information about the NICs inside the VM Profile.
                    - >-
                      Just alone, this is not sufficient to create a NIC object for the VM. The NIC object is created by
                      combining this information with the information from the NIC details provided during the
                      deployment of the VM.
                type: list
                elements: dict
                suboptions:
                    backing_info:
                        description:
                            - Backing information for the VM Profile NIC.
                        type: dict
                        suboptions:
                            dp_offload_nic:
                                description:
                                    - Backing information for the VM Profile DP Offload NIC.
                                type: dict
                                suboptions:
                                    nic_profile_reference:
                                        description:
                                            - Reference to a NIC profile.
                                        type: dict
                                        suboptions:
                                            ext_id:
                                                description:
                                                    - Globally unique identifier of a NIC profile. It should be of type UUID.
                                                type: str
                                                required: true
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
- name: Update the VM configuration of a VM profile
  nutanix.ncp.ntnx_vm_profile_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11"
    vm_configuration:
      memory_size_bytes: 8589934592
      num_cores: 4
  register: result

- name: Update the NICs of a VM profile
  nutanix.ncp.ntnx_vm_profile_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11"
    vm_configuration:
      nics:
        - backing_info:
            dp_offload_nic:
              nic_profile_reference:
                ext_id: "8f897185-e5ee-46ac-82ad-e8945f8687f4"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for updating a VM profile.
        - VM profile details if C(wait) is true.
        - Task details if C(wait) is false.
    type: dict
    returned: always
    sample:
        {
            "description": "VM profile for GPU workloads",
            "ext_id": "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11",
            "links": null,
            "name": "ai.xlarge.h100.8gpu",
            "project_ext_id": "26ff200c-e24c-47f7-809b-00a571fe7ecc",
            "shared_with_projects": null,
            "tenant_id": null,
            "update_time": "2027-01-12T07:13:52.055646+00:00",
            "updated_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000"
            },
            "vm_configuration": {
                "memory_size_bytes": 8589934592,
                "nics": [
                    {
                        "backing_info": {
                            "nic_profile_reference": {
                                "ext_id": "8f897185-e5ee-46ac-82ad-e8945f8687f4"
                            }
                        },
                        "ext_id": "5d0c9a4b-7a43-4d0e-9a2e-0d1b9f6a3c21"
                    }
                ],
                "num_cores": 4
            }
        }
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: when the VM profile is updated
    sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
ext_id:
    description: The external ID of the VM profile.
    type: str
    returned: always
    sample: "a4c0a5d2-6e2f-4a52-9d3e-5d7b1f1c8e11"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
skipped:
    description: This indicates whether the task was skipped
    type: bool
    returned: when the module is idempotent
    sample: false
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
    returned: When there is an error or module is idempotent
    sample: "Nothing to change."
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
    strip_read_only_fields,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_etag,
    get_vm_profile_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_vm_profile  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

_VM_PROFILE_READ_ONLY_FIELDS = (
    "name",
    "description",
    "project_ext_id",
    "shared_with_projects",
    "update_time",
    "updated_by",
)


def get_module_spec():
    nic_profile_reference_spec = dict(
        ext_id=dict(type="str", required=True),
    )
    dp_offload_nic_spec = dict(
        nic_profile_reference=dict(
            type="dict",
            options=nic_profile_reference_spec,
            obj=vmm_sdk.NicProfileReference,
        ),
    )
    nic_backing_info_spec = dict(
        dp_offload_nic=dict(type="dict", options=dp_offload_nic_spec),
    )
    nic_spec = dict(
        backing_info=dict(
            type="dict",
            options=nic_backing_info_spec,
            obj={
                "dp_offload_nic": vmm_sdk.VmProfileDpOffloadNicBackingInfo,
            },
        ),
    )
    vm_configuration_spec = dict(
        memory_size_bytes=dict(type="int"),
        num_cores=dict(type="int"),
        nics=dict(
            type="list",
            elements="dict",
            options=nic_spec,
            obj=vmm_sdk.VmProfileNic,
        ),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        vm_configuration=dict(
            type="dict",
            options=vm_configuration_spec,
            obj=vmm_sdk.VmProfileVmConfiguration,
        ),
    )
    return module_args


def check_idempotency(current_spec, update_spec):
    strip_internal_attributes(current_spec)
    strip_internal_attributes(update_spec)
    return current_spec == update_spec


def update_vm_profile(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_vm_profile(module, api_instance, ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VM profile update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating VM profile", **result
        )

    strip_read_only_fields(update_spec, fields=_VM_PROFILE_READ_ONLY_FIELDS)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.update_vm_profile_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating VM profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_vm_profile(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
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
    update_vm_profile(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
