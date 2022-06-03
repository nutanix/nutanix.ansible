#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402
from ..module_utils.prism.images import Image  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value, strip_extra_attrs_from_status  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    version = dict(
        product_version=dict(type="str", required=True),
        product_name=dict(type="str", required=True),
    )
    checksum = dict(
        checksum_algorithm=dict(type="str", required=True),
        checksum_value=dict(type="str", required=True),
    )
    module_args = dict(
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        source_uri=dict(type="str", required=False),
        source_path=dict(type="str", required=False),
        categories=dict(type="dict", required=False),
        image_type=dict(type="str", required=False, choices=["DISK_IMAGE", "ISO_IMAGE"], default="DISK_IMAGE"),
        version=dict(type="dict", options=version, required=False),
        architecture=dict(type="str", required=False),
        clusters=dict(type="list", elements="dict", mutually_exclusive=mutually_exclusive, options=entity_by_spec, required=False),
        project=dict(type="dict", mutually_exclusive=mutually_exclusive, options=entity_by_spec, required=False),
        owner=dict(type="dict", mutually_exclusive=mutually_exclusive, options=entity_by_spec, required=False),
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

        #upload image contents
        timeout = module.params.get("timeout", 600)
        image_upload = Image(module, upload_image=True)
        resp = image_upload.upload_image(image_uuid, source_path, timeout, raise_error=False)
        error = resp.get("error")
        if error:
            #delete the image metadata from PC
            image.delete(image_uuid)
            task.wait_for_completion(task_uuid)
            result["error"] = error
            result["changed"] = False
            result["response"] = None
            module.fail_json(msg="Failed uploading image contents", **result)
        resp = image.read(image_uuid)

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
        module.fail_json(msg="Failed deleting image", **result)
    result["image_uuid"] = image_uuid

    # read the current state of image
    resp = image.read(image_uuid)
    strip_extra_attrs_from_status(resp["status"], resp["spec"])
    resp["spec"] = resp.pop("status")

    # new spec for updating image
    update_spec, error = image.get_update_spec(resp)
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating Image update spec", **result)
        
    # check for idempotency
    if resp == update_spec:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change. Refer docs to check for fields which can be updated")

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
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name",)),
            ("state", "absent", ("image_uuid",)),
        ],
    )
    remove_param_with_none_value(module.params)
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
        elif module.params.get("source_uri") or module.params.get("source_path"):
            create_image(module, result)
        else:
            module.fail_json(msg="Provide source_path/source_uri to create new or image_uuid to update image", **result)
    elif state == "absent":
        delete_image(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
