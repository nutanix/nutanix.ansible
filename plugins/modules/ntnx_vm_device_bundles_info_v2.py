#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_device_bundles_info_v2
short_description: Fetch device bundle info for a VM
version_added: "2.7.0"
description:
    - This module allows you to fetch information about device bundles in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific device bundle attached to the VM.
    - If C(ext_id) is not provided, list multiple device bundles optionally filtered or paginated.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get a Device Bundle attached to a VM) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List Device Bundles attached to a VM) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=virtual_machine_management)"
options:
    ext_id:
        description:
            - The external ID of the device bundle of type UUID.
        type: str
    vm_ext_id:
        description:
            - A globally unique identifier of a VM of type UUID.
        type: str
        required: true
    page:
        description:
            - A URL query parameter that specifies the page number of the result set.
            - It must be a positive integer between 0 and the maximum number of pages that are available for that resource.
            - Any number out of this range might lead to no results.
        type: int
        required: false
    limit:
        description:
            - A URL query parameter that specifies the total number of records returned in the result set.
            - Must be a positive integer between 1 and 100.
            - Any number out of this range will lead to a validation error.
            - If the limit is not provided, a default value of 50 records will be returned in the result set.
        type: int
        required: false
    filter:
        description:
            - A URL query parameter that allows clients to filter a collection of resources.
            - The expression specified with $filter is evaluated for each resource in the
              collection, and only items where the expression evaluates to true are
              included in the response.
        type: str
        required: false
    orderby:
        description:
            - A URL query parameter that allows clients to specify the sort criteria for
              the returned list of objects.
            - Resources can be sorted in ascending order using asc or descending order
              using desc.
        type: str
        required: false
    read_timeout:
        description: Read timeout in milliseconds for API calls.
        type: int
        required: false
        default: 30000
    fetch_all:
        description:
            - When C(true), paginate through the list API until all available entities are returned.
              C(page) and C(limit) are ignored; each request uses the maximum page size (100).
            - When C(false), return a single page (API default limit).
            - Does not apply when fetching a single entity by C(ext_id).
        type: bool
        required: false
        default: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get a specific device bundle attached to a VM
  nutanix.ncp.ntnx_vm_device_bundles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "00000000-0000-0000-0000-000000000001"
    ext_id: "00000000-0000-0000-0000-000000000002"
  register: result

- name: List all device bundles attached to a VM
  nutanix.ncp.ntnx_vm_device_bundles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "00000000-0000-0000-0000-000000000001"
  register: result

- name: List device bundles attached to a VM with filter
  nutanix.ncp.ntnx_vm_device_bundles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "00000000-0000-0000-0000-000000000001"
    filter: "extId eq '00000000-0000-0000-0000-000000000002'"
  register: result

- name: List device bundles attached to a VM with limit
  nutanix.ncp.ntnx_vm_device_bundles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "00000000-0000-0000-0000-000000000001"
    limit: 1
  register: result

- name: List all device bundles attached to a VM with fetch_all
  nutanix.ncp.ntnx_vm_device_bundles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "00000000-0000-0000-0000-000000000001"
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix VM device bundles info v4 API.
        - It can be a single device bundle if External ID is provided.
        - List of multiple device bundles if External ID is not provided with optional filter, limit, or fetch_all.
    returned: always
    type: dict
    sample:
        {
            "backing_info": {
                "assigned_instance_info": null,
                "device_bundle_profile": {
                    "ext_id": "b2c3d4e5-6789-0abc-def1-234567890bcd"
                }
            },
            "ext_id": "c3d4e5f6-7890-abcd-ef12-34567890cdef",
            "links": null,
            "tenant_id": null
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
    sample: "Api Exception raised while fetching VM device bundles info"
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    returned: when an error occurs
    type: str
failed:
    description: This indicates whether the task failed.
    returned: always
    type: bool
    sample: false
ext_id:
    description: The external ID of the device bundle.
    returned: when external ID is provided
    type: str
    sample: "c3d4e5f6-7890-abcd-ef12-34567890cdef"
vm_ext_id:
    description: The external ID of the VM.
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000001"
total_available_results:
    description: The total number of available device bundles attached to the VM.
    returned: when all device bundles are fetched
    type: int
    sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_device_bundle  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        vm_ext_id=dict(type="str", required=True),
        page=dict(type="int"),
        limit=dict(type="int"),
        filter=dict(type="str"),
        orderby=dict(type="str"),
        fetch_all=dict(type="bool", required=False, default=False),
    )
    return module_args


def get_device_bundle_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id
    bundle = get_device_bundle(module, api_instance, vm_ext_id, ext_id)
    result["response"] = strip_internal_attributes(bundle.to_dict())


def get_device_bundles(module, api_instance, result):
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VM device bundles info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_device_bundles_by_vm_id,
            kwargs=kwargs,
            vmExtId=vm_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM device bundles info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        skip_info_args=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vm_api_instance(module)
    if module.params.get("ext_id"):
        get_device_bundle_using_ext_id(module, api_instance, result)
    else:
        get_device_bundles(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
