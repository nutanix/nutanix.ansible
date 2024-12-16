#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_images_info_v2
short_description: Fetch information about Nutanix images
description:
  - This module fetches information about Nutanix images.
  - The module can fetch information about all images or a specific image.
version_added: "2.0.0"
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
  ext_id:
    description:
      - The external ID of the image.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
- name: Fetch information about all images
  nutanix.ncp.ntnx_images_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: Fetch information about a specific image
  nutanix.ncp.ntnx_images_info_v2:
    ext_id: abc123
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
"""


RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Images.
    - it can be single image or list of image as per spec.
  type: dict
  returned: always
  sample: {
            "category_ext_ids": [
                "98b9dc89-be08-3c56-b554-692b8b676fd1"
            ],
            "checksum": null,
            "cluster_location_ext_ids": [
                "00061413-990f-363a-185b-ac1f6b6f97e2"
            ],
            "create_time": "2024-03-25T19:28:55.724068+00:00",
            "description": "from disk",
            "ext_id": "172e0d73-74ee-4d05-95f2-1894d83d7e09",
            "last_update_time": "2024-03-25T19:28:55.724068+00:00",
            "links": null,
            "name": "image1_from_disk",
            "owner_ext_id": "00000000-0000-0000-0000-000000000000",
            "placement_policy_status": null,
            "size_bytes": 262472192,
            "source": {
                "ext_id": "05de8919-3e8c-4f5c-a9e4-a6955cedd764"
            },
            "tenant_id": null,
            "type": "DISK_IMAGE"
        }
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_image_api_instance  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_image(module, result):
    images = get_image_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = images.get_image_by_id(ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching image info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_images(module, result):
    images = get_image_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating images info Spec", **result)

    try:
        resp = images.list_images(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching images info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_image(module, result)
    else:
        get_images(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
