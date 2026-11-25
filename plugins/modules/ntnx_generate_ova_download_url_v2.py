#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_generate_ova_download_url_v2
short_description: Generate OVA download URL
version_added: "2.7.0"
description:
    - Generate OVA download URL for an OVA.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Generate OVA download URL) -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager, Super Admin, Tenant Admin, Tenant Consumer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will generate OVA download URL.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier for an OVA.
        type: str
        required: true
    expiry_seconds:
        description:
            - Lifetime of the generated URL, in seconds. If not specified, the URL is valid for 600 seconds by default.
        type: int
        required: false
    preferred_location:
        description:
            - Preferred Prism Element cluster to use as the download source for the generated URL.
            - If not specified, the backend selects the source automatically.
        type: dict
        required: false
        suboptions:
            cluster_reference:
                description:
                    - A PE cluster as the preferred download source.
                type: dict
                required: false
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the cluster.
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
- name: Generate OVA download URL with default expiry
  nutanix.ncp.ntnx_generate_ova_download_url_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "12345678-1234-1234-1234-123456789012"
  register: result

- name: Generate OVA download URL with custom expiry
  nutanix.ncp.ntnx_generate_ova_download_url_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "12345678-1234-1234-1234-123456789012"
    expiry_seconds: 900
  register: result

- name: Generate OVA download URL with preferred cluster location
  nutanix.ncp.ntnx_generate_ova_download_url_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "12345678-1234-1234-1234-123456789012"
    expiry_seconds: 1200
    preferred_location:
      cluster_reference:
        ext_id: "00000000-0000-0000-0000-000000000000"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for generating OVA download URL.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-09-21T09:54:39.500000+00:00",
            "completion_details": null,
            "created_time": "2026-09-21T09:54:00.000000+00:00",
            "entities_affected": [
                {
                    "ext_id": "015e6709-d4a6-44bd-8df7-9898f062635b",
                    "rel": "vmm:content:ova"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:a0d8956a-4cc4-43aa-9715-897b5468dd57",
            "is_cancelable": false,
            "operation": "GenerateOvaDownloadUrl",
            "operation_description": "Generate OVA download URL",
            "progress_percentage": 100,
            "started_time": "2026-09-21T09:54:00.100000+00:00",
            "status": "SUCCEEDED",
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

ext_id:
    description: The external ID of the OVA.
    returned: always
    type: str
    sample: "015e6709-d4a6-44bd-8df7-9898f062635b"

task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:a0d8956a-4cc4-43aa-9715-897b5468dd57"

error:
    description: This indicates the error message if any error occurred
    returned: When an error occurs
    type: str

failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while generating OVA download URL"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_ova_api_instance  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    cluster_reference_spec = dict(ext_id=dict(type="str", required=True))

    preferred_location_spec = dict(
        cluster_reference=dict(
            type="dict",
            options=cluster_reference_spec,
            obj=vmm_sdk.ContentClusterReference,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        expiry_seconds=dict(type="int"),
        preferred_location=dict(
            type="dict",
            options=preferred_location_spec,
            obj={
                "cluster_reference": vmm_sdk.ContentClusterReference,
            },
        ),
    )
    return module_args


def generate_ova_download_url(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.OvaGenerateDownloadUrlConfig()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating generate OVA download URL spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.generate_ova_download_url(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while generating OVA download URL",
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
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_ova_api_instance(module)
    generate_ova_download_url(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
