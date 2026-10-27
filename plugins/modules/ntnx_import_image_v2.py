#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_import_image_v2
short_description: Import images from a registered Prism Element cluster into Prism Central
version_added: "2.7.0"
description:
    - Import images owned by a registered Prism Element cluster into the current Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Import images from Prism Element) -
      Required Roles: Prism Admin, Project Manager, Super Admin, Virtual Machine Admin,
      Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will import the referenced Prism Element images into Prism Central.
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    cluster_ext_id:
        description:
            - Cluster external identifier.
        type: str
        required: true
    images_ext_ids:
        description:
            - List of external identifiers for images that need to be imported.
        type: list
        elements: str
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
- name: Import images from a registered Prism Element cluster
  nutanix.ncp.ntnx_import_image_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "44cb13ea-4039-4952-a90a-65f808493637"
    images_ext_ids:
      - "b9c1e191-8237-4be9-986d-3a547c3c946c"
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
            "cluster_ext_ids": null,
            "completed_time": "2026-07-21T09:00:31.148000+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T09:00:20.412000+00:00",
            "entities_affected": [
                {
                    "ext_id": "9d4bf6f4-0e8f-4f6c-93a7-70e12b95a8b1",
                    "name": null,
                    "rel": "vmm:content:images"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:5c6ec1d6-2b3b-4f47-9d70-2f0a1d1b98d6",
            "is_background_task": false,
            "is_cancelable": false,
            "operation": "ImportImage",
            "operation_description": "Import Image",
            "progress_percentage": 100,
            "started_time": "2026-07-21T09:00:20.412000+00:00",
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
    description: The external ID of the first imported image.
    returned: when the import task completes and at least one image is imported
    type: str
    sample: "9d4bf6f4-0e8f-4f6c-93a7-70e12b95a8b1"

cluster_ext_id:
    description: The external ID of the Prism Element cluster.
    returned: always
    type: str
    sample: "44cb13ea-4039-4952-a90a-65f808493637"

imported_image_ext_ids:
    description:
        - The list of external IDs of images imported into Prism Central by this import task.
    returned: when the import task completes and at least one image is imported
    type: list
    elements: str
    sample:
        - "9d4bf6f4-0e8f-4f6c-93a7-70e12b95a8b1"

task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:5c6ec1d6-2b3b-4f47-9d70-2f0a1d1b98d6"

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
    returned: When there is an error or in check mode operation
    type: str
    sample: "Api Exception raised while importing images from Prism Element"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
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
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str", required=True),
        images_ext_ids=dict(type="list", elements="str", required=True),
    )
    return module_args


def _collect_imported_image_ext_ids(task):
    """Return image ext_ids from the completed task's entities_affected."""
    entities_affected = getattr(task, "entities_affected", None) or []
    ext_ids = []
    for entity in entities_affected:
        rel = getattr(entity, "rel", None)
        ext_id = getattr(entity, "ext_id", None)
        if rel == TASK_CONSTANTS.RelEntityType.IMAGES and ext_id:
            ext_ids.append(ext_id)
    return ext_ids


def import_image(module, result):
    images = get_image_api_instance(module)
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.ImageImportConfig()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating import image spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = images.import_image(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while importing images from Prism Element",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        imported_ext_ids = _collect_imported_image_ext_ids(task)
        if imported_ext_ids:
            result["imported_image_ext_ids"] = imported_ext_ids
            result["ext_id"] = imported_ext_ids[0]

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
        "response": None,
        "ext_id": None,
    }
    import_image(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
