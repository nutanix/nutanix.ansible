#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_generate_image_download_url_v2
short_description: Generate image download URL
version_added: "2.7.0"
description:
    - Generate image download URL for an image.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Generate image download URL) -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager, Super Admin, Tenant Admin, Tenant Consumer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will generate image download URL.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The External ID of the image.
        type: str
        required: true
    expiry_seconds:
        description:
            - Lifetime of the generated URL, in seconds. If not specified, the URL is valid for 600 seconds by default.
        type: int
        required: false
    preferred_location:
        description:
            - Preferred download source for the generated URL. If not specified, the backend selects the source automatically.
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
                            - The External ID of the cluster.
                        type: str
                        required: true
            content_repository_reference:
                description:
                    - A Content Repository as the preferred download source.
                type: dict
                required: false
                suboptions:
                    ext_id:
                        description:
                            - The External ID of the Content Repository.
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
- name: Generate image download URL with default expiry
  nutanix.ncp.ntnx_generate_image_download_url_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "12345678-1234-1234-1234-123456789012"
  register: result

- name: Generate image download URL with custom expiry
  nutanix.ncp.ntnx_generate_image_download_url_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "12345678-1234-1234-1234-123456789012"
    expiry_seconds: 900
  register: result

- name: Generate image download URL with preferred cluster location
  nutanix.ncp.ntnx_generate_image_download_url_v2:
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

- name: Generate image download URL with preferred content repository location
  nutanix.ncp.ntnx_generate_image_download_url_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "12345678-1234-1234-1234-123456789012"
    preferred_location:
      content_repository_reference:
        ext_id: "11111111-1111-1111-1111-111111111111"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for generating image download URL.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: dict
    sample:
        {
            "app_name": null,
            "batch_summary": null,
            "cluster_ext_ids": null,
            "completed_time": "2026-11-24T12:21:26.431857+00:00",
            "completion_details": [
                {
                    "name": "downloadUrl",
                    "value": "https://10.46.137.37:9440/entity_download/93fb157a-7efb-4a6d-8bc0-b3a6f70c069c?expires=1795523486&userid=00000000-0000-0000-0000-000000000000&username=admin&cluster=00066101-9650-faa8-0000-000000028f57&sig=CzqM58ddYOvnRqRGBqiiqdXRclc2p0qLmYHgGZVeLo0"
                }
            ],
            "created_time": "2026-11-24T12:21:26.358451+00:00",
            "entities_affected": [
                {
                    "ext_id": "93fb157a-7efb-4a6d-8bc0-b3a6f70c069c",
                    "name": "CentOS-7-cloudinit",
                    "rel": "vmm:content:image"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:e4329b0f-44a5-49eb-8197-4300ae55fd98",
            "is_background_task": false,
            "is_cancelable": false,
            "operation": "kGenerateImageDownloadUrl",
            "operation_description": "Generate Image Download URL",
            "progress_percentage": 100,
            "started_time": "2026-11-24T12:21:26.371015+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

ext_id:
    description: The external ID of the image.
    returned: always
    type: str
    sample: "93fb157a-7efb-4a6d-8bc0-b3a6f70c069c"

task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:e4329b0f-44a5-49eb-8197-4300ae55fd98"

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
    sample: "Api Exception raised while generating image download URL"
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
from ..module_utils.v4.vmm.api_client import get_image_api_instance  # noqa: E402

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

    content_repository_reference_spec = dict(ext_id=dict(type="str", required=True))

    preferred_location_spec = dict(
        cluster_reference=dict(
            type="dict",
            options=cluster_reference_spec,
            obj=vmm_sdk.ContentClusterReference,
        ),
        content_repository_reference=dict(
            type="dict",
            options=content_repository_reference_spec,
            obj=vmm_sdk.ContentRepositoryReference,
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
                "content_repository_reference": vmm_sdk.ContentRepositoryReference,
            },
            mutually_exclusive=[("cluster_reference", "content_repository_reference")],
        ),
    )
    return module_args


def generate_image_download_url(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.ImageGenerateDownloadUrlConfig()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating generate image download URL spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.generate_image_download_url(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while generating image download URL",
        )

    # data is TaskReference or error, handle success case
    if resp and resp.data:
        # TaskReference case
        try:
            task_ext_id = resp.data.ext_id
        except Exception:
            task_ext_id = None
        if task_ext_id:
            result["task_ext_id"] = task_ext_id
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        if result.get("task_ext_id") and module.params.get("wait"):
            task = wait_for_completion(module, result["task_ext_id"])
            result["response"] = strip_internal_attributes(task.to_dict())
    else:
        result["response"] = strip_internal_attributes(resp.to_dict()) if resp else {}

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
    api_instance = get_image_api_instance(module)
    generate_image_download_url(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
