#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_images
short_description: images module which supports pc images management CRUD operations
version_added: 1.3.0
description: "Create, Update, Delete images"
options:
    state:
        description:
        - Specify state
        - If C(state) is set to C(present) then the operation will be  create the item.
        - if C(state) is set to C(present) and C(image_uuid) is given then it will update that image.
        - if C(state) is set to C(present) then C(image_uuid), C(source_uri) and C(source_path) are mutually exclusive.
        - if C(state) is set to C(present) then C(image_uuid) or C(name) needs to be set.
        - If C(state) is set to C(absent) and if the item exists, then item is removed.
        choices:
        - present
        - absent
        type: str
        default: present
    wait:
        description: Wait for the  CRUD operation to complete.
        type: bool
        required: false
        default: True
    name:
        description: Image name
        required: false
        type: str
    image_uuid:
        description:
            - Image uuid
            - will be used to update if C(state) is C(present) and to delete if C(state) is C(absent)
        type: str
        required: false
    desc:
        description: A description for image
        required: false
        type: str
    source_uri:
        description:
            - Source URL for image
            - Mutually exclusive with C(source_path)
        required: false
        type: str
    source_path:
        description:
            - local image path
            - Mutually exclusive with C(source_uri)
        required: false
        type: str
    categories:
        description:
            - Categories for the image. This allows setting up multiple values from a single key.
            - this will override existing categories with mentioned during update
            - mutually_exclusive with C(remove_categories)
        required: false
        type: dict
    remove_categories:
        description:
            - set this flag to remove detach all categories attached to image
            - mutually_exclusive with C(categories)
        type: bool
        required: false
        default: false
    image_type:
        description: The type of image.
        required: false
        type: str
        choices:
            - ISO_IMAGE
            - DISK_IMAGE
    version:
        description: The image version, which is composed of a product name and product version.
        required: false
        type: dict
        suboptions:
            product_name:
                description: Name of the producer/distribution of the image. For example windows or red hat. <= 64 characters.
                type: str
                required: true
            product_version:
                description: Version string for the disk image. <= 64 characters
                type: str
                required: true
    clusters:
        description: Name or UUID of the cluster on which the image will be placed
        type: list
        elements: dict
        required: false
        suboptions:
            name:
                description:
                    - Cluster Name
                    - Mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - Cluster UUID
                    - Mutually exclusive with C(name)
                type: str
    checksum:
        description: Image checksum
        type: dict
        required: false
        suboptions:
            checksum_algorithm:
                description: checksum algorithm
                choices:
                    - SHA_1
                    - SHA_256
                type: str
                required: true
            checksum_value:
                description: checksum value
                type: str
                required: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: create image from local workstation
  ntnx_images:
    state: "present"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    source_path: "/Users/ubuntu/Downloads/alpine-virt-3.8.1-x86_64.iso"
    clusters:
      - name: "temp_cluster"
    categories:
      AppFamily:
        - Backup
    checksum:
      checksum_algorithm: SHA_1
      checksum_value: 44610efd741a3ab4a548a81ea94869bb8b692977
    name: "ansible-test-with-categories-mapping"
    desc: "description"
    image_type: "ISO_IMAGE"
    version:
      product_name: "test"
      product_version: "1.2.0"
    wait: true

- name: create image from with source as remote server file location
  ntnx_images:
    state: "present"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    source_uri: "https://cloud-images.ubuntu.com/releases/xenial/release/ubuntu-16.04-server-cloudimg-amd64-disk1.img"
    clusters:
      - name: "temp_cluster"
    categories:
      AppFamily:
        - Backup
    checksum:
      checksum_algorithm: SHA_1
      checksum_value: 44610efd741a3ab4a548a81ea94869bb8b692977
    name: "ansible-test-with-categories-mapping"
    desc: "description"
    image_type: "DISK_IMAGE"
    version:
      product_name: "test"
      product_version: "1.2.0"
    wait: true

- name: override categories of existing image
  ntnx_images:
    state: "present"
    image_uuid: "<image-uuid>"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    categories:
      AppTier:
        - Default
      AppFamily:
        - Backup
    wait: true

- name: dettach all categories from existing image
  ntnx_images:
    state: "present"
    image_uuid: "00000000-0000-0000-0000-000000000000"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    remove_categories: true
    wait: true

- name: delete existing image
  ntnx_images:
    state: "absent"
    image_uuid: "00000000-0000-0000-0000-000000000000"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    wait: true
"""

RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: The image kind metadata
  returned: always
  type: dict
  sample: {
                "categories": {
                    "AppFamily": "Backup"
                },
                "categories_mapping": {
                    "AppFamily": [
                        "Backup"
                    ]
                },
                "creation_time": "2022-06-09T10:13:38Z",
                "kind": "image",
                "last_update_time": "2022-06-09T10:37:14Z",
                "owner_reference": {
                    "kind": "user",
                    "name": "admin",
                    "uuid": "00000000-0000-0000-0000-000000000000"
                },
                "spec_hash": "00000000000000000000000000000000000000000000000000",
                "spec_version": 14,
                "uuid": "00000000-0000-0000-0000-000000000000"
            }
spec:
  description: An intentful representation of a image spec
  returned: always
  type: dict
  sample: {
                "description": "check123",
                "name": "update_name",
                "resources": {
                    "architecture": "X86_64",
                    "image_type": "ISO_IMAGE",
                    "source_uri": "http://dl-cdn.alpinelinux.org/alpine/v3.8/releases/x86_64/alpine-virt-3.8.1-x86_64.iso",
                    "version": {
                        "product_name": "test",
                        "product_version": "1.2.0"
                    }
                }
            }
status:
  description: An intentful representation of a image status
  returned: always
  type: dict
  sample: {
                "description": "check123",
                "execution_context": {
                    "task_uuid": [
                        "00000000-0000-0000-0000-000000000000"
                    ]
                },
                "name": "update_name",
                "resources": {
                    "architecture": "X86_64",
                    "current_cluster_reference_list": [
                        {
                            "kind": "cluster",
                            "uuid": "00000000-0000-0000-0000-000000000000"
                        }
                    ],
                    "image_type": "ISO_IMAGE",
                    "retrieval_uri_list": [
                        "<retrieval_uri>"
                    ],
                    "size_bytes": 33554432,
                    "source_uri": "http://dl-cdn.alpinelinux.org/alpine/v3.8/releases/x86_64/alpine-virt-3.8.1-x86_64.iso",
                    "version": {
                        "product_name": "test",
                        "product_version": "1.2.0"
                    }
                },
                "state": "COMPLETE"
            }
image_uuid:
  description: The created image uuid
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.v3.prism.images import Image  # noqa: E402
from ..module_utils.v3.prism.tasks import Task  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    version = dict(
        product_version=dict(type="str", required=True),
        product_name=dict(type="str", required=True),
    )
    checksum = dict(
        checksum_algorithm=dict(
            type="str", required=True, choices=["SHA_1", "SHA_256"]
        ),
        checksum_value=dict(type="str", required=True),
    )
    module_args = dict(
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        source_uri=dict(type="str", required=False),
        source_path=dict(type="str", required=False),
        remove_categories=dict(type="bool", required=False, default=False),
        categories=dict(type="dict", required=False),
        image_type=dict(
            type="str",
            required=False,
            choices=["DISK_IMAGE", "ISO_IMAGE"],
        ),
        version=dict(type="dict", options=version, required=False),
        clusters=dict(
            type="list",
            elements="dict",
            mutually_exclusive=mutually_exclusive,
            options=entity_by_spec,
            required=False,
        ),
        checksum=dict(type="dict", options=checksum, required=False),
        image_uuid=dict(type="str", required=False),
    )
    return module_args


def create_image(module, result):
    image = Image(module)
    spec, error = image.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating create Image Spec", **result)
    if module.check_mode:
        result["response"] = spec
        return

    # create image
    resp = image.create(spec)
    image_uuid = resp["metadata"]["uuid"]
    task_uuid = resp["status"]["execution_context"]["task_uuid"]
    result["image_uuid"] = image_uuid
    result["changed"] = True

    # upload image if source_path is given
    source_path = module.params.get("source_path", "")
    task = Task(module)

    if source_path:
        # wait for image create to finish
        task.wait_for_completion(task_uuid)

        # upload image contents
        timeout = module.params.get("timeout", 600)
        image_upload_obj = Image(module, upload_image=True)
        resp = image_upload_obj.upload_image(
            image_uuid, source_path, timeout, raise_error=False
        )
        error = resp.get("error")
        if error:
            # delete the image metadata from PC
            image_upload_obj.delete(image_uuid)
            task.wait_for_completion(task_uuid)
            result["error"] = error
            result["changed"] = False
            result["response"] = None
            module.fail_json(msg="Failed uploading image contents", **result)
        resp = image_upload_obj.read(image_uuid)

    elif module.params.get("wait"):
        task.wait_for_completion(task_uuid)
        # get the image
        resp = image.read(image_uuid)

    result["response"] = resp


def update_image(module, result):
    image = Image(module)
    image_uuid = module.params.get("image_uuid")
    if not image_uuid:
        result["error"] = "Missing parameter image_uuid in playbook"
        module.fail_json(msg="Failed updating image", **result)
    result["image_uuid"] = image_uuid

    # read the current state of image
    resp = image.read(image_uuid)
    utils.strip_extra_attrs(resp["status"], resp["spec"])
    resp["spec"] = resp.pop("status")

    # new spec for updating image
    update_spec, error = image.get_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating Image update spec", **result)

    # check for idempotency
    if resp == update_spec:
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. Refer docs to check for fields which can be updated"
        )

    if module.check_mode:
        result["response"] = update_spec
        return

    # update image
    resp = image.update(update_spec, uuid=image_uuid)
    task_uuid = resp["status"]["execution_context"]["task_uuid"]

    # wait for image update to finish
    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        # get the image
        resp = image.read(image_uuid)

    result["changed"] = True
    result["response"] = resp


def delete_image(module, result):
    uuid = module.params["image_uuid"]
    if not uuid:
        result["error"] = "Missing parameter image_uuid"
        module.fail_json(msg="Failed deleting Image", **result)

    image = Image(module)
    resp = image.delete(uuid)
    result["response"] = resp
    result["changed"] = True
    task_uuid = resp["status"]["execution_context"]["task_uuid"]

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)


def run_module():
    # mutually_exclusive_list have params which are not allowed together
    # we cannot update source_uri, source_path, checksum and clusters.
    mutually_exclusive_list = [
        ("image_uuid", "source_uri", "source_path"),
        ("image_uuid", "checksum"),
        ("image_uuid", "clusters"),
        ("categories", "remove_categories"),
    ]
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("source_uri", "source_path", "image_uuid"), True),
            ("state", "present", ("name", "image_uuid"), True),
            ("state", "absent", ("image_uuid",)),
        ],
        mutually_exclusive=mutually_exclusive_list,
    )
    utils.remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "image_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        if module.params.get("image_uuid"):
            update_image(module, result)
        else:
            create_image(module, result)
    elif state == "absent":
        delete_image(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
