#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_images_migrate_v2
short_description: Migrate an image to a content repository using v4 APIs
version_added: "2.7.0"
description:
    - Migrate an existing image into a content repository.
    - This module uses PC v4 VMM APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Migrate Image Content Repository) -
      Required Roles: Prism Admin, Project Admin, Project Manager, Super Admin, Tenant Admin, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - The external identifier of the image to migrate.
        type: str
        required: true
    content_repository_ext_id:
        description:
            - The external identifier of the content repository to migrate the image into.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Migrate an image to a content repository
  nutanix.ncp.ntnx_images_migrate_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "015e6709-d4a6-44bd-8df7-9898f062635b"
    content_repository_ext_id: "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d"
  register: result
"""

RETURN = r"""
response:
    description:
        - Task details when C(wait) is false.
        - Task status when C(wait) is true.
    returned: always
    type: dict
    sample: {
            "app_name": null,
            "batch_summary": null,
            "cluster_ext_ids": null,
            "completed_time": "2026-09-21T09:54:39.500000+00:00",
            "completion_details": null,
            "created_time": "2026-09-21T09:54:00.000000+00:00",
            "entities_affected": [
                {
                    "ext_id": "015e6709-d4a6-44bd-8df7-9898f062635b",
                    "name": "my-image",
                    "rel": "vmm:content:images"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:a0d8956a-4cc4-43aa-9715-897b5468dd57",
            "is_background_task": false,
            "is_cancelable": false,
            "operation": "MigrateImage",
            "operation_description": "Migrate Image",
            "progress_percentage": 100,
            "started_time": "2026-09-21T09:54:00.100000+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

ext_id:
    description: The external ID of the image.
    returned: always
    type: str
    sample: "015e6709-d4a6-44bd-8df7-9898f062635b"

content_repository_ext_id:
    description: The external ID of the content repository.
    returned: always
    type: str
    sample: "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d"

task_ext_id:
    description: The external ID of the task created for the operation.
    returned: always
    type: str
    sample: "ZXJnb24=:a0d8956a-4cc4-43aa-9715-897b5468dd57"

error:
    description: This field holds information about errors that occurred during the task execution.
    returned: When an error occurs
    type: str

failed:
    description: This indicates whether the task failed.
    returned: When something fails
    type: bool
    sample: true
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        content_repository_ext_id=dict(type="str", required=True),
    )
    return module_args


def migrate_image(module, result):
    images = get_image_api_instance(module)
    ext_id = module.params.get("ext_id")
    content_repository_ext_id = module.params.get("content_repository_ext_id")
    result["ext_id"] = ext_id
    result["content_repository_ext_id"] = content_repository_ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.ImageMigrateConfig()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating migrate image spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = images.migrate_image(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while migrating image to content repository",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

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
        "failed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    migrate_image(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
