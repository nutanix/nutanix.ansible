#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: ntnx_vms_stage_guest_customization_v2
short_description: Stage guest customization configuration for a Nutanix VM
description:
    - This module stages guest customization configuration for a Nutanix VM.
version_added: "2.0.0"
options:
    ext_id:
        description:
            - The external ID of the VM.
        type: str
        required: true
    config:
        description:
            - The guest customization configuration.
        type: dict
        suboptions:
            sysprep:
                description:
                    - The Sysprep configuration.
                type: dict
                suboptions:
                    install_type:
                        description:
                            - The Sysprep installation type.
                        type: str
                        choices:
                            - FRESH
                            - PREPARED
                    sysprep_script:
                        description:
                            - The Sysprep script configuration.
                        type: dict
                        suboptions:
                            unattendxml:
                                description:
                                    - The path to the unattend.xml file.
                                type: dict
                                suboptions:
                                    value:
                                        description:
                                            - The value of the unattend.xml file.
                                        type: str
                            custom_key_values:
                                description:
                                    - The custom key-value pairs for Sysprep.
                                type: dict
                                suboptions:
                                    key_value_pairs:
                                        description:
                                            - The list of key-value pairs.
                                        type: list
                                        elements: dict
                                        suboptions:
                                            name:
                                                description:
                                                    - The name of the key-value pair.
                                                type: str
                                            value:
                                                description:
                                                    - The value of the key-value pair.
                                                type: raw
            cloudinit:
                description:
                    - The CloudInit configuration.
                type: dict
                suboptions:
                    datasource_type:
                        description:
                            - The type of the CloudInit datasource.
                        type: str
                        choices:
                            - CONFIG_DRIVE_V2
                    metadata:
                        description:
                            - The metadata for CloudInit.
                        type: str
                    cloud_init_script:
                        description:
                            - The CloudInit script configuration.
                        type: dict
                        suboptions:
                            user_data:
                                description:
                                    - The user data for CloudInit.
                                type: dict
                                suboptions:
                                    value:
                                        description:
                                            - The value of the user data.
                                        type: str
                                        required: true
                            custom_key_values:
                                description:
                                    - The custom key-value pairs for CloudInit.
                                type: dict
                                suboptions:
                                    key_value_pairs:
                                        description:
                                            - The list of key-value pairs.
                                        type: list
                                        elements: dict
                                        suboptions:
                                            name:
                                                description:
                                                    - The name of the key-value pair.
                                                type: str
                                            value:
                                                description:
                                                    - The value of the key-value pair.
                                                type: raw
author:
 - Prem Karat (@premkarat)
 - Alaa Bishtawi (@alaa-bish)
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""
EXAMPLES = r"""
- name: Update guest script
  nutanix.ncp.ntnx_vms_stage_guest_customization_v2:
    ext_id: "7334f142-9653-4c84-7287-3c758d1a0aeb"
    config:
      cloudinit:
        datasource_type: CONFIG_DRIVE_V2
        cloud_init_script:
          user_data:
            value: I2Nsb3VkLWNvbmZpZwpkaXNhYmxlX3Jvb3Q6IGZhbHNlCnNzaF9wd2F1dGg6ICAgdHJ1ZQ==
  register: result
"""

RETURN = r"""
---
response:
    description:
        - Response for update guest customization configuration.
        - Task details status
    type: dict
    returned: always
    sample:
      {
            "cluster_ext_ids": [
                "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
            ],
            "completed_time": "2024-07-15T07:49:15.629543+00:00",
            "completion_details": null,
            "created_time": "2024-07-15T07:49:14.348791+00:00",
            "entities_affected": [
                {
                    "ext_id": "7334f142-9653-4c84-7287-3c758d1a0aeb",
                    "rel": "vmm:ahv:vm"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:faeab3ca-3dbc-5384-867b-afa179822b79",
            "is_cancelable": false,
            "last_updated_time": "2024-07-15T07:49:15.629542+00:00",
            "legacy_error_message": null,
            "operation": "CustomizeGuest",
            "operation_description": null,
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2024-07-15T07:49:14.371537+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:5e3ed0ac-c573-5f52-b72f-bc47185c7910",
                    "href": "https://10.51.144.57:9440/api/prism/v4.0.b1/config/tasks/ZXJnb24=:5e3ed0ac-c573-5f52-b72f-bc47185c7910",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }
task_ext_id:
    description:
        - The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:faeab3ca-3dbc-5384-867b-afa179822b79"
ext_id:
    description:
        - The external ID of the VM.
    type: str
    returned: always
    sample: "7334f142-9653-4c84-7287-3c758d1a0aeb"
changed:
    description:
        - Indicates whether the guest customization configuration was changed.
    type: bool
    returned: always
    sample: true
error:
    description:
        - The error message.
    type: str
    returned: always
failed:
    description:
        - Indicates whether the task failed.
    type: bool
    returned: always
    sample: false
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
        ext_id=dict(type="str", required=True),
        config=dict(
            type="dict",
            options=vm_specs.get_gc_param_spec(),
            obj=vm_specs.get_gc_allowed_types_spec(),
        ),
    )

    return module_args


def stage_customize_guest(module, result):
    vms = get_vm_api_instance(module)
    ext_id = module.params["ext_id"]
    result["ext_id"] = ext_id

    vm = get_vm(module, vms, ext_id=ext_id)

    etag = get_etag(data=vm)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for stage guest customization configuration", **result
        )

    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.GuestCustomizationParams()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating stage guest customization configuration spec",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.customize_guest_vm(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while staging guest customization configuration",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id, True)
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
    stage_customize_guest(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
