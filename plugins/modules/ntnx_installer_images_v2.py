#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_installer_images_v2
short_description: Create, Update and Delete LCM installer images on Nutanix Foundation Central (FCVM)
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete Life Cycle Management (LCM) installer images.
  - An installer image is an LCM image (AHV, AOS or ESX) used to image or upgrade nodes.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create installer image) -
      Required Roles: Super Admin
    - >-
      B(Update installer image) -
      Required Roles: Super Admin
    - >-
      B(Delete installer image) -
      Required Roles: Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided, the operation is create installer image.
      - If C(state) is set to C(present) and C(ext_id) is provided, the operation is update installer image.
      - If C(state) is set to C(absent) and C(ext_id) is provided, the operation is delete installer image.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the installer image.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the installer image.
      - Required for create operation.
    type: str
    required: false
  type:
    description:
      - Type of the installer image.
      - Required for create operation.
    type: str
    required: false
    choices:
      - AHV
      - AOS
      - ESX
  source:
    description:
      - Source of the image: LOCAL (image managed and hosted by Foundation Central),
        REMOTE_URL (image hosted outside of Foundation Central,
        and nodes will download the image from the given URL at the time of imaging)
      - Required for create operation.
    type: str
    required: false
    choices:
      - LOCAL
      - REMOTE_URL
  url:
    description:
      - URL from which the installer image file will be downloaded.
      - Applicable when C(source) is C(REMOTE_URL).
    type: str
    required: false
  checksum:
    description:
      - Checksum of the installer image.
      - Required and applicable only for AHV images.
      - Provide exactly one of C(md5) or C(sha256).
    type: dict
    required: false
    suboptions:
      md5:
        description:
          - MD5 checksum of the image.
        type: dict
        required: false
        suboptions:
          hex_digest:
            description:
              - MD5 checksum value in hexadecimal format (32 characters).
            type: str
            required: true
      sha256:
        description:
          - SHA-256 checksum of the image.
        type: dict
        required: false
        suboptions:
          hex_digest:
            description:
              - SHA-256 checksum value in hexadecimal format (64 characters).
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
- name: Create installer image
  nutanix.ncp.ntnx_installer_images_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ foundation_username }}"
    nutanix_password: "{{ foundation_password }}"
    validate_certs: false
    state: present
    name: "ahv_image_ansible"
    type: "AHV"
    source: "REMOTE_URL"
  register: result
  ignore_errors: true

- name: Update installer image with all attributes
  nutanix.ncp.ntnx_installer_images_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ foundation_username }}"
    nutanix_password: "{{ foundation_password }}"
    validate_certs: false
    state: present
    ext_id: "d1f27805-4ce3-9212-2ca4-e4b4d258fe9c"
    name: "ahv_image_ansible"
    type: "AHV"
    source: "REMOTE_URL"
    url: "https://download.example.com/ahv/host-bundle-el8.nutanix.20230302.el8.x86_64.tar.gz"
    checksum:
      sha256:
        hex_digest: "a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90"
  register: result
  ignore_errors: true

- name: Delete installer image
  nutanix.ncp.ntnx_installer_images_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ foundation_username }}"
    nutanix_password: "{{ foundation_password }}"
    validate_certs: false
    state: absent
    ext_id: "d1f27805-4ce3-9212-2ca4-e4b4d258fe9c"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting an installer image.
    - If the operation is create or update and C(wait) is true, it returns the installer image details.
    - If the operation is create or update and C(wait) is false, it returns the task details.
    - If the operation is delete, it returns the task details.
  returned: always
  type: dict
  sample:
    {
      "checksum": {
          "hex_digest": "a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90"
      },
      "created_time": "2026-09-09T05:50:00.000000+00:00",
      "ext_id": "d1f27805-4ce3-9212-2ca4-e4b4d258fe9c",
      "file_status": "URL_AVAILABLE",
      "links": null,
      "metadata_status": "NOT_AVAILABLE",
      "name": "ahv_image_ansible",
      "source": "REMOTE_URL",
      "tenant_id": null,
      "type": "AHV",
      "url": "https://download.example.com/ahv/host-bundle-el8.nutanix.20230302.el8.x86_64.tar.gz",
      "version": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the installer image.
  returned: always
  type: str
  sample: "d1f27805-4ce3-9212-2ca4-e4b4d258fe9c"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency.
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false

msg:
  description: This indicates the status/error message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating installer image"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_etag,
    get_installer_images_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_installer_image  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    md5_checksum_spec = dict(
        hex_digest=dict(type="str", required=True),
    )

    sha256_checksum_spec = dict(
        hex_digest=dict(type="str", required=True),
    )

    checksum_spec = dict(
        md5=dict(
            type="dict",
            options=md5_checksum_spec,
            obj=lifecycle_sdk.ImageMd5Checksum,
        ),
        sha256=dict(
            type="dict",
            options=sha256_checksum_spec,
            obj=lifecycle_sdk.ImageSha256Checksum,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        type=dict(
            type="str",
            choices=["AHV", "AOS", "ESX"],
            obj=lifecycle_sdk.ImageType,
        ),
        source=dict(
            type="str",
            choices=["LOCAL", "REMOTE_URL"],
            obj=lifecycle_sdk.ImageSource,
        ),
        url=dict(type="str"),
        checksum=dict(
            type="dict",
            options=checksum_spec,
            mutually_exclusive=[("md5", "sha256")],
            obj={
                "md5": lifecycle_sdk.ImageMd5Checksum,
                "sha256": lifecycle_sdk.ImageSha256Checksum,
            },
        ),
    )
    return module_args


READ_ONLY_FIELDS = [
    "file_status",
    "metadata_status",
    "version",
    "created_time",
    "links",
]


def create_installer_image(module, result, api_instance):
    validate_required_params(module, ["name", "type", "source"])
    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.ConfigImage()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create installer image spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_image(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating installer image",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_resp, rel=TASK_CONSTANTS.RelEntityType.INSTALLER_IMAGE
        )
        if ext_id:
            result["ext_id"] = ext_id
            image = get_installer_image(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(image.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Installer Image"
                ),
                msg="Failed to get entity ext_id from task for Installer Image",
            )

    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    for key in READ_ONLY_FIELDS:
        old_spec_dict.pop(key, None)
        update_spec_dict.pop(key, None)
    return old_spec_dict == update_spec_dict


def update_installer_image(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_installer_image(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating installer image", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update installer image spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_image_by_id(extId=ext_id, body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating installer image",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        image = get_installer_image(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(image.to_dict())
    result["changed"] = True


def delete_installer_image(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Installer image with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return
    resp = None
    try:
        resp = api_instance.delete_image_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting installer image",
        )
    task_ext_id = getattr(resp.data, "ext_id", None) if resp else None
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    api_instance = get_installer_images_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_installer_image(module, result, api_instance)
        else:
            create_installer_image(module, result, api_instance)
    else:
        delete_installer_image(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
