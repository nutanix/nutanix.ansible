#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_bundle_v2
short_description: Create and delete LCM bundles in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create and delete LCM (Life Cycle Manager) bundles in Nutanix Prism Central.
  - LCM bundles are packaged payloads that contain software binaries, firmware updates, or the
    LCM framework itself. They are the direct-upload payload used by dark-site / air-gapped clusters.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create an LCM bundle) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - >-
    B(Delete an LCM bundle) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create LCM bundle.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete LCM bundle.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the LCM bundle.
      - Required for delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the LCM bundle.
      - This is the file/object name of the uploaded bundle (for example the S3 object key when the
        bundle is uploaded to the Prism Central Objects Lite C(lcm-bundles) bucket).
      - Required for create operation.
    type: str
    required: false
  size_bytes:
    description:
      - Size of the LCM bundle in bytes.
    type: int
    required: false
  type:
    description:
      - Type / category of the LCM bundle.
      - Required for create operation.
      - The C(FRAMEWORK) bundle must be uploaded and inventoried before other bundle types can be used.
    type: str
    required: false
    choices:
      - FIRMWARE
      - FRAMEWORK
      - PRODUCT_META
      - SOFTWARE
  vendor:
    description:
      - Vendor of the LCM bundle.
      - Required for create operation.
    type: str
    required: false
    choices:
      - NUTANIX
      - THIRD_PARTY
  cluster_ext_id:
    description:
      - External ID of the Prism Element cluster to which the bundle belongs.
      - When not provided, the bundle is scoped to the Prism Central serving the request.
    type: str
    required: false
  checksum:
    description:
      - Checksum used to verify the uploaded LCM bundle.
      - Exactly one of C(md5_sum) or C(sha256_sum) must be provided.
    type: dict
    required: false
    suboptions:
      md5_sum:
        description:
          - MD5 checksum of the LCM bundle.
        type: dict
        required: false
        suboptions:
          hex_digest:
            description:
              - Hexadecimal MD5 digest of the LCM bundle.
            type: str
            required: true
      sha256_sum:
        description:
          - SHA-256 checksum of the LCM bundle.
        type: dict
        required: false
        suboptions:
          hex_digest:
            description:
              - Hexadecimal SHA-256 digest of the LCM bundle.
            type: str
            required: true
  images:
    description:
      - List of LCM images that make up the bundle.
    type: list
    elements: dict
    required: false
    suboptions:
      release_notes:
        description:
          - Release notes for the LCM image.
        type: str
        required: false
      spec_version:
        description:
          - Specification version of the LCM image.
        type: str
        required: false
      is_qualified:
        description:
          - Whether this LCM image is qualified.
        type: bool
        required: false
      status:
        description:
          - Availability / lifecycle status of the LCM image version.
        type: str
        required: false
        choices:
          - AVAILABLE
          - CRITICAL
          - DEPRECATED
          - EMERGENCY
          - ESTS
          - LATEST
          - LTS
          - RECOMMENDED
          - STS
      entity_class:
        description:
          - LCM entity class (for example C(AOS)).
        type: str
        required: false
      entity_model:
        description:
          - LCM entity model.
        type: str
        required: false
      entity_type:
        description:
          - Type of the LCM entity contained in the image.
        type: str
        required: false
        choices:
          - FIRMWARE
          - SOFTWARE
      entity_version:
        description:
          - Version string of the LCM entity contained in the image.
        type: str
        required: false
      hardware_family:
        description:
          - Hardware family for which this image is applicable.
        type: str
        required: false
      cluster_ext_id:
        description:
          - Cluster external ID for which this image is applicable.
        type: str
        required: false
      files:
        description:
          - List of files that make up the LCM image.
        type: list
        elements: dict
        required: false
        suboptions:
          file_location_id:
            description:
              - Image file global catalog item UUID.
            type: str
            required: false
          name:
            description:
              - Name of the image file.
            type: str
            required: false
          size_bytes:
            description:
              - Size of the image file in bytes.
            type: int
            required: false
          file_path:
            description:
              - Path of the image file within the bundle.
            type: str
            required: false
          checksum_type:
            description:
              - Type of the checksum used for the image file.
            type: str
            required: false
            choices:
              - HEX_MD5
              - SHASUM
          checksum:
            description:
              - Checksum digest of the image file.
            type: str
            required: false
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
- name: Create an LCM software bundle (minimum required fields)
  nutanix.ncp.ntnx_lcm_bundle_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "lcm-bundle-ansible.tar.gz"
    type: "SOFTWARE"
  register: bundle_min
  ignore_errors: true

- name: Create an LCM firmware bundle with all attributes
  nutanix.ncp.ntnx_lcm_bundle_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "lcm-firmware-bundle-ansible.tar.gz"
    size_bytes: 12345678
    type: "FIRMWARE"
    vendor: "NUTANIX"
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    checksum:
      sha256_sum:
        hex_digest: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    images:
      - release_notes: "Firmware bundle release notes"
        spec_version: "1"
        is_qualified: true
        status: "RECOMMENDED"
        entity_class: "AOS"
        entity_model: "AOS"
        entity_type: "FIRMWARE"
        entity_version: "7.0.0"
        hardware_family: "NX"
        cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
        files:
          - file_location_id: "b7c3f61e-0f4b-4c1c-8a52-4f8f2e7e2e3f"
            name: "firmware.bin"
            size_bytes: 12345678
            file_path: "firmware/firmware.bin"
            checksum_type: "SHASUM"
            checksum: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  register: bundle_full
  ignore_errors: true

- name: Delete an LCM bundle
  nutanix.ncp.ntnx_lcm_bundle_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "9c0a9f4a-2b7e-4f10-8f34-2b3c7a1e9a5c"
  register: bundle_delete
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating or deleting an LCM bundle.
    - If the operation is create and C(wait) is true, it will return the LCM bundle details.
    - If the operation is create and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "checksum": null,
      "cluster_ext_id": null,
      "ext_id": "9c0a9f4a-2b7e-4f10-8f34-2b3c7a1e9a5c",
      "images": null,
      "links": null,
      "name": "lcm-bundle-ansible.tar.gz",
      "size_bytes": null,
      "tenant_id": null,
      "type": "SOFTWARE",
      "vendor": "NUTANIX"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the LCM bundle.
  returned: always
  type: str
  sample: "9c0a9f4a-2b7e-4f10-8f34-2b3c7a1e9a5c"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: always
  type: bool
  sample: false

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
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating LCM bundle"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_bundles_api_instance  # noqa: E402
from ..module_utils.v4.lcm.helpers import get_lcm_bundle  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as life_cycle_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as life_cycle_management_sdk,
    )

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
        md5_sum=dict(
            type="dict",
            options=md5_checksum_spec,
            required=False,
            obj=life_cycle_management_sdk.LcmMd5Sum,
        ),
        sha256_sum=dict(
            type="dict",
            options=sha256_checksum_spec,
            required=False,
            obj=life_cycle_management_sdk.LcmSha256Sum,
        ),
    )

    image_file_spec = dict(
        file_location_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        size_bytes=dict(type="int", required=False),
        file_path=dict(type="str", required=False),
        checksum_type=dict(
            type="str",
            required=False,
            choices=["HEX_MD5", "SHASUM"],
            obj=life_cycle_management_sdk.CheckSumType,
        ),
        checksum=dict(type="str", required=False),
    )

    image_spec = dict(
        release_notes=dict(type="str", required=False),
        spec_version=dict(type="str", required=False),
        is_qualified=dict(type="bool", required=False),
        status=dict(
            type="str",
            required=False,
            choices=[
                "AVAILABLE",
                "CRITICAL",
                "DEPRECATED",
                "EMERGENCY",
                "ESTS",
                "LATEST",
                "LTS",
                "RECOMMENDED",
                "STS",
            ],
            obj=life_cycle_management_sdk.AvailableVersionStatus,
        ),
        entity_class=dict(type="str", required=False),
        entity_model=dict(type="str", required=False),
        entity_type=dict(
            type="str",
            required=False,
            choices=["FIRMWARE", "SOFTWARE"],
            obj=life_cycle_management_sdk.EntityType,
        ),
        entity_version=dict(type="str", required=False),
        hardware_family=dict(type="str", required=False),
        cluster_ext_id=dict(type="str", required=False),
        files=dict(
            type="list",
            elements="dict",
            required=False,
            options=image_file_spec,
            obj=life_cycle_management_sdk.ImageFile,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        size_bytes=dict(type="int"),
        type=dict(
            type="str",
            choices=["FIRMWARE", "FRAMEWORK", "PRODUCT_META", "SOFTWARE"],
            obj=life_cycle_management_sdk.BundleType,
        ),
        vendor=dict(
            type="str",
            choices=["NUTANIX", "THIRD_PARTY"],
            obj=life_cycle_management_sdk.BundleVendor,
        ),
        cluster_ext_id=dict(type="str"),
        checksum=dict(
            type="dict",
            options=checksum_spec,
            obj={
                "md5_sum": life_cycle_management_sdk.LcmMd5Sum,
                "sha256_sum": life_cycle_management_sdk.LcmSha256Sum,
            },
        ),
        images=dict(
            type="list",
            elements="dict",
            options=image_spec,
            obj=life_cycle_management_sdk.Image,
        ),
    )
    return module_args


def _get_existing_bundle_by_name(module, api_instance, name):
    """Return the first LCM bundle matching the given name, else None."""
    try:
        resp = api_instance.list_bundles(_filter="name eq '{0}'".format(name))
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while checking existing LCM bundle by name",
        )
    data = getattr(resp, "data", None)
    if not data:
        return None
    return data[0]


def create_Bundle(module, result, api_instance):
    validate_required_params(module, ["name", "type", "vendor"])

    checksum = module.params.get("checksum")
    if checksum and checksum.get("md5_sum") and checksum.get("sha256_sum"):
        module.fail_json(
            msg="parameters are mutually exclusive: checksum.md5_sum|checksum.sha256_sum",
            **result,
        )

    name = module.params.get("name")
    existing = _get_existing_bundle_by_name(module, api_instance, name)
    if existing is not None:
        result["ext_id"] = existing.ext_id
        result["response"] = strip_internal_attributes(existing.to_dict())
        result["skipped"] = True
        result["changed"] = False
        result["msg"] = (
            "LCM bundle with name '{0}' already exists. Skipping creation.".format(name)
        )
        return

    sg = SpecGenerator(module)
    default_spec = life_cycle_management_sdk.Bundle()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create LCM bundle spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_bundle(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating LCM bundle",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_data = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_data.to_dict())
        ext_id = get_entity_ext_id_from_task(task_data)
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_lcm_bundle(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for LCM Bundle"
                ),
                msg="Failed to get entity ext_id from task for LCM Bundle",
            )
    result["changed"] = True


def delete_Bundle(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "LCM bundle with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_bundle_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting LCM bundle",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
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
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }

    api_instance = get_bundles_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            module.fail_json(
                msg=(
                    "Update is not supported for LCM bundles. To modify a bundle, "
                    "delete the existing bundle with state=absent and re-create it."
                ),
                **result,
            )
        else:
            create_Bundle(module, result, api_instance)
    else:
        delete_Bundle(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
