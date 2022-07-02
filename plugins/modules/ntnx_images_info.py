#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_images_info
short_description: images info module
version_added: 1.3.0
description: 'Get images info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: image
    image_uuid:
        description:
            - image UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
  - name: List images using name filter criteria
    ntnx_images_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
        - name: Ubuntu
    register: result
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: Metadata for images list output
  returned: always
  type: dict
  sample: {
                "filter": "name==Ubuntu",
                "kind": "image",
                "length": 2,
                "offset": 0,
                "total_matches": 2
            }
entities:
  description: images intent response
  returned: always
  type: list
  sample: [
                {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "creation_time": "2022-06-09T12:44:17Z",
                        "kind": "image",
                        "last_update_time": "2022-06-09T12:44:21Z",
                        "owner_reference": {
                            "kind": "user",
                            "name": "admin",
                            "uuid": "00000000-0000-0000-0000-000000000000"
                        },
                        "spec_hash": "00000000000000000000000000000000000000000000000000",
                        "spec_version": 1,
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec": {
                        "description": "adasdasdsad",
                        "name": "Ubuntu",
                        "resources": {
                            "architecture": "X86_64",
                            "image_type": "DISK_IMAGE",
                            "source_uri": "<source-uri>"
                        }
                    },
                    "status": {
                        "description": "adasdasdsad",
                        "execution_context": {
                            "task_uuid": [
                                "00000000-0000-0000-0000-000000000000"
                            ]
                        },
                        "name": "Ubuntu",
                        "resources": {
                            "architecture": "X86_64",
                            "current_cluster_reference_list": [
                                {
                                    "kind": "cluster",
                                    "uuid": "00000000-0000-0000-0000-000000000000"
                                }
                            ],
                            "image_type": "DISK_IMAGE",
                            "retrieval_uri_list": [
                                "<retrieval-source-uri>"
                            ],
                            "size_bytes": 33554432,
                            "source_uri": "<source-uri>"
                        },
                        "state": "COMPLETE"
                    }
                },
                {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "creation_time": "2022-06-09T12:44:28Z",
                        "kind": "image",
                        "last_update_time": "2022-06-09T12:44:33Z",
                        "owner_reference": {
                            "kind": "user",
                            "name": "admin",
                            "uuid": "00000000-0000-0000-0000-000000000000"
                        },
                        "spec_hash": "00000000000000000000000000000000000000000000000000",
                        "spec_version": 1,
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec": {
                        "description": "adasdasd",
                        "name": "Ubuntu",
                        "resources": {
                            "architecture": "X86_64",
                            "image_type": "DISK_IMAGE",
                            "source_uri": "<ssource-uri>"
                        }
                    },
                    "status": {
                        "description": "adasdasd",
                        "execution_context": {
                            "task_uuid": [
                                "00000000-0000-0000-0000-000000000000"
                            ]
                        },
                        "name": "Ubuntu",
                        "resources": {
                            "architecture": "X86_64",
                            "current_cluster_reference_list": [
                                {
                                    "kind": "cluster",
                                    "uuid": "00000000-0000-0000-0000-000000000000"
                                }
                            ],
                            "image_type": "DISK_IMAGE",
                            "retrieval_uri_list": [
                                "<retrieval-uri>"
                            ],
                            "size_bytes": 33554432,
                            "source_uri": "<source-uri>"
                        },
                        "state": "COMPLETE"
                    }
                }
            ]

"""


from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.images import Image  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        image_uuid=dict(type="str"),
        kind=dict(type="str", default="image"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_image(module, result):
    image = Image(module)
    uuid = module.params.get("image_uuid")
    resp = image.read(uuid)
    result["response"] = resp


def get_images(module, result):
    image = Image(module)
    spec, err = image.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Image info Spec", **result)
    resp = image.list(spec)
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
        mutually_exclusive=[
            ("image_uuid", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("image_uuid"):
        get_image(module, result)
    else:
        get_images(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
