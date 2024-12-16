#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_images_v2
short_description: Manage Nutanix Prism Central images.
description:
    - This module allows you to create, update, and delete images in Nutanix.
version_added: "2.0.0"
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then the operation will be  create the item.
            - if C(state) is set to C(present) and C(ext_id) is given then it will update that image.
            - if C(state) is set to C(present) then C(ext_id) or C(name) needs to be set.
            - >-
                If C(state) is set to C(absent) and if the item exists, then
                item is removed.
        choices:
            - present
            - absent
        type: str
        default: present
    wait:
        description: Wait for the CRUD operation to complete.
        type: bool
        required: false
        default: True
    ext_id:
        description:
            - The unique identifier of the image.
            - Required to do update and delete.
        type: str
        required: false
    name:
        description:
            - The name of the image.
        type: str
        required: false
    description:
        description:
            - The description of the image.
        type: str
        required: false
    type:
        description:
            - The type of the image.
        type: str
        choices:
            - DISK_IMAGE
            - ISO_IMAGE
        required: false
    checksum:
        description:
            - The checksum of the image.
            - C(sha1) and C(sha256) are mutually exclusive.
        type: dict
        suboptions:
            sha1:
                description:
                    - The SHA1 checksum of the image.
                type: dict
                suboptions:
                    hex_digest:
                        description:
                            - The hexadecimal digest of the SHA1 checksum.
                        type: str
                        required: true
            sha256:
                description:
                    - The SHA256 checksum of the image.
                type: dict
                suboptions:
                    hex_digest:
                        description:
                            - The hexadecimal digest of the SHA256 checksum.
                        type: str
                        required: true
        required: false
    source:
        description:
            - The source of the image.
            - Required to create an image.
            - C(url_source) and C(vm_disk_source) are mutually exclusive.
        type: dict
        suboptions:
            url_source:
                description:
                    - The URL source of the image and its config.
                type: dict
                suboptions:
                    url:
                        description:
                            - The URL of the image.
                        type: str
                        required: true
                    should_allow_insecure_url:
                        description:
                            - Whether to allow insecure URLs.
                        type: bool
                        required: false
                        default: false
                    basic_auth:
                        description:
                            - The basic authentication credentials for the URL source.
                        type: dict
                        suboptions:
                            username:
                                description:
                                    - The username for basic authentication.
                                type: str
                                required: true
                            password:
                                description:
                                    - The password for basic authentication.
                                type: str
                                required: true
            vm_disk_source:
                description:
                    - The VM disk source of the image.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - The unique identifier of the VM disk.
                        type: str
                        required: true
        required: false
    category_ext_ids:
        description:
            - The list of category key-value external IDs to be associated with the image.
            - Use `[]` to remove all category key-value external IDs.
        type: list
        elements: str
        required: false
    cluster_location_ext_ids:
        description:
            - The list of cluster location external IDs for placing the images.
            - Required to create an image.
        type: list
        elements: str
        required: false
    tenant_id:
        description:
            - The tenant ID to be associated with the image.
        type: str
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
- name: Create an image
  nutanix.ncp.ntnx_images_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: my-image
    description: My image
    type: DISK_IMAGE
    checksum:
      sha1:
        hex_digest: abcdef1234567890
    source:
      url_source:
        url: http://example.com/image.qcow2
        should_allow_insecure_url: true
        basic_auth:
          username: myuser
          password: mypassword
    category_ext_ids:
      - category1
      - category2
    cluster_location_ext_ids:
      - cluster1
      - cluster2
    tenant_id: tenant1
    state: present

- name: Update an image
  nutanix.ncp.ntnx_images_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: 98b9dc89-be08-3c56-b554-692b8b676fd1
    name: updated-image
    description: Updated image
    state: present

- name: Delete an image
  nutanix.ncp.ntnx_images_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: 98b9dc89-be08-3c56-b554-692b8b676fd1
    state: absent
"""

RETURN = r"""
response:
    description:
        - The response from CRUD operation.
        - For delete, it returns task response data.
        - If update operation is idempotent, it skips the update.
    type: dict
    returned: always
    sample: {
            "category_ext_ids": null,
            "checksum": null,
            "cluster_location_ext_ids": [
                "00061413-990f-363a-185b-ac1f6b6f97e2"
            ],
            "create_time": "2024-03-25T19:18:16.547125+00:00",
            "description": "image1-updated1",
            "ext_id": "015e6709-d4a6-44bd-8df7-9898f062635b",
            "last_update_time": "2024-03-25T19:37:02.628625+00:00",
            "links": null,
            "name": "image1-updated1",
            "owner_ext_id": "00000000-0000-0000-0000-000000000000",
            "placement_policy_status": null,
            "size_bytes": 262472192,
            "source": {
                "basic_auth": null,
                "should_allow_insecure_url": false,
                "url": "http://example.com/image.qcow2"
            },
            "tenant_id": null,
            "type": "DISK_IMAGE"
        }
task_ext_id:
    description: The task external ID associated with the operation.
    type: str
    sample: "015e6709-d4a6-44bd-8df7-9898f062635b"
    returned: always
ext_id:
    description: The external ID of the image.
    type: str
    returned: always
changed:
    description: Indicates whether the state of the image was changed.
    type: bool
    returned: always
skipped:
    description: Indicates whether the image was skipped due to idempotency.
    type: bool
    returned: always
error:
    description: The error message, if any.
    type: str
    returned: always
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks  # noqa: E402
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
    get_etag,
    get_image_api_instance,
)

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    # maps of spec classes for attributes having more than one type of objects allowed as it value
    checksum_allowed_objs = {
        "sha1": vmm_sdk.ImageSha1Checksum,
        "sha256": vmm_sdk.ImageSha256Checksum,
    }
    source_allowed_objs = {
        "url_source": vmm_sdk.UrlSource,
        "vm_disk_source": vmm_sdk.VmDiskSource,
    }

    # module specs
    hex_digest = dict(hex_digest=dict(type="str", required=True))
    checksum = dict(
        sha1=dict(type="dict", options=hex_digest),
        sha256=dict(type="dict", options=hex_digest),
    )
    basic_auth = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )
    vm_disk_source = dict(ext_id=dict(type="str", required=True))
    url_source = dict(
        url=dict(type="str", required=True),
        should_allow_insecure_url=dict(type="bool", default=False),
        basic_auth=dict(type="dict", options=basic_auth, obj=vmm_sdk.UrlBasicAuth),
    )
    source = dict(
        url_source=dict(type="dict", options=url_source),
        vm_disk_source=dict(type="dict", options=vm_disk_source),
    )
    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        type=dict(type="str", choices=["DISK_IMAGE", "ISO_IMAGE"]),
        checksum=dict(
            type="dict",
            options=checksum,
            obj=checksum_allowed_objs,
            mutually_exclusive=[("sha1", "sha256")],
        ),
        source=dict(
            type="dict",
            options=source,
            obj=source_allowed_objs,
            mutually_exclusive=[("url_source", "vm_disk_source")],
        ),
        category_ext_ids=dict(type="list", elements="str"),
        cluster_location_ext_ids=dict(type="list", elements="str"),
        tenant_id=dict(type="str"),
    )
    return module_args


def get_image(module, api_instance, ext_id):
    try:
        return api_instance.get_image_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching image info using ext_id",
        )


def create_image(module, result):
    images = get_image_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.Image()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create Image Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = images.create_image(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Image",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        ext_id = get_entity_ext_id_from_task(task, rel=Tasks.RelEntityType.IMAGES)
        if ext_id:
            resp = get_image(module, images, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    if current_spec == update_spec:
        return True
    return False


def update_image(module, result):
    images = get_image_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_image(module, images, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating image update spec", **result)

    # check for idempotency
    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = images.update_image_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating image",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["ext_id"] = ext_id
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id, True)
        resp = get_image(module, images, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_image(module, result):
    images = get_image_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_image(module, images, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("unable to fetch etag for deleting image", **result)

    kwargs = {"if_match": etag}

    try:
        resp = images.delete_image_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting image",
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
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
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
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_image(module, result)
        else:
            create_image(module, result)
    else:
        delete_image(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
