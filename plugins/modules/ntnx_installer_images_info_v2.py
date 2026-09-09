#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_installer_images_info_v2
short_description: Fetch LCM installer images info from Nutanix Foundation Central (FCVM)
version_added: 2.7.0
description:
  - This module allows you to fetch information about LCM installer images.
  - If C(ext_id) is provided, fetch a particular installer image using its external ID.
  - If C(ext_id) is not provided, fetch multiple installer images with/without using filters, limit, etc.
  - This module uses v4 API based SDKs.
notes:
  - This module talks to B(Foundation Central (FCVM)), B(not) Prism Central.
    The C(nutanix_host), C(nutanix_username), C(nutanix_password) and
    C(nutanix_port) parameters MUST point to the FCVM/Foundation endpoint.
  - The installer images APIs are served under C(/api/lifecycle/v4.3/config/images)
    and are not available on Prism Central.
  - >-
    B(Get installer image(s)) -
    Requires an administrator role on Foundation Central.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  ext_id:
    description:
      - The external ID of the installer image.
      - If provided, the module fetches a single installer image.
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
- name: Get installer image using ext_id
  nutanix.ncp.ntnx_installer_images_info_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ foundation_username }}"
    nutanix_password: "{{ foundation_password }}"
    validate_certs: false
    ext_id: "d1f27805-4ce3-9212-2ca4-e4b4d258fe9c"
  register: result
  ignore_errors: true

- name: List all installer images
  nutanix.ncp.ntnx_installer_images_info_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ foundation_username }}"
    nutanix_password: "{{ foundation_password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List installer images with filter
  nutanix.ncp.ntnx_installer_images_info_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ foundation_username }}"
    nutanix_password: "{{ foundation_password }}"
    validate_certs: false
    filter: "name eq 'ahv_image_ansible'"
  register: result
  ignore_errors: true

- name: List installer images with limit
  nutanix.ncp.ntnx_installer_images_info_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ foundation_username }}"
    nutanix_password: "{{ foundation_password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix installer images info v4 API. The host is
      B(FCVM/Foundation) (not Prism Central).
    - It can be a single installer image if external ID is provided.
    - List of multiple installer images if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "certificate_chain": null,
      "checksum": {
          "hex_digest": "a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90"
      },
      "created_time": "2026-09-09T05:50:00.000000+00:00",
      "ext_id": "d1f27805-4ce3-9212-2ca4-e4b4d258fe9c",
      "file_status": "URL_AVAILABLE",
      "links": null,
      "metadata_download_url": "https://download.example.com/ahv/metadata.json",
      "metadata_status": "NOT_AVAILABLE",
      "name": "ahv_image_ansible",
      "source": "REMOTE_URL",
      "tenant_id": null,
      "type": "AHV",
      "url": "https://download.example.com/ahv/host-bundle-el8.nutanix.20230302.el8.x86_64.tar.gz",
      "version": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always False for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the installer image.
  returned: when external ID is provided
  type: str
  sample: "d1f27805-4ce3-9212-2ca4-e4b4d258fe9c"

msg:
  description: This indicates the status/error message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching installer images info"

error:
  description: This field typically holds information about any error that occurred during the task execution.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false

total_available_results:
  description: The total number of available installer images.
  returned: when all installer images are fetched
  type: int
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_installer_images_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_installer_image  # noqa: E402
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


def get_installer_image_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_installer_image(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_installer_images(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating installer images info spec", **result)

    try:
        resp = api_instance.list_images(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching installer images info",
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
    api_instance = get_installer_images_api_instance(module)
    if module.params.get("ext_id"):
        get_installer_image_using_ext_id(module, api_instance, result)
    else:
        get_installer_images(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
