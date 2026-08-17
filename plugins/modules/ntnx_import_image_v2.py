#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_import_image_v2
short_description: Import images from a registered Prism Element cluster into Prism Central
version_added: 2.5.0
description:
  - This module imports one or more images that are locally owned by a registered
    Prism Element (PE) cluster into the Prism Central (PC) global image catalog.
  - Unlike VMs, images created directly on a PE via its native APIs are not
    automatically visible in the PC catalog. This action brings the image
    metadata into PC and transfers ownership of those images from PE to PC.
  - After a successful import, the referenced images can only be managed from
    Prism Central (create, update, delete) and no longer from the source
    Prism Element.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Import Images from Prism Element) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - The intended state for the module.
      - Only C(present) is supported for the import action; C(state=absent) will
        fail with a descriptive error (delete imported images via
        C(ntnx_images_v2) with C(state=absent) instead).
      - When C(state) is C(present) the referenced PE images are imported into PC.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  cluster_ext_id:
    description:
      - The external identifier of the registered Prism Element cluster that
        currently owns the images to be imported.
      - Required for the import action.
    type: str
    required: false
  images_ext_ids:
    description:
      - The list of external identifiers of the PE-owned images to import
        into Prism Central.
      - Required for the import action; must contain at least one image
        external identifier.
    type: list
    elements: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Import images from a registered Prism Element cluster
  nutanix.ncp.ntnx_import_image_v2:
    state: present
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    images_ext_ids:
      - "b9120f28-1222-3333-4444-47f7d5066e91"
      - "6b34522d-1231-8555-8888-1388aede0a06"
  register: import_result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for importing images from a Prism Element cluster into Prism Central.
    - If C(wait) is true, this holds the completed task details returned by the
      Nutanix task subsystem, including the C(entities_affected) list which
      identifies each imported image.
    - If C(wait) is false, this holds the initial task descriptor returned by
      the Import API.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
          "00062f19-1a4d-1e58-3b53-ac1f6b21bc6e"
      ],
      "completed_time": "2026-07-21T09:00:31.148000+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T09:00:20.412000+00:00",
      "entities_affected": [
          {
              "ext_id": "9d4bf6f4-0e8f-4f6c-93a7-70e12b95a8b1",
              "name": null,
              "rel": "vmm:content:image"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:5c6ec1d6-2b3b-4f47-9d70-2f0a1d1b98d6",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T09:00:31.148000+00:00",
      "legacy_error_message": null,
      "number_of_subtasks": 0,
      "operation": "import_image",
      "operation_description": "Import Image",
      "owned_by": null,
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2026-07-21T09:00:20.412000+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task orchestrating the import operation.
  returned: always
  type: str
  sample: "ZXJnb24=:5c6ec1d6-2b3b-4f47-9d70-2f0a1d1b98d6"

ext_id:
  description:
    - The external ID of the first imported image (extracted from the task's
      C(entities_affected) list).
    - Additional imported image identifiers are available in C(imported_image_ext_ids).
  returned: when the import task completes and at least one image is imported
  type: str
  sample: "9d4bf6f4-0e8f-4f6c-93a7-70e12b95a8b1"

imported_image_ext_ids:
  description:
    - The list of external IDs of all images imported into Prism Central by
      this import task, extracted from the completed task's C(entities_affected).
  returned: when the import task completes and at least one image is imported
  type: list
  elements: str
  sample:
    - "9d4bf6f4-0e8f-4f6c-93a7-70e12b95a8b1"
    - "d1e8c22a-3d0e-4f2a-97a7-e2acb1dc8ff4"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or in check mode
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
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import get_image_api_instance  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as virtual_machine_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as virtual_machine_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str"),
        images_ext_ids=dict(type="list", elements="str"),
    )
    return module_args


def _collect_imported_image_ext_ids(task):
    """Return the list of image ext_ids from the completed task's entities_affected."""
    entities_affected = getattr(task, "entities_affected", None) or []
    ext_ids = []
    for entity in entities_affected:
        rel = getattr(entity, "rel", None)
        ext_id = getattr(entity, "ext_id", None)
        if rel == TASK_CONSTANTS.RelEntityType.IMAGES and ext_id:
            ext_ids.append(ext_id)
    return ext_ids


def create_Image(module, result, api_instance):
    validate_required_params(module, ["cluster_ext_id", "images_ext_ids"])

    images_ext_ids = module.params.get("images_ext_ids") or []
    if len(images_ext_ids) == 0:
        module.fail_json(
            msg="images_ext_ids must contain at least one image external identifier",
            **result,
        )

    sg = SpecGenerator(module)
    default_spec = virtual_machine_management_sdk.ImageImportConfig()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating import image spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.import_image(body=spec)
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
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get imported image ext_ids from task for Image"
                ),
                msg="Failed to get imported image ext_ids from task for Image",
            )

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("cluster_ext_id", "images_ext_ids")),
        ],
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
        "task_ext_id": None,
    }

    api_instance = get_image_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        create_Image(module, result, api_instance)
    else:
        module.fail_json(
            msg="state=absent is not supported by ntnx_import_image_v2; "
            "delete imported images via ntnx_images_v2 with state=absent.",
            **result,
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
