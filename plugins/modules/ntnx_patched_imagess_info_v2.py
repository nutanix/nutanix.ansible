#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_patched_imagess_info_v2
short_description: Fetch Life Cycle Management (LCM) patched images info
version_added: 2.7.0
description:
  - This module allows you to fetch information about patched hypervisor or host
    OS images in Nutanix Life Cycle Management (LCM).
  - If C(ext_id) is provided, a single patched image is fetched using its external ID.
  - If C(ext_id) is not provided, a list of patched images is fetched, optionally
    filtered/limited.
  - This module uses v4 APIs based SDKs.
notes:
  - The patched images APIs are part of the Life Cycle Management (LCM) namespace
    and are served by Foundation Central (FCVM), NOT by Prism Central (PC).
    Set C(nutanix_host) to the Foundation Central (FCVM) endpoint.
  - This module requires the appropriate administrative role on Foundation Central
    to be assigned to the user performing the operation.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  ext_id:
    description:
      - The external ID of the patched image.
      - If provided, the module fetches a single patched image.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get patched image using ext_id
  nutanix.ncp.ntnx_patched_imagess_info_v2:
    nutanix_host: "{{ fcvm_ip }}"
    nutanix_username: "{{ fcvm_username }}"
    nutanix_password: "{{ fcvm_password }}"
    validate_certs: false
    ext_id: "b6c8f0a2-4d1e-4f0a-9c1a-2d3e4f5a6b7c"
  register: result
  ignore_errors: true

- name: List all patched images
  nutanix.ncp.ntnx_patched_imagess_info_v2:
    nutanix_host: "{{ fcvm_ip }}"
    nutanix_username: "{{ fcvm_username }}"
    nutanix_password: "{{ fcvm_password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List patched images with filter
  nutanix.ncp.ntnx_patched_imagess_info_v2:
    nutanix_host: "{{ fcvm_ip }}"
    nutanix_username: "{{ fcvm_username }}"
    nutanix_password: "{{ fcvm_password }}"
    validate_certs: false
    filter: "name eq 'ahv_patched_image_ansible'"
  register: result
  ignore_errors: true

- name: List patched images with limit
  nutanix.ncp.ntnx_patched_imagess_info_v2:
    nutanix_host: "{{ fcvm_ip }}"
    nutanix_username: "{{ fcvm_username }}"
    nutanix_password: "{{ fcvm_password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix patched images info v4 API.
    - This host may be Foundation Central (FCVM), not Prism Central.
    - It can be a single patched image if the external ID is provided.
    - It can be a list of multiple patched images if the external ID is not
      provided, with an optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "claim_token_ext_id": "5f1b1b3a-1b3a-4b3a-8b3a-1b3a4b3a8b3a",
      "created_time": "2026-09-09T04:38:00.000000+00:00",
      "ext_id": "b6c8f0a2-4d1e-4f0a-9c1a-2d3e4f5a6b7c",
      "host_type": "AHV",
      "image_details": {
        "ext_id": "b6c8f0a2-4d1e-4f0a-9c1a-2d3e4f5a6b7c"
      },
      "links": null,
      "name": "ahv_patched_image_ansible",
      "node_configurations": [
        {
          "host_configuration": {
            "hostname": "ahv-host-01"
          },
          "node_ext_id": "c1d2e3f4-a5b6-4c7d-8e9f-0a1b2c3d4e5f"
        }
      ],
      "owner_ext_id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
      "patched_iso_sha256_checksum": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "patched_iso_url": "https://example.com/isos/ahv-patched.iso",
      "tenant_id": null,
      "version": "10.0"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching patched images info"

error:
  description: This field holds information about errors that occurred during task execution.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false

ext_id:
  description: External ID of the patched image.
  returned: when the external ID is provided
  type: str
  sample: "b6c8f0a2-4d1e-4f0a-9c1a-2d3e4f5a6b7c"

total_available_results:
  description: The total number of available patched images.
  returned: when all patched images are fetched
  type: int
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_patched_images_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_patched_image  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_patched_image_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_patched_image(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_patched_images(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating patched images info spec", **result)

    try:
        resp = api_instance.list_patched_images(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching patched images info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_patched_images_api_instance(module)
    if module.params.get("ext_id"):
        get_patched_image_using_ext_id(module, api_instance, result)
    else:
        get_patched_images(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
