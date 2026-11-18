#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_images_info_v2
short_description: Fetch LCM downloaded images info from Nutanix Prism Central.
version_added: "2.7.0"
description:
    - This module fetches information about LCM downloaded images available on the cluster.
    - It supports listing all images with optional filter, limit, page, orderby, select, and fetch_all.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List LCM Downloaded Images) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
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
- name: List all LCM downloaded images
  nutanix.ncp.ntnx_lcm_images_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List LCM downloaded images with filter
  nutanix.ncp.ntnx_lcm_images_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "entityClass eq 'Core Cluster'"
  register: result

- name: List LCM downloaded images with limit
  nutanix.ncp.ntnx_lcm_images_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: List all LCM downloaded images with fetch_all
  nutanix.ncp.ntnx_lcm_images_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching LCM downloaded image list.
        - List of LCM downloaded images available on the cluster.
    type: list
    returned: always
    sample:
        [
            {
                "cluster_ext_id": null,
                "entity_class": "PC CORE CLUSTER",
                "entity_model": "Nutanix Database Service",
                "entity_type": null,
                "entity_version": "3.0-EA",
                "ext_id": "1aefb501-b59a-46d4-8b56-4bd89d3e3f4b",
                "files": null,
                "hardware_family": null,
                "is_qualified": null,
                "links": null,
                "release_notes": null,
                "spec_version": null,
                "status": null,
                "tenant_id": null
            }
        ]
changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when there is an error
    type: str
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching LCM downloaded images info"
total_available_results:
    description: The total number of available LCM downloaded images in PC.
    type: int
    returned: when all LCM downloaded images are fetched
    sample: 10
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_lcm_images_api_instance  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict()
    return module_args


def get_lcm_images(module, api_instance, result):
    """List LCM downloaded images with pagination and filter support."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating LCM downloaded images info spec", **result
        )

    try:
        resp = list_entities(
            api_instance.list_images,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM downloaded images info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_lcm_images_api_instance(module)
    get_lcm_images(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
